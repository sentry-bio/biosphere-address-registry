"""Filesystem content-addressed store with logged human-readable refs."""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Mapping

from .identity import with_content_id
from .validation import load_json, require_valid


class RegistryError(RuntimeError):
    pass


class Registry:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.objects = self.root / "objects" / "sha256"
        self.refs = self.root / "refs"
        self.events = self.root / "events.jsonl"

    def initialize(self) -> None:
        self.objects.mkdir(parents=True, exist_ok=True)
        self.refs.mkdir(parents=True, exist_ok=True)
        if not self.events.exists():
            self.events.touch()

    def _require_initialized(self) -> None:
        if not self.objects.is_dir() or not self.refs.is_dir():
            raise RegistryError(f"not a BAR registry: {self.root}")

    def object_path(self, object_id: str) -> Path:
        if not object_id.startswith("sha256:") or len(object_id) != 71:
            raise RegistryError(f"invalid object id: {object_id}")
        digest = object_id.split(":", 1)[1]
        return self.objects / digest[:2] / f"{digest[2:]}.json"

    @staticmethod
    def _write_atomic(path: Path, data: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, name = tempfile.mkstemp(prefix=".bar-", dir=path.parent)
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            os.replace(name, path)
        finally:
            if os.path.exists(name):
                os.unlink(name)

    def put(
        self,
        source: Mapping[str, Any] | str | Path,
        *,
        ref: str | None = None,
    ) -> dict[str, Any]:
        self._require_initialized()
        value = load_json(source) if isinstance(source, (str, Path)) else dict(source)
        obj = with_content_id(value)
        require_valid(obj, require_id=True)
        path = self.object_path(obj["content_id"])
        encoded = (
            json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
        ).encode("utf-8")
        created = not path.exists()
        if created:
            self._write_atomic(path, encoded)
        if ref is not None:
            self.update_ref(ref, obj["content_id"])
        self._event("put", obj["content_id"], ref=ref, created=created)
        return obj

    def get(self, object_id_or_ref: str) -> dict[str, Any]:
        self._require_initialized()
        object_id = (
            object_id_or_ref
            if object_id_or_ref.startswith("sha256:")
            else self.resolve_ref(object_id_or_ref)
        )
        path = self.object_path(object_id)
        if not path.exists():
            raise RegistryError(f"object not found: {object_id}")
        obj = load_json(path)
        require_valid(obj, require_id=True)
        return obj

    def update_ref(self, name: str, object_id: str) -> None:
        self._require_initialized()
        if name.startswith("/") or ".." in Path(name).parts:
            raise RegistryError("ref must be a relative safe path")
        if not self.object_path(object_id).exists():
            raise RegistryError(f"cannot point ref to missing object: {object_id}")
        path = self.refs / name
        self._write_atomic(path, (object_id + "\n").encode("ascii"))
        self._event("update-ref", object_id, ref=name)

    def resolve_ref(self, name: str) -> str:
        path = self.refs / name
        if not path.exists():
            raise RegistryError(f"ref not found: {name}")
        return path.read_text(encoding="ascii").strip()

    def iter_objects(self) -> Iterator[tuple[str, Path]]:
        self._require_initialized()
        for path in sorted(self.objects.glob("*/*.json")):
            digest = path.parent.name + path.stem
            yield "sha256:" + digest, path

    @staticmethod
    def linked_objects(obj: Mapping[str, Any]) -> list[str]:
        """Return BAR object links whose targets should exist in one registry."""

        payload = obj.get("payload", {})
        if not isinstance(payload, Mapping):
            return []
        record_type = obj.get("record_type")
        scalar_fields = {
            "map-edition": ["reference_manifest_id"],
            "evidence": ["observation_id", "map_edition_id"],
            "transform": ["map_edition_id", "form_id"],
            "address": [
                "evidence_id",
                "map_edition_id",
                "form_id",
                "transform_id",
            ],
            "interpretation": ["evidence_id"],
        }
        list_fields = {
            "organism-record": [
                "observations",
                "evidence",
                "addresses",
                "interpretations",
            ]
        }
        links = [
            payload[field]
            for field in scalar_fields.get(str(record_type), [])
            if isinstance(payload.get(field), str)
        ]
        for field in list_fields.get(str(record_type), []):
            value = payload.get(field, [])
            if isinstance(value, list):
                links.extend(item for item in value if isinstance(item, str))
        return [item for item in links if item.startswith("sha256:")]

    def verify(self, *, graph: bool = False) -> dict[str, Any]:
        self._require_initialized()
        errors: list[str] = []
        count = 0
        objects: list[dict[str, Any]] = []
        for expected, path in self.iter_objects():
            count += 1
            try:
                obj = load_json(path)
                require_valid(obj, require_id=True)
                objects.append(obj)
                if obj["content_id"] != expected:
                    errors.append(f"path/id mismatch: {path}")
            except Exception as exc:  # verification reports every corrupt object
                errors.append(f"{path}: {exc}")
        ref_count = 0
        for path in sorted(p for p in self.refs.rglob("*") if p.is_file()):
            ref_count += 1
            target = path.read_text(encoding="ascii").strip()
            try:
                if not self.object_path(target).exists():
                    errors.append(f"dangling ref {path.relative_to(self.refs)} -> {target}")
            except RegistryError as exc:
                errors.append(f"bad ref {path.relative_to(self.refs)}: {exc}")
        if graph:
            for obj in objects:
                for target in self.linked_objects(obj):
                    try:
                        exists = self.object_path(target).exists()
                    except RegistryError:
                        exists = False
                    if not exists:
                        errors.append(
                            f"dangling object link {obj['content_id']} -> {target}"
                        )
        return {
            "ok": not errors,
            "objects": count,
            "refs": ref_count,
            "graph_checked": graph,
            "errors": errors,
        }

    def _event(
        self,
        operation: str,
        object_id: str,
        *,
        ref: str | None = None,
        created: bool | None = None,
    ) -> None:
        event = {
            "at": datetime.now(timezone.utc).isoformat(),
            "operation": operation,
            "object_id": object_id,
        }
        if ref is not None:
            event["ref"] = ref
        if created is not None:
            event["created"] = created
        with open(self.events, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, sort_keys=True) + "\n")

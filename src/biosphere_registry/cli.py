"""`bar` command-line interface."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import site
import sys
import sysconfig
from pathlib import Path

from .identity import content_id, with_content_id
from .registry import Registry, RegistryError
from .validation import load_json, validate, validate_with_schema

def schema_dir() -> Path:
    """Locate normative schemas in a source checkout or installed wheel."""

    candidates = [
        Path(__file__).resolve().parents[2] / "schemas",
        Path(sysconfig.get_path("data"))
        / "share"
        / "biosphere-address-registry"
        / "schemas",
        Path(site.USER_BASE) / "share" / "biosphere-address-registry" / "schemas",
    ]
    found = next((path for path in candidates if path.is_dir()), None)
    if found is not None:
        return found
    try:
        distribution = importlib.metadata.distribution("biosphere-address-registry")
        for item in distribution.files or []:
            text = str(item).replace("\\", "/")
            if text.endswith(
                "share/biosphere-address-registry/schemas/observation.v1.json"
            ):
                return Path(distribution.locate_file(item)).parent
    except importlib.metadata.PackageNotFoundError:
        pass
    return candidates[0]


def emit(value: object) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False))


def cmd_id(args: argparse.Namespace) -> int:
    obj = load_json(args.file)
    print(content_id(obj))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    obj = load_json(args.file)
    errors = validate(obj, require_id=args.require_id)
    if args.schema:
        errors.extend(validate_with_schema(obj, schema_dir()))
    result = {
        "ok": not errors,
        "content_id": content_id(obj),
        "record_type": obj.get("record_type"),
        "errors": errors,
    }
    emit(result)
    return 0 if not errors else 1


def cmd_stamp(args: argparse.Namespace) -> int:
    obj = with_content_id(load_json(args.file))
    encoded = json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.in_place:
        Path(args.file).write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    registry = Registry(args.registry)
    registry.initialize()
    emit({"ok": True, "registry": str(Path(args.registry).resolve())})
    return 0


def cmd_put(args: argparse.Namespace) -> int:
    obj = Registry(args.registry).put(args.file, ref=args.ref)
    emit({"ok": True, "content_id": obj["content_id"], "ref": args.ref})
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    emit(Registry(args.registry).get(args.object))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    registry = Registry(args.registry)
    emit(
        [
            {"content_id": object_id, "path": str(path.relative_to(registry.root))}
            for object_id, path in registry.iter_objects()
        ]
    )
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    result = Registry(args.registry).verify(graph=args.graph)
    emit(result)
    return 0 if result["ok"] else 1


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        prog="bar",
        description="Biosphere Address Registry v1 reference CLI",
    )
    sub = root.add_subparsers(dest="command", required=True)

    p = sub.add_parser("id", help="compute canonical content identity")
    p.add_argument("file")
    p.set_defaults(run=cmd_id)

    p = sub.add_parser("validate", help="validate a BAR JSON record")
    p.add_argument("file")
    p.add_argument("--require-id", action="store_true")
    p.add_argument("--schema", action="store_true", help="also use JSON Schema")
    p.set_defaults(run=cmd_validate)

    p = sub.add_parser("stamp", help="add the canonical content_id")
    p.add_argument("file")
    p.add_argument("--in-place", action="store_true")
    p.set_defaults(run=cmd_stamp)

    p = sub.add_parser("init", help="initialize a local registry")
    p.add_argument("registry")
    p.set_defaults(run=cmd_init)

    p = sub.add_parser("put", help="ingest an immutable object")
    p.add_argument("registry")
    p.add_argument("file")
    p.add_argument("--ref")
    p.set_defaults(run=cmd_put)

    p = sub.add_parser("get", help="read an object by ID or ref")
    p.add_argument("registry")
    p.add_argument("object")
    p.set_defaults(run=cmd_get)

    p = sub.add_parser("list", help="list registry objects")
    p.add_argument("registry")
    p.set_defaults(run=cmd_list)

    p = sub.add_parser("verify", help="verify objects and refs")
    p.add_argument("registry")
    p.add_argument("--graph", action="store_true", help="also verify object links")
    p.set_defaults(run=cmd_verify)
    return root


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        return int(args.run(args))
    except (ValueError, RegistryError, OSError, json.JSONDecodeError) as exc:
        print(f"bar: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import pytest

from biosphere_registry import (
    IdentityError,
    content_id,
    observation,
    sequence_id,
    verify_content_id,
    with_content_id,
)


def test_canonical_identity_ignores_key_order_and_self_id():
    a = {"record_type": "x", "spec_version": "bar-1.0", "payload": {"b": 2, "a": 1}}
    b = {"payload": {"a": 1, "b": 2}, "spec_version": "bar-1.0", "record_type": "x"}
    assert content_id(a) == content_id(b)
    stamped = with_content_id(a)
    assert content_id(stamped) == content_id(a)
    assert verify_content_id(stamped)


def test_identity_covers_unknown_payload_fields():
    a = {"record_type": "x", "spec_version": "bar-1.0", "payload": {"a": 1}}
    b = {"record_type": "x", "spec_version": "bar-1.0", "payload": {"a": 1, "future": 2}}
    assert content_id(a) != content_id(b)


def test_bad_supplied_identity_refused():
    with pytest.raises(IdentityError):
        with_content_id(
            {
                "record_type": "x",
                "spec_version": "bar-1.0",
                "payload": {},
                "content_id": "sha256:" + "0" * 64,
            }
        )


def test_sequence_normalization_is_explicit_and_stable():
    first, normalized = sequence_id(" acgT\nACGT ")
    second, _ = sequence_id("ACGTACGT")
    assert normalized == "ACGTACGT"
    assert first == second
    record = observation(" acgT\nACGT ", include_sequence=True)
    assert record["payload"]["sequence"] == "ACGTACGT"
    assert record["payload"]["length_bp"] == 8

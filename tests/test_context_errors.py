import pytest

from modules.context_ops import (
    apply_add, apply_set_file_index, apply_set_index, apply_set_pairs
)


def test_add_on_existing_scalar_should_error():
    ctx = {}
    apply_set_pairs(ctx, ["NAME=alpha"])
    # Now adding as a list should fail because NAME is a scalar
    with pytest.raises(SystemExit):
        apply_add(ctx, ["NAME=beta"])


def test_set_file_index_requires_single_match(tmp_path):
    ctx = {}
    (tmp_path / "a.txt").write_text("A", encoding="utf-8")
    (tmp_path / "b.txt").write_text("B", encoding="utf-8")
    with pytest.raises(SystemExit):
        apply_set_file_index(ctx, [f"ARR:0={tmp_path}/*.txt"])


def test_set_index_bad_format_raises():
    ctx = {}
    # Missing numeric index (e.g., "FOO:abc=bar") should raise
    with pytest.raises(SystemExit):
        apply_set_index(ctx, ["FOO:abc=bar"])

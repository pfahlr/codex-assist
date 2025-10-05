import pytest
from modules.context_ops import apply_set_pairs, apply_set_file, apply_set_json, apply_set_json_file
from pathlib import Path



def test_set_file_explicit_index_multi_match_errors(tmp_path):
    (tmp_path / "a.txt").write_text("A", encoding="utf-8")
    (tmp_path / "b.txt").write_text("B", encoding="utf-8")
    ctx = {}
    with pytest.raises(SystemExit):
        apply_set_file(ctx, [f"ARR[1]={tmp_path}/*.txt"])


def test_set_pairs_list_syntax_conflicts_with_existing_scalar():
    ctx = {}
    apply_set_pairs(ctx, ["NAME=alpha"])
    # old array syntax should attempt list semantics and fail
    with pytest.raises(SystemExit):
        apply_set_pairs(ctx, ["NAME[]=beta"])


def test_apply_set_pairs_missing_equals_raises():
    with pytest.raises(SystemExit):
        apply_set_pairs({}, ["NOEQUALS"])


def test_apply_set_json_invalid_json_raises():
    with pytest.raises(SystemExit):
        apply_set_json({}, ['X={not json}'])


def test_apply_set_json_file_invalid_json_raises(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{ nope", encoding="utf-8")
    with pytest.raises(SystemExit):
        apply_set_json_file({}, [f"X={bad}"])


def test_apply_set_file_assign_list_to_scalar_errors(tmp_path):
    # First set a scalar at key 'K', then try to add list semantics via file-array
    ctx = {}
    apply_set_pairs(ctx, ["K=scalar"])
    (tmp_path / "a.txt").write_text("A", encoding="utf-8")
    (tmp_path / "b.txt").write_text("B", encoding="utf-8")
    # Attempt KEY[]=glob will require 'K' to be a list (should error)
    with pytest.raises(SystemExit):
        apply_set_file(ctx, [f"K[]={tmp_path}/*.txt"])


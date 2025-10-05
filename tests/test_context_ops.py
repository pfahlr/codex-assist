from pathlib import Path

from modules.context_ops import (
    apply_set_pairs, apply_set_file, apply_set_json, apply_set_json_file,
    apply_add, apply_add_file, apply_set_index, apply_set_file_index
)


def test_apply_set_pairs_scalars_arrays_and_nesting(tmp_path):
    ctx = {}
    apply_set_pairs(ctx, ["A=1", "NEST.X=hello"])
    assert ctx["A"] == "1"
    assert ctx["NEST"]["X"] == "hello"

    # old array syntax: LIST[]=item and LIST[2]=item
    apply_set_pairs(ctx, ["LIST[]=a", "LIST[]=b", "LIST[2]=c"])
    assert ctx["LIST"] == ["a", "b", "c"]

    # file shorthand via @path
    f = tmp_path / "note.txt"
    f.write_text("FROMFILE", encoding="utf-8")
    apply_set_pairs(ctx, [f"TXT=@{f}"])
    assert ctx["TXT"] == "FROMFILE"


def test_apply_set_file_scalar_vs_list(tmp_path):
    ctx = {}

    (tmp_path / "a.txt").write_text("A", encoding="utf-8")
    (tmp_path / "b.txt").write_text("B", encoding="utf-8")

    # single => scalar
    apply_set_file(ctx, [f"ONE={tmp_path}/a.txt"])
    assert ctx["ONE"] == "A"

    # many => list
    apply_set_file(ctx, [f"MULTI={tmp_path}/*.txt"])
    assert ctx["MULTI"] == ["A", "B"]

    # list append using KEY[] with file glob
    apply_set_file(ctx, [f"ARR[]={tmp_path}/*.txt"])
    assert ctx["ARR"] == ["A", "B"]

    # explicit index requires exactly 1 match
    apply_set_file(ctx, [f"IDX[1]={tmp_path}/b.txt"])
    assert ctx["IDX"] == [None, "B"]


def test_apply_set_json_and_file(tmp_path):
    ctx = {}
    apply_set_json(ctx, ['OBJ={"a":1,"b":[1,2]}'])
    assert ctx["OBJ"] == {"a": 1, "b": [1, 2]}

    j = tmp_path / "data.json"
    j.write_text('{"ok": true, "n": 7}', encoding="utf-8")
    apply_set_json_file(ctx, [f"FROMFILE={j}"])
    assert ctx["FROMFILE"] == {"ok": True, "n": 7}


def test_add_and_index_variants(tmp_path):
    ctx = {}
    # --add (plain + from file)
    (tmp_path / "t.txt").write_text("T", encoding="utf-8")
    apply_add(ctx, ["TASKS=alpha", f"TASKS=@{tmp_path}/t.txt"])
    assert ctx["TASKS"] == ["alpha", "T"]

    # --add-file (glob)
    (tmp_path / "g1.txt").write_text("g1", encoding="utf-8")
    (tmp_path / "g2.txt").write_text("g2", encoding="utf-8")
    apply_add_file(ctx, [f"TASKS={tmp_path}/*g*.txt"])
    assert ctx["TASKS"] == ["alpha", "T", "g1", "g2"]

    # --set-index and --set-file-index
    apply_set_index(ctx, ["T2:3=pos3"])
    assert ctx["T2"] == [None, None, None, "pos3"]

    f = tmp_path / "x.txt"
    f.write_text("XVAL", encoding="utf-8")
    apply_set_file_index(ctx, [f"T2:1={f}"])
    assert ctx["T2"][1] == "XVAL"


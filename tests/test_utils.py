import os
from pathlib import Path

import pytest

from modules import utils as U


def test_expand_and_read_text_file(tmp_path, monkeypatch):
    # ~ expansion
    home_sample = tmp_path / "homefile.txt"
    home_sample.write_text("HOME!", encoding="utf-8")
    monkeypatch.setenv("HOME", str(tmp_path))

    p = U.expand_path("~/homefile.txt")
    assert Path(p).read_text(encoding="utf-8") == "HOME!"

    # $VAR expansion
    monkeypatch.setenv("MYVAR", "subdir/inner.txt")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "inner.txt").write_text("ENV!", encoding="utf-8")
    p2 = U.expand_path(str(tmp_path / "$MYVAR"))
    assert Path(p2).read_text(encoding="utf-8") == "ENV!"

    # read_text_file errors for missing file
    with pytest.raises(SystemExit):
        U.read_text_file(str(tmp_path / "does_not_exist.txt"))


def test_load_pattern_contents_glob_sorted(tmp_path):
    (tmp_path / "a.txt").write_text("A", encoding="utf-8")
    (tmp_path / "b.txt").write_text("B", encoding="utf-8")
    (tmp_path / "c.txt").write_text("C", encoding="utf-8")

    out = U.load_pattern_contents(str(tmp_path / "*.txt"))
    assert out == ["A", "B", "C"]


def test_maybe_file_value_at_sign_behavior(tmp_path):
    f = tmp_path / "note.txt"
    f.write_text("FROMFILE", encoding="utf-8")

    # @@ escapes @
    assert U.maybe_file_value("@@literal") == "@literal"
    # @path reads file
    assert U.maybe_file_value(f"@{f}") == "FROMFILE"
    # plain value unchanged
    assert U.maybe_file_value("plain") == "plain"


def test_deep_merge_nested():
    dst = {"a": 1, "b": {"x": 1, "y": 2}}
    src = {"b": {"y": 22, "z": 3}, "c": 9}
    out = U.deep_merge(dst, src)
    assert out == {"a": 1, "b": {"x": 1, "y": 22, "z": 3}, "c": 9}


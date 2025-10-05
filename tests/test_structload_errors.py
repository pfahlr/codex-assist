from pathlib import Path
import pytest

from modules.structload import load_structured_file


pytest.importorskip("yaml")


def test_glob_one_no_match_raises(tmp_path):
    yml = "doc: { $glob_one: missing.txt }\n"
    p = tmp_path / "x.yaml"
    p.write_text(yml, encoding="utf-8")
    with pytest.raises(SystemExit):
        load_structured_file(str(p))


def test_glob_one_multiple_matches_raises(tmp_path):
    (tmp_path / "a.txt").write_text("A", encoding="utf-8")
    (tmp_path / "b.txt").write_text("B", encoding="utf-8")
    yml = f"doc: {{ $glob_one: {tmp_path}/*.txt }}\n"
    p = tmp_path / "x.yaml"
    p.write_text(yml, encoding="utf-8")
    with pytest.raises(SystemExit):
        load_structured_file(str(p))


def test_files_macro_requires_list(tmp_path):
    yml = "doc: { $files: notalist }\n"
    p = tmp_path / "x.yaml"
    p.write_text(yml, encoding="utf-8")
    with pytest.raises(SystemExit):
        load_structured_file(str(p))


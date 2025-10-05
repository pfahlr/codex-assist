import pytest 
from modules.structload import load_structured_file, load_structured_glob



def test_glob_with_join_returns_scalar(tmp_path):
    (tmp_path / "a.txt").write_text("A", encoding="utf-8")
    (tmp_path / "b.txt").write_text("B", encoding="utf-8")
    yml = f"""\
doc: {{ $glob: "{tmp_path}/*.txt", $join: "|" }}
"""
    p = tmp_path / "j.yaml"
    p.write_text(yml, encoding="utf-8")
    docs = load_structured_file(str(p))
    assert docs[0]["doc"] == "A|B"


def test_load_structured_file_bad_json_raises(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{ nope", encoding="utf-8")
    with pytest.raises(SystemExit):
        load_structured_file(str(bad))


def test_load_structured_glob_single_file_path(tmp_path):
    p = tmp_path / "d.json"
    p.write_text('{"a":1}', encoding="utf-8")
    docs = load_structured_glob(str(p))
    assert docs == [{"a": 1}]

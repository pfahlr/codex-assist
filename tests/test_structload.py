from pathlib import Path

import pytest

from modules.structload import load_structured_file, load_structured_glob


pytest.importorskip("yaml")  # macros are often exercised in YAML


def test_load_json_basic(tmp_path):
    p = tmp_path / "d.json"
    p.write_text('{"x": 1, "y": {"z": 3}}', encoding="utf-8")
    docs = load_structured_file(str(p))
    assert docs == [{"x": 1, "y": {"z": 3}}]


def test_load_yaml_multidoc_and_macros(tmp_path):
    # content files to be pulled in
    (tmp_path / "intro.txt").write_text("Hello", encoding="utf-8")
    (tmp_path / "snips").mkdir()
    (tmp_path / "snips" / "a.md").write_text("A", encoding="utf-8")
    (tmp_path / "snips" / "b.md").write_text("B", encoding="utf-8")

    # YAML with two docs; first uses macros
    yml = """\
---
title: Demo
intro: { $file: intro.txt }
snippets: { $glob: snips/*.md }
joined: { $glob: snips/*.md, $join: "|" }
one: { $glob_one: intro.txt }
---
- just
- a
- list
"""
    p = tmp_path / "doc.yaml"
    p.write_text(yml, encoding="utf-8")

    docs = load_structured_file(str(p))
    assert len(docs) == 2
    d1, d2 = docs
    assert d1["title"] == "Demo"
    assert d1["intro"] == "Hello"
    assert d1["snippets"] == ["A", "B"]  # lexicographic
    assert d1["joined"] == "A|B"
    assert d1["one"] == "Hello"
    assert d2 == ["just", "a", "list"]


def test_glob_loader_aggregates(tmp_path):
    (tmp_path / "a.json").write_text('{"a":1}', encoding="utf-8")
    (tmp_path / "b.json").write_text('{"b":2}', encoding="utf-8")
    docs = load_structured_glob(str(tmp_path / "*.json"))
    # order is lexicographic by file name
    assert docs == [{"a": 1}, {"b": 2}]


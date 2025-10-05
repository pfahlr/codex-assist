import os
from pathlib import Path
import pytest

from modules import config as C


def test_find_config_path_explicit_missing(tmp_path):
    with pytest.raises(SystemExit):
        C.find_config_path(str(tmp_path / "nope.yaml"))


def test_find_config_path_returns_absolute(tmp_path, monkeypatch):
    cfg = tmp_path / "codex.yaml"
    cfg.write_text("{}", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    found = C.find_config_path(None)
    assert found == cfg.resolve()  # absolute


def test_env_tpl_paths_colon_split(monkeypatch):
    monkeypatch.setenv("CODEX_TPL_PATH", "/a:/b:/c")
    paths = C.env_tpl_paths()
    assert paths == ["/a", "/b", "/c"]


def test_merge_config_sets_out_and_rewrites_pairs(tmp_path, monkeypatch):
    # files referenced by config
    (tmp_path / "data.json").write_text('{"k":1}', encoding="utf-8")
    (tmp_path / "f.txt").write_text("F", encoding="utf-8")

    cfg = tmp_path / "codex.yaml"
    cfg.write_text(
        """\
out: ./result.txt
set_json_file:
  - obj=./data.json
set_file_index:
  - arr:1=./f.txt
""",
        encoding="utf-8",
    )

    class NS:
        template_search = []
        load = []
        load_into = []
        set = []
        set_json = []
        set_json_file = []
        set_file = []
        add = []
        add_file = []
        set_index = []
        set_file_index = []
        out = ""

    ns = NS()
    doc = C.load_config(cfg)
    C.merge_config_into_args(ns, doc, base_dir=cfg.parent)

    # out default is applied
    assert ns.out.endswith("result.txt")
    # RHS paths rewritten to absolute
    assert ns.set_json_file == [f"obj={tmp_path / 'data.json'}"]
    assert ns.set_file_index == [f"arr:1={tmp_path / 'f.txt'}"]


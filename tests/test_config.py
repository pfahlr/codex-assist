import sys
from pathlib import Path

import pytest

from modules import config as C


def test_find_config_path_prefers_local(tmp_path, monkeypatch):
    # Create a local codex.yaml and change into that dir
    cfg = tmp_path / "codex.yaml"
    cfg.write_text("set:\n  - owner=pfahlr\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    found = C.find_config_path(None)
    assert found == cfg


def test_load_config_requires_mapping(tmp_path):
    # Top-level list should be rejected
    bad = tmp_path / "codex.yaml"
    bad.write_text("- a\n- b\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        C.load_config(bad)


def test_merge_config_into_args_normalizes_load_and_load_into_and_env_paths(tmp_path, monkeypatch):
    cfgp = tmp_path / "cfg.yaml"
    # Simulate a variety of shapes:
    # - load: one entry accidentally indexed like "0=./x.yaml"
    # - load_into: dict + list-of-dicts + "KEY=VALUE" string
    # - template_search from config + CODEX_TPL_PATH from env
    cfgp.write_text(
        """\
template_search:
  - ts1
load:
  - "0=./parts.yaml"
load_into:
  DATA: ./data.json
  # also allow list of dicts and "KEY=VALUE" strings:
  EXTRA:
    - ./e1.json
    - ./e2.json
set_file:
  - intro=./intro.md
""",
        encoding="utf-8",
    )
    # files referenced (just to ensure paths can resolve to absolutes)
    (tmp_path / "parts.yaml").write_text("parts: []\n", encoding="utf-8")
    (tmp_path / "data.json").write_text('{"title":"t"}\n', encoding="utf-8")
    (tmp_path / "e1.json").write_text('{"a":1}\n', encoding="utf-8")
    (tmp_path / "e2.json").write_text('{"b":2}\n', encoding="utf-8")
    (tmp_path / "intro.md").write_text("hi\n", encoding="utf-8")

    class NS:
        # match argparse defaults (lists)
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

    args = NS()
    # Add an env tpl path and chdir so relative joining can be checked
    monkeypatch.setenv("CODEX_TPL_PATH", str(tmp_path / "envtpl"))
    (tmp_path / "envtpl").mkdir()
    C.merge_config_into_args(args, C.load_config(cfgp), base_dir=cfgp.parent)

    # template_search contains cfg value (abspath) + env path
    assert any(str(tmp_path / "ts1") in p for p in args.template_search)
    assert any(str(tmp_path / "envtpl") in p for p in args.template_search)

    # load normalized: "0=./parts.yaml" -> absolute path (no "0=")
    assert len(args.load) == 1
    assert args.load[0].endswith("parts.yaml")
    assert "0=" not in args.load[0]

    # load_into became list of "KEY=ABS" strings
    # DATA assignment must be present
    assert any(s.startswith("DATA=") for s in args.load_into)
    # EXTRA had a list -> two entries
    extra = [s for s in args.load_into if s.startswith("EXTRA=")]
    assert len(extra) == 2

    # set_file path was rewritten to absolute
    assert len(args.set_file) == 1 and args.set_file[0].startswith("intro=")
    assert str(tmp_path) in args.set_file[0]

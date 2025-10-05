import sys
from pathlib import Path

import pytest

from modules import cli


pytest.importorskip("jinja2")
pytest.importorskip("yaml")


def test_cli_end_to_end_with_config_and_loads(tmp_path, monkeypatch, capsys):
    # layout
    tdir = tmp_path / "tpl"
    tdir.mkdir()
    tfile = tdir / "main.tpl"
    tfile.write_text(
        "Owner={{ owner }} Repo={{ repo }} Intro={{ intro }} "
        "Tasks:{% for t in tasks %}{{ '-' + t }}{% endfor %} "
        "DataTitle={{ DATA.title }} "
        "Parts={{ parts|join(',') }}",
        encoding="utf-8",
    )

    # content files
    (tmp_path / "intro.md").write_text("HELLO", encoding="utf-8")
    (tmp_path / "tasks").mkdir()
    (tmp_path / "tasks" / "a.txt").write_text("A", encoding="utf-8")
    (tmp_path / "tasks" / "b.txt").write_text("B", encoding="utf-8")

    # structured docs
    (tmp_path / "data.json").write_text('{"title":"DTitle"}', encoding="utf-8")
    (tmp_path / "parts.yaml").write_text(
        """\
parts: { $glob: tasks/*.txt }
""",
        encoding="utf-8",
    )

    # local config (picked up without --config)
    (tmp_path / "codex.yaml").write_text(
        f"""\
template_search:
  - {tdir}

set:
  - owner=pfahlr
  - repo=ragx

set_file:
  - intro=./intro.md

add_file:
  - tasks=tasks/*.txt

load_into:
  DATA: ./data.json
load:
  - ./parts.yaml

out: ./out.txt
""",
        encoding="utf-8",
    )

    # run
    monkeypatch.chdir(tmp_path)
    argv = [
        "prog",
        "--template-name",
        str(tfile),
        "--print-context",
    ]
    monkeypatch.setenv("PYTHONWARNINGS", "ignore")  # silence yaml warnings
    monkeypatch.setenv("CODEX_TPL_PATH", "")  # keep search deterministic
    monkeypatch.setenv("PYTHONIOENCODING", "utf-8")
    monkeypatch.setenv("LC_ALL", "C.UTF-8")
    monkeypatch.setenv("LANG", "C.UTF-8")

    monkeypatch.setenv("PYTHONDONTWRITEBYTECODE", "1")
    monkeypatch.setenv("PYTHONHASHSEED", "0")

    monkeypatch.setattr(sys, "argv", argv)
    cli.main()

    # verify output file written by config 'out'
    outp = tmp_path / "out.txt"
    text = outp.read_text(encoding="utf-8")

    assert "Owner=pfahlr" in text
    assert "Repo=ragx" in text
    assert "Intro=HELLO" in text
    # tasks (A and B via add_file)
    assert "-A" in text and "-B" in text
    # DATA loaded via load_into
    assert "DataTitle=DTitle" in text
    # parts loaded via load (root merge) using macro
    assert "Parts=A, B" in text or "Parts=A,B" in text  # spacing-safe

import sys
from pathlib import Path

import pytest

from modules import cli


def test_help_extended_prints(monkeypatch, capsys, tmp_path):
    # need to satisfy required --template-name, but it won't be used
    dummy = tmp_path / "t.tpl"
    dummy.write_text("OK", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["prog", "--template-name", str(dummy), "--help-extended"])
    cli.main()
    out = capsys.readouterr().out
    assert "Codex Template Builder - Extended Help" in out


def test_cli_load_into_dict_shape(tmp_path, monkeypatch):
    tdir = tmp_path / "tpl"
    tdir.mkdir()
    tfile = tdir / "main.tpl"
    tfile.write_text("{{ DATA.title }}", encoding="utf-8")

    data = tmp_path / "data.json"
    data.write_text('{"title": "Yay"}', encoding="utf-8")

    cfg = tmp_path / "codex.yaml"
    cfg.write_text(
        f"""\
template_search:
  - {tdir}
load_into:
  DATA: {data}
out: {tmp_path}/out.txt
""",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog", "--template-name", str(tfile)])
    cli.main()

    outp = tmp_path / "out.txt"
    assert outp.read_text(encoding="utf-8").strip() == "Yay"


def test_cli_load_index_artifact_in_load_and_load_into(tmp_path, monkeypatch):
    tdir = tmp_path / "tpl"
    tdir.mkdir()
    tfile = tdir / "main.tpl"
    tfile.write_text("{{ DATA.title }}-{{ parts|join(',') }}", encoding="utf-8")

    (tmp_path / "p.yaml").write_text("parts: [a, b]", encoding="utf-8")
    (tmp_path / "d.json").write_text('{"title":"T"}', encoding="utf-8")

    cfg = tmp_path / "codex.yaml"
    cfg.write_text(
        f"""\
template_search: [{tdir}]
load:
  - "0=./p.yaml"
load_into:
  - "0=DATA=./d.json"
out: ./out.txt
""",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog", "--template-name", str(tfile)])
    cli.main()

    outp = tmp_path / "out.txt"
    txt = outp.read_text(encoding="utf-8").strip()
    assert txt.startswith("T-")
    assert "a" in txt and "b" in txt

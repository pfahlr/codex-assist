import sys
from pathlib import Path
import pytest

from modules import cli


def test_cli_stdout_when_no_out_and_print_context(tmp_path, monkeypatch, capsys):
    tfile = tmp_path / "t.tpl"
    tfile.write_text("X={{ x }}", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", [
        "prog", "--template-name", str(tfile),
        "--set", "x=1",
        "--print-context",
    ])
    cli.main()

    out = capsys.readouterr()
    assert out.out.strip() == "X=1"
    assert '"x": "1"' in out.err  # printed JSON context


def test_cli_load_non_mapping_in_load_errors(tmp_path, monkeypatch):
    tfile = tmp_path / "t.tpl"
    tfile.write_text("{{ a }}", encoding="utf-8")

    bad = tmp_path / "bad.yaml"
    bad.write_text("- not\n- a\n- mapping\n", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", [
        "prog", "--template-name", str(tfile),
        "--load", str(bad)
    ])
    with pytest.raises(SystemExit):
        cli.main()

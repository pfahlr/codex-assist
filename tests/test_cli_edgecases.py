import sys
from pathlib import Path
import pytest

from modules import cli


def test_cli_errors_when_template_missing(monkeypatch, tmp_path):
    missing = tmp_path / "nope.tpl"
    monkeypatch.setattr(sys, "argv", ["prog", "--template-name", str(missing)])
    with pytest.raises(SystemExit):
        cli.main()


def test_cli_load_into_invalid_string_raises(monkeypatch, tmp_path):
    tfile = tmp_path / "t.tpl"
    tfile.write_text("OK", encoding="utf-8")
    # "justapath" has no key=... and should error
    monkeypatch.setattr(
        sys,
        "argv",
        ["prog", "--template-name", str(tfile), "--load-into", "justapath"],
    )
    with pytest.raises(SystemExit):
        cli.main()


def test_cli_load_into_index_prefix_without_key_raises(monkeypatch, tmp_path):
    tfile = tmp_path / "t.tpl"
    tfile.write_text("OK", encoding="utf-8")
    # "0=./d.json" becomes "./d.json" after strip, still invalid (no KEY=...)
    monkeypatch.setattr(
        sys,
        "argv",
        ["prog", "--template-name", str(tfile), "--load-into", "0=./d.json"],
    )
    with pytest.raises(SystemExit):
        cli.main()

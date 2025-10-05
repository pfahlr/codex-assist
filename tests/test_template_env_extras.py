import pytest
from pathlib import Path

from modules.template_env import render_template


pytest.importorskip("jinja2")


def test_include_text_missing_raises(tmp_path):
    tfile = tmp_path / "main.tpl"
    tfile.write_text("{{ include_text('no-such.txt') }}", encoding="utf-8")
    with pytest.raises(SystemExit):
        render_template(tfile, {}, extra_search=[str(tmp_path)])


def test_zip_filter_with_none_lists(tmp_path):
    tfile = tmp_path / "main.tpl"
    # A is None, B is list -> zip should yield empty
    tfile.write_text("{% for a,b in A|zip(B) %}[{{a}}-{{b}}]{% endfor %}", encoding="utf-8")
    out = render_template(tfile, {"A": None, "B": [1, 2]}, extra_search=[str(tmp_path)])
    assert out.strip() == ""


def test_extra_search_finds_extra_files(tmp_path):
    base = tmp_path / "tpl"
    base.mkdir()
    extra = tmp_path / "xtra"
    extra.mkdir(parents=True)
    (extra / "sub").mkdir()
    (extra / "sub" / "only.txt").write_text("EXTRA-ONLY", encoding="utf-8")

    tfile = base / "main.tpl"
    tfile.write_text("{% include 'sub/only.txt' %}", encoding="utf-8")

    out = render_template(tfile, {}, extra_search=[str(extra)])
    assert "EXTRA-ONLY" in out

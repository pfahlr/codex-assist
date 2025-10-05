import pytest
from pathlib import Path
from modules.template_env import render_template


pytest.importorskip("jinja2")


def test_read_json_error_raises(tmp_path):
    tfile = tmp_path / "t.tpl"
    (tmp_path / "bad.json").write_text("{ nope", encoding="utf-8")
    tfile.write_text("{{ read_json('bad.json') }}", encoding="utf-8")
    with pytest.raises(SystemExit):
        render_template(tfile, {}, extra_search=[str(tmp_path)])


def test_zip_filter_mismatched_lengths(tmp_path):
    tfile = tmp_path / "t.tpl"
    tfile.write_text("{% for a,b in A|zip(B) %}[{{a}}-{{b}}]{% endfor %}", encoding="utf-8")
    out = render_template(tfile, {"A": [1, 2, 3], "B": ["x"]}, extra_search=[str(tmp_path)])
    # only one pair should render
    assert out.strip() == "[1-x]"

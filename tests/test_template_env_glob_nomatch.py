import pytest
from modules.template_env import render_template


pytest.importorskip("jinja2")


def test_include_text_glob_no_matches_raises(tmp_path):
    t = tmp_path / "t.tpl"
    t.write_text("{{ include_text_glob('nope/*.md') }}", encoding="utf-8")
    with pytest.raises(SystemExit):
        render_template(t, {}, [str(tmp_path)])


def test_read_file_alias_matches_include_text(tmp_path):
    # read_file is alias of include_text
    (tmp_path / "x.txt").write_text("HI", encoding="utf-8")
    t = tmp_path / "t.tpl"
    t.write_text("{{ include_text('x.txt') }}|{{ read_file('x.txt') }}", encoding="utf-8")
    out = render_template(t, {}, [str(tmp_path)])
    assert out.strip() == "HI|HI"


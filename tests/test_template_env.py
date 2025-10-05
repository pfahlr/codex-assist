from pathlib import Path

import pytest

from modules.template_env import render_template


pytest.importorskip("jinja2")


def test_render_with_includes_and_helpers(tmp_path):
    # folder layout
    tdir = tmp_path / "templates"
    tdir.mkdir()
    (tdir / "partial.txt").write_text("[PARTIAL]", encoding="utf-8")
    (tdir / "extra.txt").write_text("EXTRA", encoding="utf-8")
    (tdir / "data.json").write_text('{"title":"Spec"}', encoding="utf-8")
    (tdir / "snips").mkdir()
    (tdir / "snips" / "a.md").write_text("A", encoding="utf-8")
    (tdir / "snips" / "b.md").write_text("B", encoding="utf-8")

    tpl = (
        "Hello {{ name }} "
        "{% include 'partial.txt' %} "
        "{{ include_text('extra.txt') }} "
        "{{ read_json('data.json').title }} "
        "{% for a,b in A|zip(B) %}[{{a}}-{{b}}]{% endfor %} "
        "{{ include_text_glob('snips/*.md', sep='|') }}"
    )
    (tdir / "main.tpl").write_text(tpl, encoding="utf-8")

    ctx = {"name": "World", "A": [1, 2], "B": ["x", "y"]}
    out = render_template(tdir / "main.tpl", ctx, extra_search=[str(tdir)])
    # basic expectations
    assert "Hello World" in out
    assert "[PARTIAL]" in out
    assert "EXTRA" in out
    assert "Spec" in out
    assert "[1-x][2-y]" in out
    assert "A|B" in out


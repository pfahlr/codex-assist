import pytest
from modules.utils import die, deep_merge, expand_path, maybe_file_value, load_pattern_contents


def test_die_raises_system_exit():
    with pytest.raises(SystemExit):
        die("boom")


def test_deep_merge_overrides_non_dict():
    dst = {"x": {"a": 1}, "y": 2}
    src = {"x": 5, "y": {"b": 3}}
    out = deep_merge(dst, src)
    assert out["x"] == 5
    assert out["y"] == {"b": 3}


def test_expand_path_env_and_tilde(monkeypatch, tmp_path):
    monkeypatch.setenv("X", "sub/file.txt")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "file.txt").write_text("ok", encoding="utf-8")
    monkeypatch.setenv("HOME", str(tmp_path))
    p = expand_path("$X")
    assert p.endswith("sub/file.txt")
    p2 = expand_path("~/sub/file.txt")
    assert p2.endswith("sub/file.txt")


def test_maybe_file_value_at_only_raises():
    with pytest.raises(SystemExit):
        maybe_file_value("@")  # empty path after '@' is illegal


def test_load_pattern_contents_missing_file_raises(tmp_path):
    # Glob returns none -> fallback to "single file" -> missing -> raises
    with pytest.raises(SystemExit):
        load_pattern_contents(str(tmp_path / "no-such-file.txt"))

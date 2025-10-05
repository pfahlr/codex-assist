import os
import pytest

from modules import config as C


def test_env_tpl_paths_windows_semicolons(monkeypatch):
    # Pretend we're on Windows to exercise ';' splitting
    monkeypatch.setenv("CODEX_TPL_PATH", r"C:\a;D:\b;E:\c")
    monkeypatch.setattr(C.os, "name", "nt")
    paths = C.env_tpl_paths()
    assert paths == [r"C:\a", r"D:\b", r"E:\c"]

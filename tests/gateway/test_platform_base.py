from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from gateway.platforms.base import BasePlatformAdapter, validate_media_delivery_path


@pytest.fixture(params=[True, False])
def strict_mode(request, tmp_path, monkeypatch):
    monkeypatch.setenv("HERMES_MEDIA_ALLOW_DIRS", str(tmp_path / "allow"))
    (tmp_path / "allow").mkdir()
    (tmp_path / "reject").mkdir()
    monkeypatch.setattr(BasePlatformAdapter, "_is_strict_mode", staticmethod(lambda: request.param))
    return request.param



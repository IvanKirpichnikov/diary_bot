from __future__ import annotations

from typing import Any


class DiaryType:
    @classmethod
    def from_data(cls, data: Any) -> DiaryType:
        raise NotImplementedError

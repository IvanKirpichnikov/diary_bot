from __future__ import annotations

from typing import Any


class BaseType:
    @classmethod
    def from_data(cls, data: Any) -> BaseType:
        raise NotImplementedError

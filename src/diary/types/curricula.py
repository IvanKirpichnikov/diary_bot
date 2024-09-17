from dataclasses import dataclass

from diary.types.base import DiaryType


@dataclass(frozen=True)
class Curricula(DiaryType):
    id: int
    name: str
    class_level_id: int | None = None

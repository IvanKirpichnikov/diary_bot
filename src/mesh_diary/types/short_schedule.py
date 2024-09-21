from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Any, override

from adaptix import P, Retort, loader

from mesh_diary.types.base import BaseType


@dataclass(frozen=True)
class Lesson:
    begin_time: time
    end_time: time
    group_id: int
    group_name: str
    subject_id: int
    subject_name: str
    lesson_id: int | None = None
    lesson_name: str | None = None


@dataclass(frozen=True)
class ShortSchedule(BaseType):
    date: date
    lessons: list[Lesson]


@dataclass(frozen=True)
class ShortSchedules(BaseType):
    schedules: list[ShortSchedule]

    @classmethod
    @override
    def from_data(cls, data: dict[str, Any]) -> ShortSchedules:
        return retort.load(
            {"schedules": data["payload"]},
            ShortSchedules,
        )


retort = Retort(
    recipe=[
        loader(
            P[Lesson][time],
            lambda x: datetime.strptime(x, "%H:%M").time(),
        ),
        loader(
            P[ShortSchedule].date,
            lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        ),
    ],
)

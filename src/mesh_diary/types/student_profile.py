from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, override
from uuid import UUID

from adaptix import P, Retort, loader

from mesh_diary.types.base import BaseType


@dataclass(frozen=True)
class ClassUnit(BaseType):
    id: int
    name: str
    class_level_id: int


@dataclass(frozen=True)
class Curricula(BaseType):
    id: int
    name: str
    class_level_id: int | None = None


@dataclass(frozen=True)
class StudentProfile(BaseType):
    id: int
    person_id: UUID
    school_id: int
    sex: str
    short_name: str
    user_name: str
    age: int
    birth_date: date
    created_at: datetime
    updated_at: datetime
    class_level: int
    class_unit: ClassUnit
    curricula: Curricula
    deleted: bool

    @classmethod
    @override
    def from_data(cls, data: list[dict[str, Any]]) -> StudentProfile:
        return retort.load(data[0], StudentProfile)


retort = Retort(
    recipe=[
        loader(
            P[StudentProfile].birth_date,
            lambda x: datetime.strptime(x, "%d.%m.%Y").date(),
        ),
        loader(
            P[StudentProfile][datetime],
            lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M"),
        ),
        loader(P[StudentProfile].class_level, int),
    ],
)

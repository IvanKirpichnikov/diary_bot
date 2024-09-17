from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, override
from uuid import UUID

from adaptix import P, Retort, loader, name_mapping

from diary.types.base import DiaryType


@dataclass(slots=True, frozen=True)
class UserInfo(DiaryType):
    id: int
    date_birth: date
    gender: str
    guid: UUID
    first_name: str
    last_name: str
    second_name: str

    @classmethod
    @override
    def from_data(cls, data: dict[str, Any]) -> UserInfo:
        return retort.load(data, UserInfo)


retort = Retort(
    recipe=[
        name_mapping(
            UserInfo,
            map={
                "first_name": ["info", "FirstName"],
                "last_name": ["info", "LastName"],
                "second_name": ["info", "MiddleName"],
                "date_birth": ["info", "birthdate"],
                "gender": ["info", "gender"],
                "guid": ["info", "guid"],
                "id": "userId",
            },
        ),
        loader(
            P[UserInfo].date_birth,
            lambda x: datetime.strptime(x, "%d.%m.%Y").date(),
        ),
    ],
)

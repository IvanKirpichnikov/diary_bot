from __future__ import annotations

from collections.abc import Mapping
from datetime import date
from types import TracebackType
from typing import Any, Self, cast, override

from mesh_diary import MeshDiary
from mesh_diary.cache.cache_adapter import (
    CacheAdapter,
    TTLInMemoryCacheAdapter,
)
from mesh_diary.methods.base import BaseMethod
from mesh_diary.methods.get_short_schedules import GetShortSchedules
from mesh_diary.methods.get_student_profile import GetStudentProfile
from mesh_diary.methods.get_user_info import GetUserInfo
from mesh_diary.types.base import BaseType
from mesh_diary.types.short_schedule import ShortSchedule, ShortSchedules
from mesh_diary.types.student_profile import StudentProfile
from mesh_diary.types.user_info import UserInfo

type CacheMap = Mapping[
    type[BaseMethod[Any]],
    CacheAdapter[Any, Any],
]


class MeshDiaryCacheDecorator(MeshDiary):
    def __init__(
        self,
        mesh_diary: MeshDiary,
        cache_map: CacheMap | None = None,
    ) -> None:
        self._mesh_diary = mesh_diary
        if cache_map is None:
            cache_map = {
                GetShortSchedules: TTLInMemoryCacheAdapter(),
                GetUserInfo: TTLInMemoryCacheAdapter(max_size=1, ttl=10_000),
                GetStudentProfile: TTLInMemoryCacheAdapter(
                    max_size=1,
                    ttl=10_000,
                ),
            }
        self._cache_map: Mapping[Any, CacheAdapter[Any, Any]] = cache_map

    @override
    async def __aenter__(self) -> Self:
        return self

    @override
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        await self.close()

    @override
    async def send_request[MT: BaseType](
        self,
        method: BaseMethod[MT],
    ) -> MT:
        return await self._mesh_diary.send_request(method)

    @override
    async def close(self) -> None:
        await self._mesh_diary.close()

    @override
    async def get_student_profile(self) -> StudentProfile:
        identity_map = cast(
            TTLInMemoryCacheAdapter[None, StudentProfile],
            self._cache_map[GetStudentProfile],
        )

        cache_student_profile = identity_map.get(None)
        if cache_student_profile:
            return cache_student_profile

        student_profile = await self._mesh_diary.get_student_profile()
        identity_map.set(None, student_profile)
        return student_profile

    @override
    async def get_user_info(self) -> UserInfo:
        identity_map = cast(
            TTLInMemoryCacheAdapter[None, UserInfo],
            self._cache_map[GetUserInfo],
        )

        cache_user_info = identity_map.get(None)
        if cache_user_info:
            return cache_user_info

        user_info = await self._mesh_diary.get_user_info()
        identity_map.set(None, user_info)
        return user_info

    @override
    async def get_short_schedules(
        self,
        dates: list[date],
    ) -> ShortSchedules:
        identity_map = cast(
            TTLInMemoryCacheAdapter[date, ShortSchedule],
            self._cache_map[GetShortSchedules],
        )

        cache_schedules: list[ShortSchedule | None] = []
        for date_ in dates.copy():
            cache_schedule = identity_map.get(date_)
            cache_schedules.append(cache_schedule)
            if cache_schedule:
                dates.remove(date_)

        if all(cache_schedules):
            return ShortSchedules(cast(list[ShortSchedule], cache_schedules))

        schedules = await self._mesh_diary.get_short_schedules(dates)
        for schedule in schedules.schedules:
            identity_map.set(schedule.date, schedule)
            none_index = cache_schedules.index(None)
            cache_schedules[none_index] = schedule
        return ShortSchedules(cast(list[ShortSchedule], cache_schedules))

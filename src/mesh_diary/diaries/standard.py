from __future__ import annotations

from datetime import date
from types import TracebackType
from typing import Self, override

from mesh_diary.cache.diary_decorator import CacheMap, MeshDiaryCacheDecorator
from mesh_diary.diaries.base import MeshDiary
from mesh_diary.methods.base import BaseMethod
from mesh_diary.methods.get_short_schedules import GetShortSchedules
from mesh_diary.methods.get_student_profile import GetStudentProfile
from mesh_diary.methods.get_user_info import GetUserInfo
from mesh_diary.sessions.aiohttp import AiohttpSession
from mesh_diary.sessions.base import BaseSession
from mesh_diary.types.base import BaseType
from mesh_diary.types.short_schedule import ShortSchedules
from mesh_diary.types.student_profile import StudentProfile
from mesh_diary.types.user_info import UserInfo


class MeshDiaryStandard(MeshDiary):
    def __init__(
        self,
        authorization_token: str,
        session: BaseSession,
        student_profile_id: int,
    ) -> None:
        self._session = session
        self._student_profile_id = student_profile_id
        self._authorization_token = authorization_token

    @override
    async def send_request[MT: BaseType](
        self,
        method: BaseMethod[MT],
    ) -> MT:
        return await self._session.send_request(method)

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
    async def close(self) -> None:
        await self._session.close()

    @override
    async def get_student_profile(self) -> StudentProfile:
        method = GetStudentProfile(
            authorization_token=self._authorization_token,
        )
        return await self.send_request(method)

    @override
    async def get_user_info(self) -> UserInfo:
        method = GetUserInfo(
            authorization_token=self._authorization_token,
        )
        return await self.send_request(method)

    @override
    async def get_short_schedules(
        self,
        dates: list[date],
    ) -> ShortSchedules:
        method = GetShortSchedules(
            dates=dates,
            student_id=self._student_profile_id,
            authorization_token=self._authorization_token,
        )
        return await self.send_request(method)


async def create_mesh_diary(
    authorization_token: str,
    session: BaseSession | None = None,
    cache: bool = True,
    cache_map: CacheMap | None = None,
) -> MeshDiary:
    if session is None:
        session = AiohttpSession()

    student_profile = await session.send_request(
        GetStudentProfile(
            authorization_token=authorization_token,
        ),
    )
    mesh_diary = MeshDiaryStandard(
        session=session,
        authorization_token=authorization_token,
        student_profile_id=student_profile.id,
    )
    if cache:
        return MeshDiaryCacheDecorator(
            mesh_diary=mesh_diary,
            cache_map=cache_map,
        )
    return mesh_diary

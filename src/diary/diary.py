from contextlib import asynccontextmanager
from datetime import date
from types import TracebackType
from typing import AsyncIterable, Self

from diary.methods.base import DiaryMethod
from diary.methods.get_short_schedules import GetShortSchedules
from diary.methods.get_student_profile import GetStudentProfile
from diary.methods.get_user_info import GetUserInfo
from diary.sessions.aiohttp import AiohttpSession
from diary.sessions.base import BaseSession
from diary.types.base import DiaryType
from diary.types.short_schedule import ShortSchedules
from diary.types.student_profile import StudentProfile
from diary.types.user_info import UserInfo


class Diary:
    def __init__(
        self,
        bearer_token: str,
        session: BaseSession | None = None,
    ) -> None:
        self._bearer_token = bearer_token
        self._student_profile = None
        
        if session is None:
            session = AiohttpSession()
        self._session = session
    
    async def send_request[MT: DiaryType](
        self,
        method: DiaryMethod[MT],
    ) -> MT:
        return await self._session.send_request(method)
    
    async def __aenter__(self) -> Self:
        return self
    
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        await self._session.close()
    
    async def close(self) -> None:
        await self._session.close()
    
    async def get_student_profile(self) -> StudentProfile:
        method = GetStudentProfile(
            bearer_token=self._bearer_token,
        )
        return await self.send_request(method)
    
    async def get_user_info(self) -> UserInfo:
        method = GetUserInfo(
            bearer_token=self._bearer_token,
        )
        return await self.send_request(method)
    
    async def get_short_schedules(
        self,
        dates: list[date],
    ) -> ShortSchedules:
        if self._student_profile is None:
            raise ValueError
        
        method = GetShortSchedules(
            dates=dates,
            student_id=self._student_profile.id,
            bearer_token=self._bearer_token,
        )
        return await self.send_request(method)


@asynccontextmanager
async def create_diary(
    bearer_token: str,
    session: BaseSession | None = None,
) -> AsyncIterable[Diary]:
    async with Diary(
        session=session,
        bearer_token=bearer_token,
    ) as diary_object:
        student_profile = await diary_object.get_student_profile()
        diary_object._student_profile = student_profile  # noqa: SLF001
        yield diary_object

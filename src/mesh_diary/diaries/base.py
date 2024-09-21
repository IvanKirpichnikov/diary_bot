from abc import abstractmethod
from datetime import date
from types import TracebackType
from typing import Protocol, Self

from mesh_diary.methods import BaseMethod
from mesh_diary.types import BaseType, ShortSchedules, StudentProfile, UserInfo


class MeshDiary(Protocol):
    @abstractmethod
    async def send_request[MT: BaseType](
        self,
        method: BaseMethod[MT],
    ) -> MT:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    # sugar
    @abstractmethod
    async def get_student_profile(self) -> StudentProfile:
        raise NotImplementedError

    @abstractmethod
    async def get_user_info(self) -> UserInfo:
        raise NotImplementedError

    @abstractmethod
    async def get_short_schedules(
        self,
        dates: list[date],
    ) -> ShortSchedules:
        raise NotImplementedError

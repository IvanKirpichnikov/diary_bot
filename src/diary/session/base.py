from abc import abstractmethod
from asyncio import Protocol
from typing import Any, cast

from diary.methods.base import DiaryMethod
from diary.types.base import DiaryType


class BaseSession(Protocol):
    @abstractmethod
    async def _send_request[MT: DiaryType](
        self,
        method: DiaryMethod[MT],
    ) -> Any:
        raise NotImplementedError

    async def send_request[MT: DiaryType](
        self,
        method: DiaryMethod[MT],
    ) -> MT:
        data = await self._send_request(method)
        return cast(MT, method.__returning__.from_data(data))

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

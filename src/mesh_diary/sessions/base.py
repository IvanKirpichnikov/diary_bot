from abc import abstractmethod
from asyncio import Protocol
from typing import Any, cast

from mesh_diary.methods.base import BaseMethod
from mesh_diary.types.base import BaseType


class BaseSession(Protocol):
    @abstractmethod
    async def _send_request[MT: BaseType](
        self,
        method: BaseMethod[MT],
    ) -> Any:
        raise NotImplementedError

    async def send_request[MT: BaseType](
        self,
        method: BaseMethod[MT],
    ) -> MT:
        data = await self._send_request(method)
        return cast(MT, method.__returning__.from_data(data))

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

from typing import Any, override

from aiohttp import ClientSession

from mesh_diary.methods.base import BaseMethod
from mesh_diary.sessions.base import BaseSession
from mesh_diary.types.base import BaseType


class AiohttpSession(BaseSession):
    def __init__(self) -> None:
        self._session = ClientSession()

    @override
    async def _send_request[MT: BaseType](
        self,
        method: BaseMethod[MT],
    ) -> Any:
        if method.__http_method_type__ == "get":
            http_method = self._session.get
        elif method.__http_method_type__ == "post":
            http_method = self._session.post

        request_context = method.build_request_context()
        async with http_method(
            url=method.__url__,
            data=request_context.body,
            headers=request_context.headers,
            params=request_context.query_params,
        ) as response:
            return await response.json(encoding="utf-8")

    @override
    async def close(self) -> None:
        await self._session.close()

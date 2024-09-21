from abc import abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class HTTPMethodType(StrEnum):
    GET = "get"
    POST = "post"


@dataclass(frozen=True)
class RequestContext:
    body: dict[str, str] | None = None
    headers: dict[str, str] | None = None
    query_params: dict[str, str] | None = None


class BaseMethod[T](Protocol):
    __url__: str
    __returning__: type[T]
    __http_method_type__: HTTPMethodType

    @abstractmethod
    def build_request_context(self) -> RequestContext:
        raise NotImplementedError

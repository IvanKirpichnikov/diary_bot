from abc import abstractmethod
from dataclasses import dataclass
from typing import Literal, Protocol


@dataclass(frozen=True)
class RequestContext:
    body: dict[str, str] | None = None
    headers: dict[str, str] | None = None
    query_params: dict[str, str] | None = None


class DiaryMethod[T](Protocol):
    __url__: str
    __returning__: type[T]
    __http_method_type__: Literal["get", "post"]

    @abstractmethod
    def build_request_context(self) -> RequestContext:
        raise NotImplementedError

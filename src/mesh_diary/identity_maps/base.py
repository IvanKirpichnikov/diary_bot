from abc import abstractmethod
from collections.abc import Hashable
from typing import Protocol

from mesh_diary.types import BaseType


class IdentityMap[KT: Hashable, VT: BaseType](Protocol):
    @abstractmethod
    def get(self, key: KT) -> VT | None:
        raise NotImplementedError

    @abstractmethod
    def set(self, key: KT, value: VT) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: KT) -> None:
        raise NotImplementedError

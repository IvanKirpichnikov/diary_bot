from collections.abc import Hashable, MutableMapping
from typing import override

from cachetools import TTLCache

from mesh_diary.identity_maps.base import IdentityMap
from mesh_diary.types import BaseType


class TTLIdentityMap[KT: Hashable, VT: BaseType](IdentityMap[KT, VT]):
    _cache: MutableMapping[KT, VT]

    def __init__(
        self,
        max_size: int = 10000,
        ttl: int = 1000,
    ) -> None:
        self._cache = TTLCache(
            maxsize=max_size,
            ttl=ttl,
        )

    @override
    def get(self, key: KT) -> VT | None:
        return self._cache.get(key)

    @override
    def set(self, key: KT, value: VT) -> None:
        self._cache[key] = value

    @override
    def delete(self, key: KT) -> None:
        del self._cache[key]

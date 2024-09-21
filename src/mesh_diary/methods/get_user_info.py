from dataclasses import dataclass
from typing import override

from mesh_diary.methods.base import (
    BaseMethod,
    HTTPMethodType,
    RequestContext,
)
from mesh_diary.types.user_info import UserInfo


@dataclass(frozen=True)
class GetUserInfo(BaseMethod[UserInfo]):
    __returning__ = UserInfo
    __http_method_type__ = HTTPMethodType.GET
    __url__ = "https://school.mos.ru/v3/userinfo"

    authorization_token: str

    @override
    def build_request_context(self) -> RequestContext:
        return RequestContext(
            headers={
                "Authorization": f"Bearer {self.authorization_token}",
            },
        )

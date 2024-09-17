from dataclasses import dataclass
from typing import override

from diary.methods.base import DiaryMethod, RequestContext
from diary.types.user_info import UserInfo


@dataclass(frozen=True)
class GetUserInfo(DiaryMethod[UserInfo]):
    __returning__ = UserInfo
    __http_method_type__ = "get"
    __url__ = "https://school.mos.ru/v3/userinfo"

    bearer_token: str

    @override
    def build_request_context(self) -> RequestContext:
        return RequestContext(
            headers={
                "Authorization": f"Bearer {self.bearer_token}",
            },
        )

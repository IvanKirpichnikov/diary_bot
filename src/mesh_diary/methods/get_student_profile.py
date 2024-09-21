from dataclasses import dataclass
from typing import override

from mesh_diary.methods.base import (
    BaseMethod,
    HTTPMethodType,
    RequestContext,
)
from mesh_diary.types.student_profile import StudentProfile


@dataclass(frozen=True)
class GetStudentProfile(BaseMethod[StudentProfile]):
    __returning__ = StudentProfile
    __http_method_type__ = HTTPMethodType.GET
    __url__ = "https://dnevnik.mos.ru/core/api/student_profiles"

    authorization_token: str

    @override
    def build_request_context(self) -> RequestContext:
        return RequestContext(
            headers={
                "Auth-Token": self.authorization_token,
            },
        )

from dataclasses import dataclass
from typing import override

from diary.methods.base import DiaryMethod, RequestContext
from diary.types.student_profile import StudentProfile


@dataclass(frozen=True)
class GetStudentProfile(DiaryMethod[StudentProfile]):
    __http_method_type__ = "get"
    __returning__ = StudentProfile
    __url__ = "https://dnevnik.mos.ru/core/api/student_profiles"

    bearer_token: str

    @override
    def build_request_context(self) -> RequestContext:
        return RequestContext(
            headers={
                "Auth-Token": self.bearer_token,
            },
        )

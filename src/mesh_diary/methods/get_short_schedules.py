from dataclasses import dataclass
from datetime import date
from typing import override

from mesh_diary.methods.base import (
    BaseMethod,
    HTTPMethodType,
    RequestContext,
)
from mesh_diary.types.short_schedule import ShortSchedules


@dataclass(frozen=True)
class GetShortSchedules(BaseMethod[ShortSchedules]):
    __returning__ = ShortSchedules
    __http_method_type__ = HTTPMethodType.GET
    __url__ = "https://school.mos.ru/api/family/web/v1/schedule/short"

    student_id: int
    dates: list[date]
    authorization_token: str

    def __post_init__(self) -> None:
        if not self.dates:
            raise ValueError(
                "Number of dates must be greater than 0. %r" % self.dates,
            )

    @override
    def build_request_context(self) -> RequestContext:
        return RequestContext(
            headers={
                "Authorization": f"Bearer {self.authorization_token}",
                "X-mes-subsystem": "familyweb",
            },
            query_params={
                "student_id": str(self.student_id),
                "dates": ",".join(
                    [date_.strftime("%Y-%m-%d") for date_ in self.dates],
                ),
            },
        )

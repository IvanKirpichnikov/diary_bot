from dataclasses import dataclass
from datetime import date
from typing import override

from diary.methods.base import DiaryMethod, RequestContext
from diary.types.short_schedule import ShortSchedules


@dataclass(frozen=True)
class GetShortSchedules(DiaryMethod[ShortSchedules]):
    __http_method_type__ = "get"
    __returning__ = ShortSchedules
    __url__ = "https://school.mos.ru/api/family/web/v1/schedule/short"

    student_id: int
    bearer_token: str
    dates: list[date]

    def __post_init__(self) -> None:
        if not self.dates:
            raise ValueError("Number of dates must be greater than 0")

    @override
    def build_request_context(self) -> RequestContext:
        return RequestContext(
            headers={
                "Authorization": f"Bearer {self.bearer_token}",
                "X-mes-subsystem": "familyweb",
            },
            query_params={
                "student_id": str(self.student_id),
                "dates": ",".join(
                    [date_.strftime("%Y-%m-%d") for date_ in self.dates],
                ),
            },
        )

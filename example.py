import asyncio
from datetime import datetime

from diary.diary import create_diary


BEARER_TOKEN = ''


async def main():
    async with create_diary(BEARER_TOKEN) as diary:
        print(
            await diary.get_short_schedules(
                [datetime.now().date()]
            )
        )
        print(await diary.get_student_profile())
        print(await diary.get_user_info())


asyncio.run(main())

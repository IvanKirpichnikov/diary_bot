import asyncio
from datetime import datetime

from mesh_diary import create_mesh_diary

BEARER_TOKEN = ""


async def main() -> None:
    diary = await create_mesh_diary(BEARER_TOKEN)

    print(await diary.get_student_profile())
    print(await diary.get_user_info())
    print(
        await diary.get_short_schedules(
            [datetime.now().date()],
        ),
    )

    await diary.close()


asyncio.run(main())

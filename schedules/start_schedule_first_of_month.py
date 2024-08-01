import asyncio
from datetime import timedelta

from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleIntervalSpec,
    ScheduleCalendarSpec,
    ScheduleRange,
    ScheduleSpec,
    ScheduleState,
)
from your_workflows import YourSchedulesWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    await client.create_schedule(
        "workflow-schedule-id-first-of-month",
        Schedule(
            action=ScheduleActionStartWorkflow(
                YourSchedulesWorkflow.run,
                "my schedule arg",
                id="schedules-workflow-id",
                task_queue="schedules-task-queue",
            ),
            spec=ScheduleSpec(
                calendars=[ScheduleCalendarSpec(day_of_month=(ScheduleRange(1,),))]
            ),
            state=ScheduleState(note="Here's a note on my Schedule."),
        ),
    )


if __name__ == "__main__":
    asyncio.run(main())

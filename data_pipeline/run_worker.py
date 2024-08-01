import asyncio

from temporalio.client import Client
from temporalio.worker import Worker
from activities import your_activity, extract, validate, transform, load, poll
from data_pipeline.data_pipeline_workflows import YourSchedulesWorkflow, DataPipelineWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="data-pipeline-task-queue",
        workflows=[YourSchedulesWorkflow, DataPipelineWorkflow], 
        activities=[your_activity, extract, validate, transform, load, poll],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

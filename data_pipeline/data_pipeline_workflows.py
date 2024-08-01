import logging
from datetime import timedelta

from temporalio import workflow

from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from data_pipeline.activities import your_activity, extract, validate, transform, load, poll
    from data_pipeline.dataobjects import YourParams, DataPipelineParams


@workflow.defn
class YourSchedulesWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            your_activity,
            YourParams("Hello", name),
            start_to_close_timeout=timedelta(seconds=10),
        )

@workflow.defn
class DataPipelineWorkflow:
    @workflow.run
    async def run(self, input: DataPipelineParams) -> str:
        logging.info(f"The data pipeline for {input} beginning.")
        #   [ ] multiple files for the heartbeats?
        #   [ ] wait for signal version
        
        validation = await workflow.execute_activity(
            validate, input, start_to_close_timeout=timedelta(seconds=300), heartbeat_timeout=timedelta(seconds=20)
        )
        if validation == False:
            logging.info(f"Validation rejected for: {input.input_filename}")
            return "invalidated"


        activity_output = await workflow.execute_activity(
            extract, input, start_to_close_timeout=timedelta(seconds=300), heartbeat_timeout=timedelta(seconds=20)
        )
        logging.info(f"Extract status: {input.input_filename}: {activity_output}")


        activity_output = await workflow.execute_activity(
            transform, input, start_to_close_timeout=timedelta(seconds=300), heartbeat_timeout=timedelta(seconds=20)
        )
        logging.info(f"Transform status: {input.input_filename}: {activity_output}")

        activity_output = await workflow.execute_activity(
            load, input, start_to_close_timeout=timedelta(seconds=300), heartbeat_timeout=timedelta(seconds=20)
        )
        logging.info(f"Load status: {input.input_filename}: {activity_output}")

        # it's ok if this activity fails: it is polling every 2 seconds
        # see https://community.temporal.io/t/what-is-the-best-practice-for-a-polling-activity/328/2
        activity_output = await workflow.execute_activity(
            poll, input, start_to_close_timeout=timedelta(seconds=3000), heartbeat_timeout=timedelta(seconds=20), 
            retry_policy=RetryPolicy(initial_interval=timedelta(seconds=2), backoff_coefficient=1)

        )
        logging.info(f"Poll status: {input.input_filename}: {activity_output}")

        
        return f"Successfully processed: {input.input_filename}!"
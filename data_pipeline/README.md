# Data Pipeline example

These samples show how one might create a data pipeline.

To run, first see [README.md](../README.md) for prerequisites. Then, run the following from this directory to run the `data_pipeline/` sample:

    poetry run python run_worker.py
    poetry run python start_data_pipeline.py

In separate terminals

You can also demonstrate it waiting for a signal with:

    poetry run python run_worker.py
    poetry run python start_data_pipeline_wait_signal.py
    poetry run python signal_load_complete.py

All in separate terminals.
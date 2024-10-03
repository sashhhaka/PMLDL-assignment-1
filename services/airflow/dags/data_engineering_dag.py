from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
import os
import pendulum
from datetime import timedelta

project_root = os.environ.get("PROJECT_DIR")
os.chdir(project_root)

# Define your start date
start_date = pendulum.now(tz="Europe/Moscow").subtract(minutes=5)
start_date = start_date.replace(second=0, microsecond=0)

# Define the DAG
with DAG(
    dag_id="data_pipeline_dag",
    description="A data pipeline DAG for cleaning and splitting data",
    schedule_interval=timedelta(minutes=5),
    start_date=start_date,
    tags=["data processing"],
    is_paused_upon_creation=False,
) as dag:

    # Task 1: Load Data (this task is not explicitly required in the pipeline as data is loaded in the next steps)
    load_task = BashOperator(
        task_id='load_data',
        bash_command='python code/datasets/data_preprocessing.py load data/raw/raw_data.csv',
        cwd=project_root,
    )

    # Task 2: Clean Data
    clean_task = BashOperator(
        task_id='clean_data',
        bash_command='python code/datasets/data_preprocessing.py clean data/raw/raw_data.csv data/processed/cleaned_data.csv',
        cwd=project_root,
    )

    # Task 3: Split Data and Save
    split_task = BashOperator(
        task_id='split_data',
        bash_command='python code/datasets/data_preprocessing.py split_and_save data/raw/raw_data.csv data/processed/cleaned_data.csv data/processed/train_data.csv data/processed/test_data.csv',
        cwd=project_root,
    )

    # Set task dependencies
    load_task >> clean_task >> split_task

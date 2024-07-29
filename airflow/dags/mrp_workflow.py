from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os
import subprocess

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'mrp_workflow',
    default_args=default_args,
    description='Materials Requirement Planning Workflow',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Get the path to the main folder
main_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Path to your scripts
server_script_path = os.path.join(main_folder, 'backend', 'server.py')
mrp_calculations_script_path = os.path.join(main_folder, 'backend', 'mrp_calculations.py')

# Task 1: Run server.py to load data into SQL Server
def run_server_script():
    subprocess.run(['python', server_script_path], check=True)

run_server_task = PythonOperator(
    task_id='run_server_script',
    python_callable=run_server_script,
    dag=dag,
)

# Task 2: Run mrp_calculations.py to perform MRP calculations
def run_mrp_calculations_script():
    subprocess.run(['python', mrp_calculations_script_path], check=True)

run_mrp_calculations_task = PythonOperator(
    task_id='run_mrp_calculations_script',
    python_callable=run_mrp_calculations_script,
    dag=dag,
)

# Set up task dependencies
run_server_task >> run_mrp_calculations_task

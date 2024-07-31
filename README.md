# Materials Requirement Planning (MRP): Explosion Calculus

This repository demonstrates a Materials Requirement Planning (MRP) backend system using Apache Airflow for workflow automation and monitoring, Docker for containerization, and Microsoft SQL Server on Azure Cloud Platform for database management. The frontend system is orchestrated via Tableau with a connection to the Azure backend server. 

Our project is also designed to be modular in nature, where every component or tool used to develop this backend service can be easily replaced without major faults in the overall system. For example, users can opt to host their database locally using a `MySQL` connection on `localhost` and serve their own database solutions. 

## Project Structure

```plaintext
mso-esa-2d/
│
├── .venv/
│
├── src/
│   ├── server.py
│   └── mrp_calculations.py
│
├── data/
│   └── data.xlsx
│
├── airflow/
│   └── dags/
│       └── mrp_workflow.py 
│
├── .env
├── .gitignore
├── requirements.txt
├── .dockerignore
├── Dockerfile.server
├── Dockerfile.mrp_calculations
├── docker-compose.yml
├── README.md
└── requirements.txt
```
## System Architecture

![System Architecture Diagram](https://github.com/michael-hoon/mso-esa-2d/blob/main/Images/mso_architecture.jpg)

## Components

### Backend

- `server.py`: This script reads data from an Excel file (or in production situations, fetching from an API) and loads it into a Microsoft Azure SQL Server database.
- `mrp_calculations.py`: This script reads data from the SQL Server, performs MRP calculations using Pandas, and writes the results back to the SQL Server.

### Airflow

- `mrp_workflow_dag.py`: Defines the Airflow Directed Acyclic Graph (DAG) to automate the execution of `server.py` and `mrp_calculations.py`. For more information, vist the [official Gihub Repository](https://github.com/apache/airflow).

### Docker

- `Dockerfile.server`: Dockerfile to create an image for the server.py script.
- `Dockerfile.mrp_calculations`: Dockerfile to create an image for the `mrp_calculations.py` script.
- `docker-compose.yml`: Docker Compose configuration to orchestrate the services.

## Getting Started

### Prerequisites

- Docker ([Windows](https://docs.docker.com/desktop/install/windows-install/)) ([MacOS](https://docs.docker.com/desktop/install/mac-install/)) ([Linux](https://docs.docker.com/engine/install/))
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.10+](https://www.python.org/downloads/)
- Apache Airflow ([PyPI](https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html)) ([Official Docker Image](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html#using-production-docker-images) - For Production use)
### Setting Up the Environment (Using Docker)

#### 1. Clone the repository:

    git clone https://github.com/michael-hoon/mso-esa-2d.git
    cd mso-esa-2d

#### 2. Install all required dependencies for the system

    pip install -r requirements.txt

#### 3. Create and configure the .env file:
Create a .env file in the main directory with your Azure database credentials.

    DB_SERVER=your_db_server
    DB_DATABASE=your_db_name
    DB_USERNAME=your_db_username
    DB_PASSWORD=your_db_password

#### 4. Build the Docker images:

    docker-compose build

#### 5. Start the services:

    docker-compose up -d

#### 6. Access Airflow Web UI:

If you want Airflow to be containerised for production environments, [follow the instructions in the official source documentation here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html). Note that for production environments, Airflow suggests using [Kubernetes as an orchestration tool](https://airflow.apache.org/docs/helm-chart/stable/index.html) instead as Docker is not officially supported yet.

### Setting Up the Environment (Using Local Install)

#### 1. Clone the repository:

    git clone https://github.com/michael-hoon/mso-esa-2d.git
    cd mso-esa-2d

#### 2. Install all required dependencies for the system

    pip install -r requirements.txt

#### 3. Create and configure the .env file:
Create a .env file in the main directory with your database credentials.

    DB_SERVER=your_db_server
    DB_DATABASE=your_db_name
    DB_USERNAME=your_db_username
    DB_PASSWORD=your_db_password

#### 4. Access Airflow Web UI:

Ensure that the $PATH directory for your DAGs is set to the current directory under `airflow/dags/`. Do this by navigating to the folder where Airflow is installed (if via PyPI, it should be under `/home/user/airflow/`) and modify the variable `dags_folder` to `~/mso-esa-2d/airflow/dags` (for Linux systems):

    cd /home/user/airflow
    vim airflow.cfg

Now, set up an airflow administrative user

    airflow users create --username admin --firstname FIRST_NAME --lastname LAST_NAME --role Admin --email admin@example.com --password YOUR_PASSWORD

Once completed, setup the Airflow scheduler service in another terminal instance

    airflow scheduler

and run the web service in the original terminal instance

    airflow webserver --port 8080

Navigate to http://localhost:8080 to access the Airflow web interface. Use the admin credentials to log in if prompted.

### Airflow UI

Airflow will serve as an **orchestration and automated monitoring tool** for the backend system. The `server.py` and `mrp_calculations.py` scripts are set to automatically run at a daily interval via Apache Airflow, and the user need not run anything manually aside from the Airflow service below once.

![Airflow UI Example](https://github.com/michael-hoon/mso-esa-2d/blob/main/Images/airflow_ui.png)

![Airflow UI Monitoring](https://github.com/michael-hoon/mso-esa-2d/blob/main/Images/airflow_ui_zoomed.png)

The figures above show an example automated scheduling workflow, tracking days where the MRP system is down or unavailable to the end user. The Airflow user can then arrange for automated emails to be sent to the team to notify them about downtimes and potential faults of the system.

### Project Workflow (Automated Process via Apache Airflow)

#### 1. Load Data into SQL Server:

The server.py script reads data from data/data.xlsx (if productionised, will fetch from an external API connection) and loads it into the Microsoft Azure SQL Server database.

#### 2. Perform MRP Calculations:

The mrp_calculations.py script reads data from the SQL Server, performs MRP calculations, and writes the results back to the SQL Server.

#### 3. Automation with Airflow:

The Airflow DAG (mrp_workflow_dag.py) automates the execution of the above scripts.

## Directory and Files

- `/data/data.xlsx`: Contains the input data files.
- `src/server.py`: Script to load data into SQL Server.
- `src/mrp_calculations.py`: Script to perform MRP calculations.
- `.env`: Environment variables for database connection.
- `requirements.txt`: Python dependencies.
- `airflow/dags/mrp_workflow_dag.py`: Script to define Airflow DAG for the MRP workflow.
- `Dockerfile.server`: Dockerfile for the server.py script.
- `Dockerfile.mrp_calculations`: Dockerfile for the mrp_calculations.py script.
- `docker-compose.yml`: Docker Compose configuration file.
- `Images`: Folder to store images for the README file.

## Contributing

Our project is a free and open sourced solution, under the MIT License. Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License. See `LICENSE.txt` for more information. <p align="right">(<a href="#readme-top">back to top</a>)</p>
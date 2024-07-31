# Materials Requirement Planning (MRP) Project

This project demonstrates a Materials Requirement Planning (MRP) backend system using Apache Airflow for workflow automation and monitoring, Docker for containerization, and Microsoft SQL Server on Azure Cloud Platform for database management. The frontend system is orchestrated via Tableau with a connection to the Azure backend server. 

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

## Components

### Backend

- `server.py`: This script reads data from an Excel file (or in production situations, fetching from an API) and loads it into a Microsoft Azure SQL Server database.
- `mrp_calculations.py`: This script reads data from the SQL Server, performs MRP calculations using Pandas, and writes the results back to the SQL Server.

### Airflow

- `mrp_workflow_dag.py`: Defines the Airflow Directed Acyclic Graph (DAG) to automate the execution of `server.py` and `mrp_calculations.py`. 

### Docker

- `Dockerfile.server`: Dockerfile to create an image for the server.py script.
- `Dockerfile.mrp_calculations`: Dockerfile to create an image for the `mrp_calculations.py` script.
- `docker-compose.yml`: Docker Compose configuration to orchestrate the services.

## Getting Started

### Prerequisites

- [Docker]()
- [Docker Compose]()
- [Python 3.10+]()
- [Apache Airflow]()

### Setting Up the Environment (Using Docker)

#### 1. Clone the repository:

    git clone https://github.com/michael-hoon/mso-esa-2d.git
    cd mso-esa-2d

#### 2. Create and configure the .env file:
Create a .env file in the backend/ directory with your database credentials.

    DB_SERVER=your_db_server
    DB_DATABASE=your_db_name
    DB_USERNAME=your_db_username
    DB_PASSWORD=your_db_password

#### 3. Build the Docker images:

    docker-compose build

#### 4. Start the services:

    docker-compose up -d

#### 5. Access Airflow Web UI:

Navigate to http://localhost:8080 to access the Airflow web interface. Use the credentials admin for both the username and password. The airflow interface will look like: 

### Setting Up the Environment (Using Local Install)

#### 1. Clone the repository:

    git clone https://github.com/michael-hoon/mso-esa-2d.git
    cd mso-esa-2d

#### 2. Create and configure the .env file:
Create a .env file in the backend/ directory with your database credentials.

    DB_SERVER=your_db_server
    DB_DATABASE=your_db_name
    DB_USERNAME=your_db_username
    DB_PASSWORD=your_db_password

#### 3. Build the Docker images:

    docker-compose build

#### 4. Start the services:

    docker-compose up -d

#### 5. Access Airflow Web UI:

Navigate to http://localhost:8080 to access the Airflow web interface. Use the credentials admin for both the username and password.

### Project Workflow

#### 1. Load Data into SQL Server:

The server.py script reads data from data/data.xlsx and loads it into the SQL Server database.

#### 2. Perform MRP Calculations:

The mrp_calculations.py script reads data from the SQL Server, performs MRP calculations, and writes the results back to the SQL Server.

#### 3. Automation with Airflow:

The Airflow DAG (mrp_workflow_dag.py) automates the execution of the above scripts.

## Directory and Files

- backend/data: Contains the input data files.
- backend/server.py: Script to load data into SQL Server.
- backend/mrp_calculations.py: Script to perform MRP calculations.
- backend/.env: Environment variables for database connection.
- backend/requirements.txt: Python dependencies.
- dags/mrp_workflow_dag.py: Airflow DAG for the MRP workflow.
- logs/: Directory for Airflow logs.
- plugins/: Directory for any custom Airflow plugins.
- Dockerfile.server: Dockerfile for the server.py script.
- Dockerfile.mrp_calculations: Dockerfile for the mrp_calculations.py script.
- docker-compose.yml: Docker Compose configuration file.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License.
# Materials Requirement Planning (MRP) Project

This project demonstrates a Materials Requirement Planning (MRP) system using Apache Airflow for workflow automation and monitoring, Docker for containerization, and Microsoft SQL Server for database management.

## Project Structure

```plaintext
mrp_project/
│
├── backend/
│   ├── data/
│   │   └── data.xlsx
│   ├── __init__.py
│   ├── server.py
│   ├── mrp_calculations.py
│   ├── .env
│   └── requirements.txt
│
├── dags/
│   └── mrp_workflow_dag.py
│
├── logs/
│
├── plugins/
│
├── Dockerfile.server
├── Dockerfile.mrp_calculations
├── docker-compose.yml
└── README.md
```

## Components

### Backend

- `server.py`: This script reads data from an Excel file and loads it into a Microsoft SQL Server database.
- `mrp_calculations.py`: This script reads data from the SQL Server, performs MRP calculations using Pandas, and writes the results back to the SQL Server.

### Airflow

- `mrp_workflow_dag.py`: Defines the Airflow DAG to automate the execution of `server.py` and `mrp_calculations.py`.

### Docker

- `Dockerfile.server`: Dockerfile to create an image for the server.py script.
- `Dockerfile.mrp_calculations`: Dockerfile to create an image for the `mrp_calculations.py` script.
- `docker-compose.yml`: Docker Compose configuration to orchestrate the services.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.9+

### Setting Up the Environment

#### 1. Clone the repository:

    git clone https://github.com/yourusername/mrp_project.git
    cd mrp_project

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
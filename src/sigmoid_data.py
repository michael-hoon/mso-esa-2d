import pandas as pd
from sqlalchemy import create_engine
import urllib

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# read sigmoid data
main_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
excel_path = os.path.join(main_folder, 'data', 'Sigmoid Range.xlsx')

sigmoid_data = pd.read_excel(excel_path)

# Fetch database details from environment variables
server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
driver = 'ODBC Driver 17 for SQL Server'

connection_string = f'mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus("DRIVER={"+driver+"};SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password)}'

engine = create_engine(connection_string)

sigmoid_data.to_sql('Sigmoid Range', engine, if_exists='replace', index=False)

print("Sigmoid data loaded successfully")
import pandas as pd
from sqlalchemy import create_engine
import urllib

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the path to the main folder
main_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Path to excel data
excel_path = os.path.join(main_folder, 'data', 'data.xlsx')

sheets = ['PartMasterRecord', 'BOM', 'DemandForecast', 'Inventory', 'SchReceipt']
dataframes = {}

# Fetch database details from environment variables
server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
driver = 'ODBC Driver 17 for SQL Server'

connection_string = f'mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus("DRIVER={"+driver+"};SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password)}'

for sheet in sheets:
    dataframes[sheet] = pd.read_excel(excel_path, sheet_name=sheet)

dataframes['PartMasterRecord']['LeadTime'] = pd.to_numeric(dataframes['PartMasterRecord']['LeadTime'], errors='coerce')
dataframes['DemandForecast']['Week'] = pd.to_numeric(dataframes['DemandForecast']['Week'], errors='coerce')

# Set up MySQL connection 
# engine = create_engine(mysql_host)

engine = create_engine(connection_string)

# Write dataframes to MySQL
for sheet, df in dataframes.items():
    df.to_sql(sheet, engine, if_exists='replace', index=False)
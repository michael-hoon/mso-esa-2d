import pandas as pd
from sqlalchemy import create_engine
import urllib

# Read excel file
excel_path = "data/data.xlsx"
sheets = ['PartMasterRecord', 'BOM', 'DemandForecast', 'Inventory', 'SchReceipt']
dataframes = {}

# mysql_host = ''
server = 'msotest.database.windows.net'
database = 'msotest'
username = 'micha'
password = '2709'
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
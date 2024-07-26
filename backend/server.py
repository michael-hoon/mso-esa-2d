import pandas as pd
from sqlalchemy import create_engine

# Read excel file
excel_path = "data.xlsx"
sheets = ['PartMasterRecord', 'BOM', 'DemandForecast', 'Inventory', 'SchReceipt']
dataframes = {}

mysql_host = 'mysql+mysqlconnector://root:2709@localhost/msoesatest'

for sheet in sheets:
    dataframes[sheet] = pd.read_excel(excel_path, sheet_name=sheet)

dataframes['PartMasterRecord']['LeadTime'] = pd.to_numeric(dataframes['PartMasterRecord']['LeadTime'], errors='coerce')
dataframes['DemandForecast']['Week'] = pd.to_numeric(dataframes['DemandForecast']['Week'], errors='coerce')

# Set up MySQL connection 
engine = create_engine(mysql_host)

# Write dataframes to MySQL
for sheet, df in dataframes.items():
    df.to_sql(sheet, engine, if_exists='replace', index=False)
import pandas as pd
from sqlalchemy import create_engine, text
from pydantic import BaseModel, Field, field_validator
from typing import List
import logging
import urllib

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch database details from environment variables
server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
driver = 'ODBC Driver 17 for SQL Server'

# Pydantic models for data validation
class Part(BaseModel):
    PartID: int
    Name: str
    Type: str
    Unit: str
    LeadTime: int

    @field_validator('LeadTime')
    def leadtime_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('LeadTime must be non-negative')
        return v

class BOMItem(BaseModel):
    ParentID: int
    ChildID: int
    Quantity: float
    FinalProduct: int

    @field_validator('Quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v

class DemandForecast(BaseModel):
    PartID: int
    Week: int
    Quantity: float

    @field_validator('Week', 'Quantity')
    def values_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Week and Quantity must be non-negative')
        return v

class Inventory(BaseModel):
    PartID: int
    InvStart: float
    InvEnd: float

class ScheduledReceipt(BaseModel):
    Part: int
    Receipt: float
    Week_no: int

class ExplodedDemand(BaseModel):
    PartID: int
    Week: int
    Demand: float = Field(..., ge=0)
    ParentID: int 
    Inventory: float
    Receipt: float
    Type: str

def load_data_from_sql_server():
    connection_string = f'mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus("DRIVER={"+driver+"};SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password)}'
    engine = create_engine(connection_string)

    data = {}
    data['PartMasterRecord'] = [Part(**row) for row in pd.read_sql_table('PartMasterRecord', engine).to_dict('records')]
    data['BOM'] = [BOMItem(**row) for row in pd.read_sql_table('BOM', engine).to_dict('records')]
    data['DemandForecast'] = [DemandForecast(**row) for row in pd.read_sql_table('DemandForecast', engine).to_dict('records')]
    data['Inventory'] = [Inventory(**row) for row in pd.read_sql_table('Inventory', engine).to_dict('records')]
    data['SchReceipt'] = [ScheduledReceipt(**row) for row in pd.read_sql_table('SchReceipt', engine).to_dict('records')]
    return data

def combine_inventory_and_receipts(inventory: List[Inventory], sch_receipt: List[ScheduledReceipt]) -> pd.DataFrame:
    inventory_df = pd.DataFrame([inv.model_dump() for inv in inventory])
    sch_receipt_df = pd.DataFrame([rec.model_dump() for rec in sch_receipt])
    return pd.concat([
        inventory_df[['PartID', 'InvStart']].rename(columns={'InvStart': 'Inventory'}).assign(Week=0),
        sch_receipt_df.rename(columns={'Part': 'PartID', 'SchReceipt': 'Inventory', 'Week_no': 'Week'})
    ])

def adjust_final_demand(demand_forecast: List[DemandForecast], part_master: List[Part], inventory_levels: pd.DataFrame) -> pd.DataFrame:
    demand_forecast_df = pd.DataFrame([df.model_dump() for df in demand_forecast])
    part_master_df = pd.DataFrame([pm.model_dump() for pm in part_master])

    demand_forecast_final = demand_forecast_df.merge(part_master_df[['PartID', 'Type']], on='PartID')
    adjusted_final_demand = demand_forecast_final[demand_forecast_final['Type'] == 'F']
    adjusted_final_demand = adjusted_final_demand.merge(inventory_levels, how='left', on=['PartID', 'Week'])
    adjusted_final_demand['AdjustedDemand'] = (
        adjusted_final_demand['Quantity'] -
        adjusted_final_demand['Inventory'].fillna(0) -
        adjusted_final_demand['Receipt'].fillna(0)
    ).clip(lower=0)
    return adjusted_final_demand[['PartID', 'Week', 'AdjustedDemand']]

def explode_bom(demand: pd.DataFrame, bom: List[BOMItem], part_master_record: List[Part], depth=0) -> pd.DataFrame:
    if demand.empty:
        return demand

    bom_df = pd.DataFrame([b.model_dump() for b in bom])
    part_master_df = pd.DataFrame([pm.model_dump() for pm in part_master_record])

    demand = demand.merge(part_master_df[['PartID', 'LeadTime']], on='PartID')
    demand['Week'] -= demand['LeadTime']

    if 'ParentID' not in demand.columns:
        demand['ParentID'] = demand['PartID']

    exploded_demand = demand.merge(bom_df, left_on='PartID', right_on='ParentID')
    exploded_demand = exploded_demand.rename(columns={"ParentID_y": "ParentID"})
    exploded_demand['Quantity'] *= exploded_demand['Demand']
    exploded_demand = exploded_demand[['ChildID', 'Week', 'Quantity', 'ParentID']].rename(columns={
        'ChildID': 'PartID',
        'Quantity': 'Demand'
    })

    exploded_demand = explode_bom(exploded_demand, bom, part_master_record, depth + 1)

    combined_demand = pd.concat([
        demand[['PartID', 'Week', 'Demand', 'ParentID']],
        exploded_demand
    ])
    
    return combined_demand

def calculate_final_demand(exploded_demand: pd.DataFrame, inventory_levels: pd.DataFrame, part_master: List[Part]) -> pd.DataFrame:
    part_master_df = pd.DataFrame([pm.model_dump() for pm in part_master])

    exploded_demand = exploded_demand.merge(inventory_levels, how='left', on=['PartID', 'Week'])
    exploded_demand['Inventory'] = exploded_demand['Inventory'].fillna(0)
    exploded_demand['Demand'] = (exploded_demand['Demand'] - exploded_demand['Inventory']).clip(lower=0)
    final_demand = exploded_demand.merge(part_master_df[['PartID', 'Type']], on='PartID')
    # final_demand = final_demand[final_demand['Type'] == 'P']
    return final_demand.sort_values(by=['PartID', 'Week'])

def create_exploded_demand_table(engine):
    with engine.connect() as connection:
        connection.execute(text("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='exploded_demand' AND xtype='U')
        CREATE TABLE exploded_demand_3 (
            PartID VARCHAR(50),
            Week INT,
            Demand DECIMAL(10, 2),
            ParentID VARCHAR(50),
            PRIMARY KEY (PartID, Week)
        )
        """))

def main():
    connection_string = f'mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus("DRIVER={"+driver+"};SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password)}'
    engine = create_engine(connection_string)
    create_exploded_demand_table(engine)

    data = load_data_from_sql_server()
    inventory_levels = combine_inventory_and_receipts(data['Inventory'], data['SchReceipt'])
    adjusted_final_demand = adjust_final_demand(data['DemandForecast'], data['PartMasterRecord'], inventory_levels)
    initial_demand = adjusted_final_demand.rename(columns={'AdjustedDemand': 'Demand'})

    # print("Initial demand: ", initial_demand)
    exploded_demand = explode_bom(initial_demand, data['BOM'], data['PartMasterRecord'])

    print("exploded demand: ", exploded_demand)
    final_exploded_demand = calculate_final_demand(exploded_demand, inventory_levels, data['PartMasterRecord'])
    print("final exploded demand: ", final_exploded_demand)

    validated_final_demand = [ExplodedDemand(**row) for row in final_exploded_demand.to_dict('records')]
    print("validated_final_demand: ", validated_final_demand)

    final_exploded_demand_df = pd.DataFrame([demand.model_dump() for demand in validated_final_demand])

    print(final_exploded_demand_df)

    final_exploded_demand.to_sql('exploded_demand_3', engine, if_exists='replace', index=False)

    logging.info("Results have been written to 'final_exploded_demand.csv' and the 'exploded_demand' table in SQL Server.")

if __name__ == "__main__":
    main()

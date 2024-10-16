# Import libraries
import streamlit as st
import bcrypt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import numpy as np
import pandas as pd
import sys
import os
import ast
from datetime import datetime

def string_to_list(string):
    return ast.literal_eval(string)

# Add path
def setup():
    # sys.path.append(os.path.join(os.path.dirname(__file__)))
    sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))
    # print(sys.path)

# Init list users:
def initusers(userids):
    # Khởi tạo danh sách người dùng
    if 'users' not in st.session_state:
        st.session_state['users'] = userids

# Class
class Collector:
    def __init__(self, client, db):
        self.client = client
        self.db = db
        self.fmi_collection = self.db['Full_Movies_Infor']
        self.mi_collection = self.db['Movies_Infor']
        self.ui_collection = self.db['Users_Infor']
        self.r_collection = self.db['Ratings']

    def run(self): 
        # Full Movies Infor
        fmi_cursor = self.fmi_collection.find()
        # print(fmi_cursor)
        fmi_data = list(fmi_cursor)
        fmi_df = pd.DataFrame(fmi_data, index = None)
        fmi_df = fmi_df.drop('_id', axis=1, errors='ignore')
        fmi_df = fmi_df.drop_duplicates().reset_index()
        # fmi_df["genre"] = fmi_df["genre"].apply(string_to_list)
        # fmi_df["directors"] = fmi_df["directors"].apply(string_to_list)
        # fmi_df["actors"] = fmi_df["actors"].apply(string_to_list)

        current_date = datetime.now().date()
        current_date = pd.to_datetime(current_date)
        fmi_df["deltaDate"] = current_date - fmi_df["releaseDate"]

        # Movies Infor
        mi_cursor = self.mi_collection.find()
        mi_data = list(mi_cursor)
        mi_df = pd.DataFrame(mi_data, index = None)
        mi_df = mi_df.drop('_id', axis=1, errors='ignore')
        mi_df = mi_df.drop_duplicates().reset_index()

        # Users Infor
        ui_cursor = self.ui_collection.find()
        ui_data = list(ui_cursor)
        ui_df = pd.DataFrame(ui_data, index = None)
        ui_df = ui_df.drop('_id', axis=1, errors='ignore')
        ui_df = ui_df.drop_duplicates().reset_index()

        # Ratings
        r_cursor = self.r_collection.find()
        r_data = list(r_cursor)
        r_df = pd.DataFrame(r_data, index = None)
        r_df = r_df.drop('_id', axis=1, errors='ignore')
        r_df = r_df.drop_duplicates().reset_index()

        return fmi_df, mi_df, ui_df, r_df

# Test:
setup()
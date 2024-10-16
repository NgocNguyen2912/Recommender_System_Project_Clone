# Import libraries
import requests
from bs4 import BeautifulSoup
import re
import json
from time import sleep
import random
import os
import signal
import sys
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Initial varibles:
MI_FILE_PATH = 'C:/Users/ADMIN/Processing/DSA-Project/processing/movies_id'

# Class:
class Movie_Infor:
    def __init__(self):
        pass
    
    def scrape_movie_inf(self, movie_id):
        insert_data = {}
        url = "https://imdb-api.hoangthinh130322.workers.dev/title/" + movie_id;
        response = requests.get(url)
        data = response.json()
        
        insert_data["movie_id"] = movie_id
        insert_data["title"] = data["title"]
        insert_data["introduction"] = data["plot"]
        insert_data["runtime"] = data["runtime"]
        insert_data["runtimeSeconds"] = data["runtimeSeconds"]
        insert_data["rating"] = data["rating"]
        insert_data["award"] = data["award"]
        insert_data["genre"] = data["genre"]
        insert_data["releaseDate"] = data["releaseDetailed"]["date"][:10]
        insert_data["releaseLocation"] = data["releaseDetailed"]["releaseLocation"]["country"]
        insert_data["actors"] = data["actors"]
        insert_data["directors"] = data["directors"]
        
        return insert_data
    
    def preprocess_movie_inf(self, data):
        for key in data:
            data[key] = str(data[key])
        
        raw_mi_df = pd.DataFrame([data])
        for i in raw_mi_df.select_dtypes(include = 'object'):
            if raw_mi_df[i][0].find('{') != -1:
                raw_mi_df[i] = raw_mi_df[i].apply(eval)
                
        raw_mi_df = pd.concat([raw_mi_df, raw_mi_df['rating'].apply(pd.Series), raw_mi_df['award'].apply(pd.Series)],axis = 1)
        raw_mi_df.rename(columns = {'count': 'totalRatings', 'star':'ratingStar', 'wins': 'totalAwards',
                                 'nominations': 'totalNominations'}, inplace = True)
        
        raw_mi_df = raw_mi_df.drop(columns = ['runtime', 'rating', 'award'])
        
        raw_mi_df['releaseDate'] = pd.to_datetime(raw_mi_df['releaseDate'])
        
        return raw_mi_df
    
    def store_movie_inf(self, df):
        # Local MongoDB:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['T2_PreprocessedData']
        
        # Collection
        collection = db['Full_Movies_Infor']
        
        # Push data
        dict_df = df.to_dict('records')
        result = collection.insert_many(dict_df)
        print ('=> Inserted document IDs successfuly:', result.inserted_ids)
        
        # MongoDB Atlas:
        password = 'dsa123456'
        uri = f"mongodb+srv://DSA_Project:{password}@cluster0.gdtn4g6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        
        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        db = client['T2_PreprocessedData']
        
        # Collection
        collection = db['Full_Movies_Infor']
        
        # Push data
        dict_df = df.to_dict('records')
        result = collection.insert_many(dict_df)
        print ('=> Inserted document IDs successfuly:', result.inserted_ids) 
    
    def collect_movie_inf(self, movie_id):
        movie_inf = self.scrape_movie_inf(movie_id)
        raw_mi_df = self.preprocess_movie_inf(movie_inf)
        self.store_movie_inf(raw_mi_df)

# Main:
with open(MI_FILE_PATH, 'r') as json_file:
    movies_id = json.load(json_file)

scrape_movie_infor = Movie_Infor()
nmovies_id = 100
i = 0

for movie_id in movies_id.keys(): 
    if i < nmovies_id:
        if (movies_id[movie_id] == False):
            print(f"====> Collect Movie {i}")
            try: 
                scrape_movie_infor.collect_movie_inf(movie_id)
            except:
                movies_id[movie_id] = True
                pass
                # break
            
            movies_id[movie_id] = True
            i = i + 1
    else:
        break
    
with open(MI_FILE_PATH, 'w') as json_file:
    json.dump(movies_id, json_file)
    

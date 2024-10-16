# Import libraries
from tool import *
import streamlit as st
import pandas as pd
import numpy as np
import pickle
# from surprise import Dataset
# from surprise import Reader

# Class
class App: 
    def __init__(self, r_df, fmi_df, userid):
        self.r_df = r_df
        self.fmi_df = fmi_df
        self.userid = userid

    def preprocessing(self):
        movie_dataset = self.fmi_df.copy()
        movie_dataset = movie_dataset[['movie_id','title']]

        dataset = self.r_df.copy()
        merged_dataset = pd.merge(dataset, movie_dataset, how='inner', on='movie_id')

        refined_dataset = merged_dataset.groupby(by=['user_id','movie_id','title'], as_index=False).agg({"user_rating":"mean"})

        ratings_data = refined_dataset.copy()

        return ratings_data

    def recommender_system(self, model, ratings_df, n_items):
        ratings_data = self.preprocessing()
        # Get a list of all movie IDs from dataset
        movie_ids = ratings_df["movie_id"].unique()

        # Get a list of all movie IDs that have been watched by user
        movie_ids_user = ratings_df.loc[ratings_df["user_id"] == self.userid, "movie_id"]
            # Get a list off all movie IDS that that have not been watched by user
        movie_ids_to_pred = np.setdiff1d(movie_ids, movie_ids_user)

        # Apply a rating of 0 to all interactions (only to match the Surprise dataset format)
        test_set = [[self.userid, movie_id, 0] for movie_id in movie_ids_to_pred]

        # Predict the ratings and generate recommendations
        predictions = model.test(test_set)
        pred_ratings = np.array([pred.est for pred in predictions])
        print("Top {0} Recommended Movies for User {1}:".format(n_items, self.userid))

        # Rank top-n movies based on the predicted ratings
        index_max = (-pred_ratings).argsort()[:n_items]
        count =0
        movies = []
        ratings = []
        for i in index_max:
            count+=1
            movie_id = movie_ids_to_pred[i]
            print('{}. \t [Movie Title] {}, [Estimated Rating] {}'.format(count, ratings_data[ratings_data["movie_id"]==movie_id]["title"].values[0], round(pred_ratings[i],3)))
            movies.append(ratings_data[ratings_data["movie_id"]==movie_id]["title"].values[0])
            ratings.append(round(pred_ratings[i],3))

        result = pd.DataFrame({'title': movies, 'predicted rating': ratings})

        return result

    def run(self):
        st.title("Có thể bạn sẽ thích (2)")
        with open('models/svd.pkl', 'rb') as f:
            loaded_algo = pickle.load(f)

        ratings_data = self.preprocessing()
        nmovies = st.number_input("Nhập số lượng phim muốn xem:", min_value=0, max_value=100, value=10, step=1, format="%d")
        with st.spinner('Đang chạy mô hình, vui lòng chờ...'):
            list_movies = self.recommender_system(loaded_algo,ratings_data,nmovies)
        option = st.selectbox(
        'Chọn nội dung muốn hiển thị:',
        ('Kết quả', 'Thông tin')
        )
        
        if option == 'Kết quả':
            st.write(display_columnsv2(list_movies, 3))
        elif option == 'Thông tin':
            st.write(list_movies)
        
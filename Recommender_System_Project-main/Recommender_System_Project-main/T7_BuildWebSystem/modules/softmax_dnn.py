# Import libraries
from tool import *
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
import tensorflow as tf

# Class
class App: 
    def __init__(self, r_df, fmi_df, userid):
        self.r_df = r_df
        self.fmi_df = fmi_df
        self.userid = userid
        self.user_enc = LabelEncoder()
        self.item_enc = LabelEncoder()
        self.label_encoder = LabelEncoder()
    
    def preprocessing(self):
        merged_dataset = pd.merge(self.r_df, self.fmi_df, how='inner', on='movie_id')
        refined_dataset = merged_dataset.copy()

        refined_dataset['user'] = self.user_enc.fit_transform(refined_dataset['user_id'].values)
        refined_dataset['movie'] = self.item_enc.fit_transform(refined_dataset['title'].values)
        refined_dataset['user_rating'] = self.label_encoder.fit_transform(refined_dataset['user_rating'])

        return refined_dataset

    def recommender_system(self, model, n_movies):
        refined_dataset = self.preprocessing()
        user_id = self.userid
        encoded_user_id = self.user_enc.transform([user_id])

        seen_movies = list(refined_dataset[refined_dataset['user_id'] == user_id]['movie'])
        unseen_movies = [i for i in range(min(refined_dataset['movie']), max(refined_dataset['movie'])+1) if i not in seen_movies]
        model_input = [np.asarray(list(encoded_user_id)*len(unseen_movies)), np.asarray(unseen_movies)]
        predicted_ratings = model.predict(model_input)
        predicted_rating_probality = np.max(predicted_ratings, axis = 1)
        predicted_rating_class = np.argmax(predicted_ratings, axis = 1)
        predicted_rating = self.label_encoder.inverse_transform(predicted_rating_class)
        sorted_indices = np.lexsort((predicted_rating_probality, predicted_rating))[::-1]
        recommended_movies = self.item_enc.inverse_transform(sorted_indices)
        spredicted_rating = predicted_rating[sorted_indices]
        spredicted_rating_probality = predicted_rating_probality[sorted_indices]
        recommend_nmovies = pd.DataFrame({"title": list(recommended_movies[:n_movies]),
                                            "predicted rating": list(spredicted_rating[:n_movies]),
                                            "probality": spredicted_rating_probality[:n_movies]})
        return recommend_nmovies

    def run(self):
        st.title("Có thể bạn sẽ thích (1)")
        loaded_model = tf.keras.models.load_model('models/softmax_dnn.h5')
        nmovies = st.number_input("Nhập số lượng phim muốn xem:", min_value=0, max_value=100, value=10, step=1, format="%d")
        
        with st.spinner('Đang chạy mô hình, vui lòng chờ...'):
            list_movies = self.recommender_system(loaded_model, nmovies)

        option = st.selectbox(
        'Chọn nội dung muốn hiển thị:',
        ('Kết quả', 'Thông tin')
        )
        
        if option == 'Kết quả':
            st.write(display_columnsv2(list_movies, 3))
        elif option == 'Thông tin':
            st.write(list_movies)

        
        
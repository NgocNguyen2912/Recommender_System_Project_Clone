# Import libraries
from tool import *
import pandas as pd
import numpy as np
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from rapidfuzz import process
import re
import ipywidgets as widgets
from IPython.display import display
import streamlit as st
import warnings
warnings.filterwarnings('ignore')


# Class
class App: 
    def __init__(self, mi_df):
        self.mi_df = mi_df
        self.mi_df['genre'] = self.mi_df['genre'].astype(str)
    
    def preprocessing(self):
        tf = TfidfVectorizer(analyzer = 'word', ngram_range = (1, 2), min_df = 0, stop_words = 'english')
        tfidf_genre = tf.fit_transform(self.mi_df['genre'])
        cosine_sim = linear_kernel(tfidf_genre, tfidf_genre)

        return cosine_sim
    
    def genre_recommendations(self, id_query):
        cosine_sim = self.preprocessing()
        movie_title = self.mi_df[self.mi_df['movie_id'] == id_query]['title'].values[0]
        print(f"Top 10 movies similar to {movie_title}")
        indices = pd.Series(self.mi_df.index, index = self.mi_df['movie_id'])
        idx = indices[id_query]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = list(filter(lambda x: x[0] != idx, sim_scores))   # bỏ phim đang tìm khỏi danh sách đề xuất
        sim_scores = sim_scores[:10]
        movie_indices = [i[0] for i in sim_scores]
        return self.mi_df.iloc[movie_indices][['movie_id', 'title', 'genre']].reset_index()
    
    def clean_title(self, title):
        return re.sub("[^a-zA-Z0-9 ]", "", title).lower()
    
    def preprocessingv2(self):
        self.mi_df['clean_title'] = (self.mi_df['title'] + ' ' + self.mi_df['movie_id']).apply(self.clean_title)
        all_titles = self.mi_df['clean_title'].tolist()

        return all_titles
    
    def search_title(self, title, stage = 2):
        all_titles = self.preprocessingv2()
        if stage == 1:
            print(f"Finding movie names that match the query '{title}'")
            print('Do you mean...', end='')
        title = self.clean_title(title)
        closest_match = process.extract(title, all_titles)[:5]
        res = [i[0] for i in closest_match]
        list_title = pd.Series(self.mi_df.index, index = self.mi_df['clean_title'])
        idx = list(dict.fromkeys(list_title[res]))
        return self.mi_df.iloc[idx][['movie_id', 'title', 'genre']].reset_index()

    def run(self):
        st.title("Tìm kiếm các bộ phim có nội dung tương tự")
        st.subheader("Tìm kiếm những bộ phim có cùng nội dung tương tự bằng Moive Id:")
        g_option = st.selectbox(
            "**Lựa chọn**",
            ('Ẩn', 'Hiện')
            )
        if g_option == 'Hiện':
            id_query = st.text_input("Nhập Movie Id: ")
            try: 
                genre_rs = self.genre_recommendations(id_query)
                st.write("Thông tin phim:")
                st.write(genre_rs)
                st.write("Kết quả:")
                st.write(display_columns(genre_rs, 3))
            except:
                pass
            
        
        st.subheader("Tìm kiếm những bộ phim có cùng nội dung tương tự bằng Title:")
        t_option = st.selectbox(
            "**Lựa chọn** ",
            ('Ẩn', 'Hiện')
            )
        if t_option == 'Hiện':
            title = st.text_input("Nhập Title: ")
            try:
                search_rs = self.search_title(title)
                st.write("Thông tin phim:")
                st.write(search_rs)
                st.write("Kết quả:")
                st.write(display_columns(search_rs, 3))
            except: 
                pass
        
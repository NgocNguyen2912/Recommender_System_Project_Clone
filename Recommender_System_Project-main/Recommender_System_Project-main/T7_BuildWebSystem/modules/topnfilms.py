# Import libraries
import streamlit as st
from tool import *

class App():
    def __init__(self, fmi_df, mi_df):
        self.fmi_df = fmi_df
        self.mi_df = mi_df

    def change_type(self):
        for i in self.fmi_df.select_dtypes(include = 'object'):
            if self.fmi_df[i][0].find('[') != -1:
                self.fmi_df[i] = self.fmi_df[i].apply(eval)

        for i in self.mi_df.select_dtypes(include = 'object'):
            if self.mi_df[i][0].find('[') != -1:
                self.mi_df[i] = self.mi_df[i].apply(eval)

    # Ratings
    def topnfilms_ratings(self, aspect = 'ratingStar'):
        sorted_df = self.fmi_df.sort_values(by = aspect, ascending = False).head(10)
        res_df = sorted_df.reset_index()
        return res_df

    # Genres:
    def find_best_genres_by_rating(self):
        df_explode = self.fmi_df.explode('genre')
        df_genre = df_explode.groupby('genre')
        df_ranking = df_genre['ratingStar'].mean().round(1).sort_values(ascending = False).reset_index()
        return df_ranking.head(10)

    def topnfilms_genres(self, genre_name, aspect='ratingStar'):
        self.fmi_df['genre_2'] = self.fmi_df['genre']
        df_explode = self.fmi_df.explode('genre_2')
        df_genre = df_explode.groupby('genre_2')
        df_movies = df_genre.get_group(genre_name)
        df_movies = df_movies.sort_values(by = aspect, ascending = False).head(10).reset_index()
        return df_movies
    
    # Runtime
    def searchRunTime(self, startperiod, endperiod):
        runtime_df = self.fmi_df.copy()
        runtime_df['runtimeSeconds'] = runtime_df['runtimeSeconds'].astype(int)
        runtime_df['runtimeHours'] = runtime_df['runtimeSeconds']/(60*60)
        mask = (runtime_df['runtimeHours'] >= startperiod) & (runtime_df['runtimeHours']<= endperiod)
        runtime_df = runtime_df[mask].reset_index()
        # Top 10 bộ phim có rating cao theo thời lượng phim
        sorted_runtime_df = runtime_df.sort_values(by='ratingStar',ascending=False)
        rating_runtime_df = sorted_runtime_df[['movie_id','title', 'ratingStar','runtimeHours']][:10].reset_index()
        # rating_runtime_df = rating_runtime_df.drop("level_0")
        return rating_runtime_df

    # Locations:
    def find_best_locations_by_rating(self):
        df_location = self.fmi_df.groupby('releaseLocation')
        df_ranking = df_location['ratingStar'].mean().round(1).sort_values(ascending = False).reset_index()
        return df_ranking.head(10)
    
    def topnfilms_locations(self, location_name, aspect='ratingStar'):
        self.fmi_df['location'] = self.fmi_df['releaseLocation']
        df_location = self.fmi_df.groupby('location')
        df_movies = df_location .get_group(location_name)
        df_movies = df_movies.sort_values(by = aspect, ascending = False).head(10).reset_index()
        return df_movies

    # Actors:
    def find_best_actors_by_rating(self):
        df_explode = self.fmi_df.explode('actors')
        df_actor = df_explode.groupby('actors')
        df_ranking = df_actor['ratingStar'].mean().round(1).sort_values(ascending = False).reset_index()
        return df_ranking.head(10)
    
    def find_best_actors(self, aspect = 'ratingStar'):
        df_explode = self.mi_df.explode('actors')
        df_actor = df_explode.groupby('actors')
        if aspect in ['totalAwards', 'totalNominations']:
            df_ranking = df_actor[aspect].sum().sort_values(ascending = False).reset_index()
        else:
            df_ranking = df_actor[aspect].mean().round(1).sort_values(ascending = False).reset_index()
        return df_ranking.head(10)
    
    def topnfilms_actors(self, actor_name, aspect='ratingStar'):
        self.fmi_df['actors_2'] = self.fmi_df['actors']
        df_explode = self.fmi_df.explode('actors_2')
        df_actor = df_explode.groupby('actors_2')
        df_movies = df_actor.get_group(actor_name)
        df_movies = df_movies.sort_values(by = aspect, ascending = False).head(10).reset_index()
        return df_movies

    # Directors:
    def find_best_directors_by_rating(self):
        df_explode = self.mi_df.explode('directors')
        df_director = df_explode.groupby('directors')
        df_ranking = df_director['ratingStar'].mean().round(1).sort_values(ascending = False).reset_index()
        return df_ranking.head(10)
    
    def find_best_directors(self, aspect = 'ratingStar'):
        df_explode = self.mi_df.explode('directors')
        df_director = df_explode.groupby('directors')
        if aspect in ['totalAwards', 'totalNominations']:
            df_ranking = df_director[aspect].sum().sort_values(ascending = False).reset_index()
        else:
            df_ranking = df_director[aspect].mean().round(1).sort_values(ascending = False).reset_index()
        return df_ranking.head(10)
    
    def topnfilms_directors(self, director_name, aspect='ratingStar'):
        self.mi_df['directors_2'] = self.mi_df['directors']
        df_explode = self.mi_df.explode('directors_2')
        df_director = df_explode.groupby('directors_2')
        df_movies = df_director.get_group(director_name)
        df_movies = df_movies.sort_values(by = aspect, ascending = False).head(10).reset_index()
        return df_movies

    def run(self):
        try: 
            self.change_type()
        except:
            pass
        # Ratings
        st.subheader("Top phim có rating trung bình cao nhất")
        r_option = st.selectbox(
            "Lựa chọn",
            ('Ẩn', 'Hiện', 'Hiện thông tin')
        )
        topnfilms_ratings = self.topnfilms_ratings()
        if r_option == 'Hiện':
            st.write(display_columns(topnfilms_ratings, 3))
        elif r_option == 'Hiện thông tin':
            st.write(topnfilms_ratings)

        # Genres:
        st.subheader("Top phim có thể loại có nhiều phim có rating cao nhất")
        g_option = st.selectbox(
            "Lựa chọn",
            ('Ẩn', 'Hiện')
        )
        topngenres_infor = self.find_best_genres_by_rating()
        topngenres = list(topngenres_infor['genre'])
        if g_option == 'Hiện':
            col1, col2 = st.columns(2)
            col1.write(topngenres_infor)
            genre = col2.selectbox("Chọn thể loại yêu thích: ",topngenres)
            topnfilm_genres = self.topnfilms_genres(genre)
            col2.write("Thông tin")
            col2.write(topnfilm_genres)
            st.write("Kết quả")
            col2.write(display_columns(topnfilm_genres,3))

        # Runtime 
        st.subheader("Top phim có rating cao tùy vào thời lượng phim (Độ dài của phim)")
        rt_option = st.selectbox(
            "Lựa chọn   ",
            ('Ẩn', 'Hiện')
        )

        if rt_option == 'Hiện':
            col1, col2 = st.columns(2)
            startperiod = col1.number_input("Khoảng thời gian ít nhất:", min_value=0, max_value=5, value=1, step=1, format="%d")
            endperiod = col2.number_input("Khoảng thời gian dài nhất:", min_value=0, max_value=5, value=2, step=1, format="%d")
            rating_runtime_df = self.searchRunTime(startperiod, endperiod)
            option = st.selectbox(
                "Lựa chọn",
                ('Kết quả', 'Thông tin')
            )
            if option == 'Kết quả':
                st.write("Kết quả:")
                st.write(display_columns(rating_runtime_df,3))
            elif option == 'Thông tin':
                st.write("Thông tin")
                st.write(rating_runtime_df)

        # Locations
        st.subheader("Top phim của các quốc gia có rating cao")
        l_option = st.selectbox(
            "Lựa chọn  ",
            ('Ẩn', 'Hiện')
        )
        topnlocations_infor = self.find_best_locations_by_rating()
        topnlocations = list(topnlocations_infor['releaseLocation'])
        if l_option == 'Hiện':
            col1, col2 = st.columns(2)
            col1.write(topnlocations_infor)
            location = col2.selectbox("Chọn quốc gia yêu thích: ", topnlocations)
            topnfilm_locations = self.topnfilms_locations(location)
            col2.write("Thông tin")
            col2.write(topnfilm_locations)
            st.write("Kết quả")
            col2.write(display_columns(topnfilm_locations,3))
        
        # Actors:
        st.subheader("Top phim của các diễn viên tốt có nhiều giải thưởng nhất")
        a_option = st.selectbox(
            "Lựa chọn     ",
            ('Ẩn', 'Hiện')
        )
        topnactors_infor = self.find_best_actors('totalAwards')
        topnactors = list(topnactors_infor['actors'])
        if a_option == 'Hiện':
            col1, col2 = st.columns(2)
            col1.write(topnactors_infor)
            actor = col2.selectbox("Chọn diễn viên yêu thích: ",topnactors)
            topnfilm_actors = self.topnfilms_actors(actor)
            col2.write("Thông tin")
            col2.write(topnfilm_actors)
            st.write("Kết quả")
            col2.write(display_columns(topnfilm_actors,3))

        # Directors:
        st.subheader("Top phim của các đạo diễn tốt có nhiều giải thưởng nhất")
        d_option = st.selectbox(
            "Lựa chọn ",
            ('Ẩn', 'Hiện')
        )
        topndirectors_infor = self.find_best_directors('totalAwards')
        topndirectors = list(topndirectors_infor['directors'])
        if d_option == 'Hiện':
            col1, col2 = st.columns(2)
            col1.write(topndirectors_infor)
            director = col2.selectbox("Chọn đạo diễn yêu thích: ",topndirectors)
            topnfilm_directors = self.topnfilms_directors(director)
            col2.write("Thông tin")
            col2.write(topnfilm_directors)
            st.write("Kết quả")
            col2.write(display_columns(topnfilm_directors,3))

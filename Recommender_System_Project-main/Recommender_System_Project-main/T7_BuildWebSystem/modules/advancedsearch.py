# Import libraries
import init
import plotly.graph_objects as go
import streamlit as st
from tool import *

# Class
class App: 
    def __init__(self, fmi_df):
        self.fmi_df = fmi_df
    
    def rs_asearch(self, fmi_df, options):
        as_df = fmi_df.copy()
        as_df['genre'] = as_df['genre'].astype(str)
        as_df['actors'] = as_df['actors'].astype(str)
        as_df['directors'] = as_df['directors'].astype(str)
        
        for idx in options.keys():
            ### Filter:
            if (idx == 'title'):
                if options[idx] != "":
                    mask = as_df['title'].str.lower().str.contains(options['title'].lower())
                    as_df = as_df[mask]

            if (idx == 'genre'):
                if options[idx]: 
                    for opt in options[idx]:
                        mask = as_df['genre'].str.lower().str.contains(opt.lower())
                        as_df = as_df[mask]

            if (idx == 'actors'):
                if options[idx] != "":
                    mask = as_df['actors'].str.lower().str.contains(options['actors'].lower())
                    as_df = as_df[mask]
            
            if (idx == 'directors'):
                if options[idx] != "":
                    mask = as_df['directors'].str.lower().str.contains(options['directors'].lower())
                    as_df = as_df[mask]

            if (idx == 'releaseLocation'):
                if options[idx] != "":
                    mask = as_df['releaseLocation'].str.lower().str.contains(options['releaseLocation'].lower())
                    as_df = as_df[mask]

            ### Sort By:
            if (idx == 'releaseDate'):
                    if options[idx] != "": 
                        mask = as_df['releaseDate'] >= options[idx]
                        as_df = as_df[mask]
                        as_df = as_df.sort_values(by='releaseDate',ascending=False)
                        
            if (idx == 'ratingStar'):
                    if options[idx] != "": 
                        mask = as_df['ratingStar'] >= options[idx]
                        as_df = as_df[mask]
                        as_df = as_df.sort_values(by='ratingStar',ascending=False)

        return as_df[:10]
    
    def run(self):
        st.title("Tìm kiếm nâng cao")
        col1, col2, col3 = st.columns(3)
        title = col1.text_input("Nhập title:")
        actors = col2.text_input("Nhập actors:")
        directors = col3.text_input("Nhập directors:")
        genres = ['Drama', 'Thriller', 'Comedy', 'Action', 'Adventure', 'Crime',
            'Mystery', 'Sci-Fi', 'Romance', 'Horror', 'Fantasy', 'Family',
            'Animation', 'Biography', 'War', 'History', 'Western', 'Short',
            'Musical', 'Documentary', 'Music', 'Sport', 'Film-Noir', 'Reality-TV',
            'Game-Show', 'News', 'Talk-Show']
        genre = st.multiselect("Chọn thể loại yêu thích:", genres)

        options = {
            'title': title,
            'genre': genre,
            'actors': actors, 
            'directors': directors,
            'releaseLocation': "", 
            'releaseDate': '06-2010',
            'ratingStar': 8
        }
        as_df = self.rs_asearch(self.fmi_df, options).reset_index()

        option = st.selectbox(
        'Chọn nội dung muốn hiển thị:',
        ('Kết quả', 'Thông tin', 'Trực quan hóa')
        )
        
        if option == 'Kết quả':
            st.write(display_columns(as_df, 3))
        elif option == 'Thông tin':
            st.write(as_df)
        elif option == 'Trực quan hóa':
            # Tạo biểu đồ cột sử dụng Plotly
            fig = go.Figure(data=[go.Bar(y=as_df['title'], x=as_df['ratingStar'], orientation='h', marker_color='gold')])

            # Tùy chỉnh layout của biểu đồ
            fig.update_layout(title='Biểu đồ thể hiện Rating',
                                xaxis_title='ratingStar',
                                yaxis_title='title')

            # Hiển thị biểu đồ trên Streamlit
            st.plotly_chart(fig)


        

    


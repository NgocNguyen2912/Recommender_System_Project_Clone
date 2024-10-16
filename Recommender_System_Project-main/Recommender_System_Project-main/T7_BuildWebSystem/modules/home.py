# Import libraries
import streamlit as st
import numpy as np
from topnfilms import App as TopNFilms_App


# Class
class App:
    def __init__(self, fmi_df, mi_df, ui_df, userid):
        self.fmi_df = fmi_df
        self.mi_df = mi_df
        self.ui_df = ui_df
        self.userid = userid
        self.usertype = 0

    def induction(self):
        option = st.selectbox(
            "**Hướng dẫn sử dụng**",
            ('Ẩn', 'Hiện')
            )
        if option == 'Hiện':
            st.info("Khuyến khích:")
            st.write("+ **Trang chủ**: Ở đây bao gồm những top phim về thể loại, quốc gia, đạo diễn,... mà đa số các user đánh giá cao")
            st.write("+ **Tìm kiếm nâng cao**: Ở đây bạn có thể tìm kiếm các bộ phim bằng các keyword có trong các thông tin phim \
                    (Thể loại, quốc gia, đạo diễn, ...)")
            st.write("+ **Khảo sát**: Ở đây bạn sẽ thực hiện các khảo sát để chúng tôi hiểu hơn về bạn cũng như đưa ra \
                     những bộ phim đúng với sở thích của bạn")
            st.write("+ **Nội dung phim tương tự**: Ở đây bạn sẽ tìm được những bộ phim có nội dung tương tự với bộ phim mà bạn ấn \
                     tượng bằng cách nhập Movie Id hay đơn giản là chỉ cần nhớ 1 phần nhỏ title của phim đó")
            st.info("Đặc biệt:")
            st.write("+ **Có thể bạn sẽ thích (1)**: Ở đây bạn sẽ được giới thiệu những bộ phim mà những người có cùng sở thích với bạn \
                     đánh giá cao")
            st.write("+ **Có thể bạn sẽ thích (2)**: Tương tự như **Có thể bạn sẽ thích (1)**, bạn sẽ được giới thiệu những bộ phim \
                     mà những người có cùng sở thích với bạn đánh giá cao")   

    def defineusertype(self, member_since):
        lowertime_line = np.datetime64('2022-01-01')
        uppertime_line = np.datetime64('2024-05-01')
        if uppertime_line >= member_since >= lowertime_line:
            self.usertype = 1
        elif member_since < lowertime_line:
            self.usertype = 2

    def classfyuser(self, member_since):
        self.defineusertype(member_since)
        if self.usertype == 0:
            st.write("Bạn là ***New User*** (Bạn nên đọc kĩ **Hướng dẫn sử dụng** và chỉ sử dụng phần **Khuyến khích**)")
        
        elif self.usertype == 1:
            st.write("Bạn là ***Fairly New user*** (Bạn nên đọc kĩ **Hướng dẫn sử dụng** và bạn có thể sử dụng cả \
                     phần **Khuyến khích** và phần **Đặc biệt**, tuy nhiên bạn vẫn nên sử dụng phần **Khuyến khích** để chúng tôi\
                     có thể hiểu hơn về bạn)")

        elif self.usertype == 2:
            st.write("Bạn là ***Old User*** (Bạn có thể sử dụng tất cả mọi chức năng trong hệ thống)")
            
                
    def run(self):
        st.title("Trang chủ")
        try:
            username = self.ui_df[self.ui_df['user_id'] == self.userid]['user_name'].values[0]
        except:
            username = self.userid

        st.success(f"Chào mừng {username} đến với trang web phim của chúng tôi")

        # Xác định thể loại user:
        try:
            member_since = self.ui_df[self.ui_df['user_id'] == self.userid]['member_since'].values[0]
        except:
            member_since = np.datetime64('2024-08-06')

        self.classfyuser(member_since)
        self.induction()
        topnfilms_app = TopNFilms_App(self.fmi_df, self.mi_df)
        topnfilms_app.run()


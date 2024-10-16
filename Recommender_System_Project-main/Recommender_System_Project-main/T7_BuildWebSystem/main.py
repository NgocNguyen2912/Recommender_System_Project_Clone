# Import libraries
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
from streamlit_option_menu import option_menu
import bcrypt

# Import file.py
from init import *
from settings import *
from modules.home import App as Home_App
from modules.login import App as Login_App
from modules.signup import App as SignUp_App
from modules.advancedsearch import App as AS_App
from modules.softmax_dnn import App as SoftmaxDNN_App
from modules.survey import App as Survey_App

from modules.svd import App as SVD_App
from modules.content_base_filtering import App as CBF_App

# Main
if __name__ == '__main__':  
    if 'update_data' not in st.session_state:
        st.session_state['update_data'] = False

    # userids = None
    if (st.session_state['update_data'] == False):
        setup()
        ## Connect to MongoDB:
        client =  MongoClient(MONGODB_HOST)
        db = client['T2_PreprocessedData']
        collector = Collector(client, db)
        fmi_df, mi_df, ui_df, r_df = collector.run()

        st.session_state['fmi_df'] = fmi_df
        st.session_state['mi_df'] = mi_df
        st.session_state['ui_df'] = ui_df
        st.session_state['r_df'] = r_df
        st.session_state['update_data'] = True

        userids = list(ui_df['user_id'])
        initusers(userids)

    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['userid'] = ""
        st.session_state['username'] = ""

    
    if st.session_state['logged_in']:
        st.sidebar.success(f"Logged in as {st.session_state['username']}")
        with st.sidebar:
            page = option_menu("Main Menu", ['Trang chủ', 'Khảo sát', "Nội dung tương tự" ,"Tìm kiếm nâng cao",'Có thể bạn sẽ thích (1)', 'Có thể bạn sẽ thích (2)', "Đăng xuất"], 
                icons=['house', 'person-fill-add', 'stickies', 'search', 'star', 'star-fill'], menu_icon="cast", default_index=0)
            
        # page = option_menu("Menu", ["???", "???", "???", '???'], 
        #     icons=['house', 'cloud-upload', "list-task", 'gear'], 
        #     menu_icon="cast", default_index=0, orientation="horizontal")

        ## Function
        if page == "Trang chủ":
            home_app = Home_App(st.session_state['fmi_df'], st.session_state['mi_df'],\
                                st.session_state['ui_df'], st.session_state['userid'])
            home_app.run()
        elif page == "Khảo sát":
            survey_app = Survey_App(st.session_state['fmi_df'])
            survey_app.run()
        elif page == "Nội dung tương tự":
            cbf_app = CBF_App(st.session_state['mi_df'])
            cbf_app.run()
        elif page == "Tìm kiếm nâng cao":
            as_app = AS_App(st.session_state['fmi_df'])
            as_app.run()
        elif page == "Có thể bạn sẽ thích (1)":
            softmaxdnn_app = SoftmaxDNN_App(st.session_state['r_df'], st.session_state['fmi_df'], st.session_state['userid'])
            softmaxdnn_app.run()
        elif page == "Có thể bạn sẽ thích (2)":
            svd_app = SVD_App(st.session_state['r_df'], st.session_state['fmi_df'], st.session_state['userid'])
            svd_app.run()
            
        elif page == "Đăng xuất":
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.success("You have successfully logged out")
            st.experimental_rerun()


    else:
        page = st.sidebar.selectbox("Menu", ["Đăng nhập", "Đăng ký"])

        if page == "Đăng nhập":
            st.subheader("Đăng nhập tài khoản")
            userid = st.text_input("Tài khoản")
            password = st.text_input("Mật khẩu", type='password')

            login_app = Login_App(userid, password, st.session_state['ui_df'])
            login_app.run()
        
        elif page == "Đăng ký":
            st.subheader("Đăng ký tài khoản")
            new_user = st.text_input("Tài khoản")
            new_password = st.text_input("Mật khẩu", type='password')

            signup_app = SignUp_App(new_user)
            signup_app.run()

            
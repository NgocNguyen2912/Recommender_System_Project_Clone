from settings import *
import streamlit as st
import bcrypt

class App():
    def __init__(self, userid, password, ui_df):
        self.userid = userid
        self.password = password
        self.ui_df = ui_df
    
    def login(self): 
        users = st.session_state['users']
        if self.userid in users:
            stored_password = TMP_PASSWORD
            return bcrypt.checkpw(self.password.encode(), stored_password)
        return False
    
    def run(self):
        if st.button("Đăng nhập"):
            if self.login():
                st.session_state['logged_in'] = True
                try: 
                    username = self.ui_df[self.ui_df['user_id'] == self.userid]['user_name'].values[0]
                    st.session_state['userid'] = self.userid
                except:
                    username = self.userid
                    st.session_state['userid'] = self.userid
                    
                st.session_state['username'] = username
                
                st.success(f"Logged In as {self.userid}")
                st.experimental_rerun()
            else:
                st.warning("Incorrect Username/Password")


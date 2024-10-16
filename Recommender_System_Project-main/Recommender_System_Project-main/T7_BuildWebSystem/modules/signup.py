from settings import *
import streamlit as st
import bcrypt

class App():
    def __init__(self, new_user):
        self.new_user = new_user

    def run(self):
        if st.button("Đăng ký"):
            users = st.session_state['users']
            if self.new_user in users:
                st.warning("User account already exists")
            else:
                users.append(self.new_user)
                st.session_state['users'] = users
                st.success("You have successfully created a new account")
                st.info("Go to the Login menu to login")
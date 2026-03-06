import streamlit as st

def is_logged_in() -> bool:
    return st.session_state.get("user") is not None

def is_admin() -> bool:
    user = st.session_state.get("user")
    return user is not None and user.get("role") == "admin"

def get_current_user():
    return st.session_state.get("user")

def login_user(user: dict):
    st.session_state.user = user

def logout_user():
    st.session_state.user = None
    st.session_state.cart = []

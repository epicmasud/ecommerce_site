import streamlit as st
from utils.database import authenticate
from utils.auth import login_user

def show():
    col1,col2,col3 = st.columns([1,1.2,1])
    with col2:
        st.markdown("## Welcome Back")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Sign In", use_container_width=True, type="primary"):
            if not email or not password: st.error("Fill in all fields.")
            else:
                user = authenticate(email.strip().lower(), password)
                if user:
                    login_user(user)
                    st.session_state.page="home"; st.rerun()
                else: st.error("Invalid email or password.")
        st.markdown("---")
        st.info("Admin: admin@threadco.com / admin123\nCustomer: john@example.com / customer123")
        if st.button("Create Account", use_container_width=True):
            st.session_state.page="register"; st.rerun()

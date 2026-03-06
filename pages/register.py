import streamlit as st
from utils.database import create_user

def show():
    col1,col2,col3 = st.columns([1,1.2,1])
    with col2:
        st.markdown("## Create Account")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        if st.button("Register", use_container_width=True, type="primary"):
            if not all([name,email,password,confirm]): st.error("Fill all fields.")
            elif password!=confirm: st.error("Passwords do not match.")
            elif len(password)<6: st.error("Password min 6 characters.")
            else:
                ok,msg = create_user(name.strip(), email.strip().lower(), password)
                if ok: st.success(msg); st.session_state.page="login"; st.rerun()
                else: st.error(msg)
        if st.button("Already have account?", use_container_width=True):
            st.session_state.page="login"; st.rerun()

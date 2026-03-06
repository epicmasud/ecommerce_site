import streamlit as st
from utils.database import update_user_profile, change_password, get_user_orders
from utils.auth import get_current_user, logout_user

def show():
    st.markdown("## My Profile")
    user = get_current_user()
    orders = get_user_orders(user["id"])
    st.write(f"**Name:** {user['name']}  |  **Email:** {user['email']}  |  **Role:** {user['role']}")
    st.write(f"**Total Orders:** {len(orders)}")
    st.markdown("---")
    tab1,tab2 = st.tabs(["Edit Profile","Change Password"])
    with tab1:
        new_name = st.text_input("Name", value=user["name"])
        new_email = st.text_input("Email", value=user["email"])
        if st.button("Save", type="primary"):
            if update_user_profile(user["id"], new_name, new_email):
                st.session_state.user["name"]=new_name
                st.session_state.user["email"]=new_email
                st.success("Profile updated!")
            else: st.error("Could not update.")
    with tab2:
        old = st.text_input("Current Password", type="password")
        new = st.text_input("New Password", type="password")
        conf = st.text_input("Confirm New Password", type="password")
        if st.button("Update Password", type="primary"):
            if new!=conf: st.error("Passwords do not match.")
            else:
                ok,msg = change_password(user["id"],old,new)
                st.success(msg) if ok else st.error(msg)
    if st.button("Logout"):
        logout_user(); st.session_state.page="home"; st.rerun()

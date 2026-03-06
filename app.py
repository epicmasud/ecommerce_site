import streamlit as st
from utils.database import init_db
from utils.auth import is_logged_in, is_admin

st.set_page_config(page_title="ThreadCo", page_icon="👕", layout="wide")

init_db()

if "page" not in st.session_state: st.session_state.page = "home"
if "cart" not in st.session_state: st.session_state.cart = []
if "user" not in st.session_state: st.session_state.user = None

st.markdown("""<style>
#MainMenu,footer,header{visibility:hidden}
.block-container{padding-top:1rem}
</style>""", unsafe_allow_html=True)

st.markdown("## 👕 ThreadCo — Premium Clothing")
st.markdown("---")

# Navigation
if is_logged_in():
    nav_options = ["Home","Shop","Cart","Orders","Profile"]
    if is_admin(): nav_options.append("Admin")
    nav_options.append("Logout")
else:
    nav_options = ["Home","Shop","Cart","Login","Register"]

cols = st.columns(len(nav_options))
for i, label in enumerate(nav_options):
    with cols[i]:
        btn_label = f"Cart ({len(st.session_state.cart)})" if label == "Cart" else label
        if st.button(btn_label, use_container_width=True, key=f"nav_{label}"):
            if label == "Logout":
                st.session_state.user = None
                st.session_state.cart = []
                st.session_state.page = "home"
            else:
                st.session_state.page = label.lower()

st.markdown("---")

# Import and show pages
page = st.session_state.page

if page == "home":
    from pages import home
    home.show()
elif page == "shop":
    from pages import products
    products.show()
elif page == "product_detail":
    from pages import product_detail
    product_detail.show()
elif page == "cart":
    from pages import cart
    cart.show()
elif page == "checkout":
    from pages import checkout
    checkout.show()
elif page == "login":
    from pages import login
    login.show()
elif page == "register":
    from pages import register
    register.show()
elif page == "orders":
    if is_logged_in():
        from pages import orders
        orders.show()
    else:
        st.warning("Please login first.")
        st.session_state.page = "login"
elif page == "profile":
    if is_logged_in():
        from pages import profile
        profile.show()
    else:
        st.warning("Please login first.")
        st.session_state.page = "login"
elif page == "admin":
    if is_admin():
        from pages import admin
        admin.show()
    else:
        st.error("Admins only.")
else:
    from pages import home
    home.show()

import streamlit as st
from utils.database import init_db
from utils.auth import is_logged_in, is_admin
from pages import home, products, product_detail, cart, checkout, login, register, admin, orders, profile

st.set_page_config(page_title="ThreadCo", page_icon="👕", layout="wide")

init_db()

if "page" not in st.session_state: st.session_state.page = "home"
if "cart" not in st.session_state: st.session_state.cart = []
if "user" not in st.session_state: st.session_state.user = None

st.markdown("""<style>
#MainMenu,footer,header{visibility:hidden}
.block-container{padding-top:1rem}
</style>""", unsafe_allow_html=True)

st.markdown("## 👕 ThreadCo")

cols = st.columns(8)
nav = [("Home","home"),("Shop","products"),("Cart","cart"),("Login","login"),("Register","register")]
if is_logged_in():
    nav = [("Home","home"),("Shop","products"),("Cart","cart"),("Orders","orders"),("Profile","profile")]
    if is_admin(): nav.append(("Admin","admin"))
    nav.append(("Logout","logout"))

for i,(label,page) in enumerate(nav):
    with cols[i]:
        cart_label = f"Cart ({len(st.session_state.cart)})" if page=="cart" else label
        if st.button(cart_label, use_container_width=True, key=f"nav_{page}"):
            if page == "logout":
                st.session_state.user = None
                st.session_state.cart = []
                st.session_state.page = "home"
            else:
                st.session_state.page = page
            st.rerun()

st.markdown("---")

p = st.session_state.page
if p=="home": home.show()
elif p=="products": products.show()
elif p=="product_detail": product_detail.show()
elif p=="cart": cart.show()
elif p=="checkout": checkout.show()
elif p=="login": login.show()
elif p=="register": register.show()
elif p=="admin":
    if is_admin(): admin.show()
    else: st.error("Admins only.")
elif p=="orders":
    if is_logged_in(): orders.show()
    else: st.warning("Login required."); st.session_state.page="login"; st.rerun()
elif p=="profile":
    if is_logged_in(): profile.show()
    else: st.warning("Login required."); st.session_state.page="login"; st.rerun()
else: home.show()

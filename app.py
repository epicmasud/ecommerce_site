import streamlit as st

st.set_page_config(page_title="ThreadCo", page_icon="👕", layout="wide")

# Init session state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "cart" not in st.session_state:
    st.session_state.cart = []
if "user" not in st.session_state:
    st.session_state.user = None

# Init database
from utils.database import init_db
init_db()

from utils.auth import is_logged_in, is_admin

# ── Navbar ────────────────────────────────────────────────
st.markdown("## 👕 ThreadCo")
st.markdown("---")

if is_logged_in():
    nav = ["Home", "Shop", "Cart", "Orders", "Profile"]
    if is_admin():
        nav.append("Admin")
    nav.append("Logout")
else:
    nav = ["Home", "Shop", "Cart", "Login", "Register"]

cols = st.columns(len(nav))
for i, label in enumerate(nav):
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

# ── Router ────────────────────────────────────────────────
page = st.session_state.page

if page == "home":
    from pages.home import show
    show()
elif page == "shop":
    from pages.products import show
    show()
elif page == "product_detail":
    from pages.product_detail import show
    show()
elif page == "cart":
    from pages.cart import show
    show()
elif page == "checkout":
    from pages.checkout import show
    show()
elif page == "login":
    from pages.login import show
    show()
elif page == "register":
    from pages.register import show
    show()
elif page == "orders":
    if is_logged_in():
        from pages.orders import show
        show()
    else:
        st.warning("Please login first.")
        st.session_state.page = "login"
elif page == "profile":
    if is_logged_in():
        from pages.profile import show
        show()
    else:
        st.warning("Please login first.")
        st.session_state.page = "login"
elif page == "admin":
    if is_admin():
        from pages.admin import show
        show()
    else:
        st.error("Admins only.")
else:
    from pages.home import show
    show()

import streamlit as st
from utils.database import get_product_by_id

def show():
    pid = st.session_state.get("selected_product")
    if not pid: st.warning("No product selected."); return
    p = get_product_by_id(pid)
    if not p: st.error("Not found."); return
    if st.button("Back to Shop"): st.session_state.page="products"; st.rerun()
    col1,col2 = st.columns(2)
    with col1:
        st.image(p.get("image_url","https://via.placeholder.com/400"), use_container_width=True)
    with col2:
        st.markdown(f"## {p['name']}")
        st.write(f"**${p['price']:.2f}**")
        st.write(p.get("description",""))
        st.write(f"Stock: {p['stock']}")
        sizes = [s.strip() for s in p.get("sizes","S,M,L,XL").split(",")]
        colors = [c.strip() for c in p.get("colors","Black").split(",")]
        size = st.selectbox("Size", sizes)
        color = st.selectbox("Color", colors)
        qty = st.number_input("Qty", min_value=1, max_value=max(1,p["stock"]), value=1)
        if st.button("Add to Cart", use_container_width=True, type="primary"):
            _add_to_cart(p, size, color, qty)
            st.success(f"{qty} x {p['name']} added to cart!")
            st.session_state.page = "cart"; st.rerun()

def _add_to_cart(product, size, color, qty):
    if "cart" not in st.session_state:
        st.session_state.cart = []

    found = False
    for item in st.session_state.cart:
        if (item["id"] == product["id"] and
            item["size"] == size and
            item["color"] == color):
            item["qty"] += qty
            found = True
            break
    
    if not found:
        st.session_state.cart.append({
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "size": size,
            "color": color,
            "qty": qty,
            "image_url": product.get("image_url", "")
        })

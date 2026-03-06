import streamlit as st
from utils.database import get_all_products, get_all_categories

def show():
    st.markdown("## Shop All Products")
    categories = get_all_categories()
    cat_map = {"All": None}
    for c in categories: cat_map[c["name"]] = c["id"]
    col1,col2,col3 = st.columns(3)
    with col1: search = st.text_input("Search", placeholder="Search...")
    with col2: cat = st.selectbox("Category", list(cat_map.keys()))
    with col3: sort = st.selectbox("Sort", ["Newest","Price: Low","Price: High"])
    products = get_all_products(active_only=True, category_id=cat_map[cat], search=search)
    if sort == "Price: Low": products.sort(key=lambda x: x["price"])
    elif sort == "Price: High": products.sort(key=lambda x: x["price"], reverse=True)
    if not products: st.info("No products found."); return
    cols = st.columns(3)
    for i,p in enumerate(products):
        with cols[i%3]:
            img = p.get("image_url") or "https://via.placeholder.com/300"
            st.image(img, use_container_width=True)
            st.write(f"**{p['name']}**")
            st.write(f"${p['price']:.2f}")
            st.caption(f"{p.get('category_name','')} | Stock: {p['stock']}")
            c1,c2 = st.columns(2)
            with c1:
                if st.button("View", key=f"v_{p['id\]}", use_container_width=True):
                    st.session_state.selected_product = p["id"]
                    st.session_state.page = "product_detail"; st.rerun()
            with c2:
                if st.button("Add to Cart", key=f"a_{p['id\]}", use_container_width=True):
                    _add(p); st.success("Added!"); st.rerun()

def _add(p):
    sizes = p["sizes"].split(",") if p.get("sizes") else ["One Size"]
    colors = p["colors"].split(",") if p.get("colors") else ["Default"]
    for item in st.session_state.cart:
        if item["id"]==p["id"] and item["size"]==sizes[0] and item["color"]==colors[0]:
            item["qty"]+=1; return
    st.session_state.cart.append({
        "id":p["id"],"name":p["name"],"price":p["price"],
        "size":sizes[0],"color":colors[0],"qty":1,"image":p.get("image_url","")
    })


import streamlit as st
from utils.database import get_featured_products, get_all_categories

def product_card(p):
    badge_html = ""
    if p.get("badge"):
        badge_class = f"badge-{p['badge']}" if p["badge"] in ["new","sale","featured"] else "badge-new"
        badge_html = f'<span class="badge {badge_class}">{p["badge"].upper()}</span>'
    price_html = f'<span class="price-tag">${p["price"]:.2f}</span>'
    if p.get("original_price"):
        price_html += f' <span class="price-original">${p["original_price"]:.2f}</span>'
    img = p.get("image_url") or "https://via.placeholder.com/400x300?text=No+Image"
    return f"""
    <div class="product-card">
        <div style="position:relative;overflow:hidden;height:220px;">
            <img src="{img}" style="width:100%;height:100%;object-fit:cover;"/>
            <div style="position:absolute;top:12px;left:12px;">{badge_html}</div>
        </div>
        <div style="padding:16px;">
            <div style="font-size:12px;color:#6b7280;margin-bottom:4px;">{p.get("category_name","")}</div>
            <div style="font-weight:600;font-size:15px;color:#111;margin-bottom:8px;">{p["name"]}</div>
            <div>{price_html}</div>
            <div style="font-size:12px;color:{"#16a34a" if p["stock"]>5 else "#dc2626"};margin-top:6px;">
                {"✓ In Stock" if p["stock"] > 0 else "✗ Out of Stock"}
            </div>
        </div>
    </div>"""

def show():
    st.markdown("""
    <div class="hero">
        <div style="font-size:13px;letter-spacing:4px;opacity:0.6;margin-bottom:12px;text-transform:uppercase;">New Season 2025</div>
        <h1>Wear Your Story</h1>
        <p>Premium clothing crafted for the modern wardrobe.</p>
    </div>""", unsafe_allow_html=True)
    col1,col2,col3 = st.columns([2,1,2])
    with col2:
        if st.button("🛍️ Shop Now", use_container_width=True, type="primary"):
            st.session_state.page = "products"; st.rerun()
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="text-align:center">Shop by Category</div>', unsafe_allow_html=True)
    categories = get_all_categories()
    cols = st.columns(len(categories))
    icons = {"T-Shirts":"👕","Shirts":"👔","Jackets":"🧥","Jeans":"👖","Hoodies":"🧣","Accessories":"👜"}
    for i, cat in enumerate(categories):
        with cols[i]:
            if st.button(f'{icons.get(cat["name"],"🏷️")} {cat["name"]}', use_container_width=True, key=f'cat_{cat["id"]}'):
                st.session_state.selected_category = cat["id"]
                st.session_state.page = "products"; st.rerun()
    st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">✨ Featured & New Arrivals</div>', unsafe_allow_html=True)
    products = get_featured_products(6)
    cols = st.columns(3)
    for i, p in enumerate(products):
        with cols[i % 3]:
            st.markdown(product_card(p), unsafe_allow_html=True)
            if st.button("View Details", key=f'fp_{p["id"]}', use_container_width=True):
                st.session_state.selected_product = p["id"]
                st.session_state.page = "product_detail"; st.rerun()
            st.markdown("<div style='margin-bottom:16px'></div>", unsafe_allow_html=True)
    col1,col2,col3 = st.columns([2,1,2])
    with col2:
        if st.button("View All Products →", use_container_width=True):
            st.session_state.page = "products"; st.rerun()
    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="text-align:center">Why ThreadCo?</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    features = [("🚚","Free Shipping","On all orders over $50"),("↩️","Easy Returns","30-day hassle-free"),("🌿","Sustainable","Eco-friendly materials"),("⭐","Quality First","Premium fabrics")]
    for col,(icon,title,desc) in zip([c1,c2,c3,c4],features):
        with col:
            st.markdown(f'''<div style="text-align:center;padding:24px 16px;border:1px solid #e5e7eb;border-radius:12px;background:white;">
                <div style="font-size:32px;margin-bottom:10px;">{icon}</div>
                <div style="font-weight:600;font-size:15px;margin-bottom:6px;">{title}</div>
                <div style="font-size:13px;color:#6b7280;">{desc}</div></div>''', unsafe_allow_html=True)
    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
    st.markdown('''<div style="text-align:center;padding:30px;background:#111;color:#9ca3af;border-radius:12px;font-size:13px;">
        © 2025 ThreadCo · Built with ❤️ using Streamlit</div>''', unsafe_allow_html=True)

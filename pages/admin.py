import streamlit as st
from utils.database import (get_dashboard_stats, get_all_products, get_all_orders,
    get_all_users, get_all_categories, create_product, update_product,
    delete_product, update_order_status)

def show():
    st.markdown("## Admin Dashboard")
    tab1,tab2,tab3,tab4 = st.tabs(["Overview","Products","Orders","Users"])
    with tab1:
        s = get_dashboard_stats()
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Customers", s["total_users"])
        c2.metric("Products", s["total_products"])
        c3.metric("Orders", s["total_orders"])
        c4.metric("Revenue", f"${s['total_revenue']:.2f}")
        c5,c6 = st.columns(2)
        c5.metric("Pending", s["pending_orders"])
        c6.metric("Low Stock", s["low_stock"])
    with tab2:
        cats = get_all_categories()
        cat_map = {c["name"]:c["id"] for c in cats}
        st.markdown("#### Add Product")
        col1,col2 = st.columns(2)
        with col1:
            pname=st.text_input("Name",key="pn"); pprice=st.number_input("Price",min_value=0.01,value=29.99,key="pp")
            pstock=st.number_input("Stock",min_value=0,value=10,key="ps"); pcat=st.selectbox("Category",list(cat_map.keys()),key="pc")
        with col2:
            pdesc=st.text_area("Description",key="pd"); psizes=st.text_input("Sizes",value="S,M,L,XL",key="psz")
            pcolors=st.text_input("Colors",value="Black,White",key="pcl"); pimg=st.text_input("Image URL",key="pi")
            pbadge=st.selectbox("Badge",["","new","sale","featured"],key="pb")
        if st.button("Add Product",type="primary"):
            if pname.strip(): create_product(pname,pdesc,pprice,None,cat_map[pcat],pstock,psizes,pcolors,pimg,pbadge); st.success("Added!"); st.rerun()
            else: st.error("Name required.")
        st.markdown("#### All Products")
        for p in get_all_products(active_only=False):
            with st.expander(f"#{p['id']} {p['name']} — ${p['price']}"):
                col1,col2=st.columns(2)
                with col1:
                    en=st.text_input("Name",value=p["name"],key=f"en{p['id']}"); ep=st.number_input("Price",value=float(p["price"]),key=f"ep{p['id']}")
                    es=st.number_input("Stock",value=int(p["stock"]),key=f"es{p['id']}")
                with col2:
                    ea=st.checkbox("Active",value=bool(p["is_active"]),key=f"ea{p['id']}")
                    eb=st.selectbox("Badge",["","new","sale","featured"],key=f"eb{p['id']}")
                c1,c2=st.columns(2)
                with c1:
                    if st.button("Save",key=f"sv{p['id']}"):
                        update_product(p["id"],en,p.get("description",""),ep,p.get("original_price"),p["category_id"],es,p.get("sizes",""),p.get("colors",""),p.get("image_url",""),eb,int(ea))
                        st.success("Saved!"); st.rerun()
                with c2:
                    if st.button("Delete",key=f"dl{p['id']}"):
                        delete_product(p["id"]); st.warning("Deleted"); st.rerun()
    with tab3:
        for order in get_all_orders():
            with st.expander(f"Order #{order['id']} — {order['customer_name']} — ${order['total']:.2f} — {order['status']}"):
                new_s=st.selectbox("Status",["Pending","Processing","Shipped","Delivered","Cancelled"],
                    index=["Pending","Processing","Shipped","Delivered","Cancelled"].index(order["status"]),key=f"os{order['id']}")
                if st.button("Update",key=f"ou{order['id']}"): update_order_status(order["id"],new_s); st.success("Updated!"); st.rerun()
    with tab4:
        import pandas as pd
        users=get_all_users()
        if users: st.dataframe(pd.DataFrame(users),use_container_width=True,hide_index=True)

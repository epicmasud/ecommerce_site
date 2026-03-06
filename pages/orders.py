import streamlit as st
from utils.database import get_user_orders, get_order_items
from utils.auth import get_current_user

def show():
    st.markdown("## My Orders")
    user = get_current_user()
    orders = get_user_orders(user["id"])
    if not orders: st.info("No orders yet."); return
    for order in orders:
        with st.expander(f"Order #{order['id']} — ${order['total']:.2f} — {order['status']} — {order['created_at'][:10]}"):
            for item in get_order_items(order["id"]):
                st.write(f"• {item['product_name']} | {item['size']} | {item['color']} | x{item['quantity']} | ${item['price']*item['quantity']:.2f}")
            st.write(f"**Shipped to:** {order['shipping_name']}, {order['shipping_address']}, {order['shipping_city']}")
            st.write(f"**Status:** {order['status']}")

import streamlit as st
from utils.database import create_order
from utils.auth import get_current_user

def show():
    st.markdown("## Checkout")
    cart = st.session_state.cart
    user = get_current_user()
    if not cart: st.warning("Cart is empty"); return
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("### Shipping Info")
        name = st.text_input("Full Name", value=user["name"])
        address = st.text_input("Address")
        city = st.text_input("City")
        phone = st.text_input("Phone")
    with col2:
        st.markdown("### Order Summary")
        for item in cart:
            st.write(f"{item['name']} x{item['qty']} — ${item['price']*item['qty']:.2f}")
        subtotal = sum(i["price"]*i["qty"] for i in cart)
        shipping = 0 if subtotal>=50 else 9.99
        st.write(f"**Total: ${subtotal+shipping:.2f}**")
        if st.button("Place Order", type="primary", use_container_width=True):
            if not all([name,address,city,phone]):
                st.error("Please fill all fields.")
            else:
                oid = create_order(user["id"], cart, subtotal+shipping,
                    {"name":name,"address":address,"city":city,"phone":phone})
                st.session_state.cart=[]
                st.success(f"Order #{oid} placed successfully!")
                st.balloons()
                st.session_state.page="orders"; st.rerun()

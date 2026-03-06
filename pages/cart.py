import streamlit as st

def show():
    st.markdown("## Your Cart")
    cart = st.session_state.cart
    if not cart:
        st.info("Your cart is empty!")
        if st.button("Shop Now"): st.session_state.page="products"; st.rerun()
        return
    to_remove = []
    for idx,item in enumerate(cart):
        c1,c2,c3,c4 = st.columns([3,1,1,1])
        with c1: st.write(f"**{item['name']}** | {item['size']} | {item['color']}")
        with c2:
            new_qty = st.number_input("Qty", min_value=1, max_value=99,
                value=item["qty"], key=f"qty_{idx}", label_visibility="collapsed")
            if new_qty != item["qty"]: item["qty"]=new_qty; st.rerun()
        with c3: st.write(f"**${item['price']*item['qty']:.2f}**")
        with c4:
            if st.button("Remove", key=f"rm_{idx}"): to_remove.append(idx)
    for i in sorted(to_remove, reverse=True): st.session_state.cart.pop(i)
    if to_remove: st.rerun()
    st.markdown("---")
    subtotal = sum(i["price"]*i["qty"] for i in cart)
    shipping = 0 if subtotal>=50 else 9.99
    st.write(f"Subtotal: **${subtotal:.2f}**")
    st.write(f"Shipping: **{'Free' if shipping==0 else f'${shipping:.2f}'}**")
    st.write(f"### Total: ${subtotal+shipping:.2f}")
    col1,col2 = st.columns(2)
    with col1:
        if st.button("Checkout", type="primary", use_container_width=True):
            from utils.auth import is_logged_in
            if not is_logged_in():
                st.warning("Please login first")
                st.session_state.page="login"; st.rerun()
            else:
                st.session_state.page="checkout"; st.rerun()
    with col2:
        if st.button("Clear Cart", use_container_width=True):
            st.session_state.cart=[]; st.rerun()

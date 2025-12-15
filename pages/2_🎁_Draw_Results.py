import streamlit as st
import random
import math

st.set_page_config(page_title="Draw Results", page_icon="🎁", layout="wide")
st.title("🎁 Prize Draw Results")

# -----------------------
# Session Validation
# -----------------------
required_keys = ["available_numbers", "available_prizes", "original_numbers", "original_prizes"]
for key in required_keys:
    if key not in st.session_state:
        st.error("❌ Session not found. Please start from the setup page.")
        st.stop()

# Init state
st.session_state.setdefault("used_pairs", [])
st.session_state.setdefault("current_draw", [])
st.session_state.setdefault("confirm_return", None)
st.session_state.setdefault("returned_prizes", [])

# -----------------------
# Controls
# -----------------------
col1, col2 = st.columns(2)

with col1:
    if st.session_state["available_prizes"] or st.session_state["returned_prizes"]:
        if st.button("🎉 Draw Next Batch", use_container_width=True):

            # Determine batch size (max 5)
            batch_size = 5

            # Take returned prizes first
            returned_batch = st.session_state["returned_prizes"][:batch_size]
            st.session_state["returned_prizes"] = st.session_state["returned_prizes"][len(returned_batch):]

            # Remaining slots filled from available_prizes
            remaining_slots = batch_size - len(returned_batch)
            new_prizes = st.session_state["available_prizes"][:remaining_slots]
            st.session_state["available_prizes"] = st.session_state["available_prizes"][remaining_slots:]

            # All prizes for this batch
            batch_prizes = returned_batch + new_prizes

            # Pick random numbers for all batch prizes
            if len(st.session_state["available_numbers"]) < len(batch_prizes):
                st.error("Not enough numbers left for this batch.")
                st.stop()

            batch_numbers = random.sample(st.session_state["available_numbers"], len(batch_prizes))

            st.session_state["current_draw"] = []
            for prize, number in zip(batch_prizes, batch_numbers):
                st.session_state["current_draw"].append((prize, number))
                st.session_state["used_pairs"].append({"prize": prize, "number": number, "returned": False})
                st.session_state["available_numbers"].remove(number)

            st.balloons()
    else:
        st.markdown(
            """<div style="background:#E53935;color:white;padding:14px;border-radius:8px;text-align:center;font-weight:bold;">
            ❌ No More Prizes Left For This Draw
            </div>""", unsafe_allow_html=True
        )

# -----------------------
# New Session
# -----------------------
with col2:
    if st.button("🆕 New Session", use_container_width=True):
        st.session_state["available_numbers"] = st.session_state["original_numbers"][:]
        st.session_state["available_prizes"] = st.session_state["original_prizes"][:]
        st.session_state["used_pairs"] = []
        st.session_state["current_draw"] = []
        st.session_state["returned_prizes"] = []
        st.session_state["confirm_return"] = None
        st.rerun()

# -----------------------
# Return prize logic
# -----------------------
if st.session_state["confirm_return"]:
    item = st.session_state["confirm_return"]
    st.markdown("---")
    st.warning(f"⚠️ Return prize **{item['prize']}** back to next draw?")
    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("✅ Yes", use_container_width=True):
            st.session_state["returned_prizes"].append(item["prize"])
            item["returned"] = True
            st.session_state["confirm_return"] = None
            st.rerun()
    with col_no:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state["confirm_return"] = None
            st.rerun()

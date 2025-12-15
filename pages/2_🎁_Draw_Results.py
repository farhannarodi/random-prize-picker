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

# -----------------------
# Initialize session state
# -----------------------
st.session_state.setdefault("used_pairs", [])
st.session_state.setdefault("current_draw", [])
st.session_state.setdefault("confirm_return", None)

# -----------------------
# Helper: render card
# -----------------------
def render_card(title, value, color, font_size, tooltip=None):
    tip = f'title="{tooltip}"' if tooltip else ""
    return f"""
    <div {tip} style="
        background:{color};
        padding:18px;
        border-radius:14px;
        text-align:center;
        color:white;
        box-shadow:0 4px 10px rgba(0,0,0,0.15);
        min-height:120px;
        font-family:Segoe UI, sans-serif;
        margin-bottom:12px;
    ">
        <div style="font-size:14px; opacity:0.85;">{title}</div>
        <div style="font-size:{font_size}px; font-weight:bold;">{value}</div>
    </div>
    """

# -----------------------
# Controls
# -----------------------
col1, col2 = st.columns(2)

with col1:
    if st.session_state["available_prizes"] or any(p["returned"] for p in st.session_state["used_pairs"]):
        if st.button("🎉 Draw Next Batch", use_container_width=True):

            batch_size = 5
            batch_prizes = []

            # 1️⃣ Pull returned prizes first
            for item in st.session_state["used_pairs"]:
                if item["returned"] and len(batch_prizes) < batch_size:
                    batch_prizes.append(item)
                    item["returned"] = False
                    item["number"] = None  # will assign new number

            # 2️⃣ Fill remaining batch from available prizes
            remaining_slots = batch_size - len(batch_prizes)
            for _ in range(remaining_slots):
                if st.session_state["available_prizes"]:
                    prize_name = st.session_state["available_prizes"].pop(0)
                    batch_prizes.append({"prize": prize_name, "number": None, "returned": False})

            # 3️⃣ Assign random numbers from available_numbers
            if len(st.session_state["available_numbers"]) < len(batch_prizes):
                st.error("Not enough numbers left for this batch.")
                st.stop()

            batch_numbers = random.sample(st.session_state["available_numbers"], len(batch_prizes))
            for item, num in zip(batch_prizes, batch_numbers):
                item["number"] = num
                st.session_state["available_numbers"].remove(num)
                # Add to used_pairs if not already in list
                if item not in st.session_state["used_pairs"]:
                    st.session_state["used_pairs"].append(item)

            st.session_state["current_draw"] = batch_prizes
            st.balloons()
    else:
        st.markdown(
            """<div style="background:#E53935;color:white;padding:14px;border-radius:8px;text-align:center;font-weight:bold;">
            ❌ No More Prizes Left For This Draw
            </div>""",
            unsafe_allow_html=True
        )

with col2:
    if st.button("🆕 New Session", use_container_width=True):
        st.session_state["available_numbers"] = st.session_state["original_numbers"][:]
        st.session_state["available_prizes"] = st.session_state["original_prizes"][:]
        st.session_state["used_pairs"] = []
        st.session_state["current_draw"] = []
        st.session_state["confirm_return"] = None
        st.rerun()

# -----------------------
# Session Info
# -----------------------
remaining_prizes = len(st.session_state["available_prizes"]) + sum(p["returned"] for p in st.session_state["used_pairs"])
st.markdown(f"### 🧾 Session Info\n**Remaining Prizes:** {remaining_prizes}")

# -----------------------
# Current Draw (max 5)
# -----------------------
if st.session_state["current_draw"]:
    st.markdown("---")
    st.subheader("🏆 Current Draw")

    cols = st.columns(5)
    for i, item in enumerate(st.session_state["current_draw"]):
        prize = item["prize"]
        number = item["number"]
        with cols[i]:
            st.markdown(render_card(prize, number, "#1E88E5", 34), unsafe_allow_html=True)

# -----------------------
# Numbers Already Drawn (clickable, rows of 10)
# -----------------------
if st.session_state["used_pairs"]:
    st.markdown("---")
    st.subheader("🚫 Numbers Already Drawn")

    # Sort: active first, returned last
    used_sorted = sorted(st.session_state["used_pairs"], key=lambda x: x["returned"])
    rows = math.ceil(len(used_sorted) / 10)

    for r in range(rows):
        cols = st.columns(10)
        for c, item in enumerate(used_sorted[r*10:(r+1)*10]):
            with cols[c]:
                prize = item["prize"]
                number = item["number"]
                returned = item["returned"]

                if returned:
                    st.markdown(render_card(prize, number, "#9E9E9E", 20, tooltip="Prize Returned"), unsafe_allow_html=True)
                else:
                    if st.button(f"{prize}\n{number}", key=f"select_{r}_{c}", use_container_width=True):
                        st.session_state["confirm_return"] = item
                        st.rerun()

# -----------------------
# Return confirmation modal
# -----------------------
if st.session_state["confirm_return"]:
    item = st.session_state["confirm_return"]
    st.markdown("---")
    st.warning(f"⚠️ Return prize **{item['prize']}** to next draw?")

    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("✅ Yes", use_container_width=True):
            item["returned"] = True
            st.session_state["confirm_return"] = None
            st.rerun()
    with col_no:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state["confirm_return"] = None
            st.rerun()

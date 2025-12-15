import streamlit as st
import random
import math

st.set_page_config(
    page_title="Draw Results",
    page_icon="🎁",
    layout="wide"
)

st.title("🎁 Prize Draw Results")

# -----------------------
# Session Validation
# -----------------------
required_keys = [
    "available_numbers",
    "available_prizes",
    "original_numbers",
    "original_prizes"
]

for key in required_keys:
    if key not in st.session_state:
        st.error("❌ Session not found. Please start from the setup page.")
        st.stop()

# Init draw state
st.session_state.setdefault("used_pairs", [])
st.session_state.setdefault("current_draw", [])

# -----------------------
# Controls
# -----------------------
col1, col2 = st.columns(2)

# Draw Next Batch
with col1:
    if st.session_state["available_prizes"]:
        if st.button("🎉 Draw Next Batch", use_container_width=True):

            batch_size = min(5, len(st.session_state["available_prizes"]))
            prizes = st.session_state["available_prizes"][:batch_size]
            numbers = random.sample(
                st.session_state["available_numbers"],
                batch_size
            )

            st.session_state["current_draw"] = list(zip(prizes, numbers))

            # Remove drawn items
            st.session_state["available_prizes"] = st.session_state["available_prizes"][batch_size:]
            for prize, number in st.session_state["current_draw"]:
                st.session_state["available_numbers"].remove(number)
                st.session_state["used_pairs"].append((prize, number))

            st.balloons()
    else:
        st.markdown(
            """
            <div style="
                background:#E53935;
                color:white;
                padding:14px;
                border-radius:8px;
                text-align:center;
                font-weight:bold;
            ">
                ❌ No More Prizes Left For This Draw
            </div>
            """,
            unsafe_allow_html=True
        )

# New Session
with col2:
    if st.button("🆕 New Session", use_container_width=True):
        st.session_state["available_numbers"] = st.session_state["original_numbers"][:]
        st.session_state["available_prizes"] = st.session_state["original_prizes"][:]
        st.session_state["used_pairs"] = []
        st.session_state["current_draw"] = []
        st.rerun()

# -----------------------
# Session Info
# -----------------------
st.markdown("### 🧾 Session Info")
st.markdown(f"**Remaining Prizes:** {len(st.session_state['available_prizes'])}")

# -----------------------
# Card Renderer
# -----------------------
def render_card(title, value, color, font_size):
    return f"""
    <div style="
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
# Current Draw (Max 5)
# -----------------------
if st.session_state["current_draw"]:
    st.markdown("---")
    st.subheader("🏆 Current Draw")

    cols = st.columns(5)
    for i, (prize, number) in enumerate(st.session_state["current_draw"]):
        with cols[i]:
            st.markdown(
                render_card(prize, number, "#1E88E5", 34),
                unsafe_allow_html=True
            )

# -----------------------
# Already Drawn (Rows of 10)
# -----------------------
if st.session_state["used_pairs"]:
    st.markdown("---")
    st.subheader("🚫 Numbers Already Drawn")

    used = st.session_state["used_pairs"]
    rows = math.ceil(len(used) / 10)

    for r in range(rows):
        cols = st.columns(10)
        for c, (prize, number) in enumerate(used[r*10:(r+1)*10]):
            with cols[c]:
                st.markdown(
                    render_card(prize, number, "#E53935", 20),
                    unsafe_allow_html=True
                )

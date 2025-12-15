import streamlit as st
import random
import math

# Fullscreen / Wide layout
st.set_page_config(
    page_title="Draw Results",
    page_icon="🎁",
    layout="wide"
)

st.title("🎁 Prize Draw Results")

# Initialize session state if not present
if "available_numbers" not in st.session_state:
    st.session_state["available_numbers"] = list(range(1, 51))  # Example: 50 numbers
if "available_prizes" not in st.session_state:
    st.session_state["available_prizes"] = ["Prize " + str(i) for i in range(1, 21)]
if "used_numbers" not in st.session_state:
    st.session_state["used_numbers"] = []
if "current_draw" not in st.session_state:
    st.session_state["current_draw"] = []  # List of tuples (prize, number)

# --- Session Info ---
remaining_prizes = len(st.session_state.get("available_prizes", []))
st.markdown(f"""
### 🧾 Session Info
- **Remaining Prizes:** {remaining_prizes}
""")

# --- Buttons ---
col_top = st.columns([1,1])

# Left column: Draw Next Batch / No More Prizes
with col_top[0]:
    if st.session_state["available_prizes"] and st.session_state["available_numbers"]:
        if st.button("🎉 Draw Next Batch", use_container_width=True):
            # Draw up to 5 prizes
            batch_size = min(5, len(st.session_state["available_prizes"]))
            prizes_to_draw = st.session_state["available_prizes"][:batch_size]
            numbers_to_draw = random.sample(st.session_state["available_numbers"], batch_size)

            # Pair prizes with numbers
            st.session_state["current_draw"] = list(zip(prizes_to_draw, numbers_to_draw))

            # Remove drawn prizes from available and update used numbers
            for prize, number in st.session_state["current_draw"]:
                st.session_state["used_numbers"].append(number)
                st.session_state["available_numbers"].remove(number)
                st.session_state["available_prizes"].remove(prize)

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
                font-size:16px;
            ">
                ❌ No More Prizes to Draw
            </div>
            """,
            unsafe_allow_html=True
        )

# Right column: New Session
with col_top[1]:
    if st.button("🆕 New Session", use_container_width=True):
        st.session_state["available_numbers"] = list(range(1, 51))
        st.session_state["available_prizes"] = ["Prize " + str(i) for i in range(1, 21)]
        st.session_state["used_numbers"] = []
        st.session_state["current_draw"] = []
        st.rerun()

# --- Function to Render Cards ---
def render_card(title, value, color="#1E88E5", font_size=32):
    return f"""
    <div style="
        background:{color};
        padding:22px;
        border-radius:16px;
        text-align:center;
        color:white;
        box-shadow:0 4px 12px rgba(0,0,0,0.15);
        min-height:140px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-bottom:12px;
        display:flex;
        flex-direction:column;
        justify-content:center;
    ">
        <div style="font-size:16px; opacity:0.85; margin-bottom:8px;">{title}</div>
        <div style="font-size:{font_size}px; font-weight:bold;">{value}</div>
    </div>
    """

# --- Current Draw Results (5 per row) ---
if st.session_state["current_draw"]:
    st.markdown("---")
    st.subheader("🏆 Current Draw")

    items = st.session_state["current_draw"]
    cols = st.columns(5, gap="medium")  # max 5 columns per row
    for c, (prize, number) in enumerate(items):
        with cols[c]:
            st.markdown(render_card(prize, number, color="#1E88E5", font_size=34), unsafe_allow_html=True)

# --- Used Numbers (Rows of 10) ---
if st.session_state["used_numbers"]:
    st.markdown("---")
    st.subheader("🚫 Numbers Already Drawn")

    used = st.session_state["used_numbers"]
    rows = math.ceil(len(used)/10)

    for r in range(rows):
        cols = st.columns(10, gap="small")
        for c, number in enumerate(used[r*10:(r+1)*10]):
            with cols[c]:
                st.markdown(render_card("", number, color="#E53935", font_size=20), unsafe_allow_html=True)

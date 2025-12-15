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

# Initialize state
st.session_state.setdefault("used_pairs", [])
st.session_state.setdefault("current_draw", [])
st.session_state.setdefault("confirm_return", None)

# -----------------------
# Controls
# -----------------------
col1, col2 = st.columns(2)

with col1:
    if st.session_state["available_prizes"]:
        if st.button("🎉 Draw Next Batch", use_container_width=True):

            batch_size = min(5, len(st.session_state["available_prizes"]))
            prizes = st.session_state["available_prizes"][:batch_size]
            numbers = random.sample(
                st.session_state["available_numbers"],
                batch_size
            )

            st.session_state["current_draw"] = []

            for prize, number in zip(prizes, numbers):
                st.session_state["current_draw"].append((prize, number))
                st.session_state["used_pairs"].append({
                    "prize": prize,
                    "number": number,
                    "returned": False
                })
                st.session_state["available_numbers"].remove(number)

            st.session_state["available_prizes"] = st.session_state["available_prizes"][batch_size:]
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
remaining_prizes = len(st.session_state["available_prizes"])
st.markdown("### 🧾 Session Info")
st.markdown(f"**Remaining Prizes:** {remaining_prizes}")

# -----------------------
# Card Renderer
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
# Numbers Already Drawn (Styled + Clickable + Sorted)
# -----------------------
if st.session_state["used_pairs"]:
    st.markdown("---")
    st.subheader("🚫 Numbers Already Drawn")

    # Sort: active first, returned last
    used_sorted = sorted(
        st.session_state["used_pairs"],
        key=lambda x: x["returned"]
    )

    rows = math.ceil(len(used_sorted) / 10)

    for r in range(rows):
        cols = st.columns(10)
        for c, item in enumerate(used_sorted[r*10:(r+1)*10]):
            prize = item["prize"]
            number = item["number"]
            returned = item["returned"]

            color = "#9E9E9E" if returned else "#1E88E5"
            tooltip = "Prize Returned" if returned else None

            with cols[c]:
                # Use form to simulate clickable card
                form_key = f"return_form_{r}_{c}"
                with st.form(form_key):
                    html = render_card(prize, number, color, 20, tooltip=tooltip)
                    st.markdown(html, unsafe_allow_html=True)

                    if not returned:
                        # Invisible submit button over card
                        if st.form_submit_button("Return"):
                            st.session_state["confirm_return"] = item
                            st.rerun()

# -----------------------
# Confirmation Modal
# -----------------------
if st.session_state["confirm_return"]:
    item = st.session_state["confirm_return"]

    st.markdown("---")
    st.warning(
        f"⚠️ Return prize **{item['prize']}** (Number {item['number']}) back to the prize pool?"
    )

    col_yes, col_no = st.columns(2)

    with col_yes:
        if st.button("✅ Yes, Return Prize", use_container_width=True):
            st.session_state["available_prizes"].append(item["prize"])
            item["returned"] = True
            st.session_state["confirm_return"] = None
            st.rerun()

    with col_no:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state["confirm_return"] = None
            st.rerun()

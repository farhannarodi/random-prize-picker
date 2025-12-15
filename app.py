import streamlit as st

st.set_page_config(
    page_title="Prize Draw Setup",
    page_icon="🎁",
    layout="wide"
)

st.title("🎁 Prize Draw Setup")

# -----------------------
# Number Range
# -----------------------
st.subheader("🔢 Number Range")

col1, col2 = st.columns(2)
with col1:
    start_number = st.number_input(
        "Start Number",
        min_value=1,
        value=1
    )

with col2:
    end_number = st.number_input(
        "End Number",
        min_value=start_number + 1,
        value=50
    )

# -----------------------
# Prize Setup
# -----------------------
st.subheader("🏆 Prize Setup")

prize_count = st.number_input(
    "Number of Prizes",
    min_value=1,
    max_value=1000,   # ✅ Increased limit
    value=5,
    step=1
)

st.markdown("### Enter Prize Names")

prizes = []
for i in range(prize_count):
    prize = st.text_input(
        f"Prize {i + 1}",
        key=f"prize_{i}"
    )
    prizes.append(prize if prize.strip() else f"Prize {i + 1}")

# -----------------------
# Start Session
# -----------------------
if st.button("🚀 Start Draw Session", use_container_width=True):

    if (end_number - start_number + 1) < prize_count:
        st.error("❌ Number range must be greater than or equal to number of prizes.")
        st.stop()

    # Save originals
    st.session_state["original_numbers"] = list(range(start_number, end_number + 1))
    st.session_state["original_prizes"] = prizes.copy()

    # Working copies
    st.session_state["available_numbers"] = st.session_state["original_numbers"][:]
    st.session_state["available_prizes"] = st.session_state["original_prizes"][:]

    # Reset draw data
    st.session_state["used_pairs"] = []
    st.session_state["current_draw"] = []

    st.success(f"✅ Session started with {prize_count} prizes")
    st.switch_page("pages/2_🎁_Draw_Results.py")

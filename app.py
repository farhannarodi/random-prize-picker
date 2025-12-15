import streamlit as st

st.set_page_config(
    page_title="Prize Draw Setup",
    page_icon="🎉",
    layout="centered"
)

st.title("🎉 Prize Draw Setup")
st.caption("Set your number range and prizes")

# Number range
col1, col2 = st.columns(2)

with col1:
    start_range = st.number_input(
        "Start of range",
        min_value=1,
        value=1
    )

with col2:
    end_range = st.number_input(
        "End of range",
        min_value=start_range + 1,
        value=50
    )

# Number of prizes
prize_count = st.number_input(
    "🎁 Number of prizes",
    min_value=1,
    max_value=20,
    value=5
)

st.divider()
st.subheader("🏷️ Prize Names")

prize_names = []
for i in range(prize_count):

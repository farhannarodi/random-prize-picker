import streamlit as st

st.set_page_config(
    page_title="Prize Draw Setup",
    page_icon="🎁",
    layout="wide"
)

st.title("🎁 Prize Draw Setup")

# Number range
st.subheader("🔢 Number Range")

col1, col2 = st.columns(2)
with col1:
    start_number = st.number_input("Start Number", min_value=1, value=1)
with col2:
    end_number = st.number_input("End Number", min_value=start_number + 1, value=50)

# Prize input (NO numeric limits)
st.subheader("🏆 Prize List (Up to 1,000 prizes)")

prize_input = st.text_area(
    "Enter ONE prize per line",
    height=300,
    placeholder="Prize 1\nPrize 2\nPrize 3\n..."
)

prizes = [p.strip() for p in prize_input.split("\n") if p.strip()]

if len(prizes) > 1000:
    st.error("❌ Maximum 1,000 prizes allowed")
    st.stop()

if st.button("🚀 Start Draw Session", use_container_width=True):
    if not prizes:
        st.error("Please enter at least one prize.")
        st.stop()

    if (end_number - start_number + 1) < len(prizes):
        st.error("Number range must be >= number of prizes.")
        st.stop()

    st.session_state["original_numbers"] = list(range(start_number, end_number + 1))
    st.session_state["original_prizes"] = prizes.copy()

    st.session_state["available_numbers"] = st.session_state["original_numbers"][:]
    st.session_state["available_prizes"] = st.session_state["original_prizes"][:]

    st.session_state["used_pairs"] = []
    st.session_state["current_draw"] = []

    st.success(f"✅ Session started with {len(prizes)} prizes")
    st.switch_page("pages/2_🎁_Draw_Results.py")

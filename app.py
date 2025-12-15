import streamlit as st

st.set_page_config(
    page_title="Prize Draw Setup",
    page_icon="🎉",
    layout="centered"
)

st.title("🎉 Prize Draw Setup")
st.caption("Set your number range and prize count")

with st.container():
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

prizes = st.slider(
    "🎁 Number of prizes",
    min_value=1,
    max_value=20,
    value=5
)

valid = prizes <= (end_range - start_range + 1)

if not valid:
    st.error("❌ Number of prizes exceeds range size")
else:
    st.success("✅ Ready to draw!")

    if st.button("🎲 Proceed to Draw", use_container_width=True):
        st.session_state["start"] = start_range
        st.session_state["end"] = end_range
        st.session_state["prizes"] = prizes
        st.switch_page("pages/2_🎁_Draw_Results.py")

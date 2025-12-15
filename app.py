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

# Prize name inputs (THIS BLOCK FIXES THE ERROR)
prize_names = []
for i in range(int(prize_count)):
    name = st.text_input(
        f"Prize {i + 1} name",
        value=f"Prize {i + 1}"
    )
    prize_names.append(name)

# Validation
valid = prize_count <= (end_range - start_range + 1)

if not valid:
    st.error("❌ Number of prizes exceeds available numbers")
else:
    if st.button("🎲 Start Session", use_container_width=True):
        st.session_state.clear()

        st.session_state["start"] = start_range
        st.session_state["end"] = end_range
        st.session_state["prizes"] = prize_names

        st.session_state["available_numbers"] = list(
            range(start_range, end_range + 1)
        )
        st.session_state["used_numbers"] = []
        st.session_state["session_number"] = 1

        st.switch_page("pages/2_🎁_Draw_Results.py")

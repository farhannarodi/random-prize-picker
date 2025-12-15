import streamlit as st
import random

st.set_page_config(
    page_title="Draw Results",
    page_icon="🎁",
    layout="centered"
)

st.title("🎁 Prize Draw Results")

if "prizes" not in st.session_state:
    st.warning("Please configure the draw first.")
    st.stop()

start = st.session_state["start"]
end = st.session_state["end"]
prize_names = st.session_state["prizes"]

st.markdown(f"""
### 🎯 Draw Details
- **Range:** {start} – {end}
- **Prizes:** {len(prize_names)}
""")

if st.button("🎉 Draw Numbers", use_container_width=True):
    numbers = random.sample(
        range(start, end + 1),
        len(prize_names)
    )
    st.session_state["results"] = dict(zip(prize_names, numbers))

if "results" in st.session_state:
    st.divider()
    st.subheader("🏆 Winners")

    for prize, number in st.session_state["results"].items():
        st.markdown(
            f"""
            <div style="
                background:#1f77b4;
                padding:20px;
                border-radius:14px;
                margin-bottom:15px;
                color:white;
                box-shadow:0 6px 12px rgba(0,0,0,0.25);
            ">
                <div style="font-size:18px; opacity:0.9;">
                    {prize}
                </div>
                <div style="font-size:32px; font-weight:bold;">
                    {number}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.divider()

if st.button("🔄 New Draw", use_container_width=True):
    st.session_state.clear()
    st.switch_page("app.py")

import streamlit as st
import random

st.set_page_config(
    page_title="Draw Results",
    page_icon="🎁",
    layout="centered"
)

st.title("🎁 Draw Results")

if "start" not in st.session_state:
    st.warning("Please configure the draw first.")
    st.stop()

start = st.session_state["start"]
end = st.session_state["end"]
prizes = st.session_state["prizes"]

st.markdown(f"""
### 🎯 Draw Information
- **Range:** {start} – {end}
- **Prizes:** {prizes}
""")

if st.button("🎉 Draw Numbers", use_container_width=True):
    st.session_state["winners"] = random.sample(
        range(start, end + 1), prizes
    )

if "winners" in st.session_state:
    st.divider()
    st.subheader("🏆 Winning Numbers")

    cols = st.columns(5)
    for i, num in enumerate(st.session_state["winners"]):
        with cols[i % 5]:
            st.markdown(
                f"""
                <div style="
                    background:#4CAF50;
                    padding:22px;
                    border-radius:14px;
                    text-align:center;
                    color:white;
                    font-size:26px;
                    font-weight:bold;
                    box-shadow:0 6px 12px rgba(0,0,0,0.25);
                ">
                    {num}
                </div>
                """,
                unsafe_allow_html=True
            )

st.divider()

if st.button("🔄 New Draw", use_container_width=True):
    st.session_state.clear()
    st.switch_page("app.py")

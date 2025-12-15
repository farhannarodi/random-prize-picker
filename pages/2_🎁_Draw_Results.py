import streamlit as st
import random

st.set_page_config(
    page_title="Draw Results",
    page_icon="🎁",
    layout="centered"
)

st.title("🎁 Prize Draw Results")

required_keys = [
    "start", "end", "prizes",
    "available_numbers", "used_numbers",
    "session_number"
]

if not all(k in st.session_state for k in required_keys):
    st.warning("Please start a session first.")
    st.stop()

start = st.session_state["start"]
end = st.session_state["end"]
prize_names = st.session_state["prizes"]
available = st.session_state["available_numbers"]

st.markdown(f"""
### 🧾 Session #{st.session_state["session_number"]}
- **Range:** {start} – {end}
- **Remaining numbers:** {len(available)}
""")

# Draw button
if st.button("🎉 Draw Numbers", use_container_width=True):
    if len(available) < len(prize_names):
        st.error("❌ Not enough numbers left for this draw.")
    else:
        drawn = random.sample(available, len(prize_names))

        # Remove drawn numbers from available pool
        for n in drawn:
            available.remove(n)

        st.session_state["used_numbers"].extend(drawn)
        st.session_state["results"] = dict(zip(prize_names, drawn))

# Display results
if "results" in st.session_state:
    st.divider()
    st.subheader("🏆 Draw Results")

    for prize, number in st.session_state["results"].items():
        st.markdown(
            f"""
            <div style="
                background:#4CAF50;
                padding:20px;
                border-radius:14px;
                margin-bottom:15px;
                color:white;
                box-shadow:0 6px 12px rgba(0,0,0,0.25);
            ">
                <div style="font-size:18px;">{prize}</div>
                <div style="font-size:32px; font-weight:bold;">
                    {number}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Used numbers list
if st.session_state["used_numbers"]:
    st.divider()
    st.subheader("📜 Numbers Already Drawn")
    st.write(sorted(st.session_state["used_numbers"]))

st.divider()

col1, col2 = st.columns(2)

# Same session, continue drawing
with col1:
    if st.button("🔄 New Draw (Same Session)", use_container_width=True):
        st.session_state.pop("results", None)

# New session
with col2:
    if st.button("🆕 New Session", use_container_width=True):
        st.session_state["available_numbers"] = list(
            range(start, end + 1)
        )
        st.session_state["used_numbers"] = []
        st.session_state["session_number"] += 1
        st.session_state.pop("results", None)

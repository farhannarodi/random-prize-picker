import streamlit as st
import random
import math

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

# 🎉 DRAW NUMBERS
if st.button("🎉 Draw Numbers", use_container_width=True):
    if len(available) < len(prize_names):
        st.error("❌ Not enough numbers left for this draw.")
    else:
        drawn = random.sample(available, len(prize_names))

        for n in drawn:
            available.remove(n)

        st.session_state["used_numbers"].extend(drawn)
        st.session_state["results"] = dict(zip(prize_names, drawn))

# 🏆 DRAW RESULTS (5 PER ROW)
if "results" in st.session_state:
    st.divider()
    st.subheader("🏆 Draw Results")

    items = list(st.session_state["results"].items())
    rows = math.ceil(len(items) / 5)

    for r in range(rows):
        cols = st.columns(5)
        for c, (prize, number) in enumerate(items[r*5:(r+1)*5]):
            with cols[c]:
                st.markdown(
                    f"""
                    <div style="
                        background:#4CAF50;
                        padding:18px;
                        border-radius:14px;
                        text-align:center;
                        color:white;
                        box-shadow:0 6px 12px rgba(0,0,0,0.25);
                        min-height:120px;
                    ">
                        <div style="font-size:16px; opacity:0.9;">
                            {prize}
                        </div>
                        <div style="font-size:32px; font-weight:bold;">
                            {number}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# 🔴 USED NUMBERS (RED BOXES, 5 PER ROW)
if st.session_state["used_numbers"]:
    st.divider()
    st.subheader("🚫 Numbers Already Drawn")

    used = sorted(st.session_state["used_numbers"])
    rows = math.ceil(len(used) / 5)

    for r in range(rows):
        cols = st.columns(5)
        for c, number in enumerate(used[r*5:(r+1)*5]):
            with cols[c]:
                st.markdown(
                    f"""
                    <div style="
                        background:#D32F2F;
                        padding:14px;
                        border-radius:10px;
                        text-align:center;
                        color:white;
                        font-size:20px;
                        font-weight:bold;
                        box-shadow:0 4px 8px rgba(0,0,0,0.25);
                    ">
                        {number}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

st.divider()

# 🆕 NEW SESSION
if st.button("🆕 New Session", use_container_width=True):
    st.session_state["available_numbers"] = list(
        range(start, end + 1)
    )
    st.session_state["used_numbers"] = []
    st.session_state["session_number"] += 1
    st.session_state.pop("results", None)
    st.rerun()

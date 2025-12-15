import streamlit as st
import random
import math

# Fullscreen / Wide layout
st.set_page_config(
    page_title="Draw Results",
    page_icon="🎁",
    layout="wide"
)

# Auto-refresh every 5 seconds in presenter mode
if "presenter_mode" not in st.session_state:
    st.session_state["presenter_mode"] = False

if st.session_state["presenter_mode"]:
    st_autorefresh = st.experimental_rerun()  # triggers page refresh
    st.experimental_set_query_params(refresh="true")
    st.experimental_singleton.clear()  # optional: clear singleton caches

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

# Control buttons (only show in normal mode)
if not st.session_state["presenter_mode"]:
    col_top = st.columns(2)
    with col_top[0]:
        if st.button("🎉 Draw Numbers", use_container_width=True):
            if len(available) < len(prize_names):
                st.error("❌ Not enough numbers left for this draw.")
            else:
                drawn = random.sample(available, len(prize_names))
                for n in drawn:
                    available.remove(n)
                st.session_state["used_numbers"].extend(drawn)
                st.session_state["results"] = dict(zip(prize_names, drawn))
                st.session_state["confetti"] = True

    with col_top[1]:
        if st.button("🆕 New Session", use_container_width=True):
            st.session_state["available_numbers"] = list(range(start, end + 1))
            st.session_state["used_numbers"] = []
            st.session_state["session_number"] += 1
            st.session_state.pop("results", None)
            st.session_state.pop("confetti", None)
            st.rerun()

    # Presenter mode toggle
    if st.button("📺 Enter Presenter Mode", use_container_width=True):
        st.session_state["presenter_mode"] = True
        st.rerun()
else:
    if st.button("🔙 Exit Presenter Mode", use_container_width=True):
        st.session_state["presenter_mode"] = False
        st.rerun()
    # Auto-refresh every 5 seconds in presenter mode
    st.experimental_set_query_params(auto_refresh="true")
    st_autorefresh = st.experimental_rerun()

# Trigger confetti only once per new draw
if "confetti" in st.session_state and st.session_state["confetti"]:
    st.balloons()
    st.session_state["confetti"] = False

# 🏆 DRAW RESULTS (5 per row)
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
                        padding:24px;
                        border-radius:16px;
                        text-align:center;
                        color:white;
                        box-shadow:0 6px 12px rgba(0,0,0,0.25);
                        min-height:140px;
                        font-family:sans-serif;
                    ">
                        <div style="font-size:18px; opacity:0.9;">
                            {prize}
                        </div>
                        <div style="font-size:36px; font-weight:bold;">
                            {number}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# 🔴 USED NUMBERS (5 per row)
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
                        padding:18px;
                        border-radius:12px;
                        text-align:center;
                        color:white;
                        font-size:22px;
                        font-weight:bold;
                        box-shadow:0 4px 8px rgba(0,0,0,0.25);
                        font-family:sans-serif;
                    ">
                        {number}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

import streamlit as st
import random
import math

# Fullscreen / Wide layout
st.set_page_config(
    page_title="Draw Results",
    page_icon="🎁",
    layout="wide"
)

st.title("🎁 Prize Draw Results")

# Ensure session state keys exist
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

# Session info
st.markdown(f"""
### 🧾 Session #{st.session_state['session_number']}
**Range:** {start} – {end}  
**Remaining numbers:** {len(available)}
""")

# DRAW NUMBERS & NEW SESSION buttons
col_top = st.columns([1,1])

# Left column: Draw / No More Numbers
with col_top[0]:
    if len(available) == 0:
        st.markdown(
            """
            <div style="
                background:#E53935;
                color:white;
                padding:14px;
                border-radius:8px;
                text-align:center;
                font-weight:bold;
                font-size:16px;
            ">
                ❌ No More Numbers Left for this draw
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        if st.button("🎉 Draw Numbers", use_container_width=True):
            if len(available) < len(prize_names):
                st.error("❌ Not enough numbers left for this draw.")
            else:
                drawn = random.sample(available, len(prize_names))
                for n in drawn:
                    available.remove(n)
                    st.session_state["used_numbers"].append(n)
                # Store paired prize-number results
                st.session_state["results"] = dict(zip(prize_names, drawn))
                st.balloons()

# Right column: New Session button
with col_top[1]:
    if st.button("🆕 New Session", use_container_width=True):
        st.session_state["available_numbers"] = list(range(start, end + 1))
        st.session_state["used_numbers"] = []
        st.session_state["session_number"] += 1
        st.session_state.pop("results", None)
        st.rerun()

# Function to render cards
def render_card(title, value, color="#4CAF50", font_size=32):
    return f"""
    <div style="
        background:{color};
        padding:22px;
        border-radius:16px;
        text-align:center;
        color:white;
        box-shadow:0 4px 12px rgba(0,0,0,0.15);
        min-height:140px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-bottom:12px;
        display:flex;
        flex-direction:column;
        justify-content:center;
    ">
        <div style="font-size:16px; opacity:0.85; margin-bottom:8px;">{title}</div>
        <div style="font-size:{font_size}px; font-weight:bold;">{value}</div>
    </div>
    """

# DRAW RESULTS (Paired prizes + numbers, max 5 per row)
if "results" in st.session_state and st.session_state["results"]:
    st.markdown("---")
    st.subheader("🏆 Draw Results")

    items = list(st.session_state["results"].items())
    rows = math.ceil(len(items) / 5)

    for r in range(rows):
        cols = st.columns(5, gap="medium")
        for c, (prize, number) in enumerate(items[r*5:(r+1)*5]):
            with cols[c]:
                st.markdown(render_card(prize, number, color="#1E88E5", font_size=34), unsafe_allow_html=True)

# USED NUMBERS (rows of 10, soft red)
if st.session_state["used_numbers"]:
    st.markdown("---")
    st.subheader("🚫 Numbers Already Drawn")

    used = sorted(st.session_state["used_numbers"])
    rows = math.ceil(len(used) / 10)

    for r in range(rows):
        cols = st.columns(10, gap="small")
        for c, number in enumerate(used[r*10:(r+1)*10]):
            with cols[c]:
                st.markdown(render_card("", number, color="#E53935", font_size=20), unsafe_allow_html=True)

import streamlit as st
import random
import math

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="Draw Results",
    page_icon="🎁",
    layout="wide"
)

st.title("🎁 Prize Draw Results")

# -----------------------
# Global CSS
# -----------------------
st.markdown("""
<style>

.card {
    position: relative;
    border-radius: 14px;
    padding: 16px;
    height: 140px;
    text-align: center;
    font-family: Segoe UI, sans-serif;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

/* Hover animation */
.card.active:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 22px rgba(0,0,0,0.25);
    cursor: pointer;
}

/* Returned / disabled */
.card.returned {
    background: #9E9E9E !important;
    cursor: not-allowed;
    box-shadow: none;
    transform: none;
}

/* Ripple */
.card::after {
    content: "";
    position: absolute;
    width: 12px;
    height: 12px;
    background: rgba(255,255,255,0.5);
    border-radius: 50%;
    transform: scale(0);
    opacity: 0;
    pointer-events: none;
}

.card.active:active::after {
    animation: ripple 0.6s ease-out;
}

@keyframes ripple {
    0% { transform: scale(0); opacity: 0.6; }
    100% { transform: scale(18); opacity: 0; }
}

/* Glow for current draw */
.glow {
    animation: glowPulse 1.8s infinite alternate;
}

@keyframes glowPulse {
    from { box-shadow: 0 0 8px rgba(30,136,229,0.5); }
    to { box-shadow: 0 0 18px rgba(30,136,229,0.9); }
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# Validation
# -----------------------
required_keys = [
    "available_numbers",
    "available_prizes",
    "original_numbers",
    "original_prizes"
]

for key in required_keys:
    if key not in st.session_state:
        st.error("❌ Session not found. Please start from setup page.")
        st.stop()

# -----------------------
# Init State
# --------------------

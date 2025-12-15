# -----------------------
# Numbers Already Drawn (Styled + Clickable)
# -----------------------
if st.session_state["used_pairs"]:
    st.markdown("---")
    st.subheader("🚫 Numbers Already Drawn")

    # Sort: active first, returned last
    used_sorted = sorted(
        st.session_state["used_pairs"],
        key=lambda x: x["returned"]
    )

    rows = math.ceil(len(used_sorted) / 10)

    for r in range(rows):
        cols = st.columns(10)
        for c, item in enumerate(used_sorted[r*10:(r+1)*10]):
            prize = item["prize"]
            number = item["number"]
            returned = item["returned"]

            color = "#9E9E9E" if returned else "#1E88E5"
            tooltip = "Prize Returned" if returned else None

            with cols[c]:
                # Using form + button to preserve card style
                form_key = f"return_form_{r}_{c}"
                with st.form(form_key):
                    html = render_card(prize, number, color, 20, tooltip=tooltip)
                    st.markdown(html, unsafe_allow_html=True)

                    if not returned:
                        # Invisible submit button
                        if st.form_submit_button("Return"):
                            st.session_state["confirm_return"] = item
                            st.rerun()

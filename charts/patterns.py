import streamlit as st
# import pandas as pd
# import altair as alt

def render_spending_patterns(hourly_df, weekday_df):
    st.markdown("### Spending patterns")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Hour-wise spending")
        if not hourly_df.empty:
            hourly_df = (
            hourly_df
            .set_index("hour")
            .reindex(range(24), fill_value=0)
            .reset_index()
        )
            st.bar_chart(hourly_df.set_index("hour")["amount"])
        else:
            st.info("No hourly data.")

    with c2:
        st.markdown("#### Day-wise spending")
        if not weekday_df.empty:
            st.bar_chart(weekday_df.set_index("day")["amount"])
        else:
            st.info("No weekday data.")
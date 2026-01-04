import streamlit as st

def render_monthly_trends(df):
    st.markdown("### Monthly transaction trends")

    trend_df = df.copy()
    trend_df["month"] = trend_df["datetime"].dt.to_period("M").astype(str)

    trend = (
        trend_df
        .groupby(["month", "type"])["amount"]
        .sum()
        .unstack()
        .fillna(0)
    )

    if not trend.empty:
        st.bar_chart(trend)
    else:
        st.info("No data available for monthly trends.")

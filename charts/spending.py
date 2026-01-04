import streamlit as st

def render_category_spending(df):
    st.markdown("### Spending by category")

    debit_df = df[df["type"] == "DEBIT"]
    if debit_df.empty:
        st.info("No debit transactions found.")
        return

    cat = debit_df.groupby("category")["amount"].sum()
    if not cat.empty:
        st.bar_chart(cat)


def render_daily_spending(df, start_date=None, end_date=None, daily_fn=None):
    st.markdown("### Daily spending")

    if daily_fn is None:
        st.error("Daily spending function not provided.")
        return

    daily = daily_fn(df, start_date=start_date, end_date=end_date)

    if not daily.empty:
        st.line_chart(daily.set_index("date")["amount"])
    else:
        st.info("No daily spending data available.")

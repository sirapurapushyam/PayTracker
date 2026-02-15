import streamlit as st
import warnings
warnings.filterwarnings("ignore")
from pdf_reader.phonepe_pdf import extract_transactions
from charts.trends import render_monthly_trends
from charts.spending import render_category_spending, render_daily_spending
from charts.patterns import render_spending_patterns

from analytics.summary import summary
from analytics.categories import add_category
from analytics.insights import insight
from analytics.daily_money_spent import daily_money_spent
from analytics.patterns import hourly_spending_pattern, weekday_spending_pattern
from analytics.recurring import recurring_payments
from analytics.top_contacts import top_contacts

from utils.filters import apply_filters
from utils.exports import exports

st.set_page_config(page_title="PayTracker", layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    font-weight: 600;
}

.card {
    background-color: #ffffff;
    border: 1px solid #e6e6e6;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 14px;
}

.card-title {
    font-size: 13px;
    color: #6b7280;
    margin-bottom: 6px;
}

.card-value {
    font-size: 20px;
    font-weight: 600;
    color: #111827;
}

.card-sub {
    font-size: 13px;
    color: #374151;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align: center;'>PayTracker</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h6 style='text-align: center;'>Analyze and understand your PhonePe transactions</h6>",
    unsafe_allow_html=True
)
st.caption("")

with st.sidebar:
    st.header("Upload Statement")
    st.caption("Upload your PhonePe transaction PDF")
    st.caption(
    "Supported format: PhonePe transaction statement PDF downloaded from the PhonePe app."
)

    pdf = st.file_uploader("PhonePe PDF", type="pdf")

if not pdf:
    st.info("Upload your PhonePe transaction PDF using the sidebar to get started.")

    st.markdown("""
    ### How it works

#### Step 1: Download your PhonePe transaction statement
1. Open the PhonePe app on your phone  
2. Go to **History**  
3. Tap on **My Statements**  
4. Select the **date range** you want  
5. Tap **Download PDF**  
6. Save the file on your device  

#### Step 2: Upload the statement here
Upload the downloaded PhonePe transaction PDF using the sidebar.

#### Step 3: Apply filters (optional)
Refine transactions by date, amount, type, or contact.

#### Step 4: Review insights
View summaries, key insights, and spending charts.

#### Step 5: Download report
Download the summary and insights for offline reference.

Your data is processed locally and never stored.

    """)
    st.stop()

try:
    df,metadata = extract_transactions(pdf)

    required_cols = {"datetime", "amount", "type", "counterparty"}
    if df is None or df.empty or not required_cols.issubset(df.columns):
        raise ValueError("Invalid PhonePe statement structure")

    df = add_category(df)
    df = df[df["datetime"].notna()]

    if df.empty:
        raise ValueError("No valid transactions found")

except Exception:
    st.error(
        "The uploaded file does not appear to be a valid PhonePe transaction statement.\n\n"
        "Please upload the correct PhonePe PDF downloaded from the PhonePe app."
    )
    st.stop()
phone = metadata.get("phone_number")
statement_start = metadata.get("statement_start")
statement_end = metadata.get("statement_end")

if phone:
    st.markdown(
        f"<p style='text-align:center; color:#6b7280;'>"
        f"Transaction statement for <b>{phone}</b>"
        f"</p>",
        unsafe_allow_html=True
    )

if statement_start and statement_end:
    st.markdown(
        f"<p style='text-align:center; color:#6b7280;'>"
        f"Period: {statement_start.strftime('%d %b %Y')} "
        f"→ {statement_end.strftime('%d %b %Y')}"
        f"</p>",
        unsafe_allow_html=True
    )

st.markdown("<hr>", unsafe_allow_html=True)

with st.sidebar:
    st.header("Filters")
    st.caption("Refine transactions by date, amount, or contact")

    statement_start = metadata.get("statement_start")
    statement_end = metadata.get("statement_end")

    min_date = statement_start or df["datetime"].min().date()
    max_date = statement_end or df["datetime"].max().date()


    start_date = st.date_input("Start date", min_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input("End date", max_date, min_value=min_date, max_value=max_date)

    min_amount = st.number_input("Minimum amount (₹)", 0)
    max_amount = st.number_input("Maximum amount (₹)", 1_000_000)

    txn_type = st.selectbox("Transaction type", ["All", "CREDIT", "DEBIT"])
    txn_type = None if txn_type == "All" else txn_type

    people = ["All"] + sorted(df["counterparty"].unique())
    person = st.selectbox("Contact", people)
    person = None if person == "All" else person

df_f = apply_filters(
    df,
    start_date,
    end_date,
    min_amount,
    max_amount,
    txn_type,
    person
)
statement_start = metadata.get("statement_start")
statement_end = metadata.get("statement_end")
summary_start = statement_start or df_f["datetime"].min().date()
summary_end = statement_end or df_f["datetime"].max().date()

if df_f.empty:
    st.warning("No transactions found for the selected filters.")
    st.stop()

flow = summary(df_f)
st.subheader("Summary")
st.caption(
    f"Based on transactions from {summary_start.strftime('%d %b %Y')} to {summary_end.strftime('%d %b %Y')}"
)


c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Money received</div>
        <div class="card-value">₹{flow['money_in']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Money sent</div>
        <div class="card-value">₹{flow['money_out']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Net change</div>
        <div class="card-value">₹{flow['net_flow']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Total transactions</div>
        <div class="card-value">{flow['transaction_count']}</div>
    </div>
    """, unsafe_allow_html=True)

st.subheader("Key Insights")
st.caption(
    f"Based on transactions from {summary_start.strftime('%d %b %Y')} to {summary_end.strftime('%d %b %Y')}"
)

ins = insight(df_f)

if ins:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Highest total sent</div>
            <div class="card-value">{ins['highest_total_sent']}</div>
            <div class="card-sub">₹{ins['highest_total_sent_amount']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Highest total received</div>
            <div class="card-value">{ins['highest_total_received']}</div>
            <div class="card-sub">₹{ins['highest_total_received_amount']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Most frequent sender</div>
            <div class="card-value">{ins['most_frequent_received_person']}</div>
            <div class="card-sub">{ins['most_frequent_received_count']} transactions</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Most frequent recipient</div>
            <div class="card-value">{ins['most_frequent_sent_person']}</div>
            <div class="card-sub">{ins['most_frequent_sent_count']} transactions</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Largest payment sent</div>
            <div class="card-value">{ins['highest_single_sent_person']}</div>
            <div class="card-sub">₹{ins['highest_single_sent_amount']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <div class="card-title">Largest payment received</div>
            <div class="card-value">{ins['highest_single_received_person']}</div>
            <div class="card-sub">₹{ins['highest_single_received_amount']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Not enough data to generate insights.")

st.subheader("Top Contacts")

c1, c2 = st.columns(2)

with c1:
    st.markdown("#### Money sent to")
    st.dataframe(top_contacts(df_f, "paid"), width="stretch")

with c2:
    st.markdown("#### Money received from")
    st.dataframe(
    top_contacts(df_f, "received"),
    width="stretch"
)

st.subheader("Visual Analysis")
# Monthly Trends Chart
render_monthly_trends(df_f)
# Category Trends Chart
render_category_spending(df_f)

render_daily_spending(
    df_f,
    start_date=statement_start,
    end_date=statement_end,
    daily_fn=daily_money_spent
)

render_spending_patterns(
    hourly_spending_pattern(df_f),
    weekday_spending_pattern(df_f)
)


# # ---------- Charts ----------
# st.subheader("Visual Analysis")

# st.markdown("### Monthly transaction trends")
# trend_df = df_f.copy()
# trend_df["month"] = trend_df["datetime"].dt.to_period("M").astype(str)
# trend = trend_df.groupby(["month", "type"])["amount"].sum().unstack().fillna(0)
# st.bar_chart(trend)

# st.markdown("### Spending by category")
# cat_df = df_f[df_f["type"] == "DEBIT"]
# if not cat_df.empty:
#     st.bar_chart(cat_df.groupby("category")["amount"].sum())

# st.markdown("### Daily spending")
# # daily = daily_money_spent(df_f)
# # if not daily.empty:
# #     st.line_chart(daily.set_index("date")["amount"])
# daily = daily_money_spent(
#     df_f,
#     start_date=statement_start,
#     end_date=statement_end
# )

# if not daily.empty:
#     st.line_chart(daily.set_index("date")["amount"])


# # ---------- Activity Patterns ----------
# st.markdown("### Spending patterns")

# c1, c2 = st.columns(2)

# with c1:
#     st.markdown("#### Hour-wise spending")
#     hourly = hourly_spending_pattern(df_f)
#     if not hourly.empty:
#         st.bar_chart(hourly.set_index("hour")["amount"])

# with c2:
#     st.markdown("#### Day-wise spending")
#     weekday = weekday_spending_pattern(df_f)
#     if not weekday.empty:
#         st.bar_chart(weekday.set_index("day")["amount"])

# ---------- Recurring Payments ----------
# st.subheader("Recurring Payments")
# st.caption("Transactions that appear to repeat regularly")

# rec = recurring_payments(df_f)
# if rec:
#     st.dataframe(
#     rec,
#     width="stretch"
# )

# else:
#     st.info("No recurring payments detected.")

st.subheader("Download Report")
st.caption("Export summary and insights for offline reference")

st.download_button(
    "Download summary (JSON)",
    exports(flow, ins,summary_start=str(summary_start),
        summary_end=str(summary_end)),
    f"paytracker_summary_insights_from{str(summary_start)}to{str(summary_end)}.json"
)

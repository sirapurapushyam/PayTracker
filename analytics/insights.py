def insight(df):
    insights = {}

    sent_df = df[df["type"] == "DEBIT"]
    received_df = df[df["type"] == "CREDIT"]

    if not sent_df.empty:
        sent_group = sent_df.groupby("counterparty")["amount"].agg(["sum", "count"])
        insights["highest_total_sent"] = sent_group["sum"].idxmax()
        insights["highest_total_sent_amount"] = sent_group["sum"].max()

        insights["most_frequent_sent_person"] = sent_group["count"].idxmax()
        insights["most_frequent_sent_count"] = sent_group["count"].max()

        max_sent_row = sent_df.loc[sent_df["amount"].idxmax()]
        insights["highest_single_sent_amount"] = max_sent_row["amount"]
        insights["highest_single_sent_person"] = max_sent_row["counterparty"]

    if not received_df.empty:
        recv_group = received_df.groupby("counterparty")["amount"].agg(["sum", "count"])
        insights["highest_total_received"] = recv_group["sum"].idxmax()
        insights["highest_total_received_amount"] = recv_group["sum"].max()

        insights["most_frequent_received_person"] = recv_group["count"].idxmax()
        insights["most_frequent_received_count"] = recv_group["count"].max()

        max_recv_row = received_df.loc[received_df["amount"].idxmax()]
        insights["highest_single_received_amount"] = max_recv_row["amount"]
        insights["highest_single_received_person"] = max_recv_row["counterparty"]

    return insights

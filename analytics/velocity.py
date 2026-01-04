import pandas as pd
def daily_money_spent(df, start_date=None, end_date=None):
    debit_df = df[df["type"] == "DEBIT"].copy()
    if debit_df.empty:
        return pd.DataFrame(columns=["date", "amount"])

    debit_df["date"] = debit_df["datetime"].dt.date
    daily = debit_df.groupby("date")["amount"].sum()

    # Determine range
    start = start_date or daily.index.min()
    end = end_date or daily.index.max()

    # Create full date range
    full_range = pd.date_range(start=start, end=end, freq="D").date

    # Reindex to include missing days
    daily = daily.reindex(full_range, fill_value=0)

    return daily.reset_index().rename(columns={"index": "date"})

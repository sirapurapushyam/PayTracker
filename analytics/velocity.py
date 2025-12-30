def daily_money_spent(df):
    debit_df = df[df["type"] == "DEBIT"].copy()
    if debit_df.empty:
        return debit_df

    debit_df["date"] = debit_df["datetime"].dt.date
    return debit_df.groupby("date")["amount"].sum().reset_index()

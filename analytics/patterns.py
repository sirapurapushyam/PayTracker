def hourly_spending_pattern(df):
    debit_df = df[df["type"] == "DEBIT"]
    debit_df["hour"] = debit_df["datetime"].dt.hour
    return debit_df.groupby("hour")["amount"].sum().reset_index()


def weekday_spending_pattern(df):
    debit_df = df[df["type"] == "DEBIT"]
    debit_df["day"] = debit_df["datetime"].dt.day_name()
    return debit_df.groupby("day")["amount"].sum().reset_index()

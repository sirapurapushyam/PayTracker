def top_contacts(df, direction):
    return (
        df[df["direction"] == direction]
        .groupby("counterparty")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

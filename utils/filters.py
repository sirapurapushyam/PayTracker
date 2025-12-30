def apply_filters(df, start, end, min_amt, max_amt, txn_type, person):
    temp = df.copy()

    if start and end:
        temp = temp[
            (temp["datetime"].dt.date >= start) &
            (temp["datetime"].dt.date <= end)
        ]

    temp = temp[(temp["amount"] >= min_amt) & (temp["amount"] <= max_amt)]

    if txn_type:
        temp = temp[temp["type"] == txn_type]

    if person:
        temp = temp[temp["counterparty"] == person]

    return temp

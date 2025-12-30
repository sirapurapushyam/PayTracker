def recurring_payments(df):
    recurring = []

    for person in df["counterparty"].unique():
        temp = df[df["counterparty"] == person].sort_values("datetime")
        if len(temp) < 3:
            continue

        avg_gap = temp["datetime"].diff().dt.days.mean()
        if avg_gap and 25 <= avg_gap <= 35:
            recurring.append({
                "person": person,
                "average_amount": round(temp["amount"].mean(), 2),
                "frequency": "Monthly"
            })

    return recurring

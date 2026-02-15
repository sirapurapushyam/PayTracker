# def recurring_payments(df):
#     recurring = []

#     for person in df["counterparty"].unique():
#         temp = df[df["counterparty"] == person].sort_values("datetime")
#         if len(temp) < 3:
#             continue

#         avg_gap = temp["datetime"].diff().dt.days.mean()
#         if avg_gap and 25 <= avg_gap <= 35:
#             recurring.append({
#                 "person": person,
#                 "average_amount": round(temp["amount"].mean(), 2),
#                 "frequency": "Monthly"
#             })

#     return recurring

def recurring_payments(df):
    recurring = []

    for person in df["counterparty"].unique():
        temp = df[df["counterparty"] == person].sort_values("datetime")

        # Only outgoing recurring payments
        temp = temp[temp["direction"] == "paid"]

        if len(temp) < 3:
            continue

        gaps = temp["datetime"].diff().dt.days.dropna()

        # Monthly check
        if not all(25 <= g <= 35 for g in gaps):
            continue

        # Amount consistency
        if temp["amount"].std() > 0.15 * temp["amount"].mean():
            continue

        recurring.append({
            "person": person,
            "average_amount": round(temp["amount"].mean(), 2),
            "frequency": "Monthly",
            "transactions": len(temp)
        })

    return recurring


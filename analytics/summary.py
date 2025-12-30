def cash_flow(df):
    credit = df[df["type"] == "CREDIT"]["amount"].sum()
    debit = df[df["type"] == "DEBIT"]["amount"].sum()

    return {
        "money_in": credit,
        "money_out": debit,
        "net_flow": credit - debit,
        "transaction_count": len(df)
    }

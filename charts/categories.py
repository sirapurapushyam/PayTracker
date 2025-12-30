import matplotlib.pyplot as plt
import io, base64

def category_chart(df):
    debit = df[df["type"] == "DEBIT"]
    if debit.empty:
        return None

    data = debit.groupby("category")["amount"].sum()

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(data, labels=data.index, autopct="%1.1f%%")
    ax.set_title("Spending by Category")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return base64.b64encode(buf.getvalue()).decode()

import matplotlib.pyplot as plt
import io, base64

def top_contacts_chart(df):
    data = df.groupby("counterparty")["amount"].sum().sort_values(ascending=False).head(10)

    if data.empty:
        return None

    fig, ax = plt.subplots(figsize=(8, 5))
    data.plot(kind="barh", ax=ax)
    ax.set_title("Top Contacts by Amount")
    ax.set_xlabel("Amount (₹)")

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close()
    return base64.b64encode(buf.getvalue()).decode()

import matplotlib.pyplot as plt
import io, base64

def monthly_trend(df):
    if df.empty:
        return None

    df = df.copy()
    df["month"] = df["datetime"].dt.to_period("M").astype(str)
    data = df.groupby(["month", "type"])["amount"].sum().unstack().fillna(0)

    fig, ax = plt.subplots(figsize=(10, 4))
    data.plot(kind="bar", ax=ax)
    ax.set_title("Monthly Transaction Trend")
    ax.set_ylabel("Amount (₹)")
    ax.set_xlabel("Month")

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close()
    return base64.b64encode(buf.getvalue()).decode()

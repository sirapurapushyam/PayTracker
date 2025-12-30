import matplotlib.pyplot as plt
import io, base64

def hourly_chart(pattern_df):
    if pattern_df is None or pattern_df.empty:
        return None

    fig, ax = plt.subplots()
    ax.bar(pattern_df["hour"], pattern_df["amount"])
    ax.set_title("Hourly Spending Pattern")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Amount (₹)")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return base64.b64encode(buf.getvalue()).decode()


def weekday_chart(pattern_df):
    if pattern_df is None or pattern_df.empty:
        return None

    fig, ax = plt.subplots()
    ax.bar(pattern_df["day"], pattern_df["amount"])
    ax.set_title("Weekday Spending Pattern")
    ax.set_ylabel("Amount (₹)")
    ax.tick_params(axis='x', rotation=45)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close()
    return base64.b64encode(buf.getvalue()).decode()

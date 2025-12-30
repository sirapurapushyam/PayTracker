import seaborn as sns
import matplotlib.pyplot as plt
import io, base64

def activity_heatmap(df):
    df["hour"] = df["datetime"].dt.hour
    df["day"] = df["datetime"].dt.dayofweek
    pivot = df.pivot_table(values="amount", index="day", columns="hour", aggfunc="sum").fillna(0)

    fig, ax = plt.subplots(figsize=(12,4))
    sns.heatmap(pivot, ax=ax)
    ax.set_title("Activity Heatmap")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    return base64.b64encode(buf.getvalue()).decode()

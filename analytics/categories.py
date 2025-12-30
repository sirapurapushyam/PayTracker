def add_category(df):
    rules = {
        "Food": ["zomato", "swiggy", "restaurant"],
        "Shopping": ["amazon", "flipkart"],
        "Bills": ["recharge", "electricity", "bill"],
        "Transport": ["uber", "ola"],
    }

    def detect(name):
        if not isinstance(name, str):
            return "Personal"
        name = name.lower()
        for cat, keys in rules.items():
            if any(k in name for k in keys):
                return cat
        return "Personal"

    df["category"] = df["counterparty"].apply(detect)
    return df

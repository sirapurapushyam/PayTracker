def add_category(df):
    rules = {
    "Travel": ["irctc", "rail", "bus", "flight","uber", "ola","UTS","ticket"],
    "Food": ["zomato", "swiggy", "restaurant","Tiffin","canteen"],
    "Shopping": ["amazon", "flipkart"], 
    "Bills": ["recharge", "electricity", "bill"],
    "Medical":["Medicals","medical","hospital"]
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

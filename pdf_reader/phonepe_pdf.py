import pandas as pd
import PyPDF2
import re

def extract_statement_metadata(reader):
    first_page_text = reader.pages[0].extract_text()
    if not first_page_text:
        return {}

    phone_re = r"Transaction Statement for\s+(\d+)"
    phone_match = re.search(phone_re, first_page_text)

    range_re = r"([0-9]{2} [A-Z][a-z]{2}, [0-9]{4})\s*-\s*([0-9]{2} [A-Z][a-z]{2}, [0-9]{4})"
    range_match = re.search(range_re, first_page_text)

    metadata = {}

    if phone_match:
        metadata["phone_number"] = phone_match.group(1)

    if range_match:
        metadata["statement_start"] = pd.to_datetime(
            range_match.group(1), format="%d %b, %Y"
        ).date()
        metadata["statement_end"] = pd.to_datetime(
            range_match.group(2), format="%d %b, %Y"
        ).date()

    return metadata


def extract_transactions(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    metadata = extract_statement_metadata(reader)
    rows = []

    date_re = r'([A-Z][a-z]{2} \d{2}, \d{4})'
    time_re = r'(\d{2}:\d{2} [ap]m)'
    amt_re = r'₹([\d,]+(?:\.\d{2})?)'

    for page in reader.pages:
        # print(page)
        text = page.extract_text()
        print(text)
        if not text:
            continue

        lines = text.split("\n")
        i = 0

        while i < len(lines):
            date_match = re.search(date_re, lines[i])
            if not date_match:
                i += 1
                continue

            try:
                date = date_match.group(1)
                time = re.search(time_re, lines[i+1]).group(1)
                txn_type = "CREDIT" if "CREDIT" in lines[i+2] else "DEBIT"

                amt_match = re.search(amt_re, lines[i+3])
                amount = float(amt_match.group(1).replace(",", "")) if amt_match else 0

                # ---- Counterparty Extraction ----
                party_line = lines[i+4].strip()

                counterparty = "Unknown"
                direction = "unknown"

                if party_line in ["Paid to", "Payment to", "Transfer to"]:
                    name_parts = []
                    j = i + 5
                    while j < len(lines) and "Transaction ID" not in lines[j] and "UTR No" not in lines[j]:
                        name_parts.append(lines[j].strip())
                        j += 1

                    counterparty = " ".join(name_parts)
                    direction = "paid"
                elif party_line in ["Received from", "Refund from"]:
                    name_parts = []
                    j = i + 5

                    while j < len(lines) and "Transaction ID" not in lines[j] and "UTR No" not in lines[j]:
                        name_parts.append(lines[j].strip())
                        j += 1

                    counterparty = " ".join(name_parts)
                    direction = "received"

                elif party_line.startswith(("Paid to", "Payment to", "Transfer to")):
                    counterparty = party_line.split("to", 1)[1].strip()
                    direction = "paid"

                elif party_line.startswith(("Received from", "Refund from")):
                    counterparty = party_line.split("from", 1)[1].strip()
                    direction = "received"

                rows.append({
                    "date": date,
                    "time": time,
                    "type": txn_type,
                    "amount": amount,
                    "counterparty": counterparty,
                    "direction": direction
                })
                j = i + 1
                while j < len(lines) and not re.search(date_re, lines[j]):
                    j += 1
                i = j

            except Exception:
                i += 1


    df = pd.DataFrame(rows)
    df.to_csv("my_file.csv", index=False)
    print(df)
    df["datetime"] = pd.to_datetime(
        df["date"] + " " + df["time"],
        format="%b %d, %Y %I:%M %p",
        errors="coerce"
    )
    df.to_csv("date.csv", index=False)
    return df,metadata

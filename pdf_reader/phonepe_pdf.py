import pandas as pd
import PyPDF2
import re

def extract_statement_metadata(reader):
    """
    Extract phone number and statement date range from page 1
    """
    first_page_text = reader.pages[0].extract_text()
    if not first_page_text:
        return {}

    # Phone number
    phone_re = r"Transaction Statement for\s+(\d+)"
    phone_match = re.search(phone_re, first_page_text)

    # Date range
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
        text = page.extract_text()
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

                party_line = lines[i+4]
                if "Paid to" in party_line:
                    counterparty = party_line.replace("Paid to", "").strip()
                    direction = "paid"
                elif "Received from" in party_line:
                    counterparty = party_line.replace("Received from", "").strip()
                    direction = "received"
                else:
                    counterparty = "Unknown"
                    direction = "unknown"

                rows.append({
                    "date": date,
                    "time": time,
                    "type": txn_type,
                    "amount": amount,
                    "counterparty": counterparty,
                    "direction": direction
                })

                i += 6
            except Exception:
                i += 1

    df = pd.DataFrame(rows)
    df["datetime"] = pd.to_datetime(
        df["date"] + " " + df["time"],
        format="%b %d, %Y %I:%M %p",
        errors="coerce"
    )
    return df,metadata

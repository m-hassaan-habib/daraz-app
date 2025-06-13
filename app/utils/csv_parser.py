import csv
from collections import defaultdict

def parse_csv(filepath):
    orders = defaultdict(list)

    with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        # Normalize fieldnames to strip whitespace and case
        reader.fieldnames = [h.strip() for h in reader.fieldnames]

        for row in reader:
            # Normalize each key in row
            row = {k.strip(): v.strip() for k, v in row.items()}

            order_number = row.get("Order Number")
            if not order_number:
                continue

            try:
                row["Amount(Include Tax)"] = float(row.get("Amount(Include Tax)", 0)) or 0.0
            except ValueError:
                row["Amount(Include Tax)"] = 0.0

            orders[order_number].append(row)

    return orders

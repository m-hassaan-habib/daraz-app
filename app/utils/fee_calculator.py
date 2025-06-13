def calculate_handling_fee(product_price):
    if product_price <= 500:
        return 10
    elif product_price <= 1000:
        return 15
    elif product_price <= 2000:
        return 20
    else:
        return 60

def calculate_order_summary(order_rows):
    revenue = 0
    negative_fees = 0
    product_price = 0

    for row in order_rows:
        amount = row["amount"]
        fee_name = row["fee_name"].lower()

        if "product price" in fee_name:
            product_price += amount
            revenue += amount
        elif "shipping fee paid" in fee_name:
            revenue += amount
        else:
            negative_fees += -amount if amount < 0 else amount  # only deduct true charges

    handling_fee = calculate_handling_fee(product_price)
    packing_fee = 10
    logistics_fee = 5
    total_deductions = negative_fees + handling_fee + packing_fee + logistics_fee
    profit = revenue - total_deductions

    return {
        "revenue": revenue,
        "deductions": negative_fees,
        "handling_fee": handling_fee,
        "packing_fee": packing_fee,
        "logistics_fee": logistics_fee,
        "final_profit": profit,
        "product_price": product_price
    }

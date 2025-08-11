def calculate_handling_fee(product_price):
    if product_price <= 500:
        return 10
    elif product_price <= 1000:
        return 15
    elif product_price <= 2000:
        return 20
    else:
        return 60

def calculate_order_summary(order_rows, cost_price=0):
    product_price = 0.0
    shipping_paid = 0.0
    negative_fees = 0.0

    for row in order_rows:
        amount = float(row["amount"])
        fee_name = (row.get("fee_name") or "").lower().strip()

        if "product price paid by buyer" in fee_name:
            product_price += amount
        elif "shipping fee paid by buyer" in fee_name:
            shipping_paid += amount
        elif any(x in fee_name for x in ["payment fee", "commission fee", "shipping fee"]) and amount < 0:
            negative_fees += abs(amount)

    revenue = product_price + shipping_paid
    handling_fee = calculate_handling_fee(product_price)
    packing_fee = 10.0
    logistics_fee = 5.0

    total_costs = handling_fee + packing_fee + logistics_fee  # NEW
    gross_profit = revenue - negative_fees - total_costs
    final_profit = gross_profit - float(cost_price or 0)

    return {
        "product_price": product_price,
        "shipping_paid": shipping_paid,
        "revenue": revenue,
        "deductions": negative_fees,
        "handling_fee": handling_fee,
        "packing_fee": packing_fee,
        "logistics_fee": logistics_fee,
        "total_costs": total_costs,
        "cost_price": float(cost_price or 0),
        "gross_profit": gross_profit,
        "final_profit": final_profit
    }

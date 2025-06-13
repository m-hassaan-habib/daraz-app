# This will now be a simple data structure or class, not tied to SQLAlchemy
class Order:
    def __init__(self, order_number, product_name, sku, revenue, fees, costs, profit, margin, breakdown):
        self.order_number = order_number
        self.product_name = product_name
        self.sku = sku
        self.revenue = revenue
        self.fees = fees
        self.costs = costs
        self.profit = profit
        self.margin = margin
        self.breakdown = breakdown
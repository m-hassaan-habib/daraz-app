document.addEventListener("DOMContentLoaded", function () {
  const data = window.dashboardData;
  if (!data) return;

  // Revenue vs Deductions Pie
  new Chart(document.getElementById("revenuePie"), {
    type: "pie",
    data: {
      labels: ["Revenue", "Deductions"],
      datasets: [{
        data: [data.revenue, data.deductions],
        backgroundColor: ["#4CAF50", "#F44336"]
      }]
    }
  });

  // Fee Breakdown Bar
  new Chart(document.getElementById("feeBar"), {
    type: "bar",
    data: {
      labels: ["Handling", "Packing", "Logistics"],
      datasets: [{
        label: "Fees (Rs)",
        data: [data.handling_fee, data.packing_fee, data.logistics_fee],
        backgroundColor: "#2196F3"
      }]
    }
  });

  // Profit vs Cost Pie
  const totalCost = data.deductions + data.handling_fee + data.packing_fee + data.logistics_fee;
  new Chart(document.getElementById("profitPie"), {
    type: "pie",
    data: {
      labels: ["Profit", "Costs"],
      datasets: [{
        data: [data.final_profit, totalCost],
        backgroundColor: ["#66BB6A", "#FF9800"]
      }]
    }
  });

  // Revenue Component Bar (Product vs Shipping Paid)
  const productRevenue = data.product_price;
  const shippingPaid = data.revenue - productRevenue;
  new Chart(document.getElementById("revenueBar"), {
    type: "bar",
    data: {
      labels: ["Product Revenue", "Shipping Paid by Buyer"],
      datasets: [{
        label: "Revenue Split (Rs)",
        data: [productRevenue, shippingPaid],
        backgroundColor: ["#673AB7", "#00BCD4"]
      }]
    }
  });
});

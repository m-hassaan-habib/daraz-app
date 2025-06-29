document.addEventListener("DOMContentLoaded", function () {
  const data = window.dashboardData;
  if (!data) return;

const totalRevenue = data.revenue || 0;
const totalDeductions = data.deductions || 0;

// Fake 6 months split (flat or random variation)
const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"];
const revenueData = months.map(() => +(totalRevenue / 6).toFixed(1));
const deductionData = months.map(() => +(totalDeductions / 6).toFixed(1));

// Optional: add small variation for visual appeal
for (let i = 0; i < months.length; i++) {
  revenueData[i] += (Math.random() * 20 - 10); // ±10 variation
  deductionData[i] += (Math.random() * 10 - 5);
}

// Line chart
new Chart(document.getElementById("revenuePie"), {
  type: "line",
  data: {
    labels: months,
    datasets: [
      {
        label: "Revenue",
        data: revenueData,
        borderColor: "#3B82F6",
        backgroundColor: "rgba(59, 130, 246, 0.1)",
        fill: false,
        tension: 0.4
      },
      {
        label: "Deductions",
        data: deductionData,
        borderColor: "#EF4444",
        backgroundColor: "rgba(239, 68, 68, 0.1)",
        fill: false,
        tension: 0.4
      }
    ]
  },
  options: {
    plugins: {
      legend: {
        position: "top",
        labels: { color: "#334155" }
      }
    },
    scales: {
      y: { ticks: { color: "#64748B" } },
      x: { ticks: { color: "#64748B" } }
    }
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
        backgroundColor: ["#A78BFA", "#60A5FA", "#FBBF24"]
      }]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        y: { ticks: { color: "#64748B" } },
        x: { ticks: { color: "#64748B" } }
      }
    }
  });

  // Profit vs Costs Pie
  const totalCost = data.deductions + data.handling_fee + data.packing_fee + data.logistics_fee;
  new Chart(document.getElementById("profitPie"), {
    type: "pie",
    data: {
      labels: ["Profit", "Costs"],
      datasets: [{
        data: [data.final_profit, totalCost],
        backgroundColor: ["#34D399", "#F97316"]
      }]
    },
    options: {
      plugins: { legend: { position: "bottom", labels: { color: "#334155" } } }
    }
  });

  // Revenue Component Bar
  const productRevenue = data.product_price || 0;
  const shippingPaid = data.revenue - productRevenue;
  new Chart(document.getElementById("revenueBar"), {
    type: "bar",
    data: {
      labels: ["Product Revenue", "Shipping Paid by Buyer"],
      datasets: [{
        label: "Revenue Split (Rs)",
        data: [productRevenue, shippingPaid],
        backgroundColor: ["#6366F1", "#06B6D4"]
      }]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        y: { ticks: { color: "#64748B" } },
        x: { ticks: { color: "#64748B" } }
      }
    }
  });
});

// /app/static/js/charts.js
function createBillingChart(billingData) {
    const ctx = document.getElementById('billingChart').getContext('2d');
    
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    const labels = billingData.map(item => {
        const [year, month, day] = item.TimePeriod.Start.split('-').map(Number);
        return `${monthNames[month - 1]} ${year}`;
    });
    
    const datasets = {};

    billingData.forEach((item, index) => {
        item.Groups.forEach(group => {
            const service = group.Keys[0];
            const cost = parseFloat(group.Metrics.BlendedCost.Amount);

            if (!datasets[service]) {
                datasets[service] = {
                    label: service,
                    data: new Array(labels.length).fill(0),
                    backgroundColor: getRandomColor(),
                };
            }

            datasets[service].data[index] = cost;
        });
    });

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: Object.values(datasets),
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    ticks: {
                        callback: function(value, index, values) {
                            return '$' + value.toFixed(2);
                        }
                    }
                },
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function(tooltipItems) {
                            const item = billingData[tooltipItems[0].dataIndex];
                            const [startYear, startMonth, startDay] = item.TimePeriod.Start.split('-').map(Number);
                            const [endYear, endMonth, endDay] = item.TimePeriod.End.split('-').map(Number);
                            return `${startYear}-${startMonth.toString().padStart(2, '0')}-${startDay.toString().padStart(2, '0')} to ${endYear}-${endMonth.toString().padStart(2, '0')}-${endDay.toString().padStart(2, '0')}`;
                        },
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed.y);
                            }
                            return label;
                        },
                        footer: (tooltipItems) => {
                            const total = tooltipItems.reduce((sum, ti) => sum + ti.parsed.y, 0);
                            return 'Total: ' + new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(total);
                        }
                    }
                }
            }
        },
    });
}

function getRandomColor() {
    return `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.5)`;
}

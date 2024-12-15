document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('monthlyChart').getContext('2d');
    const { months, monthlyData, monthIds } = window.chartData;
    
    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: months,
            datasets: [{
                label: 'Records Added',
                data: monthlyData,
                backgroundColor: '#1db954',
                borderColor: '#1db954',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.raw;
                            return `${value} record${value !== 1 ? 's' : ''}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#b3b3b3'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: '#b3b3b3'
                    },
                    grid: {
                        display: false
                    }
                }
            },
            onClick: (event, elements) => {
                if (elements.length > 0) {
                    const index = elements[0].index;
                    const month = months[index];
                    const monthId = monthIds[month];
                    console.log('Clicking month:', month, 'Link:', monthId);
                    const monthElement = document.querySelector(`#${monthId}`);
                    if (monthElement) {
                        monthElement.scrollIntoView({ 
                            behavior: 'smooth',
                            block: 'start'
                        });
                    } else {
                        console.error('Month element not found:', monthId);
                    }
                }
            }
        }
    });

    // Add pointer cursor to bars
    ctx.canvas.style.cursor = 'pointer';
});

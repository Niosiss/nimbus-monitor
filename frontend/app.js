const cpuChartCtx = document.getElementById('cpuChart').getContext('2d');
const memoryChartCtx = document.getElementById('memoryChart').getContext('2d');
const diskChartCtx = document.getElementById('diskChart').getContext('2d');
const logoutBtn = document.getElementById('logoutBtn');

const cpuChart = new Chart(cpuChartCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'CPU Usage',
            data: [],
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)'
        }]
    },
    options: { scales: { y: { beginAtZero: true } } }
});

const memoryChart = new Chart(memoryChartCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Memory Usage',
            data: [],
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)'
        }]
    },
    options: { scales: { y: { beginAtZero: true } } }
});

const diskChart = new Chart(diskChartCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Disk Usage',
            data: [],
            borderColor: 'rgb(54, 162, 235)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)'
        }]
    },
    options: { scales: { y: { beginAtZero: true } } }
});

function updateChart(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets[0].data.push(data);
    if (chart.data.labels.length > 20) { 
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }
    chart.update();
}

logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('token')
    window.location.href = "login.html"
});

const token = localStorage.getItem('token')
if (!token) {
    window.location.href = "login.html"
}

fetch('https://orange-sniffle-pjr75wq5pqg437q94-8000.app.github.dev/api/history', {
    headers: {
    'Authorization': 'Bearer ' + token
}
})
    .then(response => {
        if (response.status === 401 || response.status === 403) {
            localStorage.removeItem('token');
            window.location.href = "login.html";
            return;
        }
        return response.json();
    })
    .then(data => {
        data.forEach(entry => {
            updateChart(cpuChart, entry.timestamp, entry.cpu_usage);
            updateChart(memoryChart, entry.timestamp, entry.memory_usage);
            updateChart(diskChart, entry.timestamp, entry.disk_usage);
        });

        

        const ws = new WebSocket("wss://orange-sniffle-pjr75wq5pqg437q94-8000.app.github.dev/ws");

        ws.onopen = () => {
            console.log("WebSocket connected!");
        };

        ws.onmessage = (event) => {
            const liveData = JSON.parse(event.data);
            
            updateChart(cpuChart, liveData.timestamp, liveData.cpu_usage);
            updateChart(memoryChart, liveData.timestamp, liveData.memory_usage);
            updateChart(diskChart, liveData.timestamp, liveData.disk_usage);
        };

        ws.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        ws.onclose = () => {
            console.log("WebSocket disconnected");
        };
    })
    .catch(error => console.error('Error fetching history:', error));
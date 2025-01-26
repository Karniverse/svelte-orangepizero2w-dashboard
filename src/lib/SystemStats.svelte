<script>
    let stats = {
        cpu: { usage: 0 },
        ram: { percent: 0 },
        disk: { percent: 0 },
    };

    async function fetchStats() {
        const response = await fetch("http://localhost:7000/api/stats");
        stats = await response.json();
    }
    // Fetch stats every 1 seconds
    setInterval(fetchStats, 1000);
    fetchStats();
</script>

<main>
    <h1>System Stats</h1>
    <p>CPU Usage: {stats.cpu.usage}%</p>
    <p>Memory Usage: {stats.ram.percent}%</p>
    <p>Disk Usage: {stats.disk.percent}%</p>
</main>

<style>
    .stats-container {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    /*.stat {
        background: #f4f4f4;
        padding: 10px;
        border-radius: 5px;
        flex: 1;
    }*/
</style>

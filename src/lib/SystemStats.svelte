<script>
    let stats = {
        cpu: 0,
        memory: 0,
        disk: 0,
    };

    // Fetch system stats from the backend
    async function fetchStats() {
        const response = await fetch("http://localhost:3000/api/stats");
        stats = await response.json();
        stats = {
            cpu: data.cpu.usage,
            memory: data.ram.percent_used,
            disk: data.disk[0].percent_used, // Use the first disk's usage
        };
    }

    // Fetch stats every 2 seconds
    setInterval(fetchStats, 2000);
    fetchStats();
</script>

<div class="stats-container">
    <div class="stat">
        <h3>CPU Usage</h3>
        <p>{stats.cpu}%</p>
    </div>
    <div class="stat">
        <h3>Memory Usage</h3>
        <p>{stats.memory}%</p>
    </div>
    <div class="stat">
        <h3>Disk Usage</h3>
        <p>{stats.disk}%</p>
    </div>
</div>

<style>
    .stats-container {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    .stat {
        background: #f4f4f4;
        padding: 10px;
        border-radius: 5px;
        flex: 1;
    }
</style>

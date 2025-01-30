<script>
    import { stats, error } from "./apidata.js";
    import { onMount } from "svelte";
    import LineChart from "../components/LineChart.svelte";
    import PieChart from "../components/PieChart.svelte";

    let cpuData = {
        labels: [],
        datasets: [
            {
                label: "CPU Usage (%)",
                data: [],
                borderColor: "rgba(75, 192, 192, 1)",
                fill: false,
                tension: 0.5,
            },
        ],
    };
    let memoryData = {
        labels: [],
        datasets: [
            {
                label: "Memory Usage (%)",
                data: [],
                borderColor: "rgba(153, 102, 255, 1)",
                fill: false,
                tension: 0.5,
            },
        ],
    };
    let networkData = {
        labels: [],
        datasets: [
            {
                label: "Upload Speed (KB/s)",
                data: [],
                borderColor: "rgba(255, 99, 130, 1)",
                backgroundColor: "rgba(255, 99, 130, 0.2)",
                fill: false,
                tension: 0.5,
            },
            {
                label: "Download Speed (KB/s)",
                data: [],
                borderColor: "rgba(54, 162, 235, 1)",
                backgroundColor: "rgba(54, 162, 235, 0.2)",
                fill: false,
                tension: 0.5,
            },
        ],
    };
    let diskData = {
        labels: ["Used (%)", "Free (%)"],
        datasets: [
            {
                data: [],
                backgroundColor: [
                    "rgba(255, 159, 64, 1)",
                    "rgba(75, 192, 192, 1)",
                ],
            },
        ],
    };

    onMount(() => {
        const interval = setInterval(fetchStats, 1000);
        return () => clearInterval(interval);
    });

    function fetchStats() {
        // Only attempt to fetch data if stats is populated
        if ($stats && $stats.cpu && $stats.ram) {
            // Update CPU data
            cpuData.labels.push(new Date().toLocaleTimeString());
            cpuData.datasets[0].data.push($stats.cpu.usage);
            if (cpuData.labels.length > 10) {
                cpuData.labels.shift();
                cpuData.datasets[0].data.shift();
            }

            // Update Memory data
            memoryData.labels.push(new Date().toLocaleTimeString());
            memoryData.datasets[0].data.push($stats.ram.percent);
            if (memoryData.labels.length > 10) {
                memoryData.labels.shift();
                memoryData.datasets[0].data.shift();
            }

            // Update Network data
            networkData.labels.push(new Date().toLocaleTimeString());
            networkData.datasets[0].data.push(
                ($stats.network.upload_speed / 1024).toFixed(2),
            );
            networkData.datasets[1].data.push(
                ($stats.network.download_speed / 1024).toFixed(2),
            );
            if (networkData.labels.length > 10) {
                networkData.labels.shift();
                networkData.datasets[0].data.shift();
                networkData.datasets[1].data.shift();
            }

            // Update Disk data for Pie chart
            const usedDisk = (
                ($stats.disk.used / $stats.disk.total) *
                100
            ).toFixed(1);
            const freeDisk = (
                ($stats.disk.free / $stats.disk.total) *
                100
            ).toFixed(1);
            diskData.datasets[0].data = [usedDisk, freeDisk];
        }
        cpuData = { ...cpuData };
        memoryData = { ...memoryData };
        networkData = { ...networkData };
        diskData = { ...diskData };
    }
</script>

<div class="dashboard">
    <h1>System Performance Dashboard</h1>

    {#if $error}
        <p style="color: red;">Error: {$error}</p>
    {:else if !$stats || !$stats.cpu || !$stats.ram}
        <p>Loading stats...</p>
        <!-- Show a loading message if stats are not available -->
    {:else}
        <div class="chart-container">
            <h2>CPU Usage</h2>
            <LineChart
                id="cpuChart"
                data={cpuData}
                options={{ responsive: true }}
            />
        </div>

        <div class="chart-container">
            <h2>Memory Usage</h2>
            <LineChart
                id="memoryChart"
                data={memoryData}
                options={{ responsive: true }}
            />
        </div>

        <div class="chart-container">
            <h2>Network Usage</h2>
            <LineChart
                id="networkChart"
                data={networkData}
                options={{ responsive: true }}
            />
        </div>

        <div class="chart-container">
            <h2>Disk Usage</h2>
            <PieChart
                id="diskChart"
                data={diskData}
                options={{ responsive: true }}
            />
        </div>
    {/if}
</div>

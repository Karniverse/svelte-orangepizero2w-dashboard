<script>
    import { stats, error } from "../lib/apidata.js";
    import { onMount } from "svelte";
    import LineChart from "../lib/charts/LineChart.svelte";

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
        }
        cpuData = { ...cpuData };
        memoryData = { ...memoryData };
        networkData = { ...networkData };
    }
</script>

<div class="component">
    {#if $error}
        <p style="color: red;">Error: {$error}</p>
    {:else if !$stats || !$stats.cpu || !$stats.ram}
        <p>Loading stats...</p>
        <!-- Show a loading message if stats are not available -->
    {:else}
        <div class="charts-wrapper">
            <div class="top-charts">
                <div class="chart-container">
                    <div class="container-title">CPU Usage</div>
                    <!-- <h2>CPU Usage</h2> -->
                    <LineChart
                        id="cpuChart"
                        data={cpuData}
                        options={{ responsive: true }}
                    />
                </div>
                <div class="chart-container">
                    <div class="container-title">Memory Usage</div>
                    <!-- <h2>Memory Usage</h2> -->
                    <LineChart
                        id="memoryChart"
                        data={memoryData}
                        options={{ responsive: true }}
                    />
                </div>
            </div>

            <div class="chart-container">
                <div class="container-title">Network Usage</div>
                <!-- <h2>Network Usage</h2> -->
                <LineChart
                    id="networkChart"
                    data={networkData}
                    options={{ responsive: true }}
                />
            </div>
        </div>
    {/if}
</div>

<style>
    .charts-wrapper {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .top-charts {
        display: flex;
        gap: 20px;
        justify-content: space-between; /* Space evenly */
        /*height: 600px;*/
    }

    .chart-container {
        flex: 1; /* Makes them equal width */
        padding: 20px;
        background: #f9f9f9;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }

    /* Give a smaller height to the Network chart */
    .chart-container:last-child {
        /*height: 200px; /* Adjust height as needed */
    }

    /* Make charts stack on smaller screens */
    @media (max-width: 768px) {
        .top-charts {
            flex-direction: column;
        }
    }
</style>

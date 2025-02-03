<script>
    import { stats, error } from "../lib/apidata.js";
    import { onMount } from "svelte";
    import PieChart from "../lib/charts/PieChart.svelte";
    import BarChart from "../lib/charts/BarChart.svelte";
    import RecentFiles from "./RecentFiles.svelte";

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

    let diskIOBytes = {
        labels: ["Read (KB)", "Write (KB)"],
        datasets: [
            {
                label: "Disk I/O Bytes",
                data: [0, 0],
                backgroundColor: [
                    "rgba(54, 162, 235, 1)", // Blue for read
                    "rgba(255, 99, 132, 1)", // Red for write
                ],
                borderWidth: 0,
            },
        ],
    };

    let diskIOCount = {
        labels: ["Read", "Write"],
        datasets: [
            {
                label: "Disk I/O Count",
                data: [0, 0],
                backgroundColor: [
                    "rgba(54, 162, 235, 1)", // Blue for read
                    "rgba(255, 99, 132, 1)", // Red for write
                ],
                borderWidth: 0,
            },
        ],
    };

    let yAxisMaxBytes,
        yAxisMaxCount = 6000; // Default max value for the Y-axis

    onMount(() => {
        const interval = setInterval(fetchStats, 1000);
        return () => clearInterval(interval);
    });

    function fetchStats() {
        if ($stats && $stats.cpu && $stats.ram) {
            // Update Pie Chart Data
            const usedDisk = (
                ($stats.disk.used / $stats.disk.total) *
                100
            ).toFixed(1);
            const freeDisk = (
                ($stats.disk.free / $stats.disk.total) *
                100
            ).toFixed(1);
            diskData.datasets[0].data = [usedDisk, freeDisk];

            // Update Bar Chart Data
            const readBytes = $stats.disk.diskrbytes / Math.pow(1024, 1);
            const writeBytes = $stats.disk.diskwbytes / Math.pow(1024, 1);
            const readcount = $stats.disk.diskrbytes / Math.pow(1024, 1);
            const writecount = $stats.disk.diskwbytes / Math.pow(1024, 1);

            // Dynamically adjust the Y-axis max value based on the data
            yAxisMaxBytes = Math.max(readBytes, writeBytes) * 1.2; // Set max to 120% of the highest value
            yAxisMaxCount = Math.max(readcount, writecount) * 1.2; // Set max to 120% of the highest value

            diskIOBytes.datasets[0].data = [readBytes, writeBytes];
            diskIOCount.datasets[0].data = [readcount, writecount];

            // Trigger Svelte reactivity
            diskData = { ...diskData };
            diskIOBytes = { ...diskIOBytes };
            //yAxisMax = { ...yAxisMax };
            //console.log("Stats data:", $stats.disk.diskrbytes);
        }
    }
</script>

<div class="component">
    {#if $error}
        <p style="color: red;">Error: {$error}</p>
    {:else if !$stats || !$stats.cpu || !$stats.ram}
        <p>Loading stats...</p>
    {:else}
        <div class="charts-wrapper">
            <div class="top-charts">
                <div class="chart-container">
                    <div class="container-title">Disk Usage</div>
                    <!--h2>Disk Usage</h2-->
                    <PieChart
                        id="diskChart"
                        data={diskData}
                        options={{ responsive: true }}
                    />
                </div>

                <div class="chart-container">
                    <div class="container-title">Disk Read/Write</div>
                    <!--h2>Disk Read/Write</h2-->
                    <BarChart
                        id="diskIOChart"
                        data={diskIOBytes}
                        options={{
                            responsive: true,
                            scales: {
                                y: { beginAtZero: true, max: yAxisMaxBytes },
                            },
                        }}
                    />
                    <!-- <div class="container-title">Disk Read/Write Count</div> -->
                    <BarChart
                        id="diskIOCount"
                        data={diskIOCount}
                        options={{
                            responsive: true,
                            scales: {
                                y: { beginAtZero: true, max: yAxisMaxCount },
                            },
                        }}
                    />
                </div>
            </div>
            <RecentFiles class="chart-container" />
        </div>
    {/if}
</div>

<style>
    .charts-wrapper {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
    .charts-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        flex-wrap: wrap;
    }

    .top-charts {
        display: flex;
        gap: 8px;
        justify-content: space-between; /* Space evenly */
        /*height: 600px;*/
    }

    .chart-container {
        background: #fff;
        padding: 5px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        flex: 1;
        min-width: 280px; /* Ensure responsiveness */
        max-width: 48%; /* Adjust max-width for two charts side-by-side */
    }

    h2 {
        text-align: center;
    }
</style>

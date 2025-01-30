<script>
    import { stats, error } from "../lib/apidata.js";
    import { onMount } from "svelte";
    import PieChart from "../lib/charts/PieChart.svelte";

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
        diskData = { ...diskData };
    }
</script>

<div class="component">
    {#if $error}
        <p style="color: red;">Error: {$error}</p>
    {:else if !$stats || !$stats.cpu || !$stats.ram}
        <p>Loading stats...</p>
        <!-- Show a loading message if stats are not available -->
    {:else}
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

<style>
    .chart-container {
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
</style>

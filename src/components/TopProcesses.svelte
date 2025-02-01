<script>
    import { stats, error } from "../lib/apidata.js"; // Ensure stats and error are stores
    import { onMount } from "svelte";

    import { get } from "svelte/store";

    let topProcesses = [];

    function fetchStats() {
        const data = get(stats); // Get the latest value of the store
        if (data && data.top_processes) {
            topProcesses = [...data.top_processes]; // Spread to trigger reactivity
        }
    }

    onMount(() => {
        fetchStats(); // Fetch once on mount
        const interval = setInterval(fetchStats, 1000); // Refresh every second
        return () => clearInterval(interval);
    });
</script>

<div class="component">
    {#if $error}
        <p style="color: red;">Error: {$error}</p>
    {:else if !topProcesses.length}
        <p>Loading stats...</p>
        <!-- Show a loading message if stats are not available -->
    {:else}
        <div class="table-container">
            <!--h2>Top 5 Processes</h2-->
            <table>
                <thead>
                    <tr>
                        <th>PID</th>
                        <th>Process Name</th>
                        <th>CPU Usage (%)</th>
                    </tr>
                </thead>
                <tbody>
                    {#each topProcesses as process}
                        <tr>
                            <td>{process.pid}</td>
                            <td>{process.name}</td>
                            <td>{process.cpu_percent.toFixed(0)}%</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}
</div>

<style>
    .table-container {
        max-width: 600px;
        margin: auto;
        padding: 20px;
        background: #f9f9f9;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        color: #333;
        text-align: center;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }

    th,
    td {
        padding: 10px;
        border: 1px solid #ddd;
    }

    th {
        background-color: #007bff;
        color: white;
    }

    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
</style>

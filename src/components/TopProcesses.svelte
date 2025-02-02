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
    @import "./table.css";
</style>

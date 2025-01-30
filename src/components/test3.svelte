<script>
    import { stats, error } from "./apidata.js";
    import { onMount } from "svelte";

    async function fetchStats() {
        try {
            console.log($stats.cpu.usage);
        } catch (err) {
            //error = err.message;
            console.error("Error fetching stats:", err);
        }
    }

    // Fetch stats every second
    onMount(() => {
        const interval = setInterval(fetchStats, 1000);
        return () => clearInterval(interval);
    });
</script>

<div>
    {#if error}
        <p style="color: red;">Error: {error}</p>
    {:else}
        <div class="dashboard"></div>
    {/if}
</div>

<style>
    @import "../app.css";
</style>

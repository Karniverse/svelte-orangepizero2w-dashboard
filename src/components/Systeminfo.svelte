<script>
    import { stats, error } from "../lib/apidata.js"; // Ensure stats and error are stores
    import { onMount } from "svelte";

    let Systeminfo = {};

    onMount(() => {
        const interval = setInterval(fetchStats, 1000); // Fetch stats every second
        return () => clearInterval(interval); // Cleanup interval on component destruction
    });

    function fetchStats() {
        if ($stats && $stats.systeminfo) {
            Systeminfo = $stats.systeminfo;
            //console.log($stats.top_processes);
        }
        Systeminfo = { ...Systeminfo };
    }
</script>

<div class="component">
    {#if $error}
        <p style="color: red;">Error: {$error}</p>
    {:else if !$stats || !$stats.cpu || !$stats.ram}
        <p>Loading stats...</p>
        <!-- Show a loading message if stats are not available -->
    {:else}
        <div>
            <h2>System Monitoring Dashboard</h2>
            <div class="infocontainer">
                <h4 class="label">Processor</h4>
                <p>{Systeminfo.processor}</p>
                <h4 class="label">Cores</h4>
                <p>{Systeminfo.corecount}</p>
                <h4 class="label">Thread</h4>
                <p>{Systeminfo.threadcount}</p>
                <h4 class="label">Platform</h4>
                <p>{Systeminfo.platform}</p>
                <h4 class="label">Machine Name</h4>
                <p>{Systeminfo.machinename}</p>
                <h4 class="label">Uptime</h4>
                <p>{Systeminfo.uptime}</p>
            </div>
            <!--Display the uptime -->
        </div>
    {/if}
</div>

<style>
    .infocontainer {
        display: grid;
        grid-template-columns: 1fr 2fr; /* Labels take 1 part, values take 2 parts */
        gap: 10px;
        align-items: center;
        max-width: 500px; /* Adjust width */
        margin: auto; /* Center it */
        padding: 20px;
        background: #f9f9f9;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        color: #333333;
    }
    h2 {
        /*display: grid;
        grid-template-columns: 1fr 2fr; /* Labels take 1 part, values take 2 parts */
        /*gap: 10px;*/
        align-items: center;
        max-width: 500px; /* Adjust width */
        margin: auto; /* Center it */
        padding: 20px;
        background: #f9f9f9;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        color: #333333;
    }
    .label {
        font-weight: bold;
        color: #333;
    }
</style>

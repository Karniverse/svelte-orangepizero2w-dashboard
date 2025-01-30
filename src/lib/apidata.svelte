<script>
    import { onMount } from "svelte";
    import { stats, error } from "./stores.js";

    async function fetchStats() {
        try {
            const response = await fetch(
                //"http://orangepizero2w.local:7000/api/stats",
                "http://localhost:7000/api/stats",
            );
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            console.log("Stats received:", data);

            // Update the stats store
            stats.set(data);
        } catch (err) {
            error.set(err.message);
            console.error("Error fetching stats:", err);
        }
    }

    // Fetch stats every second
    onMount(() => {
        const interval = setInterval(fetchStats, 1000);
        return () => clearInterval(interval);
    });
</script>

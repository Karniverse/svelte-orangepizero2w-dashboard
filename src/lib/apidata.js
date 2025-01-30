import { writable } from "svelte/store";
//import { onMount } from "svelte";

export const stats = writable({});
export const error = writable(null);

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
        //console.log("Stats received:", data);

        // Update the stats store
        stats.set(data);
    } catch (err) {
        error.set(err.message);
        console.error("Error fetching stats:", err);
    }
}
setInterval(fetchStats, 1000);
// Fetch stats every second
/*onMount(() => {
const interval = setInterval(fetchStats, 1000);
return () => clearInterval(interval);
});*/
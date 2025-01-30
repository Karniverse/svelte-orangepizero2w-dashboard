<script>
    import { onMount, onDestroy } from "svelte";
    import { Chart, registerables } from "chart.js";
    Chart.register(...registerables);

    export let id; // Unique ID for the canvas
    export let data;
    export let options;

    let chart;

    onMount(() => {
        const ctx = document.getElementById(id).getContext("2d");
        chart = new Chart(ctx, {
            type: "line",
            data,
            options,
        });
    });

    onDestroy(() => {
        if (chart) {
            chart.destroy();
        }
    });

    // Update the chart when data changes
    $: {
        if (chart) {
            chart.data = data;
            chart.update();
        }
    }
</script>

<canvas {id} />

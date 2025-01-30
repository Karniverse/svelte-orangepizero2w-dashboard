<script>
    import { onMount, onDestroy } from "svelte";
    import { Chart, registerables } from "chart.js"; // Register all Chart.js components

    Chart.register(...registerables); // Registers all chart types including 'pie'

    export let data;
    export let options = {};

    let chart;
    let chartContainer;

    onMount(() => {
        const ctx = chartContainer.getContext("2d");
        chart = new Chart(ctx, {
            type: "bar", // Pie chart type
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

<canvas bind:this={chartContainer}></canvas>

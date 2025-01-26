<script>
  import LineChart from "./components/LineChart.svelte";
  import { onMount } from "svelte";

  let cpuData = {
    labels: [],
    datasets: [
      {
        label: "CPU Usage (%)",
        data: [],
        borderColor: "rgba(75, 192, 192, 1)",
        fill: false,
      },
    ],
  };

  let memoryData = {
    labels: [],
    datasets: [
      {
        label: "Memory Usage (%)",
        data: [],
        borderColor: "rgba(153, 102, 255, 1)",
        fill: false,
      },
    ],
  };

  let diskData = {
    labels: [],
    datasets: [
      {
        label: "Disk Usage (%)",
        data: [],
        borderColor: "rgba(255, 159, 64, 1)",
        fill: false,
      },
    ],
  };

  let error = null;

  async function fetchStats() {
    try {
      const response = await fetch(
        "http://orangepizero2w.local:7000/api/stats",
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const stats = await response.json();
      console.log("Stats received:", stats);

      // Update CPU data
      cpuData.labels.push(new Date().toLocaleTimeString());
      cpuData.datasets[0].data.push(stats.cpu.usage);
      if (cpuData.labels.length > 10) {
        cpuData.labels.shift();
        cpuData.datasets[0].data.shift();
      }

      // Update Memory data
      memoryData.labels.push(new Date().toLocaleTimeString());
      memoryData.datasets[0].data.push(stats.ram.percent);
      if (memoryData.labels.length > 10) {
        memoryData.labels.shift();
        memoryData.datasets[0].data.shift();
      }

      // Update Disk data
      diskData.labels.push(new Date().toLocaleTimeString());
      diskData.datasets[0].data.push(stats.disk.percent);
      if (diskData.labels.length > 10) {
        diskData.labels.shift();
        diskData.datasets[0].data.shift();
      }

      // Force Svelte to react to data changes
      cpuData = { ...cpuData };
      memoryData = { ...memoryData };
      diskData = { ...diskData };
    } catch (err) {
      error = err.message;
      console.error("Error fetching stats:", err);
    }
  }

  // Fetch stats every second
  onMount(() => {
    const interval = setInterval(fetchStats, 1000);
    return () => clearInterval(interval);
  });
</script>

<div class="dashboard">
  <h1>System Performance Dashboard</h1>

  {#if error}
    <p style="color: red;">Error: {error}</p>
  {:else}
    <div class="chart-container">
      <h2>CPU Usage</h2>
      <LineChart id="cpuChart" data={cpuData} options={{ responsive: true }} />
    </div>

    <div class="chart-container">
      <h2>Memory Usage</h2>
      <LineChart
        id="memoryChart"
        data={memoryData}
        options={{ responsive: true }}
      />
    </div>

    <div class="chart-container">
      <h2>Disk Usage</h2>
      <LineChart
        id="diskChart"
        data={diskData}
        options={{ responsive: true }}
      />
    </div>
  {/if}
</div>

<style>
  .dashboard {
    font-family: Arial, sans-serif;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  h1 {
    color: #333;
    text-align: center;
  }
  .chart-container {
    background: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
  }
</style>

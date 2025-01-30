<script>
    import { onMount } from "svelte";
    export let data;

    // Function to format bytes into human-readable format
    function formatBytes(bytes) {
        if (bytes === 0) return "0 Bytes";
        const k = 1024;
        const sizes = ["Bytes", "KB", "MB", "GB"];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
    }

    async function getSystemInfo() {
        try {
            // Get hostname
            const [hostname] = await Promise.all([
                new Promise((resolve) => {
                    subprocess.run("hostname", (error, stdout, stderr) => {
                        if (error) resolve("Unknown");
                        else resolve(stdout.trim());
                    });
                }),
            ]);

            // Get CPU info
            const [cpuInfo] = await Promise.all([
                new Promise((resolve) => {
                    subprocess.run("lscpu", (error, stdout, stderr) => {
                        if (error) resolve({ model: "Unknown", cores: 0 });
                        else {
                            const lines = stdout.split("\n");
                            const modelLine = lines.find((line) =>
                                line.startsWith("model name"),
                            );
                            const coresLine = lines.find((line) =>
                                line.startsWith("CPU(s):"),
                            );
                            const model = modelLine
                                ? modelLine.split(":")[1].trim()
                                : "Unknown";
                            const cores = coresLine
                                ? parseInt(coresLine.split(":")[1].trim())
                                : 0;
                            resolve({ model, cores });
                        }
                    });
                }),
            ]);

            // Get memory info
            const [memoryInfo] = await Promise.all([
                new Promise((resolve) => {
                    subprocess.run("free -h", (error, stdout, stderr) => {
                        if (error)
                            resolve({ total: "Unknown", used: "Unknown" });
                        else {
                            const lines = stdout.split("\n");
                            const memLine = lines[1].split(/\s+/);
                            resolve({
                                total: formatBytes(parseInt(memLine[1])),
                                used: formatBytes(parseInt(memLine[2])),
                            });
                        }
                    });
                }),
            ]);

            // Get uptime
            const [uptime] = await Promise.all([
                new Promise((resolve) => {
                    subprocess.run("uptime", (error, stdout, stderr) => {
                        if (error) resolve("Unknown");
                        else {
                            const uptimeData = stdout
                                .split(", ")[1]
                                .split(" up ")[1];
                            resolve(uptimeData);
                        }
                    });
                }),
            ]);

            return {
                machineName: hostname,
                cpuInfo,
                memoryInfo,
                uptime,
            };
        } catch (error) {
            console.error("System info error:", error);
            return {
                machineName: "Unknown",
                cpuInfo: { model: "Unknown", cores: 0 },
                memoryInfo: { total: "Unknown", used: "Unknown" },
                uptime: "Unknown",
            };
        }
    }

    let systemInfo = await getSystemInfo();

    onMount(async () => {
        // Update system info periodically (e.g., every minute)
        const interval = setInterval(async () => {
            systemInfo = await getSystemInfo();
        }, 60000);
        return () => clearInterval(interval);
    });
</script>

<div class="system-info">
    <h2>System Information</h2>

    <div class="system-info-box">
        <h3>Machine Name</h3>
        <p>{systemInfo.machineName}</p>
    </div>

    <div class="system-info-box">
        <h3>CPU Information</h3>
        <p>Model: {systemInfo.cpuInfo.model}</p>
        <p>Cores: {systemInfo.cpuInfo.cores}</p>
    </div>

    <div class="system-info-box">
        <h3>Memory Information</h3>
        <p>Total: {systemInfo.memoryInfo.total}</p>
        <p>Used: {systemInfo.memoryInfo.used}</p>
    </div>

    <div class="system-info-box">
        <h3>Uptime</h3>
        <p>{systemInfo.uptime}</p>
    </div>
</div>

<style>
    .system-info {
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    .system-info h2 {
        color: #333;
        text-align: center;
        font-size: 1.5em;
    }

    .system-info-box {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }

    .system-info-box h3 {
        color: #666;
        font-size: 1.2em;
        margin-top: 0;
    }

    .system-info p {
        line-height: 1.4;
        color: #444;
    }
</style>

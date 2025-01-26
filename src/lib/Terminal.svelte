<script>
    let output = "";
    let command = "";

    // WebSocket connection
    const ws = new WebSocket("ws://localhost:3000/terminal");

    ws.onmessage = (event) => {
        output += event.data;
    };

    function sendCommand() {
        ws.send(command + "\n");
        command = "";
    }
</script>

<div class="terminal">
    <pre>{output}</pre>
    <input
        bind:value={command}
        on:keydown={(e) => e.key === "Enter" && sendCommand()}
        placeholder="Enter command..."
    />
</div>

<style>
    .terminal {
        background: #000;
        color: #fff;
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
        height: 300px;
        overflow-y: auto;
    }
    input {
        width: 100%;
        padding: 5px;
        margin-top: 10px;
    }
</style>

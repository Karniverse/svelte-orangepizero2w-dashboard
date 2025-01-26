<script>
    let files = [];
    let currentPath = "/";

    async function fetchFiles(path) {
        const response = await fetch(`/api/files?path=${path}`);
        files = await response.json();
    }

    fetchFiles(currentPath);

    function navigate(path) {
        currentPath = path;
        fetchFiles(path);
    }
</script>

<div class="file-explorer">
    <h3>File Explorer: {currentPath}</h3>
    {#each files as file}
        <div class="file-item" on:click={() => navigate(file)}>
            {file}
        </div>
    {/each}
</div>

<style>
    .file-explorer {
        background: #f4f4f4;
        padding: 10px;
        border-radius: 5px;
    }
    .file-item {
        cursor: pointer;
        padding: 5px;
    }
    .file-item:hover {
        background: #ddd;
    }
</style>

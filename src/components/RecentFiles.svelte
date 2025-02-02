<script>
    import { stats, error } from "../lib/apidata.js"; // Ensure stats and error are stores
    import { onMount } from "svelte";

    import { get } from "svelte/store";

    let RecentFiles = [];
    let LargeFiles = [];

    function fetchStats() {
        const data = get(stats); // Get the latest value of the store
        if (data && data.filelist.recent_files && data.filelist.large_files) {
            RecentFiles = [...data.filelist.recent_files]; // Spread to trigger reactivity
            LargeFiles = [...data.filelist.large_files];
        }
    }

    onMount(() => {
        fetchStats(); // Fetch once on mount
        const interval = setInterval(fetchStats, 1000); // Refresh every second
        return () => clearInterval(interval);
    });
</script>

<div class="component">
    {#if $error}
        <p style="color: red;">Error: {$error}</p>
    {:else if !RecentFiles.length}
        <p>Loading stats...</p>
        <!-- Show a loading message if stats are not available -->
    {:else}
        <div class="table-container">
            <div class="tabletitle">Recent Files</div>
            <!--h4>Recent Files</h4-->
            <table>
                <thead>
                    <tr>
                        <th>Filename</th>
                        <th>Size</th>
                        <th>Modified Date(%)</th>
                    </tr>
                </thead>
                <tbody>
                    {#each RecentFiles as list}
                        <tr>
                            <td>{list.name}</td>
                            <td>{list.size}</td>
                            <td>{list.modified}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
            <div class="tabletitle">Large Files</div>
            <!--h4>Large Files</h4-->
            <table>
                <thead>
                    <tr>
                        <th>Filename</th>
                        <th>Size</th>
                        <th>Modified Date(%)</th>
                    </tr>
                </thead>
                <tbody>
                    {#each LargeFiles as list}
                        <tr>
                            <td>{list.name}</td>
                            <td>{list.size}</td>
                            <td>{list.modified}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}
</div>

<style>
    @import "./table.css";
</style>

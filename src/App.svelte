<script>
  import SystemStats from "./components/SystemStats.svelte";
  import SystemInfo from "./components/SystemInfo.svelte";
  import Diskinfo from "./components/Diskstats.svelte";
  //import TopProcesses from "./components/TopProcesses.svelte";
  //import Test from "../temp/Test.svelte";
  //import Test2 from "./components/test2.svelte";
  //import Test3 from "./components/test3.svelte";
  //import Apidata from "./components/apidata.svelte";
  //import { stats, error } from "./components/stores.js";
  //import { stats, error } from "./components/apidata.svelte";
</script>

<div class="container">
  <SystemInfo />
  <SystemStats />
  <Diskinfo />
  <!--Apidata /-->
  <!--Test /-->
  <!--Test2 /-->
  <!--Test3 /-->
</div>

<style>
  @import "./app.css";
</style>

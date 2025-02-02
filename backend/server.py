from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import psutil
import time
import platform
import cpuinfo
import os
import datetime
import concurrent.futures

app = FastAPI()
system = platform.system()
cpu_info = cpuinfo.get_cpu_info()
cpu_name = cpu_info.get('brand_raw', 'Unknown CPU')  # Get the human-readable CPU name
cpu_speed = cpu_info.get('hz_advertised_friendly') if cpu_info.get('hz_advertised_friendly') else "Unknown"
# Get number of physical and logical CPU cores
physical_cores = psutil.cpu_count(logical=False)  # Physical cores
logical_cores = psutil.cpu_count(logical=True) 


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Proper cross-platform home directory detection
if platform.system() == "Linux":  # Linux
    HOME_DIR = os.getenv("HOME", os.path.expanduser("~"))  # /home/username
else:  # Windows/others
    HOME_DIR = os.path.expanduser("~")  # C:\Users\YourUsername

MAX_FILES = 5000  # Prevents excessive scanning

# Converts bytes to human-readable format
def human_readable_size(size_in_bytes):
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_in_bytes)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"

# Converts epoch timestamp to human-readable format
def human_readable_time(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime("%Y-%m-%d %H:%M:%S")

def scan_directory(directory):
    files = []
    try:
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file():
                    try:
                        file_size_bytes = entry.stat().st_size  # Keep size in bytes
                        file_size_hr = human_readable_size(file_size_bytes)  # Convert to readable size
                        modified_time = human_readable_time(entry.stat().st_mtime)  # Convert time
                        full_path = entry.path
                        
                        files.append({
                            "name": entry.name, 
                            "size": file_size_hr, 
                            "size_bytes": file_size_bytes,  # Store for sorting
                            "modified": modified_time,
                            "path": full_path
                        })
                    except Exception as e:
                        print(f"Error accessing {entry.name}: {e}")
                if len(files) >= MAX_FILES:
                    break  # Stop early if too many files
    except PermissionError:
        pass  # Ignore folders we don’t have access to
    return files

def get_top_files():
    all_files = []

    # Get only top-level directories in home
    with os.scandir(HOME_DIR) as entries:
        subdirs = [entry.path for entry in entries if entry.is_dir()]

    # Scan home + top-level directories in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(scan_directory, [HOME_DIR] + subdirs)

    # Collect all file data
    for result in results:
        all_files.extend(result)

    # Sort by modification time (recent first)
    recent_files = sorted(all_files, key=lambda x: x["modified"], reverse=True)[:5]

    # Sort by actual file size (in bytes) (largest first)
    large_files = sorted(all_files, key=lambda x: x["size_bytes"], reverse=True)[:5]

    return {"recent_files": recent_files, "large_files": large_files}

# Cross-platform CPU temperature
def get_cpu_temperature():
    #system = platform.system()
    if system == "Linux":
        try:
            output = subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True)
            return float(output.decode("utf-8")) / 1000
        except Exception as e:
            print(f"Error fetching CPU temperature (Linux): {e}")
            return 0
    elif system == "Windows":
        try:
            output = subprocess.check_output("wmic /namespace:\\\\root\\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature", shell=True)
            temperature = float(output.decode("utf-8").split("\n")[1].strip()) / 10 - 273.15
            return temperature
        except Exception as e:
            #print(f"Error fetching CPU temperature (Windows): {e}")
            return 0
    else:
        print("Unsupported OS for CPU temperature")
        return 0

# Cross-platform CPU frequency
def get_cpu_freq():
    #system = platform.system()
    if system == "Linux":
        try:
            output = subprocess.check_output("vcgencmd measure_clock arm | cut -d '=' -f 2", shell=True)
            return int(output.decode("utf-8")) / 1000000
        except Exception as e:
            print(f"Error fetching CPU frequency (Linux): {e}")
            return 0
    elif system == "Windows":
        try:
            output = subprocess.check_output("wmic cpu get CurrentClockSpeed", shell=True)
            return float(output.decode("utf-8").split("\n")[1].strip())
        except Exception as e:
            print(f"Error fetching CPU frequency (Windows): {e}")
            return 0
    else:
        print("Unsupported OS for CPU frequency")
        return 0

#calculating network usuage
# Store the previous network counters globally
previous_counters = psutil.net_io_counters()

# Interval to calculate network usage in seconds
NETWORK_UPDATE_INTERVAL = 1  # 1 second

# Store the previous disk counters globally
previous_disk_counters = psutil.disk_io_counters()

def calculate_disk_usage():
    global previous_disk_counters
    current_disk_counters = psutil.disk_io_counters()
    read_speed = (current_disk_counters.read_bytes - previous_disk_counters.read_bytes)
    write_speed = (current_disk_counters.write_bytes - previous_disk_counters.write_bytes)
    previous_disk_counters = current_disk_counters  # Update the previous counters
    return read_speed, write_speed

def calculate_network_usage():
    global previous_counters
    current_counters = psutil.net_io_counters()
    upload_speed = (current_counters.bytes_sent - previous_counters.bytes_sent) / NETWORK_UPDATE_INTERVAL
    download_speed = (current_counters.bytes_recv - previous_counters.bytes_recv) / NETWORK_UPDATE_INTERVAL
    previous_counters = current_counters  # Update the previous counters
    return upload_speed, download_speed

def timeformatter(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return '%d:%02d:%02d' % (hour, min, sec)

# Get top 5 processes by CPU usage
def get_top_processes():
    num_cores = psutil.cpu_count(logical=True)  # Get total number of cores
    
    processes = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            if p.info['name'] and "idle" in p.info['name'].lower():  # Ignore "System Idle Process"
                continue  # Skip this process
            
            cpu_percent = p.info['cpu_percent'] / num_cores  # Normalize per core
            processes.append((p.info['pid'], p.info['name'], round(cpu_percent, 2)))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    processes.sort(key=lambda x: x[2], reverse=True)  # Sort by CPU usage
    return processes[:5]  # Return top 5 processes



# System stats endpoint
@app.get("/api/stats")
def get_stats():
    #print("Fetching system stats...")
    # #cpu_temperature = get_cpu_temperature()
    # #print(f"CPU Temperature: {cpu_temperature}°C")
    cpu_usage = psutil.cpu_percent(interval=0.1)
    #print(f"CPU Usage: {cpu_usage}%")
    ram = psutil.virtual_memory()
    #print(f"RAM Used: {ram.used} bytes")
    diskusage = psutil.disk_usage("/")
    read_speed, write_speed = calculate_disk_usage()
    upload_speed, download_speed = calculate_network_usage()
    #print(f"Netwrok Usage: {network.used} bytes")
    # #print(f"Disk Used: {disk.used} bytes")
    uptime = timeformatter(time.time() - psutil.boot_time())
    #diskio=psutil.disk_io_counters()

    top_processes = get_top_processes()  # Get top 5 processes
    top_files = get_top_files()
    return {
        "cpu": {
            #"temperature": cpu_temperature,
            "usage": cpu_usage,
            "frequency": get_cpu_freq(),
        },
        "ram": {
            "used": ram.used,
            "total": ram.total,
            "percent": ram.percent,
        },
        "network": {
            "upload_speed": upload_speed,  # Bytes/sec
            "download_speed": download_speed,  # Bytes/sec
        },
        "disk": {
            "used": diskusage.used,
            "free": diskusage.free,
            "total": diskusage.total,
            "percent": diskusage.percent,
            "diskrbytes":read_speed,
            "diskwbytes":write_speed,
        },
        "systeminfo":{
            "processor":cpu_name,
            "cpuspeed":cpu_speed,
            "corecount": physical_cores,
            "threadcount": logical_cores,
            "machinename":platform.node(),
            "platform":system,
            "version":platform.release(),
            "uptime":uptime,
            #"tmp":cpu_info,
        },
        
        "top_processes": [
            {"pid": p[0], "name": p[1], "cpu_percent": p[2]} for p in top_processes
        ],
        "filelist":top_files
        
    }

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import psutil
import time
import platform

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cross-platform CPU temperature
def get_cpu_temperature():
    system = platform.system()
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
    system = platform.system()
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

# System stats endpoint
@app.get("/api/stats")
def get_stats():
    #print("Fetching system stats...")
    cpu_temperature = get_cpu_temperature()
    #print(f"CPU Temperature: {cpu_temperature}°C")
    cpu_usage = psutil.cpu_percent(interval=0.1)
    #print(f"CPU Usage: {cpu_usage}%")
    ram = psutil.virtual_memory()
    #print(f"RAM Used: {ram.used} bytes")
    disk = psutil.disk_usage("/")
    #print(f"Disk Used: {disk.used} bytes")

    return {
        "cpu": {
            "temperature": cpu_temperature,
            "usage": cpu_usage,
            "frequency": get_cpu_freq(),
        },
        "ram": {
            "used": ram.used,
            "total": ram.total,
            "percent": ram.percent,
        },
        "disk": {
            "used": disk.used,
            "total": disk.total,
            "percent": disk.percent,
        },
    }

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000)
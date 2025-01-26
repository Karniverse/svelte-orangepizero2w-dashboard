from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import psutil
import time

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (replace "*" with your frontend URL in production)
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Your existing functions
def get_cpu_temperature():
    output = subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True)
    return float(output.decode("utf-8")) / 1000

def get_cpu_min_max_freqs():
    try:
        output = subprocess.check_output("lscpu", shell=True)
        decoded_output = output.decode("utf-8")
        freqMin = 0
        freqMax = 0
        for line in decoded_output.split("\n"):
            if "CPU max" in line:
                freqMax = read_freq_from_line(line)
            elif "CPU min" in line:
                freqMin = read_freq_from_line(line)
        return (freqMin, freqMax)
    except:
        return (0, 0)

def read_freq_from_line(line):
    part = line.split(":")
    return float(part[1].strip().replace(",", "."))

def get_cpu_cur_freq():
    try:
        output = subprocess.check_output("vcgencmd measure_clock arm | cut -d '=' -f 2", shell=True)
        decoded_output = output.decode("utf-8")
        curr_freq = int(decoded_output) / 1000000
        return curr_freq
    except:
        return 0

def get_cpu_count():
    try:
        return psutil.cpu_count()
    except:
        return 1

def read_net_data():
    d = {
        'bytes_recv': 0,
        'bytes_sent': 0,
        'packets_recv': 0,
        'packets_sent': 0,
        'err_in': 0,
        'err_out': 0
    }
    for interface in ["wlan0", "eth0"]:
        try:
            net_stat = psutil.net_io_counters(pernic=True)[interface]
            d['bytes_recv'] += net_stat.bytes_recv
            d['bytes_sent'] += net_stat.bytes_sent
            d['packets_recv'] += net_stat.packets_recv
            d['packets_sent'] += net_stat.packets_sent
            d['err_in'] += net_stat.errin
            d['err_out'] += net_stat.errout
        except:
            pass
    return d

def calculate_net_speed(start_time, start_net_data, current_net_data):
    end_time = time.time() - start_time
    end_bytes_recv = current_net_data['bytes_recv'] - start_net_data['bytes_recv']
    end_bytes_sent = current_net_data['bytes_sent'] - start_net_data['bytes_sent']
    download_speed = end_bytes_recv / end_time / 1024
    upload_speed = end_bytes_sent / end_time / 1024
    return (download_speed, upload_speed)

# API endpoint to get system stats
@app.get("/api/stats")
def get_stats():
    start_net_data = read_net_data()
    start_reading_time = time.time()

    cpu_temperature = get_cpu_temperature()
    cpu_usage = psutil.cpu_percent(0.1, False)
    cpu_count = get_cpu_count()
    time.sleep(0.6)  # Pause for a correct reading of the frequency
    try:
        freqs = psutil.cpu_freq()
        cpu_freq_current = freqs.current
        cpu_freq_min = freqs.min
        cpu_freq_max = freqs.max
    except:
        cpu_freq_current = get_cpu_cur_freq()
        cpu_freq_min, cpu_freq_max = get_cpu_min_max_freqs()

    ram = psutil.virtual_memory()
    bToMb = float(2**20)
    ram_total = ram.total / bToMb
    ram_used = ram.used / bToMb
    ram_free = ram.free / bToMb
    ram_available = ram.available / bToMb
    ram_percent_used = ram.percent

    time.sleep(1)
    current_net_data = read_net_data()
    download_speed, upload_speed = calculate_net_speed(start_reading_time, start_net_data, current_net_data)

    disk_stats = []
    for part in psutil.disk_partitions():
        disk = psutil.disk_usage(part.mountpoint)
        bToGb = float(2**30)
        disk_stats.append({
            'mountpoint': part.mountpoint,
            'total': disk.total / bToGb,
            'used': disk.used / bToGb,
            'free': disk.free / bToGb,
            'percent_used': disk.percent
        })

    return {
        'cpu': {
            'temperature': cpu_temperature,
            'usage': cpu_usage,
            'count': cpu_count,
            'freq_current': cpu_freq_current,
            'freq_min': cpu_freq_min,
            'freq_max': cpu_freq_max
        },
        'ram': {
            'total': ram_total,
            'used': ram_used,
            'free': ram_free,
            'available': ram_available,
            'percent_used': ram_percent_used
        },
        'network': {
            'download_speed': download_speed,
            'upload_speed': upload_speed,
            'bytes_recv': current_net_data['bytes_recv'] / bToMb,
            'bytes_sent': current_net_data['bytes_sent'] / bToMb,
            'packets_recv': current_net_data['packets_recv'],
            'packets_sent': current_net_data['packets_sent'],
            'err_in': current_net_data['err_in'],
            'err_out': current_net_data['err_out']
        },
        'disk': disk_stats
    }

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
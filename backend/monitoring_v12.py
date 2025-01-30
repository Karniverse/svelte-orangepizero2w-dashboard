#!\venv\Scripts\python.exe
import subprocess
import psutil
import time
import array



def get_cpu_temperature():
    output = subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True)
    decoded_output = output.decode("utf-8")
    return float(decoded_output)/1000


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
        curr_freq = int(decoded_output)/1000000
        return curr_freq
    except:
        return 0

 
def get_cpu_count():
    try:
        return psutil.cpu_count()
    except:
        return 1


NET_KEY_BYTES_RECV = 'bytes_recv'
NET_KEY_BYTES_SENT = 'bytes_sent'
NET_KEY_PACKETS_RECV = 'packets_recv'
NET_KEY_PACKETS_SENT = 'packets_sent'
NET_KEY_ERR_IN = 'err_in'
NET_KEY_ERR_OUT = 'err_out'


def read_net_data():
    d = dict()
    d[NET_KEY_BYTES_RECV] = 0
    d[NET_KEY_BYTES_SENT] = 0
    d[NET_KEY_PACKETS_RECV] = 0
    d[NET_KEY_PACKETS_SENT] = 0
    d[NET_KEY_ERR_IN] = 0
    d[NET_KEY_ERR_OUT] = 0
    put_net_data_to_dict("wlan0", d)
    put_net_data_to_dict("eth0", d)
    return d


def put_net_data_to_dict(interface, d):
    try:
        net_stat = psutil.net_io_counters(pernic=True)[interface]
        d[NET_KEY_BYTES_RECV] += net_stat.bytes_recv
        d[NET_KEY_BYTES_SENT] += net_stat.bytes_sent
        d[NET_KEY_PACKETS_RECV] += net_stat.packets_recv
        d[NET_KEY_PACKETS_SENT] += net_stat.packets_sent
        d[NET_KEY_ERR_IN] += net_stat.errin
        d[NET_KEY_ERR_OUT] += net_stat.errout
    except:
        pass
    
    
def calculate_net_speed(start_time, start_net_data, current_net_data):
    end_time = time.time() - start_time
    end_bytes_recv = current_net_data[NET_KEY_BYTES_RECV] - start_net_data[NET_KEY_BYTES_RECV]
    end_bytes_sent = current_net_data[NET_KEY_BYTES_SENT] - start_net_data[NET_KEY_BYTES_SENT]
    download_speed = end_bytes_recv / end_time / 1024
    upload_speed = end_bytes_sent / end_time / 1024
    return (download_speed, upload_speed)
    

def main():
    start_net_data = read_net_data()
    start_reading_time = time.time()

    cpu_temperature = get_cpu_temperature()
    print('CpuTemp = {0:0.2f} C'.format(cpu_temperature))
    cpu_usage = psutil.cpu_percent(0.1, False)
    print('CpuUsage = {0:0.2f} %'.format(cpu_usage))
    print('CpuCount = {0:0.0f}'.format(get_cpu_count()))
    time.sleep(0.6) # Pause for a correct reading of the frequency
    try:
        freqs = psutil.cpu_freq()
        print('CpuFreqCurrent = {0:0.2f} MHz'.format(freqs.current))
        print('CpuFreqMin = {0:0.2f} MHz'.format(freqs.min))
        print('CpuFreqMax = {0:0.2f} MHz'.format(freqs.max))
    except:
        print('CpuFreqCurrent = {0:0.2f} MHz'.format(get_cpu_cur_freq()))
        (freqMin, freqMax) = get_cpu_min_max_freqs()
        print('CpuFreqMin = {0:0.2f} MHz'.format(freqMin))
        print('CpuFreqMax = {0:0.2f} MHz'.format(freqMax))

    ram = psutil.virtual_memory()
    bToMb = float(2**20)
    ram_total = ram.total / bToMb       # MiB.
    print('RamTotal = {0:0.2f} MB'.format(ram_total))
    ram_used = ram.used / bToMb
    print('RamUsed = {0:0.2f} MB'.format(ram_used))
    ram_free = ram.free / bToMb
    print('RamFree = {0:0.2f} MB'.format(ram_free))
    ram_available = ram.available / bToMb
    print('RamAvailable = {0:0.2f} MB'.format(ram_available))
    ram_percent_used = ram.percent
    print('RamPercent = {0:0.2f} %'.format(ram_percent_used))
    
    time.sleep(1)
    current_net_data = read_net_data()
    (download_speed, upload_speed) = calculate_net_speed(start_reading_time, start_net_data, current_net_data)
    print('DownloadSpeed = {0:0.2f} kB/s'.format(download_speed))
    print('UploadSpeed = {0:0.2f} kB/s'.format(upload_speed))
    print('BytesRecv = {0:0.2f} MB'.format(current_net_data[NET_KEY_BYTES_RECV] / bToMb))
    print('BytesSent = {0:0.2f} MB'.format(current_net_data[NET_KEY_BYTES_SENT] / bToMb))
    print('PacketsRecv = {0:0.0f}'.format(current_net_data[NET_KEY_PACKETS_RECV]))
    print('PacketsSent = {0:0.0f}'.format(current_net_data[NET_KEY_PACKETS_SENT]))
    print('NetErrorIn = {0:0.0f}'.format(current_net_data[NET_KEY_ERR_IN]))
    print('NetErrorOut = {0:0.0f}'.format(current_net_data[NET_KEY_ERR_OUT]))
    
    print('FS = [')
    partition = psutil.disk_partitions()
    bToGb = float(2**30)
    for part in partition:
        print('Mountpoint = ' + part.mountpoint)
        disk = psutil.disk_usage(part.mountpoint)
        disk_total = disk.total / bToGb     # GiB.
        print('DiskTotal = {0:0.2f} GB'.format(disk_total))
        disk_used = disk.used / bToGb
        print('DiskUsed = {0:0.2f} GB'.format(disk_used))
        disk_free = disk.free / bToGb
        print('DiskFree = {0:0.2f} GB'.format(disk_free))
        disk_percent_used = disk.percent
        print('DiskPercent = {0:0.2f} %'.format(disk_percent_used))
        print(',')
    print(']')



if __name__ == '__main__':
    main()
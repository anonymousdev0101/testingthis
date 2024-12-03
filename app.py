import os
import platform
import psutil
import socket
import json

def get_system_info():
    info = {}

    # OS Info
    info['OS'] = platform.system()
    info['OS Version'] = platform.version()
    info['OS Release'] = platform.release()
    info['Architecture'] = platform.architecture()

    # CPU Info
    info['CPU'] = platform.processor()
    info['CPU Cores'] = psutil.cpu_count(logical=False)
    info['Logical CPUs'] = psutil.cpu_count(logical=True)
    info['CPU Usage'] = psutil.cpu_percent(interval=1)

    # Memory Info
    memory = psutil.virtual_memory()
    info['Total Memory'] = convert_bytes(memory.total)
    info['Available Memory'] = convert_bytes(memory.available)
    info['Used Memory'] = convert_bytes(memory.used)
    info['Memory Usage'] = memory.percent

    # Disk Info
    disk = psutil.disk_usage('/')
    info['Total Disk'] = convert_bytes(disk.total)
    info['Free Disk'] = convert_bytes(disk.free)
    info['Used Disk'] = convert_bytes(disk.used)
    info['Disk Usage'] = disk.percent

    # Network Info
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    info['Hostname'] = hostname
    info['IP Address'] = ip_address

    # Battery Info (if available)
    if psutil.sensors_battery():
        battery = psutil.sensors_battery()
        info['Battery Percentage'] = battery.percent
        info['Battery Plugged'] = battery.power_plugged
        info['Battery Time Left'] = battery.secsleft // 60 if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited"

    return info

def convert_bytes(bytes_size):
    """ Convert bytes to a human-readable format (KB, MB, GB) """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024

def print_device_info(info):
    """ Pretty print device/system info in JSON format """
    print(json.dumps(info, indent=4))

if __name__ == '__main__':
    system_info = get_system_info()
    print_device_info(system_info)

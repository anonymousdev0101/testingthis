import os
import platform
import psutil
import socket
import streamlit as st

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

    # Disk Partitions
    partitions = psutil.disk_partitions()
    partition_info = []
    for partition in partitions:
        partition_info.append({
            'Device': partition.device,
            'Mount Point': partition.mountpoint,
            'Filesystem Type': partition.fstype,
            'Total': convert_bytes(psutil.disk_usage(partition.mountpoint).total),
            'Used': convert_bytes(psutil.disk_usage(partition.mountpoint).used),
            'Free': convert_bytes(psutil.disk_usage(partition.mountpoint).free),
            'Usage': psutil.disk_usage(partition.mountpoint).percent
        })
    info['Disk Partitions'] = partition_info

    # Network Info
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    info['Hostname'] = hostname
    info['IP Address'] = ip_address

    # Network Interfaces
    net_if_addrs = psutil.net_if_addrs()
    net_if_stats = psutil.net_if_stats()
    network_interfaces = []
    for interface, addrs in net_if_addrs.items():
        for addr in addrs:
            network_interfaces.append({
                'Interface': interface,
                'Address': addr.address,
                'Netmask': addr.netmask,
                'Broadcast': addr.broadcast,
                'Status': 'Up' if net_if_stats[interface].isup else 'Down'
            })
    info['Network Interfaces'] = network_interfaces

    # Uptime
    info['Uptime'] = str(psutil.boot_time())

    # Load Average (system load over the last 1, 5, and 15 minutes)
    load = psutil.getloadavg()
    info['Load Average'] = {
        '1 Minute': load[0],
        '5 Minutes': load[1],
        '15 Minutes': load[2]
    }

    # GPU Info (only works on systems with GPU and supported drivers)
    try:
        if platform.system() == 'Linux' or platform.system() == 'Windows':
            gpu_info = get_gpu_info()
            if gpu_info:
                info['GPU Info'] = gpu_info
    except Exception as e:
        info['GPU Info'] = "No GPU information available."

    # Battery Info (if available)
    try:
        if psutil.sensors_battery():
            battery = psutil.sensors_battery()
            info['Battery Percentage'] = battery.percent
            info['Battery Plugged'] = battery.power_plugged
            info['Battery Time Left'] = battery.secsleft // 60 if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited"
    except (FileNotFoundError, AttributeError):
        info['Battery Info'] = "Battery information not available (likely a desktop or VM)."

    # CPU Temperature (if available)
    try:
        cpu_temperature = psutil.sensors_temperatures().get('coretemp', [])
        if cpu_temperature:
            info['CPU Temperature'] = f"{cpu_temperature[0].current} °C"
    except Exception as e:
        info['CPU Temperature'] = "Temperature information not available."

    return info

def get_gpu_info():
    """ Function to retrieve GPU info on Linux/Windows """
    gpu_info = []
    if platform.system() == 'Linux':
        try:
            from subprocess import check_output
            # Get GPU info from the `lspci` command (Linux)
            gpu_data = check_output("lspci | grep VGA", shell=True).decode('utf-8')
            gpu_info.append(gpu_data.strip())
        except Exception as e:
            return None
    elif platform.system() == 'Windows':
        try:
            from gpuinfo import GPUInfo
            gpus = GPUInfo.get_info()
            for gpu in gpus:
                gpu_info.append(f"{gpu.name} - {gpu.memoryTotal} MB")
        except Exception as e:
            return None
    return gpu_info

def convert_bytes(bytes_size):
    """ Convert bytes to a human-readable format (KB, MB, GB) """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024

def display_device_info(info):
    """ Display the system/device info using Streamlit widgets """
    st.title("System Information")
    
    # Displaying OS Info
    st.subheader("Operating System")
    st.write(f"**OS:** {info['OS']}")
    st.write(f"**OS Version:** {info['OS Version']}")
    st.write(f"**OS Release:** {info['OS Release']}")
    st.write(f"**Architecture:** {info['Architecture']}")

    # Displaying CPU Info
    st.subheader("CPU Info")
    st.write(f"**CPU Model:** {info['CPU']}")
    st.write(f"**Physical Cores:** {info['CPU Cores']}")
    st.write(f"**Logical CPUs:** {info['Logical CPUs']}")
    st.write(f"**CPU Usage:** {info['CPU Usage']}%")

    # Displaying Memory Info
    st.subheader("Memory Info")
    st.write(f"**Total Memory:** {info['Total Memory']}")
    st.write(f"**Available Memory:** {info['Available Memory']}")
    st.write(f"**Used Memory:** {info['Used Memory']}")
    st.write(f"**Memory Usage:** {info['Memory Usage']}%")

    # Displaying Disk Info
    st.subheader("Disk Info")
    st.write(f"**Total Disk:** {info['Total Disk']}")
    st.write(f"**Free Disk:** {info['Free Disk']}")
    st.write(f"**Used Disk:** {info['Used Disk']}")
    st.write(f"**Disk Usage:** {info['Disk Usage']}%")

    # Displaying Disk Partitions
    st.subheader("Disk Partitions")
    for partition in info['Disk Partitions']:
        st.write(f"**{partition['Device']}** - Mount Point: {partition['Mount Point']}, "
                 f"Total: {partition['Total']}, Used: {partition['Used']}, Free: {partition['Free']}, Usage: {partition['Usage']}%")

    # Displaying Network Info
    st.subheader("Network Info")
    st.write(f"**Hostname:** {info['Hostname']}")
    st.write(f"**IP Address:** {info['IP Address']}")
    
    st.subheader("Network Interfaces")
    for iface in info['Network Interfaces']:
        st.write(f"**{iface['Interface']}** - IP: {iface['Address']}, Netmask: {iface['Netmask']}, "
                 f"Broadcast: {iface['Broadcast']}, Status: {iface['Status']}")

    # Displaying Uptime
    st.subheader("Uptime")
    st.write(f"**System Uptime:** {info['Uptime']}")

    # Displaying Load Average
    st.subheader("System Load Average")
    st.write(f"**1 Minute Load Average:** {info['Load Average']['1 Minute']}")
    st.write(f"**5 Minute Load Average:** {info['Load Average']['5 Minutes']}")
    st.write(f"**15 Minute Load Average:** {info['Load Average']['15 Minutes']}")

    # Displaying GPU Info
    if 'GPU Info' in info:
        st.subheader("GPU Info")
        for gpu in info['GPU Info']:
            st.write(f"**{gpu}**")

    # Displaying Battery Info
    if 'Battery Percentage' in info:
        st.subheader("Battery Info")
        st.write(f"**Battery Percentage:** {info['Battery Percentage']}%")
        st.write(f"**Battery Plugged:** {'Yes' if info['Battery Plugged'] else 'No'}")
        st.write(f"**Battery Time Left:** {info['Battery Time Left']} minutes" if isinstance(info['Battery Time Left'], int) else info['Battery Time Left'])
    else:
        st.write(info.get('Battery Info', 'No battery information available.'))

    # Displaying CPU Temperature
    if 'CPU Temperature' in info:
        st.subheader("CPU Temperature")
        st.write(f"**Current CPU Temperature:** {info['CPU Temperature']}")

if __name__ == '__main__':
    system_info = get_system_info()
    display_device_info(system_info)

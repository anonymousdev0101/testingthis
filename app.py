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

    # Network Info
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    info['Hostname'] = hostname
    info['IP Address'] = ip_address

    # Battery Info (if available)
    try:
        if psutil.sensors_battery():
            battery = psutil.sensors_battery()
            info['Battery Percentage'] = battery.percent
            info['Battery Plugged'] = battery.power_plugged
            info['Battery Time Left'] = battery.secsleft // 60 if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited"
    except (FileNotFoundError, AttributeError):
        info['Battery Info'] = "Battery information not available (likely a desktop or VM)."

    return info

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

    # Displaying Network Info
    st.subheader("Network Info")
    st.write(f"**Hostname:** {info['Hostname']}")
    st.write(f"**IP Address:** {info['IP Address']}")

    # Displaying Battery Info
    if 'Battery Percentage' in info:
        st.subheader("Battery Info")
        st.write(f"**Battery Percentage:** {info['Battery Percentage']}%")
        st.write(f"**Battery Plugged:** {'Yes' if info['Battery Plugged'] else 'No'}")
        st.write(f"**Battery Time Left:** {info['Battery Time Left']} minutes" if isinstance(info['Battery Time Left'], int) else info['Battery Time Left'])
    else:
        st.write(info.get('Battery Info', 'No battery information available.'))

if __name__ == '__main__':
    system_info = get_system_info()
    display_device_info(system_info)

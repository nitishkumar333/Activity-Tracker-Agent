import threading
import platform
import psutil
from getmac import get_mac_address

def gather_system_info(info_dict):
    """Gathers system information and updates the provided dictionary."""
    # Get MAC address
    mac_address = get_mac_address()
    
    # Get system and memory info
    cpu_count = psutil.cpu_count()
    memory_info = psutil.virtual_memory()

    # Populate the dictionary with system information
    info_dict['Node'] = platform.node()
    info_dict['System'] = platform.system()
    info_dict['MAC Address'] = mac_address
    info_dict['Version'] = platform.version()


def get_system_info():
    """Starts a thread to gather system information and returns a dictionary."""
    system_info = {}
    info_thread = threading.Thread(target=gather_system_info, args=(system_info,))
    info_thread.start()
    info_thread.join()  # Wait for the thread to finish
    return system_info

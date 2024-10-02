import threading
import platform
import psutil

def gather_system_info(info_dict):
    """Gathers system information and updates the provided dictionary."""
    # Populate the dictionary with system information
    info_dict['Node'] = platform.node()
    info_dict['System'] = platform.system()
    info_dict['machine'] = platform.machine()
    info_dict['Version'] = platform.version()


def get_system_info():
    """Starts a thread to gather system information and returns a dictionary."""
    system_info = {}
    info_thread = threading.Thread(target=gather_system_info, args=(system_info,))
    info_thread.start()
    info_thread.join()  # Wait for the thread to finish
    return system_info

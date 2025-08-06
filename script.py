import pyudev
import os
import time
import psutil

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)

GUID_FILE = "GUID.txt"

def start_listening_devices():
    monitor.filter_by(subsystem="block")
    monitor.start()

def get_mount_point(node):
    for part in psutil.disk_partitions():
        if part.device == node:
            return part.mountpoint
    return None

def wait_until_mounted(node, timeout):
    while timeout > 0:
        mount_point = get_mount_point(node)
        if not mount_point:
            timeout -= 1
            time.sleep(1) #If the device is not mounted yet, wait 1 second and try again until the device is found or the timeout is reached
            continue
        return mount_point
    return None


if __name__ == '__main__':
    context = pyudev.Context()
    start_listening_devices()
    for device in iter(monitor.poll, None):
        if device.action == "add" and device.get("ID_BUS"): #With ID_BUS I get how the device is connected to the device
            device_path = wait_until_mounted(monitor.poll().device_node, 10)
            if device_path:
                with open(os.path.join(device_path, ), "r") as f:
                    print(f.read())
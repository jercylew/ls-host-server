# sys_utils.py: Utils for system config
import subprocess


def restart_service(service_name):
    """Restart the specified app"""
    subprocess.run(f"systemctl restart {service_name}", shell=True)


def stop_service(service_name):
    """Restart the specified app"""
    subprocess.run(f"systemctl stop {service_name}", shell=True)


def start_service(service_name):
    """Restart the specified app"""
    subprocess.run(f"systemctl start {service_name}", shell=True)
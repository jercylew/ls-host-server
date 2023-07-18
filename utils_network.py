# utils_network.py: Utils for network config
import subprocess


def __get_prefix_from_mask__(mask):
    """Get the prefix from mask"""
    if mask == "" or mask is None:
        return "24"

    if mask == "255.255.255.255":
        return "32"

    if mask == "255.255.255.254":
        return "31"

    if mask == "255.255.255.252":
        return "30"

    if mask == "255.255.255.248":
        return "29"

    if mask == "255.255.255.240":
        return "28"

    if mask == "255.255.255.224":
        return "27"

    if mask == "255.255.255.192":
        return "26"

    if mask == "255.255.255.128":
        return "25"

    if mask == "255.255.255.0":
        return "24"

    if mask == "255.255.254.0":
        return "23"

    if mask == "255.255.252.0":
        return "22"

    if mask == "255.255.248.0":
        return "21"

    if mask == "255.255.240.0":
        return "20"

    if mask == "255.255.224.0":
        return "19"

    if mask == "255.255.192.0":
        return "18"

    if mask == "255.255.128.0":
        return "17"

    if mask == "255.255.0.0":
        return "16"

    if mask == "255.254.0.0":
        return "15"

    if mask == "255.252.0.0":
        return "14"

    if mask == "255.248.0.0":
        return "13"

    if mask == "255.240.0.0":
        return "12"

    if mask == "255.224.0.0":
        return "11"

    if mask == "255.192.0.0":
        return "10"

    if mask == "255.128.0.0":
        return "9"

    if mask == "255.0.0.0":
        return "8"

    if mask == "254.0.0.0":
        return "7"

    if mask == "252.0.0.0":
        return "6"

    if mask == "248.0.0.0":
        return "5"

    if mask == "240.0.0.0":
        return "4"

    if mask == "224.0.0.0":
        return "3"

    if mask == "192.0.0.0":
        return "2"

    if mask == "128.0.0.0":
        return "1"

    if mask == "0.0.0.0":
        return "0"


def get_active_network_ether_info():
    """Get basic info for active ethernet"""
    active_ethernet = subprocess.check_output("nmcli d | grep -w ethernet | cut -d ' ' -f 1 | head -n 1",
                                              shell=True).decode("utf-8")
    active_ethernet = active_ethernet.rstrip("\n")
    ip = subprocess.check_output(f"ifconfig {active_ethernet} | grep -w inet | cut -d ' ' -f 10",
                                 shell=True).decode("utf-8")
    ip = ip.rstrip("\n")

    mask = subprocess.check_output(f"ifconfig {active_ethernet} | grep -w inet | cut -d ' ' -f 13",
                                   shell=True).decode("utf-8")
    mask = mask.rstrip("\n")

    uuid = subprocess.check_output(f"nmcli con show | grep {active_ethernet} | cut -d ' ' -f 5",
                                   shell=True).decode("utf-8")
    uuid = uuid.rstrip("\n")

    temp_con_query = subprocess.check_output(f"nmcli con show {uuid} | grep IP4.GATEWAY | cut -d ':' -f 2",
                                             shell=True).decode("utf-8")
    default_gateway = temp_con_query.rstrip("\n")
    default_gateway = default_gateway.lstrip()

    temp_con_query = subprocess.check_output(f"nmcli con show {uuid} | grep IP4.DNS | cut -d ':' -f 2",
                                             shell=True).decode("utf-8")
    dns = temp_con_query.replace("\n", ",")
    dns = dns.replace(" ", "")

    return ip, mask, default_gateway, dns


def get_active_network_wifi_info():
    """Get basic info for active ethernet"""
    ip = ""
    mask = ""
    default_gateway = ""
    dns = ""

    return ip, mask, default_gateway, dns


def set_network(ip, mask, default_gateway, dns):
    """Set network"""
    active_ethernet = subprocess.check_output("nmcli d | grep -w ethernet | cut -d ' ' -f 1 | head -n 1",
                                              shell=True).decode("utf-8")
    active_ethernet = active_ethernet.rstrip("\n")
    if active_ethernet != '':
        return False, "No active ethernet device found!"

    prefix = __get_prefix_from_mask__(mask)
    subprocess.run(f"nmcli con mod {active_ethernet} ipv4.addresses {ip}/{prefix}", shell=True)
    subprocess.run(f"nmcli con mod {active_ethernet} ipv4.gateway {default_gateway}", shell=True)
    subprocess.run(f"nmcli con mod {active_ethernet} ipv4.dns '{dns}'", shell=True)
    subprocess.run(f"nmcli con mod {active_ethernet} ipv4.method manual", shell=True)
    subprocess.run(f"nmcli con up {active_ethernet}", shell=True)

    return True, "Ok"


def restore_network_with_dhcp():
    """Restore the active ethernet device to DHCP"""
    active_ethernet = subprocess.check_output("nmcli d | grep -w ethernet | cut -d ' ' -f 1 | head -n 1",
                                              shell=True).decode("utf-8")
    active_ethernet = active_ethernet.rstrip("\n")

    if active_ethernet != '':
        return False, "No active ethernet device found!"

    subprocess.run(f"nmcli con mod {active_ethernet} ipv4.address '' ", shell=True)
    subprocess.run(f"nmcli con mod {active_ethernet} ipv4.method auto", shell=True)
    subprocess.run(f"nmcli con down {active_ethernet}", shell=True)
    subprocess.run(f"nmcli con down {active_ethernet}", shell=True)

    return True, "Ok"

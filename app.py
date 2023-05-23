# -*- coding: utf-8 -*-
#@Author    : Qichunren

import threading
# import pyprctl # patch:set real thread name
import time
import os
import json
import datetime
import subprocess
import shutil
import pathlib
import requests

import network_stats
import pcat_config
from cmd_tool import CmdTool

socket_client = None
flask_app = None
main_app = None # Potin to App instance

def cmd_to_log(cmd_args, log_file):
  with open(log_file,"wb") as out, open(log_file,"wb") as err:
    subprocess.run(cmd_args, stdout=out,stderr=err)
  threading.Timer(20.0, lambda: shutil.rmtree("/cmd-shell")).start()    

# 获取文件修改时间
def modification_date(filename):
    t = os.path.getmtime(filename)
    t = datetime.datetime.fromtimestamp(t)
    t = t.strftime("%Y-%m-%d %H:%M:%S")
    return t

#　检测 SD 卡的状态
def sd_card_status(dev = "/dev/mmcblk1"):
  dev_exists = os.path.exists(dev)
  if dev_exists:
    return 1
  else:
    return 0

# 检测 Mutil Wan 的启动状态
def is_mutil_wan_enabled():
  multi_wan = False
  if os.path.islink("/etc/config/mwan3"):
    real_path = os.path.realpath("/etc/config/mwan3")
    if real_path == "/etc/config/mwan3-default":
      multi_wan = True
    elif real_path == "/etc/config/mwan3-off":
      multi_wan = False
  return multi_wan

# 开启 / 关闭 Multi Wan 功能
def enable_mutil_wan(enable_flag):
  old_flag = is_mutil_wan_enabled()
  if old_flag == enable_flag:
    print("Nothing changed for mutil wan config")
    return
  
  print("Set mutil wan config", enable_flag)
  if enable_flag:
    os.symlink("/etc/config/mwan3-default", "/etc/config/mwan3-temp")
  else:
    os.symlink("/etc/config/mwan3-off", "/etc/config/mwan3-temp")
  os.rename("/etc/config/mwan3-temp", "/etc/config/mwan3")
  threading.Timer(0.2, lambda: subprocess.run(["/usr/sbin/mwan3", "restart"])).start()

# WAN 接口是否开启
def is_wan_interface_enabled():
  try:
    cmd_output = subprocess.check_output(["uci", "get", "network.wan.disabled"]) # return bytes
    return cmd_output == b'0\n'
  except:
    return True

# 开启 / 关闭 WAN 接口
def enable_wan_interface(enable_flag):
  old_flag = is_wan_interface_enabled()
  if old_flag == enable_flag:
    print("Nothing changed for wan interface")
    return

  try:
    cmdtool = CmdTool()
    if enable_flag:
      cmdtool.prepare(["uci", "set", "network.wan.disabled=0"])
      cmdtool.prepare(["uci", "set", "network.wan6.disabled=0"])
    else:
      cmdtool.prepare(["uci", "set", "network.wan.disabled=1"])
      cmdtool.prepare(["uci", "set", "network.wan6.disabled=1"])
    cmdtool.prepare(["uci", "commit", "network"])
    cmdtool.prepare(["luci-reload"])
    cmdtool.prepare(["/etc/init.d/network", "restart"])
    threading.Timer(0.5, lambda: cmdtool.start()).start()
  except:
    print("Got error when config wan interface")

# 数据流量接口是否开启
def is_sim_interface_enabled():
  try:
    cmd_output = subprocess.check_output(["uci", "get", "network.wwan_lte.disabled"]) # return bytes
    return cmd_output == b'0\n'
  except:
    return True

# 开启 / 关闭数据流量接口
def enable_sim_interface(enable_flag):
  old_flag = is_sim_interface_enabled()
  if old_flag == enable_flag:
    print("Nothing changed for sim interface")
    return

  try:
    cmdtool = CmdTool()
    if enable_flag:
      cmdtool.prepare(["uci", "set", "network.wwan_5g.disabled=0"])
      cmdtool.prepare(["uci", "set", "network.wwan_5g_v6.disabled=0"])
      cmdtool.prepare(["uci", "set", "network.wwan_lte.disabled=0"])
      cmdtool.prepare(["uci", "set", "network.wwan_lte_v6.disabled=0"])
    else:
      cmdtool.prepare(["uci", "set", "network.wwan_5g.disabled=1"])
      cmdtool.prepare(["uci", "set", "network.wwan_5g_v6.disabled=1"])
      cmdtool.prepare(["uci", "set", "network.wwan_lte.disabled=1"])
      cmdtool.prepare(["uci", "set", "network.wwan_lte_v6.disabled=1"])
    cmdtool.prepare(["uci", "commit", "network"])
    cmdtool.prepare(["luci-reload"])
    cmdtool.prepare(["/etc/init.d/network", "restart"])
    threading.Timer(0.5, lambda: cmdtool.start()).start()
  except:
    print("Got error when config sim interface")    

# Wi-Fi是否开启
def is_wifi_interface_enabled():
  try:
    cmd_output = subprocess.check_output(["uci", "get", "wireless.radio0.disabled"]) # return bytes
    return cmd_output == b'0\n'
  except:
    return True

# 开启 / 关闭数据流量接口
def enable_wifi_interface(enable_flag):
  old_flag = is_wifi_interface_enabled()
  if old_flag == enable_flag:
    print("Nothing changed for wifi interface")
    return

  try:
    cmdtool = CmdTool()
    if enable_flag:
      cmdtool.prepare(["uci", "set", "wireless.radio0.disabled=0"])
    else:
      cmdtool.prepare(["uci", "set", "wireless.radio0.disabled=1"])
    cmdtool.prepare(["uci", "commit", "wireless"])
    cmdtool.prepare(["luci-reload"])
    cmdtool.prepare(["/sbin/wifi", "reload"])
    threading.Timer(0.5, lambda: cmdtool.start()).start()
  except:
    print("Got error when config sim interface")  

def config_network_toggle(multi_wan_flag, wan_flag, sim_flag, wifi_flag):
  cmdtool = CmdTool()
  old_flag = is_mutil_wan_enabled()
  if old_flag != multi_wan_flag:  
    print("Set mutil wan toggle", multi_wan_flag)
    if multi_wan_flag:
      cmdtool.prepare(["ln", "-s" "/etc/config/mwan3-default", "/etc/config/mwan3-temp" ])
    else:
      cmdtool.prepare(["ln", "-s" "/etc/config/mwan3-off", "/etc/config/mwan3-temp" ])
    cmdtool.prepare(["mv", "/etc/config/mwan3-temp", "/etc/config/mwan3"])
  ##############################
  old_flag = is_wan_interface_enabled()
  if old_flag != wan_flag:
    print("Set wan_interface toggle", wan_flag)
    if wan_flag:
      cmdtool.prepare(["uci", "set", "network.wan.disabled=0"])
      cmdtool.prepare(["uci", "set", "network.wan6.disabled=0"])
    else:
      cmdtool.prepare(["uci", "set", "network.wan.disabled=1"])
      cmdtool.prepare(["uci", "set", "network.wan6.disabled=1"])
    cmdtool.prepare(["uci", "commit", "network"])
  ##############################
  old_flag = is_sim_interface_enabled()
  if old_flag != sim_flag:
    print("Set sim_interface toggle", sim_flag)
    if sim_flag:
      cmdtool.prepare(["uci", "set", "network.wwan_5g.disabled=0"])
      cmdtool.prepare(["uci", "set", "network.wwan_5g_v6.disabled=0"])
      cmdtool.prepare(["uci", "set", "network.wwan_lte.disabled=0"])
      cmdtool.prepare(["uci", "set", "network.wwan_lte_v6.disabled=0"])
    else:
      cmdtool.prepare(["uci", "set", "network.wwan_5g.disabled=1"])
      cmdtool.prepare(["uci", "set", "network.wwan_5g_v6.disabled=1"])
      cmdtool.prepare(["uci", "set", "network.wwan_lte.disabled=1"])
      cmdtool.prepare(["uci", "set", "network.wwan_lte_v6.disabled=1"])
    cmdtool.prepare(["uci", "commit", "network"])
  ###############################
  old_flag = is_wifi_interface_enabled()
  if old_flag != wifi_flag:
    print("Set wifi interface toggle", wifi_flag)
    if wifi_flag:
      cmdtool.prepare(["uci", "set", "wireless.radio0.disabled=0"])
    else:
      cmdtool.prepare(["uci", "set", "wireless.radio0.disabled=1"])
    cmdtool.prepare(["uci", "commit", "wireless"])
    cmdtool.prepare(["/sbin/wifi", "reload"])
  if cmdtool.commands_length() > 0:
    cmdtool.prepare(["luci-reload"])
    cmdtool.prepare(["/etc/init.d/network", "restart"])
  threading.Timer(0.2, lambda: cmdtool.start()).start()
  

# 本地包 (pcat开头的) 版本信息
def pcat_package_version_info():
  try:
    cmdout = subprocess.check_output("opkg list-installed | grep pcat", shell=True)
  except subprocess.CalledProcessError:
    print("Warning: opkg command not found!")
    return []

  cmdout_a = cmdout.split(b'\n')
  cmdout_a = [line.decode("utf-8") for line in cmdout_a if line != b'']
  return cmdout_a

# eg: b'pcat-manager_1.0.2-0_aarch64_cortex-a53.ipk\npcat-manager-web_1.0.2-0_aarch64_cortex-a53.ipk\n'
def remote_pcat_package_version_info():
  try:
    remote_version_info = requests.get(pcat_config.package_version_url).content
  except:
    print("Warning: Failed to get version info!")
    return []

  info_a = remote_version_info.split(b'\n')
  version_list = []
  for line in info_a:
    if line != b'':
      version = line.split(b'_')[1]
      version_list.append([line.decode("utf-8"), version.decode("utf-8")])
  print("Got remote version info", version_list)
  return version_list

class App (threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)

    # Clean temp directory everytime when bootup
    current_working_path = pathlib.Path(__file__).parent.resolve()
    save_dir_path = current_working_path.joinpath("temp")
    shutil.rmtree(save_dir_path, ignore_errors=True)

    self.board_info = self.get_board_info()
    # Patch for displaying kernel build date additionally for kernel version
    board_info = self.board_info
    board_info["kernel"] = board_info.get("kernel", "") + " " + subprocess.check_output(["uname", "-v"]).decode("utf-8")
    self.board_info = board_info
    self.tick_count = 0
    self.network_stats = network_stats.NetworkStats()
    self.net_download_speed = 0
    self.net_upload_speed = 0

  def run(self):
    print("App thread run.")
    while True:
      # 固件版本查询命令发送一次即可

      if self.tick_count % 3 == 0:
        if socket_client.stm32_firmware_version is None:
          socket_client.query_stm32_version() # Query stm32 firmware version

        if socket_client.stm32_firmware_exist():  
          socket_client.query_pmu_status()     # Query Battery working status
          socket_client.query_schedule_power_events() # Query schedule timer events
          socket_client.query_charger_on_auto_start() # Query charge boot mode
        socket_client.query_network_route_mode_status()
        socket_client.query_modem_status()

      if self.tick_count % 30 == 0:
        self.network_stats.log_stats()
      self.net_download_speed = self.network_stats.log_rx_speed()
      self.net_upload_speed = self.network_stats.log_tx_speed()
      self.tick_count += 1
      time.sleep(1)

  def get_board_info(self):
    """    
    return {'kernel': '4.19.193-photonicat', 'hostname': 'OpenWrt', 'system': 'ARMv8 Processor rev 0', 
      'model': 'Rockchip RK3568 photonicat Linux Board', 'board_name': 'rockchip,rk3568-photonicat', 
      'rootfs_type': 'squashfs', 'release': {'distribution': 'OpenWrt', 'version': '21.02', 
      'target': 'armvirt/64', 'revision': 'R21.8.6', 'description': 'OpenWrt '}}
    """

    try:
      cmd_output = subprocess.check_output(["ubus", "call", "system", "board"])
    except:
      cmd_output = "{}"
    return json.loads(cmd_output)

  def get_system_info(self):
    """
    return {'localtime': 1654875214, 'uptime': 160914, 'load': [8800, 16416, 19680], 
      'memory': {'total': 951328768, 'free': 581607424, 'shared': 8155136, 'buffered': 60932096, 
      'available': 757010432, 'cached': 136847360}, 'swap': {'total': 475000832, 'free': 475000832}}
    """
    try:
      cmd_output = subprocess.check_output(["ubus", "call", "system", "info"])
    except:
      cmd_output = "{}"  
    return json.loads(cmd_output)

  def get_clients(self):
    mock = False
    mock_clients_data = {'freq': 2457, 'clients': {'7c:03:ab:48:31:6c': {'auth': True, 'assoc': True, 'authorized': True, 'preauth': False, 'wds': False, 
      'wmm': True, 'ht': True, 'vht': False, 'he': False, 'wps': False, 'mfp': False, 'rrm': [0, 0, 0, 0, 0], 'aid': 2, 'bytes':
       {'rx': 22556457, 'tx': 318005089}, 'airtime': {'rx': 0, 'tx': 460871086}, 'packets': {'rx': 158290, 'tx': 245375}, 'rate': 
       {'rx': 1000, 'tx': 1000}, 'signal': -41, 'capabilities': {}}, 'e4:42:a6:56:4e:e7': {'auth': True, 'assoc': True, 'authorized': True, 
       'preauth': False, 'wds': False, 'wmm': True, 'ht': True, 'vht': False, 'he': False, 'wps': False, 'mfp': False, 'rrm': [0, 0, 0, 0, 0], 
       'aid': 1, 'bytes': {'rx': 4549039, 'tx': 120524910}, 'airtime': {'rx': 0, 'tx': 174426269}, 'packets': {'rx': 41293, 'tx': 91143}, 
       'rate': {'rx': 1000, 'tx': 1000}, 'signal': -49, 'capabilities': {}}}}
    try:
      cmd_output = subprocess.check_output(["ubus", "call", "hostapd.wlan0", "get_clients"])
    except:
      cmd_output = ""

    if mock:
      cmd_json = mock_clients_data
    else:      
      if cmd_output == "":
        return {}
      else:
        cmd_json = json.loads(cmd_output)

    print("cmd json", type(cmd_json), cmd_json)
    clients_mac = cmd_json["clients"].keys()
    print("clients_mac", clients_mac)

    dhcp_info = []
    dhch_leases_file = '/tmp/dhcp.leases'
    if mock:
      dhch_leases_file = "/tmp/dhcp_mock_data.txt"

    """
    1654879269 7c:03:ab:48:31:6c 172.16.0.177 RedmiNote7Pro-qichun 01:7c:03:ab:48:31:6c
    1654880275 e4:42:a6:56:4e:e7 172.16.0.178 c2h2hp1070 *
    """

    try:
      dhcp_file = open(dhch_leases_file, 'r')
      dhcp_info = dhcp_file.readlines()
      dhcp_file.close()
    except Exception as e:
      print("Failed to read /tmp/dhcp.leases", e)

    response_json = {}
    response_json["devices"] = []
    for client_mac in clients_mac:

      device = {}
      device["mac"] = client_mac
      for line_item in dhcp_info:
        print("line_item::::", line_item)
        host_info = line_item.split(" ")
        if len(host_info) < 4:
          break
        if host_info[1] == client_mac:
          device["ip"] = host_info[2]
          device["name"] = host_info[3]
          break
      response_json["devices"].append(device)

    return response_json
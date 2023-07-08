# @Author    : Qichunren

from flask import Flask, jsonify, render_template, request, redirect, session, make_response, \
    url_for, send_from_directory
from flask_socketio import SocketIO, emit
from datetime import datetime, date, timedelta
from user_auth import unix_user_auth
import subprocess
import threading
# import pyprctl # patch:set real thread name
import pathlib
import json
# import base64

import pcat_config
import app as pc_app
from cmd_tool import CmdTool
import os

install_thread = None
thread_lock = threading.Lock()

MINI_UI_CHANNEL_CONF_FILE_PATH = '/usr/local/ls-app-deploy-systemd/electric_monitor_conf.json'
MODBUS_CHANNEL_CONF_FILE_PATH = '/usr/local/ls-app-deploy-systemd/modbus.json'
ELECTRIC_MONITOR_DATA_TYPES = ["temp", "leakcurrent", "current"]


def background_install_thread(file_position, file_name):
    global install_thread
    current_path = pathlib.Path(__file__).parent.resolve()
    cmd = current_path.joinpath("opkg-install.py")  # test/cmd_output_test.sh

    if file_position == "remote":
        file_name = pcat_config.volatile_packages_url + file_name

    cmd_args = [cmd, "install", file_name]
    p = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, bufsize=1)
    while True:
        socketio.sleep(0.5)
        for line in iter(p.stdout.readline, b''):
            line_str = line.decode("utf-8")
            now = datetime.now()
            time_string = now.strftime("%H:%M:%S")
            socketio.emit('log_response', {'data': line_str, 'ts': time_string})
        p.stdout.close()
        break
    install_thread = None


class FlaskAppThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("Start web service on port", pcat_config.web_port)
        try:
            flask_app.run(host="0.0.0.0", port=pcat_config.web_port)
        except PermissionError as error:
            print("!!! Failed to start web service", error)


flask_app = Flask(__name__)

# $ python -c 'import secrets; print(secrets.token_hex())'
# '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
# flask_app.secret_key = b'j\tn\x8f\xe6\x8emU\xbfAJ\xd3\x11\xe6W4'
flask_app.config['SECRET_KEY'] = 'LKJ$J#LKJDO(IUJIWEEEWELKJV(*OXWDFSD11'
socketio = SocketIO(flask_app)


# Helper functions
def base_locales():
    if 'locale' not in session:
        current_locale = "CN"
    else:
        current_locale = session["locale"]
    if current_locale == "CN":
        locales = {
            "current_locale": current_locale,

            "common_login": "登录",
            "common_save": "保存",
            "common_enable": "启用",
            "common_disable": "禁用",
            "operation_tip": "操作提示",

            "nav_dashboard": "仪表盘",
            "nav_settings": "设置",
            "nav_statistics": "数据统计",
            "nav_update": "更新",
            "nav_reboot_device": "重启设备",
            "nav_logout": "退出后台",

            "remember_login_status": "记住登录状态",
            "advanced_setting_open_wrt": "高级设置 OpenWRT",

            "tab_timers": "开关机策略",
            "tab_advanced_settings": "高级设置",
            "no_wifi_info_config": "没有可以配置的WiFi信息"
        }
    else:
        locales = {
            "current_locale": current_locale,

            "common_login": "Login",
            "common_save": "Save",
            "common_enable": "Enable",
            "common_disable": "Disable",
            "operation_tip": "Operation tip",

            "nav_dashboard": "Dashboard",
            "nav_settings": "Settings",
            "nav_statistics": "Statistics",
            "nav_update": "Update",
            "nav_reboot_device": "Reboot",
            "nav_logout": "Logout",

            "remember_login_status": "Remember login status",
            "advanced_setting_open_wrt": "Advanced settings: OpenWRT",

            "tab_timers": "Timers",
            "tab_advanced_settings": "Advanced settings",
            "no_wifi_info_config": "No available WiFi configuration."
        }
    return locales


def current_locale():
    if 'locale' not in session:
        c_locale = "CN"
    else:
        c_locale = session["locale"]
    return c_locale


def login_required():
    if 'username' not in session:
        return redirect(url_for("login_action"))


def __load_channel_conf__():
    """Load config"""
    electric_channel_conf_json = {}
    modbus_channel_conf_json = {}

    if os.path.exists(MINI_UI_CHANNEL_CONF_FILE_PATH):
        with open(MINI_UI_CHANNEL_CONF_FILE_PATH) as file_mini_ui_conf_for_read:
            electric_channel_conf_json = json.load(file_mini_ui_conf_for_read)
    else:
        electric_channel_conf_json = {
            "scene_name": "Unknown",
            "id": "",
            "channels": []
        }

    if os.path.exists(MODBUS_CHANNEL_CONF_FILE_PATH):
        with open(MODBUS_CHANNEL_CONF_FILE_PATH) as file_modbus_conf_read:
            modbus_channel_conf_json = json.load(file_modbus_conf_read)
    else:
        modbus_channel_conf_json = {
            "report_data_interval_sec": 5,
            "alarm_play_duration_sec": 10,
            "bind_alarm_relay_id": "C1R.88",
            "uv_light_start_time": "21:00:00",
            "uv_light_end_time": "22:00:00",
            "bind_rm_sensor_id": ["RM.223", "RM.228"],
            "uv_light_mannual_ctrl_shield_sec": 1500,
            "ports": [
                {
                    "mode": "tcp",
                    "ip": "192.168.2.173",
                    "port": 502,
                    "slaves": [
                        {
                            "id": 1,
                            "addr_ranges": []
                        }
                    ],
                    "data_maps": []
                }
            ],
        }

    return electric_channel_conf_json, modbus_channel_conf_json


def find_ch_in_modbus_conf(name, data_maps):
    """Find modbus configs for a specified channel"""
    out_ch_conf = None

    for map_item in data_maps:
        if map_item["name"] == name:
            out_ch_conf = map_item
            break

    return out_ch_conf


def get_conf_for_user_from_modbus_conf(ch_conf_item):
    """Convert the modbus config info to the format that the end user needs"""
    try:
        key = ch_conf_item['key']
        dot_pos = key.find('.')
        at_pos = key.find('@')
        if dot_pos < 0 or at_pos < 0:
            return None

        channel_type = ''
        if ch_conf_item['name'].endswith('temp'):
            channel_type = 'temp'
        elif ch_conf_item['name'].endswith('current'):
            channel_type = 'current'
        elif ch_conf_item['name'].endswith('leakcurrent'):
            channel_type = 'leakcurrent'
        else:
            print('Failed to extracting channel conf from modbus conf: name field missing')
            return None

        slave_id = int(key[0:dot_pos])
        read_address = int(key[dot_pos+1:at_pos])
        func_code = int(key[at_pos+1:])

        calc_ratio = ch_conf_item['calc_ratio']   # The server decides this by itself
        info_trigger_range = ''
        info_trigger_duration = -1
        alarm_trigger_range = ''
        alarm_trigger_duration = -1

        if 'alarm_thresholds' in ch_conf_item:
            thresholds = ch_conf_item['alarm_thresholds']
            if 'info' in thresholds:
                info_threshold = thresholds['info']
                if info_threshold['floor'] > 0 and info_threshold['ceil'] > 0:
                    info_trigger_range = f"{info_threshold['floor']}-{info_threshold['ceil']}"
                elif info_threshold['floor'] < 0:
                    info_trigger_range = f"<{info_threshold['ceil']}"
                elif info_threshold['ceil'] < 0:
                    info_trigger_range = f">{info_threshold['floor']}"
                else:
                    info_trigger_range = ""

                info_trigger_duration = info_threshold['duration']

            if 'alarm' in thresholds:
                info_threshold = thresholds['alarm']
                if info_threshold['floor'] > 0 and info_threshold['ceil'] > 0:
                    alarm_trigger_range = f"{info_threshold['floor']}-{info_threshold['ceil']}"
                elif info_threshold['floor'] < 0:
                    alarm_trigger_range = f"<{info_threshold['ceil']}"
                elif info_threshold['ceil'] < 0:
                    alarm_trigger_range = f">{info_threshold['floor']}"
                else:
                    alarm_trigger_range = ""

                alarm_trigger_duration = info_threshold['duration']

        out_channel_conf_json = {
            f"ch_{channel_type}_read_address": read_address,
            f"ch_{channel_type}_func_code": func_code,
            f"ch_{channel_type}_calc_ratio": calc_ratio
        }

        if info_trigger_range != '':
            out_channel_conf_json[f"{channel_type}_info_trigger_range"] = info_trigger_range
            out_channel_conf_json[f"{channel_type}_info_trigger_duration"] = info_trigger_duration
        if alarm_trigger_range != '':
            out_channel_conf_json[f"{channel_type}_alarm_trigger_range"] = alarm_trigger_range
            out_channel_conf_json[f"{channel_type}_alarm_trigger_duration"] = alarm_trigger_duration
        return out_channel_conf_json

    except Exception as ex:
        message = 'Error occurred while extracting channel conf from modbus conf:' + \
                  str(ex.__class__) + ', ' + str(ex)
        print(message)
        return None


def merge_ranges(index, addr_ranges, which, func_code):
    """Trying to merge the current range at index into other ranges, which is either floor or ceil"""
    if index >= len(addr_ranges) or index < 0:
        return

    # Item to be merged must be in the form of "a-b"
    range_values = addr_ranges[index]["range"].split("-")
    if len(range_values) != 2:
        return

    to_merge_floor = int(range_values[0])
    to_merge_ceil = int(range_values[1])

    # Check if can be merged into one of other items, one by one
    merged = False
    for pos in range(0, len(addr_ranges)):
        if pos == index:
            continue

        if "-" not in addr_ranges[pos]["range"]:
            print("Check the single item")
            existing_range_single = int(addr_ranges[pos]["range"])

            if which == "floor":
                if existing_range_single == to_merge_floor -1 and func_code == addr_ranges[pos]["func"]:
                    addr_ranges[pos]["range"] = f"{existing_range_single}-{to_merge_ceil}"
                    merged = True
                    break

            if which == 'ceil':
                if existing_range_single == to_merge_ceil + 1 and func_code == addr_ranges[pos]["func"]:
                    addr_ranges[pos]["range"] = f"{to_merge_floor}-{existing_range_single}"
                    merged = True
                    break

        to_merge_range_values = addr_ranges[pos]["range"].split("-")
        existing_range_floor = int(to_merge_range_values[0])
        existing_range_ceil = int(to_merge_range_values[1])

        if which == 'floor':
            if to_merge_floor == existing_range_ceil + 1 and func_code == addr_ranges[pos]["func"]:
                print(f"Match a range for updated floor: {to_merge_floor}")
                addr_ranges[pos]["range"] = f"{existing_range_floor}-{to_merge_ceil}"
                merged = True
                break

        if which == 'ceil':
            if to_merge_ceil == existing_range_floor - 1 and func_code == addr_ranges[pos]["func"]:
                print(f"Match a range for updated ceil: {to_merge_ceil}")
                addr_ranges[pos]["range"] = f"{to_merge_floor}-{existing_range_ceil}"
                merged = True
                break

    if merged:
        del addr_ranges[index]


def add_new_read_address(address, add_ranges, func_code):
    """Add address into the list of ranges, merge continuous ones if necessary"""
    for index in range(0, len(add_ranges)):
        addr_range = add_ranges[index]["range"]

        if "-" not in addr_range:   # range: "2000"
            single_range_value = int(addr_range)

            if address == single_range_value - 1 and func_code == add_ranges[index]["func"]:
                add_ranges[index]["range"] = f"{address}-{single_range_value}"
                merge_ranges(index, add_ranges, "floor", func_code)
                return

            if address == single_range_value + 1 and func_code == add_ranges[index]["func"]:
                add_ranges[index]["range"] = f"{single_range_value}-{address}"
                merge_ranges(index, add_ranges, "ceil", func_code)
                return
            continue

        range_values = addr_range.split("-")
        if len(range_values) != 2:
            continue
        floor = int(range_values[0])
        ceil = int(range_values[1])

        if floor <= address <= ceil:
            print(f"The address {address} is already in one of ranges")
            return

        if address == (floor - 1):
            add_ranges[index]["range"] = f"{address}-{ceil}"
            merge_ranges(index, add_ranges, "floor", func_code)
            return

        if address == (ceil + 1):
            add_ranges[index]["range"] = f"{floor}-{address}"
            merge_ranges(index, add_ranges, "ceil", func_code)
            return

    # Not merged into existing range, just create a new one
    addr_range = {
        "range": f"{address}",
        "func": func_code
    }
    add_ranges.append(addr_range)


def get_data_map_item(key, data_type, channel_json):
    """Add data map item found in channel_json into data map list of modbus config"""
    # data_type: temp | leakcurrent | current
    temp_info_floor = 0
    temp_info_ceil = 0
    if "-" in channel_json[f"{data_type}_info_trigger_range"]:
        range_values = channel_json["temp_info_trigger_range"].split('-')
        temp_info_floor = int(range_values[0])
        temp_info_ceil = int(range_values[1])
    elif channel_json[f"{data_type}_info_trigger_range"].startswith(">"):
        temp_info_floor = int(channel_json["temp_info_trigger_range"][1:])
        temp_info_ceil = -1
    elif channel_json[f"{data_type}_info_trigger_range"].startswith("<"):
        temp_info_floor = -1
        temp_info_ceil = int(channel_json[f"{data_type}_info_trigger_range"][1:])
    else:
        print("Invalid range format in temp range")
        return

    temp_info_duration = channel_json[f"{data_type}_info_trigger_duration"]
    temp_info_err_ch = ""
    temp_info_turn_off = []

    temp_alarm_floor = 0
    temp_alarm_ceil = 0
    if "-" in channel_json[f"{data_type}_alarm_trigger_range"]:
        range_values = channel_json[f"{data_type}_alarm_trigger_range"].split('-')
        temp_alarm_floor = int(range_values[0])
        temp_alarm_ceil = int(range_values[1])
    elif channel_json[f"{data_type}_alarm_trigger_range"].startswith(">"):
        temp_alarm_floor = int(channel_json[f"{data_type}_alarm_trigger_range"][1:])
        temp_alarm_ceil = -1
    elif channel_json[f"{data_type}_alarm_trigger_range"].startswith("<"):
        temp_alarm_floor = -1
        temp_alarm_ceil = int(channel_json[f"{data_type}_alarm_trigger_range"][1:])
    else:
        print("Invalid range format in temp range")
        return

    temp_alarm_duration = channel_json[f"{data_type}_alarm_trigger_duration"]
    temp_alarm_err_ch = ""
    temp_alarm_turn_off = []

    channel_id = channel_json["id"]

    data_map_item = {
        "key": key,
        "calc_ratio": 10.0,
        "alarm_thresholds": {
            "info": {"floor": temp_info_floor, "ceil": temp_info_ceil, "duration": temp_info_duration,
                     "turn_off": temp_info_turn_off, "error_ch": temp_info_err_ch},
            "alarm": {"floor": temp_alarm_floor, "ceil": temp_alarm_ceil, "duration": temp_alarm_duration,
                      "turn_off": temp_alarm_turn_off, "error_ch": temp_alarm_err_ch}
        },
        "name": f"ch_{channel_id}_{data_type}"
    }

    return data_map_item


def add_new_channel(channel_json):
    """Add the new channel into the config file, ie., modbus.json and electric_monitor_conf.json"""
    electric_channel_conf_json = {}
    modbus_channel_conf_json = {}

    modbus_conf_json, modbus_channel_conf_json = __load_channel_conf__()

    # Append the new one
    new_channel_id = str(len(electric_channel_conf_json['channels']))
    electric_channel_conf_json['channels'].append({
        "id": new_channel_id,
        "name": channel_json['ch_name']
    })

    # read_range
    channel_id = channel_json["id"]
    for data_type in ELECTRIC_MONITOR_DATA_TYPES:
        if f"ch_{data_type}_read_address" in channel_json:
            address = channel_json[f"ch_{data_type}_read_address"]
            port = modbus_channel_conf_json["ports"][0]
            # slave = port["slaves"][0]
            func_code = 4
            # add_new_read_address(address=address, add_ranges=slave["addr_ranges"], func_code=func_code)

            key = f"1.{address}@{func_code}"
            data_map_item = get_data_map_item(key=key, data_type=data_type, channel_json=channel_json)
            port["data_maps"].append(data_map_item)

    with open(MINI_UI_CHANNEL_CONF_FILE_PATH, 'w') as file_mini_ui_conf_for_write:
        json.dump(electric_channel_conf_json, file_mini_ui_conf_for_write)
    with open(MODBUS_CHANNEL_CONF_FILE_PATH, 'w') as file_modbus_conf_write:
        json.dump(modbus_channel_conf_json, file_modbus_conf_write)


@socketio.event
def client_connected(message):
    emit('connected_response', {'data': 'Welcome\n'})


@socketio.event
def request_install(message):
    filename = message.get("filename")
    global install_thread
    with thread_lock:
        if install_thread is None:
            install_thread = socketio.start_background_task(background_install_thread, "local", filename)
    emit('log_response', {'data': "Start install {filename}\n".format(filename=filename)})


@socketio.event
def request_install_package(message):
    package = message.get("package")
    global install_thread
    with thread_lock:
        if install_thread is None:
            install_thread = socketio.start_background_task(background_install_thread, "remote", package)
    emit('log_response', {'data': "Start download {package}\n".format(package=package)})


@flask_app.route("/")
def home_action():
    if 'username' not in session:
        return redirect("/login")

    c_locale = current_locale()
    if c_locale == "CN":
        locales = {
            "card_main_status": "主要状态",
            "card_system": "系统",
            "card_connection": "连接",
            "card_hardware": "硬件",

            "connection": "连接",
            "dl_up_speed": "下载/上传速度",
            "uptime": "开机时长",

            "hostname": "主机名",
            "model": "型号",
            "architecture": "架构",
            "firmware_version": "固件版本",
            "kernel_version": "内核版本",

            "ip_address": "IP地址",
            "dhcp_clients": "DHCP 客户端",
            "wifi_clients": "Wi-Fi 客户端",
            "modem_mode": "网络模式",

            "battery_status": "电量",
            "battery_voltage": "电池电压",
            "charge_voltage": "充电电压",
            "board_temperature": "核心板温度",
            "sd_card": "SD卡",
            "sim_card": "SIM卡"
        }
    else:
        locales = {
            "card_main_status": "Main status",
            "card_system": "System",
            "card_connection": "Connection",
            "card_hardware": "Hardware",

            "connection": "Connection",
            "dl_up_speed": "Download/Upload Speed",
            "uptime": "Uptime",

            "hostname": "Hostname",
            "model": "Model",
            "architecture": "Architecture",
            "firmware_version": "Firmware Version",
            "kernel_version": "Kernel Version",

            "ip_address": "IP Address",
            "dhcp_clients": "DHCP Clients",
            "wifi_clients": "Wi-Fi Clients",
            "modem_mode": "Modem mode",

            "battery_status": "Battery Status",
            "battery_voltage": "Battery Voltage",
            "charge_voltage": "Charge Voltage",
            "board_temperature": "Board temperature",
            "sd_card": "SD Card",
            "sim_card": "SIM Card"
        }

    locales.update(base_locales())
    # render_template will look up index.html in templates dir.
    return render_template('index.html', locales=locales)


@flask_app.route('/ls-host-config', defaults={'path': ''})
@flask_app.route('/ls-host-config/<path:path>')
def host_config(path):
    if path != "" and os.path.exists(flask_app.static_folder + '/ls-host-config/' + path):
        return send_from_directory(flask_app.static_folder + '/ls-host-config', path)
    else:
        return send_from_directory(flask_app.static_folder + '/ls-host-config', 'index.html')


@flask_app.route("/switch_locale")
def switch_locale_action():
    c_locale = current_locale()

    if c_locale == "CN":
        session["locale"] = "EN"
    else:
        session["locale"] = "CN"
    return redirect("/")


@flask_app.route("/api/v1/dashboard.json", methods=['GET'])
def dashboard_json():
    dashboard = {
        "connection": pc_app.socket_client.network_route_mode,
        "server_location": "Unknown",
        "down_speed": pc_app.main_app.net_download_speed,
        "up_speed": pc_app.main_app.net_upload_speed,
        "uptime": subprocess.check_output(["uptime", "-p"]).decode("utf-8"),

        "hostname": pc_app.main_app.board_info.get("hostname"),
        "model": pc_app.main_app.board_info.get("model"),
        "kernel": pc_app.main_app.board_info.get("kernel"),
        "architecture": pc_app.main_app.board_info.get("board_name"),
        "firmware_version": pc_app.socket_client.stm32_firmware_version,

        "carrier": pc_app.socket_client.modem_mode,

        "on_charging": pc_app.socket_client.on_charging,
        "charge_percent": pc_app.socket_client.charge_percent,
        "voltage": pc_app.socket_client.battery_voltage,
        "charge_voltage": pc_app.socket_client.charger_voltage,
        "board_temperature": pc_app.socket_client.board_temperature,
        "sd_state": pc_app.sd_card_status(),
        "sim_state": pc_app.socket_client.sim_state,
    }
    rsp = make_response(dashboard)
    rsp.headers['Content-Type'] = 'application/json'
    return rsp


@flask_app.route("/api/v1/electric-configs/channels", methods=['GET', 'POST'])
def electric_conf_channels():
    resp_json = {}
    if request.method == 'GET':
        try:
            # If the first time configuration, just return 5 example channels
            if not os.path.exists(MINI_UI_CHANNEL_CONF_FILE_PATH):
                print("It's the first time to configure the channels, just return the template with 5 channels")
                resp_json = {
                    "is_succeed": True,
                    "message": "Ok",
                    "data": {
                        "channels": [
                            {
                                "id": 0,
                                "ch_name": '通道0',
                                "ch_temp_read_address": 2000,
                                "ch_leakcurrent_read_address": 3000,
                                "ch_current_read_address": 4000,
                                "current_allowed_range_max": 20,
                                "current_info_trigger_range": '10-20',
                                "current_info_trigger_duration": 30,
                                "current_alarm_trigger_range": '>20',
                                "current_alarm_trigger_duration": 30,
                                "temp_info_trigger_range": '32-40',
                                "temp_info_trigger_duration": 30,
                                "temp_alarm_trigger_range": '>40',
                                "temp_alarm_trigger_duration": 30
                            },
                            {
                                "id": 1,
                                "ch_name": '通道1',
                                "ch_temp_read_address": 2001,
                                "ch_leakcurrent_read_address": 3001,
                                "ch_current_read_address": 4001,
                                "current_allowed_range_max": 20,
                                "current_info_trigger_range": '10-20',
                                "current_info_trigger_duration": 30,
                                "current_alarm_trigger_range": '>20',
                                "current_alarm_trigger_duration": 30,
                                "temp_info_trigger_range": '32-40',
                                "temp_info_trigger_duration": 30,
                                "temp_alarm_trigger_range": '>40',
                                "temp_alarm_trigger_duration": 30
                            },
                            {
                                "id": 2,
                                "ch_name": '通道2',
                                "ch_temp_read_address": 2002,
                                "ch_leakcurrent_read_address": 3002,
                                "ch_current_read_address": 4002,
                                "current_allowed_range_max": 20,
                                "current_info_trigger_range": '10-20',
                                "current_info_trigger_duration": 30,
                                "current_alarm_trigger_range": '>20',
                                "current_alarm_trigger_duration": 30,
                                "temp_info_trigger_range": '32-40',
                                "temp_info_trigger_duration": 30,
                                "temp_alarm_trigger_range": '>40',
                                "temp_alarm_trigger_duration": 30
                            },
                            {
                                "id": 3,
                                "ch_name": '通道3',
                                "ch_temp_read_address": 2003,
                                "ch_leakcurrent_read_address": 3003,
                                "ch_current_read_address": 4003,
                                "current_allowed_range_max": 20,
                                "current_info_trigger_range": '10-20',
                                "current_info_trigger_duration": 30,
                                "current_alarm_trigger_range": '>20',
                                "current_alarm_trigger_duration": 30,
                                "temp_info_trigger_range": '32-40',
                                "temp_info_trigger_duration": 30,
                                "temp_alarm_trigger_range": '>40',
                                "temp_alarm_trigger_duration": 30
                            },
                            {
                                "id": 4,
                                "ch_name": '通道4',
                                "ch_temp_read_address": 2004,
                                "ch_leakcurrent_read_address": 3004,
                                "ch_current_read_address": 4004,
                                "current_allowed_range_max": 20,
                                "current_info_trigger_range": '10-20',
                                "current_info_trigger_duration": 30,
                                "current_alarm_trigger_range": '>20',
                                "current_alarm_trigger_duration": 30,
                                "temp_info_trigger_range": '32-40',
                                "temp_info_trigger_duration": 30,
                                "temp_alarm_trigger_range": '>40',
                                "temp_alarm_trigger_duration": 30
                            }
                        ],
                        "scene_name": "Unknown",
                        "scene_id": "fb17922233-7cc55f",
                    }
                }
                resp = make_response(resp_json)
                resp.headers['Content-Type'] = 'application/json'
                return resp

            electric_channel_conf_json, modbus_conf_json = __load_channel_conf__()

            resp_electric_channels = []
            channels_conf = electric_channel_conf_json.channels

            for channel_conf in channels_conf:
                # search the channel info associated with the given id,
                # get the read address of temp, current, leak current, and info & alarm threshold settings
                resp_channel = {
                    "id": channel_conf.id,
                    "ch_name": channel_conf.ch_name,
                }

                for data_type in ELECTRIC_MONITOR_DATA_TYPES:
                    found_ch_modbus_conf = find_ch_in_modbus_conf(f"ch_{channel_conf.id}_{data_type}",
                                                                  modbus_conf_json['ports'][0]['data_maps'])
                    end_user_channel_conf = get_conf_for_user_from_modbus_conf(found_ch_modbus_conf)
                    if end_user_channel_conf is not None:
                        resp_channel.update(end_user_channel_conf)

                resp_electric_channels.append(resp_channel)

            resp_json = {
                "is_succeed": True,
                "message": "Ok",
                "data": {
                    "channels": resp_electric_channels,
                    "scene_name": "Unknown",
                    "scene_id": "fb17922233-7cc55f",
                }
            }
        except Exception as ex:
            message = 'Error occurred while processing retrieve channels: ' + \
                      str(ex.__class__) + ', ' + str(ex)
            print(message)
            resp_json = make_response({
                "is_succeed": False,
                "message": message,
                "data": {}
            })
    elif request.method == 'POST':
        try:
            received_channel_conf_json = request.get_json()
            print("Received new channel:", received_channel_conf_json, type(received_channel_conf_json))
            add_new_channel(received_channel_conf_json)
            resp_json = {
                "is_succeed": True,
                "message": "Ok",
                "data": {}
            }
        except Exception as ex:
            message = 'Error occurred while add new channel: ' + \
                      str(ex.__class__) + ', ' + str(ex)
            print(message)
            resp_json = make_response({
                "is_succeed": False,
                "message": message,
                "data": {}
            })
    else:
        print('Unsupported method')

    resp = make_response(resp_json)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@flask_app.route("/api/v1/electric-configs/channels/<channel_id>", methods=['PUT'])
def update_electric_conf_channel(channel_id):
    resp_json = {
        "is_succeed": True,
        "message": f"Update channel with id {channel_id} succeed!",
        "data": {}
    }
    try:
        print(f"Trying to update the channel with id: {channel_id}")
        electric_channel_conf_json, modbus_conf_json = __load_channel_conf__()

        received_channel_conf_json = request.get_json()
        print("Received new channel:", received_channel_conf_json, type(received_channel_conf_json))

        # if there is already one channel with specified channel id
        mini_ui_channel_conf = electric_channel_conf_json["channels"]
        channel_found = False
        for index in range(0, len(mini_ui_channel_conf)):
            if mini_ui_channel_conf["id"] == channel_id:
                mini_ui_channel_conf["name"] = received_channel_conf_json["ch_name"]
                channel_found = True
                break

        if not channel_found:
            mini_ui_channel_conf.append({
                "id": channel_id,
                "name": received_channel_conf_json["ch_name"]
            })

        # modbus conf
        port = modbus_conf_json["ports"][0]
        slave = port["slaves"][0]
        modbus_addr_data_maps = port["data_maps"]
        channel_found = False

        # data_map
        for data_type in ELECTRIC_MONITOR_DATA_TYPES:
            data_map_item_name = f"ch_{channel_id}_{data_type}"
            func_code = 4 # get_func_code_from_data_type
            data_read_address = received_channel_conf_json[f"ch_{data_type}_read_address"]
            key = f"1.{data_read_address}@{func_code}"
            data_map_item = get_data_map_item(key=key, data_type=data_type, channel_json=received_channel_conf_json)
            for index in range(0, len(modbus_addr_data_maps)):
                if modbus_addr_data_maps[index]["name"] == data_map_item_name:
                    modbus_addr_data_maps[index] = data_map_item
                    channel_found = True
                    break
            if not channel_found:
                modbus_addr_data_maps.append(data_map_item)

        with open(MINI_UI_CHANNEL_CONF_FILE_PATH, 'w') as file_mini_ui_conf_for_write:
            json.dump(electric_channel_conf_json, file_mini_ui_conf_for_write)
        with open(MODBUS_CHANNEL_CONF_FILE_PATH, 'w') as file_modbus_conf_write:
            json.dump(modbus_conf_json, file_modbus_conf_write)
    except Exception as ex:
        message = f"Error occurred while updating the channel with id {channel_id}: {str(ex.__class__)}, {str(ex)}"
        print(message)
        resp_json = make_response({
            "is_succeed": False,
            "message": message,
            "data": {}
        })

    resp = make_response(resp_json)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@flask_app.route("/api/v1/electric-configs/channels/<channel_id>", methods=['DELETE'])
def delete_electric_conf_channel(channel_id):
    resp_json = {
        "is_succeed": True,
        "message": f"Delete channel with id {channel_id} succeed!",
        "data": {}
    }
    try:
        print(f"Trying to delete the channel with id: {channel_id}")
        electric_conf_json, modbus_conf_json = __load_channel_conf__()
        mini_ui_channel_conf = electric_conf_json["channels"]

        found_index = -1
        for index in range(0, len(mini_ui_channel_conf)):
            if mini_ui_channel_conf["channel_id"] == channel_id:
                found_index = index
                break

        if found_index >= 0:
            del(mini_ui_channel_conf[found_index])

        # data_map
        port = modbus_conf_json["ports"][0]
        modbus_addr_data_maps = port["data_maps"]
        for data_type in ELECTRIC_MONITOR_DATA_TYPES:
            data_map_item_name = f"ch_{channel_id}_{data_type}"
            found_index = -1
            for index in range(0, len(modbus_addr_data_maps)):
                if modbus_addr_data_maps[index]["name"] == data_map_item_name:
                    found_index = index
                    break

            if found_index >= 0:
                del(modbus_addr_data_maps[found_index])

        with open(MINI_UI_CHANNEL_CONF_FILE_PATH, 'w') as file_mini_ui_conf_for_write:
            json.dump(electric_conf_json, file_mini_ui_conf_for_write)
        with open(MODBUS_CHANNEL_CONF_FILE_PATH, 'w') as file_modbus_conf_write:
            json.dump(modbus_conf_json, file_modbus_conf_write)

    except Exception as ex:
        message = f"Error occurred while deleting the channel with id {channel_id}: {str(ex.__class__)}, {str(ex)}"
        print(message)
        resp_json = make_response({
            "is_succeed": False,
            "message": message,
            "data": {}
        })

    resp = make_response(resp_json)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@flask_app.route('/login', methods=['GET', 'POST'])
def login_action():
    error = None
    if request.method == 'POST':
        server_ts = int(datetime.now().timestamp())
        client_datetime = request.form.get('dtt')
        if client_datetime:
            ts_diff = server_ts - int(client_datetime) // 1000

        input_user_name = "root"  # request.form['username']
        input_user_password = request.form.get('password')
        if unix_user_auth(input_user_name, input_user_password):
            session['username'] = input_user_name
            if ts_diff > 63072000 or ts_diff < -63072000:  # 60 * 60 * 24 * 365 * 2 == 63072000, 2 years
                session.permanent = True
                flask_app.permanent_session_lifetime = timedelta(minutes=52560000)  # 60*24*365*100
            else:
                if request.form.get('remember_login'):
                    # session['remember_me'] = True
                    session.permanent = True
                    flask_app.permanent_session_lifetime = timedelta(minutes=1051210)  # 60*24*365*2
            return redirect("/")
        else:
            error = 'Invalid username/password'
    elif request.method == 'GET':
        if 'username' in session:
            return redirect("/")
    locales = {}
    locales.update(base_locales())
    return render_template('login.html', error=error, locales=locales)


@flask_app.route('/logout', methods=['GET', 'POST'])
def logout_action():
    if 'username' not in session:
        return redirect("/login")

    session.pop('username', None)
    return redirect("/login")


@flask_app.route("/settings")
def settings_action():
    if 'username' not in session:
        return redirect("/login")

    c_locale = current_locale()
    if c_locale == "CN":
        locales = {
            "wifi_encrp": "Wi-Fi 加密",
            "wifi_password": "Wi-Fi 密码",
            "wifi_frequency": "Wi-Fi 频段",
            "hide_wifi_ssid": "隐藏网络不被发现",
            "configuring_wifi_message": "设备正在重新加载配置信息，大约需要 10 秒钟 ...",
            "configuring_wifi_message2": "网络连接有可能断开。",

            "wifi_ssid_is_empty": "Wi-Fi SSID 不能为空",
            "wifi_ssid_too_long": "Wi-Fi SSID 长度不能太长",
            "wifi_password_is_empty": "Wi-Fi 密码不能为空",
            "wifi_password_at_least_8": "Wi-Fi 密码长度最少为8位",

            "no_encryption": "不加密"
        }
    else:
        locales = {
            "wifi_encrp": "Wi-Fi encryption",
            "wifi_password": "Wi-Fi password",
            "wifi_frequency": "Wi-Fi frequency",
            "hide_wifi_ssid": "Hide Wi-Fi SSID",
            "configuring_wifi_message": "Configuring Wi-Fi, please wait ...",
            "configuring_wifi_message2": "WiFi connections may be disconnected for a while",

            "wifi_ssid_is_empty": "Wi-Fi SSID is empty",
            "wifi_ssid_too_long": "Wi-Fi SSID too long",
            "wifi_password_is_empty": "Wi-Fi password is empty",
            "wifi_password_at_least_8": "Wi-Fi password length is at least 8 bits",

            "no_encryption": "No encryption"
        }

    locales.update(base_locales())
    stm32_firmware_exist = pc_app.socket_client.stm32_firmware_exist()
    return render_template('settings.html', stm32_firmware_exist=stm32_firmware_exist, locales=locales)


@flask_app.route("/timer")
def settings_timer_action():
    if 'username' not in session:
        return redirect("/login")

    c_locale = current_locale()
    if c_locale == "CN":
        locales = {
            "wifi_encrp": "Wi-Fi 加密",
            "wifi_password": "Wi-Fi 密码",
            "wifi_frequency": "Wi-Fi 频段",
            "hide_wifi_ssid": "隐藏网络不被发现",
            "configuring_wifi_message": "设备正在重新加载配置信息，大约需要 10 秒钟 ...",
            "configuring_wifi_message2": "网络连接有可能断开。",

            "wifi_ssid_is_empty": "Wi-Fi SSID 不能为空",
            "wifi_ssid_too_long": "Wi-Fi SSID 长度不能太长",
            "wifi_password_is_empty": "Wi-Fi 密码不能为空",
            "wifi_password_at_least_8": "Wi-Fi 密码长度最少为8位",

            "no_encryption": "不加密"
        }
    else:
        locales = {
            "wifi_encrp": "Wi-Fi encryption",
            "wifi_password": "Wi-Fi password",
            "wifi_frequency": "Wi-Fi frequency",
            "hide_wifi_ssid": "Hide Wi-Fi SSID",
            "configuring_wifi_message": "Configuring Wi-Fi, please wait ...",
            "configuring_wifi_message2": "WiFi connections may be disconnected for a while",

            "wifi_ssid_is_empty": "Wi-Fi SSID is empty",
            "wifi_ssid_too_long": "Wi-Fi SSID too long",
            "wifi_password_is_empty": "Wi-Fi password is empty",
            "wifi_password_at_least_8": "Wi-Fi password length is at least 8 bits",

            "no_encryption": "No encryption"
        }
    locales.update(base_locales())
    stm32_firmware_exist = pc_app.socket_client.stm32_firmware_exist()
    mode_page = "car_mode_page" if pc_app.socket_client.charger_on_auto_start_mode.get(
        "enabled") == 'true' else "timer_mode_page"
    return render_template('timer.html', stm32_firmware_exist=stm32_firmware_exist, mode_page=mode_page,
                           locales=locales)


@flask_app.route("/advanced_settings")
def advanced_settings_action():
    if 'username' not in session:
        return redirect("/login")

    c_locale = current_locale()
    if c_locale == "CN":
        locales = {
            "card_network_mode": "网络模式",
            "card_device_reset": "设备重置",

            "wan_interface": "WAN 接口",
            "sim_data": "数据流量",
            "wifi_service": "Wi-Fi 服务",
            "configuring_network": "正在配置网络，请稍候 ...",
            "device_reset": "设备重置",
            "are_you_sure_reset": "你确定要恢复出厂设置吗？",
            "resetting_device": "设备正在恢复出厂设置，请稍候 ...",
            "reset_help_text": "恢复出厂设置后，所有配置信息和数据全部重置到出厂时的状态"

        }
    else:
        locales = {
            "card_network_mode": "Network mode",
            "card_device_reset": "Device reset",

            "wan_interface": "WAN interface",
            "sim_data": "Mobile data",
            "wifi_service": "Wi-Fi service",
            "configuring_network": "Configuring network, please wait ...",
            "device_reset": "Device reset",
            "are_you_sure_reset": "Are you sure to reset your device?",
            "resetting_device": "Resetting device, please wait ...",
            "reset_help_text": "After device reset, all configurations  and data will reset to initial state"
        }
    locales.update(base_locales())
    stm32_firmware_exist = pc_app.socket_client.stm32_firmware_exist()
    return render_template('advanced_settings.html', stm32_firmware_exist=stm32_firmware_exist, locales=locales)


@flask_app.route("/statistics")
def statistics():
    login_required()

    c_locale = current_locale()
    if c_locale == "CN":
        locales = {
            "card_device_list": "设备列表",
            "card_traffic_stats": "移动流量统计",

            "mac_address": "MAC地址",
            "ip_address": "IP地址",
            "device_name": "设备名",

            "today_used": "今天使用",
            "week_used": "本周使用",
            "month_used": "本月使用",
            "last_month_used": "上月使用"

        }
    else:
        locales = {
            "card_device_list": "Device list",
            "card_traffic_stats": "Mobile traffic statistics",

            "mac_address": "MAC Address",
            "ip_address": "IP Address",
            "device_name": "Device name",

            "today_used": "Today used",
            "week_used": "Week used",
            "month_used": "Month used",
            "last_month_used": "Last month used"
        }
    locales.update(base_locales())
    return render_template('statistics.html', locales=locales)


@flask_app.route("/update")
def update_action():
    if 'username' not in session:
        return redirect("/login")

    info = pc_app.pcat_package_version_info()
    c_locale = current_locale()
    if c_locale == "CN":
        locales = {
            "card_ipk_update": "ipk 更新",
            "please_select_a_update_pkg": "请选择更新包",
            "upload": "上传",
            "help_text": "支持 ipk 格式的包, 或者gz、xz和 tar 格式的压缩包",
            "check_update": "检查更新", "no_package_info": "没有版本信息.", "update": "更新"}
    else:
        locales = {
            "card_ipk_update": "ipk update",
            "please_select_a_update_pkg": "Please select a package",
            "upload": "Upload",
            "help_text": "Support ipk package, or gz / xz / tar package.",
            "check_update": "Check update", "no_package_info": "No package info.", "update": "Update"}
    locales.update(base_locales())

    return render_template('update.html', info=info, locales=locales)


@flask_app.route("/about")
def about_action():
    if 'username' not in session:
        return redirect("/login")

    locales = {}
    locales.update(base_locales())
    return render_template('about.html', locales=locales)


@flask_app.route("/advanced_admin")
def advanced_admin_action():
    host_ip = request.host.split(':')[0]
    advanced_url = "http://" + host_ip + ":" + str(pcat_config.luci_port)
    return redirect(advanced_url)


@flask_app.route("/pkg_upload", methods=['POST'])
def pkg_upload_action():
    if 'username' not in session:
        rsp = make_response("{\"status\": \"failed\", \"message\": \"Login required\"}")
        rsp.headers['Content-Type'] = 'application/json'
        return rsp

    uploaded_file = request.files['package']
    filename = uploaded_file.filename

    if filename != '':
        current_working_path = pathlib.Path(__file__).parent.resolve()
        save_dir_path = current_working_path.joinpath("temp")
        try:
            pathlib.Path(save_dir_path).mkdir(parents=True, exist_ok=True)
        except:
            rsp = make_response("{\"status\": \"failed\", \"message\": \"Failed to create dir!\"}")
            rsp.headers['Content-Type'] = 'application/json'
            return rsp
        full_path = save_dir_path.joinpath(filename)
        try:
            uploaded_file.save(full_path)
        except:
            rsp = make_response("{\"status\": \"failed\", \"message\": \"Failed to save file!\"}")
            rsp.headers['Content-Type'] = 'application/json'
            return rsp

        rsp = make_response("{\"status\": \"ok\", \"message\": \"xxxx\", \"file_name\":\"" + str(full_path) + "\"}")
        rsp.headers['Content-Type'] = 'application/json'
        return rsp


@flask_app.route("/pkg_update", methods=['GET'])
def pkg_update_action():
    if 'username' not in session:
        rsp = make_response("{\"status\": \"failed\", \"message\": \"Login required\"}")
        rsp.headers['Content-Type'] = 'application/json'
        return rsp

    info = pc_app.remote_pcat_package_version_info()
    if len(info) == 0:
        json_text = jsonify({"versions": info, "status": "failed"})
    else:
        json_text = jsonify({"versions": info, "status": "ok"})
    rsp = make_response(json_text)
    rsp.headers['Content-Type'] = 'application/json'
    return rsp


@flask_app.route("/system/reboot", methods=['POST'])
def system_reboot():
    if 'username' not in session:
        return redirect("/login")

    threading.Timer(0.1, lambda: subprocess.run(["reboot"])).start()
    rsp = make_response("{\"status\": \"ok\"}")
    rsp.headers['Content-Type'] = 'application/json'
    return rsp


@flask_app.route("/system/reset", methods=['POST'])
def system_reset():
    if 'username' not in session:
        return redirect("/login")

    reset_file = pathlib.Path("/usr/bin/pcat-factory-reset.sh")
    if not reset_file.exists():
        rsp = make_response("{\"status\": \"failed\", \"message\": \"Feature missing.\"}")
        rsp.headers['Content-Type'] = 'application/json'
        return rsp

    threading.Timer(3.0, lambda: subprocess.run([str(reset_file)])).start()
    rsp = make_response("{\"status\": \"ok\"}")
    rsp.headers['Content-Type'] = 'application/json'
    return rsp


## JSON API acitons
@flask_app.route("/api/v1/status2.json")
def status2_json_action():
    if 'username' not in session:
        return redirect("/login")

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    date_string = now.strftime("%Y-%m-%d")
    time_string = now.strftime("%H:%M")

    return {
        "firmware_version": pc_app.socket_client.stm32_firmware_version,
        "on_charging": pc_app.socket_client.on_charging,
        "charge_percent": pc_app.socket_client.charge_percent,
        "date": date_string,
        "time": time_string,
        "carmode": pc_app.socket_client.charger_on_auto_start_mode
    }


@flask_app.route("/api/v1/status.json")
def status_json_action():
    if 'username' not in session:
        return redirect("/login")

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    return {
        "username": session['username'],
        "sdcard-status": pc_app.sd_card_status(),
        "pmu-status": pc_app.socket_client.get_pmu_status(),
        "modem-status": pc_app.socket_client.modem_status,
        "time": dt_string
    }


@flask_app.route("/api/v1/system/board.json")
def system_board_json_action():
    cmd_output = subprocess.check_output(["ubus", "call", "system", "board"])
    cmd_output = cmd_output.decode("utf-8")
    cmd_output = cmd_output.replace("\n\t", "")
    cmd_output = cmd_output.replace("\t", "")
    rsp = make_response(cmd_output)
    rsp.headers['Content-Type'] = 'application/json'
    return rsp


@flask_app.route("/api/v1/system/info.json")
def system_info_json_action():
    cmd_output = subprocess.check_output(["ubus", "call", "system", "info"])
    cmd_output = cmd_output.decode("utf-8")
    cmd_output = cmd_output.replace("\n\t", "")
    cmd_output = cmd_output.replace("\t", "")
    rsp = make_response(cmd_output)
    rsp.headers['Content-Type'] = 'application/json'
    return rsp


"""
root@OpenWrt:~# uci show wireless
wireless.radio0=wifi-device
wireless.radio0.type='mac80211'
wireless.radio0.path='platform/fe2c0000.dwmmc/mmc_host/mmc2/mmc2:0001/mmc2:0001:1'
wireless.radio0.country='US'
wireless.radio0.disabled='0'
wireless.radio0.legacy_rates='1'
wireless.radio0.mu_beamformer='0'
wireless.radio0.band='2g'
wireless.radio0.channel='10'
wireless.radio0.htmode='HT20'
wireless.default_radio0=wifi-iface
wireless.default_radio0.device='radio0'
wireless.default_radio0.network='lan'
wireless.default_radio0.mode='ap'
wireless.default_radio0.ssid='PhotoniCat-3B620768'
wireless.default_radio0.networn='lan'
wireless.default_radio0.encryption='psk2'
wireless.default_radio0.key='photonicat'
wireless.default_radio0.wps_pushbutton='0'
"""


@flask_app.route("/api/v1/wireless.json", methods=['GET'])
def wireless_action():
    json_dict = {}
    mock_data = False
    if mock_data:
        current_working_path = pathlib.Path(__file__).parent.resolve()
        fixture_file = current_working_path.joinpath("test", "fixture_wireless.txt")
        f = open(fixture_file, "rb")
        cmd_output = f.read()
        f.close()
    else:
        try:
            cmd_output = subprocess.check_output(["uci", "show", "wireless"])  # return bytes
        except:
            cmd_output = ""
    if cmd_output != "":
        cmd_output = cmd_output.decode("utf-8")
        if cmd_output.endswith("\n"):
            cmd_output = cmd_output[:-1]
        cmd_output_arr = cmd_output.split("\n")

        for item in cmd_output_arr:
            item_a = item.split("=")
            item_v = item_a[1]
            if item_v.startswith("'") and item_v.endswith("'"):
                item_v = item_v[1:-1]
            json_dict[item_a[0]] = item_v
    json_str = json.dumps(json_dict)
    rsp = make_response(json_str)
    rsp.headers['Content-Type'] = 'application/json'
    return rsp


@flask_app.route("/api/v1/wireless.json", methods=['POST'])
def save_wireless_action():
    if 'username' not in session:
        json_dict = {"status": "failed", "message": "Login required"}
    else:
        json_dict = {"status": "ok"}

    p_data = request.get_json()
    print("Get form info:", p_data, type(p_data))

    ssid = str(p_data.get("ssid") or "")
    frequency = str(p_data.get("frequency") or "")
    encryption = str(p_data.get("encryption") or "")
    ssid_key = str(p_data.get("password") or "")
    if not ssid:
        json_dict = {"status": "failed", "message": "Missing params."}
    elif frequency != "2g" and frequency != "5g":
        json_dict = {"status": "failed", "message": "Params invalid."}
    elif encryption != "none" and encryption != "psk" and encryption != "psk2":
        json_dict = {"status": "failed", "message": "Params invalid."}

    if json_dict["status"] == "ok":
        cmdtool = CmdTool()
        if p_data["frequency"] == "2g":
            cmdtool.prepare(["uci", "set", "wireless.radio0.band=2g"])
            cmdtool.prepare(["uci", "set", "wireless.radio0.htmode=HT20"])
            cmdtool.prepare(["uci", "set", "wireless.radio0.channel=10"])
        elif p_data["frequency"] == "5g":
            cmdtool.prepare(["uci", "set", "wireless.radio0.band=5g"])
            cmdtool.prepare(["uci", "set", "wireless.radio0.htmode=VHT40"])
            cmdtool.prepare(["uci", "set", "wireless.radio0.channel=36"])
        cmdtool.prepare(["uci", "set", "wireless.default_radio0.ssid=" + ssid])
        cmdtool.prepare(["uci", "set", "wireless.default_radio0.encryption=" + encryption])
        if p_data.get("password") != "":
            cmdtool.prepare(["uci", "set", "wireless.default_radio0.key=" + ssid_key])
        if p_data.get("hide_ssid") == True:
            cmdtool.prepare(["uci", "set", "wireless.default_radio0.hidden=1"])
        else:
            cmdtool.prepare(["uci", "delete", "wireless.default_radio0.hidden"])

        cmdtool.prepare(["uci", "commit", "wireless"])
        cmdtool.prepare(["luci-reload"])
        cmdtool.prepare(["/sbin/wifi", "reload"])
        threading.Timer(2.0, lambda: cmdtool.start()).start()

    json_str = json.dumps(json_dict)
    rsp = make_response(json_str)
    rsp.headers['Content-Type'] = 'application/json'
    return rsp


@flask_app.route("/api/v1/wifi_clients.json", methods=['GET'])
def wifi_clients_json_action():
    response_json = pc_app.main_app.get_clients()

    rsp = make_response(response_json)
    rsp.headers['Content-Type'] = 'application/json'
    return rsp


@flask_app.route("/api/v1/time.json", methods=['GET'])
def get_time_json_action():
    response_json = {}

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    date_string = now.strftime("%Y-%m-%d")
    time_string = now.strftime("%H:%M:%S")

    response_json["date_time"] = dt_string
    response_json["date"] = date_string
    response_json["time"] = time_string
    rsp = make_response(response_json)
    rsp.headers['Content-Type'] = 'application/json'
    return rsp


#  ubus -v list
#  ubus call system board
#  ubus call system info
#  ubus call system reboot

@flask_app.route("/api/v1/timers.json", methods=['GET'])
def get_timers_json_action():
    list_data = pc_app.socket_client.schedule_power_events()
    rsp = make_response(list_data)
    rsp.headers['Content-Type'] = 'application/json'
    return rsp


@flask_app.route("/api/v1/timers.json", methods=['POST'])
def save_timers_json_action():
    json_data = request.get_json()
    # [{'hour': 0, 'minute': 0, 'actiont': 'shutdown', 'days': [3, 5]},
    #  {'hour': 5, 'minute': 0, 'actiont': 'startup', 'days': [1, 2, 3, 4, 5, 6, 7]}] <class 'list'>
    print("Get timners info:", json_data, type(json_data))

    data_valid = True
    event_list = []
    for job_j in json_data:
        time_arr = job_j.get("time", "").split(":")
        if len(time_arr) != 2:
            data_valid = False
            break
        hour = int(time_arr[0])
        minute = int(time_arr[1])
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            data_valid = False
            break
        actiontype = job_j.get("action", "shutdown")
        days = job_j.get("days", [])
        if len(days) == 0:
            data_valid = False
            break
        days = [int(day) for day in days]

        action = 0 if actiontype == "shutdown" else 1  # startup
        enabled = 1
        enable_bits = 0  # See define in PCatManagerTimeEnableBits in pcat-manager-controller project
        enable_bits = enable_bits | (1 << 3)  # hour
        enable_bits = enable_bits | (1 << 4)  # minute
        enable_bits = enable_bits | (1 << 5)  # Day of week
        dow_bits = 0  # bit 0 -> weekend, bit 1 -> Monday
        if 0 in days:
            dow_bits = dow_bits | (1 << 0)
        if 1 in days:
            dow_bits = dow_bits | (1 << 1)
        if 2 in days:
            dow_bits = dow_bits | (1 << 2)
        if 3 in days:
            dow_bits = dow_bits | (1 << 3)
        if 4 in days:
            dow_bits = dow_bits | (1 << 4)
        if 5 in days:
            dow_bits = dow_bits | (1 << 5)
        if 6 in days:
            dow_bits = dow_bits | (1 << 6)
        event_job = {"action": action, "enabled": enabled, "enable-bits": enable_bits, "hour": hour, "minute": minute,
                     "dow-bits": dow_bits}
        event_list.append(event_job)
    if data_valid:
        pc_app.socket_client.set_schedule_power_events(event_list)

    response_json = {}
    response_json["status"] = "ok" if data_valid else "failed"
    rsp = make_response(response_json)
    rsp.headers['Content-Type'] = 'application/json'
    return rsp


@flask_app.route("/api/v1/carbootmode.json", methods=['POST'])
def save_carboot_mode_action():
    json_data = request.get_json()
    # print("============== Got json", json_data)
    state = json_data.get("carmode") == 'true'
    delay_timeout = int(json_data.get("timeout", 30))
    if delay_timeout < 0:
        delay_timeout = 0
    pc_app.socket_client.set_charger_on_auto_start(state, delay_timeout)

    response_json = {}
    response_json["status"] = "ok"
    rsp = make_response(response_json)
    rsp.headers['Content-Type'] = 'application/json'
    return rsp


@flask_app.route("/api/v1/network_interfaces.json", methods=['GET'])
def network_interfaces_api():
    multi_wan = pc_app.is_mutil_wan_enabled()
    wan_enabled = pc_app.is_wan_interface_enabled()
    sim_enabled = pc_app.is_sim_interface_enabled()
    wifi_enabled = pc_app.is_wifi_interface_enabled()

    response_json = {}
    response_json["multi_wan"] = multi_wan

    response_json["wan_enabled"] = wan_enabled
    response_json["sim_enabled"] = sim_enabled
    response_json["wifi_enabled"] = wifi_enabled

    rsp = make_response(response_json)
    rsp.headers['Content-Type'] = 'application/json'
    return rsp


@flask_app.route("/api/v1/network_interfaces.json", methods=['POST'])
def save_network_interfaces_api():
    json_data = request.get_json()
    multi_wan_flag = json_data.get("mutil_wan", False)
    # pc_app.enable_mutil_wan(multi_wan_flag)

    wan_flag = json_data.get("wan", False)
    # pc_app.enable_wan_interface(wan_flag)

    sim_flag = json_data.get("sim", False)
    # pc_app.enable_sim_interface(sim_flag)

    wifi_flag = json_data.get("wifi", False)
    # pc_app.enable_wifi_interface(wifi_flag)
    pc_app.config_network_toggle(multi_wan_flag, wan_flag, sim_flag, wifi_flag)

    response_json = {}
    response_json["status"] = "ok"
    rsp = make_response(response_json)
    rsp.headers['Content-Type'] = 'application/json'
    return rsp


@flask_app.route("/api/v1/data_stats.json", methods=['GET'])
def data_stats_api():
    response_json = {}
    response_json["today_used"] = pc_app.main_app.network_stats.today_bytes() or 0
    response_json["week_used"] = pc_app.main_app.network_stats.this_week_bytes() or 0
    response_json["month_used"] = pc_app.main_app.network_stats.month_bytes(date.today()) or 0
    response_json["last_month_used"] = pc_app.main_app.network_stats.month_bytes(date.today()) or 0
    rsp = make_response(response_json)
    rsp.headers['Content-Type'] = 'application/json'
    return rsp

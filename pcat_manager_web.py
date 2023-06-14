# @Author    : Qichunren

from flask import Flask, jsonify, render_template, request, redirect, session, make_response,\
    url_for, send_from_directory
from flask_socketio import SocketIO, emit
from datetime import datetime, date, timedelta
from user_auth import unix_user_auth
import subprocess
import threading
# import pyprctl # patch:set real thread name
import pathlib
import json
import base64

import pcat_config
import app as pc_app
from cmd_tool import CmdTool
import os

install_thread = None
thread_lock = threading.Lock()


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


## Helper functions

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

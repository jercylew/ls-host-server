# @Author    : Qichunren

import threading
# import pyprctl # patch:set real thread name
import socket
import select
import time
import queue
import json
import random


class PcSocketClient(threading.Thread):

    # 当固件设备不存在时，固件版本号为空字符
    def stm32_firmware_exist(self):
        if self.stm32_firmware_version == None or self.stm32_firmware_version == "":
            return False
        version_str = self.stm32_firmware_version[-3:-1]
        if version_str == '55':  # Home version
            return False
        elif self.stm32_firmware_version[-4:] == 'HOME':
            return False
        else:
            return True

    def __init__(self):
        threading.Thread.__init__(self)
        self.running_flag = False
        self.server_address = '/tmp/pcat-manager.sock'
        self.output_fds = []
        self.input_fds = []
        self.send_cmd_queue = queue.Queue()
        self.recv_buffer = b''
        self.sock = None
        self.sock_connected = False

        self.on_charging = False
        self.charge_percent = 100  # socket 返回的数据是 0-10000
        self.prev_charge_percent = None  # 上一次接收到的数值
        self.charge_percent_buf_queue = []
        self.battery_voltage = 4229  # 单位毫伏
        self.charger_voltage = 5035  # 单位毫伏
        self.board_temperature = None
        self.event_list = []  # Schedule event list

        # 根据充电器连接状态自动开关机（车载模式）
        self.charger_on_auto_start_mode = {"enabled": 'false', "timeout": 0, "countdown": 0}
        self.modem_status = {"mode": "none", "sim_state": "absent", "isp_name": "", "isp_lpmn": ""}
        self.modem_mode = "none"  # Modem状态，可能的值：none / 2g / 3g / lte / 5g
        self.sim_state = "absent"  # SIM卡状态，可能的值：absent / not-ready / ready / need-pin / need-puk / personalized-network / bad
        self.isp_name = ""  # 网络服务提供商名称
        self.isp_plmn = ""  # 网络服务提供商编号
        self.network_route_mode = "none"  # 路由模式，可能的值：none / wired / mobile / unknown
        self.stm32_firmware_version = None  # STM32固件版本号，默认不存在固件设备的话，为空字符串

    def get_pmu_status(self):
        return {"on_charging": self.on_charging, "charge_percent": self.charge_percent,
                "battery_voltage": self.battery_voltage,
                "charger_voltage": self.charger_voltage, "stm32_firmware_version": self.stm32_firmware_version,
                "route_mode": self.network_route_mode}

    def schedule_power_events(self):
        events = {}
        job_list = []
        # "event-list": [ { "enabled": 1, "enable-bits": 56, "action": 0, "year": 0, "month": 0, "day": 0, "hour": 0, "minute": 0, "dow-bits": 1 },
        #  { "enabled": 1, "enable-bits": 56, "action": 1, "year": 0, "month": 0, "day": 0, "hour": 5, "minute": 0, "dow-bits": 127 } ]
        for event_item in self.event_list:
            enabled_flag = event_item.get("enabled")
            enable_bits = event_item.get("enable-bits", 0)
            action = event_item.get("action")
            year = event_item.get("year")
            month = event_item.get("month")
            day = event_item.get("day")
            hour = event_item.get("hour")
            minute = event_item.get("minute")
            dow_bits = event_item.get("dow-bits", 0)
            job_item = {}
            days = []
            if (dow_bits & (1 << 0)) > 0:
                days.append(0)
            if (dow_bits & (1 << 1)) > 0:
                days.append(1)
            if (dow_bits & (1 << 2)) > 0:
                days.append(2)
            if (dow_bits & (1 << 3)) > 0:
                days.append(3)
            if (dow_bits & (1 << 4)) > 0:
                days.append(4)
            if (dow_bits & (1 << 5)) > 0:
                days.append(5)
            if (dow_bits & (1 << 6)) > 0:
                days.append(6)

            if (enable_bits & (1 << 0)) > 0:
                job_item["year"] = year
            if (enable_bits & (1 << 1)) > 0:
                job_item["month"] = month
            if (enable_bits & (1 << 2)) > 0:
                job_item["day"] = day
            if (enable_bits & (1 << 3)) > 0:
                job_item["hour"] = hour
            if (enable_bits & (1 << 4)) > 0:
                job_item["minute"] = minute
            if (enable_bits & (1 << 5)) > 0:
                job_item["days"] = days

            job_item["id"] = random.randint(0, 1000000)
            job_item["time"] = "{:0>2}:{:0>2}".format(hour, minute)
            job_item["hour"] = hour
            job_item["minute"] = minute
            job_item["action"] = "shutdown" if action == 0 else "startup"

            job_list.append(job_item)
        events["events"] = job_list
        return events

    def __handle_json_command(self, json_cmd):
        # print("Handle command:", json_cmd.get("command"))
        if json_cmd.get("command") == "pmu-status":
            # { "command": "pmu-status", "code": 0, "battery-voltage": 0, "charger-voltage": 0, "on-battery": 0, "charge-percentage": 0, "board-temperature" }
            if json_cmd.get("code") == 0:
                self.on_charging = json_cmd.get("on-battery") == 0  # on-battery 0 -> 表示充电，1 -> 表示没有插电源，在用电池的电
                percent = json_cmd.get("charge-percentage")
                if self.prev_charge_percent is None:
                    self.prev_charge_percent = percent

                self.board_temperature = json_cmd.get("board-temperature", -40)
                if self.board_temperature == -40:
                    self.board_temperature = None

                # 在充电状态下，要保证每一次接收到的充电百分比不能小于上一次的数值
                if (not self.on_charging) or (self.on_charging and percent >= self.prev_charge_percent):
                    if len(self.charge_percent_buf_queue) < 10:
                        self.charge_percent_buf_queue.append(percent)
                    else:
                        self.charge_percent_buf_queue.pop(0)
                        self.charge_percent_buf_queue.append(percent)
                    percent_sum = sum(self.charge_percent_buf_queue)
                    self.charge_percent = percent_sum // len(self.charge_percent_buf_queue) // 100  # 充电百分比

                self.prev_charge_percent = percent

                self.battery_voltage = json_cmd.get("battery-voltage")  # 单位毫伏 1000mv = 1v
                self.charger_voltage = json_cmd.get("charger-voltage")  # 单位毫伏
        elif json_cmd.get("command") == "pmu-fw-version-get":
            if json_cmd.get("code") == 0:
                self.stm32_firmware_version = json_cmd.get("version")
        elif json_cmd.get("command") == "schedule-power-event-get":
            if json_cmd.get("code") == 0:
                l = json_cmd.get("event-list")
                self.event_list = l
        elif json_cmd.get("command") == "charger-on-auto-start-get":
            if json_cmd.get("code") == 0:
                state = json_cmd.get("state")
                self.charger_on_auto_start_mode["enabled"] = 'true' if state == 1 else 'false'
                self.charger_on_auto_start_mode["timeout"] = json_cmd.get("timeout", 0)
                countdown = json_cmd.get("countdown", 0)
                self.charger_on_auto_start_mode["countdown"] = 0 if countdown <= 0 else countdown
        elif json_cmd.get("command") == "modem-status-get":
            if json_cmd.get("code") == 0:
                self.modem_status = {"mode": json_cmd.get("mode"), "sim_state": json_cmd.get("sim-state"),
                                     "isp_name": json_cmd.get("isp-name"), "isp_lpmn": json_cmd.get("isp-lpmn")}
                self.modem_mode = json_cmd.get("mode")
                self.sim_state = json_cmd.get("sim-state")
                self.isp_name = json_cmd.get("isp-name")
                self.isp_lpmn = json_cmd.get("isp-lpmn")
        elif json_cmd.get("command") == "network-route-mode-get":
            if json_cmd.get("code") == 0:
                self.network_route_mode = json_cmd.get("mode")

    def __handle_recv_buffer(self):
        end_flag_i = self.recv_buffer.index(b'\0')
        while end_flag_i >= 0 and len(self.recv_buffer) > 0:
            got_bytes = self.recv_buffer[:end_flag_i]
            # print("Process", got_bytes)
            try:
                cmd_json = json.loads(got_bytes)
                self.__handle_json_command(cmd_json)
            except Exception as e:
                print("Invalid recv cmd", e)
            self.recv_buffer = self.recv_buffer[(end_flag_i + 1):]
            if len(self.recv_buffer) > 0:
                end_flag_i = self.recv_buffer.index(b'\0')

    def query_pmu_status(self):
        if not self.sock or not self.sock_connected:
            # print("Failed to query pum status: Not connected to server!")
            return
        cmd = {"command": "pmu-status"}
        cmd_str = json.dumps(cmd)
        print("Add cmd data to queue", cmd_str)
        self.send_cmd_queue.put(cmd_str.encode() + b'\0')
        if self.sock not in self.output_fds:
            self.output_fds.append(self.sock)

    def query_modem_status(self):
        if not self.sock or not self.sock_connected:
            # print("Failed to query modem status: Not connected to server!")
            return
        cmd = {"command": "modem-status-get"}
        cmd_str = json.dumps(cmd)
        print("Add cmd data to queue", cmd_str)
        self.send_cmd_queue.put(cmd_str.encode() + b'\0')
        if self.sock not in self.output_fds:
            self.output_fds.append(self.sock)

    def query_network_route_mode_status(self):
        if not self.sock or not self.sock_connected:
            # print("Failed to query network route mode status: Not connected to server!")
            return
        cmd = {"command": "network-route-mode-get"}
        cmd_str = json.dumps(cmd)
        print("Add cmd data to queue", cmd_str)
        self.send_cmd_queue.put(cmd_str.encode() + b'\0')
        if self.sock not in self.output_fds:
            self.output_fds.append(self.sock)

    def query_schedule_power_events(self):
        if not self.sock or not self.sock_connected:
            print("Failed to query schedule power events: Not connected to server!")
            return
        cmd = {"command": "schedule-power-event-get"}
        cmd_str = json.dumps(cmd)
        print("Add timers cmd data to queue", cmd_str)
        self.send_cmd_queue.put(cmd_str.encode() + b'\0')
        if self.sock not in self.output_fds:
            self.output_fds.append(self.sock)

    # 查询当前是否启用车载模式
    def query_charger_on_auto_start(self):
        if not self.sock or not self.sock_connected:
            # print("Failed to query charger-on-auto-start-get: Not connected to server!")
            return
        cmd = {"command": "charger-on-auto-start-get"}
        cmd_str = json.dumps(cmd)
        print("Add cmd data to queue", cmd_str)
        self.send_cmd_queue.put(cmd_str.encode() + b'\0')
        if self.sock not in self.output_fds:
            self.output_fds.append(self.sock)

    def set_charger_on_auto_start(self, enable, delay_timeout):
        if not self.sock or not self.sock_connected:
            print("Failed to query charger-on-auto-start-set: Not connected to server!")
            return
        if enable:
            cmd = {"command": "charger-on-auto-start-set", "state": 1, "timeout": delay_timeout}
        else:
            cmd = {"command": "charger-on-auto-start-set", "state": 0, "timeout": delay_timeout}
        cmd_str = json.dumps(cmd)
        print("Add cmd data to queue", cmd_str)
        self.send_cmd_queue.put(cmd_str.encode() + b'\0')
        if self.sock not in self.output_fds:
            self.output_fds.append(self.sock)

    def query_stm32_version(self):
        if not self.sock or not self.sock_connected:
            # print("Failed to query stm32 version: Not connected to server!")
            return
        cmd = {"command": "pmu-fw-version-get"}
        cmd_str = json.dumps(cmd)
        print("Add cmd data to queue", cmd_str)
        self.send_cmd_queue.put(cmd_str.encode() + b'\0')
        if self.sock not in self.output_fds:
            self.output_fds.append(self.sock)

            # @param event_job : {"action":0,"enabled":1,"enable-bits":56,"hour":23,"minute":59,"dow-bits":1}

    # action: 0 -> poweroff; 1 -> bootup
    # enabled: 0 -> Disabled; 1 -> Enabled
    # year, month, day ignored
    # enable-bits: 8 bits: 0, day of week, minute, hour, day, month, year
    # dow-bites: Day of week repeat flag: 8 bits: 0b00000001 -> Repeat on weekend; 0b00000011 -> Repeat on weekend and Monday
    def set_schedule_power_events(self, event_job_list):
        if not self.sock or not self.sock_connected:
            # print("Failed to query schedule power events: Not connected to server!")
            return
        cmd = {"command": "schedule-power-event-set", "event-list": event_job_list}
        cmd_str = json.dumps(cmd)
        print("Add cmd data to queue", cmd_str)
        self.send_cmd_queue.put(cmd_str.encode() + b'\0')
        if self.sock not in self.output_fds:
            self.output_fds.append(self.sock)

    def connect_to_server(self):
        while self.running_flag:
            try:
                print("Try to connect to unix socket ctrl server.")
                self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.sock.setblocking(False)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.sock.connect(self.server_address)
            except Exception as e:
                self.sock_connected = False
                print("Failed to connect to unix socket ctrl server:", e)
                time.sleep(5)
                continue

            self.sock_connected = True
            print("Connected to unix socket ctrl server.\n")
            while True:
                # print("Select checking ....")
                self.input_fds = [self.sock]
                try:
                    ready_to_read, ready_to_write, in_error = \
                        select.select(self.input_fds, self.output_fds, [], 0.1)
                except select.error:
                    self.sock.shutdown(2)  # 0 = done receiving, 1 = done sending, 2 = both
                    self.sock.close()
                    # connection error event here, maybe reconnect
                    print("select error in unix socket connection")
                    break
                if len(ready_to_read) > 0:
                    recv_bytes = self.sock.recv(2048)
                    print(f"Recved data from unin socket ctrl server: {recv_bytes}")
                    self.recv_buffer = self.recv_buffer + recv_bytes
                    self.__handle_recv_buffer()
                if len(ready_to_write) > 0:
                    try:
                        next_msg = self.send_cmd_queue.get_nowait()  # 非阻塞获取
                        print("Ready to send data to unix socket server", next_msg)
                        self.sock.send(next_msg)
                        # print("Success sent data to unix socket ctrl server")
                    except queue.Empty:
                        self.output_fds.remove(self.sock)
                    except Exception as e:  # 发送的时候客户端关闭了则会出现 writable 和 readable 同时有数据，会出现 send_cmd_queue 的 keyerror
                        err_msg = "Send Data Error! ErrMsg:%s" % str(e)
                        print(err_msg)
                        if self.sock in self.output_fds:
                            self.output_fds.remove(self.sock)

    def run(self):
        print("PcSocketClient thread run.")
        self.running_flag = True
        self.connect_to_server()

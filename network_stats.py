import os
from datetime import datetime, date, timedelta

from database import connect_db, get_rows

# device: usb0 -> 5G
# device: wwan0 -> 4G
# direction: rx or tx
def get_device_x_bytes(device, direction):
  device_path = "/sys/class/net/{0}/statistics/{1}_bytes".format(device, direction)
  file_exists = os.path.exists(device_path)
  if not file_exists:
    # print("Warning: device {} not exist".format(device))
    return 0
  f = open(device_path)
  value_str = f.readline().strip()
  f.close()
  if len(value_str) > 0:
    final_value = 0
    try:
      final_value = int(value_str)
    except:
      print("Warning: device {0} {1}_bytes invalid!".format(device))
    return final_value
  else:
    print("Warning: device {0} {1}_bytes empty!".format(device))
    return 0
  
class NetworkStats:

  def __init__(self):
    connect_db("/etc/net_stats.db")
    self.last_log_rx_speed = None
    self.last_log_tx_speed = None
    self.last_rx_bytes = None
    self.last_tx_bytes = None
    if os.path.exists("/sys/class/net/wwan0/statistics"):
      self.mode = "3G/4G"
    elif os.path.exists("/sys/class/net/usb0/statistics"):
      self.mode = "5G"
    else:
      self.mode = None

    if os.path.exists("/tmp/pcat-manager-web-bootup"):
      self.device_bootup = False
    else:
      f = open("/tmp/pcat-manager-web-bootup", "w")
      f.close()
      self.device_bootup = True

  def log_rx_speed(self):
    bytes_0 = get_device_x_bytes("eth0", "rx")
    bytes_1 = get_device_x_bytes("usb0", "rx")
    bytes_2 = get_device_x_bytes("wwan0", "rx")
    if self.last_log_rx_speed is None:
      speed = bytes_0 + bytes_1 + bytes_2
      self.last_log_rx_speed = speed
      return 0
    else:
      speed_0 = bytes_0 + bytes_1 + bytes_2
      speed = speed_0 - self.last_log_rx_speed
      self.last_log_rx_speed = speed_0
      return speed

  def log_tx_speed(self):
    bytes_0 = get_device_x_bytes("eth0", "tx")
    bytes_1 = get_device_x_bytes("usb0", "tx")
    bytes_2 = get_device_x_bytes("wwan0", "tx")
    if self.last_log_tx_speed is None:
      speed = bytes_0 + bytes_1 + bytes_2
      self.last_log_tx_speed = speed
      return 0
    else:
      speed_0 = bytes_0 + bytes_1 + bytes_2
      speed = speed_0 - self.last_log_tx_speed
      self.last_log_tx_speed = speed_0
      return speed  

  def log_stats(self):
    if self.mode is None:
      return
    if self.mode == "5G":
      device = "usb0"
    elif self.mode == "3G/4G":
      device = "wwan0"
    self.log_net_device_bytes(device, "")

  def log_net_device_bytes(self, device, remark = ""):
    now = datetime.now()
    time_string = now.strftime("%Y-%m-%d %H:%M:%S")
    rx_bytes = get_device_x_bytes(device, "rx")
    tx_bytes = get_device_x_bytes(device, "tx")
    if self.last_rx_bytes is not None:
      rx_bytes = rx_bytes - self.last_rx_bytes
    if self.last_tx_bytes is not None:
      tx_bytes = tx_bytes - self.last_tx_bytes

    sql_command = "insert into network_stats(rx_bytes,tx_bytes,device,remark,created_at)values({0},{1},'{2}','{3}','{4}')".format(rx_bytes, tx_bytes, device, remark, time_string)
    connect_db("/etc/net_stats.db", [sql_command])
    self.last_rx_bytes = rx_bytes
    self.last_tx_bytes = tx_bytes

  def today_bytes(self):
    now = datetime.now()
    time_string = now.strftime("%Y-%m-%d 00:00:00")
    sql_command = "select sum(rx_bytes),sum(tx_bytes) from network_stats where created_at >= '{0}'".format(time_string)
    rows = get_rows("/etc/net_stats.db", sql_command)
    if len(rows) > 0:
      a = rows[0][0]
      b = rows[0][1]
      if a is None:
        a = 0
      if b is None:
        b = 0
      return a + b

  def this_week_bytes(self):
    today = date.today()
    start_day = today - timedelta(days=today.weekday())
    end_day = start_day + timedelta(days=6)
    start_ts = start_day.strftime("%Y-%m-%d 00:00:00")
    end_ts = end_day.strftime("%Y-%m-%d 23:59:59")
    sql_command = "select sum(rx_bytes),sum(tx_bytes) from network_stats where created_at >= '{0}' and created_at <= '{1}'".format(start_ts, end_ts)
    rows = get_rows("/etc/net_stats.db", sql_command)
    if len(rows) > 0:
      a = rows[0][0]
      b = rows[0][1]
      if a is None:
        a = 0
      if b is None:
        b = 0
      return a + b

  def month_bytes(self, month_date):
    start_day = month_date.replace(day=1)
    start_ts = start_day.strftime("%Y-%m-%d 00:00:00")

    next_month = month_date.replace(day=28) + timedelta(days=4)
    end_day = next_month - timedelta(days=next_month.day)
    end_ts = end_day.strftime("%Y-%m-%d 23:59:59")

    sql_command = "select sum(rx_bytes),sum(tx_bytes) from network_stats where created_at >= '{0}' and created_at <= '{1}'".format(start_ts, end_ts)
    print(sql_command)
    rows = get_rows("/etc/net_stats.db", sql_command)
    if len(rows) > 0:
      a = rows[0][0]
      b = rows[0][1]
      if a is None:
        a = 0
      if b is None:
        b = 0
      return a + b

## For self test
if __name__ == "__main__":
  a1 = get_device_x_bytes("enp0s9", "rx")
  a2 = get_device_x_bytes("enp0s9", "tx")
  print("enp0s9 rx_bytes", a1, "and tx bytes", a2)
  network_stat = NetworkStats()
  print("Is first bootup?", network_stat.device_bootup)
  a = network_stat.today_bytes()
  print(a)
  a = network_stat.this_week_bytes()
  print(a)
  six_m = datetime(2022, 6, 17)
  five_m = datetime(2022, 5, 17)
  a = network_stat.month_bytes(six_m)
  print(a)
  a = network_stat.month_bytes(five_m)
  print(a)




import sqlite3
import os
import re

# ls /sys/class/net/
# bond0 eth0 ipsec0 wan0 wwan0 usb0
# bonding_masters eth1 lo br-lan ip6tnl0 tunl0

# /sys/class/net/wlan0/statistics/rx_bytes
# /sys/class/net/wlan0/statistics/tx_bytes

# python3 sqlite3 doc: https://docs.python.org/3/library/sqlite3.html

SQL = '''
CREATE TABLE network_stats(
  id INTEGER PRIMARY KEY,
  rx_bytes INTEGER,
  tx_bytes INTEGER,
  device VARCHAR(10),
  remark VARCHAR(30),
  created_at DATETIME NOT NULL
);
'''

def connect_db(db_path, commands = []):
  file_exists = os.path.exists(db_path)
  con = None
  try:
    con = sqlite3.connect(db_path)
  except sqlite3.OperationalError:
    if file_exists:
      print("sqlite3.OperationalError, failed to read " + db_path)
      os.remove(db_path)
      con = sqlite3.connect(db_path)
    else:
      print("sqlite3.OperationalError, failed to create " + db_path)
  finally:
    if con is None:
      return False
    
  cur = con.cursor()
  if not file_exists:
    print("Db file not exist.")
    lines = SQL.strip().split(";")
    # print("raw ", lines)
    s_commands = []
    for line in lines:
      command = re.sub(r'\n+\s*', '', line)
      command = re.sub(r'\s+', ' ', command)
      if len(command) > 0:
        s_commands.append(command)
    # print("sqlite command:", sqlite_commands)
    for sqlite_command in s_commands:
      print("Exec:", sqlite_command)
      cur.execute(sqlite_command)
    if len(s_commands) > 0:
      con.commit()
  if len(commands) > 0:
    for sqlite_command in commands:
      print("Exec:", sqlite_command)
      cur.execute(sqlite_command)
      con.commit()
  con.close()
  return True

def get_rows(db_path, select_cmd):
  file_exists = os.path.exists(db_path)
  con = None
  try:
    con = sqlite3.connect(db_path)
  except sqlite3.OperationalError:
    if file_exists:
      print("sqlite3.OperationalError, failed to read " + db_path)
      os.remove(db_path)
      con = sqlite3.connect(db_path)
    else:
      print("sqlite3.OperationalError, failed to create " + db_path)
  finally:
    if con is None:
      return []
    
  cur = con.cursor()
  rows = []
  for row in cur.execute(select_cmd):
    rows.append(row)
  con.close()
  return rows
import threading
# import pyprctl # patch:set real thread name
import socket
import select
import time
import queue
import json
import random


class UiSocketClient:
    def __init__(self, address, port):
        self.server_address = (address, port)
        self.sock = None

    def send_command(self, cmd_payload):
        if self.sock is None:
            return

        self.sock.sendall(cmd_payload.encode())

    def connect_to_server(self):
        try:
            print("Try to connect to mini ui server.")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setblocking(False)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.connect(self.server_address)
        except Exception as e:
            self.sock = None
            print("Failed to connect to ui server:", e)
            time.sleep(5)

    def disconnect(self):
        try:
            if self.sock is None:
                return

            self.sock.close()
            print("Disconnected from server")
        except Exception as e:
            print("Failed to disconnect from server:", e)

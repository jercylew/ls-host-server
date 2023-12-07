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

    # def is_connected(self):
    #     if self.sock is None:
    #         return False
    #
    #     try:
    #         self.sock.send(b'ping\n')
    #         data = self.sock.recv(1024)
    #         return True
    #     except (socket.error, ConnectionResetError):
    #         print('Socket connection is lost')
    #         return False

    def send_command(self, cmd_payload):
        try:
            self.sock.sendall(cmd_payload.encode())
        except Exception as ex:
            print(f"Failed to connect to ui server: ${ex}, try to reconnect to server")
            self.connect_to_server()

            if self.sock is None:
                return

            self.sock.sendall(cmd_payload.encode())

    def connect_to_server(self):
        try:
            print("Trying to connect to mini ui server...")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setblocking(False)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.connect(self.server_address)
            print("Connect to mini ui server succeed")
        except Exception as e:
            self.sock = None
            print("Failed to connect to ui server:", e)

    def disconnect(self):
        try:
            if self.sock is None:
                return

            self.sock.close()
            print("Disconnected from server")
        except Exception as e:
            print("Failed to disconnect from server:", e)

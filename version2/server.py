#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

#! ##### WARNING: #####
#! The server judge will execute files submitted by users.
#! If those files contain malicious code, your system may be messed up.
#! At the time of this writing, there is nothing to prevent this.
#! Use at your own risk
#! The GPL license does not provide any warranty, and the author(s) of this project
#! shall not be held responsible from any damage directly or indirectly caused by it.
#! You can consider running the server on a user who does not have access to any valuable files.

import os
import subprocess
import string
import random
import socket
import threading
import pickle
import json
import colorama
from colorama import Fore
from hashlib import sha256
colorama.init()


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))

        self.clients = []

    def start(self):
        self.server.listen()
        print(f"{Fore.GREEN}Server started on {self.ip}{Fore.RESET}")

        while True:
            conn, addr = self.server.accept()
            client = Client(conn, addr)
            self.clients.append(client)


class Client:
    header = 64
    padding = " " * header
    packet_size = 1024

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr

        self.alert("INFO", "Connected")
        self.auth()
        threading.Thread(target=self.start).start()

    def auth(self):
        chars = bytes(range(256))
        task = b"".join(random.choices([chars[i:i+1] for i in range(len(chars))], k=64))
        answer = sha256(task).hexdigest()
        self.send({"type": "auth", "task": task})
        reply = self.recv()["answer"]
        if answer == reply:
            self.alert("INFO", "Authenticated")
        else:
            self.alert("ERROR", "Authentication failed")
            self.conn.close()

    def start(self):
        while True:
            msg = self.recv()

            if msg["type"] == "quit":
                self.conn.close()
                self.alert("INFO", "Disconnected")
                return

    def alert(self, type, msg):
        color = Fore.RESET
        if type == "INFO":
            color = Fore.CYAN
        elif type == "WARNING":
            color = Fore.YELLOW
        elif type == "ERROR":
            color = Fore.RED

        print(f"{color}[{self.addr}] {msg}{Fore.RESET}")

    def send(self, obj):
        data = pickle.dumps(obj)
        len_msg = (str(len(data)) + self.padding)[:self.header].encode()

        packets = []
        while data:
            curr_len = min(len(data), self.packet_size)
            packets.append(data[:curr_len])
            data = data[curr_len:]

        self.conn.send(len_msg)
        for packet in packets:
            self.conn.send(packet)

    def recv(self):
        len_msg = b""
        while len(len_msg) < self.header:
            len_msg += self.conn.recv(self.header-len(len_msg))

        length = int(len_msg)
        data = b""
        while len(data) < length:
            curr_len = min(self.packet_size, length-len(data))
            data += self.conn.recv(curr_len)

        return pickle.loads(data)


def main():
    if os.path.isfile("settings.json"):
        with open("settings.json", "r") as file:
            data = json.load(file)
            ip = data["ip"]
    else:
        ip = input("IP: ")

    server = Server(ip, 5555)
    server.start()


main()

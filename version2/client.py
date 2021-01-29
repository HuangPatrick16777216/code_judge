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

import os
import socket
import pickle
import json
from hashlib import sha256
from tkinter import Tk
from tkinter.filedialog import askopenfilename
Tk().withdraw()


class Client:
    header = 64
    padding = " " * header
    packet_size = 1024

    def __init__(self, ip, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))
        self.auth()

    def auth(self):
        task = self.recv()["task"]
        ans = sha256(task).hexdigest()
        self.send({"type": "auth", "answer": ans})

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

    conn = Client(ip, 5555)

    while True:
        print("s: submit a solution")
        print("q: quit")
        action = input("Action: ")

        if action == "q":
            conn.send({"type": "quit"})
            return

        elif action == "s":
            print()
            print("1: Python 3.8.0")
            print("2: Python 2.7.17")
            print("3: C++ (g++ 7.5.0)")
            lang = int(input("Language: "))
            pid = int(input("Problem ID: "))
            path = askopenfilename()

            if os.path.isfile(path):
                with open(path, "r") as file:
                    code = file.read()

                data = {
                    "type": "submit",
                    "lang": lang,
                    "pid": pid,
                    "code": code,
                }
                conn.send(data)

                reply = conn.recv()
                print()
                if reply["status"]:
                    print("The server is grading your submission.")
                else:
                    print("The server sent an error: "+reply["error"])


main()
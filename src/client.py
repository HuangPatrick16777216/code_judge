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

import sys
import os
import socket
import pickle
import json
import colorama
from colorama import Fore
from hashlib import sha256
from tkinter import Tk
from tkinter.filedialog import askopenfilename
Tk().withdraw()
colorama.init()


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


def clearline():
    sys.stdout.write("\r")
    sys.stdout.write(" "*80)
    sys.stdout.write("\r")


def main():
    if os.path.isfile("settings.json"):
        with open("settings.json", "r") as file:
            data = json.load(file)
            ip = data["ip"]
    else:
        ip = input("IP: ")

    conn = Client(ip, 5555)
    if sys.platform == "linux":
        clear = lambda: os.system("clear")
    elif sys.platform == "windows":
        clear = lambda: os.system("cls")
    else:
        clear = lambda: None

    while True:
        clear()
        print("s: submit a solution")
        print("q: quit")
        action = input("Action: ")

        if action == "q":
            conn.send({"type": "quit"})
            return

        elif action == "s":
            clear()
            print("1: Python 3.8.0")
            print("2: Python 2.7.17")
            print("3: C++ (g++ 7.5.0)")
            lang = int(input("Language: "))

            clear()
            conn.send({"type": "get_problems"})
            problems = conn.recv()
            print("ID: Name, Difficulty, Number of cases")
            for pid, name, difficult, num_cases in problems:
                print(f"{pid}: {name}, {difficult}, {num_cases}")
            pid = int(input("Problem ID: "))

            path = askopenfilename()
            if path and os.path.isfile(path):
                with open(path, "r") as file:
                    code = file.read()

                conn.send({"type": "submit", "lang": lang, "pid": pid, "code": code})
                reply = conn.recv()
                if reply["status"]:
                    clear()
                    sys.stdout.write("Your submission is in the server queue and will be graded shortly.")
                    sys.stdout.flush()
                    num_cases = conn.recv()["num_cases"]
                    results = []

                    errored = False
                    for i in range(num_cases):
                        clearline()
                        sys.stdout.write(f"Grading case {i+1} of {num_cases}...")
                        sys.stdout.flush()
                        curr_result = conn.recv()
                        results.append(curr_result)
                        if curr_result["result"] == "!" and i == 0:
                            clearline()
                            print("Error when grading case 1:")
                            print(curr_result["error"])
                            input("Press enter to clear.")
                            errored = True
                            break
                    if errored:
                        continue

                    clearline()
                    sys.stdout.write("Grading finished. Results are below.\n")
                    sys.stdout.write("* = correct\n")
                    sys.stdout.write("x = wrong\n")
                    sys.stdout.write("! = runtime error\n")
                    sys.stdout.write("t = time limit exceeded (3 seconds)\n")
                    for i in range(num_cases):
                        sys.stdout.write("+-------")
                    sys.stdout.write("+\n")
                    for result in results:
                        symbol = result["result"]
                        color = Fore.GREEN if symbol == "*" else Fore.RED
                        sys.stdout.write(f"|   {color}{symbol}{Fore.RESET}   ")
                    sys.stdout.write("|\n")
                    for result in results:
                        sys.stdout.write("|")
                        if result["result"] == "*":
                            elapse = str(int(result["elapse"]*1000)) + " ms"
                            offset = int((7-len(elapse)) / 2)
                            sys.stdout.write(" "*offset)
                            sys.stdout.write(elapse)
                            sys.stdout.write(" "*(7-offset-len(elapse)))
                        else:
                            sys.stdout.write("       ")
                    sys.stdout.write("|\n")
                    for i in range(num_cases):
                        sys.stdout.write("+-------")
                    sys.stdout.write("+\n")
                    sys.stdout.flush()
                    input("Press enter to clear.")

                else:
                    print("The server sent an error: "+reply["error"])
                    input("Press enter to continue.")


main()

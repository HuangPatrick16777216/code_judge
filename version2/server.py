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
#! At the time of this writing, there is no code to check for this.
#! Use at your own risk
#! The GPL license does not provide any warranty, and the author(s) of this project
#! shall not be held responsible from any damage directly or indirectly caused by it.
#! You can consider running the server on a user who does not have access to any valuable files.

import os
import time
import subprocess
import random
import socket
import threading
import pickle
import json
import colorama
from colorama import Fore
from hashlib import sha256
from datetime import datetime
colorama.init()


class Server:
    def __init__(self, ip, port, grader):
        self.ip = ip
        self.port = port
        self.grader = grader
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))

        self.clients = []

    def start(self):
        self.server.listen()
        print(f"{Fore.GREEN}Server started on {self.ip}{Fore.RESET}")

        while True:
            conn, addr = self.server.accept()
            client = Client(conn, addr, self.grader)
            self.clients.append(client)


class Client:
    header = 64
    padding = " " * header
    packet_size = 1024

    def __init__(self, conn, addr, grader):
        self.conn = conn
        self.addr = addr
        self.grader = grader
        self.active = True

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
                self.active = False
                self.conn.close()
                self.alert("INFO", "Disconnected")
                return

            elif msg["type"] == "submit":
                pid = msg["pid"]
                lang = msg["lang"]
                code = msg["code"]

                result = self.grader.grade(self, pid, lang, code)
                if result["status"]:
                    self.send({"type": "submit", "status": True})
                    self.alert("INFO", "Submitted a solution")
                else:
                    self.send({"type": "submit", "status": False, "error": result["error"]})
                    self.alert("WARNING", "Submitted with error "+result["error"])

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


class Grader:
    parent = os.path.realpath(os.path.dirname(__file__))
    supported_langs = (1, 2, 3)

    def __init__(self):
        self.queue = []
        self.pids = []

        os.makedirs(os.path.join(self.parent, "grader"), exist_ok=True)
        os.makedirs(os.path.join(self.parent, "submissions"), exist_ok=True)
        self.load_problems()
        threading.Thread(target=self.grader).start()

    def grader(self):
        while True:
            while len(self.queue) == 0:
                time.sleep(0.01)

            try:
                client, pid, lang, code = self.queue.pop(0)
                submit_path = os.path.join(self.parent, "grader", "submission")
                submissions_path = os.path.join(self.parent, "submissions")
                compiled_path = os.path.join(self.parent, "grader", "compiled")
                in_path = os.path.join(self.parent, "grader", "in")
                out_path = os.path.join(self.parent, "grader", "out")
                err_path = os.path.join(self.parent, "grader", "err")
                data_path = os.path.join(self.parent, "problems", self.pids[[x[1] for x in self.pids].index(pid)][0])
                submit_save_path = 0
                if len(os.listdir(submissions_path)) > 0:
                    submit_save_path = max(map(lambda x: int(x.split(".")[0]), os.listdir(submissions_path))) + 1
                submit_save_path = os.path.join(self.parent, "submissions", str(submit_save_path)+".json")
                if lang == 3:
                    submit_path += ".cpp"

                with open(data_path, "rb") as file:
                    prob_data = pickle.load(file)
                with open(submit_path, "w") as file:
                    file.write(code)

                with open(submit_save_path, "w") as file:
                    json.dump({"from": client.addr, "time": str(datetime.now()), "code": code}, file, indent=4)

                if lang == 3:
                    os.system(f"g++ {submit_path} -o {compiled_path}")

                client.send({"type": "submit", "num_cases": len(prob_data["cases"])})

                for i, data in enumerate(prob_data["cases"]):
                    in_data, out_data = data
                    with open(in_path, "w") as file:
                        file.write(in_data)
                    with open(out_path, "w") as file:
                        file.close()

                    with open(in_path, "r") as in_file, open(out_path, "w") as out_file, open(err_path, "w") as err_file:
                        if lang not in self.supported_langs:
                            continue

                        commands = None
                        time_start = time.time()
                        if lang == 1:
                            commands = ["python3", submit_path]
                        elif lang == 2:
                            commands = ["python2", submit_path]
                        elif lang == 3:
                            commands = [compiled_path]

                        p = subprocess.Popen(commands, stdin=in_file, stdout=out_file, stderr=err_file)
                        p.wait()
                        elapse = time.time() - time_start

                    with open(err_path, "r") as file:
                        err = file.read()
                    if err.strip() != "":
                        client.send({"type": "submit", "result": "!", "error": err})
                        if i == 0:
                            break
                        continue
                    with open(out_path, "r") as file:
                        ans = file.read()
                    result = "*" if ans.strip() == out_data.strip() else "x"
                    client.send({"type": "submit", "result": result, "elapse": elapse})

            except Exception as e:
                print(f"Error in grading: {e}")

    def load_problems(self):
        for filepath in os.listdir(os.path.join(self.parent, "problems")):
            try:
                with open(os.path.join(self.parent, "problems", filepath), "rb") as file:
                    data = pickle.load(file)
                self.pids.append((filepath, data["pid"]))
            except:
                pass

    def grade(self, client, pid, lang, code):
        if pid not in [x[1] for x in self.pids]:
            return {"status": False, "error": "Invalid PID."}
        if lang not in self.supported_langs:
            return {"status": False, "error": "Invalid language."}

        self.queue.append((client, pid, lang, code))
        return {"status": True}


def main():
    if os.path.isfile("settings.json"):
        with open("settings.json", "r") as file:
            data = json.load(file)
            ip = data["ip"]
    else:
        ip = input("IP: ")

    grader = Grader()
    server = Server(ip, 5555, grader)
    server.start()


main()

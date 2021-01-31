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
from getpass import getpass
colorama.init()

CPP_COMPILE = "g++ {} -o {}"
C_COMPILE = "gcc {} -o {}"
PY3_CMD = "python3.8 {}"
PY2_CMD = "python2 {}"
GO_CMD = "go run {}"


class Server:
    def __init__(self, ip, port, grader, password):
        self.ip = ip
        self.port = port
        self.grader = grader
        self.password = password
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))

        self.clients = []

    def start(self):
        self.server.listen()
        print(f"{Fore.GREEN}Server started on {self.ip}{Fore.RESET}")

        while True:
            conn, addr = self.server.accept()
            client = Client(conn, addr, self.grader)
            threading.Thread(target=client.init, args=(self.password,)).start()
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

    def init(self, password):
        self.alert("INFO", "Connected")
        if self.auth(password):
            threading.Thread(target=self.start).start()

    def auth(self, password):
        chars = bytes(range(256))
        task = b"".join(random.choices([chars[i:i+1] for i in range(len(chars))], k=64))
        answer = sha256(task).hexdigest()
        self.send({"type": "auth", "task": task, "password": password != ""})

        reply = self.recv()
        if answer == reply["answer"]:
            self.alert("INFO", "Authenticated")
        else:
            self.alert("ERROR", "Authentication failed")
            self.conn.close()
            return False
        if password != "" and reply["password"] != password:
            self.alert("ERROR", "Wrong password")
            self.conn.close()
            return False

        return True

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

            elif msg["type"] == "get_problems":
                problems = self.grader.get_problems()
                problems = sorted(problems, key=lambda x: x[0])
                self.send({"type": "get_problems", "problems": problems})

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
    supported_langs = (1, 2, 3, 4, 5)

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
                submit_path += {1: ".py", 2: ".py", 3: ".cpp", 4: ".c", 5: ".go"}[lang]

                with open(data_path, "rb") as file:
                    prob_data = pickle.load(file)
                with open(submit_path, "w") as file:
                    file.write(code)
                with open(submit_save_path, "w") as file:
                    json.dump({"from": client.addr, "time": str(datetime.now()), "code": code}, file, indent=4)

                client.send({"type": "submit", "num_cases": len(prob_data["cases"])})

                status = 0
                if lang == 3:
                    status = os.system(CPP_COMPILE.format(submit_path, compiled_path))
                elif lang == 4:
                    status = os.system(C_COMPILE.format(submit_path, compiled_path))
                if status == 0:
                    client.send({"type": "submit", "compiled": True})
                else:
                    client.send({"type": "submit", "compiled": False})

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
                            commands = PY3_CMD.format(submit_path).split()
                        elif lang == 2:
                            commands = PY2_CMD.format(submit_path).split()
                        elif lang in (3, 4):
                            commands = [compiled_path]
                        elif lang == 5:
                            commands = GO_CMD.format(submit_path).split()

                        p = subprocess.Popen(commands, stdin=in_file, stdout=out_file, stderr=err_file)
                        timeout = False
                        while p.poll() is None:
                            if time.time() - time_start > 3:
                                p.kill()
                                timeout = True
                                break

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
                    if timeout:
                        result = "t"
                    client.send({"type": "submit", "result": result, "elapse": elapse})

            except Exception as e:
                print(f"Error in grading: {e}")

    def load_problems(self):
        for filepath in os.listdir(os.path.join(self.parent, "problems")):
            try:
                with open(os.path.join(self.parent, "problems", filepath), "rb") as file:
                    data = pickle.load(file)
                if data["pid"] not in [x[1] for x in self.pids]:
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

    def get_problems(self):
        problems = []
        for path, pid in self.pids:
            with open(os.path.join(self.parent, "problems", path), "rb") as file:
                data = pickle.load(file)
            problems.append((pid, data["name"], data["difficulty"], len(data["cases"])))
        return problems


def main():
    if os.path.isfile("settings.json"):
        with open("settings.json", "r") as file:
            data = json.load(file)
            ip = data["ip"]
            password = data["password"]
    else:
        ip = input("IP: ")
        password = getpass("Password (leave blank for none): ")

    grader = Grader()
    server = Server(ip, 5555, grader, password)
    server.start()


main()

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

#! WARNING:
#! The server judge will execute files submitted by users.
#! If those files contain malicious code, your system may be messed up.
#! At the time of this writing, there is nothing to prevent this.
#! Use at your own risk
#! The GPL license does not provide any warranty, and the author(s) of this project
#! shall not be held responsible from any damage directly or indirectly caused by it.

import os
import subprocess
import socket
import threading
import pickle
import colorama
from colorama import Fore
colorama.init()


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))

    def start(self):
        self.server.listen()
        print(f"{Fore.GREEN}Server started on {self.ip}{Fore.RESET}")

        while True:
            conn, addr = self.server.accept()


def main():
    server = Server(input("IP: "), 5555)
    server.start()


main()

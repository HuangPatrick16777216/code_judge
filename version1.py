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
import time
import multiprocessing
import json
import colorama
from colorama import Fore
colorama.init()


def check_test_info(path):
    if not os.path.isdir(path):
        print(f"Invalid path: {path}")
        return
    if not os.path.isfile(os.path.join(path, "info.json")):
        print("No info file (info.json).")
        return

    with open(os.path.join(path, "info.json"), "r") as file:
        json_info = json.load(file)

    info = {}
    info["path"] = path
    info["time_limit"] = json_info["time_limit"]
    info["cases"] = json_info["cases"]

    for case in info["cases"]:
        if not os.path.isfile(os.path.join(path, f"{case}.in")):
            print(f"Missing input file for case {case}")
            return
        if not os.path.isfile(os.path.join(path, f"{case}.out")):
            print(f"Missing output file for case {case}")
            return

    return info


def test_file(info, path):
    if info is None:
        print(f"Invalid info.")
        return
    if not os.path.isfile(path):
        print(f"Invalid path: {path}")
        return

    pardir = os.path.realpath(os.path.dirname(__file__))
    data_path = info["path"]

    with open(path, "r") as file:
        test_data = file.read()

    for case in info["cases"]:
        with open(os.path.join(data_path, f"{case}.in"), "r") as file:
            data = file.read()
        with open(os.path.join(pardir, "file.in"), "w") as file:
            file.write(data)
        with open(os.path.join(data_path, f"{case}.out"), "r") as file:
            correct_ans = file.read().strip()

        msg = f"Testing case {case}"
        sys.stdout.write(msg)
        sys.stdout.flush()

        start = time.time()
        exec(test_data)
        elapse = time.time() - start
        elapse = str(int(100000*elapse)/100)

        if os.path.isfile(os.path.join(pardir, "file.out")):
            with open(os.path.join(pardir, "file.out"), "r") as file:
                ans = file.read()
            if ans == correct_ans:
                result = Fore.GREEN + f"Correct, {elapse}ms"
            else:
                result = Fore.RED + f"Wrong"
        else:
            result = Fore.RED + "No output file."

        sys.stdout.write("\r" + " "*len(msg) + "\r")
        sys.stdout.write(result)
        sys.stdout.write(Fore.WHITE)
        sys.stdout.write("\n")
        sys.stdout.flush()

    os.remove(os.path.join(pardir, "file.in"))
    os.remove(os.path.join(pardir, "file.out"))


def main():
    test_info = None

    while True:
        cmd = input(">>> ")

        if cmd in ("quit", "exit"):
            return

        elif cmd.startswith("set"):
            path = cmd[3:].strip()
            result = check_test_info(path)
            if isinstance(result, dict):
                test_info = result

        elif cmd.startswith("test"):
            path = cmd[4:].strip()
            test_file(test_info, path)


main()

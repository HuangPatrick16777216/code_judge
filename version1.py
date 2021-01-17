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
import time
import multiprocessing
import json
import colorama
from colorama import Fore
colorama.init()


def check_test_info(path):
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Invalid path: {path}")
    if not os.path.isfile(os.path.join(path, "info.json")):
        raise FileNotFoundError("No info file (info.json).")

    info = {}

    with open(os.path.join(path, "info.json"), "r") as file:
        json_info = json.load(file)

    info["time_limit"] = json_info["time_limit"]
    info["cases"] = json_info["cases"]
    for case in info["cases"]:
        if not os.path.isfile(os.path.join(path, f"{case}.in")):
            raise FileNotFoundError(f"Missing input file for case {case}")
        if not os.path.isfile(os.path.join(path, f"{case}.out")):
                raise FileNotFoundError(f"Missing output file for case {case}")

    return info


def main():
    test_info = None

    while True:
        cmd = input(">>> ")

        if cmd.startswith("set"):
            path = cmd.replace("set", "").strip()
            result = check_test_info(path)
            if isinstance(result, dict):
                test_info = result


main()

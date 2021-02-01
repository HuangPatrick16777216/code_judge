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
import pygame
from copy import deepcopy
from getpass import getpass
from hashlib import sha256
from tkinter import Tk
from tkinter.filedialog import askopenfilename
pygame.init()
Tk().withdraw()

WIDTH, HEIGHT = 1280, 720
FPS = 60

BLACK = (0, 0, 0)
GRAY_DARK = (64, 64, 64)
GRAY = (128, 128, 128)
GRAY_LIGHT = (192, 192, 192)
WHITE = (255, 255, 255)

FONT_SMALL = pygame.font.SysFont("ubuntu", 14)
FONT_MED = pygame.font.SysFont("ubuntu", 20)
FONT_LARGE = pygame.font.SysFont("ubuntu", 36)


class Text:
    def __init__(self, text):
        self.text = text

    def draw(self, window, loc):
        text_loc = [loc[i] - self.text.get_size()[i]//2 for i in range(2)]
        window.blit(self.text, text_loc)


class Button:
    def __init__(self, text):
        self.text = text

    def draw(self, window, events, loc, size):
        loc = list(loc)
        loc[0] -= size[0]//2

        clicked = self.clicked(events, loc, size)
        color = (GRAY_DARK if clicked else GRAY_LIGHT) if self.hovered(loc, size) else WHITE
        text_loc = [loc[i] + (size[i]-self.text.get_size()[i])//2 for i in range(2)]

        pygame.draw.rect(window, color, (*loc, *size))
        pygame.draw.rect(window, BLACK, (*loc, *size), 2)
        window.blit(self.text, text_loc)

        return clicked

    def hovered(self, loc, size):
        mouse = pygame.mouse.get_pos()
        if loc[0] <= mouse[0] <= loc[0]+size[0] and loc[1] <= mouse[1] <= loc[1]+size[1]:
            return True
        return False

    def clicked(self, events, loc, size):
        if self.hovered(loc, size):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return True
        return False


class TextInput:
    """Also written by Arjun Sahlot <https://github.com/ArjunSahlot>"""

    def __init__(self, font, label="", password=False, on_enter=None):
        self.font = font
        self.label = label
        self.password = password
        self.on_enter = on_enter

        self.cursor_pos = 0
        self.text = ""
        self.editing = False
        self.frame = 0

        self.key_rpt_count = {}
        self.key_rpt_init = 400
        self.key_rpt_int = 35
        self.clock = pygame.time.Clock()

    def draw(self, window, events, loc, size):
        self.frame += 1
        loc = list(loc)
        loc[0] -= size[0]//2

        clicked = self.clicked(events, loc, size)
        str_text = self.label if not self.editing and self.text == "" else self.text
        if self.password and not self.text == "":
            str_text = "*" * len(str_text)
        text = self.font.render(str_text, 1, BLACK)
        text_loc = [loc[i] + (size[i]-text.get_size()[i])//2 for i in range(2)]

        color = GRAY_DARK if clicked else (GRAY_LIGHT if self.hovered(loc, size) and not self.editing else WHITE)
        pygame.draw.rect(window, color, (*loc, *size))
        pygame.draw.rect(window, BLACK, (*loc, *size), 2)
        window.blit(text, text_loc)
        if self.editing and (self.frame//30) % 2 == 0:
            cursor_x = text_loc[0] + self.font.render(str_text[:self.cursor_pos], 1, BLACK).get_width()
            pygame.draw.line(window, BLACK, (cursor_x, loc[1]+12), (cursor_x, loc[1]+size[1]-12))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.editing = self.hovered(loc, size)
            elif event.type == pygame.KEYDOWN and self.editing:
                if event.key in (pygame.K_ESCAPE, pygame.K_TAB):
                    self.editing = False
                elif event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                    self.editing = False
                    if self.on_enter is not None:
                        self.editing = True
                        self.on_enter()
                        self.text = ""

                else:
                    if event.key not in self.key_rpt_count:
                        self.key_rpt_count[event.key] = [0, event.unicode]

                    if event.key == pygame.K_LEFT:
                        self.cursor_pos -= 1
                    elif event.key == pygame.K_RIGHT:
                        self.cursor_pos += 1
                    elif event.key in (pygame.K_HOME, pygame.K_PAGEDOWN):
                        self.cursor_pos = 0
                    elif event.key in (pygame.K_END, pygame.K_PAGEUP):
                        self.cursor_pos = len(self.text)

                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                        self.cursor_pos -= 1
                    elif event.key == pygame.K_DELETE:
                        self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
                    else:
                        self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                        self.cursor_pos += 1

                self.cursor_pos = min(max(self.cursor_pos, 0), len(self.text))

            elif event.type == pygame.KEYUP:
                if event.key in self.key_rpt_count:
                    del self.key_rpt_count[event.key]

        for key in self.key_rpt_count:
            self.key_rpt_count[key][0] += self.clock.get_time()

            if self.key_rpt_count[key][0] >= self.key_rpt_init:
                self.key_rpt_count[key][0] = self.key_rpt_init - self.key_rpt_int
                event_key, event_unicode = key, self.key_rpt_count[key][1]
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=event_key, unicode=event_unicode))

        self.clock.tick()

    def hovered(self, loc, size):
        mouse = pygame.mouse.get_pos()
        if loc[0] <= mouse[0] <= loc[0]+size[0] and loc[1] <= mouse[1] <= loc[1]+size[1]:
            return True
        return False

    def clicked(self, events, loc, size):
        if self.hovered(loc, size):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return True
        return False


class Client:
    header = 64
    padding = " " * header
    packet_size = 1024

    def __init__(self, ip, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))
        self.auth()

    def auth(self):
        task = self.recv()
        ans = sha256(task["task"]).hexdigest()
        password = ""
        if task["password"]:
            password = getpass("Password: ")
        self.send({"type": "auth", "answer": ans, "password": password})

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


class Manager:
    """Manages and displays everything."""

    supported_langs = ("Python 3.8.0", "Python 2.7.17", "C++ (g++ 7.5.0)", "C (gcc 7.5.0)", "Go", "Java 11")
    text_pid = Text(FONT_LARGE.render("Choose a Problem", 1, BLACK))
    text_lang = Text(FONT_LARGE.render("Choose a Language", 1, BLACK))
    text_file = Text(FONT_LARGE.render("Choose a File", 1, BLACK))
    text_submitting = Text(FONT_LARGE.render("Server is grading...", 1, BLACK))

    button_back = Button(FONT_MED.render("Back", 1, BLACK))
    button_select_file = Button(FONT_MED.render("Select File", 1, BLACK))
    button_submit = Button(FONT_MED.render("Submit", 1, BLACK))

    def __init__(self, conn):
        self.conn = conn
        self.status = "PID"
        self.init()

    def init(self):
        self.curr_info = {}
        self.sel_path = None

        self.conn.send({"type": "get_problems"})
        self.problems = self.conn.recv()["problems"]
        self.pid_buttons = [Button(FONT_MED.render(f"{pid}: {name}, Difficulty={difficult}, Number of cases={num_cases}", 1, BLACK))
            for pid, name, difficult, num_cases in self.problems]

        self.lang_buttons = [Button(FONT_MED.render(lang, 1, BLACK)) for lang in self.supported_langs]

    def draw(self, window, events):
        if self.status == "PID":
            self.text_pid.draw(window, (WIDTH//2, 50))
            clicked = [button.draw(window, events, (WIDTH//2, 150+50*i), (WIDTH-200, 35)) for i, button in enumerate(self.pid_buttons)]
            if True in clicked:
                self.curr_info["pid"] = self.problems[clicked.index(True)][0]
                self.status = "LANG"

        elif self.status == "LANG":
            self.text_lang.draw(window, (WIDTH//2, 50))
            clicked = [button.draw(window, events, (WIDTH//2, 150+50*i), (WIDTH-200, 35)) for i, button in enumerate(self.lang_buttons)]
            if True in clicked:
                self.curr_info["lang"] = clicked.index(True) + 1
                self.status = "FILE"

        elif self.status == "FILE":
            self.text_file.draw(window, (WIDTH//2, 50))
            if self.button_select_file.draw(window, events, (490, 670), (150, 35)):
                self.sel_path = askopenfilename()
            if self.button_submit.draw(window, events, (790, 670), (150, 35)) and self.sel_path is not None:
                send_data = deepcopy(self.curr_info)
                send_data["type"] = "submit"
                with open(self.sel_path, "r") as file:
                    send_data["code"] = file.read()
                self.conn.send(send_data)
                self.status = "SUBMITTING"

            if self.sel_path is None:
                text_path = Text(FONT_MED.render("Selected file: <No file selected>", 1, BLACK))
            else:
                text_path = Text(FONT_MED.render(f"Selected file: {self.sel_path}", 1, BLACK))
            text_path.draw(window, (640, 300))

        elif self.status == "SUBMITTING":
            self.text_submitting.draw(window, (WIDTH//2, 50))

        if self.status != "SUBMITTING" and self.button_back.draw(window, events, (50, 15), (70, 35)):
            if self.status == "FILE":
                self.status = "LANG"
            elif self.status == "LANG":
                self.status = "PID"


def main():
    if os.path.isfile("settings.json"):
        with open("settings.json", "r") as file:
            data = json.load(file)
            ip = data["ip"]
    else:
        ip = input("IP: ")

    conn = Client(ip, 5555)
    manager = Manager(conn)

    pygame.display.set_caption("Code Judge")
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                conn.send({"type": "quit"})
                pygame.quit()
                return

        window.fill(WHITE)
        manager.draw(window, events)


main()

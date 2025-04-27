import tkinter as tk
from tkinter import font
import random
import ctypes
import subprocess
import winsound
import threading
import cv2
from PIL import Image, ImageTk
import os

# 启用Windows 10的高DPI支持
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# 配置你的视频路径
VIDEO_PATH = r"C:\path\to\your\video.mp4"  # TODO: 改成你自己的路径

class VirusSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.color_inverted = False
        self.original_bg = "#f0f0f0"
        self.original_fg = "#000000"
        self.inverted_bg = "#1a1a1a"
        self.inverted_fg = "#ffffff"

        self.base_x = 100
        self.base_y = 100
        self.offset = 35
        self.current_x = self.base_x
        self.current_y = self.base_y

        self.root.after(1000, self.invert_colors)
        self.root.after(1500, self.create_wave)

    def get_current_colors(self):
        return (self.inverted_bg, self.inverted_fg) if self.color_inverted else (self.original_bg, self.original_fg)

    def invert_colors(self):
        self.color_inverted = not self.color_inverted
        self.root.after(800, self.invert_colors)

    def calculate_position(self):
        self.current_x += self.offset
        self.current_y += int(self.offset * 0.8)

        if self.current_x > self.screen_width - 300:
            self.current_x = self.base_x + random.randint(-20, 20)
        if self.current_y > self.screen_height - 200:
            self.current_y = self.base_y + random.randint(-20, 20)

        return self.current_x, self.current_y

    def create_virus_window(self):
        bg_color, fg_color = self.get_current_colors()

        window = tk.Toplevel(self.root)
        window.overrideredirect(1)
        window.attributes("-topmost", True)

        x, y = self.calculate_position()
        window.geometry(f"300x150+{x}+{y}")

        canvas = tk.Canvas(window, bg=bg_color, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        canvas.create_oval(20, 20, 50, 50,
                           fill="#ff4444" if random.random() > 0.5 else "#44ff44",
                           outline="")

        error_codes = ["0x80070005", "0xC000021A", "CRITICAL_ERROR"]
        warning_text = random.choice([
            "系统文件损坏\n立即修复！",
            "检测到恶意软件\n正在窃取数据！",
            f"错误代码：{random.choice(error_codes)}\n需要管理员权限"
        ])

        sys_font = font.nametofont("TkDefaultFont")
        canvas.create_text(
            80, 40,
            text=warning_text,
            fill=fg_color,
            font=(sys_font.actual()["family"], 10, "bold"),
            anchor="w"
        )

        canvas.create_rectangle(
            20, 110, 280, 130,
            outline=fg_color,
            fill=bg_color
        )
        canvas.create_rectangle(
            22, 112, 22 + random.randint(50, 250), 128,
            fill="#ff0000" if self.color_inverted else "#00ff00",
            outline=""
        )

        window.after(2500 + random.randint(0, 1000), window.destroy)

    def pop_cmd(self):
        subprocess.Popen(
            "start cmd /k echo 系统严重错误！ & title !! SYSTEM ERROR !! & mode con: cols=60 lines=10",
            shell=True
        )

    def play_warning_sound(self):
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)

    def play_video_window(self):
        """弹出一个播放视频的窗口"""
        if not os.path.exists(VIDEO_PATH):
            print("视频文件不存在！")
            return

        video_window = tk.Toplevel(self.root)
        video_window.title("系统警告 - 视频播放")
        video_window.geometry("640x480")
        video_window.resizable(False, False)
        video_window.attributes("-topmost", True)

        canvas = tk.Canvas(video_window, width=640, height=480)
        canvas.pack()

        cap = cv2.VideoCapture(VIDEO_PATH)

        def update_frame():
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                canvas.create_image(0, 0, anchor="nw", image=imgtk)
                canvas.imgtk = imgtk
                video_window.after(30, update_frame)
            else:
                cap.release()
                video_window.destroy()

        update_frame()

    def create_wave(self, count=0):
        if count < 520:
            self.create_virus_window()

            # 5%概率弹出cmd
            if random.random() < 0.05:
                self.pop_cmd()

            # 10%概率播放系统警告声
            if random.random() < 0.1:
                self.play_warning_sound()

            # 1%概率播放视频（控制频率）
            if random.random() < 0.01:
                threading.Thread(target=self.play_video_window).start()

            delay = max(30, 300 - count)
            self.root.after(delay, lambda: self.create_wave(count + 1))

            if random.random() > 0.95:
                self.current_x = self.base_x + random.randint(-100, 100)
                self.current_y = self.base_y + random.randint(-50, 50)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    simulator = VirusSimulator()
    simulator.run()

import tkinter as tk
import subprocess
import threading
import ctypes
import time
import random
from ctypes import wintypes

# Windows API初始化
user32 = ctypes.WinDLL('user32', use_last_error=True)
gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)

# 定义Windows常量
SPI_SETDESKWALLPAPER = 0x0014
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02
SWP_NOSIZE = 0x0001
SWP_NOZORDER = 0x0004

class SystemHacker:
    def __init__(self):
        self.running = False
        self.cmd_count = 0
        self.color_inverted = False
        self.original_color = self.get_system_color()

        # 创建隐藏控制窗口
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.protocol("WM_DELETE_WINDOW", self.safe_exit)

        # 安全计数器
        self.safety_counter = 0
        self.max_operations = 100  # 最大操作次数限制

    def get_system_color(self):
        # 简化实现，实际上是伪装的白色
        return 0xFFFFFF

    def invert_system_colors(self):
        # 伪装改变颜色（不是真正反转屏幕颜色）
        self.color_inverted = not self.color_inverted
        # 这里可以添加真实操作，比如改变主题，壁纸什么的
        # 但为了安全，这里我们只是切换标志位

    def create_cmd(self):
        while self.running and self.safety_counter < self.max_operations:
            try:
                x = random.randint(0, user32.GetSystemMetrics(0) - 200)
                y = random.randint(0, user32.GetSystemMetrics(1) - 100)

                color_code = "4F" if self.color_inverted else "2E"
                title = f"系统警告_{self.cmd_count}"

                # 创建cmd窗口，隐藏主cmd窗口只弹出子窗口
                subprocess.Popen(
                    f'start "" /MIN cmd.exe /K "mode con: cols=40 lines=10 && title {title} && color {color_code}"',
                    shell=True,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )

                time.sleep(0.3)  # 给系统一点反应时间

                # 定位窗口
                hwnd = user32.FindWindowW(None, title)
                if hwnd:
                    user32.SetWindowPos(hwnd, 0, x, y, 0, 0, SWP_NOSIZE | SWP_NOZORDER)

                self.cmd_count += 1
                self.safety_counter += 1
                time.sleep(0.5 + random.uniform(0, 0.5))
            except Exception as e:
                print(f"[create_cmd 错误]: {e}")
                break

    def color_thread(self):
        while self.running and self.safety_counter < self.max_operations:
            try:
                self.invert_system_colors()
                self.safety_counter += 1
                time.sleep(1.0 + random.uniform(0, 0.5))
            except Exception as e:
                print(f"[color_thread 错误]: {e}")
                break

    def start_attack(self):
        if not self.running:
            self.running = True

            # 启动子线程
            threading.Thread(target=self.create_cmd, daemon=True).start()
            threading.Thread(target=self.color_thread, daemon=True).start()

            # 60秒后自动退出
            self.root.after(60000, self.safe_exit)
            self.root.mainloop()

    def safe_exit(self):
        if not self.running:
            return
        self.running = False

        try:
            # 恢复颜色
            if self.color_inverted:
                self.invert_system_colors()

            # 关闭自己的cmd窗口（更安全，只杀有特定标题的）
            for i in range(self.cmd_count):
                title = f"系统警告_{i}"
                hwnd = user32.FindWindowW(None, title)
                if hwnd:
                    user32.PostMessageW(hwnd, 0x0010, 0, 0)  # 发送WM_CLOSE消息
        except Exception as e:
            print(f"[safe_exit 错误]: {e}")
        finally:
            self.root.quit()
            self.root.destroy()

if __name__ == "__main__":
    print("警告：此程序可能影响系统稳定性，请谨慎运行！")
    confirm = input("确实要运行吗？(输入 'I_ACCEPT_RISKS' 继续): ")

    if confirm == "I_ACCEPT_RISKS":
        hacker = SystemHacker()
        try:
            hacker.start_attack()
        except KeyboardInterrupt:
            hacker.safe_exit()
    else:
        print("操作已取消。")

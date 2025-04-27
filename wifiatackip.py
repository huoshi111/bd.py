import tkinter as tk
import subprocess
import threading
import ctypes
import time
import random
from ctypes import wintypes

# Windows API初始化
user32 = ctypes.WinDLL('user32')
gdi32 = ctypes.WinDLL('gdi32')
SHFullScreen = ctypes.windll.shell32.SHFullScreen

# 定义Windows常量
SPI_SETDESKWALLPAPER = 0x0014
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

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
        # 获取当前系统主题色（简化实现）
        return 0xFFFFFF  # 默认白色

    def invert_system_colors(self):
        # 使用Windows API反转颜色
        if self.color_inverted:
            color = self.original_color
        else:
            color = 0xFFFFFF - self.original_color

        # 创建临时纯色BMP
        hdc = user32.GetDC(0)
        bitmap = gdi32.CreateBitmap(1, 1, 1, 32, ctypes.byref(ctypes.c_ulong(color)))
        user32.SetSysColors(1, ctypes.byref(ctypes.c_int(1)), ctypes.byref(ctypes.c_ulong(color)))
        
        # 设置壁纸
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            None,
            SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )
        
        self.color_inverted = not self.color_inverted

    def create_cmd(self):
        # 安全创建CMD窗口
        while self.running and self.safety_counter < self.max_operations:
            try:
                # 随机位置参数
                x = random.randint(0, ctypes.windll.user32.GetSystemMetrics(0)-200)
                y = random.randint(0, ctypes.windll.user32.GetSystemMetrics(1)-100)
                
                # 使用Windows API创建定位窗口
                subprocess.Popen(
                    f'cmd /c start /MIN cmd.exe /K "mode con: cols=40 lines=10 && title 系统警告_{self.cmd_count} && color {"4F" if self.color_inverted else "2E"}"',
                    shell=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                # 窗口定位（需要额外处理）
                time.sleep(0.2)
                hwnd = user32.FindWindowW(None, f"系统警告_{self.cmd_count}")
                if hwnd:
                    user32.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0001)
                
                self.cmd_count += 1
                self.safety_counter += 1
                time.sleep(0.5 + random.random())
            except:
                break

    def color_thread(self):
        # 颜色反转线程
        while self.running and self.safety_counter < self.max_operations:
            self.invert_system_colors()
            self.safety_counter += 1
            time.sleep(1.2 + random.uniform(-0.2, 0.5))

    def start_attack(self):
        if not self.running:
            self.running = True
            # 启动线程
            threading.Thread(target=self.create_cmd, daemon=True).start()
            threading.Thread(target=self.color_thread, daemon=True).start()
            
            # 安全计时器
            self.root.after(60000, self.safe_exit)  # 60秒自动停止
            self.root.mainloop()

    def safe_exit(self):
        # 安全恢复机制
        self.running = False
        try:
            # 恢复原始颜色
            if self.color_inverted:
                self.invert_system_colors()
            # 关闭所有CMD窗口
            subprocess.run('taskkill /F /IM cmd.exe', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        finally:
            self.root.destroy()

if __name__ == "__main__":
    print("警告：此程序会产生破坏性效果！")
    confirm = input("确实要运行吗？(输入'I_ACCEPT_RISKS'继续): ")
    
    if confirm == "I_ACCEPT_RISKS":
        hacker = SystemHacker()
        try:
            hacker.start_attack()
        except KeyboardInterrupt:
            hacker.safe_exit()
    else:
        print("操作已取消")

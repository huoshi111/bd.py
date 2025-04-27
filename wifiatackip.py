import tkinter as tk
from tkinter import font
import random
import ctypes

# 启用Windows 10的高DPI支持
ctypes.windll.shcore.SetProcessDpiAwareness(1)


class VirusSimulator:
    def __init__(self):
        # 主窗口初始化
        self.root = tk.Tk()
        self.root.withdraw()

        # 获取屏幕尺寸
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # 颜色反转控制
        self.color_inverted = False
        self.original_bg = "#f0f0f0"  # 默认浅色背景
        self.original_fg = "#000000"  # 默认黑色文字
        self.inverted_bg = "#1a1a1a"  # 深色背景
        self.inverted_fg = "#ffffff"  # 白色文字

        # 弹窗位置参数
        self.base_x = 100
        self.base_y = 100
        self.offset = 35  # 窗口间距
        self.current_x = self.base_x
        self.current_y = self.base_y

        # 首次执行延迟
        self.root.after(1000, self.invert_colors)
        self.root.after(1500, self.create_wave)

    def get_current_colors(self):
        """获取当前颜色配置"""
        return (self.inverted_bg, self.inverted_fg) if self.color_inverted \
            else (self.original_bg, self.original_fg)

    def invert_colors(self):
        """反转系统颜色（模拟效果）"""
        self.color_inverted = not self.color_inverted
        # 递归调用实现颜色闪烁
        self.root.after(800, self.invert_colors)

    def calculate_position(self):
        """计算病毒式扩散坐标"""
        self.current_x += self.offset
        self.current_y += int(self.offset * 0.8)

        # 边界检测（保留100像素边距）
        if self.current_x > self.screen_width - 300:
            self.current_x = self.base_x + random.randint(-20, 20)
        if self.current_y > self.screen_height - 200:
            self.current_y = self.base_y + random.randint(-20, 20)

        return self.current_x, self.current_y

    def create_virus_window(self):
        """创建单个病毒窗口"""
        bg_color, fg_color = self.get_current_colors()

        window = tk.Toplevel(self.root)
        window.overrideredirect(1)  # 移除窗口装饰
        window.attributes("-topmost", True)

        # 动态位置计算
        x, y = self.calculate_position()
        window.geometry(f"300x150+{x}+{y}")

        # 病毒样式内容
        canvas = tk.Canvas(
            window,
            bg=bg_color,
            highlightthickness=0
        )
        canvas.pack(fill=tk.BOTH, expand=True)

        # 警告图标
        canvas.create_oval(20, 20, 50, 50,
                           fill="#ff4444" if random.random() > 0.5 else "#44ff44",
                           outline="")

        # 动态文字内容
        error_codes = ["0x80070005", "0xC000021A", "CRITICAL_ERROR"]
        warning_text = random.choice([
            "系统文件损坏\n立即修复！",
            "检测到恶意软件\n正在窃取数据！",
            f"错误代码：{random.choice(error_codes)}\n需要管理员权限"
        ])

        # 使用系统字体
        sys_font = font.nametofont("TkDefaultFont")
        canvas.create_text(
            80, 40,
            text=warning_text,
            fill=fg_color,
            font=(sys_font.actual()["family"], 10, "bold"),
            anchor="w"
        )

        # 伪进度条
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

        # 自动销毁
        window.after(2500 + random.randint(0, 1000), window.destroy)

    def create_wave(self, count=0):
        """创建弹窗波次"""
        if count < 520:  # 总弹窗数控制
            # 每波生成3-5个窗口
            for _ in range(random.randint(3, 5)):
                self.create_virus_window()

            # 动态调整生成速度（逐渐加快）
            delay = max(50, 200 - count * 2)
            self.root.after(delay, lambda: self.create_wave(count + 1))

            # 随机重置起始位置
            if random.random() > 0.8:
                self.current_x = self.base_x + random.randint(-100, 100)
                self.current_y = self.base_y + random.randint(-50, 50)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    simulator = VirusSimulator()
    simulator.run()
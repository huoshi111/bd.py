import subprocess
import winsound

class VirusSimulator:
    def __init__(self):
        # ... 你的初始化内容 ...
        pass
    
    def pop_cmd(self):
        subprocess.Popen("start cmd /k echo 正在修复系统错误... & timeout /t 1 & exit", shell=True)
    
    def play_warning_sound(self):
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
    
    def create_wave(self, count=0):
        if count < 520:
            self.create_virus_window()
            
            # 偶尔弹出cmd窗口
            if random.random() < 0.05:
                self.pop_cmd()
            
            # 偶尔播放警告声音
            if random.random() < 0.1:
                self.play_warning_sound()
            
            delay = max(30, 300 - count)
            self.root.after(delay, lambda: self.create_wave(count + 1))
            
            if random.random() > 0.95:
                self.current_x = self.base_x + random.randint(-100, 100)
                self.current_y = self.base_y + random.randint(-50, 50)

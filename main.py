import tkinter as tk
import random
import threading
import time
import sys
import os

# 添加隐藏控制台窗口的代码
if sys.executable.endswith('pythonw.exe'):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

class RollCallApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('随点SRC')
        self.window.geometry('400x300')
        
        self.names = []
        self.running = False
        
        # 添加导入按钮
        self.import_btn = tk.Button(self.window, text='导入名单', command=self.import_names,
                            font=('微软雅黑', 14), bg='#2196F3', fg='white')
        self.import_btn.pack(pady=5)
        
        self.name_label = tk.Label(self.window, text='准备就绪', font=('微软雅黑', 24))
        self.name_label.pack(pady=20)
        
        self.btn = tk.Button(self.window, text='开始点名', command=self.start_rollcall,
                            font=('微软雅黑', 14), bg='#4CAF50', fg='white')
        self.btn.pack(pady=10)
        
    def import_names(self):
        from tkinter import filedialog, messagebox
        file_path = filedialog.askopenfilename(filetypes=[('文本文件', '*.txt')])
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.names = [name.strip() for name in f.readlines() if name.strip()]
                count = len(self.names)
                messagebox.showinfo('导入成功', f'成功导入 {count} 个学生名单！')
                self.name_label.config(text=f'已加载 {count} 人')
        except Exception as e:
            messagebox.showerror('导入失败', f'文件读取失败：{str(e)}')
            self.names = []

    def start_rollcall(self):
        if not self.names:
            self.name_label.config(text='名单为空!')
            return
            
        self.running = True
        self.btn.config(state=tk.DISABLED)
        
        threading.Thread(target=self.rollcall_animation).start()

    def rollcall_animation(self):
        end_time = time.time() + 5
        while time.time() < end_time and self.running:
            self.name_label.config(text=random.choice(self.names))
            self.window.update()
            time.sleep(0.1)
        
        selected = random.choice(self.names)
        self.name_label.config(text=selected, font=('微软雅黑', 24, 'bold'))
        self.btn.config(state=tk.NORMAL)
        self.running = False

if __name__ == '__main__':
    app = RollCallApp()
    app.window.mainloop()
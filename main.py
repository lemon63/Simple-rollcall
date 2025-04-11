import tkinter as tk
import random
import threading
import time
import sys
import os

# 隐藏控制台窗口的代码
if sys.executable.endswith('pythonw.exe'):
    sys.stdout = sys.__stdout__ = open(os.devnull, 'w')
    sys.stderr = sys.__stderr__ = open(os.devnull, 'w')

class RollCallApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('简单点名SRC v1.4')
        self.window.geometry('300x270')
        
        # 添加版权标签
        self.copyright_label = tk.Label(self.window, 
                                      text="© 2025 Simple-rollcall - All Rights Reserved",
                                      font=('微软雅黑', 8), 
                                      fg='gray',
                                      cursor="hand2")
        self.copyright_label.pack(side=tk.TOP, pady=5)
        self.copyright_label.bind("<Button-1>", self.show_copyright_info)
        
        self.names = []
        self.running = False
        
        # 加入导入按钮
        self.import_btn = tk.Button(self.window, text='导入名单', command=self.import_names,
                            font=('微软雅黑', 14), bg='#2196F3', fg='white')
        self.import_btn.pack(pady=5)
        
        # 人数选择控件
        self.count_frame = tk.Frame(self.window)
        self.count_frame.pack()
        tk.Label(self.count_frame, text='点名人数:', font=('微软雅黑', 12)).pack(side=tk.LEFT)
        self.num_spin = tk.Spinbox(self.count_frame, from_=1, to=1, width=3, 
                                 font=('微软雅黑', 12), state='readonly')
        self.num_spin.pack(side=tk.LEFT, padx=5)
        
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
                
                # 动态调整人数上限
                max_limit = 1
                if count >= 60:
                    max_limit = 30
                elif count >= 50:
                    max_limit = 20
                elif count >= 20:
                    max_limit = 5
                
                self.num_spin.config(from_=1, to=max_limit)
                
        except Exception as e:
            messagebox.showerror('导入失败', f'文件读取失败：{str(e)}')
            self.names = []
        self.selected_names = []  # 新增：用于记录已点过的名字
        
    def start_rollcall(self):
        try:
            select_num = int(self.num_spin.get())
        except:
            select_num = 1

        # 人数校验逻辑
        min_require = {5:20, 20:50, 30:60}
        for limit, threshold in min_require.items():
            if select_num >= limit and len(self.names) < threshold:
                tk.messagebox.showwarning('人数不足',
                    f'当前学生{len(self.names)}人，至少需要{threshold}人才可同时点名{limit}人')
                return

        if not self.names:
            self.name_label.config(text='名单为空!')
            return
            
        self.running = True
        self.btn.config(state=tk.DISABLED)
        self.selected_names = []  # 重置已点名单
        threading.Thread(target=self.rollcall_animation, args=(select_num,)).start()

    def rollcall_animation(self, select_num=1):
        end_time = time.time() + 5
        candidates = [name for name in self.names if name not in self.selected_names]  # 过滤已点名字
        
        while time.time() < end_time and self.running and candidates:  # 添加candidates检查
            self.name_label.config(text=random.choice(candidates))
            self.window.update()
            time.sleep(0.1)
        
        # 不重复抽取逻辑
        selected = []
        for _ in range(min(select_num, len(candidates))):
            pick = random.choice(candidates)
            selected.append(pick)
            candidates.remove(pick)
            self.selected_names.append(pick)  # 记录已点名字
            
        # 结果显示逻辑
        if select_num == 1:
            self.name_label.config(text=selected[0], font=('微软雅黑', 24, 'bold'))
        else:
            result_window = tk.Toplevel(self.window)
            result_window.title('点名结果')
            
            # 创建带滚动条的画布
            canvas = tk.Canvas(result_window)
            scrollbar = tk.Scrollbar(result_window, orient="horizontal", command=canvas.xview)
            canvas.configure(xscrollcommand=scrollbar.set)
            
            # 创建内容容器
            frame = tk.Frame(canvas)
            canvas.create_window((0,0), window=frame, anchor='nw')
            
            # 自动计算列数（每行最多6个）
            columns = min(6, len(selected))
            for i, name in enumerate(selected):
                row = i // columns
                col = i % columns
                tk.Label(frame, text=name, font=('微软雅黑', 16), padx=10, pady=5,
                        borderwidth=1, relief="solid").grid(row=row, column=col, sticky="ew")
            
            # 动态调整窗口尺寸
            frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
            max_width = min(800, columns*150)
            result_window.geometry(f"{max_width}x400")
            
            # 布局组件
            canvas.pack(side="top", fill="both", expand=True)
            scrollbar.pack(side="bottom", fill="x")
            
            # 绑定鼠标滚轮滚动
            canvas.bind("<MouseWheel>", lambda e: canvas.xview_scroll(-1*(e.delta//120), "units"))
            
        self.btn.config(state=tk.NORMAL)
        self.running = False

    def show_copyright_info(self, event):
        """版权信息"""
        from tkinter import messagebox
        info = """简单点名SRC v1.4
        
开发者: 向南996
联系方式: 3462134162@qq.com
发布日期: 2025-4-12
        
本软件遵循GPL-3.0协议"""
        messagebox.showinfo("关于本软件", info)

if __name__ == '__main__':
    app = RollCallApp()
    app.window.mainloop()
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class DemoApp:
    """
    演示常用UI组件的示例应用
    A simple demo application to showcase common UI components.
    """
    def __init__(self, root):
        """
        初始化应用
        Initialize the application with the root window.
        """
        self.root = root
        self.root.title("Python UI Demo")
        self.root.geometry("400x350")
        
        self.create_widgets()

    def create_widgets(self):
        """
        创建并排列组件
        Create and arrange widgets in the window.
        """
        # 标签 Label
        self.label = tk.Label(self.root, text="Welcome to UI Demo", font=("Arial", 14))
        self.label.pack(pady=10)
        
        # 输入框 Entry
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(pady=5)
        tk.Label(self.entry_frame, text="Name:").pack(side=tk.LEFT)
        self.name_entry = tk.Entry(self.entry_frame)
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        # 复选框 Checkbutton
        self.check_var = tk.BooleanVar()
        self.check = tk.Checkbutton(self.root, text="I agree to terms", variable=self.check_var)
        self.check.pack(pady=5)
        
        # 下拉框 Combobox
        self.combo_label = tk.Label(self.root, text="Select Color:")
        self.combo_label.pack()
        self.combo = ttk.Combobox(self.root, values=["Red", "Green", "Blue"])
        self.combo.current(0)
        self.combo.pack(pady=5)
        
        # 单选按钮 Radiobutton
        self.radio_var = tk.StringVar(value="Option 1")
        self.radio_frame = tk.Frame(self.root)
        self.radio_frame.pack(pady=5)
        tk.Radiobutton(self.radio_frame, text="Option 1", variable=self.radio_var, value="Option 1").pack(side=tk.LEFT)
        tk.Radiobutton(self.radio_frame, text="Option 2", variable=self.radio_var, value="Option 2").pack(side=tk.LEFT)

        # 按钮 Button
        self.btn = tk.Button(self.root, text="Submit", command=self.on_submit, bg="#DDDDDD")
        self.btn.pack(pady=10)
        
    def on_submit(self):
        """
        处理提交按钮点击事件
        Handle button click event.
        """
        name = self.name_entry.get()
        agreed = self.check_var.get()
        color = self.combo.get()
        option = self.radio_var.get()
        
        if not name:
            messagebox.showwarning("Warning", "Please enter your name")
            return
            
        if not agreed:
            messagebox.showwarning("Warning", "You must agree to terms")
            return
            
        messagebox.showinfo("Success", f"Hello {name}!\nYou chose {color} and {option}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DemoApp(root)
    root.mainloop()

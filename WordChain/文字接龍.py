#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文字接龍遊戲
規則：
1. 輸入一個詞語（2-4個字）
2. 下一個詞必須以上一個詞的最後一個字開頭
3. 不能重複使用已經出現過的詞
4. 可以選擇單人模式（對電腦）或雙人模式
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import random

class 文字接龍遊戲:
    def __init__(self, root):
        self.root = root
        self.root.title("文字接龍遊戲")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # 遊戲狀態
        self.已使用詞語 = []
        self.當前字 = None
        self.玩家分數 = 0
        self.電腦分數 = 0
        self.遊戲模式 = None  # 'single' 或 'double'
        self.當前玩家 = 1  # 1 或 2
        
        # 電腦詞庫
        self.詞庫 = self.建立詞庫()
        
        self.建立介面()
        
    def 建立詞庫(self):
        """從外部文件讀取詞庫"""
        詞庫 = {}
        try:
            with open('詞庫.txt', 'r', encoding='utf-8') as f:
                for 行 in f:
                    行 = 行.strip()
                    if not 行:
                        continue
                    parts = 行.split('|')
                    if len(parts) >= 2:
                        首字 = parts[0]
                        詞語列表 = parts[1:]
                        詞庫[首字] = 詞語列表
            return 詞庫
        except FileNotFoundError:
            messagebox.showerror("錯誤", "找不到詞庫.txt文件！\n請確保詞庫文件與程式在同一目錄。")
            return {}
        except Exception as e:
            messagebox.showerror("錯誤", f"讀取詞庫時發生錯誤：{str(e)}")
            return {}
    
    def 建立介面(self):
        """建立遊戲介面"""
        # 標題
        標題 = tk.Label(self.root, text="文字接龍遊戲", font=("微軟正黑體", 24, "bold"), fg="#2c3e50")
        標題.pack(pady=20)
        
        # 遊戲模式選擇框架
        self.模式框架 = tk.Frame(self.root)
        self.模式框架.pack(pady=10)
        
        tk.Label(self.模式框架, text="選擇遊戲模式：", font=("微軟正黑體", 14)).pack()
        
        模式按鈕框 = tk.Frame(self.模式框架)
        模式按鈕框.pack(pady=10)
        
        單人按鈕 = tk.Button(模式按鈕框, text="單人模式（對電腦）", font=("微軟正黑體", 12),
                           bg="#3498db", fg="white", padx=20, pady=10,
                           command=lambda: self.選擇模式('single'))
        單人按鈕.pack(side=tk.LEFT, padx=5)
        
        雙人按鈕 = tk.Button(模式按鈕框, text="雙人模式", font=("微軟正黑體", 12),
                           bg="#2ecc71", fg="white", padx=20, pady=10,
                           command=lambda: self.選擇模式('double'))
        雙人按鈕.pack(side=tk.LEFT, padx=5)
        
        # 遊戲資訊框架
        self.資訊框架 = tk.Frame(self.root)
        
        # 分數顯示
        分數框架 = tk.Frame(self.資訊框架)
        分數框架.pack(pady=10)
        
        self.玩家1分數標籤 = tk.Label(分數框架, text="玩家1：0分", font=("微軟正黑體", 12), fg="#3498db")
        self.玩家1分數標籤.pack(side=tk.LEFT, padx=20)
        
        self.玩家2分數標籤 = tk.Label(分數框架, text="電腦：0分", font=("微軟正黑體", 12), fg="#e74c3c")
        self.玩家2分數標籤.pack(side=tk.LEFT, padx=20)
        
        # 當前字提示
        self.當前字標籤 = tk.Label(self.資訊框架, text="請輸入第一個詞語", 
                                   font=("微軟正黑體", 16, "bold"), fg="#e74c3c")
        self.當前字標籤.pack(pady=10)
        
        # 當前玩家提示
        self.玩家提示標籤 = tk.Label(self.資訊框架, text="", font=("微軟正黑體", 12), fg="#9b59b6")
        self.玩家提示標籤.pack(pady=5)
        
        # 輸入框架
        輸入框架 = tk.Frame(self.資訊框架)
        輸入框架.pack(pady=10)
        
        tk.Label(輸入框架, text="輸入詞語：", font=("微軟正黑體", 12)).pack(side=tk.LEFT)
        
        self.輸入框 = tk.Entry(輸入框架, font=("微軟正黑體", 14), width=15)
        self.輸入框.pack(side=tk.LEFT, padx=5)
        self.輸入框.bind('<Return>', lambda e: self.提交詞語())
        
        提交按鈕 = tk.Button(輸入框架, text="提交", font=("微軟正黑體", 12),
                            bg="#27ae60", fg="white", command=self.提交詞語)
        提交按鈕.pack(side=tk.LEFT, padx=5)
        
        # 歷史記錄
        tk.Label(self.資訊框架, text="詞語歷史：", font=("微軟正黑體", 12)).pack(pady=(20, 5))
        
        self.歷史文本 = scrolledtext.ScrolledText(self.資訊框架, height=12, width=50, 
                                                 font=("微軟正黑體", 11), state='disabled')
        self.歷史文本.pack(pady=5)
        
        # 控制按鈕
        按鈕框架 = tk.Frame(self.資訊框架)
        按鈕框架.pack(pady=10)
        
        重新開始按鈕 = tk.Button(按鈕框架, text="重新開始", font=("微軟正黑體", 12),
                               bg="#e67e22", fg="white", command=self.重新開始)
        重新開始按鈕.pack(side=tk.LEFT, padx=5)
        
        提示按鈕 = tk.Button(按鈕框架, text="提示", font=("微軟正黑體", 12),
                            bg="#9b59b6", fg="white", command=self.顯示提示)
        提示按鈕.pack(side=tk.LEFT, padx=5)
        
        規則按鈕 = tk.Button(按鈕框架, text="遊戲規則", font=("微軟正黑體", 12),
                            bg="#34495e", fg="white", command=self.顯示規則)
        規則按鈕.pack(side=tk.LEFT, padx=5)
    
    def 選擇模式(self, 模式):
        """選擇遊戲模式"""
        self.遊戲模式 = 模式
        self.模式框架.pack_forget()
        self.資訊框架.pack()
        
        if 模式 == 'single':
            self.玩家2分數標籤.config(text="電腦：0分")
            self.更新玩家提示()
        else:
            self.玩家2分數標籤.config(text="玩家2：0分")
            self.更新玩家提示()
        
        self.輸入框.focus()
    
    def 更新玩家提示(self):
        """更新當前玩家提示"""
        if self.遊戲模式 == 'single':
            self.玩家提示標籤.config(text="輪到你了！")
        else:
            self.玩家提示標籤.config(text=f"輪到玩家{self.當前玩家}！")
    
    def 提交詞語(self):
        """提交詞語"""
        詞語 = self.輸入框.get().strip()
        self.輸入框.delete(0, tk.END)
        
        if not 詞語:
            messagebox.showwarning("警告", "請輸入詞語！")
            return
        
        # 檢查詞語長度
        if len(詞語) < 2 or len(詞語) > 4:
            messagebox.showerror("錯誤", "詞語長度必須在2-4個字之間！")
            return
        
        # 檢查是否重複
        if 詞語 in self.已使用詞語:
            messagebox.showerror("錯誤", f"「{詞語}」已經使用過了！")
            return
        
        # 檢查接龍規則
        if self.當前字 and 詞語[0] != self.當前字:
            messagebox.showerror("錯誤", f"詞語必須以「{self.當前字}」開頭！")
            return
        
        # 詞語有效，加入記錄
        self.已使用詞語.append(詞語)
        self.當前字 = 詞語[-1]
        
        # 更新分數
        if self.遊戲模式 == 'single' or self.當前玩家 == 1:
            self.玩家分數 += len(詞語)
            self.玩家1分數標籤.config(text=f"玩家1：{self.玩家分數}分")
            玩家名 = "玩家1"
        else:
            self.電腦分數 += len(詞語)
            self.玩家2分數標籤.config(text=f"玩家2：{self.電腦分數}分")
            玩家名 = "玩家2"
        
        # 更新歷史
        self.更新歷史(f"{玩家名}：{詞語}")
        
        # 更新提示
        self.當前字標籤.config(text=f"下一個詞必須以「{self.當前字}」開頭")
        
        # 切換玩家或電腦回合
        if self.遊戲模式 == 'single':
            self.root.after(500, self.電腦回合)
        else:
            self.當前玩家 = 2 if self.當前玩家 == 1 else 1
            self.更新玩家提示()
    
    def 電腦回合(self):
        """電腦出詞"""
        if not self.當前字:
            return
        
        # 從詞庫中尋找可用的詞
        可用詞語 = []
        if self.當前字 in self.詞庫:
            for 詞 in self.詞庫[self.當前字]:
                if 詞 not in self.已使用詞語:
                    可用詞語.append(詞)
        
        if not 可用詞語:
            messagebox.showinfo("遊戲結束", f"電腦無法接龍！\n\n最終分數：\n玩家：{self.玩家分數}分\n電腦：{self.電腦分數}分\n\n你獲勝了！")
            self.重新開始()
            return
        
        # 隨機選擇一個詞
        電腦詞語 = random.choice(可用詞語)
        
        # 加入記錄
        self.已使用詞語.append(電腦詞語)
        self.當前字 = 電腦詞語[-1]
        
        # 更新分數
        self.電腦分數 += len(電腦詞語)
        self.玩家2分數標籤.config(text=f"電腦：{self.電腦分數}分")
        
        # 更新歷史
        self.更新歷史(f"電腦：{電腦詞語}")
        
        # 更新提示
        self.當前字標籤.config(text=f"下一個詞必須以「{self.當前字}」開頭")
        self.更新玩家提示()
    
    def 更新歷史(self, 文本):
        """更新歷史記錄"""
        self.歷史文本.config(state='normal')
        self.歷史文本.insert(tk.END, 文本 + '\n')
        self.歷史文本.see(tk.END)
        self.歷史文本.config(state='disabled')
    
    def 顯示提示(self):
        """顯示提示"""
        if not self.當前字:
            messagebox.showinfo("提示", "請先輸入第一個詞語！")
            return
        
        # 尋找可用的詞
        可用詞語 = []
        if self.當前字 in self.詞庫:
            for 詞 in self.詞庫[self.當前字]:
                if 詞 not in self.已使用詞語:
                    可用詞語.append(詞)
                    if len(可用詞語) >= 3:
                        break
        
        if 可用詞語:
            提示文本 = f"以「{self.當前字}」開頭的詞語提示：\n\n" + "、".join(可用詞語)
        else:
            提示文本 = f"詞庫中沒有以「{self.當前字}」開頭的詞語了！\n請自己想一個吧！"
        
        messagebox.showinfo("提示", 提示文本)
    
    def 顯示規則(self):
        """顯示遊戲規則"""
        規則 = """
        文字接龍遊戲規則：
        
        1. 輸入一個詞語（2-4個字）
        
        2. 下一個詞必須以上一個詞的
           最後一個字開頭
        
        3. 不能重複使用已經出現過的詞
        
        4. 單人模式：與電腦對戰，看誰
           先無法接龍
        
        5. 雙人模式：兩位玩家輪流出詞
        
        6. 每個詞的字數即為得分
        
        祝你遊戲愉快！
        """
        messagebox.showinfo("遊戲規則", 規則)
    
    def 重新開始(self):
        """重新開始遊戲"""
        self.已使用詞語 = []
        self.當前字 = None
        self.玩家分數 = 0
        self.電腦分數 = 0
        self.當前玩家 = 1
        
        self.玩家1分數標籤.config(text="玩家1：0分")
        
        if self.遊戲模式 == 'single':
            self.玩家2分數標籤.config(text="電腦：0分")
        else:
            self.玩家2分數標籤.config(text="玩家2：0分")
        
        self.當前字標籤.config(text="請輸入第一個詞語")
        self.歷史文本.config(state='normal')
        self.歷史文本.delete(1.0, tk.END)
        self.歷史文本.config(state='disabled')
        self.輸入框.delete(0, tk.END)
        self.輸入框.focus()
        self.更新玩家提示()

def main():
    root = tk.Tk()
    遊戲 = 文字接龍遊戲(root)
    root.mainloop()

if __name__ == "__main__":
    main()


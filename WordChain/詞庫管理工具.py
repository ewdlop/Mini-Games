#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
詞庫管理工具
用於方便地新增、查看、編輯詞庫
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import os

class 詞庫管理工具:
    def __init__(self, root):
        self.root = root
        self.root.title("文字接龍 - 詞庫管理工具")
        self.root.geometry("700x600")
        
        self.詞庫檔案 = "詞庫.txt"
        self.詞庫 = {}
        
        self.建立介面()
        self.載入詞庫()
        
    def 建立介面(self):
        """建立管理介面"""
        # 標題
        標題 = tk.Label(self.root, text="詞庫管理工具", 
                       font=("微軟正黑體", 20, "bold"), fg="#2c3e50")
        標題.pack(pady=15)
        
        # 統計資訊
        self.統計標籤 = tk.Label(self.root, text="", 
                                font=("微軟正黑體", 11), fg="#7f8c8d")
        self.統計標籤.pack(pady=5)
        
        # 新增詞語區域
        新增框架 = tk.LabelFrame(self.root, text="新增詞語", 
                                font=("微軟正黑體", 12, "bold"),
                                padx=10, pady=10)
        新增框架.pack(padx=20, pady=10, fill="x")
        
        輸入框架 = tk.Frame(新增框架)
        輸入框架.pack(pady=5)
        
        tk.Label(輸入框架, text="詞語：", font=("微軟正黑體", 11)).pack(side=tk.LEFT, padx=5)
        
        self.詞語輸入框 = tk.Entry(輸入框架, font=("微軟正黑體", 12), width=15)
        self.詞語輸入框.pack(side=tk.LEFT, padx=5)
        self.詞語輸入框.bind('<Return>', lambda e: self.新增詞語())
        
        新增按鈕 = tk.Button(輸入框架, text="新增", 
                            font=("微軟正黑體", 11),
                            bg="#27ae60", fg="white",
                            command=self.新增詞語)
        新增按鈕.pack(side=tk.LEFT, padx=5)
        
        提示 = tk.Label(新增框架, 
                       text="提示：輸入2-4個字的詞語，系統會自動根據首字分類",
                       font=("微軟正黑體", 9), fg="#7f8c8d")
        提示.pack(pady=5)
        
        # 查詢區域
        查詢框架 = tk.LabelFrame(self.root, text="查詢詞語", 
                                font=("微軟正黑體", 12, "bold"),
                                padx=10, pady=10)
        查詢框架.pack(padx=20, pady=10, fill="x")
        
        查詢輸入框架 = tk.Frame(查詢框架)
        查詢輸入框架.pack(pady=5)
        
        tk.Label(查詢輸入框架, text="首字：", 
                font=("微軟正黑體", 11)).pack(side=tk.LEFT, padx=5)
        
        self.查詢輸入框 = tk.Entry(查詢輸入框架, 
                                   font=("微軟正黑體", 12), width=5)
        self.查詢輸入框.pack(side=tk.LEFT, padx=5)
        self.查詢輸入框.bind('<Return>', lambda e: self.查詢詞語())
        
        查詢按鈕 = tk.Button(查詢輸入框架, text="查詢", 
                            font=("微軟正黑體", 11),
                            bg="#3498db", fg="white",
                            command=self.查詢詞語)
        查詢按鈕.pack(side=tk.LEFT, padx=5)
        
        # 顯示區域
        顯示框架 = tk.LabelFrame(self.root, text="詞庫內容", 
                                font=("微軟正黑體", 12, "bold"),
                                padx=10, pady=10)
        顯示框架.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.顯示文本 = scrolledtext.ScrolledText(顯示框架, 
                                                 height=15, 
                                                 font=("微軟正黑體", 10),
                                                 wrap=tk.WORD)
        self.顯示文本.pack(fill="both", expand=True)
        
        # 按鈕區域
        按鈕框架 = tk.Frame(self.root)
        按鈕框架.pack(pady=10)
        
        顯示全部按鈕 = tk.Button(按鈕框架, text="顯示全部", 
                               font=("微軟正黑體", 11),
                               bg="#9b59b6", fg="white",
                               command=self.顯示全部詞庫)
        顯示全部按鈕.pack(side=tk.LEFT, padx=5)
        
        重新載入按鈕 = tk.Button(按鈕框架, text="重新載入", 
                               font=("微軟正黑體", 11),
                               bg="#e67e22", fg="white",
                               command=self.載入詞庫)
        重新載入按鈕.pack(side=tk.LEFT, padx=5)
        
        匯出按鈕 = tk.Button(按鈕框架, text="匯出統計", 
                            font=("微軟正黑體", 11),
                            bg="#16a085", fg="white",
                            command=self.匯出統計)
        匯出按鈕.pack(side=tk.LEFT, padx=5)
    
    def 載入詞庫(self):
        """從文件載入詞庫"""
        self.詞庫 = {}
        try:
            if not os.path.exists(self.詞庫檔案):
                messagebox.showwarning("警告", f"找不到{self.詞庫檔案}文件！")
                return
            
            with open(self.詞庫檔案, 'r', encoding='utf-8') as f:
                for 行 in f:
                    行 = 行.strip()
                    if not 行:
                        continue
                    parts = 行.split('|')
                    if len(parts) >= 2:
                        首字 = parts[0]
                        詞語列表 = parts[1:]
                        self.詞庫[首字] = 詞語列表
            
            self.更新統計()
            messagebox.showinfo("成功", f"已載入詞庫！\n共{len(self.詞庫)}個首字")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"載入詞庫時發生錯誤：{str(e)}")
    
    def 儲存詞庫(self):
        """儲存詞庫到文件"""
        try:
            with open(self.詞庫檔案, 'w', encoding='utf-8') as f:
                # 按首字排序
                for 首字 in sorted(self.詞庫.keys()):
                    詞語列表 = self.詞庫[首字]
                    行 = 首字 + '|' + '|'.join(詞語列表) + '\n'
                    f.write(行)
            return True
        except Exception as e:
            messagebox.showerror("錯誤", f"儲存詞庫時發生錯誤：{str(e)}")
            return False
    
    def 新增詞語(self):
        """新增詞語到詞庫"""
        詞語 = self.詞語輸入框.get().strip()
        self.詞語輸入框.delete(0, tk.END)
        
        if not 詞語:
            messagebox.showwarning("警告", "請輸入詞語！")
            return
        
        if len(詞語) < 2 or len(詞語) > 4:
            messagebox.showerror("錯誤", "詞語長度必須在2-4個字之間！")
            return
        
        首字 = 詞語[0]
        
        # 檢查是否已存在
        if 首字 in self.詞庫:
            if 詞語 in self.詞庫[首字]:
                messagebox.showinfo("提示", f"詞語「{詞語}」已經存在！")
                return
            self.詞庫[首字].append(詞語)
        else:
            self.詞庫[首字] = [詞語]
        
        # 儲存到文件
        if self.儲存詞庫():
            messagebox.showinfo("成功", f"已新增詞語「{詞語}」\n首字：{首字}")
            self.更新統計()
            self.詞語輸入框.focus()
    
    def 查詢詞語(self):
        """查詢特定首字的詞語"""
        首字 = self.查詢輸入框.get().strip()
        
        if not 首字:
            messagebox.showwarning("警告", "請輸入要查詢的首字！")
            return
        
        if len(首字) > 1:
            首字 = 首字[0]
        
        self.顯示文本.delete(1.0, tk.END)
        
        if 首字 in self.詞庫:
            詞語列表 = self.詞庫[首字]
            內容 = f"以「{首字}」開頭的詞語（共{len(詞語列表)}個）：\n\n"
            內容 += "、".join(詞語列表)
            self.顯示文本.insert(tk.END, 內容)
        else:
            self.顯示文本.insert(tk.END, f"詞庫中沒有以「{首字}」開頭的詞語。")
    
    def 顯示全部詞庫(self):
        """顯示所有詞庫內容"""
        self.顯示文本.delete(1.0, tk.END)
        
        if not self.詞庫:
            self.顯示文本.insert(tk.END, "詞庫為空！")
            return
        
        總詞數 = sum(len(詞語列表) for 詞語列表 in self.詞庫.values())
        內容 = f"詞庫統計：{len(self.詞庫)}個首字，共{總詞數}個詞語\n\n"
        內容 += "=" * 60 + "\n\n"
        
        for 首字 in sorted(self.詞庫.keys()):
            詞語列表 = self.詞庫[首字]
            內容 += f"【{首字}】（{len(詞語列表)}個）：\n"
            內容 += "    " + "、".join(詞語列表) + "\n\n"
        
        self.顯示文本.insert(tk.END, 內容)
    
    def 更新統計(self):
        """更新統計資訊"""
        if not self.詞庫:
            self.統計標籤.config(text="詞庫為空")
            return
        
        總詞數 = sum(len(詞語列表) for 詞語列表 in self.詞庫.values())
        統計文本 = f"目前詞庫：{len(self.詞庫)} 個首字 | {總詞數} 個詞語"
        self.統計標籤.config(text=統計文本)
    
    def 匯出統計(self):
        """匯出詞庫統計資訊"""
        if not self.詞庫:
            messagebox.showinfo("提示", "詞庫為空，無法匯出統計！")
            return
        
        try:
            總詞數 = sum(len(詞語列表) for 詞語列表 in self.詞庫.values())
            
            統計內容 = "文字接龍詞庫統計報告\n"
            統計內容 += "=" * 50 + "\n\n"
            統計內容 += f"總計：{len(self.詞庫)} 個首字，{總詞數} 個詞語\n\n"
            統計內容 += "各首字詞語數量排行：\n"
            統計內容 += "-" * 50 + "\n"
            
            # 按詞語數量排序
            排序詞庫 = sorted(self.詞庫.items(), 
                            key=lambda x: len(x[1]), 
                            reverse=True)
            
            for 排名, (首字, 詞語列表) in enumerate(排序詞庫, 1):
                統計內容 += f"{排名:3d}. 【{首字}】 {len(詞語列表):3d} 個詞語\n"
            
            統計檔案 = "詞庫統計.txt"
            with open(統計檔案, 'w', encoding='utf-8') as f:
                f.write(統計內容)
            
            messagebox.showinfo("成功", f"統計資訊已匯出到「{統計檔案}」！")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"匯出統計時發生錯誤：{str(e)}")

def main():
    root = tk.Tk()
    工具 = 詞庫管理工具(root)
    root.mainloop()

if __name__ == "__main__":
    main()


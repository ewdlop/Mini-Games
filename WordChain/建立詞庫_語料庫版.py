#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
從 Hugging Face 中文語料庫建立詞庫
使用 NLTK 進行中文分詞和詞語提取
"""

import re
from collections import defaultdict
from datasets import load_dataset
import jieba
import nltk
from tqdm import tqdm

class 詞庫建立器:
    def __init__(self):
        self.詞庫 = defaultdict(set)
        self.詞頻統計 = defaultdict(int)
        
    def 是否為有效詞語(self, 詞):
        """檢查詞語是否有效"""
        # 長度檢查：2-4個字
        if len(詞) < 2 or len(詞) > 4:
            return False
        
        # 只包含中文字
        if not all('\u4e00' <= char <= '\u9fff' for char in 詞):
            return False
        
        # 排除常見停用詞開頭
        停用詞開頭 = ['這個', '那個', '什麼', '怎麼', '一個', '不是', '沒有', '可以', '如果']
        if 詞 in 停用詞開頭:
            return False
            
        return True
    
    def 從語料庫提取詞語_方法1(self, max_samples=10000):
        """
        方法1：從 Hugging Face 的 Chinese Wikipedia 語料庫提取
        """
        print("正在載入中文維基百科語料庫...")
        try:
            # 載入中文維基百科數據集（較小的樣本）
            dataset = load_dataset("graelo/wikipedia", "20230601.zh", split="train", streaming=True)
            
            print("開始提取詞語...")
            count = 0
            for item in tqdm(dataset, total=max_samples, desc="處理文章"):
                if count >= max_samples:
                    break
                    
                text = item['text']
                # 使用 jieba 分詞
                words = jieba.cut(text)
                
                for 詞 in words:
                    詞 = 詞.strip()
                    if self.是否為有效詞語(詞):
                        首字 = 詞[0]
                        self.詞庫[首字].add(詞)
                        self.詞頻統計[詞] += 1
                
                count += 1
                
        except Exception as e:
            print(f"載入維基百科數據集時發生錯誤：{e}")
            print("將嘗試其他數據源...")
    
    def 從語料庫提取詞語_方法2(self, max_samples=5000):
        """
        方法2：從 CLUECorpus 中文語料庫提取
        """
        print("正在載入 CLUE 中文語料庫...")
        try:
            # 載入 CLUE 語料庫
            dataset = load_dataset("clue", "csl", split="train[:5000]")
            
            print("開始提取詞語...")
            for item in tqdm(dataset, desc="處理樣本"):
                # 從摘要和關鍵詞提取
                if 'abst' in item:
                    text = item['abst']
                    words = jieba.cut(text)
                    
                    for 詞 in words:
                        詞 = 詞.strip()
                        if self.是否為有效詞語(詞):
                            首字 = 詞[0]
                            self.詞庫[首字].add(詞)
                            self.詞頻統計[詞] += 1
                
                if 'keyword' in item:
                    for 詞 in item['keyword']:
                        詞 = 詞.strip()
                        if self.是否為有效詞語(詞):
                            首字 = 詞[0]
                            self.詞庫[首字].add(詞)
                            self.詞頻統計[詞] += 1
                            
        except Exception as e:
            print(f"載入 CLUE 數據集時發生錯誤：{e}")
    
    def 從語料庫提取詞語_方法3(self, max_samples=5000):
        """
        方法3：從新聞語料庫提取
        """
        print("正在載入中文新聞語料庫...")
        try:
            # 載入中文新聞數據集
            dataset = load_dataset("shibing624/nli_zh", "STS-B", split="train[:5000]")
            
            print("開始提取詞語...")
            for item in tqdm(dataset, desc="處理新聞"):
                for field in ['sentence1', 'sentence2']:
                    if field in item and item[field]:
                        text = item[field]
                        words = jieba.cut(text)
                        
                        for 詞 in words:
                            詞 = 詞.strip()
                            if self.是否為有效詞語(詞):
                                首字 = 詞[0]
                                self.詞庫[首字].add(詞)
                                self.詞頻統計[詞] += 1
                                
        except Exception as e:
            print(f"載入新聞數據集時發生錯誤：{e}")
    
    def 合併現有詞庫(self, 檔案路徑="詞庫.txt"):
        """合併現有的詞庫文件"""
        print(f"正在合併現有詞庫：{檔案路徑}...")
        try:
            with open(檔案路徑, 'r', encoding='utf-8') as f:
                for 行 in f:
                    行 = 行.strip()
                    if not 行:
                        continue
                    parts = 行.split('|')
                    if len(parts) >= 2:
                        首字 = parts[0]
                        詞語列表 = parts[1:]
                        for 詞 in 詞語列表:
                            self.詞庫[首字].add(詞)
                            self.詞頻統計[詞] += 100  # 給現有詞庫較高權重
            print(f"已合併現有詞庫")
        except FileNotFoundError:
            print("未找到現有詞庫文件，將創建新詞庫")
        except Exception as e:
            print(f"合併詞庫時發生錯誤：{e}")
    
    def 過濾低頻詞語(self, 最小頻率=2):
        """過濾掉出現頻率太低的詞語"""
        print(f"過濾低於 {最小頻率} 次的詞語...")
        過濾前數量 = sum(len(詞語集) for 詞語集 in self.詞庫.values())
        
        for 首字 in list(self.詞庫.keys()):
            self.詞庫[首字] = {詞 for 詞 in self.詞庫[首字] 
                              if self.詞頻統計[詞] >= 最小頻率}
            if not self.詞庫[首字]:
                del self.詞庫[首字]
        
        過濾後數量 = sum(len(詞語集) for 詞語集 in self.詞庫.values())
        print(f"過濾完成：{過濾前數量} -> {過濾後數量} 個詞語")
    
    def 保存詞庫(self, 輸出檔案="詞庫_增強版.txt"):
        """保存詞庫到文件"""
        print(f"正在保存詞庫到 {輸出檔案}...")
        
        with open(輸出檔案, 'w', encoding='utf-8') as f:
            # 按首字排序
            for 首字 in sorted(self.詞庫.keys()):
                詞語列表 = sorted(list(self.詞庫[首字]))
                if 詞語列表:
                    行 = 首字 + '|' + '|'.join(詞語列表) + '\n'
                    f.write(行)
        
        print(f"詞庫已保存！")
        self.顯示統計()
    
    def 顯示統計(self):
        """顯示詞庫統計資訊"""
        總詞數 = sum(len(詞語集) for 詞語集 in self.詞庫.values())
        print("\n" + "=" * 60)
        print("詞庫統計資訊")
        print("=" * 60)
        print(f"首字數量：{len(self.詞庫)}")
        print(f"詞語總數：{總詞數}")
        print(f"平均每個首字的詞語數：{總詞數 / len(self.詞庫):.1f}")
        
        # 顯示前10個詞語最多的首字
        print("\n詞語數量前10的首字：")
        排序結果 = sorted(self.詞庫.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        for i, (首字, 詞語集) in enumerate(排序結果, 1):
            範例 = list(詞語集)[:5]
            print(f"{i:2d}. {首字}：{len(詞語集):3d} 個詞語 - 範例：{'、'.join(範例)}")
        print("=" * 60)

def main():
    print("=" * 60)
    print("文字接龍遊戲 - 詞庫建立工具（語料庫版）")
    print("=" * 60)
    print()
    
    建立器 = 詞庫建立器()
    
    # 先合併現有詞庫
    建立器.合併現有詞庫("詞庫.txt")
    
    print("\n請選擇語料庫來源：")
    print("1. 中文維基百科（推薦，但下載較慢）")
    print("2. CLUE 中文語料庫")
    print("3. 中文新聞語料庫")
    print("4. 全部（需要較長時間）")
    print("5. 只使用現有詞庫（跳過下載）")
    
    選擇 = input("\n請輸入選項 (1-5)：").strip()
    
    if 選擇 == '1':
        建立器.從語料庫提取詞語_方法1(max_samples=5000)
    elif 選擇 == '2':
        建立器.從語料庫提取詞語_方法2(max_samples=5000)
    elif 選擇 == '3':
        建立器.從語料庫提取詞語_方法3(max_samples=5000)
    elif 選擇 == '4':
        建立器.從語料庫提取詞語_方法1(max_samples=3000)
        建立器.從語料庫提取詞語_方法2(max_samples=3000)
        建立器.從語料庫提取詞語_方法3(max_samples=3000)
    elif 選擇 == '5':
        print("跳過語料庫下載...")
    else:
        print("無效選項，使用預設方法...")
        建立器.從語料庫提取詞語_方法3(max_samples=5000)
    
    # 過濾低頻詞語
    if 選擇 != '5':
        建立器.過濾低頻詞語(最小頻率=2)
    
    # 保存詞庫
    建立器.保存詞庫("詞庫_增強版.txt")
    
    print("\n完成！詞庫已保存為「詞庫_增強版.txt」")
    print("您可以：")
    print("1. 將「詞庫_增強版.txt」重新命名為「詞庫.txt」來使用新詞庫")
    print("2. 使用詞庫管理工具查看和編輯詞庫")

if __name__ == "__main__":
    main()


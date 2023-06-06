"""
title: accounting program

input:
    1. name: str
    2. main_ctgr: str | enum(int)
    3. sub_ctgr: str | enum(int)
    4. tag: str
    5. desc: str
    6. amount: int
    7. date: datetime.Datetime

example:
    name: "elden ring"
    main_ctgr: "entertainment"
    sub_ctgr: "game"
    tag: "steam"
    desc: str
    amount: 1290
    date: 2022/03/29
"""
import re
import datetime
import pandas as pd
# import numpy as np

# 將 date 格式統一
def reformat_date(date_str):
    patt_for_date = re.compile(r"[\/\.\-\,]")
    date_parts = re.split(patt_for_date, date_str)
    return "/".join(date_parts)

# 資料整理
data = pd.read_csv('記帳程式用 - 範例.csv')
data = data.fillna("na") # 填充字元
data = data.applymap(lambda x: x.lower() if isinstance(x, str) else x) # 轉小寫
data["amount"] = data["amount"].apply(lambda x: 0 if x=="na" else x) # amount 空格 賦予 0
data["date"] = data["date"].apply(lambda x: str( datetime.date.today() ) if x=="na" else  reformat_date(x)) # date 空格 賦予 今日

data.sort_values(by = ["date", "main_ctgr", "sub_ctgr"], inplace = True) # 針對日期排序
"""
為什麼不能這樣寫?
for i in data:
    print(i)
    data = data[i].str.lower()
"""
# print(df)
data.to_csv("記帳程式用 - 紀錄.csv", index = False)

import os

def open_file_with_vscode(file_path):
    try:
        os.system(file_path)
    except FileNotFoundError:
        print("无法找到VSCode安装路径，请确保已正确安装VSCode。")

# 用法示例
file_path = 'G:\Files\code\GitHub\accounting\記帳程式用 - 紀錄.csv'
open_file_with_vscode(file_path)
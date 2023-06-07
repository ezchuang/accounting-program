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

# csv 資料整理
def data_clean_up(path):
    data = pd.read_csv(path)
    data = data.fillna("na") # 填充字元
    data = data.applymap(lambda x: x.lower() if isinstance(x, str) else x) # 轉小寫
    data["amount"] = data["amount"].apply(lambda x: 0 if x=="na" else x) # amount 空格 賦予 0
    data["date"] = data["date"].apply(lambda x: str( datetime.date.today() ) if x=="na" else reformat_date(x)) # date 空格 賦予 今日
    data.sort_values(by = ["date", "main_ctgr", "sub_ctgr"], inplace = True) # 針對日期排序
    
    return data
    # print(df)

    """
    修改大小寫，為什麼不能這樣寫?
    for i in data:
        print(i)
        data = data[i].str.lower()
    """


input_mode_select, output_mode_select = "", ""

while True:
    # input_mode_select = input(
    #     "csv批次輸入 請輸入 0\n單筆資料輸入 請輸入 1\n輸入請選擇模式: "
    #     )
    # output_mode_select = input(
    #     "建立新的帳務檔案 請輸入 0\n新增資料到既有檔案 請輸入 1 (請確保既有檔案有放入此資料夾中，並將其命名為 \"記帳程式用-紀錄\")\n輸出請選擇模式: "
    #     )
    # 測試用
    input_mode_select="0"
    output_mode_select="0"

    if (input_mode_select == "0" or input_mode_select == "1") or\
        (output_mode_select == "0" or output_mode_select == "1"):
        break
    print("模式選擇異常")

# 輸入模式切換
if input_mode_select == "0": # input csv
    print("請將目標csv檔案與本程式放置於相同資料夾中")
    # path = input("請輸入csv檔案名稱: ")
    # 測試用
    path = "記帳程式用 - 範例"

    if ".csv" not in path:
        path += ".csv"
    data = data_clean_up(path)
else: # 個別資料 input
    print("尚未完成，完成期限遙遙無期")

# 輸出模式切換
if output_mode_select == "0": # 建立新檔案
    data.to_csv("記帳程式用-紀錄.csv", index = False)
    print("\033[92m" + "完成" + "\033[0m")
    print("\033[92m" + "新帳務檔案檔名為: 記帳程式用-紀錄.csv" + "\033[0m")
else: # 修改舊檔案
    path_be_modify = input("請輸入欲修改的檔案: ")
    with open(path_be_modify, mode = "a") as path_tmp:
        print("檔案不存在，自動新建")
        """
        mode = "a"，可用於 .to_csv() 中，此 arg 會同 open() 的設定方式，"a" 表示加在檔案內資料的後面

        .tell()，會 return 指向之記憶體位置，"==0" 表 path_tmp 為空或不存在，則需加入 header
        """
        data.to_csv(path_tmp, header = (path_tmp.tell() == 0), index = False)
    print("尚未完成")

# 呼叫資料
# if 



# 寫不出來，想要於完成後呼叫其他程式打開該檔案
# import subprocess

# def open_file_with_vscode(file_path):
#     try:
#         subprocess.Popen(['code', file_path])
#     except FileNotFoundError:
#         print("无法找到VSCode安装路径，请确保已正确安装VSCode。")

# # 用法示例
# file_path = 'G:\Files\code\GitHub\accounting\記帳程式用 - 紀錄.csv'
# open_file_with_vscode(file_path)
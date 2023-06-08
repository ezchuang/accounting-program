import re
import pandas as pd
import numpy
import datetime

from colorama import Fore 
from colorama import Style

# 個別輸入用
def data_input_func():
    data_input={
        "name" : [],
        "main_ctgr" : [],
        "sub_ctgr" : [],
        "tag" : [],
        "desc" : [],
        "amount" : [],
        "date" : [],
    }
    con_ipt = "0"
    while True:
        if con_ipt == "1":
            break
        elif con_ipt != "0":
            print(Fore.RED + Style.BRIGHT + "輸入異常" + Style.RESET_ALL)
            continue
        data_input["name"].append( input(Fore.CYAN + Style.BRIGHT + "請輸入 name : " + Style.RESET_ALL) )
        data_input["main_ctgr"].append( input(Fore.CYAN + Style.BRIGHT + "請輸入 main_ctgr : " + Style.RESET_ALL) )
        data_input["sub_ctgr"].append( input(Fore.CYAN + Style.BRIGHT + "請輸入 sub_ctgr : " + Style.RESET_ALL) )
        data_input["tag"].append( input(Fore.CYAN + Style.BRIGHT + "請輸入 tag : " + Style.RESET_ALL) )
        data_input["desc"].append(  input(Fore.CYAN + Style.BRIGHT + "請輸入 desc : " + Style.RESET_ALL) )
        data_input["amount"].append(  int( input(Fore.CYAN + Style.BRIGHT + "請輸入 amount : " + Style.RESET_ALL) ) )
        data_input["date"].append(  input(Fore.CYAN + Style.BRIGHT + "請輸入 date : " + Style.RESET_ALL) )
        con_ipt = input(Fore.CYAN + Style.BRIGHT + "是否要繼續輸入資料(是:0, 否:1): " + Style.RESET_ALL)
    data = pd.DataFrame(data_input)
    data["date"] = data["date"].apply(reformat_date)
    return data


# 將 date 格式統一
def reformat_date(date_str):
    # 本來就是空值
    if pd.isnull(date_str):
        return None
    # 建立 正規表達式 的 pattern，並套用
    patt_for_date = re.compile(r"[\/\.\-\,]")
    date_parts = re.split(patt_for_date, date_str)
    
    # 針對這種樣式的切版 -> 20230608
    if len(date_parts) == 1:
        # 數值異常，數字太少或太多
        if len(date_parts[0]) != 8:
            return None
        # 數值正常，切版
        else:
            date_parts = [date_parts[0][:4], date_parts[0][4:6], date_parts[0][6:]]

    # 數值超出正常範圍
    if not int(date_parts[0]) >= 0 or \
        not 0 <= int(date_parts[1]) <= 12 or \
        not 0 <= int(date_parts[2]) <= 31:
        return None
    elif int(date_parts[1]) in [2,4,6,9,11] and int(date_parts[2]) > 30:
        return None

    return "-".join(date_parts) # 2023/06/08


# csv 資料整理
def data_clean_up(path):
    data = pd.read_csv(path)
    data["date"] = data["date"].apply(reformat_date) # date 空格 賦予 今日
    return data
"""
舊資料
# df可以只輸出不是NAN的東西
    # data = data.fillna("na") # 填充字元
# numpy.NaN 處理 <- 調查一下
    # data = data.applymap(lambda x: x.lower() if isinstance(x, str) else x) # 轉小寫
    # 判斷時用s.lower()做比較
    # data["amount"] = data["amount"].apply(lambda x: 0 if x=="na" else x) # amount 空格 賦予 0
# 日期不要賦予今日
    # data["date"] = data["date"].apply(lambda x: str( datetime.date.today() ) if x=="na" else b_data_sum.reformat_date(x)) # date 空格 賦予 今日
    data.sort_values(by = ["date", "main_ctgr", "sub_ctgr"], inplace = True) # 針對日期排序
"""


# 統計 items 重複之處並統計(將 item 相同的 amount 相加)，回傳統計資料
def data_sum(data, item_name, time_start, time_end):
    num, date = "amount", "date"
    # 移除 na
    data_filtered = data[[item_name, num, date]].dropna(inplace = False)
    # 日期格式轉換
    data_filtered[date] = pd.to_datetime(data_filtered[date])
    # 篩選日期
    data_filtered = data_filtered[(data_filtered[date] >= time_start) & (data_filtered[date] <= time_end)]
    # 選出指定col
    data_filtered = data_filtered[ [item_name, num] ]
    
    # 若指定之 col 為 name 則不執行統計(加總)
    if item_name == "name":
        data_merged = data_filtered
    # 非 name 進行加總
    else:
        data_merged = data_filtered.groupby(data_filtered[item_name]) \
        .agg({item_name: 'first', num: 'sum'})
    """
    .groupby() 可依列分組(可多列)，會輪巡該列元素後分組，分組後 return
    .agg() 用於合併的操作，能在一個 .agg() 內執行多個功能 ex: .agg(['sum', 'mean', 'min', 'max'])
    上面 "else:" 內的函示等同
        1. 以 .groupby() 依 item_name (該col)分組
        2. 以 .agg() item_name 置入該組第一個值，num 置入該組各項總和
    """

    data_merged.sort_values(by = [num], inplace = True, ascending = False) # inplace，由大到小
    # 此時 index 項目會跟 item 內容一樣
    data_merged.reset_index(drop=True) # inplace，重置index

    return data_merged
"""
OOP測試
"""
import re
import pandas as pd
import numpy as np
import sys
import os
import textcolor

class General():
    # 日期格式化
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


class InputFileCmd():
    # csv批次輸入資料
    def Ipt_csv():
        path_ipt = input(textcolor.Color.mode_select("請輸入csv檔案名稱: "))
        # 副檔名確認
        if ".csv" not in path_ipt:
            path_ipt += ".csv"
        # 檔名搜不到檔案
        if not os.path.isfile(path_ipt):
            sys.exit(textcolor.Color.warning("無此檔案，本程式自動結束"))
        # csv 資料整理
        data = pd.read_csv(path_ipt)
        # 整理 date 格式
        data["date"] = data["date"].apply(General.reformat_date)
        return data
    
    # 個別輸入資料
    def Ipt_sep():
        item = ["name", "main_ctgr", "sub_ctgr", "tag", "desc", "amount", "date"]
        data_input={
            "name" : [],
            "main_ctgr" : [],
            "sub_ctgr" : [],
            "tag" : [],
            "desc" : [],
            "amount" : [],
            "date" : [],
        }
        cmd_dict_Ipt_sep ={"0","1"}
        con_ipt = "1"
        first_round = 1
        while con_ipt != "0":
            if first_round == 1:
                con_ipt = input( textcolor.Color.mode_select("是否要繼續輸入資料(是:0, 否:1): ") )
                first_round = 0
            if con_ipt not in cmd_dict_Ipt_sep:
                print(textcolor.Color.warning("輸入異常"))
                continue
            for i in item:
                data_input[i].append( input(textcolor.Color.mode_select(f"請輸入 {i} : ")) )
        data = pd.DataFrame(data_input)
        data["date"] = data["date"].apply(General.reformat_date)
        return data

    # 還沒用上
    def Ipt_Msg(self):
        if self == 1:
            return textcolor.Color.depiction("csv批次輸入 請輸入 0\n單筆資料輸入 請輸入 1\n") + \
                    textcolor.Color.mode_select("請選擇 輸入 模式: ")
        


"""
OOP測試
"""
import pandas as pd
import numpy as np
import sys
import os
import textcolor

class InputFileCmd():
    def Ipt(self):
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
        data["date"] = data["date"].apply(data_clean_up.reformat_date)
        return data
    
    def Ipt_sep():
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
        first_turn = 1
        while True:
            if first_turn != 1:
                con_ipt = input(textcolor.Color.mode_select("是否要繼續輸入資料(是:0, 否:1): "))
            if con_ipt == "1":
                break
            elif con_ipt != "0":
                print(textcolor.Color.warning("輸入異常"))
                continue
            data_input["name"].append( input(textcolor.Color.mode_select("請輸入 name : ")) )
            data_input["main_ctgr"].append( input(textcolor.Color.mode_select("請輸入 main_ctgr : ")) )
            data_input["sub_ctgr"].append( input(textcolor.Color.mode_select("請輸入 sub_ctgr : ")) )
            data_input["tag"].append( input(textcolor.Color.mode_select("請輸入 tag : ")) )
            data_input["desc"].append( input(textcolor.Color.mode_select("請輸入 desc : ")) )
            data_input["amount"].append( int( input(textcolor.Color.mode_select("請輸入 amount : ")) ) )
            data_input["date"].append( input(textcolor.Color.mode_select("請輸入 date : ")) )
            if first_turn == 1:
                first_turn = 0
        data = pd.DataFrame(data_input)
        data["date"] = data["date"].apply(reformat_date)
        return data


    def Ipt_Msg(self, msg):
        print(textcolor.Color.depiction(msg))
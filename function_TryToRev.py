"""
OOP測試
"""
import re
import pandas as pd
import numpy as np
import sys
import os
import textcolor

class General:
    # 日期格式化
    def Reformat_date(date_str):
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
    
    
    # 副檔名檢查
    def File_name_check(name):
        if ".csv" not in name:
            name += ".csv"

    # 檔案是否存在
    def File_exist(name):
        return os.path.isfile(name)


class InputFileCmd:
    # 共用 msg
    def Ipt_Msg(stage, mode):
        if stage == 1 and mode == "1":
            return textcolor.Color.depiction("csv批次輸入 請輸入 0\n單筆資料輸入 請輸入 1\n") + \
                    textcolor.Color.mode_select("請選擇 輸入 模式: ")
        elif stage == 2:
            if mode == "0":
                return textcolor.Color.warning("無此檔案，本程式自動結束")

        
    
    # csv批次輸入資料
    def Ipt_csv():
        path_ipt = input(textcolor.Color.mode_select("請輸入csv檔案名稱: "))
        # 副檔名確認
        General.File_name_check(path_ipt)
        # 檔名搜不到檔案
        if not General.File_exist(path_ipt):
            sys.exit(textcolor.Color.warning("無此檔案，本程式自動結束"))
        # csv 資料整理
        data = pd.read_csv(path_ipt)
        
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
        cmd_dict_Ipt_sep = {"0","1"}
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
                data_input[i].append( input(textcolor.Color.mode_select(f"請輸入 {i}: ")) )
        data = pd.DataFrame(data_input)
        
        return data

        

class OnputFileCmd():
    # 共用 msg
    def Opt_msg(stage, mode):
        if stage == 1:
            if mode == "0":
                return textcolor.Color.depiction(
                        "建立新的帳務檔案 請輸入 0\n" + 
                        "新增資料到既有檔案 請輸入 1 (請確保既有檔案有放入此資料夾中)\n" + 
                        "不另行儲存，只調取資料 請輸入 2\n"
                        ) + \
                        textcolor.Color.mode_select("請選擇 輸出 模式: ")
            elif mode == "1":
                return textcolor.Color.depiction(
                        "建立新的帳務檔案 請輸入 0\n" + 
                        "新增資料到既有檔案 請輸入 1 (請確保既有檔案有放入此資料夾中)\n"
                        ) + \
                        textcolor.Color.mode_select("請選擇 輸出 模式: ")
        elif stage == 2:
            if mode == "0":
                return textcolor.Color.mode_select("請輸入欲新增的檔案名稱: ")
            elif mode == "1":
                return textcolor.Color.mode_select("請輸入欲修改的檔案: ")
        elif stage == 3:
            if mode == "0":
                return textcolor.Color.finished_msg("完成") + "\n" + textcolor.Color.mode_select("新帳務檔案檔名為: ")
            elif mode == "1":
                return textcolor.Color.finished_msg("完成") + "\n" + textcolor.Color.mode_select("合併後檔案檔名為: ")
    
    # csv輸出
    def Opt_new(data):
        # 輸入檔名
        path_opt_new = input(OnputFileCmd.Opt_msg(2, "0"))
        # 確認副檔名
        General.File_name_check(path_opt_new)
        # 輸出成檔案
        data.to_csv(path_opt_new , index = False)
        # 列印完成資訊
        print(OnputFileCmd.Opt_msg(3, "0"))

    def Opt_rev(data):
        # 輸入檔名
        path_opt_new = input(OnputFileCmd.Opt_msg(2, "1"))
        # 確認副檔名
        General.File_name_check(path_opt_new)
def ipt_msg():
    cmd_dict = {
        "0": "csv批次輸入 請輸入 0",
        "1": "單筆資料輸入 請輸入 1",
    }
    return cmd_dict

def ipt_run(ipt_data):
    cmd_dict = {
        "0" : ipt_data.ipt_csv,
        "1" : ipt_data.ipt_sep,
    }
    return cmd_dict

def opt_msg(mode):
    cmd_dict = {
        "0": "建立新的帳務檔案 請輸入 0",
        "1": "新增資料到既有檔案 請輸入 1 (請確保既有檔案有放入此資料夾中)",
    }
    if mode == "1":
        cmd_dict["2"] = "不另行儲存，只調取資料 請輸入 2"
    return cmd_dict


def opt_run(opt_data, mode):
    cmd_dict = {
        "0" : opt_data.opt_new,
        "1" : opt_data.opt_rev,
    }
    if mode == "1":
        cmd_dict["2"] = "不另行儲存，只調取資料 請輸入 2"
    return cmd_dict

def show_data_mode_msg():
    cmd_dict = {
        "0" : "是請按 0",
        "1" : "否請按 1",
    }
    return cmd_dict

def show_data_select_msg():
    cmd_dict = {
        "0": "name (不分類，且個別輸出)請輸入 0",
        "1": "main category 請輸入 1",
        "2": "sub category 請輸入 2",
        "3": "tag 請輸入 3",
        "4": "date 請輸入 4",
        "5": "結束程序 請輸入 5",
    }
    return cmd_dict
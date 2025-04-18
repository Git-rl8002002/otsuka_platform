#!/usr/bin/python3
# -*- coding: UTF-8 -*-

檢查字串是否以https:// 開頭 python 程式碼

def check_url(url):
    if url.startswith("https://"):
        return True
    else:
        return False

# 測試函數
test_url = "https://www.example.com"
result = check_url(test_url)
print(result)  # Output: True

test_url = "http://www.example.com"
result = check_url(test_url)
print(result)  # Output: False

test_url = "www.example.com"
result = check_url(test_url)
print(result)  # Output: False



將整數陣列 or 列表 轉換為逗號隔開的字串

def list_to_comma_string(lst):
    # 將整數列表轉換為字符串列表
    str_list = [str(i) for i in lst]
    # 使用 join() 方法將字符串列表連接成一個逗號隔開的字符串
    return ",".join(str_list)

# 測試函數
int_list = [1, 2, 3, 4, 5]
result = list_to_comma_string(int_list)
print(result)  # Output: "1,2,3,4,5"



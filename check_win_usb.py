#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author   : JasonHung
# Date     : 20221102
# Update   : 20230919
# Function : otsuka factory import excel file

import pywinusb.hid as hid
import time , logging

########
# log
########
log_format = "%(asctime)s %(message)s"
logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")

# 定義回調函數，用於處理USB設備事件
def device_callback(data):
    if data.event_type == hid.HID_EVT_DEVICE_ARRIVAL:
        print("USB設備插入：{}".format(data.device.vendor_name))
    elif data.event_type == hid.HID_EVT_DEVICE_REMOVAL:
        print("USB設備拔出：{}".format(data.device.vendor_name))

# 創建USB設備監聽器
devices = hid.HidDeviceFilter().get_devices()
for device in devices:
    device.open()
    device.set_raw_data_handler(device_callback)

try:
    print("開始監聽USB設備事件，按Ctrl+C結束...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    # 關閉設備連接
    for device in devices:
        device.close()
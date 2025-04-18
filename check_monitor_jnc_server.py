#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author   : JasonHung
# Date     : 20221116
# Update   : 20230307
# Version  : 1.2
# Function : 大塚製藥 check JNC Server statistics

import time , pymysql , platform , os , smtplib , datetime , pysftp as sftp , sys
from pyModbusTCP.client import *
from control.jnc_dao import * 
from fpdf import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

################################################################################################################################################
#
# main content - monitor
#
################################################################################################################################################
class monitor():
    
    #########
    # init
    #########
    def __init__(self):
        pass
    
    #####################
    # check_jnc_server
    #####################
    def check_jnc_server_statistics(self):
        
        ##############
        # I6-1(品管)
        ##############
        i6_1 = ModbusClient(host=jnc_server['host'],port=jnc_server['port'],unit_id=jnc_server['i6-1'],auto_open=True,auto_close=True,debug=False)
        
        try:
            ### record time
            r_time    = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
            r_year    = time.strftime("%Y" , time.localtime())
            r_month   = time.strftime("%Y_%m" , time.localtime())
            r_day     = time.strftime("%Y-%m-%d" , time.localtime())
            pre_r_day = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")

            ### senser value
            i6_1_1_temp  = i6_1.read_input_registers(int(jnc_server['i6-1_1_temp'],16),1)
            i6_1_2_rh    = i6_1.read_input_registers(int(jnc_server['i6-1_2_rh'],16),1)
            i6_1_3_temp  = i6_1.read_input_registers(int(jnc_server['i6-1_3_temp'],16),1)
            i6_1_4_rh    = i6_1.read_input_registers(int(jnc_server['i6-1_4_rh'],16),1)
            i6_1_5_temp  = i6_1.read_input_registers(int(jnc_server['i6-1_5_temp'],16),1)
            i6_1_6_temp  = i6_1.read_input_registers(int(jnc_server['i6-1_6_temp'],16),1)
            i6_1_7_rh    = i6_1.read_input_registers(int(jnc_server['i6-1_7_rh'],16),1)
            i6_1_8_temp  = i6_1.read_input_registers(int(jnc_server['i6-1_8_temp'],16),1)
            i6_1_9_rh    = i6_1.read_input_registers(int(jnc_server['i6-1_9_rh'],16),1)
            i6_1_10_temp = i6_1.read_input_registers(int(jnc_server['i6-1_10_temp'],16),1)
            i6_1_11_rh   = i6_1.read_input_registers(int(jnc_server['i6-1_11_rh'],16),1)
            i6_1_12_temp = i6_1.read_input_registers(int(jnc_server['i6-1_12_temp'],16),1)
            i6_1_13_rh   = i6_1.read_input_registers(int(jnc_server['i6-1_13_rh'],16),1)
            i6_1_14_temp = i6_1.read_input_registers(int(jnc_server['i6-1_14_temp'],16),1)
            i6_1_15_rh   = i6_1.read_input_registers(int(jnc_server['i6-1_15_rh'],16),1)
            i6_1_16_temp = i6_1.read_input_registers(int(jnc_server['i6-1_16_temp'],16),1)
            i6_1_17_rh   = i6_1.read_input_registers(int(jnc_server['i6-1_17_rh'],16),1)
            i6_1_18_temp = i6_1.read_input_registers(int(jnc_server['i6-1_18_temp'],16),1)
            i6_1_19_rh   = i6_1.read_input_registers(int(jnc_server['i6-1_19_rh'],16),1)
            i6_1_20_temp = i6_1.read_input_registers(int(jnc_server['i6-1_20_temp'],16),1)
            i6_1_21_rh   = i6_1.read_input_registers(int(jnc_server['i6-1_21_rh'],16),1)
            
            ### print msg
            print('----------------------------------------------------------------------------------------------')
            print('I6-1 (品管)')
            print(r_time + ' , 中間品室 , \t' + ' Temperature : ' + str(i6_1_1_temp[0]/10) + ' °C , Humidity : ' + str(i6_1_2_rh[0]/10) + ' % ')
            print(r_time + ' , 樣品室-1(25°C) , \t' + ' Temperature : ' + str(i6_1_3_temp[0]/10) + ' °C , Humidity : ' + str(i6_1_4_rh[0]/10) + ' % ')
            print(r_time + ' , 樣品室-1(冰箱) , \t' + ' Temperature : ' + str(i6_1_5_temp[0]/10) + ' °C ')
            print(r_time + ' , 樣品室-2(30°C) , \t' + ' Temperature : ' + str(i6_1_6_temp[0]/10) + ' °C , Humidity : ' + str(i6_1_7_rh[0]/10) + ' % ')
            print(r_time + ' , 樣品室-3(30°C) , \t' + ' Temperature : ' + str(i6_1_8_temp[0]/10) + ' °C , Humidity : ' + str(i6_1_9_rh[0]/10) + ' % ')
            print(r_time + ' , 安全性實驗室-1 , \t'  + ' Temperature : ' + str(i6_1_10_temp[0]/10) + ' °C , Humidity : ' + str(i6_1_11_rh[0]/10) + ' % ')
            print(r_time + ' , 安全性實驗室-2 , \t'  + ' Temperature : ' + str(i6_1_12_temp[0]/10) + ' °C , Humidity : ' + str(i6_1_13_rh[0]/10) + ' % ')
            print(r_time + ' , 安全性實驗室-3 , \t'  + ' Temperature : ' + str(i6_1_14_temp[0]/10) + ' °C , Humidity : ' + str(i6_1_15_rh[0]/10) + ' % ')
            print(r_time + ' , 安全性實驗室-4 , \t'  + ' Temperature : ' + str(i6_1_16_temp[0]/10) + ' °C , Humidity : ' + str(i6_1_17_rh[0]/10) + ' % ')
            print(r_time + ' , 安全性實驗室-5 , \t'  + ' Temperature : ' + str(i6_1_18_temp[0]/10) + ' °C , Humidity : ' + str(i6_1_19_rh[0]/10) + ' % ')
            print(r_time + ' , 安全性實驗室-6 , \t'  + ' Temperature : ' + str(i6_1_20_temp[0]/10) + ' °C , Humidity : ' + str(i6_1_21_rh[0]/10) + ' % ')
            print('----------------------------------------------------------------------------------------------')
            
        except Exception as e:
            print('< Error > I6-1(品管) : ' + str(e) + '\n')
        finally:
            i6_1.close()
        
        ##############
        # I6-2(倉庫)
        ##############
        i6_2 = ModbusClient(host=jnc_server['host'],port=jnc_server['port'],unit_id=jnc_server['i6-2'],auto_open=True,auto_close=True,debug=False)
        
        try:
            ### record time
            r_time    = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
            r_year    = time.strftime("%Y" , time.localtime())
            r_month   = time.strftime("%Y_%m" , time.localtime())
            r_day     = time.strftime("%Y-%m-%d" , time.localtime())
            pre_r_day = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")

            ### senser value
            i6_2_1  = i6_2.read_input_registers(int(jnc_server['i6-2_1'],16),1)
            i6_2_2  = i6_2.read_input_registers(int(jnc_server['i6-2_2'],16),1)
            i6_2_3  = i6_2.read_input_registers(int(jnc_server['i6-2_3'],16),1)
            i6_2_4  = i6_2.read_input_registers(int(jnc_server['i6-2_4'],16),1)
            i6_2_5  = i6_2.read_input_registers(int(jnc_server['i6-2_5'],16),1)
            i6_2_6  = i6_2.read_input_registers(int(jnc_server['i6-2_6'],16),1)
            i6_2_7  = i6_2.read_input_registers(int(jnc_server['i6-2_7'],16),1)
            i6_2_8  = i6_2.read_input_registers(int(jnc_server['i6-2_8'],16),1)
            i6_2_9  = i6_2.read_input_registers(int(jnc_server['i6-2_9'],16),1)
            i6_2_10 = i6_2.read_input_registers(int(jnc_server['i6-2_10'],16),1)
            i6_2_11 = i6_2.read_input_registers(int(jnc_server['i6-2_11'],16),1)
            i6_2_12 = i6_2.read_input_registers(int(jnc_server['i6-2_12'],16),1)
            i6_2_13 = i6_2.read_input_registers(int(jnc_server['i6-2_13'],16),1)
            i6_2_14 = i6_2.read_input_registers(int(jnc_server['i6-2_14'],16),1)
            i6_2_15 = i6_2.read_input_registers(int(jnc_server['i6-2_15'],16),1)
            i6_2_16 = i6_2.read_input_registers(int(jnc_server['i6-2_16'],16),1)
            i6_2_17 = i6_2.read_input_registers(int(jnc_server['i6-2_17'],16),1)
            i6_2_18 = i6_2.read_input_registers(int(jnc_server['i6-2_18'],16),1)
            i6_2_19 = i6_2.read_input_registers(int(jnc_server['i6-2_19'],16),1)
            i6_2_20 = i6_2.read_input_registers(int(jnc_server['i6-2_20'],16),1)
            i6_2_21 = i6_2.read_input_registers(int(jnc_server['i6-2_21'],16),1)
            i6_2_22 = i6_2.read_input_registers(int(jnc_server['i6-2_22'],16),1)
            i6_2_23 = i6_2.read_input_registers(int(jnc_server['i6-2_23'],16),1)
            i6_2_24 = i6_2.read_input_registers(int(jnc_server['i6-2_24'],16),1)
            i6_2_25 = i6_2.read_input_registers(int(jnc_server['i6-2_25'],16),1)
            i6_2_26 = i6_2.read_input_registers(int(jnc_server['i6-2_26'],16),1)
            
            ### print msg
            print('I6-2 (倉庫)')
            print(r_time + ' , 製品三倉        , \t' + ' Temperature : ' + str(i6_2_1[0]/10) + ' °C , Humidity : ' + str(i6_2_2[0]/10) + ' °C ')
            print(r_time + ' , 製品倉庫(一)25°C , \t' + ' Temperature : ' + str(i6_2_3[0]/10) + ' °C , Humidity : ' + str(i6_2_4[0]/10) + ' % ')
            print(r_time + ' , 製品倉庫(一)30°C , \t' + ' Temperature : ' + str(i6_2_5[0]/10) + ' °C , Humidity : ' + str(i6_2_6[0]/10) + ' % ')
            print(r_time + ' , 原料倉(一)      , \t' + ' Temperature : ' + str(i6_2_7[0]/10) + ' °C , Humidity : ' + str(i6_2_8[0]/10) + ' % ')
            print(r_time + ' , 製品倉C(三)30°C , \t' + ' Temperature : ' + str(i6_2_9[0]/10) + ' °C , Humidity : ' + str(i6_2_10[0]/10) + ' % ')
            print(r_time + ' , 製品倉B(三)30°C , \t' + ' Temperature : ' + str(i6_2_11[0]/10) + ' °C , Humidity : ' + str(i6_2_12[0]/10) + ' % ')
            print(r_time + ' , 製品倉庫(三)25°C , \t' + ' Temperature : ' + str(i6_2_13[0]/10) + ' °C , Humidity : ' + str(i6_2_14[0]/10) + ' % ')
            print(r_time + ' , 製品倉A(三)25°C , \t' + ' Temperature : ' + str(i6_2_15[0]/10) + ' °C , Humidity : ' + str(i6_2_16[0]/10) + ' % ')
            print(r_time + ' , 製品倉庫(二)    , \t' + ' Temperature : ' + str(i6_2_17[0]/10) + ' °C , Humidity : ' + str(i6_2_18[0]/10) + ' % ')
            print(r_time + ' , 原料倉(二)      , \t' + ' Temperature : ' + str(i6_2_19[0]/10) + ' °C , Humidity : ' + str(i6_2_20[0]/10) + ' % ')
            print(r_time + ' , 物料倉庫        , \t' + ' Temperature : ' + str(i6_2_21[0]/10) + ' °C , Humidity : ' + str(i6_2_22[0]/10) + ' % ')
            print(r_time + ' , 退貨品倉庫      , \t' + ' Temperature : ' + str(i6_2_23[0]/10) + ' °C , Humidity : ' + str(i6_2_24[0]/10) + ' % ')
            print(r_time + ' , unknow          , \t' + ' Temperature : ' + str(i6_2_25[0]/10) + ' °C , Humidity : ' + str(i6_2_26[0]/10) + ' % ')
            
            print('----------------------------------------------------------------------------------------------')
            
        except Exception as e:
            print('< Error > I6-2(倉庫) : ' + str(e) + '\n')
        finally:
            i6_2.close()
    

################################################################################################################################################
#
# start
#
################################################################################################################################################
if __name__ == '__main__':

    check_jnc_server = monitor()

    if len(sys.argv) < 2:
        print("\n")
        print("#####################################################################################################")
        print("# 大塚製藥")
        print("# usage : (即時抓 JNC Server 上 I6-1 , I6-2 感測器數值)")
        print("# \t check_monitor_jnc_server.py")
        print("#")
        print("#####################################################################################################")
        check_jnc_server.check_jnc_server_statistics()
    else:
        check_jnc_server.check_jnc_server_statistics()
        

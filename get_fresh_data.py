#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author   : JasonHung
# Date     : 20221102
# Update   : 20240221
# Function : TWOP get data program

from control.config.config import parameter
from control.web_cloud_dao import *
from datetime import datetime , date , timedelta

from ldap3 import Server, Connection, ALL, NTLM, SAFE_SYNC
from ldap3.core.exceptions import LDAPException 

from pyVim import connect
from pyVmomi import vim
from tqdm import tqdm

import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import mimetypes

import ssl , socket
import pandas as pd
import pymysql , logging , pyodbc , csv , sys , os , json , requests , calendar , pymssql , mysql.connector , asyncio , aiomysql , time , shutil

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime, timedelta




########
# log
########
log_format = "%(asctime)s %(message)s"
logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")

#######################################
#
# factory card reader 大門 txt to HRM
#
#######################################
class fa_card_reader_main_door_txt:

    #########
    # init
    #########
    def __init__(self):
        try:
            self.fa_main_door_card_reader_txt()
            
        except Exception as e:
            logging.error('< Error > fa_card_reader_main_door_txt init : ' + str(e))
        finally:
            pass
   
    #################################
    # fa_main_door_card_reader_txt
    #################################
    def fa_main_door_card_reader_txt(self):
        try:
            mysql_93_conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
            mysql_93_curr = mysql_93_conn.cursor()

            ### variable
            r_day     = time.strftime("%Y%m%d" , time.localtime())
            sql_day   = time.strftime("%Y-%m-%d" , time.localtime())
            sql_month = time.strftime("%Y%m" , time.localtime())
            r_time    = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
            day_file  = 'txt/factory_card_reader/FA'+r_day+'.txt'
            
            sql = f"SELECT date_format(r_date , '%Y%m%d') , r_time , p_id , e_id , position , c_action , e_name , c_id , c_remark FROM `card_reader_{sql_month}` WHERE r_date='{sql_day}' and p_name='大門' order by r_time asc"
            mysql_93_curr.execute(sql)
            mysql_93_res = mysql_93_curr.fetchall()  
            
            with open(day_file , 'w' , encoding='utf-8') as file:
                print(f'------------------------------------------------------------------------------ start : {r_time}')
                for val in mysql_93_res:
                    add_content  = str(val).replace('\'','').replace('(','').replace(')','')
                    print(f"{add_content}")
                    file.write(add_content + '\n')
                print(f'------------------------------------------------------------------------------ stop : {r_time}')
            file.close()

        except Exception as e:
            logging.error("< Error > fa_main_door_card_reader_txt : " + str(e))

        finally:
            mysql_93_curr.close()
            mysql_93_conn.close()


#######################
#
# COMODO device list 
#
#######################
class device_list:

    #########
    # init
    #########
    def __init__(self):
        try:
            self.update_device_list()
            
        except Exception as e:
            logging.error('< Error > device list init : ' + str(e))
        finally:
            pass
   
    #####################
    # update_day_money
    #####################
    def update_device_list(self):
        try:
            self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
            self.curr = self.conn.cursor()
            
            print("------------------------------------------------------------------------------------------------------------------\n")

            ####################    
            # import csv file
            ####################
            
            ### 檢查檔案資料夾最新的檔案
            if sys.platform.startswith('win'):
                folder_path = 'C:/Jason_python/otsuka_factory_work_time_record/device_list'
                
            elif sys.platform.startswith('darwin'):
                folder_path = '/home/otsuka/otsuka_platform/device_list/'
                #folder_path = 'F:/otsuka/Git/otsuka_factory_work_time_record/device_list' 

            files = os.listdir(folder_path)
            files = [f for f in files if os.path.isfile(os.path.join(folder_path , f))]

            if files:
                latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))

                if sys.platform.startswith('win'):
                    # 正式機
                    csv_file    = 'C:/Jason_python/otsuka_factory_work_time_record/device_list/' + latest_file
                elif sys.platform.startswith('darwin'):
                    # 開發機
                    #csv_file = "F:/otsuka/Git/otsuka_factory_work_time_record/device_list/" + latest_file
                    csv_file = '/home/otsuka/otsuka_platform/device_list/' + latest_file
                
                with open(csv_file , 'r' , encoding='utf-8') as device_list_csv:
                    csv_reader = csv.reader(device_list_csv)

                    for val in csv_reader:

                        r_date     = val[10]
                        r_year     = val[10][0:4]
                        r_month    = val[10][5:7]
                        r_day      = val[10][8:10]
                        r_now_time = val[10][11:22]

                        search_sql = f"select * from device_list where d_name='{val[2]}' and l_activity='{val[10]}'"
                        self.curr.execute(search_sql)
                        s_res = self.curr.fetchone()

                        #logging.info(f"{search_sql}")

                        if s_res is None:
                            
                            if str(r_now_time) != 'ty':
                                time_24h   = datetime.strptime(r_now_time , "%I:%M:%S %p").strftime("%H:%M:%S")
                                l_activity = r_year + '-' + r_month + '-' + r_day + ' ' + time_24h
                                
                                device_sql  = f"insert into device_list("
                                device_sql += f"os          , d_status   , d_name     , c_s_status , p_status   , a_p_count , "
                                device_sql += f"customer    , d_group    , l_l_i_user , d_owner    , l_activity , o_name , "
                                device_sql += f"o_ver       , ccs_ver    , ccc_ver    , e_ip       , i_ip       , a_ldap , "
                                device_sql += f"d_workgroup , model      , processor  , s_number   , s_model    , s_manu , "
                                #device_sql += f"o_type      , registered , l_t_zone   , s_pack     , r_time     , r_reason , "
                                device_sql += f"o_type      , registered , l_t_zone   , s_pack     , r_time     , "
                                device_sql += f"cpu_usage   ,  ram_usage , net_usage  , disk_usage , s_profiles , r_date , r_year , r_month , r_day , r_now_time"
                                device_sql += f") value("
                                device_sql += f"'{val[0]}','{val[1]}','{val[2]}','{val[3]}','{val[4]}','{val[5]}' , "
                                device_sql += f"'{val[6]}','{val[7]}','{val[8]}','{val[9]}','{l_activity}','{val[11]}' , "
                                device_sql += f"'{val[12]}','{val[13]}','{val[14]}','{val[15]}','{val[16]}','{val[17]}' , "
                                device_sql += f"'{val[18]}','{val[19]}','{val[20]}','{val[21]}','{val[22]}','{val[23]}' , "
                                #device_sql += f"'{val[24]}','{val[25]}','{val[26]}','{val[27]}','{val[28]}','{val[29]}' , "
                                device_sql += f"'{val[24]}','{val[25]}','{val[26]}','{val[27]}','{val[28]}' , "
                                device_sql += f"'{val[30]}/{val[31]}','{val[32]}/{val[33]}/{val[34]}','{val[35]}','{val[36]}/{val[37]}','{val[38]}' , '{r_date}' , '{r_year}' , '{r_month}' , '{r_day}' , '{time_24h}'"
                                device_sql += f")"

                                #logging.info(f"{device_sql}")

                                self.curr.execute(device_sql)
                                self.conn.commit()

                logging.info(f"< Msg > {latest_file} , update 電腦使用紀錄 更新完成。.")
                print("------------------------------------------------------------------------------------------------------------------")

        except Exception as e:
            logging.error("< Error > update_device_list : " + str(e))

        finally:
            self.curr.close()
            self.conn.close()

#####################
#
# work schuled img
#            
#####################         
'''
class work_schuled_img:
    # 創建模擬數據
    data = {
        'Task': ['Task 1', 'Task 2', 'Task 3', 'Task 4'],
        'Start': [datetime(2024, 6, 1), datetime(2024, 6, 5), datetime(2024, 6, 10), datetime(2024, 6, 15)],
        'End': [datetime(2024, 6, 4), datetime(2024, 6, 9), datetime(2024, 6, 14), datetime(2024, 6, 20)],
        'Status': ['Completed', 'In Progress', 'Not Started', 'In Progress']
    }

    df = pd.DataFrame(data)

    # 設置顏色
    colors = {'Completed': 'green', 'In Progress': 'orange', 'Not Started': 'red'}

    # 設置圖形
    fig, ax = plt.subplots(figsize=(10, 5))

    # 繪製甘特圖
    for idx, row in df.iterrows():
        ax.barh(row['Task'], (row['End'] - row['Start']).days, left=row['Start'], height=0.5, align='center', color=colors[row['Status']])

    # 設置日期格式
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # 設置標題和標籤
    plt.title('甘特圖')
    plt.xlabel('日期')
    plt.ylabel('任務')

    # 添加圖例
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in colors]
    plt.legend(handles, colors.keys())

    # 自動調整日期標籤
    fig.autofmt_xdate()

    # 顯示圖表
    plt.show()
'''   

####################
#
# day money oil
#
####################
class day_money_oil:

    #########
    # inito
    #########
    def __init__(self):
        try:
            self.bpm_day_money_oil()
            
        except Exception as e:
            logging.error('< Error > day money oil init : ' + str(e))
        finally:
            pass
   
    ###########################
    # update_day_money_oil
    ###########################
    def update_day_money_oils(self):
        try:
                    self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    self.curr = self.conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    #month = '0' + month if int(month) < 10 else month

                    # all day by month 
                    name_sql = f"select a_name from day_money_oil where day_r_year='2023' and day_r_month='09' group by a_name order by day_r_day asc"
                    self.curr.execute(name_sql)
                    name_res = self.curr.fetchall() 

                    for name_val in name_res:
                        
                        day_sql = f"select day_r_day from day_money_oil where day_r_year='2023' and day_r_month='09' group by day_r_day order by day_r_day asc"
                        self.curr.execute(day_sql)
                        day_res = self.curr.fetchall()

                        for day_val in day_res:
                             
                             search_sql = f"select * from day_money_oil where day_r_year='2023' and day_r_month='09' and day_r_day='{day_val[0]}' and a_name='{name_val[0]}'"
                             self.curr.execute(search_sql)
                             search_res = self.curr.fetchone()

                             if search_res is None:
                                add_sql = f"insert into day_money_oil(day_r_year , day_r_month , day_r_day , a_name , day_t_money) value('2023','09','{day_val[0]}','{name_val[0]}','0')"
                                self.curr.execute(add_sql)  
                    
                    #return day_res
                    self.conn.commit()
                    logging.info('< Msg > synchronization update day money tolls 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

        except Exception as e:
            logging.error("< Error > connect mysql fail (update_day_money_oil) : " + str(e))

        finally:
            self.curr.close()
            self.conn.close()

    ##########################
    # bpm_day_money_traffic
    ##########################
    def bpm_day_money_oil(self):
        
        try:    
                if sys.platform.startswith('win'):
                    conn_str = f"DRIVER={{SQL Server}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                
                conn_mssql = pyodbc.connect(conn_str)
                curr_mssql = conn_mssql.cursor()  
                #sql = f"select ITEM14 , ITEM72 , ITEM15 , ITEM12 from ART00721676130332682_INS where ITEM26='true' and ITEM44='true' order by ITEM12 desc"
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                #############################
                sql  = f"select ITEM14 , ITEM51 , ITEM15 , ITEM12 , ITEM58 , ITEM57 , ITEM107 from ART00851684549915660_INS where ITEM75='true' and ITEM18='true'" 
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                # table : ART00851684549915660ITEM53
                # ITEM1:日期
                # ITEM3:日當
                # ITEM4:交通費
                # ITEM5:超里程
                # ITEM6:停車費
                # ITEM7:過路費
                # ITEM8:車票
                # ITEM9: Taxi
                # ITEM10:住宿
                # ITEM11:其他
                # ITEM12:油單
                # ITEM14:註記原因
                # ITEM15:加減金額
                #
                #############################
                sql2  = f"select a.ITEM14 , a.ITEM51 , a.ITEM15 , a.ITEM12 , a.ITEM58 , a.ITEM57 , a.ITEM107 , b.ITEM1 , b.ITEM12 , b.ITEM14 , b.ITEM15 " 
                sql2 += f"from ART00851684549915660_INS a left join ART00851684549915660ITEM53 b on a.INSID=b.INSID " 
                sql2 += f"where a.ITEM75='true' and a.ITEM18='true' and b.ITEM12 != '0' "
                curr_mssql.execute(sql2)
                res  = curr_mssql.fetchall()

                try:
                    conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    curr = conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    for val in res:
                        
                        #logging.info(f"{val[0]} , {val[1]} , {val[2]} , {val[3]}")
                        
                        r_year      = val[3][0:4]
                        r_month     = val[3][5:7]
                        r_day       = val[3][8:10]
                        day_r_year  = val[7][0:4]
                        day_r_month = val[7][5:7]
                        day_r_day   = val[7][8:10]
                        
                        ###############################################
                        #
                        # Check if there are records in the database
                        #
                        ###############################################
                        #s_mysql_sql = f"select * from day_money where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_date='{val[7]}' and day_t_money='{val[8]}'"
                        #s_mysql_sql = f"select * from day_money_oil where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"
                        s_mysql_sql = f"select * from day_money_oil where f_name='{val[0]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"

                        curr.execute(s_mysql_sql)
                        mysql_res = curr.fetchone()

                        #logging.info(s_mysql_sql)
                        #exit()

                        day_money = val[8]

                        #####################################
                        #
                        # get english name by chinese name
                        #
                        #####################################
                        g_e_mysql_sql = f"select employee_eng_name from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_e_mysql_sql)
                        g_e_name = curr.fetchone()

                        g_d_mysql_sql = f"select department_code from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_d_mysql_sql)
                        g_d_name = curr.fetchone()

                        if mysql_res is None:
                            
                            mysql_sql  = f"insert into day_money_oil("
                            mysql_sql += f"r_date , r_year , r_month , r_day , " 
                            mysql_sql += f"f_name , a_name , e_name  , d_name , t_money , c_t_money , erp_num , " 
                            mysql_sql += f"form_num , day_r_year , day_r_month , day_t_money , day_money_mark , day_money_diff" 
                            mysql_sql += f") " 
                            mysql_sql += f"value(" 
                            mysql_sql += f"'{val[3]}' , '{r_year}'     , '{r_month}'     , '{r_day}'  , "
                            mysql_sql += f"'{val[0]}' , '{val[1]}'     , '{g_e_name[0]}' , '{g_d_name[0]}' , '{val[2]}' , '{val[4]}' , '{val[5]}' ," 
                            mysql_sql += f"'{val[6]}' , '{day_r_year}' , '{day_r_month}' , '{0}' , '{val[9]}' , '{val[10]}'" 
                            mysql_sql += f")"
                            curr.execute(mysql_sql)
                            conn.commit()

                            #logging.info(f"{mysql_sql}") 
                            #logging.info(f"新日當資料 > 表單日期 : {val[3]} , 填表人 : {val[0]} , 申請人 : {val[1]} {g_e_name[0]} , 總金額 : {val[2]} , 日當日期 : {val[7]} , 日當金額 : {val[8]} , 註記原因 : {val[9]} , 加減金額 : {val[10]}")
                        
                        elif str(day_r_day) == '01':
                            mysql_sql  = f"update day_money_oil set day_t_money1='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            #logging.info(f"{mysql_sql}") 
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '02':
                            mysql_sql  = f"update day_money_oil set day_t_money2='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '03':
                            mysql_sql  = f"update day_money_oil set day_t_money3='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '04':
                            mysql_sql  = f"update day_money_oil set day_t_money4='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '05':
                            mysql_sql  = f"update day_money_oil set day_t_money5='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '06':
                            mysql_sql  = f"update day_money_oil set day_t_money6='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '07':
                            mysql_sql  = f"update day_money_oil set day_t_money7='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '08':
                            mysql_sql  = f"update day_money_oil set day_t_money8='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '09':
                            mysql_sql  = f"update day_money_oil set day_t_money9='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '10':
                            mysql_sql  = f"update day_money_oil set day_t_money10='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '11':
                            mysql_sql  = f"update day_money_oil set day_t_money11='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '12':
                            mysql_sql  = f"update day_money_oil set day_t_money12='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '13':
                            mysql_sql  = f"update day_money_oil set day_t_money13='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '14':
                            mysql_sql  = f"update day_money_oil set day_t_money14='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '15':
                            mysql_sql  = f"update day_money_oil set day_t_money15='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '16':
                            mysql_sql  = f"update day_money_oil set day_t_money16='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '17':
                            mysql_sql  = f"update day_money_oil set day_t_money17='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '18':
                            mysql_sql  = f"update day_money_oil set day_t_money18='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '19':
                            mysql_sql  = f"update day_money_oil set day_t_money19='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '20':
                            mysql_sql  = f"update day_money_oil set day_t_money20='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '21':
                            mysql_sql  = f"update day_money_oil set day_t_money21='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '22':
                            mysql_sql  = f"update day_money_oil set day_t_money22='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '23':
                            mysql_sql  = f"update day_money_oil set day_t_money23='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '24':
                            mysql_sql  = f"update day_money_oil set day_t_money24='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '25':
                            mysql_sql  = f"update day_money_oil set day_t_money25='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '26':
                            mysql_sql  = f"update day_money_oil set day_t_money26='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '27':
                            mysql_sql  = f"update day_money_oil set day_t_money27='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '28':
                            mysql_sql  = f"update day_money_oil set day_t_money28='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '29':
                            mysql_sql  = f"update day_money_oil set day_t_money29='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '30':
                            mysql_sql  = f"update day_money_oil set day_t_money30='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '31':
                            mysql_sql  = f"update day_money_oil set day_t_money31='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        mysql_sql  = f"update day_money_oil set day_t_total=("
                        mysql_sql += f"day_t_money1+day_t_money2+day_t_money3+day_t_money4+day_t_money5+day_t_money6+day_t_money7+day_t_money8+day_t_money9+day_t_money10+"
                        mysql_sql += f"day_t_money11+day_t_money12+day_t_money13+day_t_money14+day_t_money15+day_t_money16+day_t_money17+day_t_money18+day_t_money19+day_t_money20+"
                        mysql_sql += f"day_t_money21+day_t_money22+day_t_money23+day_t_money24+day_t_money25+day_t_money26+day_t_money27+day_t_money28+day_t_money29+day_t_money30+day_t_money31"
                        mysql_sql += f") "
                        mysql_sql += "where "
                        mysql_sql += f"r_date='{val[3]}'   and r_year='{r_year}'         and r_month='{r_month}'         and r_day='{r_day}'           and " 
                        mysql_sql += f"f_name='{val[0]}'   and a_name='{val[1]}'         and e_name='{g_e_name[0]}'      and t_money='{val[2]}'        and c_t_money='{val[4]}'      and erp_num='{val[5]}' and " 
                        mysql_sql += f"form_num='{val[6]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' and day_money_mark='{val[9]}' and day_money_diff='{val[10]}'" 
                        
                        curr.execute(mysql_sql)
                        conn.commit()
                    
                    logging.info('< Msg > update BPM day money 日當油單 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

                except Exception as e:
                    logging.error("< Error > bpm_day_money_oil - connect mysql fail : " + str(e))

                finally:
                    curr.close()
                    conn.close()

        except Exception as e:
            logging.error("< Error > bpm_day_money_oil - connect mssql fail : " + str(e))

        finally:
            curr_mssql.close()
            conn_mssql.close()

####################
#
# day money other
#
####################
class day_money_other:

    #########
    # init
    #########
    def __init__(self):
        try:
            self.bpm_day_money_other()
            
        except Exception as e:
            logging.error('< Error > day money other init : ' + str(e))
        finally:
            pass
   
    ###########################
    # update_day_money_other
    ###########################
    def update_day_money_other(self):
        try:
                    self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    self.curr = self.conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    #month = '0' + month if int(month) < 10 else month

                    # all day by month 
                    name_sql = f"select a_name from day_money_other where day_r_year='2023' and day_r_month='09' group by a_name order by day_r_day asc"
                    self.curr.execute(name_sql)
                    name_res = self.curr.fetchall() 

                    for name_val in name_res:
                        
                        day_sql = f"select day_r_day from day_money_other where day_r_year='2023' and day_r_month='09' group by day_r_day order by day_r_day asc"
                        self.curr.execute(day_sql)
                        day_res = self.curr.fetchall()

                        for day_val in day_res:
                             
                             search_sql = f"select * from day_money_other where day_r_year='2023' and day_r_month='09' and day_r_day='{day_val[0]}' and a_name='{name_val[0]}'"
                             self.curr.execute(search_sql)
                             search_res = self.curr.fetchone()

                             if search_res is None:
                                add_sql = f"insert into day_money_other(day_r_year , day_r_month , day_r_day , a_name , day_t_money) value('2023','09','{day_val[0]}','{name_val[0]}','0')"
                                self.curr.execute(add_sql)  
                    
                    #return day_res
                    self.conn.commit()
                    logging.info('< Msg > synchronization update day money tolls 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

        except Exception as e:
            logging.error("< Error > connect mysql fail (update_day_money_other) : " + str(e))

        finally:
            self.curr.close()
            self.conn.close()

    ##########################
    # bpm_day_money_traffic
    ##########################
    def bpm_day_money_other(self):
        
        try:    
                if sys.platform.startswith('win'):
                    conn_str = f"DRIVER={{SQL Server}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                
                conn_mssql = pyodbc.connect(conn_str)
                curr_mssql = conn_mssql.cursor()  
                #sql = f"select ITEM14 , ITEM72 , ITEM15 , ITEM12 from ART00721676130332682_INS where ITEM26='true' and ITEM44='true' order by ITEM12 desc"
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                #############################
                sql  = f"select ITEM14 , ITEM51 , ITEM15 , ITEM12 , ITEM58 , ITEM57 , ITEM107 from ART00851684549915660_INS where ITEM75='true' and ITEM18='true'" 
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                # table : ART00851684549915660ITEM53
                # ITEM1:日期
                # ITEM3:日當
                # ITEM4:交通費
                # ITEM5:超里程
                # ITEM6:停車費
                # ITEM7:過路費
                # ITEM8:車票
                # ITEM9: Taxi
                # ITEM10:住宿
                # ITEM11:其他
                # ITEM12:油單
                # ITEM14:註記原因
                # ITEM15:加減金額
                #
                #############################
                sql2  = f"select a.ITEM14 , a.ITEM51 , a.ITEM15 , a.ITEM12 , a.ITEM58 , a.ITEM57 , a.ITEM107 , b.ITEM1 , b.ITEM11 , b.ITEM14 , b.ITEM15 " 
                sql2 += f"from ART00851684549915660_INS a left join ART00851684549915660ITEM53 b on a.INSID=b.INSID " 
                sql2 += f"where a.ITEM75='true' and a.ITEM18='true' and b.ITEM11 != '0' "
                curr_mssql.execute(sql2)
                res  = curr_mssql.fetchall()

                try:
                    conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    curr = conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    for val in res:
                        
                        #logging.info(f"{val[0]} , {val[1]} , {val[2]} , {val[3]}")
                        
                        r_year      = val[3][0:4]
                        r_month     = val[3][5:7]
                        r_day       = val[3][8:10]
                        day_r_year  = val[7][0:4]
                        day_r_month = val[7][5:7]
                        day_r_day   = val[7][8:10]
                        
                        ###############################################
                        #
                        # Check if there are records in the database
                        #
                        ###############################################
                        #s_mysql_sql = f"select * from day_money where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_date='{val[7]}' and day_t_money='{val[8]}'"
                        #s_mysql_sql = f"select * from day_money_other where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"
                        s_mysql_sql = f"select * from day_money_other where f_name='{val[0]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"

                        curr.execute(s_mysql_sql)
                        mysql_res = curr.fetchone()

                        #logging.info(s_mysql_sql)
                        #exit()

                        day_money = val[8]

                        #####################################
                        #
                        # get english name by chinese name
                        #
                        #####################################
                        g_e_mysql_sql = f"select employee_eng_name from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_e_mysql_sql)
                        g_e_name = curr.fetchone()
                        
                        g_d_mysql_sql = f"select department_code from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_d_mysql_sql)
                        g_d_name = curr.fetchone()

                        if mysql_res is None:
                            
                            mysql_sql  = f"insert into day_money_other("
                            mysql_sql += f"r_date , r_year , r_month , r_day , " 
                            mysql_sql += f"f_name , a_name , e_name  , d_name , t_money , c_t_money , erp_num , " 
                            mysql_sql += f"form_num , day_r_year , day_r_month , day_t_money , day_money_mark , day_money_diff" 
                            mysql_sql += f") " 
                            mysql_sql += f"value(" 
                            mysql_sql += f"'{val[3]}' , '{r_year}'     , '{r_month}'     , '{r_day}'  , "
                            mysql_sql += f"'{val[0]}' , '{val[1]}'     , '{g_e_name[0]}' , '{g_d_name[0]}', '{val[2]}' , '{val[4]}' , '{val[5]}' ," 
                            mysql_sql += f"'{val[6]}' , '{day_r_year}' , '{day_r_month}' , '{0}' , '{val[9]}' , '{val[10]}'" 
                            mysql_sql += f")"
                            curr.execute(mysql_sql)
                            conn.commit()

                            #logging.info(f"{mysql_sql}") 
                            #logging.info(f"新日當資料 > 表單日期 : {val[3]} , 填表人 : {val[0]} , 申請人 : {val[1]} {g_e_name[0]} , 總金額 : {val[2]} , 日當日期 : {val[7]} , 日當金額 : {val[8]} , 註記原因 : {val[9]} , 加減金額 : {val[10]}")
                        
                        elif str(day_r_day) == '01':
                            mysql_sql  = f"update day_money_other set day_t_money1='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            #logging.info(f"{mysql_sql}") 
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '02':
                            mysql_sql  = f"update day_money_other set day_t_money2='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '03':
                            mysql_sql  = f"update day_money_other set day_t_money3='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '04':
                            mysql_sql  = f"update day_money_other set day_t_money4='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '05':
                            mysql_sql  = f"update day_money_other set day_t_money5='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '06':
                            mysql_sql  = f"update day_money_other set day_t_money6='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '07':
                            mysql_sql  = f"update day_money_other set day_t_money7='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '08':
                            mysql_sql  = f"update day_money_other set day_t_money8='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '09':
                            mysql_sql  = f"update day_money_other set day_t_money9='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '10':
                            mysql_sql  = f"update day_money_other set day_t_money10='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '11':
                            mysql_sql  = f"update day_money_other set day_t_money11='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '12':
                            mysql_sql  = f"update day_money_other set day_t_money12='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '13':
                            mysql_sql  = f"update day_money_other set day_t_money13='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '14':
                            mysql_sql  = f"update day_money_other set day_t_money14='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '15':
                            mysql_sql  = f"update day_money_other set day_t_money15='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '16':
                            mysql_sql  = f"update day_money_other set day_t_money16='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '17':
                            mysql_sql  = f"update day_money_other set day_t_money17='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '18':
                            mysql_sql  = f"update day_money_other set day_t_money18='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '19':
                            mysql_sql  = f"update day_money_other set day_t_money19='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '20':
                            mysql_sql  = f"update day_money_other set day_t_money20='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '21':
                            mysql_sql  = f"update day_money_other set day_t_money21='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '22':
                            mysql_sql  = f"update day_money_other set day_t_money22='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '23':
                            mysql_sql  = f"update day_money_other set day_t_money23='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '24':
                            mysql_sql  = f"update day_money_other set day_t_money24='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '25':
                            mysql_sql  = f"update day_money_other set day_t_money25='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '26':
                            mysql_sql  = f"update day_money_other set day_t_money26='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '27':
                            mysql_sql  = f"update day_money_other set day_t_money27='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '28':
                            mysql_sql  = f"update day_money_other set day_t_money28='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '29':
                            mysql_sql  = f"update day_money_other set day_t_money29='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '30':
                            mysql_sql  = f"update day_money_other set day_t_money30='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '31':
                            mysql_sql  = f"update day_money_other set day_t_money31='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        mysql_sql  = f"update day_money_other set day_t_total=("
                        mysql_sql += f"day_t_money1+day_t_money2+day_t_money3+day_t_money4+day_t_money5+day_t_money6+day_t_money7+day_t_money8+day_t_money9+day_t_money10+"
                        mysql_sql += f"day_t_money11+day_t_money12+day_t_money13+day_t_money14+day_t_money15+day_t_money16+day_t_money17+day_t_money18+day_t_money19+day_t_money20+"
                        mysql_sql += f"day_t_money21+day_t_money22+day_t_money23+day_t_money24+day_t_money25+day_t_money26+day_t_money27+day_t_money28+day_t_money29+day_t_money30+day_t_money31"
                        mysql_sql += f") "
                        mysql_sql += "where "
                        mysql_sql += f"r_date='{val[3]}'   and r_year='{r_year}'         and r_month='{r_month}'         and r_day='{r_day}'           and " 
                        mysql_sql += f"f_name='{val[0]}'   and a_name='{val[1]}'         and e_name='{g_e_name[0]}'      and t_money='{val[2]}'        and c_t_money='{val[4]}'      and erp_num='{val[5]}' and " 
                        mysql_sql += f"form_num='{val[6]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' and day_money_mark='{val[9]}' and day_money_diff='{val[10]}'" 
                        
                        curr.execute(mysql_sql)
                        conn.commit()
                    
                    logging.info('< Msg > update BPM day money 日當其他 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

                except Exception as e:
                    logging.error("< Error > bpm_day_money_other - connect mysql fail : " + str(e))

                finally:
                    curr.close()
                    conn.close()

        except Exception as e:
            logging.error("< Error > bpm_day_money_other - connect mssql fail : " + str(e))

        finally:
            curr_mssql.close()
            conn_mssql.close()

####################
#
# day money stay
#
####################
class day_money_stay:

    #########
    # init
    #########
    def __init__(self):
        try:
            self.bpm_day_money_stay()
            
        except Exception as e:
            logging.error('< Error > day money stay init : ' + str(e))
        finally:
            pass
   
    ###########################
    # update_day_money_stay
    ###########################
    def update_day_money_trick(self):
        try:
                    self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    self.curr = self.conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    #month = '0' + month if int(month) < 10 else month

                    # all day by month 
                    name_sql = f"select a_name from day_money_stay where day_r_year='2023' and day_r_month='09' group by a_name order by day_r_day asc"
                    self.curr.execute(name_sql)
                    name_res = self.curr.fetchall() 

                    for name_val in name_res:
                        
                        day_sql = f"select day_r_day from day_money_stay where day_r_year='2023' and day_r_month='09' group by day_r_day order by day_r_day asc"
                        self.curr.execute(day_sql)
                        day_res = self.curr.fetchall()

                        for day_val in day_res:
                             
                             search_sql = f"select * from day_money_stay where day_r_year='2023' and day_r_month='09' and day_r_day='{day_val[0]}' and a_name='{name_val[0]}'"
                             self.curr.execute(search_sql)
                             search_res = self.curr.fetchone()

                             if search_res is None:
                                add_sql = f"insert into day_money_stay(day_r_year , day_r_month , day_r_day , a_name , day_t_money) value('2023','09','{day_val[0]}','{name_val[0]}','0')"
                                self.curr.execute(add_sql)  
                    
                    #return day_res
                    self.conn.commit()
                    logging.info('< Msg > synchronization update day money tolls 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

        except Exception as e:
            logging.error("< Error > connect mysql fail (update_day_money_stay) : " + str(e))

        finally:
            self.curr.close()
            self.conn.close()

    ##########################
    # bpm_day_money_traffic
    ##########################
    def bpm_day_money_stay(self):
        
        try: 
                if sys.platform.startswith('win'):
                    conn_str = f"DRIVER={{SQL Server}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                
                conn_mssql = pyodbc.connect(conn_str)
                curr_mssql = conn_mssql.cursor()  
                #sql = f"select ITEM14 , ITEM72 , ITEM15 , ITEM12 from ART00721676130332682_INS where ITEM26='true' and ITEM44='true' order by ITEM12 desc"
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                #############################
                sql  = f"select ITEM14 , ITEM51 , ITEM15 , ITEM12 , ITEM58 , ITEM57 , ITEM107 from ART00851684549915660_INS where ITEM75='true' and ITEM18='true'" 
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                # table : ART00851684549915660ITEM53
                # ITEM1:日期
                # ITEM3:日當
                # ITEM4:交通費
                # ITEM5:超里程
                # ITEM6:停車費
                # ITEM7:過路費
                # ITEM8:車票
                # ITEM9: Taxi
                # ITEM10:住宿
                # ITEM11:其他
                # ITEM12:油單
                # ITEM14:註記原因
                # ITEM15:加減金額
                #
                #############################
                sql2  = f"select a.ITEM14 , a.ITEM51 , a.ITEM15 , a.ITEM12 , a.ITEM58 , a.ITEM57 , a.ITEM107 , b.ITEM1 , b.ITEM10 , b.ITEM14 , b.ITEM15 " 
                sql2 += f"from ART00851684549915660_INS a left join ART00851684549915660ITEM53 b on a.INSID=b.INSID " 
                sql2 += f"where a.ITEM75='true' and a.ITEM18='true' and b.ITEM10 != '0' "
                curr_mssql.execute(sql2)
                res  = curr_mssql.fetchall()

                try:
                    conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    curr = conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    for val in res:
                        
                        #logging.info(f"{val[0]} , {val[1]} , {val[2]} , {val[3]}")
                        
                        r_year      = val[3][0:4]
                        r_month     = val[3][5:7]
                        r_day       = val[3][8:10]
                        day_r_year  = val[7][0:4]
                        day_r_month = val[7][5:7]
                        day_r_day   = val[7][8:10]
                        
                        ###############################################
                        #
                        # Check if there are records in the database
                        #
                        ###############################################
                        #s_mysql_sql = f"select * from day_money where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_date='{val[7]}' and day_t_money='{val[8]}'"
                        #s_mysql_sql = f"select * from day_money_stay where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"
                        s_mysql_sql = f"select * from day_money_stay where f_name='{val[0]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"

                        curr.execute(s_mysql_sql)
                        mysql_res = curr.fetchone()

                        #logging.info(s_mysql_sql)
                        #exit()

                        day_money = val[8]

                        #####################################
                        #
                        # get english name by chinese name
                        #
                        #####################################
                        g_e_mysql_sql = f"select employee_eng_name from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_e_mysql_sql)
                        g_e_name = curr.fetchone()
                        
                        g_d_mysql_sql = f"select department_code from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_d_mysql_sql)
                        g_d_name = curr.fetchone()

                        if mysql_res is None:
                            
                            mysql_sql  = f"insert into day_money_stay("
                            mysql_sql += f"r_date , r_year , r_month , r_day , " 
                            mysql_sql += f"f_name , a_name , e_name  , d_name , t_money , c_t_money , erp_num , " 
                            mysql_sql += f"form_num , day_r_year , day_r_month , day_t_money , day_money_mark , day_money_diff" 
                            mysql_sql += f") " 
                            mysql_sql += f"value(" 
                            mysql_sql += f"'{val[3]}' , '{r_year}'     , '{r_month}'     , '{r_day}'  , "
                            mysql_sql += f"'{val[0]}' , '{val[1]}'     , '{g_e_name[0]}' , '{g_d_name[0]}' , '{val[2]}' , '{val[4]}' , '{val[5]}' ," 
                            mysql_sql += f"'{val[6]}' , '{day_r_year}' , '{day_r_month}' , '{0}' , '{val[9]}' , '{val[10]}'" 
                            mysql_sql += f")"
                            curr.execute(mysql_sql)
                            conn.commit()

                            #logging.info(f"{mysql_sql}") 
                            #logging.info(f"新日當資料 > 表單日期 : {val[3]} , 填表人 : {val[0]} , 申請人 : {val[1]} {g_e_name[0]} , 總金額 : {val[2]} , 日當日期 : {val[7]} , 日當金額 : {val[8]} , 註記原因 : {val[9]} , 加減金額 : {val[10]}")
                        
                        elif str(day_r_day) == '01':
                            mysql_sql  = f"update day_money_stay set day_t_money1='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            #logging.info(f"{mysql_sql}") 
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '02':
                            mysql_sql  = f"update day_money_stay set day_t_money2='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '03':
                            mysql_sql  = f"update day_money_stay set day_t_money3='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '04':
                            mysql_sql  = f"update day_money_stay set day_t_money4='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '05':
                            mysql_sql  = f"update day_money_stay set day_t_money5='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '06':
                            mysql_sql  = f"update day_money_stay set day_t_money6='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '07':
                            mysql_sql  = f"update day_money_stay set day_t_money7='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '08':
                            mysql_sql  = f"update day_money_stay set day_t_money8='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '09':
                            mysql_sql  = f"update day_money_stay set day_t_money9='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '10':
                            mysql_sql  = f"update day_money_stay set day_t_money10='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '11':
                            mysql_sql  = f"update day_money_stay set day_t_money11='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '12':
                            mysql_sql  = f"update day_money_stay set day_t_money12='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '13':
                            mysql_sql  = f"update day_money_stay set day_t_money13='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '14':
                            mysql_sql  = f"update day_money_stay set day_t_money14='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '15':
                            mysql_sql  = f"update day_money_stay set day_t_money15='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '16':
                            mysql_sql  = f"update day_money_stay set day_t_money16='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '17':
                            mysql_sql  = f"update day_money_stay set day_t_money17='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '18':
                            mysql_sql  = f"update day_money_stay set day_t_money18='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '19':
                            mysql_sql  = f"update day_money_stay set day_t_money19='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '20':
                            mysql_sql  = f"update day_money_stay set day_t_money20='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '21':
                            mysql_sql  = f"update day_money_stay set day_t_money21='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '22':
                            mysql_sql  = f"update day_money_stay set day_t_money22='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '23':
                            mysql_sql  = f"update day_money_stay set day_t_money23='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '24':
                            mysql_sql  = f"update day_money_stay set day_t_money24='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '25':
                            mysql_sql  = f"update day_money_stay set day_t_money25='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '26':
                            mysql_sql  = f"update day_money_stay set day_t_money26='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '27':
                            mysql_sql  = f"update day_money_stay set day_t_money27='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '28':
                            mysql_sql  = f"update day_money_stay set day_t_money28='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '29':
                            mysql_sql  = f"update day_money_stay set day_t_money29='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '30':
                            mysql_sql  = f"update day_money_stay set day_t_money30='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '31':
                            mysql_sql  = f"update day_money_stay set day_t_money31='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        mysql_sql  = f"update day_money_stay set day_t_total=("
                        mysql_sql += f"day_t_money1+day_t_money2+day_t_money3+day_t_money4+day_t_money5+day_t_money6+day_t_money7+day_t_money8+day_t_money9+day_t_money10+"
                        mysql_sql += f"day_t_money11+day_t_money12+day_t_money13+day_t_money14+day_t_money15+day_t_money16+day_t_money17+day_t_money18+day_t_money19+day_t_money20+"
                        mysql_sql += f"day_t_money21+day_t_money22+day_t_money23+day_t_money24+day_t_money25+day_t_money26+day_t_money27+day_t_money28+day_t_money29+day_t_money30+day_t_money31"
                        mysql_sql += f") "
                        mysql_sql += "where "
                        mysql_sql += f"r_date='{val[3]}'   and r_year='{r_year}'         and r_month='{r_month}'         and r_day='{r_day}'           and " 
                        mysql_sql += f"f_name='{val[0]}'   and a_name='{val[1]}'         and e_name='{g_e_name[0]}'      and t_money='{val[2]}'        and c_t_money='{val[4]}'      and erp_num='{val[5]}' and " 
                        mysql_sql += f"form_num='{val[6]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' and day_money_mark='{val[9]}' and day_money_diff='{val[10]}'" 
                        
                        curr.execute(mysql_sql)
                        conn.commit()
                    
                    logging.info('< Msg > update BPM day money 日當住宿 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

                except Exception as e:
                    logging.error("< Error > bpm_day_money_stay - connect mysql fail : " + str(e))

                finally:
                    curr.close()
                    conn.close()

        except Exception as e:
            logging.error("< Error > bpm_day_money_stay - connect mssql fail : " + str(e))

        finally:
            curr_mssql.close()
            conn_mssql.close()

####################
#
# day money taxi
#
####################
class day_money_taxi:

    #########
    # init
    #########
    def __init__(self):
        try:
            self.bpm_day_money_taxi()
            
        except Exception as e:
            logging.error('< Error > day money taxi init : ' + str(e))
        finally:
            pass
   
    ###########################
    # update_day_money_tolls
    ###########################
    def update_day_money_trick(self):
        try:
                    self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    self.curr = self.conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    #month = '0' + month if int(month) < 10 else month

                    # all day by month 
                    name_sql = f"select a_name from day_money_taxi where day_r_year='2023' and day_r_month='09' group by a_name order by day_r_day asc"
                    self.curr.execute(name_sql)
                    name_res = self.curr.fetchall() 

                    for name_val in name_res:
                        
                        day_sql = f"select day_r_day from day_money_taxi where day_r_year='2023' and day_r_month='09' group by day_r_day order by day_r_day asc"
                        self.curr.execute(day_sql)
                        day_res = self.curr.fetchall()

                        for day_val in day_res:
                             
                             search_sql = f"select * from day_money_taxi where day_r_year='2023' and day_r_month='09' and day_r_day='{day_val[0]}' and a_name='{name_val[0]}'"
                             self.curr.execute(search_sql)
                             search_res = self.curr.fetchone()

                             if search_res is None:
                                add_sql = f"insert into day_money_taxi(day_r_year , day_r_month , day_r_day , a_name , day_t_money) value('2023','09','{day_val[0]}','{name_val[0]}','0')"
                                self.curr.execute(add_sql)  
                    
                    #return day_res
                    self.conn.commit()
                    logging.info('< Msg > synchronization update day money tolls 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

        except Exception as e:
            logging.error("< Error > connect mysql fail (update_day_money_taxi) : " + str(e))

        finally:
            self.curr.close()
            self.conn.close()

    ##########################
    # bpm_day_money_traffic
    ##########################
    def bpm_day_money_taxi(self):
        
        try: 
                if sys.platform.startswith('win'):
                    conn_str = f"DRIVER={{SQL Server}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                
                conn_mssql = pyodbc.connect(conn_str)
                curr_mssql = conn_mssql.cursor()  
                #sql = f"select ITEM14 , ITEM72 , ITEM15 , ITEM12 from ART00721676130332682_INS where ITEM26='true' and ITEM44='true' order by ITEM12 desc"
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                #############################
                sql  = f"select ITEM14 , ITEM51 , ITEM15 , ITEM12 , ITEM58 , ITEM57 , ITEM107 from ART00851684549915660_INS where ITEM75='true' and ITEM18='true'" 
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                # table : ART00851684549915660ITEM53
                # ITEM1:日期
                # ITEM3:日當
                # ITEM4:交通費
                # ITEM5:超里程
                # ITEM6:停車費
                # ITEM7:過路費
                # ITEM8:車票
                # ITEM9: Taxi
                # ITEM10:住宿
                # ITEM11:其他
                # ITEM12:油單
                # ITEM14:註記原因
                # ITEM15:加減金額
                #
                #############################
                sql2  = f"select a.ITEM14 , a.ITEM51 , a.ITEM15 , a.ITEM12 , a.ITEM58 , a.ITEM57 , a.ITEM107 , b.ITEM1 , b.ITEM9 , b.ITEM14 , b.ITEM15 " 
                sql2 += f"from ART00851684549915660_INS a left join ART00851684549915660ITEM53 b on a.INSID=b.INSID " 
                sql2 += f"where a.ITEM75='true' and a.ITEM18='true' and b.ITEM9 != '0' "
                curr_mssql.execute(sql2)
                res  = curr_mssql.fetchall()

                try:
                    conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    curr = conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    for val in res:
                        
                        #logging.info(f"{val[0]} , {val[1]} , {val[2]} , {val[3]}")
                        
                        r_year      = val[3][0:4]
                        r_month     = val[3][5:7]
                        r_day       = val[3][8:10]
                        day_r_year  = val[7][0:4]
                        day_r_month = val[7][5:7]
                        day_r_day   = val[7][8:10]
                        
                        ###############################################
                        #
                        # Check if there are records in the database
                        #
                        ###############################################
                        #s_mysql_sql = f"select * from day_money where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_date='{val[7]}' and day_t_money='{val[8]}'"
                        #s_mysql_sql = f"select * from day_money_taxi where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"
                        s_mysql_sql = f"select * from day_money_taxi where f_name='{val[0]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"

                        curr.execute(s_mysql_sql)
                        mysql_res = curr.fetchone()

                        #logging.info(s_mysql_sql)
                        #exit()

                        day_money = val[8]

                        #####################################
                        #
                        # get english name by chinese name
                        #
                        #####################################
                        g_e_mysql_sql = f"select employee_eng_name from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_e_mysql_sql)
                        g_e_name = curr.fetchone()

                        g_d_mysql_sql = f"select department_code from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_d_mysql_sql)
                        g_d_name = curr.fetchone()

                        if mysql_res is None:
                            
                            mysql_sql  = f"insert into day_money_taxi("
                            mysql_sql += f"r_date , r_year , r_month , r_day , " 
                            mysql_sql += f"f_name , a_name , e_name , d_name , t_money , c_t_money , erp_num , " 
                            mysql_sql += f"form_num , day_r_year , day_r_month , day_t_money , day_money_mark , day_money_diff" 
                            mysql_sql += f") " 
                            mysql_sql += f"value(" 
                            mysql_sql += f"'{val[3]}' , '{r_year}'     , '{r_month}'     , '{r_day}'  , "
                            mysql_sql += f"'{val[0]}' , '{val[1]}'     , '{g_e_name[0]}' , '{g_d_name[0]}', '{val[2]}' , '{val[4]}' , '{val[5]}' ," 
                            mysql_sql += f"'{val[6]}' , '{day_r_year}' , '{day_r_month}' , '{0}' , '{val[9]}' , '{val[10]}'" 
                            mysql_sql += f")"
                            curr.execute(mysql_sql)
                            conn.commit()

                            #logging.info(f"{mysql_sql}") 
                            #logging.info(f"新日當資料 > 表單日期 : {val[3]} , 填表人 : {val[0]} , 申請人 : {val[1]} {g_e_name[0]} , 總金額 : {val[2]} , 日當日期 : {val[7]} , 日當金額 : {val[8]} , 註記原因 : {val[9]} , 加減金額 : {val[10]}")
                        
                        elif str(day_r_day) == '01':
                            mysql_sql  = f"update day_money_taxi set day_t_money1='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            #logging.info(f"{mysql_sql}") 
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '02':
                            mysql_sql  = f"update day_money_taxi set day_t_money2='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '03':
                            mysql_sql  = f"update day_money_taxi set day_t_money3='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '04':
                            mysql_sql  = f"update day_money_taxi set day_t_money4='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '05':
                            mysql_sql  = f"update day_money_taxi set day_t_money5='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '06':
                            mysql_sql  = f"update day_money_taxi set day_t_money6='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '07':
                            mysql_sql  = f"update day_money_taxi set day_t_money7='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '08':
                            mysql_sql  = f"update day_money_taxi set day_t_money8='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '09':
                            mysql_sql  = f"update day_money_taxi set day_t_money9='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '10':
                            mysql_sql  = f"update day_money_taxi set day_t_money10='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '11':
                            mysql_sql  = f"update day_money_taxi set day_t_money11='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '12':
                            mysql_sql  = f"update day_money_taxi set day_t_money12='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '13':
                            mysql_sql  = f"update day_money_taxi set day_t_money13='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '14':
                            mysql_sql  = f"update day_money_taxi set day_t_money14='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '15':
                            mysql_sql  = f"update day_money_taxi set day_t_money15='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '16':
                            mysql_sql  = f"update day_money_taxi set day_t_money16='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '17':
                            mysql_sql  = f"update day_money_taxi set day_t_money17='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '18':
                            mysql_sql  = f"update day_money_taxi set day_t_money18='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '19':
                            mysql_sql  = f"update day_money_taxi set day_t_money19='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '20':
                            mysql_sql  = f"update day_money_taxi set day_t_money20='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '21':
                            mysql_sql  = f"update day_money_taxi set day_t_money21='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '22':
                            mysql_sql  = f"update day_money_taxi set day_t_money22='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '23':
                            mysql_sql  = f"update day_money_taxi set day_t_money23='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '24':
                            mysql_sql  = f"update day_money_taxi set day_t_money24='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '25':
                            mysql_sql  = f"update day_money_taxi set day_t_money25='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '26':
                            mysql_sql  = f"update day_money_taxi set day_t_money26='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '27':
                            mysql_sql  = f"update day_money_taxi set day_t_money27='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '28':
                            mysql_sql  = f"update day_money_taxi set day_t_money28='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '29':
                            mysql_sql  = f"update day_money_taxi set day_t_money29='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '30':
                            mysql_sql  = f"update day_money_taxi set day_t_money30='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '31':
                            mysql_sql  = f"update day_money_taxi set day_t_money31='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        mysql_sql  = f"update day_money_taxi set day_t_total=("
                        mysql_sql += f"day_t_money1+day_t_money2+day_t_money3+day_t_money4+day_t_money5+day_t_money6+day_t_money7+day_t_money8+day_t_money9+day_t_money10+"
                        mysql_sql += f"day_t_money11+day_t_money12+day_t_money13+day_t_money14+day_t_money15+day_t_money16+day_t_money17+day_t_money18+day_t_money19+day_t_money20+"
                        mysql_sql += f"day_t_money21+day_t_money22+day_t_money23+day_t_money24+day_t_money25+day_t_money26+day_t_money27+day_t_money28+day_t_money29+day_t_money30+day_t_money31"
                        mysql_sql += f") "
                        mysql_sql += "where "
                        mysql_sql += f"r_date='{val[3]}'   and r_year='{r_year}'         and r_month='{r_month}'         and r_day='{r_day}'           and " 
                        mysql_sql += f"f_name='{val[0]}'   and a_name='{val[1]}'         and e_name='{g_e_name[0]}'      and t_money='{val[2]}'        and c_t_money='{val[4]}'      and erp_num='{val[5]}' and " 
                        mysql_sql += f"form_num='{val[6]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' and day_money_mark='{val[9]}' and day_money_diff='{val[10]}'" 
                        
                        curr.execute(mysql_sql)
                        conn.commit()
                    
                    logging.info('< Msg > update BPM day money 日當計程車 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

                except Exception as e:
                    logging.error("< Error > bpm_day_money_taxi - connect mysql fail : " + str(e))

                finally:
                    curr.close()
                    conn.close()

        except Exception as e:
            logging.error("< Error > bpm_day_money_taxi - connect mssql fail : " + str(e))

        finally:
            curr_mssql.close()
            conn_mssql.close()

####################
#
# day money trick
#
####################
class day_money_trick:

    #########
    # init
    #########
    def __init__(self):
        try:
            self.bpm_day_money_trick()
            
        except Exception as e:
            logging.error('< Error > day money trick init : ' + str(e))
        finally:
            pass
   
    ###########################
    # update_day_money_tolls
    ###########################
    def update_day_money_trick(self):
        try:
                    self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    self.curr = self.conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    #month = '0' + month if int(month) < 10 else month

                    # all day by month 
                    name_sql = f"select a_name from day_money_trick where day_r_year='2023' and day_r_month='09' group by a_name order by day_r_day asc"
                    self.curr.execute(name_sql)
                    name_res = self.curr.fetchall() 

                    for name_val in name_res:
                        
                        day_sql = f"select day_r_day from day_money_trick where day_r_year='2023' and day_r_month='09' group by day_r_day order by day_r_day asc"
                        self.curr.execute(day_sql)
                        day_res = self.curr.fetchall()

                        for day_val in day_res:
                             
                             search_sql = f"select * from day_money_trick where day_r_year='2023' and day_r_month='09' and day_r_day='{day_val[0]}' and a_name='{name_val[0]}'"
                             self.curr.execute(search_sql)
                             search_res = self.curr.fetchone()

                             if search_res is None:
                                add_sql = f"insert into day_money_trick(day_r_year , day_r_month , day_r_day , a_name , day_t_money) value('2023','09','{day_val[0]}','{name_val[0]}','0')"
                                self.curr.execute(add_sql)  
                    
                    #return day_res
                    self.conn.commit()
                    logging.info('< Msg > synchronization update day money tolls 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

        except Exception as e:
            logging.error("< Error > connect mysql fail (update_day_money_trick) : " + str(e))

        finally:
            self.curr.close()
            self.conn.close()

    ##########################
    # bpm_day_money_traffic
    ##########################
    def bpm_day_money_trick(self):
        
        try: 
                if sys.platform.startswith('win'):
                    conn_str = f"DRIVER={{SQL Server}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  

                conn_mssql = pyodbc.connect(conn_str)
                curr_mssql = conn_mssql.cursor()  
                #sql = f"select ITEM14 , ITEM72 , ITEM15 , ITEM12 from ART00721676130332682_INS where ITEM26='true' and ITEM44='true' order by ITEM12 desc"
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                #############################
                sql  = f"select ITEM14 , ITEM51 , ITEM15 , ITEM12 , ITEM58 , ITEM57 , ITEM107 from ART00851684549915660_INS where ITEM75='true' and ITEM18='true'" 
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                # table : ART00851684549915660ITEM53
                # ITEM1:日期
                # ITEM3:日當
                # ITEM4:交通費
                # ITEM5:超里程
                # ITEM6:停車費
                # ITEM7:過路費
                # ITEM8:車票
                # ITEM9: Taxi
                # ITEM10:住宿
                # ITEM11:其他
                # ITEM12:油單
                # ITEM14:註記原因
                # ITEM15:加減金額
                #
                #############################
                sql2  = f"select a.ITEM14 , a.ITEM51 , a.ITEM15 , a.ITEM12 , a.ITEM58 , a.ITEM57 , a.ITEM107 , b.ITEM1 , b.ITEM8 , b.ITEM14 , b.ITEM15 " 
                sql2 += f"from ART00851684549915660_INS a left join ART00851684549915660ITEM53 b on a.INSID=b.INSID " 
                sql2 += f"where a.ITEM75='true' and a.ITEM18='true' and b.ITEM8 != '0' "
                curr_mssql.execute(sql2)
                res  = curr_mssql.fetchall()

                try:
                    conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    curr = conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    for val in res:
                        
                        #logging.info(f"{val[0]} , {val[1]} , {val[2]} , {val[3]}")
                        
                        r_year      = val[3][0:4]
                        r_month     = val[3][5:7]
                        r_day       = val[3][8:10]
                        day_r_year  = val[7][0:4]
                        day_r_month = val[7][5:7]
                        day_r_day   = val[7][8:10]
                        
                        ###############################################
                        #
                        # Check if there are records in the database
                        #
                        ###############################################
                        #s_mysql_sql = f"select * from day_money where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_date='{val[7]}' and day_t_money='{val[8]}'"
                        #s_mysql_sql = f"select * from day_money_trick where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"
                        s_mysql_sql  = f"select * from day_money_trick where f_name='{val[0]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"

                        curr.execute(s_mysql_sql)
                        mysql_res = curr.fetchone()

                        #logging.info(s_mysql_sql)
                        #exit()

                        day_money = val[8]

                        #####################################
                        #
                        # get english name by chinese name
                        #
                        #####################################
                        g_e_mysql_sql = f"select employee_eng_name from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_e_mysql_sql)
                        g_e_name = curr.fetchone()
                        
                        g_d_mysql_sql = f"select department_code from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_d_mysql_sql)
                        g_d_name = curr.fetchone()

                        if mysql_res is None:
                            
                            mysql_sql  = f"insert into day_money_trick("
                            mysql_sql += f"r_date , r_year , r_month , r_day , " 
                            mysql_sql += f"f_name , a_name , e_name , d_name , t_money , c_t_money , erp_num , " 
                            mysql_sql += f"form_num , day_r_year , day_r_month , day_t_money , day_money_mark , day_money_diff" 
                            mysql_sql += f") " 
                            mysql_sql += f"value(" 
                            mysql_sql += f"'{val[3]}' , '{r_year}'     , '{r_month}'     , '{r_day}'  , "
                            mysql_sql += f"'{val[0]}' , '{val[1]}'     , '{g_e_name[0]}' , '{g_d_name[0]}', '{val[2]}' , '{val[4]}' , '{val[5]}' ," 
                            mysql_sql += f"'{val[6]}' , '{day_r_year}' , '{day_r_month}' , '{0}' , '{val[9]}' , '{val[10]}'" 
                            mysql_sql += f")"
                            curr.execute(mysql_sql)
                            conn.commit()

                            #logging.info(f"{mysql_sql}") 
                            #logging.info(f"新日當資料 > 表單日期 : {val[3]} , 填表人 : {val[0]} , 申請人 : {val[1]} {g_e_name[0]} , 總金額 : {val[2]} , 日當日期 : {val[7]} , 日當金額 : {val[8]} , 註記原因 : {val[9]} , 加減金額 : {val[10]}")
                        
                        elif str(day_r_day) == '01':
                            mysql_sql  = f"update day_money_trick set day_t_money1='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            #logging.info(f"{mysql_sql}") 
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '02':
                            mysql_sql  = f"update day_money_trick set day_t_money2='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '03':
                            mysql_sql  = f"update day_money_trick set day_t_money3='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '04':
                            mysql_sql  = f"update day_money_trick set day_t_money4='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '05':
                            mysql_sql  = f"update day_money_trick set day_t_money5='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '06':
                            mysql_sql  = f"update day_money_trick set day_t_money6='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '07':
                            mysql_sql  = f"update day_money_trick set day_t_money7='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '08':
                            mysql_sql  = f"update day_money_trick set day_t_money8='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '09':
                            mysql_sql  = f"update day_money_trick set day_t_money9='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '10':
                            mysql_sql  = f"update day_money_trick set day_t_money10='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '11':
                            mysql_sql  = f"update day_money_trick set day_t_money11='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '12':
                            mysql_sql  = f"update day_money_trick set day_t_money12='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '13':
                            mysql_sql  = f"update day_money_trick set day_t_money13='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '14':
                            mysql_sql  = f"update day_money_trick set day_t_money14='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '15':
                            mysql_sql  = f"update day_money_trick set day_t_money15='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '16':
                            mysql_sql  = f"update day_money_trick set day_t_money16='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '17':
                            mysql_sql  = f"update day_money_trick set day_t_money17='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '18':
                            mysql_sql  = f"update day_money_trick set day_t_money18='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '19':
                            mysql_sql  = f"update day_money_trick set day_t_money19='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '20':
                            mysql_sql  = f"update day_money_trick set day_t_money20='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '21':
                            mysql_sql  = f"update day_money_trick set day_t_money21='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '22':
                            mysql_sql  = f"update day_money_trick set day_t_money22='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '23':
                            mysql_sql  = f"update day_money_trick set day_t_money23='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '24':
                            mysql_sql  = f"update day_money_trick set day_t_money24='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '25':
                            mysql_sql  = f"update day_money_trick set day_t_money25='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '26':
                            mysql_sql  = f"update day_money_trick set day_t_money26='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '27':
                            mysql_sql  = f"update day_money_trick set day_t_money27='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '28':
                            mysql_sql  = f"update day_money_trick set day_t_money28='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '29':
                            mysql_sql  = f"update day_money_trick set day_t_money29='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '30':
                            mysql_sql  = f"update day_money_trick set day_t_money30='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '31':
                            mysql_sql  = f"update day_money_trick set day_t_money31='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        mysql_sql  = f"update day_money_trick set day_t_total=("
                        mysql_sql += f"day_t_money1+day_t_money2+day_t_money3+day_t_money4+day_t_money5+day_t_money6+day_t_money7+day_t_money8+day_t_money9+day_t_money10+"
                        mysql_sql += f"day_t_money11+day_t_money12+day_t_money13+day_t_money14+day_t_money15+day_t_money16+day_t_money17+day_t_money18+day_t_money19+day_t_money20+"
                        mysql_sql += f"day_t_money21+day_t_money22+day_t_money23+day_t_money24+day_t_money25+day_t_money26+day_t_money27+day_t_money28+day_t_money29+day_t_money30+day_t_money31"
                        mysql_sql += f") "
                        mysql_sql += "where "
                        mysql_sql += f"r_date='{val[3]}'   and r_year='{r_year}'         and r_month='{r_month}'         and r_day='{r_day}'           and " 
                        mysql_sql += f"f_name='{val[0]}'   and a_name='{val[1]}'         and e_name='{g_e_name[0]}'      and t_money='{val[2]}'        and c_t_money='{val[4]}'      and erp_num='{val[5]}' and " 
                        mysql_sql += f"form_num='{val[6]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' and day_money_mark='{val[9]}' and day_money_diff='{val[10]}'" 
                        
                        curr.execute(mysql_sql)
                        conn.commit()
                    
                    logging.info('< Msg > update BPM day money 日當車票 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

                except Exception as e:
                    logging.error("< Error > bpm_day_money_trick - connect mysql fail : " + str(e))

                finally:
                    curr.close()
                    conn.close()

        except Exception as e:
            logging.error("< Error > bpm_day_money_trick - connect mssql fail : " + str(e))

        finally:
            curr_mssql.close()
            conn_mssql.close()

####################
#
# day money tolls
#
####################
class day_money_tolls:

    #########
    # init
    #########
    def __init__(self):
        try:
            self.bpm_day_money_tolls()
            
        except Exception as e:
            logging.error('< Error > day money tolls init : ' + str(e))
        finally:
            pass
   
    ###########################
    # update_day_money_tolls
    ###########################
    def update_day_money_tolls(self):
        try:
                    self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    self.curr = self.conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    #month = '0' + month if int(month) < 10 else month

                    # all day by month 
                    name_sql = f"select a_name from day_money_tolls where day_r_year='2023' and day_r_month='09' group by a_name order by day_r_day asc"
                    self.curr.execute(name_sql)
                    name_res = self.curr.fetchall() 

                    for name_val in name_res:
                        
                        day_sql = f"select day_r_day from day_money_tolls where day_r_year='2023' and day_r_month='09' group by day_r_day order by day_r_day asc"
                        self.curr.execute(day_sql)
                        day_res = self.curr.fetchall()

                        for day_val in day_res:
                             
                             search_sql = f"select * from day_money_tolls where day_r_year='2023' and day_r_month='09' and day_r_day='{day_val[0]}' and a_name='{name_val[0]}'"
                             self.curr.execute(search_sql)
                             search_res = self.curr.fetchone()

                             if search_res is None:
                                add_sql = f"insert into day_money_tolls(day_r_year , day_r_month , day_r_day , a_name , day_t_money) value('2023','09','{day_val[0]}','{name_val[0]}','0')"
                                self.curr.execute(add_sql)  
                    
                    #return day_res
                    self.conn.commit()
                    logging.info('< Msg > synchronization update day money tolls 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

        except Exception as e:
            logging.error("< Error > connect mysql fail (update_day_money_tolls) : " + str(e))

        finally:
            self.curr.close()
            self.conn.close()

    ##########################
    # bpm_day_money_traffic
    ##########################
    def bpm_day_money_tolls(self):
        
        try: 
                if sys.platform.startswith('win'):
                    conn_str = f"DRIVER={{SQL Server}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                
                conn_mssql = pyodbc.connect(conn_str)
                curr_mssql = conn_mssql.cursor()  
                #sql = f"select ITEM14 , ITEM72 , ITEM15 , ITEM12 from ART00721676130332682_INS where ITEM26='true' and ITEM44='true' order by ITEM12 desc"
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                #############################
                sql  = f"select ITEM14 , ITEM51 , ITEM15 , ITEM12 , ITEM58 , ITEM57 , ITEM107 from ART00851684549915660_INS where ITEM75='true' and ITEM18='true'" 
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                # table : ART00851684549915660ITEM53
                # ITEM1:日期
                # ITEM3:日當
                # ITEM4:交通費
                # ITEM5:超里程
                # ITEM6:停車費
                # ITEM7:過路費
                # ITEM8:車票
                # ITEM9: Taxi
                # ITEM10:住宿
                # ITEM11:其他
                # ITEM12:油單
                # ITEM14:註記原因
                # ITEM15:加減金額
                #
                #############################
                sql2  = f"select a.ITEM14 , a.ITEM51 , a.ITEM15 , a.ITEM12 , a.ITEM58 , a.ITEM57 , a.ITEM107 , b.ITEM1 , b.ITEM7 , b.ITEM14 , b.ITEM15 " 
                sql2 += f"from ART00851684549915660_INS a left join ART00851684549915660ITEM53 b on a.INSID=b.INSID " 
                sql2 += f"where a.ITEM75='true' and a.ITEM18='true' and b.ITEM7 != '0' "
                curr_mssql.execute(sql2)
                res  = curr_mssql.fetchall()

                try:
                    conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    curr = conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    for val in res:
                        
                        #logging.info(f"{val[0]} , {val[1]} , {val[2]} , {val[3]}")
                        
                        r_year      = val[3][0:4]
                        r_month     = val[3][5:7]
                        r_day       = val[3][8:10]
                        day_r_year  = val[7][0:4]
                        day_r_month = val[7][5:7]
                        day_r_day   = val[7][8:10]
                        
                        ###############################################
                        #
                        # Check if there are records in the database
                        #
                        ###############################################
                        #s_mysql_sql = f"select * from day_money where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_date='{val[7]}' and day_t_money='{val[8]}'"
                        #s_mysql_sql = f"select * from day_money_tolls where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"
                        s_mysql_sql = f"select * from day_money_tolls where f_name='{val[0]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"

                        curr.execute(s_mysql_sql)
                        mysql_res = curr.fetchone()

                        #logging.info(s_mysql_sql)
                        #exit()

                        day_money = val[8]

                        #####################################
                        #
                        # get english name by chinese name
                        #
                        #####################################
                        g_e_mysql_sql = f"select employee_eng_name from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_e_mysql_sql)
                        g_e_name = curr.fetchone()

                        g_d_mysql_sql = f"select department_code from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_d_mysql_sql)
                        g_d_name = curr.fetchone()

                        if mysql_res is None:
                            
                            mysql_sql  = f"insert into day_money_tolls("
                            mysql_sql += f"r_date , r_year , r_month , r_day , " 
                            mysql_sql += f"f_name , a_name , e_name , d_name , t_money , c_t_money , erp_num , " 
                            mysql_sql += f"form_num , day_r_year , day_r_month , day_t_money , day_money_mark , day_money_diff" 
                            mysql_sql += f") " 
                            mysql_sql += f"value(" 
                            mysql_sql += f"'{val[3]}' , '{r_year}'     , '{r_month}'     , '{r_day}'  , "
                            mysql_sql += f"'{val[0]}' , '{val[1]}'     , '{g_e_name[0]}' , '{g_d_name[0]}' , '{val[2]}' , '{val[4]}' , '{val[5]}' ," 
                            mysql_sql += f"'{val[6]}' , '{day_r_year}' , '{day_r_month}' , '{0}' , '{val[9]}' , '{val[10]}'" 
                            mysql_sql += f")"
                            curr.execute(mysql_sql)
                            conn.commit()

                            #logging.info(f"{mysql_sql}") 
                            #logging.info(f"新日當資料 > 表單日期 : {val[3]} , 填表人 : {val[0]} , 申請人 : {val[1]} {g_e_name[0]} , 總金額 : {val[2]} , 日當日期 : {val[7]} , 日當金額 : {val[8]} , 註記原因 : {val[9]} , 加減金額 : {val[10]}")
                        
                        elif str(day_r_day) == '01':
                            mysql_sql  = f"update day_money_tolls set day_t_money1='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            #logging.info(f"{mysql_sql}") 
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '02':
                            mysql_sql  = f"update day_money_tolls set day_t_money2='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '03':
                            mysql_sql  = f"update day_money_tolls set day_t_money3='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '04':
                            mysql_sql  = f"update day_money_tolls set day_t_money4='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '05':
                            mysql_sql  = f"update day_money_tolls set day_t_money5='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '06':
                            mysql_sql  = f"update day_money_tolls set day_t_money6='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '07':
                            mysql_sql  = f"update day_money_tolls set day_t_money7='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '08':
                            mysql_sql  = f"update day_money_tolls set day_t_money8='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '09':
                            mysql_sql  = f"update day_money_tolls set day_t_money9='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '10':
                            mysql_sql  = f"update day_money_tolls set day_t_money10='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '11':
                            mysql_sql  = f"update day_money_tolls set day_t_money11='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '12':
                            mysql_sql  = f"update day_money_tolls set day_t_money12='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '13':
                            mysql_sql  = f"update day_money_tolls set day_t_money13='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '14':
                            mysql_sql  = f"update day_money_tolls set day_t_money14='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '15':
                            mysql_sql  = f"update day_money_tolls set day_t_money15='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '16':
                            mysql_sql  = f"update day_money_tolls set day_t_money16='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '17':
                            mysql_sql  = f"update day_money_tolls set day_t_money17='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '18':
                            mysql_sql  = f"update day_money_tolls set day_t_money18='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '19':
                            mysql_sql  = f"update day_money_tolls set day_t_money19='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '20':
                            mysql_sql  = f"update day_money_tolls set day_t_money20='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '21':
                            mysql_sql  = f"update day_money_tolls set day_t_money21='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '22':
                            mysql_sql  = f"update day_money_tolls set day_t_money22='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '23':
                            mysql_sql  = f"update day_money_tolls set day_t_money23='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '24':
                            mysql_sql  = f"update day_money_tolls set day_t_money24='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '25':
                            mysql_sql  = f"update day_money_tolls set day_t_money25='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '26':
                            mysql_sql  = f"update day_money_tolls set day_t_money26='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '27':
                            mysql_sql  = f"update day_money_tolls set day_t_money27='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '28':
                            mysql_sql  = f"update day_money_tolls set day_t_money28='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '29':
                            mysql_sql  = f"update day_money_tolls set day_t_money29='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '30':
                            mysql_sql  = f"update day_money_tolls set day_t_money30='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '31':
                            mysql_sql  = f"update day_money_tolls set day_t_money31='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 

                            
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        mysql_sql  = f"update day_money_tolls set day_t_total=("
                        mysql_sql += f"day_t_money1+day_t_money2+day_t_money3+day_t_money4+day_t_money5+day_t_money6+day_t_money7+day_t_money8+day_t_money9+day_t_money10+"
                        mysql_sql += f"day_t_money11+day_t_money12+day_t_money13+day_t_money14+day_t_money15+day_t_money16+day_t_money17+day_t_money18+day_t_money19+day_t_money20+"
                        mysql_sql += f"day_t_money21+day_t_money22+day_t_money23+day_t_money24+day_t_money25+day_t_money26+day_t_money27+day_t_money28+day_t_money29+day_t_money30+day_t_money31"
                        mysql_sql += f") "
                        mysql_sql += "where "
                        mysql_sql += f"r_date='{val[3]}'   and r_year='{r_year}'         and r_month='{r_month}'         and r_day='{r_day}'           and " 
                        mysql_sql += f"f_name='{val[0]}'   and a_name='{val[1]}'         and e_name='{g_e_name[0]}'      and t_money='{val[2]}'        and c_t_money='{val[4]}'      and erp_num='{val[5]}' and " 
                        mysql_sql += f"form_num='{val[6]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' and day_money_mark='{val[9]}' and day_money_diff='{val[10]}'" 
                        
                        curr.execute(mysql_sql)
                        conn.commit()
                    
                    logging.info('< Msg > update BPM day money 日當過路費 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

                except Exception as e:
                    logging.error("< Error > bpm_day_money_tolls - connect mysql fail : " + str(e))

                finally:
                    curr.close()
                    conn.close()

        except Exception as e:
            logging.error("< Error > bpm_day_money_tolls - connect mssql fail : " + str(e))

        finally:
            curr_mssql.close()
            conn_mssql.close()

###########################
#
# day money parking fee
#
###########################
class day_money_parking_fee:

    #########
    # init
    #########
    def __init__(self):
        try:
            self.bpm_day_money_parking_fee()
            
        except Exception as e:
            logging.error('< Error > day money parking fee init : ' + str(e))
        finally:
            pass
   
    #################################
    # update_day_money_parking_fee
    #################################
    def update_day_money_parking_fee(self):
        try:
                    self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    self.curr = self.conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    #month = '0' + month if int(month) < 10 else month

                    # all day by month 
                    name_sql = f"select a_name from day_money_parking_fee where day_r_year='2023' and day_r_month='09' group by a_name order by day_r_day asc"
                    self.curr.execute(name_sql)
                    name_res = self.curr.fetchall() 

                    for name_val in name_res:
                        
                        day_sql = f"select day_r_day from day_money_parking_fee where day_r_year='2023' and day_r_month='09' group by day_r_day order by day_r_day asc"
                        self.curr.execute(day_sql)
                        day_res = self.curr.fetchall()

                        for day_val in day_res:
                             
                             search_sql = f"select * from day_money_parking_fee where day_r_year='2023' and day_r_month='09' and day_r_day='{day_val[0]}' and a_name='{name_val[0]}'"
                             self.curr.execute(search_sql)
                             search_res = self.curr.fetchone()

                             if search_res is None:
                                add_sql = f"insert into day_money_parking_fee(day_r_year , day_r_month , day_r_day , a_name , day_t_money) value('2023','09','{day_val[0]}','{name_val[0]}','0')"
                                self.curr.execute(add_sql)  
                    
                    #return day_res
                    self.conn.commit()
                    logging.info('< Msg > synchronization update day money parking fee 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

        except Exception as e:
            logging.error("< Error > connect mysql fail (update_day_money_parking_fee) : " + str(e))

        finally:
            self.curr.close()
            self.conn.close()

    ##########################
    # bpm_day_money_traffic
    ##########################
    def bpm_day_money_parking_fee(self):
        
        try: 
                if sys.platform.startswith('win'):
                    conn_str = f"DRIVER={{SQL Server}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                
                conn_mssql = pyodbc.connect(conn_str)
                curr_mssql = conn_mssql.cursor()  
                #sql = f"select ITEM14 , ITEM72 , ITEM15 , ITEM12 from ART00721676130332682_INS where ITEM26='true' and ITEM44='true' order by ITEM12 desc"
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                #############################
                sql  = f"select ITEM14 , ITEM51 , ITEM15 , ITEM12 , ITEM58 , ITEM57 , ITEM107 from ART00851684549915660_INS where ITEM75='true' and ITEM18='true'" 
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                # table : ART00851684549915660ITEM53
                # ITEM1:日期
                # ITEM3:日當
                # ITEM4:交通費
                # ITEM5:超里程
                # ITEM6:停車費
                # ITEM7:過路費
                # ITEM8:車票
                # ITEM9: Taxi
                # ITEM10:住宿
                # ITEM11:其他
                # ITEM12:油單
                # ITEM14:註記原因
                # ITEM15:加減金額
                #
                #############################
                sql2  = f"select a.ITEM14 , a.ITEM51 , a.ITEM15 , a.ITEM12 , a.ITEM58 , a.ITEM57 , a.ITEM107 , b.ITEM1 , b.ITEM6 , b.ITEM14 , b.ITEM15 " 
                sql2 += f"from ART00851684549915660_INS a left join ART00851684549915660ITEM53 b on a.INSID=b.INSID " 
                sql2 += f"where a.ITEM75='true' and a.ITEM18='true' and b.ITEM6 != '0' "
                curr_mssql.execute(sql2)
                res  = curr_mssql.fetchall()

                try:
                    conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    curr = conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    for val in res:
                        
                        #logging.info(f"{val[0]} , {val[1]} , {val[2]} , {val[3]}")
                        
                        r_year      = val[3][0:4]
                        r_month     = val[3][5:7]
                        r_day       = val[3][8:10]
                        day_r_year  = val[7][0:4]
                        day_r_month = val[7][5:7]
                        day_r_day   = val[7][8:10]
                        
                        ###############################################
                        #
                        # Check if there are records in the database
                        #
                        ###############################################
                        #s_mysql_sql = f"select * from day_money where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_date='{val[7]}' and day_t_money='{val[8]}'"
                        #s_mysql_sql = f"select * from day_money_parking_fee where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"
                        s_mysql_sql = f"select * from day_money_parking_fee where f_name='{val[0]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"
                        curr.execute(s_mysql_sql)
                        mysql_res = curr.fetchone()

                        #logging.info(s_mysql_sql)
                        #exit()

                        day_money = val[8]

                        #####################################
                        #
                        # get english name by chinese name
                        #
                        #####################################
                        g_e_mysql_sql = f"select employee_eng_name from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_e_mysql_sql)
                        g_e_name = curr.fetchone()

                        g_d_mysql_sql = f"select department_code from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_d_mysql_sql)
                        g_d_name = curr.fetchone()

                        if mysql_res is None:
                            
                            mysql_sql  = f"insert into day_money_parking_fee("
                            mysql_sql += f"r_date , r_year , r_month , r_day , " 
                            mysql_sql += f"f_name , a_name , e_name , d_name , t_money , c_t_money , erp_num , " 
                            mysql_sql += f"form_num , day_r_year , day_r_month , day_t_money , day_money_mark , day_money_diff" 
                            mysql_sql += f") " 
                            mysql_sql += f"value(" 
                            mysql_sql += f"'{val[3]}' , '{r_year}'     , '{r_month}'     , '{r_day}'  , "
                            mysql_sql += f"'{val[0]}' , '{val[1]}'     , '{g_e_name[0]}' , '{g_d_name[0]}' , '{val[2]}' , '{val[4]}' , '{val[5]}' ," 
                            mysql_sql += f"'{val[6]}' , '{day_r_year}' , '{day_r_month}' , '{0}' , '{val[9]}' , '{val[10]}'" 
                            mysql_sql += f")"
                            curr.execute(mysql_sql)
                            conn.commit()

                            #logging.info(f"{mysql_sql}") 
                            #logging.info(f"新日當資料 > 表單日期 : {val[3]} , 填表人 : {val[0]} , 申請人 : {val[1]} {g_e_name[0]} , 總金額 : {val[2]} , 日當日期 : {val[7]} , 日當金額 : {val[8]} , 註記原因 : {val[9]} , 加減金額 : {val[10]}")
                        
                        elif str(day_r_day) == '01':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money1='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            #logging.info(f"{mysql_sql}") 
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '02':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money2='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '03':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money3='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '04':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money4='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '05':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money5='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '06':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money6='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '07':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money7='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '08':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money8='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '09':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money9='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '10':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money10='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '11':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money11='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '12':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money12='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '13':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money13='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '14':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money14='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '15':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money15='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '16':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money16='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '17':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money17='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '18':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money18='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '19':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money19='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '20':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money20='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '21':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money21='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '22':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money22='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '23':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money23='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '24':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money24='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '25':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money25='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '26':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money26='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '27':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money27='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '28':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money28='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '29':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money29='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '30':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money30='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '31':
                            mysql_sql  = f"update day_money_parking_fee set day_t_money31='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        mysql_sql  = f"update day_money_parking_fee set day_t_total=("
                        mysql_sql += f"day_t_money1+day_t_money2+day_t_money3+day_t_money4+day_t_money5+day_t_money6+day_t_money7+day_t_money8+day_t_money9+day_t_money10+"
                        mysql_sql += f"day_t_money11+day_t_money12+day_t_money13+day_t_money14+day_t_money15+day_t_money16+day_t_money17+day_t_money18+day_t_money19+day_t_money20+"
                        mysql_sql += f"day_t_money21+day_t_money22+day_t_money23+day_t_money24+day_t_money25+day_t_money26+day_t_money27+day_t_money28+day_t_money29+day_t_money30+day_t_money31"
                        mysql_sql += f") "
                        mysql_sql += "where "
                        mysql_sql += f"r_date='{val[3]}'   and r_year='{r_year}'         and r_month='{r_month}'         and r_day='{r_day}'           and " 
                        mysql_sql += f"f_name='{val[0]}'   and a_name='{val[1]}'         and e_name='{g_e_name[0]}'      and t_money='{val[2]}'        and c_t_money='{val[4]}'      and erp_num='{val[5]}' and " 
                        mysql_sql += f"form_num='{val[6]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' and day_money_mark='{val[9]}' and day_money_diff='{val[10]}'" 
                        
                        curr.execute(mysql_sql)
                        conn.commit()
                    
                    logging.info('< Msg > update BPM day money 日當停車費 更新完成。')
                    print("------------------------------------------------------------------------------------------------------------------")

                except Exception as e:
                    logging.error("< Error > bpm_day_money_parking_fee - connect mysql fail : " + str(e))

                finally:
                    curr.close()
                    conn.close()

        except Exception as e:
            logging.error("< Error > bpm_day_money_parking_fee - connect mssql fail : " + str(e))

        finally:
            curr_mssql.close()
            conn_mssql.close()

###########################
#
# day money over traffic 
#
###########################
class day_money_over_traffic:

    #########
    # init
    #########
    def __init__(self):
        try:
            self.bpm_day_money_over_traffic()
            
        except Exception as e:
            logging.error('< Error > day money over traffic init : ' + str(e))
        finally:
            pass
   
    #############################
    # update_day_money_traffic
    #############################
    def update_day_money_over_traffice(self):
        try:
                    self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    self.curr = self.conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    #month = '0' + month if int(month) < 10 else month

                    # all day by month 
                    name_sql = f"select a_name from day_money_over_traffic where day_r_year='2023' and day_r_month='09' group by a_name order by day_r_day asc"
                    self.curr.execute(name_sql)
                    name_res = self.curr.fetchall() 

                    for name_val in name_res:
                        
                        day_sql = f"select day_r_day from day_money_over_traffic where day_r_year='2023' and day_r_month='09' group by day_r_day order by day_r_day asc"
                        self.curr.execute(day_sql)
                        day_res = self.curr.fetchall()

                        for day_val in day_res:
                             
                             search_sql = f"select * from day_money_over_traffic where day_r_year='2023' and day_r_month='09' and day_r_day='{day_val[0]}' and a_name='{name_val[0]}'"
                             self.curr.execute(search_sql)
                             search_res = self.curr.fetchone()

                             if search_res is None:
                                add_sql = f"insert into day_money_over_traffic(day_r_year , day_r_month , day_r_day , a_name , day_t_money) value('2023','09','{day_val[0]}','{name_val[0]}','0')"
                                self.curr.execute(add_sql)  
                    
                    #return day_res
                    self.conn.commit()
                    logging.info('< Msg > synchronization update day money over traffic 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

        except Exception as e:
            logging.error("< Error > connect mysql fail (update_day_money_over_traffic) : " + str(e))

        finally:
            self.curr.close()
            self.conn.close()

    ##########################
    # bpm_day_money_traffic
    ##########################
    def bpm_day_money_over_traffic(self):
        
        try: 
                if sys.platform.startswith('win'):
                    conn_str = f"DRIVER={{SQL Server}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                
                conn_mssql = pyodbc.connect(conn_str)
                curr_mssql = conn_mssql.cursor()  
                #sql = f"select ITEM14 , ITEM72 , ITEM15 , ITEM12 from ART00721676130332682_INS where ITEM26='true' and ITEM44='true' order by ITEM12 desc"
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                #############################
                sql  = f"select ITEM14 , ITEM51 , ITEM15 , ITEM12 , ITEM58 , ITEM57 , ITEM107 from ART00851684549915660_INS where ITEM75='true' and ITEM18='true'" 
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                # table : ART00851684549915660ITEM53
                # ITEM1:日期
                # ITEM3:日當
                # ITEM4:交通費
                # ITEM5:超里程
                # ITEM6:停車費
                # ITEM7:過路費
                # ITEM8:車票
                # ITEM9: Taxi
                # ITEM10:住宿
                # ITEM11:其他
                # ITEM12:油單
                # ITEM14:註記原因
                # ITEM15:加減金額
                #
                #############################
                sql2  = f"select a.ITEM14 , a.ITEM51 , a.ITEM15 , a.ITEM12 , a.ITEM58 , a.ITEM57 , a.ITEM107 , b.ITEM1 , b.ITEM5 , b.ITEM14 , b.ITEM15 " 
                sql2 += f"from ART00851684549915660_INS a left join ART00851684549915660ITEM53 b on a.INSID=b.INSID " 
                sql2 += f"where a.ITEM75='true' and a.ITEM18='true' and b.ITEM5 != '0' "
                curr_mssql.execute(sql2)
                res  = curr_mssql.fetchall()

                try:
                    conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    curr = conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    for val in res:
                        
                        #logging.info(f"{val[0]} , {val[1]} , {val[2]} , {val[3]}")
                        
                        r_year      = val[3][0:4]
                        r_month     = val[3][5:7]
                        r_day       = val[3][8:10]
                        day_r_year  = val[7][0:4]
                        day_r_month = val[7][5:7]
                        day_r_day   = val[7][8:10]
                        
                        ###############################################
                        #
                        # Check if there are records in the database
                        #
                        ###############################################
                        #s_mysql_sql = f"select * from day_money where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_date='{val[7]}' and day_t_money='{val[8]}'"
                        #s_mysql_sql = f"select * from day_money_over_traffic where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"
                        s_mysql_sql = f"select * from day_money_over_traffic where f_name='{val[0]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"
                        curr.execute(s_mysql_sql)
                        mysql_res = curr.fetchone()

                        #logging.info(s_mysql_sql)
                        #exit()

                        day_money = val[8]

                        #####################################
                        #
                        # get english name by chinese name
                        #
                        #####################################
                        g_e_mysql_sql = f"select employee_eng_name from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_e_mysql_sql)
                        g_e_name = curr.fetchone()

                        g_d_mysql_sql = f"select department_code from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_d_mysql_sql)
                        g_d_name = curr.fetchone()

                        if mysql_res is None:
                            
                            mysql_sql  = f"insert into day_money_over_traffic("
                            mysql_sql += f"r_date , r_year , r_month , r_day , " 
                            mysql_sql += f"f_name , a_name , e_name , d_name , t_money , c_t_money , erp_num , " 
                            mysql_sql += f"form_num , day_r_year , day_r_month , day_t_money , day_money_mark , day_money_diff" 
                            mysql_sql += f") " 
                            mysql_sql += f"value(" 
                            mysql_sql += f"'{val[3]}' , '{r_year}'     , '{r_month}'     , '{r_day}'  , "
                            mysql_sql += f"'{val[0]}' , '{val[1]}'     , '{g_e_name[0]}' , '{g_d_name[0]}'    , '{val[2]}' , '{val[4]}' , '{val[5]}' ," 
                            mysql_sql += f"'{val[6]}' , '{day_r_year}' , '{day_r_month}' , '{0}' , '{val[9]}' , '{val[10]}'" 
                            mysql_sql += f")"
                            curr.execute(mysql_sql)
                            conn.commit()

                            #logging.info(f"{mysql_sql}") 
                            #logging.info(f"新日當資料 > 表單日期 : {val[3]} , 填表人 : {val[0]} , 申請人 : {val[1]} {g_e_name[0]} , 總金額 : {val[2]} , 日當日期 : {val[7]} , 日當金額 : {val[8]} , 註記原因 : {val[9]} , 加減金額 : {val[10]}")
                        
                        elif str(day_r_day) == '01':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money1='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            #logging.info(f"{mysql_sql}") 
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '02':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money2='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '03':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money3='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '04':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money4='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '05':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money5='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '06':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money6='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '07':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money7='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '08':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money8='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '09':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money9='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '10':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money10='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '11':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money11='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '12':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money12='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '13':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money13='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '14':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money14='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '15':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money15='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '16':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money16='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '17':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money17='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '18':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money18='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '19':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money19='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '20':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money20='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '21':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money21='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '22':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money22='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '23':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money23='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '24':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money24='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '25':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money25='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '26':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money26='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '27':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money27='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '28':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money28='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '29':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money29='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '30':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money30='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '31':
                            mysql_sql  = f"update day_money_over_traffic set day_t_money31='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        mysql_sql  = f"update day_money_over_traffic set day_t_total=("
                        mysql_sql += f"day_t_money1+day_t_money2+day_t_money3+day_t_money4+day_t_money5+day_t_money6+day_t_money7+day_t_money8+day_t_money9+day_t_money10+"
                        mysql_sql += f"day_t_money11+day_t_money12+day_t_money13+day_t_money14+day_t_money15+day_t_money16+day_t_money17+day_t_money18+day_t_money19+day_t_money20+"
                        mysql_sql += f"day_t_money21+day_t_money22+day_t_money23+day_t_money24+day_t_money25+day_t_money26+day_t_money27+day_t_money28+day_t_money29+day_t_money30+day_t_money31"
                        mysql_sql += f") "
                        mysql_sql += "where "
                        mysql_sql += f"r_date='{val[3]}'   and r_year='{r_year}'         and r_month='{r_month}'         and r_day='{r_day}'           and " 
                        mysql_sql += f"f_name='{val[0]}'   and a_name='{val[1]}'         and e_name='{g_e_name[0]}'      and t_money='{val[2]}'        and c_t_money='{val[4]}'      and erp_num='{val[5]}' and " 
                        mysql_sql += f"form_num='{val[6]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' and day_money_mark='{val[9]}' and day_money_diff='{val[10]}'" 
                        
                        curr.execute(mysql_sql)
                        conn.commit()
                    
                    logging.info('< Msg > update BPM day money 日當超里程 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

                except Exception as e:
                    logging.error("< Error > bpm_day_money_over_traffic - connect mysql fail : " + str(e))

                finally:
                    curr.close()
                    conn.close()

        except Exception as e:
            logging.error("< Error > bpm_day_money_over_traffic - connect mssql fail : " + str(e))

        finally:
            curr_mssql.close()
            conn_mssql.close()

######################
#
# day money traffic 
#
######################
class day_money_traffic:

    #########
    # init
    #########
    def __init__(self):
        try:
            self.bpm_day_money_traffic()
            
        except Exception as e:
            logging.error('< Error > day money traffic init : ' + str(e))
        finally:
            pass
   
    #############################
    # update_day_money_traffic
    #############################
    def update_day_money_traffice(self):
        try:
                    self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    self.curr = self.conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    #month = '0' + month if int(month) < 10 else month

                    # all day by month 
                    name_sql = f"select a_name from day_money_traffic where day_r_year='2023' and day_r_month='09' group by a_name order by day_r_day asc"
                    self.curr.execute(name_sql)
                    name_res = self.curr.fetchall() 

                    for name_val in name_res:
                        
                        day_sql = f"select day_r_day from day_money_traffic where day_r_year='2023' and day_r_month='09' group by day_r_day order by day_r_day asc"
                        self.curr.execute(day_sql)
                        day_res = self.curr.fetchall()

                        for day_val in day_res:
                             
                             search_sql = f"select * from day_money_traffic where day_r_year='2023' and day_r_month='09' and day_r_day='{day_val[0]}' and a_name='{name_val[0]}'"
                             self.curr.execute(search_sql)
                             search_res = self.curr.fetchone()

                             if search_res is None:
                                add_sql = f"insert into day_money_traffic(day_r_year , day_r_month , day_r_day , a_name , day_t_money) value('2023','09','{day_val[0]}','{name_val[0]}','0')"
                                self.curr.execute(add_sql)  
                    
                    #return day_res
                    self.conn.commit()
                    logging.info('< Msg > synchronization update day money traffic 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

        except Exception as e:
            logging.error("< Error > connect mysql fail (update_day_money_traffice) : " + str(e))

        finally:
            self.curr.close()
            self.conn.close()

    ##########################
    # bpm_day_money_traffic
    ##########################
    def bpm_day_money_traffic(self):
        
        try: 
                if sys.platform.startswith('win'):
                    conn_str = f"DRIVER={{SQL Server}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                
                conn_mssql = pyodbc.connect(conn_str)
                curr_mssql = conn_mssql.cursor()  
                #sql = f"select ITEM14 , ITEM72 , ITEM15 , ITEM12 from ART00721676130332682_INS where ITEM26='true' and ITEM44='true' order by ITEM12 desc"
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                #############################
                sql  = f"select ITEM14 , ITEM51 , ITEM15 , ITEM12 , ITEM58 , ITEM57 , ITEM107 from ART00851684549915660_INS where ITEM75='true' and ITEM18='true'" 
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                # table : ART00851684549915660ITEM53
                # ITEM1:日期
                # ITEM3:日當
                # ITEM4:交通費
                # ITEM5:超里程
                # ITEM6:停車費
                # ITEM7:過路費
                # ITEM8:車票
                # ITEM9: Taxi
                # ITEM10:住宿
                # ITEM11:其他
                # ITEM12:油單
                # ITEM14:註記原因
                # ITEM15:加減金額
                #
                #############################
                sql2  = f"select a.ITEM14 , a.ITEM51 , a.ITEM15 , a.ITEM12 , a.ITEM58 , a.ITEM57 , a.ITEM107 , b.ITEM1 , b.ITEM4 , b.ITEM14 , b.ITEM15 " 
                sql2 += f"from ART00851684549915660_INS a left join ART00851684549915660ITEM53 b on a.INSID=b.INSID " 
                sql2 += f"where a.ITEM75='true' and a.ITEM18='true' and b.ITEM4 != '0' "
                curr_mssql.execute(sql2)
                res  = curr_mssql.fetchall()

                try:
                    conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    curr = conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    for val in res:
                        
                        #logging.info(f"{val[0]} , {val[1]} , {val[2]} , {val[3]}")
                        
                        r_year      = val[3][0:4]
                        r_month     = val[3][5:7]
                        r_day       = val[3][8:10]
                        day_r_year  = val[7][0:4]
                        day_r_month = val[7][5:7]
                        day_r_day   = val[7][8:10]
                        
                        ###############################################
                        #
                        # Check if there are records in the database
                        #
                        ###############################################
                        #s_mysql_sql = f"select * from day_money_traffice where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_date='{val[7]}' and day_t_money='{val[8]}'"
                        #s_mysql_sql = f"select * from day_money_traffic where r_date='{val[3]}' and t_money='{val[2]}' and f_name='{val[0]}' and a_name='{val[1]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"
                        s_mysql_sql = f"select * from day_money_traffic where f_name='{val[0]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"
                        curr.execute(s_mysql_sql)
                        mysql_res = curr.fetchone()

                        #logging.info(s_mysql_sql)
                        #exit()

                        day_money = val[8]

                        #####################################
                        #
                        # get english name by chinese name
                        #
                        #####################################
                        g_e_mysql_sql = f"select employee_eng_name from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_e_mysql_sql)
                        g_e_name = curr.fetchone()

                        g_d_mysql_sql = f"select department_code from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_d_mysql_sql)
                        g_d_name = curr.fetchone()

                        if mysql_res is None:
                            
                            mysql_sql  = f"insert into day_money_traffic("
                            mysql_sql += f"r_date , r_year , r_month , r_day , " 
                            mysql_sql += f"f_name , a_name , e_name , d_name , t_money , c_t_money , erp_num , " 
                            mysql_sql += f"form_num , day_r_year , day_r_month , day_t_money , day_money_mark , day_money_diff" 
                            mysql_sql += f") " 
                            mysql_sql += f"value(" 
                            mysql_sql += f"'{val[3]}' , '{r_year}'     , '{r_month}'     , '{r_day}'  , "
                            mysql_sql += f"'{val[0]}' , '{val[1]}'     , '{g_e_name[0]}' , '{g_d_name[0]}' , '{val[2]}' , '{val[4]}' , '{val[5]}' ," 
                            mysql_sql += f"'{val[6]}' , '{day_r_year}' , '{day_r_month}' , '{0}' , '{val[9]}' , '{val[10]}'" 
                            mysql_sql += f")"
                            curr.execute(mysql_sql)
                            conn.commit()

                            #logging.info(f"{mysql_sql}") 
                            #logging.info(f"新日當資料 > 表單日期 : {val[3]} , 填表人 : {val[0]} , 申請人 : {val[1]} {g_e_name[0]} , 總金額 : {val[2]} , 日當日期 : {val[7]} , 日當金額 : {val[8]} , 註記原因 : {val[9]} , 加減金額 : {val[10]}")
                        
                        elif str(day_r_day) == '01':
                            mysql_sql  = f"update day_money_traffic set day_t_money1='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            #logging.info(f"{mysql_sql}") 
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '02':
                            mysql_sql  = f"update day_money_traffic set day_t_money2='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '03':
                            mysql_sql  = f"update day_money_traffic set day_t_money3='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '04':
                            mysql_sql  = f"update day_money_traffic set day_t_money4='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '05':
                            mysql_sql  = f"update day_money_traffic set day_t_money5='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '06':
                            mysql_sql  = f"update day_money_traffic set day_t_money6='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '07':
                            mysql_sql  = f"update day_money_traffic set day_t_money7='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '08':
                            mysql_sql  = f"update day_money_traffic set day_t_money8='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '09':
                            mysql_sql  = f"update day_money_traffic set day_t_money9='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '10':
                            mysql_sql  = f"update day_money_traffic set day_t_money10='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '11':
                            mysql_sql  = f"update day_money_traffic set day_t_money11='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '12':
                            mysql_sql  = f"update day_money_traffic set day_t_money12='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '13':
                            mysql_sql  = f"update day_money_traffic set day_t_money13='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '14':
                            mysql_sql  = f"update day_money_traffic set day_t_money14='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '15':
                            mysql_sql  = f"update day_money_traffic set day_t_money15='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '16':
                            mysql_sql  = f"update day_money_traffic set day_t_money16='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '17':
                            mysql_sql  = f"update day_money_traffic set day_t_money17='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '18':
                            mysql_sql  = f"update day_money_traffic set day_t_money18='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '19':
                            mysql_sql  = f"update day_money_traffic set day_t_money19='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '20':
                            mysql_sql  = f"update day_money_traffic set day_t_money20='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '21':
                            mysql_sql  = f"update day_money_traffic set day_t_money21='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '22':
                            mysql_sql  = f"update day_money_traffic set day_t_money22='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '23':
                            mysql_sql  = f"update day_money_traffic set day_t_money23='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '24':
                            mysql_sql  = f"update day_money_traffic set day_t_money24='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '25':
                            mysql_sql  = f"update day_money_traffic set day_t_money25='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '26':
                            mysql_sql  = f"update day_money_traffic set day_t_money26='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '27':
                            mysql_sql  = f"update day_money_traffic set day_t_money27='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '28':
                            mysql_sql  = f"update day_money_traffic set day_t_money28='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '29':
                            mysql_sql  = f"update day_money_traffic set day_t_money29='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '30':
                            mysql_sql  = f"update day_money_traffic set day_t_money30='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '31':
                            mysql_sql  = f"update day_money_traffic set day_t_money31='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        mysql_sql  = f"update day_money_traffic set day_t_total=("
                        mysql_sql += f"day_t_money1+day_t_money2+day_t_money3+day_t_money4+day_t_money5+day_t_money6+day_t_money7+day_t_money8+day_t_money9+day_t_money10+"
                        mysql_sql += f"day_t_money11+day_t_money12+day_t_money13+day_t_money14+day_t_money15+day_t_money16+day_t_money17+day_t_money18+day_t_money19+day_t_money20+"
                        mysql_sql += f"day_t_money21+day_t_money22+day_t_money23+day_t_money24+day_t_money25+day_t_money26+day_t_money27+day_t_money28+day_t_money29+day_t_money30+day_t_money31"
                        mysql_sql += f") "
                        mysql_sql += "where "
                        mysql_sql += f"r_date='{val[3]}'   and r_year='{r_year}'         and r_month='{r_month}'         and r_day='{r_day}'           and " 
                        mysql_sql += f"f_name='{val[0]}'   and a_name='{val[1]}'         and e_name='{g_e_name[0]}'      and t_money='{val[2]}'        and c_t_money='{val[4]}'      and erp_num='{val[5]}' and " 
                        mysql_sql += f"form_num='{val[6]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' and day_money_mark='{val[9]}' and day_money_diff='{val[10]}'" 
                        
                        curr.execute(mysql_sql)
                        conn.commit()
                    
                    logging.info('< Msg > update BPM day money 日當交通費 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

                except Exception as e:
                    logging.error("< Error > bpm_day_money traffic (日當 交通費) - connect mysql fail : " + str(e))

                finally:
                    curr.close()
                    conn.close()

        except Exception as e:
            logging.error("< Error > bpm_day_money traffic - connect mssql fail : " + str(e))

        finally:
            curr_mssql.close()
            conn_mssql.close()

##################
#
# day money 
#
##################
class day_money:

    #########
    # init
    #########
    def __init__(self):
        try:
            self.bpm_day_money()
            
        except Exception as e:
            logging.error('< Error > day money init : ' + str(e))
        finally:
            pass
   
    #####################
    # update_day_money
    #####################
    def update_day_money(self):
        try:
                    self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    self.curr = self.conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    #month = '0' + month if int(month) < 10 else month

                    # all day by month 
                    name_sql = f"select a_name from day_money where day_r_year='2023' and day_r_month='09' group by a_name order by day_r_day asc"
                    self.curr.execute(name_sql)
                    name_res = self.curr.fetchall() 

                    for name_val in name_res:
                        
                        day_sql = f"select day_r_day from day_money where day_r_year='2023' and day_r_month='09' group by day_r_day order by day_r_day asc"
                        self.curr.execute(day_sql)
                        day_res = self.curr.fetchall()

                        for day_val in day_res:
                             
                             search_sql = f"select * from day_money where day_r_year='2023' and day_r_month='09' and day_r_day='{day_val[0]}' and a_name='{name_val[0]}'"
                             self.curr.execute(search_sql)
                             search_res = self.curr.fetchone()

                             if search_res is None:
                                add_sql = f"insert into day_money(day_r_year , day_r_month , day_r_day , a_name , day_t_money) value('2023','09','{day_val[0]}','{name_val[0]}','0')"
                                self.curr.execute(add_sql)  
                    
                    #return day_res
                    self.conn.commit()
                    logging.info('< Msg > synchronization day money 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

        except Exception as e:
            logging.error("< Error > connect mysql fail : " + str(e))

        finally:
            self.curr.close()
            self.conn.close()

    ##################
    # bpm_day_money
    ##################
    def bpm_day_money(self):
        
        try: 
                if sys.platform.startswith('win'):
                    conn_str = f"DRIVER={{SQL Server}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']}"  
                
                conn_mssql = pyodbc.connect(conn_str)
                curr_mssql = conn_mssql.cursor()  
                #sql = f"select ITEM14 , ITEM72 , ITEM15 , ITEM12 from ART00721676130332682_INS where ITEM26='true' and ITEM44='true' order by ITEM12 desc"
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                #############################
                sql  = f"select ITEM14 , ITEM51 , ITEM15 , ITEM12 , ITEM58 , ITEM57 , ITEM107 from ART00851684549915660_INS where ITEM75='true' and ITEM18='true'" 
                
                #############################
                #
                # table : ART00851684549915660_INS
                # ITEM12:申請日期
                # ITEM14:填表人(以此為主)
                # ITEM51:申請人
                # ITEM18:日當(true/false)
                # ITEM15:總金額
                # ITEM58:審核後總金額
                # ITEM57: ERP傳票號碼
                # ITEM75:已結案(true/false)
                # ITEM107:表單號碼
                #
                # table : ART00851684549915660ITEM53
                # ITEM1:日期
                # ITEM3:日當
                # ITEM14:註記原因
                # ITEM15:加減金額
                #
                #############################
                sql2 = f"select a.ITEM14 , a.ITEM51 , a.ITEM15 , a.ITEM12 , a.ITEM58 , a.ITEM57 , a.ITEM107 , b.ITEM1 , b.ITEM3 , b.ITEM14 , b.ITEM15 " 
                sql2 += f"from ART00851684549915660_INS a left join ART00851684549915660ITEM53 b on a.INSID=b.INSID "
                sql2 += f"where a.ITEM75='true' and a.ITEM18='true' and b.ITEM3 != '0' "

                curr_mssql.execute(sql2)
                res  = curr_mssql.fetchall()

                try:
                    conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
                    curr = conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    for val in res:
                        
                        #logging.info(f"{val[0]} , {val[1]} , {val[2]} , {val[3]}")
                        
                        r_year      = val[3][0:4]
                        r_month     = val[3][5:7]
                        r_day       = val[3][8:10]
                        day_r_year  = val[7][0:4]
                        day_r_month = val[7][5:7]

                        #logging.info(f"{val[7]} , {val[1]} , {day_r_year} , {day_r_month} , {day_r_day}")
                        
                        ###############################################
                        #
                        # Check if there are records in the database
                        #
                        ###############################################
                        s_mysql_sql = f"select * from day_money where f_name='{val[0]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}'"
                        curr.execute(s_mysql_sql)
                        mysql_res = curr.fetchone()

                        day_r_day = val[7][8:10]
                        #logging.info(s_mysql_sql)
                        #exit()

                        day_money = val[8]

                        #####################################
                        #
                        # get english name by chinese name
                        #
                        #####################################
                        g_e_mysql_sql = f"select employee_eng_name from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_e_mysql_sql)
                        g_e_name = curr.fetchone()

                        g_d_mysql_sql = f"select department_code from hr_a where employee_name='{val[1]}'"
                        curr.execute(g_d_mysql_sql)
                        g_d_name = curr.fetchone()

                        if mysql_res is None:
                            
                            mysql_sql  = f"insert into day_money("
                            mysql_sql += f"r_date , r_year , r_month , r_day , " 
                            mysql_sql += f"f_name , a_name , e_name , d_name , t_money , c_t_money , erp_num , " 
                            mysql_sql += f"form_num , day_r_year , day_r_month , day_t_money , day_money_mark , day_money_diff" 
                            mysql_sql += f") " 
                            mysql_sql += f"value(" 
                            mysql_sql += f"'{val[3]}' , '{r_year}'     , '{r_month}'     , '{r_day}'       , "
                            mysql_sql += f"'{val[0]}' , '{val[1]}'     , '{g_e_name[0]}' , '{g_d_name[0]}' , '{val[2]}' , '{val[4]}' , '{val[5]}' ," 
                            mysql_sql += f"'{val[6]}' , '{day_r_year}' , '{day_r_month}' , '{0}' , '{val[9]}' , '{val[10]}'" 
                            mysql_sql += f")"
                            curr.execute(mysql_sql)
                            conn.commit()

                            #logging.info(f"{mysql_sql}") 
                            #logging.info(f"新日當資料 > 表單日期 : {val[3]} , 填表人 : {val[0]} , 申請人 : {val[1]} {g_e_name[0]} , 總金額 : {val[2]} , 日當日期 : {val[7]} , 日當金額 : {val[8]} , 註記原因 : {val[9]} , 加減金額 : {val[10]}")
                        
                        elif str(day_r_day) == '01':
                            mysql_sql  = f"update day_money set day_t_money1='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            #logging.info(f"{mysql_sql}") 
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '02':
                            mysql_sql  = f"update day_money set day_t_money2='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()

                        elif str(day_r_day) == '03':
                            mysql_sql  = f"update day_money set day_t_money3='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '04':
                            mysql_sql  = f"update day_money set day_t_money4='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '05':
                            mysql_sql  = f"update day_money set day_t_money5='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '06':
                            mysql_sql  = f"update day_money set day_t_money6='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '07':
                            mysql_sql  = f"update day_money set day_t_money7='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '08':
                            mysql_sql  = f"update day_money set day_t_money8='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '09':
                            mysql_sql  = f"update day_money set day_t_money9='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        elif str(day_r_day) == '10':
                            mysql_sql  = f"update day_money set day_t_money10='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '11':
                            mysql_sql  = f"update day_money set day_t_money11='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '12':
                            mysql_sql  = f"update day_money set day_t_money12='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '13':
                            mysql_sql  = f"update day_money set day_t_money13='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '14':
                            mysql_sql  = f"update day_money set day_t_money14='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '15':
                            mysql_sql  = f"update day_money set day_t_money15='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '16':
                            mysql_sql  = f"update day_money set day_t_money16='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '17':
                            mysql_sql  = f"update day_money set day_t_money17='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '18':
                            mysql_sql  = f"update day_money set day_t_money18='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '19':
                            mysql_sql  = f"update day_money set day_t_money19='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '20':
                            mysql_sql  = f"update day_money set day_t_money20='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '21':
                            mysql_sql  = f"update day_money set day_t_money21='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '22':
                            mysql_sql  = f"update day_money set day_t_money22='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '23':
                            mysql_sql  = f"update day_money set day_t_money23='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '24':
                            mysql_sql  = f"update day_money set day_t_money24='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '25':
                            mysql_sql  = f"update day_money set day_t_money25='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '26':
                            mysql_sql  = f"update day_money set day_t_money26='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '27':
                            mysql_sql  = f"update day_money set day_t_money27='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '28':
                            mysql_sql  = f"update day_money set day_t_money28='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '29':
                            mysql_sql  = f"update day_money set day_t_money29='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '30':
                            mysql_sql  = f"update day_money set day_t_money30='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        elif str(day_r_day) == '31':
                            mysql_sql  = f"update day_money set day_t_money31='{day_money}' where "
                            mysql_sql += f"f_name='{val[0]}' and a_name='{val[1]}' and e_name='{g_e_name[0]}' " 
                            mysql_sql += f"and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' " 
                            
                            curr.execute(mysql_sql)
                            conn.commit()
                        
                        mysql_sql  = f"update day_money set day_t_total=("
                        mysql_sql += f"day_t_money1+day_t_money2+day_t_money3+day_t_money4+day_t_money5+day_t_money6+day_t_money7+day_t_money8+day_t_money9+day_t_money10+"
                        mysql_sql += f"day_t_money11+day_t_money12+day_t_money13+day_t_money14+day_t_money15+day_t_money16+day_t_money17+day_t_money18+day_t_money19+day_t_money20+"
                        mysql_sql += f"day_t_money21+day_t_money22+day_t_money23+day_t_money24+day_t_money25+day_t_money26+day_t_money27+day_t_money28+day_t_money29+day_t_money30+day_t_money31"
                        mysql_sql += f") "
                        mysql_sql += "where "
                        mysql_sql += f"r_date='{val[3]}'   and r_year='{r_year}'         and r_month='{r_month}'         and r_day='{r_day}'           and " 
                        mysql_sql += f"f_name='{val[0]}'   and a_name='{val[1]}'         and e_name='{g_e_name[0]}'      and t_money='{val[2]}'        and c_t_money='{val[4]}'      and erp_num='{val[5]}' and " 
                        mysql_sql += f"form_num='{val[6]}' and day_r_year='{day_r_year}' and day_r_month='{day_r_month}' and day_money_mark='{val[9]}' and day_money_diff='{val[10]}'" 
                        
                        curr.execute(mysql_sql)
                        conn.commit()
                    
                    logging.info('< Msg > update BPM day money 日當 更新完成。.')
                    print("------------------------------------------------------------------------------------------------------------------")

                    

                except Exception as e:
                    logging.error("< Error > bpm_day_money - connect mysql fail : " + str(e))

                finally:
                    curr.close()
                    conn.close()

        except Exception as e:
            logging.error("< Error > bpm_day_money - connect mssql fail : " + str(e))

        finally:
            curr_mssql.close()
            conn_mssql.close()

####################
#
# get vmware data
#
####################
class get_vmware_data:

    #########
    # init
    #########
    def __init__(self):
        try:
            
            ###############
            # get vmware
            ###############
            self.get_taipei_vmware()
            self.get_factory_vmware()
            
        except Exception as e:
            logging.error('< Error > get_vmware_data : ' + str(e))
        finally:
            pass
   
    #######################
    # get_factory_vmware
    #######################
    def get_factory_vmware(self):
        
        ### Specify the TLS version
        ssl_version  = ssl.PROTOCOL_SSLv23
        vcenter_host = '192.168.111.10'
        username     = 'administrator@vsphere.local'
        password     = 'OtsukatW168!'
        position     = 'factory'
        sum = 0
        
        # check time
        check_date   = time.strftime("%Y%m%d" , time.localtime()) 
        check_time   = time.strftime("%H:%M:%S" , time.localtime())
        check_d_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        try:
            ssl_context = ssl.SSLContext(ssl_version)
            ssl_context.verify_mode = ssl.CERT_NONE
            
            service_instance = connect.SmartConnect(
                host=vcenter_host,
                user=username,
                pwd=password,
                sslContext=ssl_context
            )

            ### get all vaware data
            content = service_instance.RetrieveContent()
            datacenter = content.rootFolder.childEntity[0]  

            ### get vmware list
            print(f"Virtual Machine ")
            vm_list = datacenter.vmFolder.childEntity

            conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
            curr = conn.cursor()

            try:
                for vm in vm_list:
                    if isinstance(vm, vim.VirtualMachine):
                        
                        sum += 1
                        print(f"Virtual Machine position  : {position}")
                        print(f"Virtual Machine Name      : {vm.name}")
                        print(f"Virtual Machine Power     : {vm.runtime.powerState}")
                        print(f"Virtual Machine OS        : {vm.guest.guestFullName}")
                        print(f"Virtual Machine OS state  : {vm.guest.guestState}")
                        print(f"Virtual Machine state     : {vm.runtime.connectionState}")
                        print(f"Virtual Machine boot time : {vm.runtime.bootTime}")
                        print(f"Virtual Machine IP        : {vm.guest.ipAddress}")
                        
                        # 取得虛擬機器的 CPU 使用量
                        cpu_usage_mhz = vm.summary.quickStats.overallCpuUsage
                        cpu_usage     = f"{vm.config.hardware.numCPU} threads / {cpu_usage_mhz} MHz"
                        print(f"Virtual Machine CPU       : {vm.config.hardware.numCPU} threads / {cpu_usage_mhz} MHz")
                        
                        # 取得虛擬機器的 RAM 使用量
                        memory_usage_mb = vm.summary.quickStats.guestMemoryUsage
                        ram_usage = f"{round(vm.config.hardware.memoryMB / (1024),2) } GB / {memory_usage_mb} MB"
                        print(f"Virtual Machine RAM       : {round(vm.config.hardware.memoryMB / (1024),2) } GB / {memory_usage_mb} MB")
                        
                        # 取得虛擬機器的儲存空間使用量
                        storage_usage_gb = (vm.summary.storage.committed / 1024 / 1024 / 1024)

                        for device in vm.config.hardware.device:
                            if isinstance(device, vim.vm.device.VirtualDisk):
                                    disk_capacity_gb = round(device.capacityInKB / (1024 * 1024), 2)
                                    hdd_usage = f" {disk_capacity_gb} GB / {storage_usage_gb:.2f} GB"
                                    print(f"Virtual Machine HDD       : {disk_capacity_gb} GB / {storage_usage_gb:.2f} GB")
                        
                        sql  = f"insert into otsuka_vmware(c_date , c_time , c_d_time , vm_position , vm_name , vm_power , vm_os , vm_os_state , vm_state , vm_boot_time , vm_ip , vm_cpu , vm_ram , vm_hdd) "
                        sql += f"value('{check_date}' , '{check_time}' , '{check_d_time}' , '{position}' , '{vm.name}' , '{vm.runtime.powerState}' , '{vm.guest.guestFullName}' , '{vm.guest.guestState}' , '{vm.runtime.connectionState}' , '{vm.runtime.bootTime}' , '{vm.guest.ipAddress}' , '{cpu_usage}' , '{ram_usage}' , '{hdd_usage}')"
                        curr.execute(sql)
                        conn.commit()
                        
                        print("---------------------------------------------------------------")

            except Exception as e:
                logging.info('<Error> get_factory_vmware : ' + str(e))
            finally:
                conn.close()
                curr.close()
                    

            print(f"total {sum}")

        except Exception as e:
            logging.error("< Error > get_factory_vmware : " + str(e))

        finally:
            pass


    ######################
    # get_taipei_vmware
    ######################
    def get_taipei_vmware(self):
        
        ### Specify the TLS version
        ssl_version  = ssl.PROTOCOL_SSLv23
        vcenter_host = '192.168.1.41'
        username     = 'administrator@vsphere.local'
        password     = 'OtsukatW2024!'
        position     = 'taipei'
        sum = 0
        
        try:
            ssl_context = ssl.SSLContext(ssl_version)
            ssl_context.verify_mode = ssl.CERT_NONE
            
            service_instance = connect.SmartConnect(
                host=vcenter_host,
                user=username,
                pwd=password,
                sslContext=ssl_context
            )

            ### get all vaware data
            content = service_instance.RetrieveContent()
            datacenter = content.rootFolder.childEntity[0]  

            ### get vmware list
            print(f"Virtual Machine ")
            vm_list = datacenter.vmFolder.childEntity

            # check time
            check_date   = time.strftime("%Y%m%d" , time.localtime()) 
            check_time   = time.strftime("%H:%M:%S" , time.localtime())
            check_d_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
            
            conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
            curr = conn.cursor()

            try:

                for vm in vm_list:
                    if isinstance(vm, vim.VirtualMachine):
                        sum += 1
                        print(f"Virtual Machine position  : {position}")
                        print(f"Virtual Machine Name      : {vm.name}")
                        print(f"Virtual Machine Power     : {vm.runtime.powerState}")
                        print(f"Virtual Machine OS        : {vm.guest.guestFullName}")
                        print(f"Virtual Machine OS state  : {vm.guest.guestState}")
                        print(f"Virtual Machine state     : {vm.runtime.connectionState}")
                        print(f"Virtual Machine boot time : {vm.runtime.bootTime}")
                        print(f"Virtual Machine IP        : {vm.guest.ipAddress}")
                        
                        # 取得虛擬機器的 CPU 使用量
                        cpu_usage_mhz = vm.summary.quickStats.overallCpuUsage
                        cpu_usage     = f"{vm.config.hardware.numCPU} threads / {cpu_usage_mhz} MHz"
                        print(f"Virtual Machine CPU       : {vm.config.hardware.numCPU} threads / {cpu_usage_mhz} MHz")
                        
                        # 取得虛擬機器的 RAM 使用量
                        memory_usage_mb = vm.summary.quickStats.guestMemoryUsage
                        ram_usage = f"{round(vm.config.hardware.memoryMB / (1024),2) } GB / {memory_usage_mb} MB"
                        print(f"Virtual Machine RAM       : {round(vm.config.hardware.memoryMB / (1024),2) } GB / {memory_usage_mb} MB")
                        
                        # 取得虛擬機器的儲存空間使用量
                        storage_usage_gb = (vm.summary.storage.committed / 1024 / 1024 / 1024)

                        for device in vm.config.hardware.device:
                            if isinstance(device, vim.vm.device.VirtualDisk):
                                disk_capacity_gb = round(device.capacityInKB / (1024 * 1024), 2)
                                hdd_usage = f" {disk_capacity_gb} GB / {storage_usage_gb:.2f} GB"
                                print(f"Virtual Machine HDD       : {disk_capacity_gb} GB / {storage_usage_gb:.2f} GB")

                        sql  = f"insert into otsuka_vmware(c_date , c_time , c_d_time , vm_position , vm_name , vm_power , vm_os , vm_os_state , vm_state , vm_boot_time , vm_ip , vm_cpu , vm_ram , vm_hdd) "
                        sql += f"value('{check_date}' , '{check_time}' , '{check_d_time}' , '{position}' , '{vm.name}' , '{vm.runtime.powerState}' , '{vm.guest.guestFullName}' , '{vm.guest.guestState}' , '{vm.runtime.connectionState}' , '{vm.runtime.bootTime}' , '{vm.guest.ipAddress}' , '{cpu_usage}' , '{ram_usage}' , '{hdd_usage}')"
                        curr.execute(sql)
                        conn.commit()

                        print("---------------------------------------------------------------")
            
            except Exception as e:
                logging.info('<Error> get_factory_vmware : ' + str(e))
            finally:
                conn.close()
                curr.close()


            print(f"total {sum}")

        except Exception as e:
            logging.error("< Error > get_taipei_vmware : " + str(e))

        finally:
            pass

############################
#
# get taipei spam maillog
#
############################
class get_spam_maillog:

    #########
    # init
    #########
    def __init__(self):
        try:
            
            #####################
            # get spam maillog
            #####################
            self.get_spam_maillog()
            
        except Exception as e:
            logging.error('< Error > get_spam_maillog : ' + str(e))
        finally:
            pass
   
    #####################
    # get_spam_maillog
    #####################
    def get_spam_maillog(self):

        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.bind(('0.0.0.0',514))
        
        while True:
            rec_msg, addr = udp.recvfrom(2048)
            client_ip, client_port = addr
            msg =  client_ip + " " + rec_msg.rstrip(b'\x00').decode('utf-8','ignore')
        
            print('Message from TWOP spam server : \n ', msg)    
            
            #filename = client_ip   + '_' +  str(date.today())  + ".log"

            ### write txt file
            #with open(filename,'a+',encoding = "utf-8") as f:
            #    f.write( msg + "\n")

            ### insert DB
            self.__connect__()
            try:
                contract_sql = f"insert into spam_maillog(spam_log) value('{msg}')"
                self.curr.execute(contract_sql)
                self.conn.commit()
                
            except Exception as e:
                logging.info(f"<Error> get_spam_maillog : {str(e)}")
            finally:
                self.__disconnect__()
    
    ################
    # __connect__ 
    ################
    def __connect__(self):
        
        try:
            self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
            self.curr = self.conn.cursor()

        except Exception as e:
            logging.info("< ERROR > __connect__ " + str(e))

        finally:
            pass

    ###################
    # __disconnect__
    ###################
    def __disconnect__(self):
        
        try:
            self.conn.commit()
            self.conn.close()

        except Exception as e:
            logging.info("< ERROR > __disconnect__ : " + str(e))

        finally:
            pass

########################################
#
# get factory card reader data record
#
########################################
class get_factory_card_reader_data_record:

    #########
    # init
    #########
    def __init__(self):
        try:
            
            ########################################
            # get factory card reader data record
            ########################################
            self.get_factory_card_reader_data_record()
            
        except Exception as e:
            logging.error('< Error > get_factory_card_reader_data_record : ' + str(e))
        finally:
            pass
   
    ########################################
    # get_factory_card_reader_data_record
    ########################################
    def get_factory_card_reader_data_record(self):
        
        #conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],passwd=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])    
        #curr = conn.cursor()
        self.__connect__()
        
        # time record
        now_month = time.strftime("%Y%m" , time.localtime())
        now_day   = time.strftime("%Y%m%d" , time.localtime())
        now_time  = time.strftime("%H:%M:%S" , time.localtime())
        
        try:
            
            c_sql = f"create table card_reader_{now_month}(no int not null primary key AUTO_INCREMENT,r_date date null,r_time varchar(30) null,p_id varchar(30) null,p_name varchar(30) null,e_id varchar(30) null,e_name varchar(30) null,position varchar(30) null,c_action varchar(30) null,c_id varchar(30) null,c_remark varchar(50) null,d_name varchar(50) null)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"
            self.curr.execute(c_sql)
            
            #logging.info(f'create tb : {now_day} successful.')

        except Exception as e:
        
            ###########################
            # read txt save to MySQL
            ###########################
            file_path = 'D:/Card_input/' + now_day + '.txt'

            with open(file_path , 'r') as file:
                line = file.readlines()

            for val in line:
                data = val.split(',')
                data[0] = data[0].strip()
                #print(f"{data[0]} / {data[1]} / {data[2]} / {data[3]} / {data[4]} / {data[5]} / {data[6]} / {data[7]} / {data[8]} / {data[9]}")

                s_sql  = f"select * from card_reader_{now_month} where r_date='{data[0]}' and r_time='{data[1]}' and p_id='{data[2]}' and e_name='{data[6]}'"
                self.curr.execute(s_sql)
                self.res = self.curr.fetchone()

                if self.res is None:

                    s_sql2 = f"select p_name from card_reader_p where p_id='{data[2]}'"
                    self.curr.execute(s_sql2)
                    self.res2 = self.curr.fetchall()

                    for p_name in self.res2:
                        
                        d_name = str(data[9]).strip()
                        a_sql = f"insert into card_reader_{now_month}(r_date , r_time , p_id , e_id , e_name , c_action , c_id , position , c_remark , p_name , d_name) value('{data[0]}','{data[1]}','{data[2]}','{data[3]}','{data[6]}','{data[5]}','{data[7]}','{data[4]}','{data[8]}','{p_name[0]}','{d_name}')"
                        #a_sql = f"insert into card_reader_{now_day}(r_date , r_time , p_id , e_id , e_name , c_action , c_id , position , c_remark , p_name , d_name) value('{data[0]}','{data[1]}','{data[2]}','{data[3]}','{data[6]}','{data[5]}','{data[7]}','{data[4]}','{data[8]}','{p_name[0]}','{data[9]}')"
                        self.curr.execute(a_sql)

            logging.info(f'add data to tb : card_reader_{now_month} successful.')
                
        finally:
            self.__disconnect__()
    
    ################
    # __connect__ 
    ################
    def __connect__(self):
        
        try:
            self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
            self.curr = self.conn.cursor()

        except Exception as e:
            logging.info("< ERROR > __connect__ " + str(e))

        finally:
            pass

    ###################
    # __disconnect__
    ###################
    def __disconnect__(self):
        
        try:
            self.conn.commit()
            self.conn.close()

        except Exception as e:
            logging.info("< ERROR > __disconnect__ : " + str(e))

        finally:
            pass

#################################
#
# get AD Server account record
#
#################################
class get_ad_server_account_record:

    #########
    # init
    #########
    def __init__(self):
        try:
            
            #####################
            # get spam maillog
            #####################
            self.get_ad_server_account_record()
            
        except Exception as e:
            logging.error('< Error > get_ad_server_account_record init : ' + str(e))
        finally:
            pass
   
    #################################
    # get_ad_server_account_record
    #################################
    def get_ad_server_account_record(self):

        # link WMS AD Server
        conn_str_wms   = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={parameter.otsuka_factory9_wms['host']};DATABASE={parameter.otsuka_factory9_wms['db']};UID={parameter.otsuka_factory9_wms['user']};PWD={parameter.otsuka_factory9_wms['password']};TrustServerCertificate=yes;"  
        conn_mssql_wms = pyodbc.connect(conn_str_wms)
        curr_mssql_wms = conn_mssql_wms.cursor()

        # AD 服务器和登录凭据
        server_address = '192.168.1.10'
        username       = 'otsukatw\\administrator'
        password       = 'OtsukatW2024!'
        add_sum        = 0
        update_sum     = 0

        # 连接到服务器
        server = Server(server_address, port=389, get_info=ALL, use_ssl=False)  # 建议使用 SSL
        conn   = Connection(server, user=username, password=password, auto_bind=True, authentication='SIMPLE')

        # 验证连接是否成功
        if not conn.bind():
            logging.info("<Msg> 無法連接到 AD 伺服器 !")
            exit()

        # 搜索用户信息
        search_base   = 'dc=otsukatw,dc=corp'  
        search_filter = '(objectClass=user)'  
        attributes    = ['sAMAccountName', 'userPrincipalName', 'displayName', 'userAccountControl' , 'department' , 'title']  

        # 执行搜索
        conn.search(search_base, search_filter, attributes=attributes)

        # 输出所有用户账号信息和启用状态
        for entry in conn.entries:
            account_name = entry.sAMAccountName
            display_name = entry.displayName
            user_principal_name = entry.userPrincipalName
            user_control = int(entry.userAccountControl.value)
            user_dep     = entry.department
            user_title   = entry.title

            # 检查帐户是否已启用
            is_enabled = not (user_control & 2)  
            status     = "Enabled" if is_enabled else "Disabled"

            w_user   = str(account_name).strip()
            w_email  = str(user_principal_name).strip()
            data     = str(display_name).strip().split('-')
            w_dep    = str(user_dep).strip()
            w_title  = str(user_title).strip()
            

            # 去掉前後空白
            if len(data) >= 2:
                w_e_name = data[0].strip()
                w_c_name = data[1].strip()
            else:
                w_e_name = data[0].strip()  
                w_c_name = ""  
                w_status = str(status).strip()

            # AD Server 帳號比對後新增更新到 WMS Server 權限資料庫
            try:
                
                # check time
                r_date   = time.strftime("%Y-%m-%d" , time.localtime()) 
                r_time   = time.strftime("%H:%M:%S" , time.localtime())
                r_d_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

                w_name_up = w_user.upper() + '$'

                s_ad_sql  = '''
                            SELECT * from wms_ad_account where u_name = ? 
                '''

                curr_mssql_wms.execute(s_ad_sql , (w_user,w_name_up,))
                res = curr_mssql_wms.fetchone()

                if res is None:
                    
                    i_ad_sql = ''' 
                                insert into wms_ad_account(u_name , u_email , u_e_name , u_c_name , w_status , w_dep , w_title , c_d_time , c_date , c_time) values(?,?,?,?,?,?,?,?,?,?)
                    '''

                    curr_mssql_wms.execute(i_ad_sql , (w_user,w_email,w_e_name,w_c_name,w_status,w_dep,w_title,r_d_time,r_date,r_time,))
                    conn_mssql_wms.commit()
                    add_sum += 1
                    
                    logging.info(f"WMS 倉儲系統 權限管理 , 帳號 {w_user.ljust(20)} 已新增 , 姓名 {w_c_name.ljust(50)} , 帳號狀態為 {w_status.ljust(20)}")

                else:
                    
                    u_ad_sql = '''
                            update wms_ad_account set w_status = ? , c_date = ? , c_time = ? where u_name = ? 
                    '''

                    curr_mssql_wms.execute(u_ad_sql , (w_status,r_date,r_time,w_user,))
                    conn_mssql_wms.commit()
                    update_sum += 1
                    
                    logging.info(f"WMS 倉儲系統 權限管理 , 帳號 {w_user.ljust(20)} 已存在 , 姓名 {w_c_name.ljust(50)} , 並已更新帳號狀態為 {w_status.ljust(20)}")

            except Exception as e:
                logging.info(f"\n\n<Error> get_ad_server_account_record : {str(e)}\n\n")

            finally:
                pass
        
        print('----------------------------------------------------------------------------------------------------------------------------------')
        logging.info(f"<Result> 共新增 {add_sum} 筆 , 共更新 {update_sum} 筆。\n")

        conn.unbind()
        conn_mssql_wms.close()
    
    ##########################
    # __connect_mssql_wms__ 
    ##########################
    def __connect_mssql_wms__(self):
        
        try:
            ############
            # FreeTDS 
            ############
            #conn_str = f"DRIVER={{FreeTDS}};SERVER={parameter.otsuka_factory2['host']};port=1433;DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']};TrustServerCertificate=yes;"  
            #conn_str = f"DRIVER={{FreeTDS}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']};TrustServerCertificate=yes;"  
            #self.conn_mssql = pyodbc.connect(conn_str)
            #self.curr_mssql = self.conn_mssql.cursor()
            
            ##################################
            # ODBC Driver 18 for SQL Server 
            ##################################
            conn_str_wms = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={parameter.otsuka_factory9_wms['host']};DATABASE={parameter.otsuka_factory9_wms['db']};UID={parameter.otsuka_factory9_wms['user']};PWD={parameter.otsuka_factory9_wms['pwd']};TrustServerCertificate=yes;"  
            self.conn_mssql_wms = pyodbc.connect(conn_str_wms)
            self.curr_mssql_wms = self.conn_mssql_wms.cursor()
            
        except Exception as e:
            logging.info("\n\n<Error> __connect_mssql_wms__ " + str(e))

        finally:
            pass
            #self.curr_mssql.close()
            #self.conn_mssql.close()
    
    #############################
    # __disconnect_mssql_wms__ 
    #############################
    def __disconnect_mssql_wms__(self):
        
        try:
            self.conn_mssql_wms.close()
            
        except Exception as e:
            logging.info("\n\n<Error> __disconnect_mssql_wms__ " + str(e))

        finally:
            pass

    
    ################
    # __connect__ 
    ################
    def __connect__(self):
        
        try:
            self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
            self.curr = self.conn.cursor()

        except Exception as e:
            logging.info("< ERROR > __connect__ " + str(e))

        finally:
            pass

    ###################
    # __disconnect__
    ###################
    def __disconnect__(self):
        
        try:
            self.conn.commit()
            self.conn.close()

        except Exception as e:
            logging.info("< ERROR > __disconnect__ : " + str(e))

        finally:
            pass


#########################################
#
# test function
#
#########################################
class test_function:

    #########
    # init
    #########
    def __init__(self , name):
        try:
            
            #########################################
            # test_function
            #########################################
            self.name = name
            
        except Exception as e:
            logging.error('< Error > test_function init : ' + str(e))
        finally:
            pass
            
    ###############
    # start_task
    ###############
    async def start_task(self):
        await asyncio.gather(self.do_task() , self.do_task2())

    #############
    # do_task2
    #############
    async def do_task2(self):
        conn = await aiomysql.connect(** parameter.otsuka_factory8)
        try:
            cursor = await conn.cursor()
            query = f'select * from w_import_form order by no desc'
            await cursor.execute(query)

            res = await cursor.fetchall()
            print(f'{self.name} , Total rows : {len(res)}')

            for val in res:
                print(f'{val}')

            print('\n')

        except aiomysql.Error as e:
            logging.info(f'<Error> do task2 : {str(e)}')
        finally:
            conn.close()

    ##################
    # do_task
    ##################    
    async def do_task(self):
        
        # Connect to the database
        conn = await aiomysql.connect(**parameter.otsuka_factory8)
        
        try:
            # Create a cursor
            cursor = await conn.cursor()
            
            # SQL query to execute
            query = "SELECT * FROM w_basic_product_form"
            await cursor.execute(query)
            
            # Fetch all results
            results = await cursor.fetchall()
            print(f"{self.name} , Total rows: {len(results)}")
            
            # Process results
            for row in results:
                print(row)
            
            print('\n')

        except Exception as e:
            logging.info(f'<Error> test function : {str(e)}')
                
        finally:
            # Close the connection
            conn.close()

#########################################
#
# update otsuka product basic data
#
#########################################
class update_otsuka_product_basic_data:

    #########
    # init
    #########
    def __init__(self):
        try:
            
            #########################################
            # update otsuka product basic data
            #########################################
            self.update_otsuka_product_basic_data()
            
        except Exception as e:
            logging.error('< Error > get_ad_server_account_record init : ' + str(e))
        finally:
            pass
   
    
    ##############################
    #
    # 商品基本檔單
    #
    ##############################
    def update_otsuka_product_basic_data(self):
        
        # 豐田外倉專案代號
        otsuka_project_no = 'M812' # update M812 20240411
        
        # check time
        check_date   = time.strftime("%Y-%m-%d" , time.localtime()) 
        check_date2  = time.strftime("%Y%m%d" , time.localtime()) 
        check_time   = time.strftime("%H:%M:%S" , time.localtime())
        check_d_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        
        self.__erp_connect_mssql__()
        
        try:
            erp_basic_product_sql  = f"SELECT " 
            erp_basic_product_sql += f"INVMB.MB001 AS '品號', INVMB.MB002 AS '品名', INVMB.MB003 AS '規格', '輸液' AS '產品類型' , "
            erp_basic_product_sql += f"'Y' AS '效期需求', 'Y' AS '批號需求', 'N' AS '恆溫倉需求' , "
            erp_basic_product_sql += f"INVMB.MB073 AS '中包裝 PCS 數', INVMB.MB016 AS '中包裝單位', 0 AS '大包裝 PCS 數', '' AS '大包裝單位', "
            erp_basic_product_sql += f"1 AS '基礎包裝量', INVMB.MB004 AS '基礎包裝單位' , 'N' AS '冷藏需求', 'N' AS '管制藥' , "
            erp_basic_product_sql += f"INVMB.MB013 AS '國際條碼', 'Y' AS '刷讀條碼' "
            erp_basic_product_sql += f"FROM INVMB "
            erp_basic_product_sql += f"WHERE MB001 LIKE 'XH%' "
            erp_basic_product_sql += f"AND  MB002 NOT LIKE '%不再使用%' "

            self.erp_curr_mssql.execute(erp_basic_product_sql)
            res = self.erp_curr_mssql.fetchall()

            ### backup - save to mysql
            self.__connect__()
            self.__connect_mssql_wms_product__()
            b_p_sum = 0

            for val in res:
                
                ##########################################################
                #
                # send otsuka erp 商本基本檔單 save to WMS otsuka_product 
                #
                ##########################################################
                try:
                    
                    check_erp_basic_product_sql = f"select * from wms_product_basic_data where f_b_num='{val[0]}' and f_b_name='{val[1]}'"
                    self.curr_mssql_wms_product.execute(check_erp_basic_product_sql)
                    check_erp_basic_product_res = self.curr_mssql_wms_product.fetchone()

                    if check_erp_basic_product_res is None:
                        erp_basic_product_sql  = f"insert into wms_product_basic_data( "
                        erp_basic_product_sql += f"c_date  , c_time , c_d_time , "
                        erp_basic_product_sql += f"f_b_num , f_b_name , f_spec , f_limit , f_b_limit , f_a_temp , f_l_medicial , f_l_cool , f_b_package , "
                        erp_basic_product_sql += f"f_b_p_unit , f_m_package , f_m_p_unit , f_b_p_amount , f_b_p_unit2 , f_i_barcode , f_p_type , f_rw_barcode "
                        erp_basic_product_sql += f") values( "
                        erp_basic_product_sql += f"'{check_date}' , '{check_time}' , '{check_d_time}' , "
                        erp_basic_product_sql += f"'{val[0]}'  , '{val[1]}' , '{val[2]}' , '{val[3]}', '{val[4]}' , '{val[5]}' , '{val[6]}' , '{val[7]}' , "
                        erp_basic_product_sql += f"'{val[8]}'  , '{val[9]}' , '{val[10]}' , '{val[11]}', '{val[12]}' , '{val[13]}' , '{val[14]}' , '{val[15]}' , "
                        erp_basic_product_sql += f"'{val[16]}' )"
                        
                        self.curr_mssql_wms_product.execute(erp_basic_product_sql)
                        self.conn_mssql_wms_product.commit()

                        ### 商品基本檔 更新完成
                        logging.info(f'<Message> ERP 商品基本檔共 {b_p_sum} 筆 , WMS 更新完成.')

                    else:
                        ### 商品基本檔 無新商品資料
                        logging.info(f'<Message> ERP 商品基本檔 , {val[0]} - {val[1]} , WMS 商品資料已建立.')

                except Exception as e:
                    logging.info(f"<Error> save to WMS mssql - basic product form: {str(e)}")
                finally: 
                    pass
                
                ##########################################################
                #
                # send otsuka erp 商本基本檔單 to MySQL
                #
                ##########################################################
                try:
                    
                    check_erp_basic_product_sql = f"select * from w_basic_product_form where item_2='{val[0]}' and item_3='{val[1]}'"
                    self.curr.execute(check_erp_basic_product_sql)
                    check_erp_basic_product_res = self.curr.fetchone()

                    if check_erp_basic_product_res is None:
                        erp_basic_product_sql  = f"insert into w_basic_product_form( "
                        erp_basic_product_sql += f"c_date  , c_time , c_d_time , "
                        erp_basic_product_sql += f"item_1 , item_2 , item_3 , item_4 , item_5 , item_6 ,item_7 ,item_8 ,item_9 , "
                        erp_basic_product_sql += f"item_10 , item_11 , item_12 , item_13 , item_14 , item_15 , item_16 , item_17 , item_18 , d_from "
                        erp_basic_product_sql += f") value( "
                        erp_basic_product_sql += f"'{check_date}' , '{check_time}' , '{check_d_time}' , '{otsuka_project_no}' , "
                        erp_basic_product_sql += f"'{val[0]}'  , '{val[1]}' , '{val[2]}' , '{val[3]}', '{val[4]}' , '{val[5]}' , '{val[6]}' , '{val[7]}' , "
                        erp_basic_product_sql += f"'{val[8]}'  , '{val[9]}' , '{val[10]}' , '{val[11]}', '{val[12]}' , '{val[13]}' , '{val[14]}' , '{val[15]}' , "
                        erp_basic_product_sql += f"'{val[16]}' , 'ERP' )"
                        
                        self.curr.execute(erp_basic_product_sql)
                        self.conn.commit()

                        ### 商品基本檔 更新完成
                        logging.info(f'<Message> ERP 商品基本檔共 {b_p_sum} 筆 , 更新完成.')

                    else:
                        ### 商品基本檔 無新商品資料
                        logging.info(f'<Message> ERP 商品基本檔 , {val[0]} - {val[1]} , 商品資料已建立.')

                except Exception as e:
                    logging.info(f"<Error> save to mysql - basic product form: {str(e)}")
                finally: 
                    pass
            
            self.__disconnect__()
            self.__disconnect_mssql_wms_product__()

            
        except Exception as e:
            logging.info(f"<Error> update_otsuka_product_basic_data : " + str(e))
        finally:
            self.__erp_disconnect_mssql__()

    ###################################
    # __connect_mssql_wms_product__ 
    ###################################
    def __connect_mssql_wms_product__(self):
        
        try:
            ############
            # FreeTDS 
            ############
            #conn_str = f"DRIVER={{FreeTDS}};SERVER={parameter.otsuka_factory2['host']};port=1433;DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']};TrustServerCertificate=yes;"  
            #conn_str = f"DRIVER={{FreeTDS}};SERVER={parameter.otsuka_factory2['host']};DATABASE={parameter.otsuka_factory2['db']};UID={parameter.otsuka_factory2['user']};PWD={parameter.otsuka_factory2['pwd']};TrustServerCertificate=yes;"  
            #self.conn_mssql = pyodbc.connect(conn_str)
            #self.curr_mssql = self.conn_mssql.cursor()
            
            ##################################
            # ODBC Driver 18 for SQL Server 
            ##################################
            conn_str_wms_product = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={parameter.otsuka_wms_pro_1_61['host']};DATABASE={parameter.otsuka_wms_pro_1_61['db']};UID={parameter.otsuka_wms_pro_1_61['user']};PWD={parameter.otsuka_wms_pro_1_61['password']};TrustServerCertificate=yes;"  
            self.conn_mssql_wms_product = pyodbc.connect(conn_str_wms_product)
            self.curr_mssql_wms_product = self.conn_mssql_wms_product.cursor()
            
            
        except Exception as e:
            logging.info("\n<Error> __connect_mssql_wms_product__ " + str(e))

        finally:
            pass
            #self.curr_mssql.close()
            #self.conn_mssql.close()
    
    ####################################
    # __disconnect_mssql_wms_product__ 
    ####################################
    def __disconnect_mssql_wms_product__(self):
        
        try:
            self.curr_mssql_wms_product.close()
            self.conn_mssql_wms_product.close()
            
        except Exception as e:
            logging.info("\n<Error> __disconnect_mssql_wms_product__ " + str(e))

        finally:
            pass
    
    
    ################
    # __connect__ 
    ################
    def __connect__(self):
        
        
        ####################
        # mysql.connectot
        ####################
        try:
            self.conn = mysql.connector.connect(**parameter.otsuka_factory8)
            self.curr = self.conn.cursor()
        except mysql.connector.Error as e:
            logging.info(f"<Error> __connect__ : {str(e)}")
            
        finally:
            pass
        
        ############
        # pymysql
        ############
        '''
        try:
            self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
            self.curr = self.conn.cursor()

        except Exception as e:
            logging.info("< ERROR > __connect__ " + str(e))

        finally:
            pass
        '''

    ###################
    # __disconnect__
    ###################
    def __disconnect__(self):
        
        try:
            self.conn.commit()
            self.conn.close()

        except Exception as e:
            logging.info("< ERROR > __disconnect__ : " + str(e))

        finally:
            pass

    ###########################
    # __erp_connect_mssql__ 
    ###########################
    def __erp_connect_mssql__(self):
        
        try:
            ##################################
            # ODBC Driver 17 for SQL Server 
            ##################################
            erp_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={parameter.otsuka_factory5['host']};DATABASE={parameter.otsuka_factory5['db']};UID={parameter.otsuka_factory5['user']};PWD={parameter.otsuka_factory5['pwd']};TrustServerCertificate=yes;"  
            self.erp_conn_mssql = pyodbc.connect(erp_conn_str)
            self.erp_curr_mssql = self.erp_conn_mssql.cursor()

        except Exception as e:
            logging.info("< ERROR > __erp_connect_mssql__ " + str(e))

        finally:
            pass
    
    ##############################
    # __erp_disconnect_mssql__ 
    ##############################
    def __erp_disconnect_mssql__(self):
        
        try:
            self.erp_curr_mssql.close()
            self.erp_conn_mssql.close()
            
        except Exception as e:
            logging.info("< ERROR > __erp_disconnect_mssql__ " + str(e))

        finally:
            pass

#########################################
#
# update factory warehouse data record
#
#########################################
class update_factory_warehouse_data_record:

    #########
    # init
    #########
    def __init__(self):
        try:
            
            #########################################
            # update_factory_warehouse_data_record
            #########################################
            self.update_factory_warehouse_data_record()
            
        except Exception as e:
            logging.error('< Error > get_ad_server_account_record init : ' + str(e))
        finally:
            pass
   
    
    ##############################
    #
    # 商品基本檔單
    #
    ##############################
    def update_otsuka_product_basic_data(self):
        
        # 豐田外倉專案代號
        otsuka_project_no = 'M812' # update M812 20240411
        
        # check time
        check_date   = time.strftime("%Y-%m-%d" , time.localtime()) 
        check_date2  = time.strftime("%Y%m%d" , time.localtime()) 
        check_time   = time.strftime("%H:%M:%S" , time.localtime())
        check_d_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        
        self.__erp_connect_mssql__()
        
        try:
            erp_basic_product_sql  = f"SELECT " 
            erp_basic_product_sql += f"INVMB.MB001 AS '品號', INVMB.MB002 AS '品名', INVMB.MB003 AS '規格', '輸液' AS '產品類型' , "
            erp_basic_product_sql += f"'Y' AS '效期需求', 'Y' AS '批號需求', 'N' AS '恆溫倉需求' , "
            erp_basic_product_sql += f"INVMB.MB073 AS '中包裝 PCS 數', INVMB.MB016 AS '中包裝單位', 0 AS '大包裝 PCS 數', '' AS '大包裝單位', "
            erp_basic_product_sql += f"1 AS '基礎包裝量', INVMB.MB004 AS '基礎包裝單位' , 'N' AS '冷藏需求', 'N' AS '管制藥' , "
            erp_basic_product_sql += f"INVMB.MB013 AS '國際條碼', 'Y' AS '刷讀條碼' "
            erp_basic_product_sql += f"FROM INVMB "
            erp_basic_product_sql += f"WHERE MB001 LIKE 'XH%' "
            erp_basic_product_sql += f"AND  MB002 NOT LIKE '%不再使用%' "

            self.erp_curr_mssql.execute(erp_basic_product_sql)
            res = self.erp_curr_mssql.fetchall()

            ### backup - save to mysql
            self.__connect__()
            b_p_sum = 0

            for val in res:

                b_p_sum += 1

                ###  出貨日期為訂單日期自動+1天 , 遇六+2天,遇日+1天 工作天
                today = date.today()
                next_business_day = self.add_business_day(today)

                ### json format
                otsuka_basic_product = {'WMS104_01':otsuka_project_no , 
                                        'WMS104_03':val[0] , 
                                        'WMS104_04':val[1] , 
                                        'WMS104_05':val[2] , 
                                        'WMS104_08':val[3] , 
                                        'WMS104_09':val[4] , 
                                        'WMS104_10':val[5] , 
                                        'WMS104_11':val[6] , 
                                        'WMS104_14':val[7] , 
                                        'WMS104_15':val[8] , 
                                        'WMS104_16':val[9] , 
                                        'WMS104_17':val[10] , 
                                        'WMS104_18':val[11] , 
                                        'WMS104_19':val[12] , 
                                        'WMS104_22':val[13] ,
                                        'WMS104_24':val[14] , 
                                        'WMS104_25':val[15] , 
                                        'WMS104_28':val[16] 
                                        }
                
                json_val = json.dumps(otsuka_basic_product , sort_keys=True , indent=4 , separators=(',',':') , default=self.date_converter , ensure_ascii=False)
                #print(json_val)
                
                ##########################################################
                #
                # send otsuka erp 商本基本檔單 json format to 豐田外倉 API 
                #
                ##########################################################
                try:
                    
                    check_erp_basic_product_sql = f"select * from w_basic_product_form where item_2='{val[0]}' and item_3='{val[1]}'"
                    self.curr.execute(check_erp_basic_product_sql)
                    check_erp_basic_product_res = self.curr.fetchone()

                    if check_erp_basic_product_res is None:
                        erp_basic_product_sql  = f"insert into w_basic_product_form( "
                        erp_basic_product_sql += f"c_date  , c_time , c_d_time , "
                        erp_basic_product_sql += f"item_1 , item_2 , item_3 , item_4 , item_5 , item_6 ,item_7 ,item_8 ,item_9 , "
                        erp_basic_product_sql += f"item_10 , item_11 , item_12 , item_13 , item_14 , item_15 , item_16 , item_17 , item_18 , d_from "
                        erp_basic_product_sql += f") value( "
                        erp_basic_product_sql += f"'{check_date}' , '{check_time}' , '{check_d_time}' , '{otsuka_project_no}' , "
                        erp_basic_product_sql += f"'{val[0]}'  , '{val[1]}' , '{val[2]}' , '{val[3]}', '{val[4]}' , '{val[5]}' , '{val[6]}' , '{val[7]}' , "
                        erp_basic_product_sql += f"'{val[8]}'  , '{val[9]}' , '{val[10]}' , '{val[11]}', '{val[12]}' , '{val[13]}' , '{val[14]}' , '{val[15]}' , "
                        erp_basic_product_sql += f"'{val[16]}' , 'ERP' )"
                        
                        self.curr.execute(erp_basic_product_sql)
                        self.conn.commit()

                        #####################################
                        # 寫入豐田外倉 - 使用商品基本檔建立 API
                        #####################################
                        #encoded_data = json_val.encode('utf-8')
                        #response = requests.post(basic_product_url , data=encoded_data , headers={'Content-Type':'application/json'})
                        #print(response.text)

                        ### 商品基本檔 更新完成
                        logging.info(f'<Message> ERP 商品基本檔共 {b_p_sum} 筆 , 更新完成.')

                    else:
                        pass

                except Exception as e:
                    logging.info(f"<Error> save to mysql - basic product form: {str(e)}")
                finally: 
                    pass
            
            
            
            self.__disconnect__()

            
        except Exception as e:
            logging.info(f"<Error> update_factory_warehouse_data_record erp basic product build : " + str(e))
        finally:
            self.__erp_disconnect_mssql__()

    #########################################
    # update factory warehouse data record
    #########################################
    def update_factory_warehouse_data_record(self):
        
        ##############
        #
        # variables
        #
        ##############
        
        # 豐田外倉專案代號
        otsuka_project_no = 'M812' # update M812 20240411
        
        # 豐田外倉 出貨單 API URL
        export_formal_url = "http://vts.fengtien.com.tw/Webservice/API/WMSA20" 
        export_test_url   = "http://122.147.154.213/Webservice/API/WMSA20"
        export_url        = export_test_url # 目前使用正式機 20240411
        
        # 豐田外倉 進貨單 API URL
        import_formal_url = "http://vts.fengtien.com.tw/Webservice/API/WMS200"
        import_test_url   = "http://122.147.154.213/Webservice/API/WMS200"
        import_url        = import_test_url # 目前使用正式機 20240411

        # 豐田外倉 商品基本檔單 API URL
        basic_product_formal_url = "http://vts.fengtien.com.tw/Webservice/API/WMS104"
        basic_product_test_url   = "http://122.147.154.213/Webservice/API/WMS104"
        basic_product_url        = basic_product_test_url # 目前使用正式機 20240411

        # check time
        check_date   = time.strftime("%Y-%m-%d" , time.localtime()) 
        check_date2  = time.strftime("%Y%m%d" , time.localtime()) 
        check_time   = time.strftime("%H:%M:%S" , time.localtime())
        check_d_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ##############################
        #
        # 商品基本檔單
        #
        ##############################
        self.__erp_connect_mssql__()
        
        try:
            erp_basic_product_sql  = f"SELECT " 
            erp_basic_product_sql += f"INVMB.MB001 AS '品號', INVMB.MB002 AS '品名', INVMB.MB003 AS '規格', '輸液' AS '產品類型' , "
            erp_basic_product_sql += f"'Y' AS '效期需求', 'Y' AS '批號需求', 'N' AS '恆溫倉需求' , "
            erp_basic_product_sql += f"INVMB.MB073 AS '中包裝 PCS 數', INVMB.MB016 AS '中包裝單位', 0 AS '大包裝 PCS 數', '' AS '大包裝單位', "
            erp_basic_product_sql += f"1 AS '基礎包裝量', INVMB.MB004 AS '基礎包裝單位' , 'N' AS '冷藏需求', 'N' AS '管制藥' , "
            erp_basic_product_sql += f"INVMB.MB013 AS '國際條碼', 'Y' AS '刷讀條碼' "
            erp_basic_product_sql += f"FROM INVMB "
            erp_basic_product_sql += f"WHERE MB001 LIKE 'XH%' "
            erp_basic_product_sql += f"AND  MB002 NOT LIKE '%不再使用%' "

            self.erp_curr_mssql.execute(erp_basic_product_sql)
            res = self.erp_curr_mssql.fetchall()

            ### backup - save to mysql
            self.__connect__()
            b_p_sum = 0

            for val in res:

                b_p_sum += 1

                ###  出貨日期為訂單日期自動+1天 , 遇六+2天,遇日+1天 工作天
                today = date.today()
                next_business_day = self.add_business_day(today)

                ### json format
                otsuka_basic_product = {'WMS104_01':otsuka_project_no , 
                                        'WMS104_03':val[0] , 
                                        'WMS104_04':val[1] , 
                                        'WMS104_05':val[2] , 
                                        'WMS104_08':val[3] , 
                                        'WMS104_09':val[4] , 
                                        'WMS104_10':val[5] , 
                                        'WMS104_11':val[6] , 
                                        'WMS104_14':val[7] , 
                                        'WMS104_15':val[8] , 
                                        'WMS104_16':val[9] , 
                                        'WMS104_17':val[10] , 
                                        'WMS104_18':val[11] , 
                                        'WMS104_19':val[12] , 
                                        'WMS104_22':val[13] ,
                                        'WMS104_24':val[14] , 
                                        'WMS104_25':val[15] , 
                                        'WMS104_28':val[16] 
                                        }
                
                json_val = json.dumps(otsuka_basic_product , sort_keys=True , indent=4 , separators=(',',':') , default=self.date_converter , ensure_ascii=False)
                #print(json_val)
                
                ##########################################################
                #
                # send otsuka erp 商本基本檔單 json format to 豐田外倉 API 
                #
                ##########################################################
                try:
                    
                    check_erp_basic_product_sql = f"select * from w_basic_product_form where item_2='{val[0]}' and item_3='{val[1]}'"
                    self.curr.execute(check_erp_basic_product_sql)
                    check_erp_basic_product_res = self.curr.fetchone()

                    if check_erp_basic_product_res is None:
                        erp_basic_product_sql  = f"insert into w_basic_product_form( "
                        erp_basic_product_sql += f"c_date  , c_time , c_d_time , "
                        erp_basic_product_sql += f"item_1 , item_2 , item_3 , item_4 , item_5 , item_6 ,item_7 ,item_8 ,item_9 , "
                        erp_basic_product_sql += f"item_10 , item_11 , item_12 , item_13 , item_14 , item_15 , item_16 , item_17 , item_18 , d_from "
                        erp_basic_product_sql += f") value( "
                        erp_basic_product_sql += f"'{check_date}' , '{check_time}' , '{check_d_time}' , '{otsuka_project_no}' , "
                        erp_basic_product_sql += f"'{val[0]}'  , '{val[1]}' , '{val[2]}' , '{val[3]}', '{val[4]}' , '{val[5]}' , '{val[6]}' , '{val[7]}' , "
                        erp_basic_product_sql += f"'{val[8]}'  , '{val[9]}' , '{val[10]}' , '{val[11]}', '{val[12]}' , '{val[13]}' , '{val[14]}' , '{val[15]}' , "
                        erp_basic_product_sql += f"'{val[16]}' , 'ERP' )"
                        
                        self.curr.execute(erp_basic_product_sql)
                        self.conn.commit()

                        #####################################
                        # 寫入豐田外倉 - 使用商品基本檔建立 API
                        #####################################
                        #encoded_data = json_val.encode('utf-8')
                        #response = requests.post(basic_product_url , data=encoded_data , headers={'Content-Type':'application/json'})
                        #print(response.text)

                        ### 商品基本檔 更新完成
                        logging.info(f'<Message> ERP 商品基本檔共 {b_p_sum} 筆 , 更新完成.')

                    else:
                        pass

                except Exception as e:
                    logging.info(f"<Error> save to mysql - basic product form: {str(e)}")
                finally: 
                    pass
            
            
            
            self.__disconnect__()

            
        except Exception as e:
            logging.info(f"<Error> update_factory_warehouse_data_record erp basic product build : " + str(e))
        finally:
            self.__erp_disconnect_mssql__()
        
        
        
        ##############################
        #
        # 進貨單
        #
        ##############################
        
        ##############
        #
        # ERP 進貨單
        #
        ##############
        self.__erp_connect_mssql__()
        try:
            erp_import_sql  = f"SELECT '豐田指定代號' AS '豐田指定專案代號', LEFT(INVTA.TA001,3)+'-'+INVTA.TA002 AS '採購單號', "
            erp_import_sql += f"ROW_NUMBER() OVER(ORDER BY TA001) AS '採購單序號', INVTA.TA014  AS '預計進貨日', "
            erp_import_sql += f"INVTB.TB004 AS '商品編號', 'OTSUKATW' AS '供貨商代號', '台灣大塚' AS '供應商名稱',  "
            erp_import_sql += f"'' AS '供應商料號', INVTB.TB014 AS '批號', INVTB.TB015 AS '效期', "
            erp_import_sql += f"INVTB.TB007 AS '預計進貨數', LEFT(INVTA.TA001,3)+'-'+INVTA.TA002 AS '供應商單號', "
            erp_import_sql += f"'' AS '備註' "
            erp_import_sql += f"FROM INVTA, INVTB "
            erp_import_sql += f"WHERE INVTA.TA009='12' "
            erp_import_sql += f"AND INVTA.TA001='201' "
            erp_import_sql += f"AND INVTA.TA006='Y' "
            erp_import_sql += f"AND INVTB.TB013='0062' "
            erp_import_sql += f"AND INVTA.TA001=INVTB.TB001 "
            erp_import_sql += f"AND INVTA.TA002=INVTB.TB002 "

            self.erp_curr_mssql.execute(erp_import_sql)
            res = self.erp_curr_mssql.fetchall()
            
            ### backup - save to mysql
            self.__connect__()
            b_p_sum = 0

            for val in res:
                
                

                b_p_sum += 1

                ###  出貨日期為訂單日期自動+1天 , 遇六+2天,遇日+1天 工作天
                today = date.today()
                next_business_day = self.add_business_day(today)

                ### 轉換為日期對象 , 進貨日期
                date_obj = datetime.strptime(str(val[3]), '%Y%m%d')
                formatted_date = date_obj.strftime('%Y/%m/%d')

                ### 轉換為日期對象 , 效期
                date_obj2 = datetime.strptime(str(val[9]), '%Y%m%d')
                formatted_date2 = date_obj2.strftime('%Y/%m/%d')

                ### 預計進貨數
                in_amount = int(val[10])

                ### json format
                otsuka_import_product = {'WMS200_02':otsuka_project_no , 
                                         'WMS200_05':val[1] ,
                                         'Data':[{
                                            'WMS200_06':val[2] ,
                                            'WMS200_07':formatted_date ,
                                            'WMS200_08':val[4] ,
                                            'WMS200_09':val[5] ,
                                            'WMS200_10':val[6] ,
                                            'WMS200_11':val[7] ,
                                            'WMS200_12':val[8] ,
                                            'WMS200_13':formatted_date2,
                                            'WMS200_14':in_amount ,
                                            'WMS200_26':val[11] ,
                                            'WMS200_94':val[12] 
                                        }]}
                
                import_json_val = json.dumps(otsuka_import_product , sort_keys=True , indent=4 , separators=(',',':') , default=self.date_converter , ensure_ascii=False)
                #print(import_json_val)
                
                ##########################################################
                #
                # send otsuka erp 進貨單 json format to 豐田外倉 API 
                #
                ##########################################################
                try:
                    
                    check_erp_import_sql = f"select * from w_import_form where item_2='{val[1]}'"
                    self.curr.execute(check_erp_import_sql)
                    check_erp_import_res = self.curr.fetchone()

                    if check_erp_import_res is None:
                        erp_import_sql  = f"insert into w_import_form( "
                        erp_import_sql += f"c_date  , c_time , c_d_time , "
                        erp_import_sql += f"item_1 , item_2 , item_3 , item_4 , item_5 , item_6 ,item_7 ,item_8 ,item_9 , "
                        erp_import_sql += f"item_10 , item_11 , item_12 , item_13 , d_from "
                        erp_import_sql += f") value( "
                        erp_import_sql += f"'{check_date}' , '{check_time}' , '{check_d_time}' , '{otsuka_project_no}' , "
                        erp_import_sql += f"'{val[1]}' , '{val[2]}' , '{val[3]}', '{val[4]}' , '{val[5]}' , '{val[6]}' , '{val[7]}' , "
                        erp_import_sql += f"'{val[8]}'  , '{val[9]}' , '{val[10]}' , '{val[11]}' , '{val[12]}' , 'ERP' ) "
                        
                        self.curr.execute(erp_import_sql)
                        self.conn.commit()

                        ##############################
                        # 寫入豐田外倉 - 進貨單建立 API
                        ##############################
                        #import_encoded_data = import_json_val.encode('utf-8')
                        #import_response = requests.post(import_url , data=import_encoded_data , headers={'Content-Type':'application/json'})
                        #print(import_response.text)

                        ###  進貨單 更新完成
                        logging.info(f'<Message> ERP 進貨單共 {b_p_sum} 筆 , 更新完成.')

                    else:
                        pass

                except Exception as e:
                    logging.info(f"<Error> save to mysql - import form: {str(e)}")
                finally: 
                    pass
            
            

            self.__disconnect__()
            
        except Exception as e:
            logging.info(f"<Error> update_factory_warehouse_data_record erp import : " + str(e))
        finally:
            self.__erp_disconnect_mssql__()
        

        ##############################
        #
        # 出貨單
        #
        ##############################
        
        ##############
        #
        # ERP 出貨單
        # 
        ##############
        self.__erp_connect_mssql__()
        try:
            erp_export_sql  = f"SELECT '豐田指定代號' AS '豐田指定專案代號', INVTA.TA014  AS '訂單日期', "
            erp_export_sql += f"INVTA.TA014  AS '指送日期', LEFT(INVTA.TA001,3)+'-'+INVTA.TA002 AS '出貨單號', "
            erp_export_sql += f"CASE INVTB.TB013 WHEN '0011' THEN 'TA' "
            erp_export_sql += f"WHEN '004' THEN 'TL' "
            erp_export_sql += f"END  AS '客戶代號', "
            erp_export_sql += f"CASE INVTB.TB013 WHEN '0011' THEN '大隆興' "
            erp_export_sql += f"WHEN '004'  THEN '台灣大塚' "
            erp_export_sql += f"END  AS '客戶名稱', "
            erp_export_sql += f"'' AS '客戶電話', '' AS  '訂單備註', 0 AS '代收款',"
            erp_export_sql += f"1 AS '配次', 1 AS '出貨代碼', "
            erp_export_sql += f"ROW_NUMBER() OVER(ORDER BY TA001) AS '出貨序號', INVTB.TB005 AS '品號', "
            erp_export_sql += f"INVTB.TB014 AS '指定批號', INVTB.TB015 AS '指定效期', INVTB.TB007 AS '出貨數量', "
            erp_export_sql += f"'' AS '建議售價', '' AS '單價', '' AS '總價', '' AS '明細備註', "
            erp_export_sql += f"'' AS '子單號', '' AS '子單折扣', '' AS '子單運費', '' AS '健保代碼', "
            erp_export_sql += f"'' AS '英文品號', '台灣大塚製藥' AS '藥廠名稱', '' AS '慢簽單號' "
            erp_export_sql += f"FROM INVTA, INVTB "
            erp_export_sql += f"WHERE INVTA.TA009='12' "
            erp_export_sql += f"AND INVTA.TA001='204' "
            erp_export_sql += f"AND INVTA.TA006='Y' "
            erp_export_sql += f"AND INVTB.TB013='0062' "
            erp_export_sql += f"AND INVTA.TA001=INVTB.TB001 "
            erp_export_sql += f"AND INVTA.TA002=INVTB.TB002 "

            self.erp_curr_mssql.execute(erp_export_sql)
            res = self.erp_curr_mssql.fetchall()
            
            ### backup - save to mysql
            self.__connect__()
            b_p_sum = 0

            for val in res:

                b_p_sum += 1

                ###  出貨日期為訂單日期自動+1天 , 遇六+2天,遇日+1天 工作天
                today = date.today()
                next_business_day = self.add_business_day(today)

                ### json format
                otsuka_import_product = {'WMS20_01':otsuka_project_no , 
                                        'WMS20_02':val[0] , 
                                        'WMS20_03':val[1] ,
                                        'WMS20_05':val[2] , 
                                        'WMS20_11':val[3] ,
                                        'WMS20_12':val[4] , 
                                        'WMS20_13':val[5] ,
                                        'WMS20_14':val[6] , 
                                        'WMS20_15':val[7] ,
                                        'WMS20_20':val[8] ,
                                        'WMS20_45':val[9] ,
                                        'WMS20_99':val[10] ,       
                                        'Data':[{
                                            'WMS20_06':val[11] ,
                                            'WMS20_07':val[12] ,
                                            'WMS20_08':val[13] ,
                                            'WMS20_09':val[14] ,
                                            'WMS20_10':val[15] ,
                                            'WMS20_26':val[16] ,
                                            'WMS20_32':val[17] ,
                                            'WMS20_35':val[18] ,
                                            'WMS20_37':val[19] ,
                                            'WMS20_39':val[20] ,
                                            'WMS20_40':val[21] ,
                                            'WMS20_41':val[22] ,
                                            'WMS20_42':val[23] ,
                                            'WMS20_43':val[24] ,
                                            'WMS20_44':val[25] ,
                                            'WMS20_46':val[26] ,
                                                }] 
                                        }
                
                export_json_val = json.dumps(otsuka_import_product , sort_keys=True , indent=4 , separators=(',',':') , default=self.date_converter , ensure_ascii=False)
                #print(export_json_val)

                ##########################################################
                #
                # send otsuka erp 出貨單 json format to 豐田外倉 API 
                #
                ##########################################################
                try:
                    
                    check_erp_export_sql = f"select * from w_export_form where item_4='{val[3]}'"
                    self.curr.execute(check_erp_export_sql)
                    check_erp_export_res = self.curr.fetchone()

                    if check_erp_export_res is None:
                        erp_export_sql  = f"insert into w_export_form( "
                        erp_export_sql += f"c_date  , c_time , c_d_time , "
                        erp_export_sql += f"item_1 , item_2 , item_3 , item_4 , item_5 , item_6 ,item_7 ,item_8 ,item_9 , "
                        erp_export_sql += f"item_10 , item_11 , item_12 , item_13 , item_14 , item_15 ,item_16 ,item_17 ,item_18 , "
                        erp_export_sql += f"item_19 , item_20 , item_21 , item_22 , item_23 , item_24 ,item_25 ,item_26 ,item_27 , "
                        erp_export_sql += f"item_28 , d_from "
                        erp_export_sql += f") value( "
                        erp_export_sql += f"'{check_date}' , '{check_time}' , '{check_d_time}' , '{otsuka_project_no}' , "
                        erp_export_sql += f"'{val[0]}'  , '{val[1]}'  , '{val[2]}'  , '{val[3]}' , '{val[4]}'  , '{val[5]}'  , '{val[6]}'  , '{val[7]}'  , "
                        erp_export_sql += f"'{val[8]}'  , '{val[9]}'  , '{val[10]}' , '{val[11]}', '{val[12]}' , '{val[13]}' , '{val[14]}' , '{val[15]}' , "
                        erp_export_sql += f"'{val[16]}' , '{val[17]}' , '{val[18]}' , '{val[19]}', '{val[20]}' , '{val[21]}' , '{val[22]}' , '{val[23]}' , "
                        erp_export_sql += f"'{val[24]}' , '{val[25]}' , '{val[26]}' , 'ERP' ) "
                        
                        self.curr.execute(erp_import_sql)
                        self.conn.commit()

                        ##############################
                        # 寫入豐田外倉 - 出貨單建立 API
                        ##############################
                        #export_encoded_data = export_json_val.encode('utf-8')
                        #export_response = requests.post(export_url , data=export_encoded_data , headers={'Content-Type':'application/json'})
                        #print(export_response.text)

                        ###  進貨單 更新完成
                        logging.info(f'<Message> ERP 出貨單共 {b_p_sum} 筆 , 更新完成.')

                    else:
                        pass

                except Exception as e:
                    logging.info(f"<Error> save to mysql - export form: {str(e)}")
                finally: 
                    pass
            
            

            self.__disconnect__()
            
        except Exception as e:
            logging.info(f"<Error> update_factory_warehouse_data_record erp export : " + str(e))
        finally:
            self.__erp_disconnect_mssql__()


        ##############
        #
        # SS2 注文單
        #
        ##############    
        self.__ss2_connect_mssql__()

        try:

            ### variable
            r_date = time.strftime("%Y_%m" , time.localtime())
            r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
            r_day  = time.strftime("%Y-%m-%d" , time.localtime())

            '''
            ss2_sql   = f"select "
            ss2_sql  += f"ORDERS.ODR_DATE , ORDERS.SHIP_DATE  , ORDERS.ODR_NO    , ORDERS.CUST_ID , ORDERS.CUST_NAME , ORDERS.SHIP_ADDRESS , "
            ss2_sql  += f"ORDERS.CNT_TEL  , ORDERS.REMARK     , ORDERSITEM.WH_ID , ORDERS.ODR_NO  , ORDERSITEM.DESP  , ORDERSITEM.LOT_NO , "
            ss2_sql  += f"ORDERSITEM.EXPIRE_DATE , (ORDERSITEM.QTY + ORDERSITEM.QTY_TEMP + ORDERSITEM.QTY_TEMP2 + ORDERSITEM.QTY_SAMPLE) as export_total , ORDERS.PO "
            ss2_sql  += f"from ORDERS LEFT JOIN ORDERSITEM ON ORDERS.ID = ORDERSITEM.ODR_ID WHERE ORDERS.ODR_DATE = '{check_date}'"
            '''

            ss2_sql   = f"select "
            ss2_sql  += f"ORDERS.ODR_DATE    , ORDERS.ODR_DATE , ORDERS.ODR_NO , ORDERS.CUST_ID , ORDERS.CUST_NAME , ORDERS.SHIP_ADDRESS , ORDERS.CNT_TEL , "
            ss2_sql  += f"ORDERSITEM.PROD_ID , ORDERSITEM.LOT_NO , ORDERSITEM.EXPIRE_DATE , (ORDERSITEM.QTY+ORDERSITEM.QTY_TEMP+ORDERSITEM.QTY_TEMP2+ORDERSITEM.QTY_SAMPLE) , "
            ss2_sql  += f"ORDERS.SHIP_DATE   , (ORDERS.REMARK+ORDERSITEM.REMARK) "
            ss2_sql  += f"from ORDERS LEFT JOIN ORDERSITEM ON ORDERS.ID = ORDERSITEM.ODR_ID WHERE ORDERS.ODR_DATE = '{check_date}'"

            self.ss2_curr_mssql.execute(ss2_sql)
            ss2_res = self.ss2_curr_mssql.fetchall()

            ### backup - save to mysql
            #self.__connect__()
            ss2_i_sum = 0

            export_ss2_res = []

            for val in ss2_res:

                ss2_i_sum += 1

                '''
                value  = f"訂單日期 {val[0]} \n"
                value += f"銷貨單號 {val[1]}{val[2]} \n"
                value += f"序號    {ss2_i_sum} \n"
                value += f"客戶代號 {val[3]} \n"
                value += f"客戶名稱 {val[4]} \n"
                value += f"客戶地址 {val[5]} \n"
                value += f"客戶電話 {val[6]} \n"
                value += f"品號    {val[7]} \n"
                value += f"批號    {val[8]} \n"
                value += f"效期    {val[9]} \n"
                value += f"出貨數量 {val[10]} \n"
                value += f"指送日期 {val[11]} \n"
                value += f"備註    {val[12]} \n"
                value += f"代收款   N \n"
                value += f"配送狀況 A \n"
                '''
                '''
                value  = f"{o_date}/"
                value += f"{o_num}{val[2]}/"
                value += f"{ss2_i_sum}/"
                value += f"{val[3]}/"
                value += f"{val[4]}/"
                value += f"{val[5]}/"
                value += f"{val[6]}/"
                value += f"{val[7]}/"
                value += f"{val[8]}/"
                value += f"{val[9]}/"
                value += f"{val[10]}/"
                value += f"{val[11]}/"
                value += f"{val[12]}/"
                value += f"N/"
                value += f"A\n"
                print(value)
                '''

                o_date = str(val[0]).replace("-","")
                o_num = str(val[1]).replace("-","")
                o_num_list = f"{o_num}{val[2]}" 

                export_ss2_res.append((o_date,o_num_list,ss2_i_sum,val[3],val[4],val[5],val[6],val[7],val[8],val[9],val[10],val[11],val[12],'N','A'))
                 
            #####################################################
            #
            # export excel
            #
            # path : home/otsuka/otsuka_platform/excel_toyota     
            #
            #####################################################
            workbook   = openpyxl.Workbook()
            sheet      = workbook.active
            ss2_excel_file = f"/home/otsuka/otsuka_platform/excel_toyota/ss2_export_{r_day}.xlsx"

            ### title
            sheet.freeze_panes = 'A2'
            title = ['訂單日期','銷貨單號','序號','客戶代號','客戶名稱','客戶地址','客戶電話','品號','批號','效期','出貨數量','指送日期','備註','代收款','配送狀況']

            for col_num , header in enumerate(title , 1):
                cell            = sheet.cell(row=1 , column=col_num , value=header)
                cell.font       = Font(bold=True , color="FFFFFF")
                cell.alignment  = Alignment(horizontal="center")
                cell.fill       = PatternFill(start_color="A9A9A9", end_color="A9A9A9", fill_type="solid")  # 背景顏色設為灰色

            ### content
            for row_idx , row_data in enumerate(export_ss2_res , start=2):
                for col_idx , cell_val in enumerate(row_data , start=1):
                    sheet.cell(row=row_idx , column=col_idx , value=cell_val)

            workbook.save(ss2_excel_file)   
            
            ####################
            #
            # 寄 Email 及附件
            #
            ####################
            try:
                ### variable
                subject         = "< SS2 注文單 - 豐田外倉 >"
                body            = f"{subject} \n\n 日期 : {r_day} \n\n 內容 : SS2 注文單 - 豐田外倉 , 請參照附件 \n\n 檔案 : ss2_export_{r_day}.xlsx"
                r_year          = time.strftime("%Y" , time.localtime())
                r_month         = time.strftime("%Y-%m" , time.localtime())
                r_day           = time.strftime("%Y-%m-%d" , time.localtime())
                r_daytime       = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
                e_status        = time.strftime("%H" , time.localtime())

                sender_email    = "Jason_Hung@otsuka.com.tw"
                password        = "otsuka#123"
                
                ### email 
                receiver_email1 = "Jason_Hung@otsuka.com.tw"   # 資訊部
                receiver_email2 = "dixie.tai@otsuka.com.tw"    # 營支部
                receiver_email3 = "shelly.chung@otsuka.com.tw" # 財務部
                
                
                ### 資訊部 Jason
                self.send_email_and_file(subject , body , r_day ,r_year , r_month , r_daytime  ,  check_date , sender_email , password , receiver_email1 , e_status)
                ### 營支部 dixie
                self.send_email_and_file(subject , body , r_day ,r_year , r_month , r_daytime  ,  check_date , sender_email , password , receiver_email2 , e_status)
                ### 財務部 shelly
                self.send_email_and_file(subject , body , r_day ,r_year , r_month , r_daytime  ,  check_date , sender_email , password , receiver_email3 , e_status)
                
            except smtplib.SMTPException as e:
                logging.info(f"< Error > send mail : {str(e)}")
            finally:
                pass
                
            ################################################################################################################
            #
            # 20240620 目前 SS2 跟豐田外倉資料對接方式不要直接對接資料伺服器 , 改成從 SS2 撈出注文單財務部跟營支部加工過再寄給豐田外倉窗口
            #
            ################################################################################################################
            ''' 
                ###  出貨日期為訂單日期自動+1天 , 遇六+2天,遇日+1天 工作天
                today = date.today()
                next_business_day = self.add_business_day(today)

                ### json format
                otsuka_data = {'WMSA20_01':otsuka_project_no , 
                               'WMSA20_02':val[0] , 
                               'WMSA20_03':next_business_day, 
                               'WMSA20_05':val[2] , 
                               'WMSA20_11':val[3] , 
                               'WMSA20_12':val[4] , 
                               'WMSA20_13':val[5] , 
                               'WMSA20_14':val[6] , 
                               'WMSA20_15':val[7] , 
                               'WMSA20_99':val[8] ,
                               'Data':[{
                                            'WMSA20_06':val[9] , 
                                            'WMSA20_07':val[10] , 
                                            'WMSA20_08':val[11] , 
                                            'WMSA20_09':val[12] , 
                                            'WMSA20_10':val[13]
                                        }] 
                               }
                
                json_val = json.dumps(otsuka_data , sort_keys=True , indent=4 , separators=(',',':') , default=self.date_converter , ensure_ascii=False)
                print(json_val)
                
                ##########################
                # 使用 豐田外倉 出貨單 API
                ##########################
                encoded_data = json_val.encode('utf-8')
                response = requests.post(export_url , data=encoded_data , headers={'Content-Type':'application/json'})
                print(response.text)

                #####################################################
                #
                # send otsuka ss2 出貨單 json format to 豐田外倉 API 
                #
                #####################################################
                try:
                    
                    check_ss2_shipment_sql = f"select o_p_no from w_shipment_form where ord_date='{val[0]}' and ord_no='{val[2]}'"
                    self.curr.execute(check_ss2_shipment_sql)
                    check_ss2_shipment_res = self.curr.fetchone()

                    if check_ss2_shipment_res is None:
                        ss2_shipment_sql  = f"insert into w_shipment_form( "
                        ss2_shipment_sql += f"c_date  , c_time , c_d_time , o_p_no  , ord_date , ship_date , ord_no    , cust_id    , cust_name , ship_address , "
                        ss2_shipment_sql += f"cnt_tel , remark , wh_id    , ord_no2 , desp     , lot_no    , expire_no , qty_amount , po , d_from ) value( "
                        ss2_shipment_sql += f"'{check_date}' , '{check_time}' , '{check_d_time}' , '{otsuka_project_no}' , '{val[0]}' , '{next_business_day}' , '{val[2]}' , '{val[3]}' , '{val[4]}' , "
                        ss2_shipment_sql += f"'{val[5]}' , '{val[6]}' , '{val[7]}' , '{val[8]}' , '{val[9]}' , '{val[10]}' , '{val[11]}', '{val[12]}' , '{val[13]}' , '{val[14]}' , 'ss2')"
                        
                        self.curr.execute(ss2_shipment_sql)
                        self.conn.commit()

                        ### 商品基本檔 更新完成
                        logging.info(f'<Message> SS2 出貨單共 {ss2_i_sum} 筆 , 更新完成.')

                    else:
                        ### 商品基本檔 更新完成
                        logging.info(f'<Message> SS2 出貨單 , 無新增資料.')

                except Exception as e:
                    logging.info(f"<Error> save to mysql - ss2 import from : {str(e)}")
                finally: 
                    pass
            '''
            
        except Exception as e:
            logging.info(f"<Error> update_factory_warehouse_data_record ss2 import : {str(e)}")
            
        finally:
            self.__ss2_disconnect_mssql__()

    ################################
    #
    # send_email_only (只寄 Email)
    #
    ################################
    def send_email_only(self , subject , sender_email , password , receiver_email , mail_content):
        try:
            
            smtpobj = smtplib.SMTP('smtp.office365.com' , 587)
            smtpobj.ehlo() 
            smtpobj.starttls()

            smtpobj.login(sender_email,password)
            
            msg = MIMEMultipart()
            msg["subject"] = subject
            msg["from"]    = sender_email
            msg["to"]      = receiver_email
            msg.attach(MIMEText(mail_content))
            smtpobj.send_message(msg=msg)

            ### send msg     
            logging.info(f'{subject} , 通知 : {receiver_email} , 成功')
            
            smtpobj.quit()

        except Exception as e:
            logging.info(f"<Error> send_email_only : {(str(e))}")    
        finally:
            pass
    
    #########################################
    #
    # send_email_and_file (寄 Email 跟附件)
    #
    #########################################
    def send_email_and_file(self , subject , body , r_day ,r_year , r_month , r_daytime  ,  check_date , sender_email , password , receiver_email , e_status):
        try:
            msg = MIMEMultipart()
            msg['From']    = formataddr(("Otsuka", sender_email))
            msg['To']      = receiver_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))

            file_path = f"/home/otsuka/otsuka_platform/excel_toyota/ss2_export_{r_day}.xlsx"
            
            mime_type, _ = mimetypes.guess_type(file_path)
            mime_type, mime_subtype = mime_type.split('/')

            with open(file_path, 'rb') as file:
                part = MIMEBase(mime_type, mime_subtype)
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{file_path.split("/")[-1]}"')
                msg.attach(part)
                
                self.__connect7_1_38__()
                try:
                    sql = f"select email from ss2_export_record where email='{receiver_email}' and ss2_form='{check_date}' and e_status='{e_status}'"
                    self.curr.execute(sql)
                    res = self.curr.fetchone()

                    if res is None:
                        
                        sql2 = f"insert into ss2_export_record(c_year , c_month , c_day , c_d_time , email,ss2_form , e_status) value('{r_year}','{r_month}','{r_day}','{r_daytime}','{receiver_email}','{check_date}','{e_status}')"
                        self.curr.execute(sql2)
                        self.conn.commit()

                        try:    
                            with smtplib.SMTP('smtp.office365.com', 587) as server:  
                                server.starttls()  
                                server.login(sender_email, password)
                                server.send_message(msg)
                            print(f"SS2 注文單 - 豐田外倉 , Email sent : {receiver_email} successfully.")
                        except Exception as e:
                            print(f"SS2 注文單 - 豐田外倉 , Failed to send email : {e}")

                except:
                    logging.info(f"<Error> check_email_status : {str(e)}")
                finally:
                    self.__disconnect7_1_38__()

        except Exception as e:
            logging.info(f"<Error> send_ss2_export_mail : {str(e)}")
        finally:
            pass

    ###################
    # date_converter
    ###################
    def add_business_day(self,d):
        # 增加一天
        next_day = d + timedelta(days=1)
        # 檢查星期幾，周六為5，周日為6
        weekday = next_day.weekday()
        
        # 如果下一天是周六，加兩天
        if weekday == 5:
            return next_day + timedelta(days=2)
        # 如果下一天是周日，加一天
        elif weekday == 6:
            return next_day + timedelta(days=1)
        # 否则，直接返回下一天
        else:
            return next_day

    ###################
    # date_converter
    ###################
    def date_converter(self , o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()    
    
    ######################
    # __connect7_1_38__ 
    ######################
    def __connect7_1_38__(self):
        
        
        ####################
        # mysql.connectot
        ####################
        try:
            self.conn = mysql.connector.connect(**parameter.otsuka_factory7_1_38)
            self.curr = self.conn.cursor()
        except mysql.connector.Error as e:
            logging.info(f"<Error> __connect7_1_38__ : {str(e)}")
            
        finally:
            pass
        
        ############
        # pymysql
        ############
        '''
        try:
            self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
            self.curr = self.conn.cursor()

        except Exception as e:
            logging.info("< ERROR > __connect__ " + str(e))

        finally:
            pass
        '''

    #######################
    # __disconnect7_1_38__
    #######################
    def __disconnect7_1_38__(self):
        
        try:
            self.conn.commit()
            self.conn.close()

        except Exception as e:
            logging.info(f"< ERROR > __disconnect7_1_38__ : {str(e)}")

        finally:
            pass
    
    ################
    # __connect__ 
    ################
    def __connect__(self):
        
        
        ####################
        # mysql.connectot
        ####################
        try:
            self.conn = mysql.connector.connect(**parameter.otsuka_factory8)
            self.curr = self.conn.cursor()
        except mysql.connector.Error as e:
            logging.info(f"<Error> __connect__ : {str(e)}")
            
        finally:
            pass
        
        ############
        # pymysql
        ############
        '''
        try:
            self.conn = pymysql.connect(host=parameter.otsuka_factory['host'],port=parameter.otsuka_factory['port'],user=parameter.otsuka_factory['user'],password=parameter.otsuka_factory['pwd'],database=parameter.otsuka_factory['db'],charset=parameter.otsuka_factory['charset'])
            self.curr = self.conn.cursor()

        except Exception as e:
            logging.info("< ERROR > __connect__ " + str(e))

        finally:
            pass
        '''

    ###################
    # __disconnect__
    ###################
    def __disconnect__(self):
        
        try:
            self.conn.commit()
            self.conn.close()

        except Exception as e:
            logging.info("< ERROR > __disconnect__ : " + str(e))

        finally:
            pass
    
    ###########################
    # __erp_connect_mssql__ 
    ###########################
    def __erp_connect_mssql__(self):
        
        try:
            ##################################
            # ODBC Driver 17 for SQL Server 
            ##################################
            erp_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={parameter.otsuka_factory5['host']};DATABASE={parameter.otsuka_factory5['db']};UID={parameter.otsuka_factory5['user']};PWD={parameter.otsuka_factory5['pwd']};TrustServerCertificate=yes;"  
            self.erp_conn_mssql = pyodbc.connect(erp_conn_str)
            self.erp_curr_mssql = self.erp_conn_mssql.cursor()

        except Exception as e:
            logging.info("< ERROR > __erp_connect_mssql__ " + str(e))

        finally:
            pass
    
    ##############################
    # __erp_disconnect_mssql__ 
    ##############################
    def __erp_disconnect_mssql__(self):
        
        try:
            self.erp_curr_mssql.close()
            self.erp_conn_mssql.close()
            
        except Exception as e:
            logging.info("< ERROR > __erp_disconnect_mssql__ " + str(e))

        finally:
            pass


    ###########################
    # __ss2_connect_mssql__ 
    ###########################
    def __ss2_connect_mssql__(self):
        
        try:
            ##################################
            # ODBC Driver 18 for SQL Server 
            ##################################
            ss2_conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={parameter.otsuka_factory6['host']};DATABASE={parameter.otsuka_factory6['db']};UID={parameter.otsuka_factory6['user']};PWD={parameter.otsuka_factory6['pwd']};TrustServerCertificate=yes;"  
            self.ss2_conn_mssql = pyodbc.connect(ss2_conn_str)
            self.ss2_curr_mssql = self.ss2_conn_mssql.cursor()

        except Exception as e:
            logging.info("< ERROR > __ss2_connect_mssql__ " + str(e))

        finally:
            pass
    
    ##############################
    # __ss2_disconnect_mssql__ 
    ##############################
    def __ss2_disconnect_mssql__(self):
        
        try:
            self.ss2_curr_mssql.close()
            self.ss2_conn_mssql.close()
            
        except Exception as e:
            logging.info("< ERROR > __ss2_disconnect_mssql__ " + str(e))

        finally:
            pass
    
    

##########################################################################################################################################################################
#
# main
#
##########################################################################################################################################################################
if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        logging.info('\n')
        logging.info('*********************************************************************************************************************************')
        logging.info('* TWOP get data program'                                         )
        logging.info('*'                                                               )
        logging.info('*         parameter :                                           ')
        logging.info('*             01).get VMware data record               : g_vm'   )
        logging.info('*             02).get Taipei card reader data record   : g_t_c_r')
        logging.info('*             02).get Factory card reader data record  : g_f_c_r')
        logging.info('*             03).get Comodo list data record          : g_c_l_r')
        logging.info('*             04).get Taipei spam server log record    : g_t_s_r')
        logging.info('*             05).get AD Server account data record    : g_a_a_r')
        logging.info('*             06).update account data record           : u_a_r'  )
        logging.info('*             07).update factory warehouse data record : u_f_w_r')
        logging.info('*             08).update otsuka product data record    : u_o_p_d_r')
        logging.info('*             09).FDA bulletin list record             : f_b_l_r')
        logging.info('*             10).modify AD pwd                        : m_a_p'  )
        logging.info('*             11).test function                        : t_f'    )
        logging.info('*             12).factory main door card reader txt    : f_m_d_c_r_t')
        logging.info('*'                                                               )
        logging.info('* Usage :'                                                       )
        logging.info('*         get_fresh_data.py f_c_r'                               )
        logging.info('*'                                                               )
        logging.info('*********************************************************************************************************************************')
    
    ################################################
    #
    # factory main door card reader txt    : f_m_d_c_r_t
    #
    ################################################
    elif sys.argv[1] == 'f_m_d_c_r_t':
        fa_card_reader_main_door_txt()

    ################################################
    #
    # get VMware data record              : g_vm
    #
    ################################################
    elif sys.argv[1] == 'g_vm':
        
        ### 抓取 vmware 資料
        get_vmware_data = get_vmware_data()
    
    ################################################
    #
    # get Taipei card reader data record : g_f_c_r
    #
    ################################################
    elif sys.argv[1] == 'g_t_c_r':
        pass

    ################################################
    #
    # get Factory card reader data record : g_f_c_r
    #
    ################################################
    elif sys.argv[1] == 'g_f_c_r':
        
        get_factory_card_reader = get_factory_card_reader_data_record()
    
    ################################################
    #
    # get Comodo list data record         : g_c_l_r
    #
    ################################################
    elif sys.argv[1] == 'g_c_l_r':
        
        ### 更新 comodo device list 資料
        check_device_list = device_list()
    
    ################################################
    #
    # get Taipei spam server log record   : g_t_s_r
    #
    ################################################
    elif sys.argv[1] == 'g_t_s_r':
        
        ### get taipei spam mail log
        get_taipei_spam_log = get_spam_maillog()

    ################################################
    #
    # get AD Server account data record   : g_a_a_r
    #
    ################################################
    elif sys.argv[1] == 'g_a_a_r':
        
        ### get taipei spam mail log
        get_taipei_spam_log = get_ad_server_account_record()

    ####################################################
    #
    # update factory warehouse data record : u_f_w_r'
    #
    ####################################################
    elif sys.argv[1] == 'u_f_w_r':
        
        ### update factory warehouse data record
        get_taipei_spam_log = update_factory_warehouse_data_record()

    ####################################################
    #
    # update otsuka product data record : u_o_p_d_r'
    #
    ####################################################
    elif sys.argv[1] == 'u_o_p_d_r':
        
        ### update otsuka product basic data
        get_taipei_spam_log = update_otsuka_product_basic_data()
    
    ################################################
    #
    # update account data record          : u_a_r'
    #
    ################################################
    elif sys.argv[1] == 'u_a_r':
        
        ### 更新 hr account list
        update_hr_account = web_cloud_dao()
        update_hr_account.erp_hr_account_list()
    
    ###################################################
    #
    # FDA bulletin list record             : f_b_l_r
    #
    ###################################################
    elif sys.argv[1] == 'f_b_l_r':
        
        ### 更新 hr account list
        #year = sys.argv[2]
        #pn   = sys.argv[3]
        dao = web_cloud_dao()
        dao.mrd_8_query_announcement_auto_search_res()
    
    ###################################################
    #
    # modify AD pwd             : m_a_p
    #
    ###################################################
    elif sys.argv[1] == 'm_a_p':
        
        ### 更新 hr account list
        account = sys.argv[2]
        #pn   = sys.argv[3]
        dao = web_cloud_dao()
        dao.modify_ad_pwd(account)
    
    ################################################
    #
    # test function                         : t_f
    #
    ################################################
    elif sys.argv[1] == 't_f':

        async def main():
            async_class = test_function('test asyncio class')
            await async_class.start_task()

        asyncio.run(main())
        
        

        
        

    











    

#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author   : JasonHung
# Date     : 20221102
# Update   : 20230919
# Function : otsuka factory import excel file

from control.config import *
from control.web_cloud_dao import *
from datetime import datetime

import pandas as pd
import pymysql , logging , pyodbc , csv , sys , os , msal , requests 

########
# log
########
log_format = "%(asctime)s %(message)s"
logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")

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
            self.conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
            self.curr = self.conn.cursor()
            
            print("------------------------------------------------------------------------------------------------------------------\n")

            ####################    
            # import csv file
            ####################
            
            ### 檢查檔案資料夾最新的檔案
            if sys.platform.startswith('win'):
                folder_path = 'C:/Jason_python/otsuka_factory_work_time_record/device_list'
                
            elif sys.platform.startswith('darwin'):
                folder_path = '/Users/jason_hungotsuka.com.tw/Documents/git/otsuka_factory_system/device_list'
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
                    csv_file = '/Users/jason_hungotsuka.com.tw/Documents/git/otsuka_factory_system/device_list/' + latest_file
                
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

####################
#
# day money oil
#
####################
class day_money_oil:

    #########
    # init
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
                    self.conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    conn_str = f"DRIVER={{SQL Server}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                
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
                    conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    self.conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    conn_str = f"DRIVER={{SQL Server}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                
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
                    conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    self.conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    conn_str = f"DRIVER={{SQL Server}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                
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
                    conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    self.conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    conn_str = f"DRIVER={{SQL Server}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                
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
                    conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    self.conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    conn_str = f"DRIVER={{SQL Server}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  

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
                    conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    self.conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    conn_str = f"DRIVER={{SQL Server}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                
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
                    conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    self.conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    conn_str = f"DRIVER={{SQL Server}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                
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
                    conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    self.conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    conn_str = f"DRIVER={{SQL Server}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                
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
                    conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    self.conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    conn_str = f"DRIVER={{SQL Server}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                
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
                    conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    self.conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
                    conn_str = f"DRIVER={{SQL Server}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                elif sys.platform.startswith('darwin'):
                    conn_str = f"DRIVER={{/opt/homebrew/Cellar/msodbcsql17/17.10.5.1/lib/libmsodbcsql.17.dylib}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                
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
                    conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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


################
#
# get outlook
#
################
class get_outlook:

    #########
    # init
    #########
    def __init__(self):
        try:
            self.get_outlook_calendar()
            
        except Exception as e:
            logging.error('< Error > get outlook init : ' + str(e))
        finally:
            pass
   
    #########################
    # get_outlook_calendar
    #########################
    def get_outlook_calendar(self):
        try:
            # 定义应用程序ID和机密
            client_id = 'your_client_id'
            client_secret = 'your_client_secret'

            # 定义Microsoft Graph API端点
            graph_api_endpoint = 'https://graph.microsoft.com/v1.0/'

            # 定义要访问的Outlook日历的URL
            calendar_url = 'https://graph.microsoft.com/v1.0/me/calendars'

            # 使用MSAL库进行身份验证
            authority = 'https://login.microsoftonline.com/your_tenant_id'
            app = PublicClientApplication(client_id, authority=authority)
            result = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])

            if 'access_token' in result:
                # 获取访问令牌
                access_token = result['access_token']

                # 构建请求标头
                headers = {
                    'Authorization': 'Bearer ' + access_token,
                    'Content-Type': 'application/json'
                }

                # 获取用户的日历列表
                response = requests.get(calendar_url, headers=headers)

                if response.status_code == 200:
                    calendars = response.json()
                    for calendar in calendars['value']:
                        print('Calendar Name:', calendar['name'])
                else:
                    print('Failed to retrieve calendars. Status code:', response.status_code)
        except Exception as e:
            logging.info(f"{str(e)}")
        finally:
            pass

#####################################################################################
#
# main
#
#####################################################################################
if __name__ == '__main__':
    
    

    
    '''
    while True:
        
        ### 更新 hr account list
        update_hr_account = web_cloud_dao()
        update_hr_account.erp_hr_account_list()
        
        ### 更新日當 油單 月報表資料
        check_day_money_oil = day_money_oil()
        
        ### 更新日當 其他 月報表資料
        check_day_money_other = day_money_other()
        
        ### 更新日當 住宿 月報表資料
        check_day_money_stay = day_money_stay()
        
        ### 更新日當 計程車 月報表資料
        check_day_money_taxi = day_money_taxi()
        
        ### 更新日當 車票 月報表資料
        check_day_money_trick = day_money_trick()
        
        ### 更新日當 過路費 月報表資料
        check_day_money_tolls = day_money_tolls()
        
        ### 更新日當 停車費 月報表資料
        check_day_money_parking_fee = day_money_parking_fee()
        
        ### 更新日當 超里程 月報表資料
        check_day_money_over_traffic = day_money_over_traffic()
        
        ### 更新日當 交通費 月報表資料
        check_day_money_traffic = day_money_traffic()
        
        ### 更新 日當 月報表資料
        check_day_money = day_money()
        
        ### 更新 comodo device list 資料
        check_device_list = device_list()

        

        time.sleep(600)
    '''

    












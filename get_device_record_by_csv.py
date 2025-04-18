#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author   : JasonHung
# Date     : 20221102
# Update   : 20231016
# Function : otsuka device record from comodo export csv file

from control.config import *
from control.web_cloud_dao import *

import pandas as pd
import pymysql , logging , pyodbc , csv , chardet , sys

########
# log
########
log_format = "%(asctime)s %(message)s"
logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")

#############
#
# get data
#
#############
class get_data:
    
    ########
    # log
    ########
    log_format = "%(asctime)s %(message)s"
    logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")
    #logging.disable(logging.INFO)

    #########
    # init
    #########
    def __init__(self , csv):
        try:

            self.comodo_device_csv(csv)
            
        except Exception as e:
            logging.info('< Error > init : ' + str(e))
        finally:
            pass

    ######################
    # comodo_device_csv
    ######################
    def comodo_device_csv(self , csv_file):
        try:
            
            csv_name = str(csv_file).split(' ')

            ####################
            #
            # insert CSV date
            #
            ####################
            now_day = str(csv_name[2])
            date    = str(now_day).split('-')
            r_year  = date[0]
            r_month = date[1]
            r_day   = date[2]
            
            csv_file_path = 'F:/otsuka/Git/otsuka_factory_work_time_record/csv/' + str(csv_file)

            '''
            #########
            #
            # date
            #
            #########
            now_day = time.strftime("%Y-%m-%d" , time.localtime()) 
            r_year  = time.strftime("%Y" , time.localtime()) 
            r_month = time.strftime("%m" , time.localtime()) 
            r_day   = time.strftime("%d" , time.localtime()) 
            '''

            '''
            ########################
            #
            # detect CSV encoding
            #
            ########################
            with open(csv_file_path , 'rb') as file:
                res = chardet.detect(file.read())

            logging.info("<msg> Detected encoding : " , res['encoding'])
            '''

            ##############################################
            #
            # comodo csv default encoding = Big5
            #
            ##############################################
            with open(csv_file_path , 'r' , encoding='utf-8') as file:
                
                csv_reader = csv.reader(file)
                sum = 0
                
                for val in csv_reader:

                    self.__connect__()
                    
                    try:
                        s_sql = f"select * from check_device_record where r_date='{now_day}' and d_name='{val[2]}'"
                        self.curr.execute(s_sql)
                        s_res = self.curr.fetchone()

                        if s_res is None:
                            i_sql  = f"insert into check_device_record" 
                            i_sql += f"("
                            i_sql += f"r_date , r_year , r_month , r_day , d_os , d_status , d_name , "
                            i_sql += f"d_client_security_status , d_patch_status , d_available_patches_count , "
                            i_sql += f"d_customer , d_group , d_last_logged_in_user , d_owner , d_last_activity , "
                            i_sql += f"d_os_name , d_os_version , d_ccs_version , d_ccc_version , d_external_ip , "
                            i_sql += f"d_internal_ip , d_ad_ldap , d_domain_workgroup , d_model , d_process , "
                            i_sql += f"d_serial_num , d_system_model , d_system_manufacturer , d_ownership_type , "
                            i_sql += f"d_registered , d_local_time_zone , d_service_pack , d_reboot_time , "
                            i_sql += f"d_reboot_reason , d_cpu_usage , d_cpu_frequency , d_ram_usage_1 , d_ram_usage_2 , "
                            i_sql += f"d_total_ram , d_network_usage , d_disk_free_GB , d_disk_used_GB , d_security_profiles , "
                            i_sql += f"d_tags , d_notes"
                            i_sql += f") "
                            i_sql += f"value("
                            i_sql += f"'{now_day}' , '{r_year}'  , '{r_month}' , '{r_day}' , '{val[0]}' , '{val[1]}' , '{val[2]}' ,"
                            i_sql += f"'{val[3]}'  , '{val[4]}'  , '{val[5]}'  , "
                            i_sql += f"'{val[6]}'  , '{val[7]}'  , '{val[8]}'  , '{val[9]}'  , '{val[10]}' , "
                            i_sql += f"'{val[11]}' , '{val[12]}' , '{val[13]}' , '{val[14]}' , '{val[15]}' , "
                            i_sql += f"'{val[16]}' , '{val[17]}' , '{val[18]}' , '{val[19]}' , '{val[20]}' , "
                            i_sql += f"'{val[21]}' , '{val[22]}' , '{val[23]}' , '{val[24]}' , "
                            i_sql += f"'{val[25]}' , '{val[26]}' , '{val[27]}' , '{val[28]}' , "
                            i_sql += f"'{val[29]}' , '{val[30]}' , '{val[31]}' , '{val[32]}' , '{val[33]}' , "
                            i_sql += f"'{val[34]}' , '{val[35]}' , '{val[36]}' , '{val[37]}' , '{val[38]}' , "
                            i_sql += f"'{val[39]}' , '{val[40]}'"
                            i_sql += ")"
                            
                            sum += 1
                            self.curr.execute(i_sql)
                            self.conn.commit()

                    except Exception as e:
                        logging.info("< Error > connect mysql : " + str(e))

                    finally:
                        self.__disconnect__()

                logging.info(f'<msg> insert new data total {sum} amount.')
                file.close()

        except Exception as e:
            logging.info('< Error > comodo_device_csv : ' + str(e))

        finally:
            pass

    ##################
    # bpm_day_money
    ##################
    def bpm_day_money(self):
        try:
                conn_str = f"DRIVER={{SQL Server}};SERVER={otsuka_factory2['host']};DATABASE={otsuka_factory2['db']};UID={otsuka_factory2['user']};PWD={otsuka_factory2['pwd']}"  
                conn_mssql = pyodbc.connect(conn_str)
                curr_mssql = conn_mssql.cursor()  
                sql = f"select ITEM14 , ITEM72 , ITEM15 , ITEM12 from ART00721676130332682_INS where ITEM26='true' and ITEM44='true' order by ITEM12 desc" 
                curr_mssql.execute(sql)
                res           = curr_mssql.fetchall()

                try:
                    conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
                    curr = conn.cursor()
                    
                    print("------------------------------------------------------------------------------------------------------------------\n")

                    for val in res:
                        
                        #logging.info(f"{val[0]} , {val[1]} , {val[2]} , {val[3]}")
                        
                        r_year  = val[3][0:4]
                        r_month = val[3][5:7]
                        r_day   = val[3][8:10]

                        s_mysql_sql = f"select * from day_money where r_date='{val[3]}' and t_money='{val[2]}' and c_name='{val[0]}'"
                        curr.execute(s_mysql_sql)
                        mysql_res = curr.fetchone()

                        if mysql_res is None:
                            mysql_sql = f"insert into day_mon ey(r_date , r_year , r_month , r_day , c_name , b_name , t_money) value('{val[3]}' , '{r_year}' ,'{r_month}' , '{r_day}' , '{val[0]}','{val[1]}','{val[2]}')"
                            curr.execute(mysql_sql)
                            conn.commit()
                            
                            logging.info(f"新日當資料 :  日期 : {val[3]} , 填表人 : {val[0]} , 金額 : {val[2]}")
                        
                    print("\n")
                    logging.info('update BPM day money is done.')
                    print("------------------------------------------------------------------------------------------------------------------")

                except Exception as e:
                    logging.info("< ERROR > connect mysql fail : " + str(e))

                finally:
                    curr.close()
                    conn.close()
                

        except Exception as e:
            logging.info("< ERROR > connect mysql fail : " + str(e))

        finally:
            curr_mssql.close()
            conn_mssql.close()

    ################
    # __connect__ 
    ################
    def __connect__(self):
        
        try:
            self.conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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


#####################################################################################
#
# main
#
#####################################################################################
if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        logging.info('*******************************************')
        logging.info('*')
        logging.info('* Usage :')
        logging.info('*         get_device_record.py <CVS-file>')
        logging.info('*')
        logging.info('*')
        logging.info('*******************************************')
    else:
        # check device record
        csv_file = sys.argv[1] + ' ' + sys.argv[2] + ' ' + sys.argv[3] + ' ' + sys.argv[4] + ' ' + sys.argv[5] 
        check_device_record = get_data(str(csv_file))











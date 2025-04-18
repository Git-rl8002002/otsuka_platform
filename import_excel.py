#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author   : JasonHung
# Date     : 20221102
# Update   : 20230919
# Function : otsuka factory import excel file

from control.config import *

import pandas as pd
import pymysql , logging

########
# log
########
log_format = "%(asctime)s %(message)s"
logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")

######################
#
# insert into mysql
#
######################
try:
    file  = '20230919工廠在職.xlsx'
    sheet = 'new sheet'
    df = pd.read_excel(file , sheet_name=sheet)

    try:
        conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
        curr = conn.cursor()

        for index , row in df.iterrows():
            
            s_sql = f"select e_name from factory_hr_a where e_name='{row['中文姓名']}'"
            curr.execute(s_sql)
            res = curr.fetchone()

            if res is None:
                
                val1 = str(row['流程組別']).strip()
                val2 = str(row['單位代碼']).strip()
                val3 = str(row['單位名稱']).strip()
                val4 = str(row['員工編號']).strip()
                val5 = str(row['中文姓名']).strip()
                val6 = str(row['登入帳號']).strip()
                val7 = str(row['性別']).strip()
                val8 = str(row['職稱中文']).strip()
                val9 = str(row['到職日期']).strip()
                val10 = str(row['電子信箱']).strip()
                
                a_sql  = f"insert into factory_hr_a"
                a_sql += f"(d_name , d_id , d_name2 , e_id , e_name , l_account , sex , j_name , j_date , email)"
                a_sql += f"value("
                a_sql += f"'{val1}' , '{val2}' , '{val3}' , '{val4}' , '{val5}' , '{val6}' , '{val7}' , '{val8}' , '{val9}' , '{val10}')"
                curr.execute(a_sql)
            else:
                logging.info(f"< ERROR > {row['流程組別'] } , {row['中文姓名']} , 已經存在資料庫 !")
            
        conn.commit()
        
        logging.info('data insert successfully.')

    except Exception as e:
        logging.info("< ERROR > connect mysql fail : " + str(e))

    finally:
        curr.close()
        conn.close()

except FileExistsError as e:
    logging.info('< ERROR > : ' + str(e))

finally:
    pass










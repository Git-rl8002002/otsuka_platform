#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author   : JasonHung
# Date     : 20221102
# Update   : 20230919
# Function : otsuka spam mail log


from control.config import *
from control.web_cloud_dao import *
from datetime import datetime , date

from ldap3 import Server, Connection, ALL, NTLM

import ssl , socket
import pandas as pd
import pymysql , logging , pyodbc , csv , sys , os 

########
# log
########
log_format = "%(asctime)s %(message)s"
logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")


#####################
#
# get spam maillog
#
#####################
class get_spam_maillog:


    #########
    # init
    #########
    def __init__(self):
        try:
            
            #####################
            # get spam maillog
            #####################
            self.get_spam_maillog_client()
            
            ###############
            # get ad
            ###############
            #self.get_ad()
            
        except Exception as e:
            logging.error('< Error > get_spam_maillog : ' + str(e))
        finally:
            pass
   
    #####################
    # get_spam_maillog
    #####################
    def get_spam_maillog_client(self):

        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(socket.AF_INET, socket.SOCK_DGRAM)
        now = str(datetime.today())[:19]
        ack_msg = now + ' hello,udp client ' 
        addr = ('192.168.1.39',514) 
        udp.sendto(ack_msg.encode('utf8'),addr)
        
#####################################################################################
#
# main
#
#####################################################################################
if __name__ == '__main__':
    
    #while True:
        
        ### 更新 hr account list
        #update_hr_account = web_cloud_dao()
        #update_hr_account.erp_hr_account_list()
        
        ### 抓取 spam maillog 
        get_spam_maillog = get_spam_maillog()

        ### 抓取 AD Server 資料

        
        

        #time.sleep(600)

    











    

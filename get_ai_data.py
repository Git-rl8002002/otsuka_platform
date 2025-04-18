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
import pymysql , logging , pyodbc , csv , sys , os , json , requests , calendar , pymssql , mysql.connector , asyncio , aiomysql

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime, timedelta

########
# log
########
log_format = "%(asctime)s %(message)s"
logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")



####################################################################################################################################
#
# class : get_ai_data
#
####################################################################################################################################
class get_ai_data:

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
        logging.info('* TWOP get ai data program'                                      )
        logging.info('*'                                                               )
        logging.info('*         parameter :                                           ')
        logging.info('*             01).get ai data record                : g_a_d_r'   )
        logging.info('*'                                                               )
        logging.info('* Usage :'                                                       )
        logging.info('*            get_ai_data.py f_c_r'                               )
        logging.info('*'                                                               )
        logging.info('*********************************************************************************************************************************')
    
    ################################################
    #
    # get ai data record              : g_vm
    #
    ################################################
    elif sys.argv[1] == 'g_vm':
        
        get_vmware_data = get_ai_data()
    
    
    
    

        
        

    











    

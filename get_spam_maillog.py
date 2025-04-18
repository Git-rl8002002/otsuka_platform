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
            
            ###############
            # get ad
            ###############
            #self.get_ad()
            
        except Exception as e:
            logging.error('< Error > get_vmware_data : ' + str(e))
        finally:
            pass
   
    ####################
    # get_ad
    ####################
    def get_ad(self):
        
        server = Server('192.168.1.10' , port=389 , get_info=ALL)
        conn   = Connection(server, user='otsukatw\Administrator', password='OtsukatW2024!', auto_bind=True , authentication='SIMPLE')
        print(server.info)

        # 查询
        res = conn.search('dc=otsukatw,dc=corp', '(objectclass=user)', attributes=['objectclass'])
        print(conn.result)  # 查询失败的原因
        print(conn.entries)  # 查询到的数据        

        '''
        try:
            with Connection(server, 'cn=admin,dc=otsukatw,dc=corp', 'admin', auto_bind=True) as conn:
                conn.start_tls()
                print('Connected to Active Directory using StartTLS')

        except Exception as e:
            print(f'Error connecting to Active Directory: {e}')

        finally:
            pass
        '''

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

            conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
            
            conn = pymysql.connect(host=otsuka_factory['host'],port=otsuka_factory['port'],user=otsuka_factory['user'],password=otsuka_factory['pwd'],database=otsuka_factory['db'],charset=otsuka_factory['charset'])
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
            self.get_spam_maillog()
            
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
    def get_spam_maillog(self):

        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.bind(('0.0.0.0',514))
        
        
        
        while True:
            rec_msg, addr = udp.recvfrom(2048)
            client_ip, client_port =addr
            msg =  client_ip + " " + rec_msg.rstrip(b'\x00').decode('utf-8','ignore')
        
            print('msg from client:', msg)    
            filename = client_ip   + '_' +  str(date.today())  + ".log"
            with open(filename,'a+',encoding = "utf-8") as f:
                f.write( msg + "\n")

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
    
    #while True:
        
        ### 更新 hr account list
        #update_hr_account = web_cloud_dao()
        #update_hr_account.erp_hr_account_list()
        
        ### 抓取 spam maillog 
        get_spam_maillog = get_spam_maillog()

        ### 抓取 AD Server 資料

        
        

        #time.sleep(600)

    











    

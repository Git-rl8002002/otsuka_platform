#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author   : JasonHung
# Date     : 20221116
# Update   : 20230307
# Version  : 1.2
# Function : 大塚製藥 get I6 sensor value

#######
#
# OS
#
#######
os = {'ubuntu_host':'192.168.111.13' , 'ubuntu_gw':'192.168.111.254' ,  
      'ubuntu_u1':'allen' , 'ubuntu_p1':'OtsukatW168!' , 
      'ubuntu_u2':'root'  , 'ubuntu_p2':'OtsukatW168!123' , 
      'win_host':'192.168.111.12' , 'win_u':'user' , 'win_p':'' ,
      'jnc_u':'admin' , 'jnc_p':'1qaz2wsx'}

##########
#
# MySQL
#
##########
db_connect = {'host':'192.168.111.13' , 'port':3306 , 
              'user':'backup' , 'pwd':'Otsukabackup#123' , 
              'user2':'root'  , 'pwd2':'password'  ,  
              'db':'tinfar_medicine' , 
              'charset':'utf8'}
###############
#
# JNC Server
#
###############
jnc_server = {'host':'192.168.111.12' , 'port':502 , 
              'i6-1':1 , 
              'i6-1_1_temp':'0x0000' , 'i6-1_2_rh':'0x0001' , 'i6-1_3_temp':'0x0002' , 'i6-1_4_rh':'0x0003' , 'i6-1_5_temp':'0x0004' ,
              'i6-1_6_temp':'0x0005' , 'i6-1_7_rh':'0x0006' , 'i6-1_8_temp':'0x0007' , 'i6-1_9_rh':'0x0008' , 'i6-1_10_temp':'0x0009' ,
              'i6-1_11_rh':'0x000A' , 'i6-1_12_temp':'0x000B' , 'i6-1_13_rh':'0x000C' , 'i6-1_14_temp':'0x000D' , 'i6-1_15_rh':'0x000E' ,
              'i6-1_16_temp':'0x000F' , 'i6-1_17_rh':'0x0010' , 'i6-1_18_temp':'0x0011' , 'i6-1_19_rh':'0x0012' , 'i6-1_20_temp':'0x0013' ,
              'i6-1_21_rh':'0x0014' ,
              'i6-2':2 , 
              'i6-2_1':'0x0000' , 'i6-2_2':'0x0001' , 'i6-2_3':'0x0002' , 'i6-2_4':'0x0003' , 'i6-2_5':'0x0004' ,
              'i6-2_6':'0x0005' , 'i6-2_7':'0x0006' , 'i6-2_8':'0x0007' , 'i6-2_9':'0x0008' , 'i6-2_10':'0x0009' ,
              'i6-2_11':'0x000A' , 'i6-2_12':'0x000B' , 'i6-2_13':'0x000C' , 'i6-2_14':'0x000D' , 'i6-2_15':'0x000E' ,
              'i6-2_16':'0x000F' , 'i6-2_17':'0x0010' , 'i6-2_18':'0x0011' , 'i6-2_19':'0x0012' , 'i6-2_20':'0x0013' ,
              'i6-2_21':'0x0014' , 'i6-2_22':'0x0015' , 'i6-2_23':'0x0016' , 'i6-2_24':'0x0017' , 'i6-2_25':'0x0018' , 'i6-2_26':'0x0019'    
              }

#################
#
# Otsuka Email
#
#################
tinfar_email = {'jason':'Jason_Hung@otsuka.com.tw'}
otsuka_email = {'bill':'bill_cheng@otsuka.com.tw' , 
                'ray':'Ray_Song@otsuka.com.tw' ,
                'allen':'allen@otsuka.com.tw' ,
                'yihsien':'Yihsien_Chen@otsuka.com.tw' ,
                'richard':'Richard_Hsieh@otsuka.com.tw' }

#############
#
# txt path
#
#############
txt_path = {'linux_txt_path':'/var/www/html/medicine/txt/' , 'linux_pdf_path':'/var/www/html/medicine/pdf/nas/backup_record.txt'}

#############
#
# NAS path 
#
#############
nas_para = {'host':'192.168.111.8' , 'user':'Jason' , 'pwd':'Otsukatw168' , 'port':22 , 
            'linux_path_s1':'/var/www/html/medicine/pdf/nas/S1/' , 
            'nas_path_s1':'Temperature/WHFP-1-25' , 
            'linux_path_s2':'/var/www/html/medicine/pdf/nas/S2/' , 
            'nas_path_s2':'Temperature/WHFP-1-30' ,
            'linux_path_s3':'/var/www/html/medicine/pdf/nas/S3/' , 
            'nas_path_s3':'Temperature/WHR-1' , 
            'linux_path_s4':'/var/www/html/medicine/pdf/nas/S4/' , 
            'nas_path_s4':'Temperature/WHFP-3-30-C' , 
            'linux_path_s5':'/var/www/html/medicine/pdf/nas/S5/' , 
            'nas_path_s5':'Temperature/WHFP-3-30-B' , 
            'linux_path_s6':'/var/www/html/medicine/pdf/nas/S6/' , 
            'nas_path_s6':'Temperature/WHFP-3-25' , 
            'linux_path_s7':'/var/www/html/medicine/pdf/nas/S7/' , 
            'nas_path_s7':'Temperature/WHFP-3-30-A' , 
            'linux_path_s8':'/var/www/html/medicine/pdf/nas/S8/' , 
            'nas_path_s8':'Temperature/WHFP-2' , 
            'linux_path_s9':'/var/www/html/medicine/pdf/nas/S9/' , 
            'nas_path_s9':'Temperature/WHR-2' , 
            'linux_path_s10':'/var/www/html/medicine/pdf/nas/S10/' , 
            'nas_path_s10':'Temperature/WHM' , 
            'linux_path_s11-1':'/var/www/html/medicine/pdf/nas/S11-1/' , 
            'nas_path_s11-1':'Temperature/SR-1' , 
            'linux_path_s11-2':'/var/www/html/medicine/pdf/nas/S11-2/' , 
            'nas_path_s11-2':'Temperature/SR-1-CS' , 
            'linux_path_s12':'/var/www/html/medicine/pdf/nas/S12/' , 
            'nas_path_s12':'Temperature/SR-2' , 
            'linux_path_s13':'/var/www/html/medicine/pdf/nas/S13/' , 
            'nas_path_s13':'Temperature/SR-2-CS' , 
            'linux_path_s14':'/var/www/html/medicine/pdf/nas/S14/' , 
            'nas_path_s14':'Temperature/WHRE' , 
            'linux_path_s15-1':'/var/www/html/medicine/pdf/nas/S15-1/' , 
            'nas_path_s15-1':'Temperature/SB-1' , 
            'linux_path_s15-2':'/var/www/html/medicine/pdf/nas/S15-2/' , 
            'nas_path_s15-2':'Temperature/SB-2' , 
            'linux_path_s15-3':'/var/www/html/medicine/pdf/nas/S15-3/' , 
            'nas_path_s15-3':'Temperature/SB-3' , 
            'linux_path_s15-4':'/var/www/html/medicine/pdf/nas/S15-4/' , 
            'nas_path_s15-4':'Temperature/SB-4' , 
            'linux_path_s15-5':'/var/www/html/medicine/pdf/nas/S15-5/' , 
            'nas_path_s15-5':'Temperature/SB-5' , 
            'linux_path_s15-6':'/var/www/html/medicine/pdf/nas/S15-6/' , 
            'nas_path_s15-6':'Temperature/SB-6' , 
            'linux_path_s16':'/var/www/html/medicine/pdf/nas/S16/' , 
            'nas_path_s16':'Temperature/WIP' ,
            'linux_path_s17':'/var/www/html/medicine/pdf/nas/S17/' , 
            'nas_path_s17':'Temperature/WHFP-2-CS' , 
            'linux_path_s18':'/var/www/html/medicine/pdf/nas/S18/' , 
            'nas_path_s18':'Temperature/WHFP-3-CS',
            'linux_path_s19':'/var/www/html/medicine/pdf/nas/S19/' , 
            'nas_path_s19':'Temperature/unknow'}

#############
#
# PDF path
#
#############
pdf_path = {'mac_pdf_month_path':'/Users/user/eclipse-workspace/tinfar/medicine/pdf/month/' , 
            'linux_pdf_month_path':'/var/www/html/medicine/pdf/month/' , 
            'windows_pdf_month_path':'d:/medicine\pdf/month/' , 
            'mac_pdf_day_path':'/Users/user/eclipse-workspace/tinfar/medicine/pdf/day/' , 
            'linux_pdf_day_path':'/var/www/html/medicine/pdf/day/' ,
            'windows_pdf_day_path':'d:/medicine/pdf/day/'}

##########
#
# I6 -2
#
##########
### I6-2 by modbusTCP - 大塚製藥
m_i6_tcp_connect_2 = {'ip':'192.168.113.100','port':502}
m_i6_tcp_param_2   = {'kind':'I6-2','protocol':'modbusTCP','position':'I6-2','position_n':'倉庫管理室'}
m_i6_tcp_sensor_2  = {'s17-temp':'0x0000',
                      's18-temp':'0x0001',
                      's1-temp':'0x0002','s1-rh':'0x0003',
                      's2-temp':'0x0004','s2-rh':'0x0005',
                      's3-temp':'0x0006','s3-rh':'0x0007',
                      's4-temp':'0x0008','s4-rh':'0x0009',
                      's5-temp':'0x000A','s5-rh':'0x000B',
                      's6-temp':'0x000C','s6-rh':'0x000D',
                      's7-temp':'0x000E','s7-rh':'0x000F',
                      's8-temp':'0x0010','s8-rh':'0x0011',
                      's9-temp':'0x0012','s9-rh':'0x0013',
                      's10-temp':'0x0014','s10-rh':'0x0015',
                      's14-temp':'0x0016','s14-rh':'0x0017',
                      's19-temp':'0x0018','s19-rh':'0x0019'}

### S-1 by modbusTCP from I6-2 - 大塚製藥
s_1_tcp_connect = {'ip':'192.168.113.100','port':502}
s_1_tcp_param   = {'kind':'S-1','protocol':'modbusTCP','position':'WHFP-1-25°C','position_n':'製品倉庫(一)25°C'}
s_1_tcp_sensor  = {'temp':'0x0002','rh':'0x0003'}

### S-2 by modbusTCP from I6-2 - 大塚製藥
s_2_tcp_connect = {'ip':'192.168.113.100','port':502}
s_2_tcp_param   = {'kind':'S-2','protocol':'modbusTCP','position':'WHFP-1-30°C','position_n':'製品倉庫(一)30°C'}
s_2_tcp_sensor  = {'temp':'0x0004','rh':'0x0005'}

### S-3 by modbusTCP from I6-2 - 大塚製藥
s_3_tcp_connect = {'ip':'192.168.113.100','port':502}
s_3_tcp_param   = {'kind':'S-3','protocol':'modbusTCP','position':'WHR-1','position_n':'原料庫(一)'}
s_3_tcp_sensor  = {'temp':'0x0006','rh':'0x0007'}

### S-4 by modbusTCP from I6-2 - 大塚製藥
s_4_tcp_connect = {'ip':'192.168.113.100','port':502}
s_4_tcp_param   = {'kind':'S-4','protocol':'modbusTCP','position':'WHFP-3-30°C-C','position_n':'製品倉庫(三)30° C'}
s_4_tcp_sensor  = {'temp':'0x0008','rh':'0x0009'}

### S-5 by modbusTCP from I6-2 - 大塚製藥
s_5_tcp_connect = {'ip':'192.168.113.100','port':502}
s_5_tcp_param   = {'kind':'S-5','protocol':'modbusTCP','position':'WHFP-3-30°C-B','position_n':'製品倉庫(三)30° B'}
s_5_tcp_sensor  = {'temp':'0x000A','rh':'0x000B'}

### S-6 by modbusTCP from I6-2 - 大塚製藥
s_6_tcp_connect = {'ip':'192.168.113.100','port':502}
s_6_tcp_param   = {'kind':'S-6','protocol':'modbusTCP','position':'WHFP-3-25°C','position_n':'製品倉庫(三)25° C'}
s_6_tcp_sensor  = {'temp':'0x000C','rh':'0x000D'}

### S-7 by modbusTCP from I6-2 - 大塚製藥
s_7_tcp_connect = {'ip':'192.168.113.100','port':502}
s_7_tcp_param   = {'kind':'S-7','protocol':'modbusTCP','position':'WHFP-3-30°C-A','position_n':'製品倉庫(三)30° A'}
s_7_tcp_sensor  = {'temp':'0x000E','rh':'0x000F'}

### S-8 by modbusTCP from I6-2 - 大塚製藥
s_8_tcp_connect = {'ip':'192.168.113.100','port':502}
s_8_tcp_param   = {'kind':'S-8','protocol':'modbusTCP','position':'WHFP-2','position_n':'製品倉庫(二)'}
s_8_tcp_sensor  = {'temp':'0x0010','rh':'0x0011','pw':'0x0002'}

### S-9 by modbusTCP from I6-2 - 大塚製藥
s_9_tcp_connect = {'ip':'192.168.113.100','port':502}
s_9_tcp_param   = {'kind':'S-9','protocol':'modbusTCP','position':'WHR-2','position_n':'原料倉(二)'}
s_9_tcp_sensor  = {'temp':'0x0012','rh':'0x0013','pw':'0x0002'}

### S-10 by modbusTCP from I6-2 - 大塚製藥
s_10_tcp_connect = {'ip':'192.168.113.100','port':502}
s_10_tcp_param   = {'kind':'S-10','protocol':'modbusTCP','position':'WHM','position_n':'物料倉庫'}
s_10_tcp_sensor  = {'temp':'0x0014','rh':'0x0015','pw':'0x0002'}

### S-14 by modbusTCP from I6-2 - 大塚製藥
s_14_tcp_connect = {'ip':'192.168.113.100','port':502}
s_14_tcp_param   = {'kind':'S-14','protocol':'modbusTCP','position':'WHRE','position_n':'退貨品倉庫'}
s_14_tcp_sensor  = {'temp':'0x0016','rh':'0x0017','pw':'0x0002'}

### S-17 by modbusTCP from I6-2 - 大塚製藥
s_17_tcp_connect = {'ip':'192.168.113.68','port':502}
s_17_tcp_param   = {'kind':'S-17','protocol':'modbusTCP','position':'WHFP-2-CS','position_n':'製品三倉-溫度'}
s_17_tcp_sensor  = {'temp':'0x0000','rh':'0x0001','pw':'0x0002'}

### S-18 by modbusTCP from I6-2 - 大塚製藥
s_18_tcp_connect = {'ip':'192.168.114.68','port':502}
s_18_tcp_param   = {'kind':'S-18','protocol':'modbusTCP','position':'WHFP-3-CS','position_n':'製品二倉-溫度'}
s_18_tcp_sensor  = {'temp':'0x0000','rh':'0x0001','pw':'0x0002'}

### S-19 by modbusTCP from I6-2 - 大塚製藥 (20231026 new add)
s_19_tcp_connect = {'ip':'192.168.113.100','port':502}
s_19_tcp_param   = {'kind':'S-19','protocol':'modbusTCP','position':'unknow','position_n':'安定性試驗室'}
s_19_tcp_sensor  = {'temp':'0x0018','rh':'0x0019'}

###########
#
# I6 - 1
#
###########
### I6-1 by modbusTCP - 大塚製藥
m_i6_tcp_connect = {'ip':'192.168.111.78','port':502}
m_i6_tcp_param   = {'kind':'I6-1','protocol':'modbusTCP','position':'I6-1','position_n':'警衛室'}
m_i6_tcp_sensor  = {'s16-temp':'0x0000','s16-rh':'0x0001',
                    's11-1-temp':'0x0002','s11-1-rh':'0x0003',
                    's11-2-temp':'0x0004',
                    's12-temp':'0x0005','s12-rh':'0x0006',
                    's13-temp':'0x0007','s13-rh':'0x0008',
                    's15-1-temp':'0x0009','s15-1-rh':'0x000A',
                    's15-2-temp':'0x000B','s15-2-rh':'0x000C',
                    's15-3-temp':'0x000D','s15-3-rh':'0x000E',
                    's15-4-temp':'0x0010','s15-4-rh':'0x0011',
                    's15-5-temp':'0x0012','s15-5-rh':'0x0013',
                    's15-6-temp':'0x0014','s15-6-rh':'0x0015'}

### S-11-1 by modbusTCP from I6-2 - 大塚製藥
s_11_tcp_connect_1 = {'ip':'192.168.111.78','port':502}
s_11_tcp_param_1   = {'kind':'S-11-1','protocol':'modbusTCP','position':'SR-1','position_n':'樣品室-1(25°C)'}
s_11_tcp_sensor_1  = {'temp':'0x0002','rh':'0x0003'}

### S-11-2 by modbusTCP from I6-2 - 大塚製藥
s_11_tcp_connect_2 = {'ip':'192.168.111.78','port':502}
s_11_tcp_param_2   = {'kind':'S-11-2','protocol':'modbusTCP','position':'SR-1-CS','position_n':'樣品室-1(冰箱)'}
s_11_tcp_sensor_2  = {'temp':'0x0004'}

### S-12 by modbusTCP from I6-2 - 大塚製藥
s_12_tcp_connect = {'ip':'192.168.111.78','port':502}
s_12_tcp_param   = {'kind':'S-12','protocol':'modbusTCP','position':'SR-2','position_n':'樣品室-2(20°C)'}
s_12_tcp_sensor  = {'temp':'0x0005','rh':'0x0006','pw':'0x0002'}

### S-13 by modbusTCP from I6-2 - 大塚製藥
s_13_tcp_connect = {'ip':'192.168.111.78','port':502}
s_13_tcp_param   = {'kind':'S-13','protocol':'modbusTCP','position':'SR-2-CS','position_n':'樣品室-3(30°C)'}
s_13_tcp_sensor  = {'temp':'0x0007','rh':'0x0008','pw':'0x0002'}

### S-15-1 by modbusTCP from I6-2 - 大塚製藥
s_15_tcp_connect_1 = {'ip':'192.168.111.78','port':502}
s_15_tcp_param_1   = {'kind':'S-15-1','protocol':'modbusTCP','position':'SB-1','position_n':'安全性實驗箱-1'}
s_15_tcp_sensor_1  = {'temp1':'0x0009','rh1':'0x000A'}

### S-15-2 by modbusTCP from I6-2 - 大塚製藥
s_15_tcp_connect_2 = {'ip':'192.168.111.78','port':502}
s_15_tcp_param_2   = {'kind':'S-15-2','protocol':'modbusTCP','position':'SB-2','position_n':'安全性實驗箱-2'}
s_15_tcp_sensor_2  = {'temp2':'0x000B','rh2':'0x000C'}                

### S-15-3 by modbusTCP from I6-2 - 大塚製藥
s_15_tcp_connect_3 = {'ip':'192.168.111.78','port':502}
s_15_tcp_param_3   = {'kind':'S-15-3','protocol':'modbusTCP','position':'SB-3','position_n':'安全性實驗箱-3'}
s_15_tcp_sensor_3  = {'temp3':'0x000D','rh3':'0x000E'}     

### S-15-4 by modbusTCP from I6-2 - 大塚製藥
s_15_tcp_connect_4 = {'ip':'192.168.111.78','port':502}
s_15_tcp_param_4   = {'kind':'S-15-4','protocol':'modbusTCP','position':'SB-4','position_n':'安全性實驗箱-4'}
s_15_tcp_sensor_4  = {'temp4':'0x0010','rh4':'0x0011'} 

### S-15-5 by modbusTCP from I6-2 - 大塚製藥
s_15_tcp_connect_5 = {'ip':'192.168.111.78','port':502}
s_15_tcp_param_5   = {'kind':'S-15-5','protocol':'modbusTCP','position':'SB-5','position_n':'安全性實驗箱-5'}
s_15_tcp_sensor_5  = {'temp5':'0x0012','rh5':'0x0013'}          

### S-15-6 by modbusTCP from I6-2 - 大塚製藥
s_15_tcp_connect_6 = {'ip':'192.168.111.78','port':502}
s_15_tcp_param_6   = {'kind':'S-15-6','protocol':'modbusTCP','position':'SB-6','position_n':'安全性實驗箱-6'}
s_15_tcp_sensor_6  = {'temp6':'0x0014','rh6':'0x0015'} 

### S-16 by modbusTCP from I6-2 - 大塚製藥
s_16_tcp_connect = {'ip':'192.168.111.78','port':502}
s_16_tcp_param   = {'kind':'S-16','protocol':'modbusTCP','position':'WIP','position_n':'中間品室'}
s_16_tcp_sensor  = {'temp':'0x0000','rh':'0x0001','pw':'0x0002'}                





#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author   : JasonHung
# Date     : 20221102
# Update   : 20240526 , 20240930
# Function : otsuka factory work time record

class parameter:

  #############
  #
  # variable
  #
  #############
  parm = {'title':'台灣大塚製藥'}

  #######
  #
  # HR
  #
  #######
  hr_data = {'hr_file_1':'hr/員工明細資料.xlsx' , 
             'hr_file_2':'hr/人事異動單_201701.xlsx' ,
             'hr_file_3':'hr/2023_2024訓練記錄.xlsx' 
             }

  ##############
  #
  # AD Server
  #
  ##############
  ad_server = {'host':'192.168.1.10:389' , 'domain':'otsukatw'}

  ########
  #
  # nas
  #
  ########
  nas_para = {'host':'192.168.111.8' , 'user':'Jason' , 'pwd':'Otsukatw168' , 'port':22 , 
              'linux_path_card_reader':'/home/otsuka/otsuka_project_1/' , 
              'nas_path_card_reader':'Temperature/card_reader'
              } 

  ##############################################################################################################################
  #
  # MRD 醫藥法規開發處
  #
  # mrd_8 : 
  #           食品添加物使用範圍及限量暨規格標準 -> t=17 代表第 17 項  , 不帶 t 參數  , 就搜尋全部 , 
  #           食品添加物許可證資料查詢 -> 1&ct=1&cn=5&en=2&cp=6&ph1=3&ph2=7&ph3=4&k=8 , 不帶參數就是就搜尋全部    
  #
  ##############################################################################################################################
  mrd_8 = { '食品添加物使用範圍及限量暨規格標準':'https://consumer.fda.gov.tw/Law/foodadditiveslist.aspx?nodeID=521' ,        
            '食品添加物許可證資料查詢':'https://consumer.fda.gov.tw/Food/FoodAdd.aspx?nodeID=161',
            '食品原料整合查詢平臺':'https://consumer.fda.gov.tw/Food/Material.aspx?nodeID=160',
            '衛生福利部審核通過之健康食品資料查詢':'https://consumer.fda.gov.tw/Food/InfoHealthFood.aspx?nodeID=162',
            '特定疾病配方食品':'https://consumer.fda.gov.tw/Food/SpecialFood.aspx?nodeID=163',
            '輸入膠囊錠狀食品核備查詢':'https://consumer.fda.gov.tw/Food/CapsuleAuditQuery.aspx?nodeID=165',
            '國產維生素類錠狀膠囊狀食品查驗登記證資料查詢':'https://consumer.fda.gov.tw/Food/DomesticFormulationsQuery.aspx?nodeID=166',
            '衛生福利部審核通過之基因改造食品原料之查詢':'https://consumer.fda.gov.tw/Food/GmoInfo.aspx?nodeID=167',
            '嬰兒與較大嬰兒配方食品許可資料查詢':'https://consumer.fda.gov.tw/Food/BabyFood.aspx?nodeID=1074',
            '化粧品禁限用成分管理規定':'https://consumer.fda.gov.tw/LAW/Cosmetic1.aspx?nodeID=1068',
            '西藥許可證查詢':'https://lmspiq.fda.gov.tw/web/DRPIQ/DRPIQLicSearch',
            '商標檢索系統':'https://cloud.tipo.gov.tw/S282/OS0/OS0101.jsp',
            '衛生福利部食品藥物管理署公告':'https://www.fda.gov.tw/TC/news.aspx?cid=3',
            '台灣藥物法規資訊網':'https://regulation.cde.org.tw/index.html',
            '整合查詢服務':'https://consumer.fda.gov.tw/Pages/List.aspx?nodeID=6'
          }

  ###########################
  #
  # factory monitor device
  #
  ###########################
  m_device = {'S-1'   :'製品倉庫(一)25°C' , 'S-2'   :'製品倉庫(一)30°C' ,
              'S-3'   :'原料庫(一)'       , 'S-4'   :'製品倉庫(三)30° C' ,
              'S-5'   :'原料庫(三)30° B'  , 'S-6'   :'製品倉庫(三)25° C' ,
              'S-7'   :'原料庫(三)30° A'  , 'S-8'   :'製品倉庫(二)' ,
              'S-9'   :'原料庫(二)'       , 'S-10'  :'物料倉庫' ,
              'S-11-1':'樣品室-1(25°C)'   , 'S-11-2':'樣品室-1(冰箱)' ,
              'S-12'  :'樣品室-2(20°C)'   , 'S-13'  :'樣品室-3(30°C)' ,
              'S-14'  :'退貨品倉庫'       , 
              'S-15-1':'安全性實驗箱-1'   , 'S-15-2':'安全性實驗箱-2' ,
              'S-15-3':'安全性實驗箱-3'   , 'S-15-4':'安全性實驗箱-4' ,
              'S-15-5':'安全性實驗箱-5'   , 'S-15-6':'安全性實驗箱-6' ,
              'S-16'  :'中間品室'         , 'S-17'  :'製品三倉-溫度' ,
              'S-18'  :'製品二倉-溫度'    , 'S-19'  :'安定性試驗室'
            }

  ############################################################################
  #
  # factory : otsuka_factory
  # taipei  : otsuka_taipei_office
  #
  # HRM <---> BPM table 
  #   IP  : 192.168.1.45
  #   DB  : Agentflow
  #   tb1 : T_HR_Department - 人事組織連動資料表
  #   tb2 : T_HR_Employee   - 人事組織連動資料表
  #
  ############################################################################
  otsuka_factory       = {'host':'192.168.1.93'    , 'port':3306 , 'user':'otsuka'     , 'pwd':'OtsukatW168!'         , 'db':'otsuka_factory'          , 'charset':'utf8'}
  otsuka_factory2      = {'host':'192.168.1.45'    , 'port':1433 , 'user':'HR2BPM'     , 'pwd':'Otsukatw14001297!'    , 'db':'Agentflow'               , 'charset':'utf8'} 
  otsuka_factory3      = {'host':'192.168.1.31'    , 'port':1433 , 'user':'Jason_Hung' , 'pwd':'e03vu,4timqotu!'      , 'db':'SHRM'                    , 'charset':'utf8'}
  otsuka_factory4      = {'host':'192.168.111.13'  , 'port':3306 , 'user':'backup'     , 'pwd':'Otsukabackup#123'     , 'db':'tinfar_medicine'         , 'charset':'utf8'}
  otsuka_factory5      = {'host':'192.168.1.7'     , 'port':1433 , 'user':'dbadmin'    , 'pwd':'ej/ck4vupvu3!'        , 'db':'OtsukaDB'                , 'charset':'utf8'}
  otsuka_factory6      = {'host':'192.168.1.31'    , 'port':1433 , 'user':'sa'         , 'pwd':'e03vu,4timqotu!'      , 'db':'SALES2'                  , 'charset':'utf8'}
  otsuka_factory7      = {'host':'192.168.1.93'    , 'port':3306 , 'user':'otsuka'     , 'pwd':'OtsukatW168!'         , 'db':'otsuka_taipei_office'    , 'charset':'utf8'}
  otsuka_factory8      = {'host':'192.168.1.93'    , 'port':3306 , 'user':'otsuka'     , 'password':'OtsukatW168!'    , 'db':'otsuka_factory'          , 'charset':'utf8'}
  otsuka_factory9_wms  = {'host':'192.168.1.61'    , 'port':1433 , 'user':'sa'         , 'password':'PAssw0rd'        , 'db':'otsuka_account'          , 'charset':'utf8'}
  otsuka_factory_1_38  = {'host':'192.168.1.38'    , 'port':3306 , 'user':'otsuka'     , 'password':'otsuka#123'      , 'db':'otsuka_factory'          , 'charset':'utf8'}
  otsuka_taipei_1_38   = {'host':'192.168.1.38'    , 'port':3306 , 'user':'root'       , 'password':'Otsuka#14001297!', 'db':'otsuka_taipei_comodolog' , 'charset':'utf8'}
  otsuka_factory7_1_38 = {'host':'192.168.1.93'    , 'port':3306 , 'user':'otsuka'     , 'password':'OtsukatW168!'    , 'db':'otsuka_taipei_office'    , 'charset':'utf8'}
  phpmyadmin_login     = {'host':'192.168.1.93'    , 'port':3306 , 'user':'root'       , 'password':'OtsukatW168!'    , 'db':'otsuka_taipei_office'    , 'charset':'utf8'}
  otsuka_wms_1_61      = {'host':'192.168.1.61'    , 'port':3306 , 'user':'sa'         , 'password':'PAssw0rd'        , 'db':'otsuka_form'             , 'charset':'utf8'}
  otsuka_wms_pro_1_61  = {'host':'192.168.1.61'    , 'port':3306 , 'user':'sa'         , 'password':'PAssw0rd'        , 'db':'otsuka_product'          , 'charset':'utf8'}

  #############
  #
  # txt path
  #
  #############
  txt_path = {'linux_txt_path':'/var/www/html/medicine/txt/' , 'linux_pdf_path':'/var/www/html/medicine/pdf/nas/backup_record.txt'}

  ################
  #
  # line notify 
  #
  ################
  token = {'rl8002002':'etECmdmXAitOol7GnYBbrccF8m9Fx7IrZ8v7j45cYuN'}

  ####################################################################################################
  #
  #  ERP schema
  # 
  #  IP : 192.168.1.7:1433
  #  DB : OtsukaDB
  #
  ####################################################################################################
  erp_db = {"固資查詢表":"SELECT A.MB001 AS '固資編號', A.MB002 AS '固資名稱', A.MB016 AS '取得日期',B.MC003 AS '工號', D.MV002 AS '保管人姓名', B.MC002 AS '部門代號',C.ME002 AS '部門名稱', B.MC006 AS '放置地點'FROM ASTMB A, ASTMC B, CMSME C, CMSMV D WHERE A.MB001=B.MC001 AND C.ME001=B.MC002 AND D.MV001=B.MC003AND MB001='46N0696'" ,
            "固定資產表":"SELECT C.MC002 AS '部門代號', E.ME002 AS '部門名稱', B.MB006 AS '資產類別' , A.MA002 AS '類別名稱', B.MB001 AS '資產編號', B.MB002 AS '資產名稱' , B.MB003 AS '資產規格', C.MC003 AS '保管人代號', V.MV002 AS '保管人名稱' , C.MC004 AS '數量' FROM   ASTMB B, ASTMC C, CMSME E, CMSMV V, ASTMA A WHERE  B.MB001=C.MC001 AND E.ME001=C.MC002 AND B.MB006=A.MA001 AND C.MC003=V.MV001 AND B.MB071='20240621'"
            }

  ####################################################################################################
  #
  #  BPM schema
  # 
  #  費用申請單
  #  IP : 192.168.1.45:1433
  #  DB : OtsukaDB
  #
  ####################################################################################################
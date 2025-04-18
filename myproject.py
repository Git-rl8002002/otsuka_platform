#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author   : JasonHung
# Date     : 20221102
# Update   : 20230720 , 20240930
# Function : otsuka factory work time record

from argparse import Namespace
from dataclasses import dataclass
from distutils.log import debug
from email import charset
from hashlib import md5
import hashlib , time , logging , random  , csv , os , mimetypes , pymysql , asyncio , aiomysql , aioodbc , json
from tabnanny import check
from flask import Flask,render_template,request,session,url_for,redirect , Response , send_file , render_template_string , make_response , jsonify
from flask_cors import CORS
from flask_socketio import SocketIO , emit 
from flask_bootstrap import Bootstrap
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO
import numpy as np
from matplotlib import font_manager as fm


### matplotlib 
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

### config
from control.config.config import parameter
from control.web_cloud_dao import web_cloud_dao , async_web_cloud_dao

db       = web_cloud_dao()
async_db = async_web_cloud_dao()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
CORS(app)
bootstrap = Bootstrap(app)

########
# log
########
log_format = "%(asctime)s %(message)s"
logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")

##############
# variables
##############
title  = parameter.parm['title']


##############################
# /test3
##############################
@app.route("/test3")
async def test3():

    
    ##########
    # mysql
    ##########
    try:
        pool2 = await async_db.__async_connect_mysql__()
        if not pool2:
            return "Failed to connect to the mysql", 500
        mysql_res = await async_db.async_mysql_query(pool2 , "select * from w_basic_product_form ")

    finally:
        if pool2:
            if asyncio.iscoroutinefunction(pool2.close):
                await pool2.close()
            else:
                pool2.close()
    
    
    ##########
    # mssql
    ##########
    try:
        pool = await async_db.__async_connect_mssql__()
        if not pool:
            return "Failed to connect to the mssql", 500
        
        mssql_res = await async_db.async_mssql_query(pool , 'select DepartmentID , count(*) from T_HR_Department group by DepartmentID')

    finally:
        if pool:
            # Ensure the close method matches its proper usage
            if asyncio.iscoroutinefunction(pool.close):
                await pool.close()
            else:
                pool.close() 
    
    return render_template('test3.html' , name='test page')

##############################
# /test2
##############################
@app.route("/test2")
def test2():
    return render_template('test3.html')    

##############################
# /test
##############################
@app.route("/test")
def test():
    #################
    # main content 
    #################
    
    ######################################
    #
    # Generate a simple Matplotlib plot
    #
    ######################################
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot([1, 2, 3, 4, 5], [2, 4, 6, 8, 10] , label='Line')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    FigureCanvas(fig).print_png(img)
    img.seek(0)

    # Convert the image to base64 for embedding in HTML
    img_data = base64.b64encode(img.getvalue()).decode('utf-8')

    ######################################
    #
    # Generate a simple Matplotlib plot
    #
    ######################################
    fig2 = Figure()
    axis2 = fig2.add_subplot(1, 1, 1)
    axis2.plot([1, 2, 3, 4, 5], [2, 4, 6, 8, 10] , label='Points' , color='red' , marker='o')

    # Save the plot to a BytesIO object
    img2 = io.BytesIO()
    FigureCanvas(fig2).print_png(img2)
    img.seek(0)

    # Convert the image to base64 for embedding in HTML
    img_data2 = base64.b64encode(img2.getvalue()).decode('utf-8')

    ######################################
    #
    # Generate a simple Matplotlib plot
    #
    ######################################
    fig3 = Figure()
    axis3 = fig3.add_subplot(1, 1, 1)

    fig = plt.figure(figsize=(6,6))
    ax = plt.subplot(projection='3d')   # 設定為 3D 圖表
    x = range(5)
    y = [1,5,8,4,6]
    ax.plot(x,y)

    # Save the plot to a BytesIO object
    img3 = io.BytesIO()
    FigureCanvas(fig3).print_png(img3)
    img3.seek(0)

    # Convert the image to base64 for embedding in HTML
    img_data3 = base64.b64encode(img2.getvalue()).decode('utf-8')

    return render_template('test.html', img_data=img_data , img_data2=img_data2)

##############################
# /update_hr_account
##############################
@app.route("/update_hr_account")
def update_hr_account():
    #################
    # main content 
    #################
    res = db.erp_hr_account_list()

    return render_template('update_hr_account.html' , title=title , hr_account=res)    

##############################
# /reload_menu_account_list
##############################
@app.route("/reload_menu_account_list", methods=['POST','GET'])
def reload_menu_account_list():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '權限管理 -  載入帳號清單'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station      = db.factory_work_station()
            factory_work_account_list = db.factory_work_account_list()

            return render_template('ajax/menu_account_management.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , factory_work_account_list=factory_work_account_list)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

####################################
# /show_sensor_position_list
####################################
@app.route("/show_sensor_position_list", methods=['POST','GET'])
def show_sensor_position_list():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '工廠溫溼度器紀錄 > 溫溼度感測器清單'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            S1 = db.sensor_position_detail('S-1')
            S2 = db.sensor_position_detail('S-2')
            S3 = db.sensor_position_detail('S-3')
            S4 = db.sensor_position_detail('S-4')
            S5 = db.sensor_position_detail('S-5')
            S6 = db.sensor_position_detail('S-6')
            S7 = db.sensor_position_detail('S-7')
            S8 = db.sensor_position_detail('S-8')
            S9 = db.sensor_position_detail('S-9')
            S10 = db.sensor_position_detail('S-10')
            S11_1 = db.sensor_position_detail('S-11-1')
            S11_2 = db.sensor_position_detail('S-11-2')
            S12 = db.sensor_position_detail('S-12')
            S13 = db.sensor_position_detail('S-13')
            S14 = db.sensor_position_detail('S-14')
            S15_1 = db.sensor_position_detail('S-15-1')
            S15_2 = db.sensor_position_detail('S-15-2')
            S15_3 = db.sensor_position_detail('S-15-3')
            S15_4 = db.sensor_position_detail('S-15-4')
            S15_5 = db.sensor_position_detail('S-15-5')
            S15_6 = db.sensor_position_detail('S-15-6')
            S16 = db.sensor_position_detail('S-16')
            S17 = db.sensor_position_detail('S-17')
            S18 = db.sensor_position_detail('S-18')
            S19 = db.sensor_position_detail('S-19')
                    
            return render_template('ajax/detail_sensor_position_record.html' , user=user , title=title , dep_id=dep_id , S1=S1 , S2=S2 , S3=S3 , S4=S4 , S5=S5 , S6=S6 , S7=S7 , S8=S8 , S9=S9 , S10=S10 , S11_1=S11_1 , S12=S12 , S13=S13 , S14=S14 , S15_1=S15_1 , S15_2=S15_2 , S15_3=S15_3 , S15_4=S15_4 , S15_5=S15_5 , S15_6=S15_6 , S16=S16 , S17=S17 , S18=S18 , S19=S19)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

####################################
# /show_computer_serial_name_list
####################################
@app.route("/show_computer_serial_name_list", methods=['POST','GET'])
def show_computer_serial_name_list():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '使用紀錄 > 電腦系號清單'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            u_detail = db.computer_s_number_detail()
                    
            return render_template('ajax/detail_computer_serial_record.html' , user=user , title=title , dep_id=dep_id , u_detail=u_detail)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

######################################
# /search_show_computer_user_detail
######################################
@app.route("/search_show_computer_user_detail", methods=['POST','GET'])
def search_show_computer_user_detail():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '使用紀錄 > 搜尋電腦使用詳細紀錄'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                s_number = request.form['s_number']
                u_detail = db.search_show_computer_user_detail(s_number)
                    
                return render_template('ajax/search_detail_computer_user_record.html' , user=user , title=title , dep_id=dep_id , s_number=s_number , u_detail=u_detail)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###############################
# /show_factory_monitor_detail
###############################
@app.route("/show_factory_monitor_detail", methods=['POST','GET'])
def show_factory_monitor_detail():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '監控紀錄 > 工廠溫溼度紀錄'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                s_kind                   = request.form['s_kind']
                s_c_kind                 = parameter.m_device[s_kind]
                kind_detail              = db.show_factory_monitor_detail(s_kind)
                kind_detail_temp_img     = db.show_factory_monitor_detail_temp_img(s_kind)
                kind_detail_rh_img       = db.show_factory_monitor_detail_rh_img(s_kind)
                kind_detail_temp_pie_img = db.show_factory_monitor_detail_temp_pie_img(s_kind)
                kind_detail_rh_pie_img   = db.show_factory_monitor_detail_rh_pie_img(s_kind)

                kind_detail_temp_val = db.show_factory_monitor_detail_temp_val(s_kind)
                kind_detail_rh_val   = db.show_factory_monitor_detail_rh_val(s_kind)
                    
                return render_template('ajax/detail_factory_monitor_record.html' , user=user , title=title , dep_id=dep_id , s_kind=s_kind , s_c_kind=s_c_kind , kind_detail=kind_detail , kind_detail_temp_img=kind_detail_temp_img , kind_detail_rh_img=kind_detail_rh_img , kind_detail_temp_val=kind_detail_temp_val , kind_detail_rh_val=kind_detail_rh_val , kind_detail_temp_pie_img=kind_detail_temp_pie_img , kind_detail_rh_pie_img=kind_detail_rh_pie_img)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###############################
# /show_computer_user_detail
###############################
@app.route("/show_computer_user_detail", methods=['POST','GET'])
def show_computer_user_detail():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '使用紀錄 > 電腦使用詳細紀錄'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                d_name = request.form['d_name']
                u_detail = db.show_computer_user_detail(d_name)
                    
                return render_template('ajax/detail_computer_user_record.html' , user=user , title=title , dep_id=dep_id , d_name=d_name , u_detail=u_detail)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##################################
# /factory_monitor_record_chart
##################################
@app.route("/factory_monitor_record_chart")
def factory_monitor_record_chart():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '監控紀錄 > 工廠溫溼度紀錄圖'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            # 数据
            labels = ['A', 'B', 'C', 'D']
            sizes = [15, 30, 45, 10]
            colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']

            # 创建圆饼图
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # 确保圆饼图是正圆

            # 将图像保存到内存中
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close(fig)

            # 将图像嵌入到HTML页面中
            image_data = base64.b64encode(buffer.read()).decode('utf-8')
            return render_template('pie_chart.html', image_data=image_data)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###################
# /vmware_detail
###################
@app.route("/vmware_detail", methods=['POST','GET'])
def vmware_detail():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '監控紀錄 > VMware 詳細使用紀錄'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':
                vm_name = request.form['vm_name']  

                logging.info(vm_name)
            
                vm_name_detail = db.show_vmware_detail_record(vm_name)
                vm_name_boot   = db.show_vmware_detail_item_record(vm_name , 'vm_boot_time')
                vm_name_cpu    = db.show_vmware_detail_item_record(vm_name , 'vm_cpu')
                vm_name_ram    = db.show_vmware_detail_item_record(vm_name , 'vm_ram')
                vm_name_hdd    = db.show_vmware_detail_item_record(vm_name , 'vm_hdd')
                vm_item_os     = db.show_vmware_item_detail(vm_name , 'vm_os')
                vm_item_state  = db.show_vmware_item_detail(vm_name , 'vm_os_state')
                vm_item_boot   = db.show_vmware_item_detail(vm_name , 'vm_boot_time')
                vm_item_ip     = db.show_vmware_item_detail(vm_name , 'vm_ip')
            
                return render_template('ajax/vmware_detail.html' , 
                                       vm_name=vm_name , vm_name_detail=vm_name_detail , 
                                       vm_name_cpu=vm_name_cpu , vm_name_ram=vm_name_ram , vm_name_hdd=vm_name_hdd , vm_name_boot=vm_name_boot ,
                                       vm_item_os=vm_item_os , vm_item_state=vm_item_state , vm_item_boot=vm_item_boot , vm_item_ip=vm_item_ip  
                                       )

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

############################
# /vmware_monitor_record
############################
@app.route("/vmware_monitor_record")
def vmware_monitor_record():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '監控紀錄 > VMware使用紀錄'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            kind_position = db.show_factory_monitor_position()
            
            ### 日當月報表
            day_money_by_year  = r_year
            day_money_by_month = db.bpm_day_money_by_month(r_year)

            ### VMware monitor state
            title_c                  = 'VMware monitor state'
            vm_statistics_taipei     = db.show_vmware_statistics_taipei()
            vm_statistics_factory    = db.show_vmware_statistics_factory()
            vm_host_taipei           = db.show_vmware_host_taipei()
            vm_host_factory          = db.show_vmware_host_factory()

            vm_taipei_run_title      = 'Taipei VMware running'
            vm_taipei_run            = db.show_check_vm_state('taipei','running')
            vm_taipei_stop_title     = 'Taipei VMware notRunning'
            vm_taipei_stop           = db.show_check_vm_state('taipei','notRunning')
            vm_factory_run_title     = 'Factory VMware running'
            vm_factory_run           = db.show_check_vm_state('factory','running')
            vm_factory_stop_title    = 'Factory VMware notRunning'
            vm_factory_stop          = db.show_check_vm_state('factory','notRunning')

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
            
            return render_template('vmware_monitor_record.html' , 
                                   user=user , title=title , dep_id=dep_name , updep_name=updep_name , kind_position=kind_position , 
                                   day_money_by_year=day_money_by_year , day_money_by_month=day_money_by_month ,
                                   title_c=title_c , vm_statistics_taipei=vm_statistics_taipei , vm_statistics_factory=vm_statistics_factory , 
                                   vm_host_taipei=vm_host_taipei , vm_host_factory=vm_host_factory
                                    )

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

################################
# /bpm_information_form_chart
################################
@app.route("/bpm_information_form_chart")
def bpm_information_form_chart():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'BPM 資訊需求單查詢 > 統計圖'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            kind_position = db.show_factory_monitor_position()
            
            ### 日當月報表
            day_money_by_year  = r_year
            day_money_by_month = db.bpm_day_money_by_month(r_year)

            ### 溫濕度圖表(品管,倉庫)
            warehouse_c              = 'Warehouse and Quality control sensor Temp'
            warehouse_temp_img       = db.show_factory_monitor_detail_warehouse_temp_img()
            warehouse_rh_img         = db.show_factory_monitor_detail_warehouse_rh_img()
            quality_control_temp_img = db.show_factory_monitor_detail_quality_control_temp_img()
            quality_control_rh_img   = db.show_factory_monitor_detail_quality_control_rh_img()

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
            
            return render_template('factory_monitor_record.html' , 
                                   user=user , title=title , dep_id=dep_name , updep_name=updep_name , kind_position=kind_position , 
                                   warehouse_c=warehouse_c , warehouse_temp_img=warehouse_temp_img , quality_control_temp_img=quality_control_temp_img ,
                                   warehouse_rh_img=warehouse_rh_img , quality_control_rh_img=quality_control_rh_img ,
                                   day_money_by_year=day_money_by_year , day_money_by_month=day_money_by_month
                                   )

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

############################
# /factory_monitor_record
############################
@app.route("/factory_monitor_record")
def factory_monitor_record():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '監控紀錄 > 工廠溫溼度紀錄'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            kind_position = db.show_factory_monitor_position()
            
            ### 日當月報表
            day_money_by_year  = r_year
            day_money_by_month = db.bpm_day_money_by_month(r_year)

            ### 溫濕度圖表(品管,倉庫)
            warehouse_c              = 'Warehouse and Quality control sensor Temp'
            warehouse_temp_img       = db.show_factory_monitor_detail_warehouse_temp_img()
            warehouse_rh_img         = db.show_factory_monitor_detail_warehouse_rh_img()
            quality_control_temp_img = db.show_factory_monitor_detail_quality_control_temp_img()
            quality_control_rh_img   = db.show_factory_monitor_detail_quality_control_rh_img()

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
            
            return render_template('factory_monitor_record.html' , 
                                   user=user , title=title , dep_id=dep_name , updep_name=updep_name , kind_position=kind_position , 
                                   warehouse_c=warehouse_c , warehouse_temp_img=warehouse_temp_img , quality_control_temp_img=quality_control_temp_img ,
                                   warehouse_rh_img=warehouse_rh_img , quality_control_rh_img=quality_control_rh_img ,
                                   day_money_by_year=day_money_by_year , day_money_by_month=day_money_by_month
                                   )

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##########################
# /computer_used_record
##########################
@app.route("/computer_used_record")
def computer_used_record():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '使用紀錄 > 電腦使用紀錄'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time``
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            
            ### 日當月報表
            day_money_by_year  = r_year
            day_money_by_month = db.bpm_day_money_by_month(r_year)
            d_name             = db.show_device_name_list()

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
                
            return render_template('computer_used_record.html' , user=user , title=title , dep_id=dep_name , updep_name=updep_name , d_name=d_name , 
                                   day_money_by_year=day_money_by_year, day_money_by_month=day_money_by_month
                                   )

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#####################################
# /submit_alter_new_work_record_form
#####################################
@app.route("/submit_alter_new_work_record_form", methods=['POST','GET'])
def submit_alter_new_work_record_form():
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':
               
                w_title      = request.form['w_title']
                w_year       = request.form['w_year']
                w_month      = request.form['w_month']
                w_day        = request.form['w_day']
                w_place      = request.form['w_place']
                w_start      = request.form['w_start']
                w_end        = request.form['w_end']
                w_status     = request.form['w_status']
                w_dep        = request.form['w_dep']
                w_user       = request.form['w_user']
                w_new_work_record_content = request.form['w_new_work_record_content']
                
                ### operation record title
                operation_record_title = f'修改工作進度表 - {w_title} / {w_user}'    
                
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                ### 更新工作進度表
                db.alter_work_record(w_title , w_year , w_month , w_day , w_place , w_start , w_end , w_status , w_dep , w_user , w_new_work_record_content)
                res_list = db.work_record_list(w_dep)
                
                return render_template('ajax/work_record_form_list.html' , res_list=res_list)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#####################################
# /submit_add_new_work_record_form
#####################################
@app.route("/submit_add_new_work_record_form", methods=['POST','GET'])
def submit_add_new_work_record_form():
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':
               
                w_title      = request.form['w_title']
                w_year       = request.form['w_year']
                w_month      = request.form['w_month']
                w_day        = request.form['w_day']
                w_place      = request.form['w_place']
                w_start      = request.form['w_start']
                w_end        = request.form['w_end']
                w_status     = request.form['w_status']
                w_kind       = request.form['w_kind']
                w_dep        = request.form['w_dep']
                w_user       = request.form['w_user']
                w_new_work_record_content = request.form['w_new_work_record_content']
                
                ### operation record title
                operation_record_title = f'建立工作進度表 - {w_title} / {w_user}'    
                
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                db.add_work_record(w_title , w_year , w_month , w_day , w_place , w_start , w_end , w_status , w_dep , w_user , w_new_work_record_content , w_kind)
                res_list = db.work_record_list(w_dep)
                
                return render_template('ajax/work_record_form_list.html' , res_list=res_list)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#############################
# /submit_add_account_form
#############################
@app.route("/submit_add_account_form", methods=['POST','GET'])
def submit_add_account_form():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '權限管理 -  建立帳號'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                a_date     = request.form['a_date']
                a_work_no  = request.form['a_work_no']
                a_name     = request.form['a_name']
                a_user     = request.form['a_user']
                a_position = request.form['a_position']
                a_status   = request.form['a_status']

                res = db.add_account(a_date , a_name , a_work_no , a_position , a_status , a_user)

                if res:
                    return render_template('ajax/add_account_form.html' , user=user , lv=lv , title=title , r_date=r_date , msg='ok')
                
                return render_template('ajax/add_account_form.html' , user=user , lv=lv , title=title , r_date=r_date , msg='no')

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#######################
# /load_account_form
#######################
@app.route("/load_account_form" , methods=['POST','GET'])
def load_account_form():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '權限管理 -  新增帳號表'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_position = db.factory_work_position()

            return render_template('ajax/add_account_form.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_position=factory_work_position)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#############################
# /menu_account_management
#############################
@app.route("/menu_account_management")
def menu_account_management():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '權限管理 - 帳號管理'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station()
            factory_work_account_list = db.factory_work_account_list()

            return render_template('menu_account_management.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , factory_work_account_list=factory_work_account_list)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

############################
# /download_day_money_csv
############################
@app.route("/download_day_money_csv" , methods=['POST','GET'])
def download_day_money_csv():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '財務部 - 下載日當月報表'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            if request.method == 'POST':
                
                year  = request.form['year']
                month = request.form['month']

                csv = year+'_'+month+'.csv'
                
                with open(csv , mode='w' , newline='') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


                days_in_month = 31
                name_in_month = db.show_day_money_detail_name(year , month)
                day_in_total  = db.show_day_money_detail_day_total(year , month)

                for row in name_in_month:
                    writer.writerow(row)

                

                #return render_template('ajax/show_day_money_detail.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , year=year , month=month , days_in_month=days_in_month , name_in_month=name_in_month , day_in_total=day_in_total)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#########################################
# /download_mrlibrary_file
#########################################
@app.route('/download_mrlibrary_file' , methods=['GET'])
def download_mrlibrary_file():
    
    if request.method == 'GET':
        ai_name = request.args.get('f_name')
        
        if ai_name.endswith(".pdf"):
            
            download_file = f"/home/otsuka/otsuka_platform/m_report/{ai_name}"
            d_name        = f"{ai_name}"
            
            return send_file(
                    download_file,
                    as_attachment=True,     # 将文件作为附件下载
                    download_name=d_name,   # 自定义下载的文件名
                    #mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'          # 设置 Excel 文件的 MIME 类型
                    #mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'  # 设置 PPT 文件的 MIME 类型
                    mimetype='application/pdf'   # 设置 PDF 文件的 MIME 类型
                    #mimetype='video/x-ms-wmv'   # 设置 WMV 文件的 MIME 类型
            )
        
        elif ai_name.endswith(".wmv"):
            
            download_ppt = f"/home/otsuka/otsuka_platform/m_report/{ai_name}"
            ppt_name     = f"{ai_name}"

            # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
            return send_file(
                download_ppt,
                as_attachment=True,      # 将文件作为附件下载
                download_name=ppt_name,  # 自定义下载的文件名
                #mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'          # 设置 Excel 文件的 MIME 类型
                #mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'  # 设置 PPT 文件的 MIME 类型
                #mimetype='application/pdf'  # 设置 PDF 文件的 MIME 类型
                mimetype='video/x-ms-wmv'    # 设置 WMV 文件的 MIME 类型
            )
        
        elif ai_name.endswith(".ppt"):

            download_ppt = f"/home/otsuka/otsuka_platform/m_report/{ai_name}"
            ppt_name     = f"{ai_name}"

            return send_file(
                download_ppt,
                as_attachment=True,      # 将文件作为附件下载
                download_name=ppt_name,  # 自定义下载的文件名
                #mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'         # 设置 Excel 文件的 MIME 类型
                mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'  # 设置 PPT 文件的 MIME 类型
                #mimetype='application/pdf'  # 设置 PDF 文件的 MIME 类型
                #mimetype='video/x-ms-wmv'   # 设置 WMV 文件的 MIME 类型
            )

#########################################
# /download_ai_rapid_miner_file
#########################################
@app.route('/download_ai_rapid_miner_file' , methods=['GET'])
def download_ai_rapid_miner_file():
    
    if request.method == 'GET':
        ai_name = request.args.get('f_name')
        
        if ai_name.endswith(".pdf"):
            
            download_file = f"/home/otsuka/otsuka_platform/ai/rapid_miner/{ai_name}"
            d_name        = f"{ai_name}"
            
            return send_file(
                    download_file,
                    as_attachment=True,     # 将文件作为附件下载
                    download_name=d_name,   # 自定义下载的文件名
                    #mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'          # 设置 Excel 文件的 MIME 类型
                    #mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'  # 设置 PPT 文件的 MIME 类型
                    mimetype='application/pdf'   # 设置 PDF 文件的 MIME 类型
                    #mimetype='video/x-ms-wmv'   # 设置 WMV 文件的 MIME 类型
            )
        
        elif ai_name.endswith(".wmv"):
            
            download_ppt = f"/home/otsuka/otsuka_platform/ai/rapid_miner/{ai_name}"
            ppt_name     = f"{ai_name}"

            # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
            return send_file(
                download_ppt,
                as_attachment=True,      # 将文件作为附件下载
                download_name=ppt_name,  # 自定义下载的文件名
                #mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'          # 设置 Excel 文件的 MIME 类型
                #mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'  # 设置 PPT 文件的 MIME 类型
                #mimetype='application/pdf'  # 设置 PDF 文件的 MIME 类型
                mimetype='video/x-ms-wmv'    # 设置 WMV 文件的 MIME 类型
            )
        
        elif ai_name.endswith(".ppt"):

            download_ppt = f"/home/otsuka/otsuka_platform/ai/rapid_miner/{ai_name}"
            ppt_name     = f"{ai_name}"

            return send_file(
                download_ppt,
                as_attachment=True,      # 将文件作为附件下载
                download_name=ppt_name,  # 自定义下载的文件名
                #mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'         # 设置 Excel 文件的 MIME 类型
                mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'  # 设置 PPT 文件的 MIME 类型
                #mimetype='application/pdf'  # 设置 PDF 文件的 MIME 类型
                #mimetype='video/x-ms-wmv'   # 设置 WMV 文件的 MIME 类型
            )

#########################################
# /download_ai_fine_tuning_file
#########################################
@app.route('/download_ai_fine_tuning_file' , methods=['GET'])
def download_ai_fine_tuning_file():
    
    if request.method == 'GET':
        ai_date = request.args.get('ai_date')
        
        download_ppt = f"/home/otsuka/otsuka_platform/ai/ai_fine_tuning_{ai_date}.pptx"
        ppt_name     = f"ai_fine_tuning_{ai_date}.pptx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_ppt,
            as_attachment=True,        # 将文件作为附件下载
            download_name=ppt_name,  # 自定义下载的文件名
           #mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'  # 设置 PPT 文件的 MIME 类型

        )

#########################################
# /download_card_reader_excel_by_month
#########################################
@app.route('/download_card_reader_excel_by_month' , methods=['GET'])
def download_card_reader_excel_by_month():
    
    if request.method == 'GET':
        position = request.args.get('position')
        month    = request.args.get('month')
        
        download_excel = f"/home/otsuka/otsuka_platform/excel/card_reader_{position}_{month}.xlsx"
        excel_name     = f"card_reader_{position}_{month}.xlsx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )

############################################
# /download_bpm_expenditure_excel
############################################
@app.route('/download_bpm_expenditure_excel' , methods=['GET'])
def download_bpm_expenditure_excel():
    
    if request.method == 'GET':
        
        q_s_date       = request.args.get('s_date')
        q_e_date       = request.args.get('e_date')
        q_b_e_dep      = request.args.get('dep')
        q_b_e_d_member = request.args.get('member')
        q_b_e_status   = request.args.get('status')
        
        download_excel = f"/home/otsuka/otsuka_platform/excel/bpm/開支證明單_{q_b_e_dep}_{q_b_e_d_member}_{q_b_e_status}.xlsx"
        excel_name     = f"開支證明單_{q_b_e_dep}_{q_b_e_d_member}_{q_b_e_status}.xlsx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )

############################################
# /download_card_reader_excel_every_month
############################################
@app.route('/download_card_reader_excel_every_month' , methods=['GET'])
def download_card_reader_excel_every_month():
    
    if request.method == 'GET':
        position = request.args.get('position')
        tb       = request.args.get('tb')
        
        download_excel = f"/home/otsuka/otsuka_platform/excel/{tb}_{position}.xlsx"
        excel_name     = f"{tb}_{position}.xlsx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )

####################################
# /download_factory_erp_ss2_json
####################################
@app.route('/download_factory_erp_ss2_json' , methods=['GET'])
def download_factory_erp_ss2_json():
    
    if request.method == 'GET':
        
        q_s_date = request.args.get('q_s_date')
        q_e_date = request.args.get('q_e_date')
        q_c_name = request.args.get('q_c_name')
        q_p_name = request.args.get('q_p_name')
        
        download_excel = f"/home/otsuka/otsuka_platform/json/factory_erp_ss2/factory_erp_ss2_{q_s_date}_{q_e_date}.json"
        excel_name     = f"factory_erp_ss2_{q_s_date}_{q_e_date}.json"
        
        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )


########################################
# /download_factory_erp_subform_excel
########################################
@app.route('/download_factory_erp_subform_excel' , methods=['GET'])
def download_factory_erp_subform_excel():
    
    if request.method == 'GET':
        
        q_s_date = request.args.get('q_s_date')
        q_e_date = request.args.get('q_e_date')
                           
        download_excel = f"/home/otsuka/otsuka_platform/excel/factory_erp_ss2/factory_erp_subform_{q_s_date}_{q_e_date}.xlsx"
        excel_name     = f"factory_erp_subform_{q_s_date}_{q_e_date}.xlsx"
        
        return send_file(
            download_excel,
            as_attachment=True,        
            download_name=excel_name,  
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 類型
        )

####################################
# /download_factory_erp_ss2_excel
####################################
@app.route('/download_factory_erp_ss2_excel' , methods=['GET'])
def download_factory_erp_ss2_excel():
    
    if request.method == 'GET':
        
        q_s_date = request.args.get('q_s_date')
        q_e_date = request.args.get('q_e_date')
        q_c_name = request.args.get('q_c_name')
        q_p_name = request.args.get('q_p_name')
        
        download_excel = f"/home/otsuka/otsuka_platform/excel/factory_erp_ss2/factory_erp_ss2_{q_s_date}_{q_e_date}.xlsx"
        excel_name     = f"factory_erp_ss2_{q_s_date}_{q_e_date}.xlsx"
        
        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )

#################################
# /download_hr_360_excel
#################################
@app.route('/download_hr_360_excel' , methods=['GET'])
def download_hr_360_excel():
    
    if request.method == 'GET':
        job = request.args.get('job')
        
        download_excel = f"/home/otsuka/otsuka_platform/excel/hr_360/hr_360_{job}.xlsx"
        excel_name     = f"hr_360_{job}.xlsx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )

#################################
# /download_card_reader_excel
#################################
@app.route('/download_card_reader_excel' , methods=['GET'])
def download_card_reader_excel():
    
    if request.method == 'GET':
        position = request.args.get('position')
        day      = request.args.get('day')
        
        download_excel = f"/home/otsuka/otsuka_platform/excel/card_reader_{position}_{day}.xlsx"
        excel_name     = f"card_reader_{position}_{day}.xlsx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )

#################################
# /download_parking_fee_excel
#################################
@app.route('/download_parking_fee_excel' , methods=['GET'])
def download_parking_fee_excel():
    
    if request.method == 'GET':
        year  = request.args.get('year')
        month = request.args.get('month')

        host_name = os.environ['COMPUTERNAME']
        
        if host_name == 'OTSUAK-JASON':
            # 開發機
            download_excel = f"F:/otsuka/Git/otsuka_factory_work_time_record/excel/parking_fee_{year}{month}.xlsx"
        else:
            # 正式機
            download_excel = f"C:/Jason_python/otsuka_factory_work_time_record/excel/parking_fee_{year}{month}.xlsx"
        
        excel_name     = f"parking_fee_{year}{month}.xlsx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )

#################################
# /download_over_traffic_excel
#################################
@app.route('/download_over_traffic_excel' , methods=['GET'])
def download_over_traffic_excel():
    
    if request.method == 'GET':
        year  = request.args.get('year')
        month = request.args.get('month')

        host_name = os.environ['COMPUTERNAME']
        
        if host_name == 'OTSUAK-JASON':
            # 開發機
            download_excel = f"F:/otsuka/Git/otsuka_factory_work_time_record/excel/over_traffic_{year}{month}.xlsx"
        else:
            # 正式機
            download_excel = f"C:/Jason_python/otsuka_factory_work_time_record/excel/over_traffic_{year}{month}.xlsx"
        
        excel_name     = f"over_traffic_{year}{month}.xlsx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )

############################
# /download_traffic_excel
############################
@app.route('/download_traffic_excel' , methods=['GET'])
def download_traffic_excel():
    
    if request.method == 'GET':
        year  = request.args.get('year')
        month = request.args.get('month')

        host_name = os.environ['COMPUTERNAME']
        
        if host_name == 'OTSUAK-JASON':
            # 開發機
            download_excel = f"F:/otsuka/Git/otsuka_factory_work_time_record/excel/traffic_{year}{month}.xlsx"
        else:
            # 正式機
            download_excel = f"C:/Jason_python/otsuka_factory_work_time_record/excel/traffic_{year}{month}.xlsx"
        
        excel_name     = f"traffic_{year}{month}.xlsx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )

##########################
# /download_tolls_excel
##########################
@app.route('/download_tolls_excel' , methods=['GET'])
def download_tolls_excel():
    
    if request.method == 'GET':
        year  = request.args.get('year')
        month = request.args.get('month')

        host_name = os.environ['COMPUTERNAME']
        
        if host_name == 'OTSUAK-JASON':
            # 開發機
            download_excel = f"F:/otsuka/Git/otsuka_factory_work_time_record/excel/tolls_{year}{month}.xlsx"
        else:
            # 正式機
            download_excel = f"C:/Jason_python/otsuka_factory_work_time_record/excel/tolls_{year}{month}.xlsx"
        
        excel_name     = f"tolls_{year}{month}.xlsx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )

##########################
# /download_trick_excel
##########################
@app.route('/download_trick_excel' , methods=['GET'])
def download_trick_excel():
    
    if request.method == 'GET':
        year  = request.args.get('year')
        month = request.args.get('month')

        host_name = os.environ['COMPUTERNAME']
        
        if host_name == 'OTSUAK-JASON':
            # 開發機
            download_excel = f"F:/otsuka/Git/otsuka_factory_work_time_record/excel/trick_{year}{month}.xlsx"
        else:
            # 正式機
            download_excel = f"C:/Jason_python/otsuka_factory_work_time_record/excel/trick_{year}{month}.xlsx"
        
        excel_name     = f"trick_{year}{month}.xlsx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )

#########################
# /download_taxi_excel
#########################
@app.route('/download_taxi_excel' , methods=['GET'])
def download_taxi_excel():
    
    if request.method == 'GET':
        year  = request.args.get('year')
        month = request.args.get('month')

        host_name = os.environ['COMPUTERNAME']
        
        if host_name == 'OTSUAK-JASON':
            # 開發機
            download_excel = f"F:/otsuka/Git/otsuka_factory_work_time_record/excel/taxi_{year}{month}.xlsx"
        else:
            # 正式機
            download_excel = f"C:/Jason_python/otsuka_factory_work_time_record/excel/taxi_{year}{month}.xlsx"
        
        excel_name     = f"taxi_{year}{month}.xlsx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )
    
#########################
# /download_stay_excel
#########################
@app.route('/download_stay_excel' , methods=['GET'])
def download_stay_excel():
    
    if request.method == 'GET':
        year  = request.args.get('year')
        month = request.args.get('month')

        host_name = os.environ['COMPUTERNAME']
        
        if host_name == 'OTSUAK-JASON':
            # 開發機
            download_excel = f"F:/otsuka/Git/otsuka_factory_work_time_record/excel/stay_{year}{month}.xlsx"
        else:
            # 正式機
            download_excel = f"C:/Jason_python/otsuka_factory_work_time_record/excel/stay_{year}{month}.xlsx"
        
        excel_name     = f"stay_{year}{month}.xlsx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )

##########################
# /download_other_excel
##########################
@app.route('/download_other_excel' , methods=['GET'])
def download_other_excel():
    
    if request.method == 'GET':
        year  = request.args.get('year')
        month = request.args.get('month')

        host_name = os.environ['COMPUTERNAME']
        
        if host_name == 'OTSUAK-JASON':
            # 開發機
            download_excel = f"F:/otsuka/Git/otsuka_factory_work_time_record/excel/other_{year}{month}.xlsx"
        else:
            # 正式機
            download_excel = f"C:/Jason_python/otsuka_factory_work_time_record/excel/other_{year}{month}.xlsx"
        
        excel_name     = f"other_{year}{month}.xlsx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )

########################
# /download_oil_excel
########################
@app.route('/download_oil_excel' , methods=['GET'])
def download_oil_excel():
    
    if request.method == 'GET':
        year  = request.args.get('year')
        month = request.args.get('month')

        host_name = os.environ['COMPUTERNAME']
        
        if host_name == 'OTSUAK-JASON':
            # 開發機
            download_excel = f"F:/otsuka/Git/otsuka_factory_work_time_record/excel/oil_{year}{month}.xlsx"
        else:
            # 正式機
            download_excel = f"C:/Jason_python/otsuka_factory_work_time_record/excel/oil_{year}{month}.xlsx"
        
        excel_name     = f"oil_{year}{month}.xlsx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )

####################
# /download_excel
####################
@app.route('/download_excel' , methods=['GET'])
def download_excel():
    
    if request.method == 'GET':
        year  = request.args.get('year')
        month = request.args.get('month')

        host_name = os.environ['COMPUTERNAME']
        
        if host_name == 'OTSUAK-JASON':
            # 開發機
            download_excel = f"F:/otsuka/Git/otsuka_factory_work_time_record/excel/{year}{month}.xlsx"
        else:
            # 正式機
            download_excel = f"C:/Jason_python/otsuka_factory_work_time_record/excel/{year}{month}.xlsx"
        
        excel_name     = f"{year}{month}.xlsx"

        # 使用 send_file 函数发送 Excel 文件供下载，并设置 MIME 类型
        return send_file(
            download_excel,
            as_attachment=True,        # 将文件作为附件下载
            download_name=excel_name,  # 自定义下载的文件名
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # 设置 Excel 文件的 MIME 类型
        )

##############################
# /download_day_money_excel
##############################
@app.route("/download_day_money_excel" , methods=['POST','GET'])
def download_day_money_excel():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '財務部 - 下載日當月報表內容'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            if request.method == 'POST':
                
                year  = request.form['year']
                month = request.form['month']

                try:
                    #download_excel = f"F:\otsuka\Git\otsuka_factory_work_time_record\excel\{year}{month}.xlsx"
                    download_excel = f"F:/otsuka/Git/otsuka_factory_work_time_record/excel/{year}{month}.xlsx"
                    excel_name = f"{year}{month}.xlsx"
                    
                    if os.path.exists(download_excel):
                        
                        mime_type, _ = mimetypes.guess_type(download_excel)
                            
                        #logging.info(f"{download_excel} , 文件存在。")
                        download_name='custom-filename.xlsx',  # 自定义下载的文件名
                        # 设置 Excel 文件的 MIME 类型
                        return send_file(download_excel , as_attachment=True , mimetype=mime_type , download_name=excel_name)
                
                    else:
                        logging.info(f"{download_excel} , 文件不存在。")
                
                except Exception as e:
                    logging.error('<Error> download excel :' + str(e))

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

########################################
# /show_day_month_parking_fee_detail
########################################
@app.route("/show_day_month_parking_fee_detail" , methods=['POST','GET'])
def show_day_month_parking_fee_detail():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '財務部 - 日當停車費月報表內容'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            if request.method == 'POST':
                
                year  = request.form['year']
                month = request.form['month']

                days_in_month = 31
                name_in_month = db.show_day_money_parking_fee_detail_name(year , month)
                day_in_total  = db.show_day_money_parking_fee_detail_day_total(year , month)

                return render_template('ajax/show_day_money_detail.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , year=year , month=month , days_in_month=days_in_month , name_in_month=name_in_month , day_in_total=day_in_total)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

########################################
# /show_day_month_over_traffic_detail
########################################
@app.route("/show_day_month_over_traffic_detail" , methods=['POST','GET'])
def show_day_month_over_traffic_detail():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '財務部 - 日當超里程月報表內容'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            if request.method == 'POST':
                
                year  = request.form['year']
                month = request.form['month']

                days_in_month = 31
                name_in_month = db.show_day_money_over_traffic_detail_name(year , month)
                day_in_total  = db.show_day_money_over_traffic_detail_day_total(year , month)

                return render_template('ajax/show_day_money_detail.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , year=year , month=month , days_in_month=days_in_month , name_in_month=name_in_month , day_in_total=day_in_total)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###################################
# /show_day_month_traffic_detail
###################################
@app.route("/show_day_month_traffic_detail" , methods=['POST','GET'])
def show_day_month_traffic_detail():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '財務部 - 日當交通費月報表內容'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            if request.method == 'POST':
                
                year  = request.form['year']
                month = request.form['month']

                days_in_month = 31
                name_in_month = db.show_day_money_traffic_detail_name(year , month)
                day_in_total  = db.show_day_money_traffic_detail_day_total(year , month)

                return render_template('ajax/show_day_money_detail.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , year=year , month=month , days_in_month=days_in_month , name_in_month=name_in_month , day_in_total=day_in_total)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#################################
# /show_day_month_tolls_detail
#################################
@app.route("/show_day_month_tolls_detail" , methods=['POST','GET'])
def show_day_month_tolls_detail():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '財務部 - 日當過路費月報表內容'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            if request.method == 'POST':
                
                year  = request.form['year']
                month = request.form['month']

                days_in_month = 31
                name_in_month = db.show_day_money_tolls_detail_name(year , month)
                day_in_total  = db.show_day_money_tolls_detail_day_total(year , month)

                return render_template('ajax/show_day_money_detail.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , year=year , month=month , days_in_month=days_in_month , name_in_month=name_in_month , day_in_total=day_in_total)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#################################
# /show_day_month_trick_detail
#################################
@app.route("/show_day_month_trick_detail" , methods=['POST','GET'])
def show_day_month_trick_detail():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '財務部 - 日當車票月報表內容'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            if request.method == 'POST':
                
                year  = request.form['year']
                month = request.form['month']

                days_in_month = 31
                name_in_month = db.show_day_money_trick_detail_name(year , month)
                day_in_total  = db.show_day_money_trick_detail_day_total(year , month)

                return render_template('ajax/show_day_money_detail.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , year=year , month=month , days_in_month=days_in_month , name_in_month=name_in_month , day_in_total=day_in_total)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

################################
# /show_day_month_taxi_detail
################################
@app.route("/show_day_month_taxi_detail" , methods=['POST','GET'])
def show_day_month_taxi_detail():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '財務部 - 日當計程車月報表內容'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            if request.method == 'POST':
                
                year  = request.form['year']
                month = request.form['month']

                days_in_month = 31
                name_in_month = db.show_day_money_taxi_detail_name(year , month)
                day_in_total  = db.show_day_money_taxi_detail_day_total(year , month)

                return render_template('ajax/show_day_money_detail.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , year=year , month=month , days_in_month=days_in_month , name_in_month=name_in_month , day_in_total=day_in_total)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

################################
# /show_day_month_stay_detail
################################
@app.route("/show_day_month_stay_detail" , methods=['POST','GET'])
def show_day_month_stay_detail():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '財務部 - 日當住宿月報表內容'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            if request.method == 'POST':
                
                year  = request.form['year']
                month = request.form['month']

                days_in_month = 31
                name_in_month = db.show_day_money_stay_detail_name(year , month)
                day_in_total  = db.show_day_money_stay_detail_day_total(year , month)

                return render_template('ajax/show_day_money_detail.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , year=year , month=month , days_in_month=days_in_month , name_in_month=name_in_month , day_in_total=day_in_total)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#################################
# /show_day_month_other_detail
#################################
@app.route("/show_day_month_other_detail" , methods=['POST','GET'])
def show_day_month_other_detail():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '財務部 - 日當其他月報表內容'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            if request.method == 'POST':
                
                year  = request.form['year']
                month = request.form['month']

                days_in_month = 31
                name_in_month = db.show_day_money_other_detail_name(year , month)
                day_in_total  = db.show_day_money_other_detail_day_total(year , month)

                return render_template('ajax/show_day_money_detail.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , year=year , month=month , days_in_month=days_in_month , name_in_month=name_in_month , day_in_total=day_in_total)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###############################
# /show_day_month_oil_detail
###############################
@app.route("/show_day_month_oil_detail" , methods=['POST','GET'])
def show_day_month_oil_detail():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '財務部 - 日當油單月報表內容'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            if request.method == 'POST':
                
                year  = request.form['year']
                month = request.form['month']

                days_in_month = 31
                name_in_month = db.show_day_money_oil_detail_name(year , month)
                day_in_total  = db.show_day_money_oil_detail_day_total(year , month)

                return render_template('ajax/show_day_money_detail.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , year=year , month=month , days_in_month=days_in_month , name_in_month=name_in_month , day_in_total=day_in_total)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###########################
# /show_day_month_detail
###########################
@app.route("/show_day_month_detail" , methods=['POST','GET'])
def show_day_month_detail():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '財務部 - 日當月報表內容'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            if request.method == 'POST':
                
                year  = request.form['year']
                month = request.form['month']

                days_in_month = 31
                name_in_month = db.show_day_money_detail_name(year , month)
                day_in_total  = db.show_day_money_detail_day_total(year , month)

                return render_template('ajax/show_day_money_detail.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , year=year , month=month , days_in_month=days_in_month , name_in_month=name_in_month , day_in_total=day_in_total)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

######################
# /day_money_report
######################
@app.route("/day_money_report")
def day_money_report():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '財務部 - 日當月報表'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            day_money_by_year  = r_year
            day_money_by_month = db.bpm_day_money_by_month(r_year)

            return render_template('day_money_report.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , day_money_by_year=day_money_by_year , day_money_by_month=day_money_by_month)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###################################
# /prouuction_3_work_time_record
###################################
@app.route("/production_3_work_time_record")
def prouuction_3_work_time_record():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '生產三部 - 液劑工時時間記錄表'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            ### 日當月報表
            day_money_by_year  = r_year
            day_money_by_month = db.bpm_day_money_by_month(r_year)

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)

            return render_template('production_3_work_time_record.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , 
                                   a_work_no=a_work_no , a_name=a_name , dep_id=dep_name , updep_name=updep_name , day_money_by_year=day_money_by_year , 
                                   day_money_by_month=day_money_by_month
                                   )

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###################################
# /prouuction_1_work_time_record
###################################
@app.route("/production_1_work_time_record")
def prouuction_1_work_time_record():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '生產一部 - 液劑工時時間記錄表'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_1()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            return render_template('production_1_work_time_record.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

############################
# /department_list_detail
############################
@app.route("/department_list_detail" , methods=['GET','POST'])
def department_list_detail():
    
    ### session 
    user = session['user']
    lv   = session['lv']
    login_code = session['login_code']
    dep_id     = session['department_id']

    ### r_time
    r_date  = time.strftime("%Y-%m-%d" , time.localtime())
    r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
    r_year  = time.strftime("%Y" , time.localtime())
    r_month = time.strftime("%m" , time.localtime())

    ### check repeat login
    check_repeat_login = db.check_login_code(user,login_code)
    
    operation_record_title = '部門詳細資料'    
    ### operation record
    db.operation_record(r_time,user,login_code,operation_record_title)    

    #################
    # main content 
    #################

    if request.method == 'POST':

        d_code   = request.form['d_code']
        d_e_name = db.department_list_detail(d_code)
        
        return render_template('ajax/department_list_detail.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , r_date=r_date , d_e_name=d_e_name)

##############################
# /department_no_search_val
##############################
@app.route("/department_no_search_val" , methods=['GET','POST'])
def department_no_search_val():
    
    ### session 
    user = session['user']
    lv   = session['lv']
    login_code = session['login_code']
    dep_id     = session['department_id']

    ### r_time
    r_date  = time.strftime("%Y-%m-%d" , time.localtime())
    r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
    r_year  = time.strftime("%Y" , time.localtime())
    r_month = time.strftime("%m" , time.localtime())

    ### check repeat login
    check_repeat_login = db.check_login_code(user,login_code)
    
    operation_record_title = '部門代號查詢結果'    
    ### operation record
    db.operation_record(r_time,user,login_code,operation_record_title)    

    #################
    # main content 
    #################

    if request.method == 'POST':

        employee_name   = request.form['search_name']
        res = db.department_no_search_val(employee_name)
        
        return render_template('ajax/department_no_search.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , r_date=r_date , res=res)

###############################
# /submit_it_annual_budget
###############################
@app.route("/submit_it_annual_budget" , methods=['POST','GET'])
def submit_it_annual_budget():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '確定新增 IT 年度預算'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)
            

            if request.method == 'POST':
                
                it_annual_budget_date            = request.form['it_annual_budget_date'];   
                it_annual_budget_build_year      = request.form['it_annual_budget_build_year'];   
                it_annual_budget_kind            = request.form['it_annual_budget_kind'];   
                it_annual_budget_title           = request.form['it_annual_budget_title'];   
                it_annual_budget_otsuka_holdings = request.form['it_annual_budget_otsuka_holdings'];   
                it_annual_budget_year            = request.form['it_annual_budget_year'];   
                it_annual_budget_remaining_now   = request.form['it_annual_budget_remaining_now'];   
                it_annual_budget_comment         = request.form['it_annual_budget_comment'];   

                db.submit_it_annual_budget(it_annual_budget_date , it_annual_budget_build_year , it_annual_budget_kind , it_annual_budget_title , it_annual_budget_otsuka_holdings , it_annual_budget_year , it_annual_budget_remaining_now , it_annual_budget_comment)

                ### IT 年度預算清單
                it_annual_budget_select_kind            = db.it_annual_budget_kind_list() # 種類清單
                it_annual_budget_select_otsuka_holdings = db.it_annual_budget_otsuka_holdings_list() # otsuka_holdings 清單
                it_annual_budget_year_total             = db.it_annual_budget_year_total() # 年度總計

                ### IT 年度預算清單
                it_annual_budget_list_by_date = db.it_annual_budget_by_date()
                contract_list_by_kind = db.otsuka_contract_by_kind()

                return render_template('it_annual_budget.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , 
                                       a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , it_annual_budget_select_kind=it_annual_budget_select_kind , 
                                       it_annual_budget_select_otsuka_holdings=it_annual_budget_select_otsuka_holdings , it_annual_budget_year_total=it_annual_budget_year_total)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###############################
# /load_dep_detail2
###############################
@app.route("/load_dep_detail2" , methods=['POST','GET'])
def load_dep_detail2():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '載入部門清單資料'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            
            if request.method == 'POST':
                
                dep2_no      = request.form['dep2']
                dep2_name    = request.form['dep2_name']        
                upper_dep2 = db.bpm_load_account_list_by_dep2(dep2_no)

                return render_template('ajax/load_dep_detail2.html' , upper_dep2=upper_dep2 , dep2_name=dep2_name)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 


###############################
# /load_dep_detail
###############################
@app.route("/load_dep_detail" , methods=['POST','GET'])
def load_dep_detail():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '載入處(部)門清單資料'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':
                
                dep_no      = request.form['dep'];    
                upper_dep = db.bpm_load_account_list_by_dep(dep_no)

                return render_template('ajax/load_dep_detail.html' , upper_dep=upper_dep)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###############################
# /submit_otsuka_contract
###############################
@app.route("/submit_otsuka_contract" , methods=['POST','GET'])
def submit_otsuka_contract():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '確定新增合約'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station_3()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            if request.method == 'POST':
                
                o_c_date      = request.form['o_c_date'];   
                o_c_kind      = request.form['o_c_kind'];   
                o_c_title     = request.form['o_c_title'];   
                o_c_cost      = request.form['o_c_cost'];   
                o_c_time      = request.form['o_c_time'];   
                o_c_company   = request.form['o_c_company'];   
                o_c_name      = request.form['o_c_name'];   
                o_c_telephone = request.form['o_c_telephone'];   
                o_c_phone     = request.form['o_c_phone'];   
                o_c_comment   = request.form['o_c_comment'];  

                db.submit_otsuka_contract(o_c_date , o_c_kind , o_c_title , o_c_cost , o_c_time , o_c_company , o_c_name , o_c_telephone , o_c_phone , o_c_comment)

                ### 合約清單
                contract_list_by_date = db.otsuka_contract_by_date()
                contract_list_by_kind = db.otsuka_contract_by_kind()

                return render_template('it_contract.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , contract_list_by_date=contract_list_by_date , contract_list_by_kind=contract_list_by_kind)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

######################################
# /reload_it_annual_budget_add_form
######################################
@app.route("/reload_it_annual_budget_add_form")
def reload_it_annual_budget_add_form():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'reload IT 年度預算表新增表'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            
            it_annual_budget_select_kind            = db.it_annual_budget_kind_list() # 種類清單
            it_annual_budget_select_otsuka_holdings = db.it_annual_budget_otsuka_holdings_list() # otsuka_holdings 清單
            
            return render_template('ajax/reload_it_annual_budget_add_form.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_id , it_annual_budget_select_kind=it_annual_budget_select_kind , 
                                   it_annual_budget_select_otsuka_holdings=it_annual_budget_select_otsuka_holdings)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))  


#####################################
# /query_account
#####################################
@app.route("/query_account" , methods=['POST','GET'])
def query_account():
    
    if 'user' in session:
        
        ### operation record title
        query_account = request.form['query_account']   
        operation_record_title = f'搜尋 帳號 : {query_account} 內容'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                query_account = request.form['query_account']   

                res_query_account = db.bpm_account_list_by_dep_search(query_account)
                
            return render_template('ajax/bpm_account_list_by_dep_search.html' , res_query_account=res_query_account)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#####################################
# /mrd_8_del_auto_email_push
#####################################
@app.route("/mrd_8_del_auto_email_push" , methods=['POST','GET'])
def mrd_8_del_auto_email_push():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢 / 公告自動 Email 通知設定 , 刪除 Email'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                mrd_8_add_auto_email    = request.form['mrd_8_add_auto_email']   
                
                check_email = db.mrd_8_del_auto_email(mrd_8_add_auto_email)
                
            return render_template('ajax/mrd_8_government_bulletin_del_email.html' , check_email=check_email , email=mrd_8_add_auto_email)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#####################################
# /mrd_8_add_auto_email_push2
#####################################
@app.route("/mrd_8_add_auto_email_push2" , methods=['POST','GET'])
def mrd_8_add_auto_email_push2():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢 / 公告自動 Email 通知設定 , 新增 Email'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                mrd_8_add_auto_email    = request.form['mrd_8_add_auto_email']   
                
                check_email = db.mrd_8_add_auto_email(mrd_8_add_auto_email)
                
            return render_template('ajax/mrd_8_government_bulletin_add_email.html' , check_email=check_email , email=mrd_8_add_auto_email)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#####################################
# /mrd_8_add_auto_email_push
#####################################
@app.route("/mrd_8_add_auto_email_push" , methods=['POST','GET'])
def mrd_8_add_auto_email_push():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢 / 公告自動 Email 通知設定'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            
            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
                
            return render_template('ajax/mrd_8_government_bulletin.html' , mrd_8_query_announcement_search_res_title=operation_record_title)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 


#####################################
# /mrd_8_query_announcement_submit
#####################################
@app.route("/mrd_8_query_announcement_submit" , methods=['POST','GET'])
def mrd_8_query_announcement_submit():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢 / 衛生福利部食品藥物管理署 公告'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                mrd_8_query_announcement_year    = request.form['mrd_8_query_announcement_year']   
                mrd_8_query_announcement_item    = request.form['mrd_8_query_announcement_item']   
                mrd_8_query_announcement_keyword = request.form['mrd_8_query_announcement_keyword']   

            mrd_8_query_announcement_search_res = db.mrd_8_query_announcement_search_res(mrd_8_query_announcement_year , mrd_8_query_announcement_item , mrd_8_query_announcement_keyword)
            mrd_8_query_announcement_search_res = str(mrd_8_query_announcement_search_res).replace('[' , " ")
            mrd_8_query_announcement_search_res = str(mrd_8_query_announcement_search_res).replace(']' , " ")
            mrd_8_query_announcement_search_res = str(mrd_8_query_announcement_search_res).replace('class="listTable"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_query_announcement_search_res = str(mrd_8_query_announcement_search_res).replace('<a' , '<a target="_blank" ')
            mrd_8_query_announcement_search_res = str(mrd_8_query_announcement_search_res).replace('news' , 'https://www.fda.gov.tw/TC/news')
            mrd_8_query_announcement_search_res = str(mrd_8_query_announcement_search_res).replace('images/icon/new.gif' , 'https://ap1.otsuka.com.tw/static/images/icon/new.gif')
            
            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
                
            return render_template('ajax/mrd_8_query_announcement_search_res.html' , mrd_8_query_announcement_search_res=mrd_8_query_announcement_search_res , mrd_8_query_announcement_search_res_title=operation_record_title)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 


########################################################
# /mrd_8_cosmetic_query_ingredients_prohibited_submit
########################################################
@app.route("/mrd_8_cosmetic_query_ingredients_prohibited_submit" , methods=['POST','GET'])
def mrd_8_cosmetic_query_ingredients_prohibited_submit():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢 / 化粧品禁限用成分管理規定'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                mrd_8_cosmetic_query_ingredients_prohibited_k  = request.form['mrd_8_cosmetic_query_ingredients_prohibited_k']   

            mrd_8_cosmetic_query_ingredients_prohibited_search_res = db.mrd_8_cosmetic_query_ingredients_prohibited_search_res(mrd_8_cosmetic_query_ingredients_prohibited_k)
            mrd_8_cosmetic_query_ingredients_prohibited_search_res = str(mrd_8_cosmetic_query_ingredients_prohibited_search_res).replace('[' , " ")
            mrd_8_cosmetic_query_ingredients_prohibited_search_res = str(mrd_8_cosmetic_query_ingredients_prohibited_search_res).replace(']' , " ")
            mrd_8_cosmetic_query_ingredients_prohibited_search_res = str(mrd_8_cosmetic_query_ingredients_prohibited_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_cosmetic_query_ingredients_prohibited_search_res = str(mrd_8_cosmetic_query_ingredients_prohibited_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_cosmetic_query_ingredients_prohibited_search_res = str(mrd_8_cosmetic_query_ingredients_prohibited_search_res).replace('consumer.fda.gov.tw//Food/consumer.fda.gov.tw/Law/' , 'consumer.fda.gov.tw//Food/')
            mrd_8_cosmetic_query_ingredients_prohibited_search_res = str(mrd_8_cosmetic_query_ingredients_prohibited_search_res).replace('<a' , '<a target="_blank"')
            mrd_8_cosmetic_query_ingredients_prohibited_search_res = str(mrd_8_cosmetic_query_ingredients_prohibited_search_res).replace('/uc/GetFile' , 'https://consumer.fda.gov.tw/uc/GetFile')
            mrd_8_cosmetic_query_ingredients_prohibited_search_res = str(mrd_8_cosmetic_query_ingredients_prohibited_search_res).replace('/Food/Baby' , 'https://consumer.fda.gov.tw/Food/Baby')
            
            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
                
            return render_template('ajax/mrd_8_cosmetic_query_ingredients_prohibited_search_res.html' , mrd_8_cosmetic_query_ingredients_prohibited_search_res=mrd_8_cosmetic_query_ingredients_prohibited_search_res , mrd_8_cosmetic_query_ingredients_prohibited_search_res_title=operation_record_title)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##################################################
# /mrd_8_food_query_infant_formula_submit
##################################################
@app.route("/mrd_8_food_query_infant_formula_submit" , methods=['POST','GET'])
def mrd_8_food_query_infant_formula_submit():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢 / 嬰兒與較大嬰兒配方食品許可資料查詢'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                mrd_8_food_query_infant_formula_ct  = request.form['mrd_8_food_query_infant_formula_ct']    
                mrd_8_food_query_infant_formula_cn  = request.form['mrd_8_food_query_infant_formula_cn']    
                mrd_8_food_query_infant_formula_en  = request.form['mrd_8_food_query_infant_formula_en']    
                mrd_8_food_query_infant_formula_cp  = request.form['mrd_8_food_query_infant_formula_cp']    
                mrd_8_food_query_infant_formula_ph1 = request.form['mrd_8_food_query_infant_formula_ph1']    
                mrd_8_food_query_infant_formula_ph2 = request.form['mrd_8_food_query_infant_formula_ph2']    
                mrd_8_food_query_infant_formula_ph3 = request.form['mrd_8_food_query_infant_formula_ph3']    
                mrd_8_food_query_infant_formula_k   = request.form['mrd_8_food_query_infant_formula_k']    

            mrd_8_food_query_infant_formula_search_res = db.mrd_8_food_query_infant_formula_search_res(mrd_8_food_query_infant_formula_ct , mrd_8_food_query_infant_formula_cn , mrd_8_food_query_infant_formula_en , mrd_8_food_query_infant_formula_cp , mrd_8_food_query_infant_formula_ph1 , mrd_8_food_query_infant_formula_ph2 , mrd_8_food_query_infant_formula_ph3 , mrd_8_food_query_infant_formula_k)
            mrd_8_food_query_infant_formula_search_res = str(mrd_8_food_query_infant_formula_search_res).replace('[' , " ")
            mrd_8_food_query_infant_formula_search_res = str(mrd_8_food_query_infant_formula_search_res).replace(']' , " ")
            mrd_8_food_query_infant_formula_search_res = str(mrd_8_food_query_infant_formula_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_query_infant_formula_search_res = str(mrd_8_food_query_infant_formula_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_query_infant_formula_search_res = str(mrd_8_food_query_infant_formula_search_res).replace('consumer.fda.gov.tw//Food/consumer.fda.gov.tw/Law/' , 'consumer.fda.gov.tw//Food/')
            mrd_8_food_query_infant_formula_search_res = str(mrd_8_food_query_infant_formula_search_res).replace('<a' , '<a target="_blank"')
            mrd_8_food_query_infant_formula_search_res = str(mrd_8_food_query_infant_formula_search_res).replace('/uc/GetFile' , 'https://consumer.fda.gov.tw/uc/GetFile')
            mrd_8_food_query_infant_formula_search_res = str(mrd_8_food_query_infant_formula_search_res).replace('/Food/Baby' , 'https://consumer.fda.gov.tw/Food/Baby')
            
            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
                
            return render_template('ajax/mrd_8_food_query_infant_formula_search_res.html' , mrd_8_food_query_infant_formula_search_res=mrd_8_food_query_infant_formula_search_res , mrd_8_food_query_infant_formula_search_res_title=operation_record_title)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##################################################
# /mrd_8_food_8_all_search_submit
##################################################
@app.route("/mrd_8_food_8_all_search_submit" , methods=['POST','GET'])
def mrd_8_food_8_all_search_submit():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢 / 統一搜尋入口 整合查詢服務'  
        title_1 = 'MRD - 08.政府公開資料庫比對查詢 / 衛生福利部審核通過之基因改造食品原料之查詢'  
        title_2 = 'MRD - 08.政府公開資料庫比對查詢 / 國產維生素類錠狀膠囊狀食品查驗登記證資料查詢'  
        title_3 = 'MRD - 08.政府公開資料庫比對查詢 / 輸入膠囊錠狀食品核備查詢'
        title_4 = 'MRD - 08.政府公開資料庫比對查詢 / 特定疾病配方食品'
        title_5 = 'MRD - 08.政府公開資料庫比對查詢 / 衛生福利部審核通過之健康食品資料查詢'
        title_6 = 'MRD - 08.政府公開資料庫比對查詢 / 食品原料整合查詢平臺'
        title_7 = 'MRD - 08.政府公開資料庫比對查詢 / 食品添加物使用範圍及限量暨規格標準'
        title_8 = 'MRD - 08.政府公開資料庫比對查詢 / 食品添加物許可證資料查詢'
        title_9 = 'MRD - 08.政府公開資料庫比對查詢 / 嬰兒與較大嬰兒配方食品許可資料查詢'

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                mrd_8_food_8_all_search_k  = request.form['mrd_8_food_8_all_search_k']          

            # 衛生福利部審核通過之基因改造食品原料之查詢
            mrd_8_food_query_genetic_modification_all_search_res = db.mrd_8_food_query_genetic_modification_all_search_res(mrd_8_food_8_all_search_k)
            mrd_8_food_query_genetic_modification_all_search_res = str(mrd_8_food_query_genetic_modification_all_search_res).replace('[' , " ")
            mrd_8_food_query_genetic_modification_all_search_res = str(mrd_8_food_query_genetic_modification_all_search_res).replace(']' , " ")
            mrd_8_food_query_genetic_modification_all_search_res = str(mrd_8_food_query_genetic_modification_all_search_res).replace('class="rwd-table tdbreakall"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_query_genetic_modification_all_search_res = str(mrd_8_food_query_genetic_modification_all_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_query_genetic_modification_all_search_res = str(mrd_8_food_query_genetic_modification_all_search_res).replace('consumer.fda.gov.tw//Food/consumer.fda.gov.tw/Law/' , 'consumer.fda.gov.tw//Food/')
            mrd_8_food_query_genetic_modification_all_search_res = str(mrd_8_food_query_genetic_modification_all_search_res).replace('<a' , '<a target="_blank"')
            mrd_8_food_query_genetic_modification_all_search_res = str(mrd_8_food_query_genetic_modification_all_search_res).replace('href="/Food' , 'href="consumer.fda.gov.tw/Food')
            
            # 國產維生素類錠狀膠囊狀食品查驗登記證資料查詢
            mrd_8_food_query_domestic_vitamins_all_search_res = db.mrd_8_food_query_domestic_vitamins_all_search_res(mrd_8_food_8_all_search_k)
            mrd_8_food_query_domestic_vitamins_all_search_res = str(mrd_8_food_query_domestic_vitamins_all_search_res).replace('[' , " ")
            mrd_8_food_query_domestic_vitamins_all_search_res = str(mrd_8_food_query_domestic_vitamins_all_search_res).replace(']' , " ")
            mrd_8_food_query_domestic_vitamins_all_search_res = str(mrd_8_food_query_domestic_vitamins_all_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_query_domestic_vitamins_all_search_res = str(mrd_8_food_query_domestic_vitamins_all_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_query_domestic_vitamins_all_search_res = str(mrd_8_food_query_domestic_vitamins_all_search_res).replace('consumer.fda.gov.tw//Food/consumer.fda.gov.tw/Law/' , 'consumer.fda.gov.tw//Food/')
            mrd_8_food_query_domestic_vitamins_all_search_res = str(mrd_8_food_query_domestic_vitamins_all_search_res).replace('<a' , '<a target="_blank"')
            mrd_8_food_query_domestic_vitamins_all_search_res = str(mrd_8_food_query_domestic_vitamins_all_search_res).replace('/Food' , 'https://consumer.fda.gov.tw/Food')

            # 輸入膠囊錠狀食品核備查詢
            mrd_8_food_query_enter_capsule_all_search_res = db.mrd_8_food_query_enter_capsule_all_search_res(mrd_8_food_8_all_search_k)
            mrd_8_food_query_enter_capsule_all_search_res = str(mrd_8_food_query_enter_capsule_all_search_res).replace('[' , " ")
            mrd_8_food_query_enter_capsule_all_search_res = str(mrd_8_food_query_enter_capsule_all_search_res).replace(']' , " ")
            mrd_8_food_query_enter_capsule_all_search_res = str(mrd_8_food_query_enter_capsule_all_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_query_enter_capsule_all_search_res = str(mrd_8_food_query_enter_capsule_all_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_query_enter_capsule_all_search_res = str(mrd_8_food_query_enter_capsule_all_search_res).replace('consumer.fda.gov.tw//Food/consumer.fda.gov.tw/Law/' , 'consumer.fda.gov.tw//Food/')
            mrd_8_food_query_enter_capsule_all_search_res = str(mrd_8_food_query_enter_capsule_all_search_res).replace('<a' , '<a target="_blank"')
            mrd_8_food_query_enter_capsule_all_search_res = str(mrd_8_food_query_enter_capsule_all_search_res).replace('CapsuleAudit' , 'https://consumer.fda.gov.tw/Food/CapsuleAudit')

            # 特定疾病配方食品
            mrd_8_food_query_disease_recipe_all_search_res = db.mrd_8_food_query_disease_recipe_all_search_res(mrd_8_food_8_all_search_k)
            mrd_8_food_query_disease_recipe_all_search_res = str(mrd_8_food_query_disease_recipe_all_search_res).replace('[' , " ")
            mrd_8_food_query_disease_recipe_all_search_res = str(mrd_8_food_query_disease_recipe_all_search_res).replace(']' , " ")
            mrd_8_food_query_disease_recipe_all_search_res = str(mrd_8_food_query_disease_recipe_all_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_query_disease_recipe_all_search_res = str(mrd_8_food_query_disease_recipe_all_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_query_disease_recipe_all_search_res = str(mrd_8_food_query_disease_recipe_all_search_res).replace('consumer.fda.gov.tw//Food/consumer.fda.gov.tw/Law/' , 'consumer.fda.gov.tw//Food/')
            mrd_8_food_query_disease_recipe_all_search_res = str(mrd_8_food_query_disease_recipe_all_search_res).replace('<a' , '<a target="_blank"')
            mrd_8_food_query_disease_recipe_all_search_res = str(mrd_8_food_query_disease_recipe_all_search_res).replace('SpecialFood' , 'https://consumer.fda.gov.tw/Food/SpecialFood')

            # 衛生福利部審核通過之健康食品資料查詢
            mrd_8_food_query_pass_all_search_res = db.mrd_8_food_query_pass_all_search_res(mrd_8_food_8_all_search_k)
            mrd_8_food_query_pass_all_search_res = str(mrd_8_food_query_pass_all_search_res).replace('[' , " ")
            mrd_8_food_query_pass_all_search_res = str(mrd_8_food_query_pass_all_search_res).replace(']' , " ")
            mrd_8_food_query_pass_all_search_res = str(mrd_8_food_query_pass_all_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_query_pass_all_search_res = str(mrd_8_food_query_pass_all_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_query_pass_all_search_res = str(mrd_8_food_query_pass_all_search_res).replace('<a' , '<a target="_blank"')

            # 食品原料整合查詢平臺
            mrd_8_food_query_platform_all_search_res = db.mrd_8_food_query_platform_all_search_res(mrd_8_food_8_all_search_k)
            mrd_8_food_query_platform_all_search_res = str(mrd_8_food_query_platform_all_search_res).replace('[' , " ")
            mrd_8_food_query_platform_all_search_res = str(mrd_8_food_query_platform_all_search_res).replace(']' , " ")
            mrd_8_food_query_platform_all_search_res = str(mrd_8_food_query_platform_all_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_query_platform_all_search_res = str(mrd_8_food_query_platform_all_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_query_platform_all_search_res = str(mrd_8_food_query_platform_all_search_res).replace('consumer.fda.gov.tw//Food/consumer.fda.gov.tw/Law/' , 'https://consumer.fda.gov.tw//Food/')
            mrd_8_food_query_platform_all_search_res = str(mrd_8_food_query_platform_all_search_res).replace('<a' , '<a target="_blank"')

            # 食品添加物使用範圍及限量暨規格標準
            mrd_8_food_all_search_res = db.mrd_8_food_all_search_res(mrd_8_food_8_all_search_k)
            mrd_8_food_all_search_res = str(mrd_8_food_all_search_res).replace('[' , " ")
            mrd_8_food_all_search_res = str(mrd_8_food_all_search_res).replace(']' , " ")
            mrd_8_food_all_search_res = str(mrd_8_food_all_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_all_search_res = str(mrd_8_food_all_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_all_search_res = str(mrd_8_food_all_search_res).replace('Food' , 'https://consumer.fda.gov.tw/Law/Food')
            mrd_8_food_all_search_res = str(mrd_8_food_all_search_res).replace('/uc' , 'https://consumer.fda.gov.tw/uc')
            mrd_8_food_all_search_res = str(mrd_8_food_all_search_res).replace('tw//' , 'tw/')
            mrd_8_food_all_search_res = str(mrd_8_food_all_search_res).replace('tw///' , 'tw/')
            mrd_8_food_all_search_res = str(mrd_8_food_all_search_res).replace('<a' , '<a target="_blank"')

            # 食品添加物許可證資料查詢
            mrd_8_license_all_search_res = db.mrd_8_license_all_search_res(mrd_8_food_8_all_search_k)
            mrd_8_license_all_search_res = str(mrd_8_license_all_search_res).replace('[' , " ")
            mrd_8_license_all_search_res = str(mrd_8_license_all_search_res).replace(']' , " ")
            mrd_8_license_all_search_res = str(mrd_8_license_all_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_license_all_search_res = str(mrd_8_license_all_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_license_all_search_res = str(mrd_8_license_all_search_res).replace('/Food/Food' , 'https://consumer.fda.gov.tw/Food/Food')

            # 嬰兒與較大嬰兒配方食品許可資料查詢
            mrd_8_food_query_infant_formula_all_search_res = db.mrd_8_food_query_infant_formula_all_search_res(mrd_8_food_8_all_search_k)
            mrd_8_food_query_infant_formula_all_search_res = str(mrd_8_food_query_infant_formula_all_search_res).replace('[' , " ")
            mrd_8_food_query_infant_formula_all_search_res = str(mrd_8_food_query_infant_formula_all_search_res).replace(']' , " ")
            mrd_8_food_query_infant_formula_all_search_res = str(mrd_8_food_query_infant_formula_all_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_query_infant_formula_all_search_res = str(mrd_8_food_query_infant_formula_all_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_query_infant_formula_all_search_res = str(mrd_8_food_query_infant_formula_all_search_res).replace('consumer.fda.gov.tw//Food/consumer.fda.gov.tw/Law/' , 'consumer.fda.gov.tw//Food/')
            mrd_8_food_query_infant_formula_all_search_res = str(mrd_8_food_query_infant_formula_all_search_res).replace('<a' , '<a target="_blank"')
            mrd_8_food_query_infant_formula_all_search_res = str(mrd_8_food_query_infant_formula_all_search_res).replace('/uc/GetFile' , 'https://consumer.fda.gov.tw/uc/GetFile')
            mrd_8_food_query_infant_formula_all_search_res = str(mrd_8_food_query_infant_formula_all_search_res).replace('/Food/Baby' , 'https://consumer.fda.gov.tw/Food/Baby')


            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
                
            return render_template('ajax/mrd_8_food_8_all_search_res.html' , 
                                   mrd_8_food_query_genetic_modification_all_search_res = mrd_8_food_query_genetic_modification_all_search_res , 
                                   mrd_8_food_query_genetic_modification_all_search_res_title = title_1 , 
                                   mrd_8_food_query_domestic_vitamins_all_search_res = mrd_8_food_query_domestic_vitamins_all_search_res ,
                                   mrd_8_food_query_domestic_vitamins_all_search_res_title = title_2 , 
                                   mrd_8_food_query_enter_capsule_all_search_res = mrd_8_food_query_enter_capsule_all_search_res , 
                                   mrd_8_food_query_enter_capsule_all_search_res_title = title_3 ,
                                   mrd_8_food_query_disease_recipe_all_search_res = mrd_8_food_query_disease_recipe_all_search_res , 
                                   mrd_8_food_query_disease_recipe_all_search_res_title = title_4 , 
                                   mrd_8_food_query_pass_all_search_res = mrd_8_food_query_pass_all_search_res , 
                                   mrd_8_food_query_pass_all_search_res_title = title_5 , 
                                   mrd_8_food_query_platform_all_search_res = mrd_8_food_query_platform_all_search_res , 
                                   mrd_8_food_query_platform_all_search_res_title = title_6 , 
                                   mrd_8_food_all_search_res = mrd_8_food_all_search_res , 
                                   mrd_8_food_all_search_res_title = title_7 ,
                                   mrd_8_license_all_search_res = mrd_8_license_all_search_res , 
                                   mrd_8_license_all_search_res_title = title_8 , 
                                   mrd_8_food_query_infant_formula_all_search_res = mrd_8_food_query_infant_formula_all_search_res , 
                                   mrd_8_food_query_infant_formula_all_search_res_title = title_9
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 


##################################################
# /mrd_8_food_query_genetic_modification_submit
##################################################
@app.route("/mrd_8_food_query_genetic_modification_submit" , methods=['POST','GET'])
def mrd_8_food_query_genetic_modification_submit():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢 / 衛生福利部審核通過之基因改造食品原料之查詢'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                mrd_8_food_query_genetic_modification_t  = request.form['mrd_8_food_query_genetic_modification_t']          
                mrd_8_food_query_genetic_modification_t2 = request.form['mrd_8_food_query_genetic_modification_t2']          
                mrd_8_food_query_genetic_modification_pn = request.form['mrd_8_food_query_genetic_modification_pn']          
                mrd_8_food_query_genetic_modification_an = request.form['mrd_8_food_query_genetic_modification_an']          
                mrd_8_food_query_genetic_modification_sd = request.form['mrd_8_food_query_genetic_modification_sd']          
                mrd_8_food_query_genetic_modification_ed = request.form['mrd_8_food_query_genetic_modification_ed']          
                mrd_8_food_query_genetic_modification_k  = request.form['mrd_8_food_query_genetic_modification_k']   

            mrd_8_food_query_genetic_modification_search_res = db.mrd_8_food_query_genetic_modification_search_res(mrd_8_food_query_genetic_modification_t , mrd_8_food_query_genetic_modification_t2 , mrd_8_food_query_genetic_modification_pn , mrd_8_food_query_genetic_modification_an , mrd_8_food_query_genetic_modification_sd , mrd_8_food_query_genetic_modification_ed , mrd_8_food_query_genetic_modification_k)
            mrd_8_food_query_genetic_modification_search_res = str(mrd_8_food_query_genetic_modification_search_res).replace('[' , " ")
            mrd_8_food_query_genetic_modification_search_res = str(mrd_8_food_query_genetic_modification_search_res).replace(']' , " ")
            mrd_8_food_query_genetic_modification_search_res = str(mrd_8_food_query_genetic_modification_search_res).replace('class="rwd-table tdbreakall"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_query_genetic_modification_search_res = str(mrd_8_food_query_genetic_modification_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_query_genetic_modification_search_res = str(mrd_8_food_query_genetic_modification_search_res).replace('consumer.fda.gov.tw//Food/consumer.fda.gov.tw/Law/' , 'consumer.fda.gov.tw//Food/')
            mrd_8_food_query_genetic_modification_search_res = str(mrd_8_food_query_genetic_modification_search_res).replace('<a' , '<a target="_blank"')
            mrd_8_food_query_genetic_modification_search_res = str(mrd_8_food_query_genetic_modification_search_res).replace('href="/Food' , 'href="consumer.fda.gov.tw/Food')
            
            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
                
            return render_template('ajax/mrd_8_food_query_genetic_modification_search_res.html' , mrd_8_food_query_genetic_modification_search_res=mrd_8_food_query_genetic_modification_search_res , mrd_8_food_query_genetic_modification_search_res_title=operation_record_title)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 



###############################################
# /mrd_8_food_query_domestic_vitamins_submit
###############################################
@app.route("/mrd_8_food_query_domestic_vitamins_submit" , methods=['POST','GET'])
def mrd_8_food_query_domestic_vitamins_submit():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢 / 國產維生素類錠狀膠囊狀食品查驗登記證資料查詢'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                mrd_8_food_query_domestic_vitamins_ct  = request.form['mrd_8_food_query_domestic_vitamins_ct']          
                mrd_8_food_query_domestic_vitamins_cn  = request.form['mrd_8_food_query_domestic_vitamins_cn']          
                mrd_8_food_query_domestic_vitamins_en  = request.form['mrd_8_food_query_domestic_vitamins_en']          
                mrd_8_food_query_domestic_vitamins_cp  = request.form['mrd_8_food_query_domestic_vitamins_cp']          
                mrd_8_food_query_domestic_vitamins_ph1 = request.form['mrd_8_food_query_domestic_vitamins_ph1']          
                mrd_8_food_query_domestic_vitamins_ph2 = request.form['mrd_8_food_query_domestic_vitamins_ph2']          
                mrd_8_food_query_domestic_vitamins_ph3 = request.form['mrd_8_food_query_domestic_vitamins_ph3']          
                mrd_8_food_query_domestic_vitamins_k   = request.form['mrd_8_food_query_domestic_vitamins_k']          
                

            mrd_8_food_query_domestic_vitamins_search_res = db.mrd_8_food_query_domestic_vitamins_search_res(mrd_8_food_query_domestic_vitamins_ct , mrd_8_food_query_domestic_vitamins_cn , mrd_8_food_query_domestic_vitamins_en , mrd_8_food_query_domestic_vitamins_cp , mrd_8_food_query_domestic_vitamins_ph1 , mrd_8_food_query_domestic_vitamins_ph2 , mrd_8_food_query_domestic_vitamins_ph3 , mrd_8_food_query_domestic_vitamins_k)
            mrd_8_food_query_domestic_vitamins_search_res = str(mrd_8_food_query_domestic_vitamins_search_res).replace('[' , " ")
            mrd_8_food_query_domestic_vitamins_search_res = str(mrd_8_food_query_domestic_vitamins_search_res).replace(']' , " ")
            mrd_8_food_query_domestic_vitamins_search_res = str(mrd_8_food_query_domestic_vitamins_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_query_domestic_vitamins_search_res = str(mrd_8_food_query_domestic_vitamins_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_query_domestic_vitamins_search_res = str(mrd_8_food_query_domestic_vitamins_search_res).replace('consumer.fda.gov.tw//Food/consumer.fda.gov.tw/Law/' , 'consumer.fda.gov.tw//Food/')
            mrd_8_food_query_domestic_vitamins_search_res = str(mrd_8_food_query_domestic_vitamins_search_res).replace('<a' , '<a target="_blank"')
            mrd_8_food_query_domestic_vitamins_search_res = str(mrd_8_food_query_domestic_vitamins_search_res).replace('/Food' , 'https://consumer.fda.gov.tw/Food')
            
            
            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)

            return render_template('ajax/mrd_8_food_query_domestic_vitamins_search_res.html' , mrd_8_food_query_domestic_vitamins_search_res=mrd_8_food_query_domestic_vitamins_search_res , mrd_8_food_query_domestic_vitamins_search_res_title=operation_record_title)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 


############################################
# /mrd_8_food_query_enter_capsule_submit
############################################
@app.route("/mrd_8_food_query_enter_capsule_submit" , methods=['POST','GET'])
def mrd_8_food_query_enter_capsule_submit():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢 / 輸入膠囊錠狀食品核備查詢'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                mrd_8_food_query_enter_capsule_ct  = request.form['mrd_8_food_query_enter_capsule_ct']          
                mrd_8_food_query_enter_capsule_cn  = request.form['mrd_8_food_query_enter_capsule_cn']          
                mrd_8_food_query_enter_capsule_en  = request.form['mrd_8_food_query_enter_capsule_en']          
                mrd_8_food_query_enter_capsule_cp  = request.form['mrd_8_food_query_enter_capsule_cp']          
                mrd_8_food_query_enter_capsule_ph1 = request.form['mrd_8_food_query_enter_capsule_ph1']          
                mrd_8_food_query_enter_capsule_ph2 = request.form['mrd_8_food_query_enter_capsule_ph2']          
                mrd_8_food_query_enter_capsule_ph3 = request.form['mrd_8_food_query_enter_capsule_ph3']          
                mrd_8_food_query_enter_capsule_k   = request.form['mrd_8_food_query_enter_capsule_k']          
                

            mrd_8_food_query_enter_capsule_search_res = db.mrd_8_food_query_enter_capsule_search_res(mrd_8_food_query_enter_capsule_ct , mrd_8_food_query_enter_capsule_cn , mrd_8_food_query_enter_capsule_en , mrd_8_food_query_enter_capsule_cp , mrd_8_food_query_enter_capsule_ph1 , mrd_8_food_query_enter_capsule_ph2 , mrd_8_food_query_enter_capsule_ph3 , mrd_8_food_query_enter_capsule_k)
            mrd_8_food_query_enter_capsule_search_res = str(mrd_8_food_query_enter_capsule_search_res).replace('[' , " ")
            mrd_8_food_query_enter_capsule_search_res = str(mrd_8_food_query_enter_capsule_search_res).replace(']' , " ")
            mrd_8_food_query_enter_capsule_search_res = str(mrd_8_food_query_enter_capsule_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_query_enter_capsule_search_res = str(mrd_8_food_query_enter_capsule_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_query_enter_capsule_search_res = str(mrd_8_food_query_enter_capsule_search_res).replace('consumer.fda.gov.tw//Food/consumer.fda.gov.tw/Law/' , 'consumer.fda.gov.tw//Food/')
            mrd_8_food_query_enter_capsule_search_res = str(mrd_8_food_query_enter_capsule_search_res).replace('<a' , '<a target="_blank"')
            mrd_8_food_query_enter_capsule_search_res = str(mrd_8_food_query_enter_capsule_search_res).replace('CapsuleAudit' , 'https://consumer.fda.gov.tw/Food/CapsuleAudit')
            
            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
                
            return render_template('ajax/mrd_8_food_query_enter_capsule_search_res.html' , mrd_8_food_query_enter_capsule_search_res=mrd_8_food_query_enter_capsule_search_res , mrd_8_food_query_enter_capsule_search_res_title=operation_record_title)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 


############################################
# /mrd_8_food_query_disease_recipe_submit
############################################
@app.route("/mrd_8_food_query_disease_recipe_submit" , methods=['POST','GET'])
def mrd_8_food_query_disease_recipe_submit():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢 / 特定疾病配方食品'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                mrd_8_food_query_disease_recipe_t   = request.form['mrd_8_food_query_disease_recipe_t']          
                mrd_8_food_query_disease_recipe_ct  = request.form['mrd_8_food_query_disease_recipe_ct']          
                mrd_8_food_query_disease_recipe_cn  = request.form['mrd_8_food_query_disease_recipe_cn']          
                mrd_8_food_query_disease_recipe_en  = request.form['mrd_8_food_query_disease_recipe_en']          
                mrd_8_food_query_disease_recipe_cp  = request.form['mrd_8_food_query_disease_recipe_cp']          
                mrd_8_food_query_disease_recipe_ph1 = request.form['mrd_8_food_query_disease_recipe_ph1']          
                mrd_8_food_query_disease_recipe_ph2 = request.form['mrd_8_food_query_disease_recipe_ph2']          
                mrd_8_food_query_disease_recipe_ph3 = request.form['mrd_8_food_query_disease_recipe_ph3']          
                mrd_8_food_query_disease_recipe_k   = request.form['mrd_8_food_query_disease_recipe_k']          
                
            
            mrd_8_food_query_disease_recipe_search_res = db.mrd_8_food_query_disease_recipe_search_res(mrd_8_food_query_disease_recipe_t , mrd_8_food_query_disease_recipe_ct , mrd_8_food_query_disease_recipe_cn , mrd_8_food_query_disease_recipe_en , mrd_8_food_query_disease_recipe_cp , mrd_8_food_query_disease_recipe_ph1 , mrd_8_food_query_disease_recipe_ph2 , mrd_8_food_query_disease_recipe_ph3 , mrd_8_food_query_disease_recipe_k)
            mrd_8_food_query_disease_recipe_search_res = str(mrd_8_food_query_disease_recipe_search_res).replace('[' , " ")
            mrd_8_food_query_disease_recipe_search_res = str(mrd_8_food_query_disease_recipe_search_res).replace(']' , " ")
            mrd_8_food_query_disease_recipe_search_res = str(mrd_8_food_query_disease_recipe_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_query_disease_recipe_search_res = str(mrd_8_food_query_disease_recipe_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_query_disease_recipe_search_res = str(mrd_8_food_query_disease_recipe_search_res).replace('consumer.fda.gov.tw//Food/consumer.fda.gov.tw/Law/' , 'consumer.fda.gov.tw//Food/')
            mrd_8_food_query_disease_recipe_search_res = str(mrd_8_food_query_disease_recipe_search_res).replace('<a' , '<a target="_blank"')
            mrd_8_food_query_disease_recipe_search_res = str(mrd_8_food_query_disease_recipe_search_res).replace('SpecialFood' , 'https://consumer.fda.gov.tw/Food/SpecialFood')
            
            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
                
            return render_template('ajax/mrd_8_food_query_disease_recipe_search_res.html' , mrd_8_food_query_disease_recipe_search_res=mrd_8_food_query_disease_recipe_search_res , mrd_8_food_query_disease_recipe_title=operation_record_title)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

########################################
# /mrd_8_food_query_pass_submit
########################################
@app.route("/mrd_8_food_query_pass_submit" , methods=['POST','GET'])
def mrd_8_food_query_pass_submit():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢 / 衛生福利部審核通過之健康食品資料查詢'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                mrd_8_food_query_pass_t   = request.form['mrd_8_food_query_pass_t']          
                mrd_8_food_query_pass_Tid = request.form['mrd_8_food_query_pass_Tid']          
                mrd_8_food_query_pass_Cop = request.form['mrd_8_food_query_pass_Cop']          
                mrd_8_food_query_pass_Cna = request.form['mrd_8_food_query_pass_Cna']          
                mrd_8_food_query_pass_t2  = request.form['mrd_8_food_query_pass_t2']          
                mrd_8_food_query_pass_k   = request.form['mrd_8_food_query_pass_k']          
                

            mrd_8_food_query_pass_search_res = db.mrd_8_food_query_pass_search_res(mrd_8_food_query_pass_t , mrd_8_food_query_pass_Tid , mrd_8_food_query_pass_Cop , mrd_8_food_query_pass_Cna , mrd_8_food_query_pass_t2 , mrd_8_food_query_pass_k)
            mrd_8_food_query_pass_search_res = str(mrd_8_food_query_pass_search_res).replace('[' , " ")
            mrd_8_food_query_pass_search_res = str(mrd_8_food_query_pass_search_res).replace(']' , " ")
            mrd_8_food_query_pass_search_res = str(mrd_8_food_query_pass_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_query_pass_search_res = str(mrd_8_food_query_pass_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_query_pass_search_res = str(mrd_8_food_query_pass_search_res).replace('<a' , '<a target="_blank"')
            
            
            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
                
            return render_template('ajax/mrd_8_food_query_pass_submit_search.html' , mrd_8_food_query_pass_search_res=mrd_8_food_query_pass_search_res , mrd_8_food_query_pass_title=operation_record_title)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

########################################
# /mrd_8_food_query_platform_submit
########################################
@app.route("/mrd_8_food_query_platform_submit" , methods=['POST','GET'])
def mrd_8_food_query_platform_submit():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢 / 食品原料整合查詢平臺'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                mrd_8_food_query_platform_c     = request.form['mrd_8_food_query_platform_c']
                mrd_8_food_query_platform_t     = request.form['mrd_8_food_query_platform_t']     
                mrd_8_food_query_platform_k     = request.form['mrd_8_food_query_platform_k']          
                

            mrd_8_food_query_platform_search_res = db.mrd_8_food_query_platform_search_res(mrd_8_food_query_platform_c , mrd_8_food_query_platform_t , mrd_8_food_query_platform_k)
            mrd_8_food_query_platform_search_res = str(mrd_8_food_query_platform_search_res).replace('[' , " ")
            mrd_8_food_query_platform_search_res = str(mrd_8_food_query_platform_search_res).replace(']' , " ")
            mrd_8_food_query_platform_search_res = str(mrd_8_food_query_platform_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_query_platform_search_res = str(mrd_8_food_query_platform_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_query_platform_search_res = str(mrd_8_food_query_platform_search_res).replace('consumer.fda.gov.tw//Food/consumer.fda.gov.tw/Law/' , 'https://consumer.fda.gov.tw//Food/')
            mrd_8_food_query_platform_search_res = str(mrd_8_food_query_platform_search_res).replace('<a' , '<a target="_blank"')
            
            
            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
                
            return render_template('ajax/mrd_8_food_query_platform_submit_search.html' , mrd_8_food_query_platform_search_res=mrd_8_food_query_platform_search_res , mrd_8_food_query_platform_title=operation_record_title)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

########################################
# /mrd_8_license_submit
########################################
@app.route("/mrd_8_license_submit" , methods=['POST','GET'])
def mrd_8_license_submit():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢 / 食品添加物許可證資料查詢'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                mrd_8_license_ct     = request.form['mrd_8_license_ct']     
                mrd_8_license_cn     = request.form['mrd_8_license_cn']     
                mrd_8_license_en     = request.form['mrd_8_license_en']     
                mrd_8_license_cp     = request.form['mrd_8_license_cp']
                mrd_8_license_ph1    = request.form['mrd_8_license_ph1']     
                mrd_8_license_ph2    = request.form['mrd_8_license_ph2']     
                mrd_8_license_ph3    = request.form['mrd_8_license_ph3']     
                mrd_8_license_k      = request.form['mrd_8_license_k']          

            mrd_8_license_search_res = db.mrd_8_license_search_res(mrd_8_license_ct , mrd_8_license_cn , mrd_8_license_en , mrd_8_license_cp , mrd_8_license_ph1 , mrd_8_license_ph2 , mrd_8_license_ph3 , mrd_8_license_k)
            mrd_8_license_search_res = str(mrd_8_license_search_res).replace('[' , " ")
            mrd_8_license_search_res = str(mrd_8_license_search_res).replace(']' , " ")
            mrd_8_license_search_res = str(mrd_8_license_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_license_search_res = str(mrd_8_license_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_license_search_res = str(mrd_8_license_search_res).replace('/Food/Food' , 'https://consumer.fda.gov.tw/Food/Food')
            
            
            mrd_8_license_search_res = str(mrd_8_license_search_res).replace('<a' , '<a target="_blank"')
            
            
            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
                
            return render_template('ajax/mrd_8_license_submit_search.html' , mrd_8_license_search_res=mrd_8_license_search_res , mrd_8_license_title=operation_record_title)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

########################################
# /mrd_8_food_submit
########################################
@app.route("/mrd_8_food_submit" , methods=['POST','GET'])
def mrd_8_food_submit():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢 / 食品添加物使用範圍及限量暨規格標準'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                mrd_8_food_t      = request.form['mrd_8_food_t']     
                mrd_8_food_k      = request.form['mrd_8_food_k']    

            mrd_8_food_search_res = db.mrd_8_food_search_res(mrd_8_food_t , mrd_8_food_k)
            mrd_8_food_search_res = str(mrd_8_food_search_res).replace('[' , " ")
            mrd_8_food_search_res = str(mrd_8_food_search_res).replace(']' , " ")
            mrd_8_food_search_res = str(mrd_8_food_search_res).replace('class="rwd-table"' , 'class="table table-bordered table-striped table-hover"')
            mrd_8_food_search_res = str(mrd_8_food_search_res).replace('class="page"' , 'class="text-center"')
            mrd_8_food_search_res = str(mrd_8_food_search_res).replace('Food' , 'https://consumer.fda.gov.tw/Law/Food')
            mrd_8_food_search_res = str(mrd_8_food_search_res).replace('/uc' , 'https://consumer.fda.gov.tw/uc')
            mrd_8_food_search_res = str(mrd_8_food_search_res).replace('tw//' , 'tw/')
            mrd_8_food_search_res = str(mrd_8_food_search_res).replace('tw///' , 'tw/')
            mrd_8_food_search_res = str(mrd_8_food_search_res).replace('<a' , '<a target="_blank"')
            
            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
                
            return render_template('ajax/mrd_8_food_submit_search.html' , mrd_8_food_search_res=mrd_8_food_search_res , mrd_8_food_title=operation_record_title)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))  

########################################
# /otsuka_mrd_8
########################################
@app.route("/otsuka_mrd_8" , methods=['POST','GET'])
def otsuka_mrd_8():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'MRD - 08.政府公開資料庫比對查詢'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### mrd 8 announcement search url
            mrd_8_announcement_1_url = parameter.mrd_8['衛生福利部食品藥物管理署公告']
            mrd_8_announcement_2_url = parameter.mrd_8['台灣藥物法規資訊網']

            ### mrd 8 product search url
            mrd_8_product_1_url = parameter.mrd_8['商標檢索系統']
            
            ### mrd 8 cosmetic search url
            mrd_8_cosmetic_1_url = parameter.mrd_8['化粧品禁限用成分管理規定']

            ### mrd 8 food search url
            mrd_8_food_8_all_search = parameter.mrd_8['整合查詢服務']
            mrd_8_food_9_url  = parameter.mrd_8['嬰兒與較大嬰兒配方食品許可資料查詢']
            mrd_8_food_8_url  = parameter.mrd_8['衛生福利部審核通過之基因改造食品原料之查詢']
            mrd_8_food_7_url  = parameter.mrd_8['國產維生素類錠狀膠囊狀食品查驗登記證資料查詢']
            mrd_8_food_6_url  = parameter.mrd_8['輸入膠囊錠狀食品核備查詢']
            mrd_8_food_5_url  = parameter.mrd_8['特定疾病配方食品']
            mrd_8_food_4_url  = parameter.mrd_8['衛生福利部審核通過之健康食品資料查詢']
            mrd_8_food_3_url  = parameter.mrd_8['食品原料整合查詢平臺']
            mrd_8_food_2_url  = parameter.mrd_8['食品添加物許可證資料查詢']
            mrd_8_food_1_url  = parameter.mrd_8['食品添加物使用範圍及限量暨規格標準']

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
                
            return render_template('otsuka_mrd_8.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , r_date=r_date , dep_id=dep_name , 
                                   updep_name=updep_name , mrd_8_food_3_url=mrd_8_food_3_url , mrd_8_food_2_url=mrd_8_food_2_url , mrd_8_food_1_url=mrd_8_food_1_url ,
                                   mrd_8_food_4_url=mrd_8_food_4_url , mrd_8_food_5_url=mrd_8_food_5_url , mrd_8_food_6_url=mrd_8_food_6_url , mrd_8_food_7_url=mrd_8_food_7_url , 
                                   mrd_8_food_8_url=mrd_8_food_8_url , mrd_8_food_9_url=mrd_8_food_9_url , mrd_8_cosmetic_1_url=mrd_8_cosmetic_1_url , mrd_8_product_1_url=mrd_8_product_1_url ,
                                   mrd_8_announcement_1_url=mrd_8_announcement_1_url , mrd_8_announcement_2_url=mrd_8_announcement_2_url 
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))  

########################################
# /reload_it_annual_budget_year_total
########################################
@app.route("/reload_it_annual_budget_year_total" , methods=['POST','GET'])
def reload_it_annual_budget_year_total():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'reload IT 年度預算表總計'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                ### reload IT 年度預算表總計
                reload_it_annual_budget_year_total = db.it_annual_budget_year_total()
                
                return render_template('ajax/reload_it_annual_budget_year_total.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , r_date=r_date , dep_id=dep_id , reload_it_annual_budget_year_total=reload_it_annual_budget_year_total)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))  

####################################
# /load_annual_budget_year_detail
####################################
@app.route("/load_annual_budget_year_detail" , methods=['POST','GET'])
def load_annual_budget_year_detail():
    if 'user' in session:
        
        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################

            if request.method == 'POST':

                l_year      = request.form['year']     

                ### operation record title
                operation_record_title = f'載入 IT {l_year} 年度預算詳細資料'  
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)     
                
                it_annual_budget_year_kind_total        = db.it_annual_budget_year_total_by_kind(l_year) # 依照種類統計
                #it_annual_budget_kind_use_cost          = db.it_annual_budget_year_total_by_kind_use_cost(l_year) # 依照種類使用統計
                #it_annual_budget_kind_use_cost          = db.it_annual_budget_year_total_by_kind_use_cost(l_year) # 依照種類使用統計
                it_annual_budget_kind_remaining_cost    = db.it_annual_budget_year_total_by_kind_remaining_cost(l_year) ## 依照種類剩餘費用

                return render_template('ajax/load_annual_budget_year_detail.html' ,
                                       it_annual_budget_year_kind_total=it_annual_budget_year_kind_total,
                                       it_annual_budget_kind_remaining_cost=it_annual_budget_kind_remaining_cost)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#############################
# /otsuka_it_annual_budget
#############################
@app.route("/otsuka_it_annual_budget")
def otsuka_it_annual_budget():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'IT 年度預算'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### IT 年度預算清單
            it_annual_budget_select_kind            = db.it_annual_budget_kind_list() # 種類清單
            it_annual_budget_select_otsuka_holdings = db.it_annual_budget_otsuka_holdings_list() # otsuka_holdings 清單
            it_annual_budget_year_total             = db.it_annual_budget_year_total() # 年度總計

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)

            return render_template('it_annual_budget.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name , it_annual_budget_select_kind=it_annual_budget_select_kind , 
                                   it_annual_budget_select_otsuka_holdings=it_annual_budget_select_otsuka_holdings ,
                                   it_annual_budget_year_total=it_annual_budget_year_total )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))    


##########################
# /show_query_device
##########################
@app.route("/show_query_device" , methods=['GET','POST'])
def show_query_device():
        
    ### operation record title
    operation_record_title = '固資查詢清單'    

    ### session 
    user = session['user']
    lv   = session['lv']
    login_code = session['login_code']
    
    ### r_time
    r_date  = time.strftime("%Y-%m-%d" , time.localtime())
    r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
    r_year  = time.strftime("%Y" , time.localtime())
    r_month = time.strftime("%m" , time.localtime())

    ### operation record
    db.operation_record(r_time,user,login_code,operation_record_title)    
    
    #################
    # main content 
    #################

    ### 固資清單
    if request.method == 'POST':
        
        query_device_no  = request.form['query_device_no']
    
    device_list = db.erp_query_device(query_device_no)

    ### department name & updepartment name
    dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
    updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
    updep_name         = db.bpm_account_up_department(updep_id)
    
    
    return render_template('ajax/show_query_device.html' , device_list=device_list , dep_id=dep_name , updep_name=updep_name)

#####################################
# /load_hr_360_query_data_name2
#####################################
@app.route("/load_hr_360_query_data_name2", methods=['GET','POST'])
def load_hr_360_query_data_name2():
    
    if 'user' in session:
        
        

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record title
            operation_record_title = '載入 - HR 360 部門人員清單'    

            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            
            if request.method == 'POST':
                
                h_3_m_dep = request.form['h_3_m_dep']

                h_3_m_dep_member_list = db.HR_360_department_query_member(h_3_m_dep)
            
                return render_template('ajax/load_hr_360_dep_member_list1_2.html' , 
                                       h_3_m_dep_member_list=h_3_m_dep_member_list
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

#####################################
# /load_hr_360_query_data_name
#####################################
@app.route("/load_hr_360_query_data_name", methods=['GET','POST'])
def load_hr_360_query_data_name():
    
    if 'user' in session:
        
        

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record title
            operation_record_title = '載入 - HR 360 部門人員清單'    

            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            
            if request.method == 'POST':
                
                h_3_m_dep = request.form['h_3_m_dep']

                h_3_m_dep_member_list = db.HR_360_department_query_member(h_3_m_dep)
            
                return render_template('ajax/load_hr_360_dep_member_list.html' , 
                                       h_3_m_dep_member_list=h_3_m_dep_member_list
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

#####################################
# /select_erp_realtime_query_data3_1
#####################################
@app.route("/select_erp_realtime_query_data3_1", methods=['GET','POST'])
def select_erp_realtime_query_data3_1():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '載入 ERP - 原物料使用-原物料TO製品'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            
            if request.method == 'POST':
                
                q_e_p_num = request.form['q_e_p_num']

                erp_realtime_p_all_num = db.show_erp_realtime_query_data3_1('產品批號' , q_e_p_num)
            
                return render_template('ajax/load_erp_realtime_query_data3_1.html' , 
                                       erp_realtime_p_all_num=erp_realtime_p_all_num
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#####################################
# /select_erp_realtime_query_data3
#####################################
@app.route("/select_erp_realtime_query_data3", methods=['GET','POST'])
def select_erp_realtime_query_data3():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '載入 ERP 即時庫存資料'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            
            if request.method == 'POST':
                
                q_e_r_num   = request.form['q_e_r_num']
                q_e_p_name  = request.form['q_e_p_name']
                q_e_p_a_num = request.form['q_e_p_a_num']

                
                erp_realtime_p_name        = db.show_erp_realtime_query_data('產品名稱' , q_e_r_num , q_e_p_name)
                erp_realtime_p_num         = db.show_erp_realtime_query_data('產品批號' , q_e_r_num , q_e_p_name)
                erp_realtime_p_limit_date  = db.show_erp_realtime_query_data2('有效日期' , q_e_r_num , q_e_p_name , q_e_p_a_num)
            
                return render_template('ajax/load_erp_realtime_query_data3.html' , 
                                       erp_realtime_p_name=erp_realtime_p_name , 
                                       erp_realtime_p_num=erp_realtime_p_num , 
                                       erp_realtime_p_limit_date=erp_realtime_p_limit_date
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#####################################
# /select_erp_realtime_query_data2
#####################################
@app.route("/select_erp_realtime_query_data2", methods=['GET','POST'])
def select_erp_realtime_query_data2():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '載入 ERP 即時庫存資料'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            
            if request.method == 'POST':
                
                q_e_r_num  = request.form['q_e_r_num']
                q_e_p_name = request.form['q_e_p_name']

                
                erp_realtime_p_name = db.show_erp_realtime_query_data('產品名稱' , q_e_r_num , q_e_p_name)
                erp_realtime_p_num  = db.show_erp_realtime_query_data('產品批號' , q_e_r_num , q_e_p_name)
            
                return render_template('ajax/load_erp_realtime_query_data2.html' , 
                                       erp_realtime_p_name=erp_realtime_p_name , 
                                       erp_realtime_p_num=erp_realtime_p_num
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#####################################
# /select_erp_realtime_query_data
#####################################
@app.route("/select_erp_realtime_query_data", methods=['GET','POST'])
def select_erp_realtime_query_data():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '載入 ERP 即時庫存資料'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            
            if request.method == 'POST':
                
                q_e_r_num  = request.form['q_e_r_num']
                q_e_p_name = request.form['q_e_p_name']

                
                erp_realtime_p_name = db.show_erp_realtime_query_data('產品名稱' , q_e_r_num , q_e_p_name)
                erp_realtime_p_num  = db.show_erp_realtime_query_data('產品批號' , q_e_r_num , q_e_p_name)
            
                return render_template('ajax/load_erp_realtime_query_data.html' , 
                                       erp_realtime_p_name=erp_realtime_p_name , 
                                       erp_realtime_p_num=erp_realtime_p_num
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))  

#####################################
# /select_bpm_expenditure_dep_user
#####################################
@app.route("/select_bpm_expenditure_dep_user", methods=['GET','POST'])
def select_bpm_expenditure_dep_user():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'BPM 開支證明單 - 申請人'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            
            if request.method == 'POST':
                
                q_b_e_dep = request.form['q_b_e_dep']

                bpm_dep_member    = db.show_bpm_expenditure_deplist_member(q_b_e_dep)
                bpm_budget_source = db.show_bpm_expenditure_budget_source_by_dep(q_b_e_dep)
            
                return render_template('ajax/load_bpm_expenditure_dep_member.html' , 
                                       bpm_dep_member = bpm_dep_member ,
                                       bpm_budget_source=bpm_budget_source 
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))  

###########################################
# /show_select_erp_realtime_query_search3
###########################################
@app.route("/show_select_erp_realtime_query_search3" , methods=['GET','POST'])
def show_select_erp_realtime_query_search3():
    
    if 'user' in session:
        
        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################

            if request.method == 'POST':
                
                q_e_p_num3   = request.form['q_e_p_num3']
                q_e_p_a_num3 = request.form['q_e_p_a_num3']
                
                ### operation record title
                operation_record_title = f'ERP 原物料使用-原物料TO製品 查詢 - 品號 {q_e_p_num3} / 批號 {q_e_p_a_num3}'  
                
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                show_erp_realtime_query_search3 = db.show_erp_realtime_query_search3(q_e_p_num3 , q_e_p_a_num3)
            
                return render_template('ajax/show_erp_realtime_query_search3.html' , 
                                       show_erp_realtime_query_search3=show_erp_realtime_query_search3
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###########################################
# /show_select_erp_realtime_query_search2
###########################################
@app.route("/show_select_erp_realtime_query_search2" , methods=['GET','POST'])
def show_select_erp_realtime_query_search2():
    
    if 'user' in session:
        
        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################

            if request.method == 'POST':
                
                q_e_p_i_y_month    = request.form['q_e_p_i_y_month']
                
                ### operation record title
                operation_record_title = f'ERP 製品庫存&生產實績 入庫年月 查詢 - {q_e_p_i_y_month}'  
                
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                show_erp_realtime_query_search2 = db.show_erp_realtime_query_search2(q_e_p_i_y_month)
            
                return render_template('ajax/show_erp_realtime_query_search2.html' , 
                                       show_erp_realtime_query_search2=show_erp_realtime_query_search2
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 


####################################################
# /show_select_login_out_account_operation_record
####################################################
@app.route("/show_select_login_out_account_operation_record" , methods=['GET','POST'])
def show_select_login_out_account_operation_record():
    
    if 'user' in session:
        
        
        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################

            if request.method == 'POST':
                
                l_o_a_query = request.form['l_o_a_query']
                q_s_date    = request.form['q_s_date']
                q_e_date    = request.form['q_e_date']
                
                ### operation record title
                operation_record_title = f'帳號操作紀錄 帳號 : {l_o_a_query} , 時間 : {q_s_date} ~ {q_e_date} 查詢...'  
                
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                show_login_out_record_query_operation_search = db.show_login_out_record_query_operation_search(l_o_a_query , q_s_date , q_e_date)
            
                return render_template('ajax/show_login_out_record_query_operation_search.html' , 
                                       show_login_out_record_query_operation_search=show_login_out_record_query_operation_search
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###########################################
# /show_select_login_out_account_record
###########################################
@app.route("/show_select_login_out_account_record" , methods=['GET','POST'])
def show_select_login_out_account_record():
    
    if 'user' in session:
        
        
        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################

            if request.method == 'POST':
                
                l_o_a_query = request.form['l_o_a_query']
                q_s_date    = request.form['q_s_date']
                q_e_date    = request.form['q_e_date']
                
                ### operation record title
                operation_record_title = f'帳號進出紀錄 帳號 : {l_o_a_query} , 時間 : {q_s_date} ~ {q_e_date} 查詢...'  
                
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                show_login_out_record_query_search = db.show_login_out_record_query_search(l_o_a_query , q_s_date , q_e_date)
            
                return render_template('ajax/show_login_out_record_query_search.html' , 
                                       show_login_out_record_query_search=show_login_out_record_query_search
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###########################################
# /add_hr_360_setup_2
###########################################
@app.route("/add_hr_360_setup_2" , methods=['GET','POST'])
def add_hr_360_setup_2():
    
    if 'user' in session:
        
        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################

            if request.method == 'POST':
                
                h_360_m_dep      = request.form['h_360_m_dep']
                h_360_m_name     = request.form['h_360_m_name']
                h_360_m_lv       = request.form['h_360_m_lv']
                h_360_c_m_name   = request.form['h_360_c_m_name']
                h_360_c_p_1_name = request.form['h_360_c_p_1_name']
                h_360_c_p_2_name = request.form['h_360_c_p_2_name']
                h_360_c_s_1_name = request.form['h_360_c_s_1_name']
                h_360_c_s_2_name = request.form['h_360_c_s_2_name']
                
                ### operation record title
                operation_record_title = f'HR 360 考評設定 - {h_360_m_dep} / {h_360_m_name} / {h_360_m_lv} / {h_360_c_m_name} / {h_360_c_p_1_name} / {h_360_c_p_2_name} / {h_360_c_s_1_name} / {h_360_c_s_2_name}'  
                
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                show_hr_360_person_1_data = db.add_hr_360_setup_data(h_360_m_dep , h_360_m_name , h_360_m_lv , h_360_c_m_name , h_360_c_p_1_name , h_360_c_p_2_name , h_360_c_s_1_name , h_360_c_s_2_name)
            
                return render_template('ajax/load_hr_360_dep_member_list3_2.html' , 
                                       show_hr_360_person_1_data=show_hr_360_person_1_data
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

###########################################
# /add_hr_360_setup
###########################################
@app.route("/add_hr_360_setup" , methods=['GET','POST'])
def add_hr_360_setup():
    
    if 'user' in session:
        
        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################

            if request.method == 'POST':
                
                h_360_m_dep      = request.form['h_360_m_dep']
                h_360_m_name     = request.form['h_360_m_name']
                h_360_m_lv       = request.form['h_360_m_lv']
                h_360_c_m_name   = request.form['h_360_c_m_name']
                h_360_c_p_1_name = request.form['h_360_c_p_1_name']
                h_360_c_p_2_name = request.form['h_360_c_p_2_name']
                h_360_c_s_1_name = request.form['h_360_c_s_1_name']
                h_360_c_s_2_name = request.form['h_360_c_s_2_name']
                
                ### operation record title
                operation_record_title = f'HR 360 考評設定 - {h_360_m_dep} / {h_360_m_name} / {h_360_m_lv} / {h_360_c_m_name} / {h_360_c_p_1_name} / {h_360_c_p_2_name} / {h_360_c_s_1_name} / {h_360_c_s_2_name}'  
                
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                add_hr_360_setup_data = db.add_hr_360_setup_data(h_360_m_dep , h_360_m_name , h_360_m_lv , h_360_c_m_name , h_360_c_p_1_name , h_360_c_p_2_name , h_360_c_s_1_name , h_360_c_s_2_name)
            
                return render_template('ajax/load_hr_360_dep_member_list2.html' , 
                                       add_hr_360_setup_data=add_hr_360_setup_data
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

###########################################
# /show_select_erp_realtime_query_search
###########################################
@app.route("/show_select_erp_realtime_query_search" , methods=['GET','POST'])
def show_select_erp_realtime_query_search():
    
    if 'user' in session:
        
        
        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################

            if request.method == 'POST':
                
                q_e_p_num    = request.form['q_e_p_num']
                q_e_p_name   = request.form['q_e_p_name']
                q_e_p_a_num  = request.form['q_e_p_a_num']
                q_e_p_l_date = request.form['q_e_p_l_date']
                
                ### operation record title
                operation_record_title = f'ERP 即時庫存查詢 - {q_e_p_num} / {q_e_p_name} / {q_e_p_a_num} / {q_e_p_l_date}'  
                
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                show_erp_realtime_query_search = db.show_erp_realtime_query_search(q_e_p_num , q_e_p_name , q_e_p_a_num , q_e_p_l_date)
            
                return render_template('ajax/show_erp_realtime_query_search.html' , 
                                       show_erp_realtime_query_search=show_erp_realtime_query_search
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 


########################################
# /show_select_bpm_expenditure_search
########################################
@app.route("/show_select_bpm_expenditure_search" , methods=['GET','POST'])
def show_select_bpm_expenditure_search():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'BPM 開支證明單 - 搜尋'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            if request.method == 'POST':
                
                q_s_date         = request.form['q_s_date']
                q_e_date         = request.form['q_e_date']
                q_b_e_dep        = request.form['q_b_e_dep']
                q_b_e_d_member   = request.form['q_b_e_d_member']
                q_b_e_status     = request.form['q_b_e_status']
                q_b_b_s_b_budget = request.form['q_b_b_s_b_budget']

                show_bpm_expenditure_form_search           = db.show_bpm_expenditure_form_search(q_s_date , q_e_date , q_b_e_dep , q_b_e_d_member , q_b_e_status , q_b_b_s_b_budget)
                show_bpm_expenditure_form_search_sum_money = db.show_bpm_expenditure_form_search_money_sum(q_s_date , q_e_date , q_b_e_dep , q_b_e_d_member , q_b_e_status , q_b_b_s_b_budget)
            
                return render_template('ajax/show_bpm_expenditure_form_search.html' , 
                                       show_bpm_expenditure_form_search=show_bpm_expenditure_form_search , q_b_e_dep=q_b_e_dep , 
                                       q_b_e_d_member=q_b_e_d_member ,  q_b_e_status=q_b_e_status , show_bpm_expenditure_form_search_sum_money=show_bpm_expenditure_form_search_sum_money
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))  

###################################
# /load_factory_erp_subform_list
###################################
@app.route("/load_factory_erp_subform_list", methods=['GET','POST'])
def load_factory_erp_subform_list():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                q_s_date = request.form['q_s_date']
                q_e_date = request.form['q_e_date']

                ### operation record title
                operation_record_title = '工廠 ERP - 搜尋 ERP - 子單身 ' + q_s_date + ' ~ ' + q_e_date + ' 資料'    

                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                ### department name & updepartment name
                dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
                updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
                updep_name   = db.bpm_account_up_department(updep_id)
                c_name       = db.bpm_account_data(user,'EmployeeName')

                ### 工廠 ERP - 子單身查詢
                f_subform_query_1 = db.factory_erp_subform_query1(q_s_date , q_e_date)

                return render_template('ajax/load_factory_erp_subform_list.html' , 
                                    user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                    r_date=r_date , dep_id=dep_name , updep_name=updep_name , f_subform_query_1=f_subform_query_1
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###############################
# /load_factory_erp_bom_list
###############################
@app.route("/load_factory_erp_bom_list", methods=['GET','POST'])
def load_factory_erp_bom_list():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                q_c_name = request.form['q_c_name']

                ### operation record title
                operation_record_title = '工廠 ERP - 搜尋 BOM 主件品號 ' + q_c_name + ' 資料'    

                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                ### department name & updepartment name
                dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
                updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
                updep_name   = db.bpm_account_up_department(updep_id)
                c_name       = db.bpm_account_data(user,'EmployeeName')

                ### 工廠 ERP - BOM 維護
                f_bom_query_1        = db.factory_erp_bom_query1(q_c_name)
                f_bom_query_2        = db.factory_erp_bom_query2(q_c_name)

                return render_template('ajax/load_factory_erp_bom_list.html' , 
                                    user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                    r_date=r_date , dep_id=dep_name , updep_name=updep_name , f_bom_query_1=f_bom_query_1 ,
                                    f_bom_query_2=f_bom_query_2
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###############################
# /load_factory_erp_ss2_list
###############################
@app.route("/load_factory_erp_ss2_list", methods=['GET','POST'])
def load_factory_erp_ss2_list():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':

            ### operation record title
            operation_record_title = '工廠 ERP - 搜尋銷售實績'    
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                q_s_date = request.form['q_s_date']
                q_e_date = request.form['q_e_date']
                q_c_name = request.form['q_c_name']
                q_p_name = request.form['q_p_name']

                ### department name & updepartment name
                dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
                updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
                updep_name   = db.bpm_account_up_department(updep_id)
                c_name       = db.bpm_account_data(user,'EmployeeName')

                ### 工廠 ERP - 銷售實績
                f_ss2_query_res        = db.factory_erp_ss2_product_name_query2(q_s_date , q_e_date , q_c_name , q_p_name)
                f_ss2_query_res_total  = db.factory_erp_ss2_product_name_total(q_s_date , q_e_date , q_c_name , q_p_name)
                f_ss2_query_res_total2 = db.factory_erp_ss2_product_name_total2(q_s_date , q_e_date , q_c_name , q_p_name)

                return render_template('ajax/load_factory_erp_ss2_sales_list.html' , 
                                    user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                    r_date=r_date , dep_id=dep_name , updep_name=updep_name , f_ss2_query_res=f_ss2_query_res , 
                                    f_ss2_query_res_total=f_ss2_query_res_total , f_ss2_query_res_total2=f_ss2_query_res_total2 ,
                                    q_s_date=q_s_date , q_e_date=q_e_date , q_c_name=q_c_name , q_p_name=q_p_name
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##########################
# /e_board
##########################
@app.route("/e_board")
def e_board():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '電子看板'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### 電子看板
            e_b_list  = db.e_board_list()
            
            return render_template('e_board.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name , e_b_list=e_b_list 
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##########################
# /f_erp_realtime_query8
##########################
@app.route("/f_erp_realtime_query8")
def f_erp_realtime_query8():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'ERP / SS2 品號對應管理'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### ERP / SS2 品號對應管理
            p_s_query_res  = db.purchase_sales_erp_query()
            p_s_query_res2 = db.purchase_sales_erp_query2()

            p_s_query_person_res  = db.purchase_sales_erp_person_query()
            p_s_query_res_by_date = db.purchase_sales_erp_query_by_date()

            return render_template('f_erp_realtime_query8.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name , p_s_query_res=p_s_query_res,
                                   p_s_query_res2=p_s_query_res2 , p_s_query_person_res=p_s_query_person_res , p_s_query_res_by_date=p_s_query_res_by_date
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##########################
# /f_erp_realtime_query7
##########################
@app.route("/f_erp_realtime_query7")
def f_erp_realtime_query7():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '工廠 ERP - 進銷項明細查詢'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### 工廠 ERP - 進銷項明細表 , 進銷項彙總表
            p_s_query_res  = db.purchase_sales_erp_query()
            p_s_query_res2 = db.purchase_sales_erp_query2()

            p_s_query_person_res  = db.purchase_sales_erp_person_query()
            p_s_query_res_by_date = db.purchase_sales_erp_query_by_date()

            return render_template('f_erp_realtime_query7.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name , p_s_query_res=p_s_query_res,
                                   p_s_query_res2=p_s_query_res2 , p_s_query_person_res=p_s_query_person_res , p_s_query_res_by_date=p_s_query_res_by_date
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##########################
# /f_erp_realtime_query6
##########################
@app.route("/f_erp_realtime_query6")
def f_erp_realtime_query6():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '工廠 ERP - 子單身查詢'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### 工廠 ERP - 子單身查詢
            f_ss2_query_res  = db.factory_erp_ss2_query()
            f_ss2_query_res2 = db.factory_erp_ss2_product_name_query()
            f_ss2_query_res3 = db.factory_erp_ss2_customer_name_query()
            f_ss2_query_res4 = db.factory_erp_product_num_query()
            
            return render_template('f_erp_realtime_query6.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name , f_ss2_query_res=f_ss2_query_res , f_ss2_query_res2=f_ss2_query_res2 , 
                                   f_ss2_query_res3=f_ss2_query_res3 , f_ss2_query_res4=f_ss2_query_res4
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##########################
# /f_erp_realtime_query5
##########################
@app.route("/f_erp_realtime_query5")
def f_erp_realtime_query5():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '工廠 ERP - BOM 維護'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### 工廠 ERP - BOM 維護
            f_ss2_query_res  = db.factory_erp_ss2_query()
            f_ss2_query_res2 = db.factory_erp_ss2_product_name_query()
            f_ss2_query_res3 = db.factory_erp_ss2_customer_name_query()
            f_ss2_query_res4 = db.factory_erp_product_num_query()
            
            return render_template('f_erp_realtime_query5.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name , f_ss2_query_res=f_ss2_query_res , f_ss2_query_res2=f_ss2_query_res2 , 
                                   f_ss2_query_res3=f_ss2_query_res3 , f_ss2_query_res4=f_ss2_query_res4
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 


##########################
# /f_erp_realtime_query4
##########################
@app.route("/f_erp_realtime_query4")
def f_erp_realtime_query4():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '工廠 ERP - 銷售實績'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### 工廠 ERP - 銷售實績
            f_ss2_query_res  = db.factory_erp_ss2_query()
            f_ss2_query_res2 = db.factory_erp_ss2_product_name_query()
            f_ss2_query_res3 = db.factory_erp_ss2_customer_name_query()
            
            return render_template('f_erp_realtime_query4.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name , f_ss2_query_res=f_ss2_query_res , f_ss2_query_res2=f_ss2_query_res2 , 
                                   f_ss2_query_res3=f_ss2_query_res3 
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##########################
# /f_erp_realtime_query3
##########################
@app.route("/f_erp_realtime_query3")
def f_erp_realtime_query3():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '工廠 ERP - 原物料使用-原物料TO製品'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### 工廠 ERP - 原物料使用-原物料TO製品
            f_query_res   = db.factory_erp_query()
            f_query_res_3 = db.factory_erp_query_import_3()
            
            return render_template('f_erp_realtime_query3.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name , f_query_res=f_query_res , 
                                   f_query_res_3=f_query_res_3
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##########################
# /f_erp_realtime_query2
##########################
@app.route("/f_erp_realtime_query2")
def f_erp_realtime_query2():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '工廠 ERP - 製品庫存&生產實績'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### 工廠 ERP 製品庫存&生產實績
            f_query_res   = db.factory_erp_query()
            f_query_res_2 = db.factory_erp_query_import_year_month()
            
            return render_template('f_erp_realtime_query2.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name , f_query_res=f_query_res , 
                                   f_query_res_2=f_query_res_2
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##########################
# /login_out_record
##########################
@app.route("/login_out_record")
def login_out_record():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record title
            operation_record_title = '帳號紀錄'    
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### function
            login_out_record_res = db.login_out_record()
            
            return render_template('login_out_record.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name , login_out_record_res=login_out_record_res
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

##########################
# /f_erp_realtime_query
##########################
@app.route("/f_erp_realtime_query")
def f_erp_realtime_query():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '工廠 ERP - 即時庫存查詢'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### 工廠 ERP 即時庫存查詢
            f_query_res   = db.factory_erp_query()
            f_query_res_1 = db.factory_erp_query_product_num('產品品號')
            
            return render_template('f_erp_realtime_query.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name , f_query_res=f_query_res , 
                                   f_query_res_1=f_query_res_1
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#######################################
# /submit_hr_360_content_data_member
#######################################
@app.route("/submit_hr_360_content_data_member", methods=['GET','POST'])
def submit_hr_360_content_data_member():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                check_hr_360_date = request.form['check_hr_360_date']
                check_hr_360_user = request.form['check_hr_360_user']
                check_hr_360_lv   = request.form['check_hr_360_lv']
                check_hr_360_name = request.form['check_hr_360_name']

                hr_360_total_1_1  = request.form['hr_360_total_1_1']
                hr_360_total_1_2  = request.form['hr_360_total_1_2']
                hr_360_total_1_3  = request.form['hr_360_total_1_3']
                hr_360_total_1_4  = request.form['hr_360_total_1_4']
                hr_360_total_1_5  = request.form['hr_360_total_1_5']
                
                hr_360_total_2_1  = request.form['hr_360_total_2_1']
                hr_360_total_2_2  = request.form['hr_360_total_2_2']
                hr_360_total_2_3  = request.form['hr_360_total_2_3']
                hr_360_total_2_4  = request.form['hr_360_total_2_4']
                hr_360_total_2_5  = request.form['hr_360_total_2_5']
                
                hr_360_total_3_1  = request.form['hr_360_total_3_1']
                hr_360_total_3_2  = request.form['hr_360_total_3_2']
                hr_360_total_3_3  = request.form['hr_360_total_3_3']
                hr_360_total_3_4  = request.form['hr_360_total_3_4']
                hr_360_total_3_5  = request.form['hr_360_total_3_5']
                
                hr_360_total_4_1  = request.form['hr_360_total_4_1']
                hr_360_total_4_2  = request.form['hr_360_total_4_2']
                hr_360_total_4_3  = request.form['hr_360_total_4_3']
                hr_360_total_4_4  = request.form['hr_360_total_4_4']
                hr_360_total_4_5  = request.form['hr_360_total_4_5']
                
                hr_360_total_5_1  = request.form['hr_360_total_5_1']
                hr_360_total_5_2  = request.form['hr_360_total_5_2']
                hr_360_total_5_3  = request.form['hr_360_total_5_3']
                hr_360_total_5_4  = request.form['hr_360_total_5_4']
                hr_360_total_5_5  = request.form['hr_360_total_5_5']
                hr_360_total_5_6  = request.form['hr_360_total_5_6']

                total_1     = request.form['total_1']
                total_1_avg = request.form['total_1_avg']
                
                total_2     = request.form['total_2']
                total_2_avg = request.form['total_2_avg']

                total_3     = request.form['total_3']
                total_3_avg = request.form['total_3_avg']

                total_4     = request.form['total_4']
                total_4_avg = request.form['total_4_avg']

                total_5     = request.form['total_5']
                total_5_avg = request.form['total_5_avg']

                


                ### operation record title
                operation_record_title = f'送出 HR - 360 考評人員 {check_hr_360_name} 內容項目資料'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                submit_hr_360_content_data = db.submit_hr_360_content_data_member(check_hr_360_date , check_hr_360_user , check_hr_360_lv , 
                                                                                  check_hr_360_name , 
                                                                                  hr_360_total_1_1 , hr_360_total_1_2 , hr_360_total_1_3 , hr_360_total_1_4 , hr_360_total_1_5 ,
                                                                                  hr_360_total_2_1 , hr_360_total_2_2 , hr_360_total_2_3 , hr_360_total_2_4 , hr_360_total_2_5 , 
                                                                                  hr_360_total_3_1 , hr_360_total_3_2 , hr_360_total_3_3 , hr_360_total_3_4 , hr_360_total_3_5 ,
                                                                                  hr_360_total_4_1 , hr_360_total_4_2 , hr_360_total_4_3 , hr_360_total_4_4 , hr_360_total_4_5 , 
                                                                                  hr_360_total_5_1 , hr_360_total_5_2 , hr_360_total_5_3 , hr_360_total_5_4 , hr_360_total_5_5 , hr_360_total_5_6 ,
                                                                                  total_1 , total_1_avg ,total_2 , total_2_avg ,total_3 , total_3_avg ,total_4 , total_4_avg ,total_5 , total_5_avg
                                                                                  )

                return render_template('ajax/submit_hr_360_content_name_member.html' , 
                                        submit_hr_360_content_data=submit_hr_360_content_data
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

################################
# /submit_hr_360_content_data
################################
@app.route("/submit_hr_360_content_data", methods=['GET','POST'])
def submit_hr_360_content_data():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                check_hr_360_date = request.form['check_hr_360_date']
                check_hr_360_user = request.form['check_hr_360_user']
                check_hr_360_lv   = request.form['check_hr_360_lv']
                check_hr_360_name = request.form['check_hr_360_name']

                hr_360_total_1_1  = request.form['hr_360_total_1_1']
                hr_360_total_1_2  = request.form['hr_360_total_1_2']
                hr_360_total_1_3  = request.form['hr_360_total_1_3']
                hr_360_total_1_4  = request.form['hr_360_total_1_4']
                hr_360_total_1_5  = request.form['hr_360_total_1_5']
                
                hr_360_total_2_1  = request.form['hr_360_total_2_1']
                hr_360_total_2_2  = request.form['hr_360_total_2_2']
                hr_360_total_2_3  = request.form['hr_360_total_2_3']
                hr_360_total_2_4  = request.form['hr_360_total_2_4']
                hr_360_total_2_5  = request.form['hr_360_total_2_5']
                hr_360_total_2_6  = request.form['hr_360_total_2_6']
                
                hr_360_total_3_1  = request.form['hr_360_total_3_1']
                hr_360_total_3_2  = request.form['hr_360_total_3_2']
                hr_360_total_3_3  = request.form['hr_360_total_3_3']
                hr_360_total_3_4  = request.form['hr_360_total_3_4']
                hr_360_total_3_5  = request.form['hr_360_total_3_5']
                
                hr_360_total_4_1  = request.form['hr_360_total_4_1']
                hr_360_total_4_2  = request.form['hr_360_total_4_2']
                hr_360_total_4_3  = request.form['hr_360_total_4_3']
                hr_360_total_4_4  = request.form['hr_360_total_4_4']
                
                hr_360_total_5_1  = request.form['hr_360_total_5_1']
                hr_360_total_5_2  = request.form['hr_360_total_5_2']
                hr_360_total_5_3  = request.form['hr_360_total_5_3']
                
                hr_360_total_6_1  = request.form['hr_360_total_6_1']
                hr_360_total_6_2  = request.form['hr_360_total_6_2']
                hr_360_total_6_3  = request.form['hr_360_total_6_3']
                hr_360_total_6_4  = request.form['hr_360_total_6_4']
                hr_360_total_6_5  = request.form['hr_360_total_6_5']

                total_1     = request.form['total_1']
                total_1_avg = request.form['total_1_avg']
                
                total_2     = request.form['total_2']
                total_2_avg = request.form['total_2_avg']

                total_3     = request.form['total_3']
                total_3_avg = request.form['total_3_avg']

                total_4     = request.form['total_4']
                total_4_avg = request.form['total_4_avg']

                total_5     = request.form['total_5']
                total_5_avg = request.form['total_5_avg']

                total_6     = request.form['total_6']
                total_6_avg = request.form['total_6_avg']


                ### operation record title
                operation_record_title = f'送出 HR - 360 考評人員 {check_hr_360_name} 內容項目資料'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                submit_hr_360_content_data = db.submit_hr_360_content_data(check_hr_360_date , check_hr_360_user , check_hr_360_lv , check_hr_360_name , hr_360_total_1_1 , hr_360_total_1_2 , hr_360_total_1_3 , hr_360_total_1_4 , hr_360_total_1_5 ,hr_360_total_2_1 , hr_360_total_2_2 , hr_360_total_2_3 , hr_360_total_2_4 , hr_360_total_2_5 , hr_360_total_2_6 ,hr_360_total_3_1 , hr_360_total_3_2 , hr_360_total_3_3 , hr_360_total_3_4 , hr_360_total_3_5 ,hr_360_total_4_1 , hr_360_total_4_2 , hr_360_total_4_3 , hr_360_total_4_4 , hr_360_total_5_1 , hr_360_total_5_2 , hr_360_total_5_3 ,hr_360_total_6_1 , hr_360_total_6_2 , hr_360_total_6_3 , hr_360_total_6_4 , hr_360_total_6_5 ,total_1 , total_1_avg ,total_2 , total_2_avg ,total_3 , total_3_avg ,total_4 , total_4_avg ,total_5 , total_5_avg ,total_6 , total_6_avg)

                return render_template('ajax/submit_hr_360_content_name.html' , 
                                        submit_hr_360_content_data=submit_hr_360_content_data
                                      )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

################################
# /hr_360_content_name_member
################################
@app.route("/hr_360_content_name_member", methods=['GET','POST'])
def hr_360_content_name_member():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                hr_360_content_name = request.form['hr_360_content_name']

                ### operation record title
                operation_record_title = f'載入 HR - 360 考評人員 {hr_360_content_name} 內容項目'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title) 
                hr_360_person_lv = db.search_hr_360_person_lv_member(user , hr_360_content_name)   

                return render_template('ajax/load_hr_360_content_name2.html' , 
                                    hr_360_content_name=hr_360_content_name , r_date=r_date , user=user , hr_360_person_lv=hr_360_person_lv
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

##############################
# /hr_360_content_name
##############################
@app.route("/hr_360_content_name", methods=['GET','POST'])
def hr_360_content_name():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                hr_360_content_name = request.form['hr_360_content_name']

                ### operation record title
                operation_record_title = f'載入 HR - 360 考評人員 {hr_360_content_name} 內容項目'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title) 
                hr_360_person_lv = db.search_hr_360_person_lv(user , hr_360_content_name)   

                return render_template('ajax/load_hr_360_content_name1.html' , 
                                    hr_360_content_name=hr_360_content_name , r_date=r_date , user=user , hr_360_person_lv=hr_360_person_lv
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

##############################
# /hr_360_employee_hr_name_5_5
##############################
@app.route("/hr_360_employee_hr_name_5_5", methods=['GET','POST'])
def hr_360_employee_hr_name_5_5():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                h_360_hr_name  = request.form['h_360_hr_name']

                ### operation record title
                operation_record_title = f'搜尋 HR - 360 考評人員 {h_360_hr_name} 姓名'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_360_employee_hr_name = db.HR_360_employee_hr_name(h_360_hr_name)
                
                return render_template('ajax/load_hr_360_dep_member_list9_1.html' , 
                                    show_360_employee_hr_name=show_360_employee_hr_name
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##############################
# /hr_360_employee_hr_name_5
##############################
@app.route("/hr_360_employee_hr_name_5", methods=['GET','POST'])
def hr_360_employee_hr_name_5():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                h_360_hr_name  = request.form['h_360_hr_name']

                ### operation record title
                operation_record_title = f'搜尋 HR - 360 考評人員 {h_360_hr_name} 姓名'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_360_employee_hr_name = db.HR_360_employee_hr_name(h_360_hr_name)
                
                return render_template('ajax/load_hr_360_dep_member_list9.html' , 
                                    show_360_employee_hr_name=show_360_employee_hr_name
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##############################
# /hr_360_employee_hr_name_4_4
##############################
@app.route("/hr_360_employee_hr_name_4_4", methods=['GET','POST'])
def hr_360_employee_hr_name_4_4():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                h_360_hr_name  = request.form['h_360_hr_name']

                ### operation record title
                operation_record_title = f'搜尋 HR - 360 考評人員 {h_360_hr_name} 姓名'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_360_employee_hr_name = db.HR_360_employee_hr_name(h_360_hr_name)
                
                return render_template('ajax/load_hr_360_dep_member_list8_1.html' , 
                                    show_360_employee_hr_name=show_360_employee_hr_name
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##############################
# /hr_360_employee_hr_name_4
##############################
@app.route("/hr_360_employee_hr_name_4", methods=['GET','POST'])
def hr_360_employee_hr_name_4():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                h_360_hr_name  = request.form['h_360_hr_name']

                ### operation record title
                operation_record_title = f'搜尋 HR - 360 考評人員 {h_360_hr_name} 姓名'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_360_employee_hr_name = db.HR_360_employee_hr_name(h_360_hr_name)
                
                return render_template('ajax/load_hr_360_dep_member_list8.html' , 
                                    show_360_employee_hr_name=show_360_employee_hr_name
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##############################
# /hr_360_employee_hr_name_3_3
##############################
@app.route("/hr_360_employee_hr_name_3_3", methods=['GET','POST'])
def hr_360_employee_hr_name_3_3():
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                h_360_hr_name  = request.form['h_360_hr_name']

                ### operation record title
                operation_record_title = f'搜尋 HR - 360 考評人員 {h_360_hr_name} 姓名'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_360_employee_hr_name = db.HR_360_employee_hr_name(h_360_hr_name)
                
                return render_template('ajax/load_hr_360_dep_member_list7_1.html' , 
                                    show_360_employee_hr_name=show_360_employee_hr_name
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##############################
# /hr_360_employee_hr_name_3
##############################
@app.route("/hr_360_employee_hr_name_3", methods=['GET','POST'])
def hr_360_employee_hr_name_3():
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                h_360_hr_name  = request.form['h_360_hr_name']

                ### operation record title
                operation_record_title = f'搜尋 HR - 360 考評人員 {h_360_hr_name} 姓名'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_360_employee_hr_name = db.HR_360_employee_hr_name(h_360_hr_name)
                
                return render_template('ajax/load_hr_360_dep_member_list7.html' , 
                                    show_360_employee_hr_name=show_360_employee_hr_name
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##############################
# /hr_360_employee_hr_name_2_2
##############################
@app.route("/hr_360_employee_hr_name_2_2", methods=['GET','POST'])
def hr_360_employee_hr_name_2_2():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                h_360_hr_name  = request.form['h_360_hr_name']

                ### operation record title
                operation_record_title = f'搜尋 HR - 360 考評人員 {h_360_hr_name} 姓名'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_360_employee_hr_name = db.HR_360_employee_hr_name(h_360_hr_name)
                
                return render_template('ajax/load_hr_360_dep_member_list6_1.html' , 
                                    show_360_employee_hr_name=show_360_employee_hr_name
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##############################
# /hr_360_employee_hr_name_2
##############################
@app.route("/hr_360_employee_hr_name_2", methods=['GET','POST'])
def hr_360_employee_hr_name_2():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                h_360_hr_name  = request.form['h_360_hr_name']

                ### operation record title
                operation_record_title = f'搜尋 HR - 360 考評人員 {h_360_hr_name} 姓名'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_360_employee_hr_name = db.HR_360_employee_hr_name(h_360_hr_name)
                
                return render_template('ajax/load_hr_360_dep_member_list6.html' , 
                                    show_360_employee_hr_name=show_360_employee_hr_name
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 


##############################
# /hr_360_employee_hr_name_1
##############################
@app.route("/hr_360_employee_hr_name_1", methods=['GET','POST'])
def hr_360_employee_hr_name_1():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                h_360_hr_name  = request.form['h_360_hr_name']

                ### operation record title
                operation_record_title = f'搜尋 HR - 360 考評人員 {h_360_hr_name} 姓名'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_360_employee_hr_name = db.HR_360_employee_hr_name(h_360_hr_name)
                
                return render_template('ajax/load_hr_360_dep_member_list5_1.html' , 
                                    show_360_employee_hr_name=show_360_employee_hr_name
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##############################
# /hr_360_employee_hr_name_1_1
##############################
@app.route("/hr_360_employee_hr_name_1_1", methods=['GET','POST'])
def hr_360_employee_hr_name_1_1():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                h_360_hr_name  = request.form['h_360_hr_name']

                ### operation record title
                operation_record_title = f'搜尋 HR - 360 考評人員 {h_360_hr_name} 姓名'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_360_employee_hr_name = db.HR_360_employee_hr_name(h_360_hr_name)
                
                return render_template('ajax/load_hr_360_dep_member_list5_1.html' , 
                                    show_360_employee_hr_name=show_360_employee_hr_name
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##############################
# /hr_360_employee_hr_name
##############################
@app.route("/hr_360_employee_hr_name", methods=['GET','POST'])
def hr_360_employee_hr_name():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                h_360_hr_name  = request.form['h_360_hr_name']

                ### operation record title
                operation_record_title = f'搜尋 HR - 360 考評人員 {h_360_hr_name} 姓名'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_360_employee_hr_name = db.HR_360_employee_hr_name(h_360_hr_name)
                
                return render_template('ajax/load_hr_360_dep_member_list5.html' , 
                                    show_360_employee_hr_name=show_360_employee_hr_name
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##############################
# /alter_hr_360_manager_list2
##############################
@app.route("/alter_hr_360_manager_list2", methods=['GET','POST'])
def alter_hr_360_manager_list2():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                d_dep  = request.form['d_dep']
                d_name = request.form['d_name']

                ### operation record title
                operation_record_title = f'修改 HR - 360 考評 {d_dep} / {d_name} 資料'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)  
                
                ### 資料
                show_hr_360_person_1_data = db.alter_hr_360_person_data(d_dep , d_name)
                
                return render_template('ajax/load_hr_360_dep_member_list4_2.html' , 
                                    show_hr_360_person_1_data=show_hr_360_person_1_data
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##############################
# /alter_hr_360_manager_list
##############################
@app.route("/alter_hr_360_manager_list", methods=['GET','POST'])
def alter_hr_360_manager_list():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                d_dep  = request.form['d_dep']
                d_name = request.form['d_name']

                ### operation record title
                operation_record_title = f'修改 HR - 360 考評 {d_dep} / {d_name} 資料'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)  
                
                ### 資料
                show_hr_360_person_1_data = db.alter_hr_360_person_data(d_dep , d_name)
                
                return render_template('ajax/load_hr_360_dep_member_list4.html' , 
                                    show_hr_360_person_1_data=show_hr_360_person_1_data
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#####################################
# /show_test_radar_pic
#####################################
@app.route('/show_test_radar_pic')
def show_test_radar_pic():
    try:
           
            # Data for the radar chart
            labels = np.array(['管理能力', '提供支援', '以身作則', '效率導向', '培育人才', '高效溝通'])
            values = np.array([4, 3, 4.2, 5, 4.5, 4.7])

            # Close the loop for the radar chart
            values = np.concatenate((values, [values[0]]))
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            angles += angles[:1]

            # Plot radar chart
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.fill(angles, values, color='blue', alpha=0.25)
            ax.plot(angles, values, color='blue', linewidth=2)

            font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'  # 替換為你的字體文件路徑
            prop = fm.FontProperties(fname=font_path)
            # Set font to a font that supports Chinese characters
            plt.rcParams['font.sans-serif'] = [font_path]
            plt.rcParams['axes.unicode_minus'] = False

            ax.set_yticklabels([])
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels, fontproperties=prop)

            # Save the plot to a BytesIO object
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            img = base64.b64encode(buf.getvalue()).decode('utf8')
            buf.close()

            # Render the image in the webpage
            pie_pic = f'<img class="img-fluid w-100" src="data:image/png;base64,{img}"/>'

            return pie_pic
        
    except Exception as e:
        logging.info(f"<Error> show_radar_picture : {str(e)}\n\n")
    finally:
        pass

#####################################
# /show_test_pic
#####################################
@app.route('/show_test_pic')
def show_test_pic():
    # 数据
    total = 5
    actual = 4
    remaining = total - actual

    # 甜甜圈图的部分
    sizes = [actual, remaining]
    colors = ['blue', 'lightgray']  # 实际得分显示为蓝色，剩余部分显示为浅灰色
    labels = ['Actual Score', 'Remaining']

    # 绘制甜甜圈图
    fig, ax = plt.subplots()
    ax.pie(sizes, colors=colors, startangle=90, counterclock=False, 
           wedgeprops=dict(width=0.3))

    # 添加中心的圆来创建甜甜圈效果
    center_circle = plt.Circle((0,0), 0.7, color='white')
    fig.gca().add_artist(center_circle)

    # 在中心添加文本
    ax.text(0, 0, f'{actual}', horizontalalignment='center', 
            verticalalignment='center', fontsize=24, fontweight='bold')

    # 将图表保存到内存中的一个字节流
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode('utf8')
    buf.close()

    # 渲染图像到网页中
    pie_pic = f'<img src="data:image/png;base64,{img}"/>'
    return render_template_string(pie_pic)


#####################################
# /export_hr_360_pdf
#####################################
@app.route('/export_hr_360_pdf', methods=['GET'])
def export_hr_360_pdf():
    try:
        if request.method == 'GET':

            s_name = request.args.get('s_name')

            print_url = f"/show_hr_360_person_result2_2_export_pdf?s_name={s_name}"
            print_pdf = f"hr_360_{s_name}.pdf"
        
            rendered = render_template(print_url)  # Render your HTML template
            html = HTML(string=rendered)  # Create an HTML object
            pdf = html.write_pdf()  # Convert HTML to PDF
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename={print_pdf}'
            return response
        
    except Exception as e:
        logging.info(f"\n\n<Error> export_hr_360_pdf : {str(e)}\n\n")
    finally:
        pass
    

#############################################
# /show_hr_360_person_result2_2_export_pdf
#############################################
@app.route("/show_hr_360_person_result2_2_export_pdf", methods=['GET'])
def show_hr_360_person_result2_2_export_pdf():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'GET':

                s_name = request.args.get('s_name')

                ### operation record title
                operation_record_title = f'載入 HR - 360 考評 , 受評人員 : {s_name} 總分數資料'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ############
                # 考評人員
                ############
                show_hr_360_person_1_check_data = db.show_hr_360_person_process_total_data2_2(s_name)
                
                c_name         = db.search_hr_360_person_name(s_name , 'c_name')
                c_manager      = db.search_hr_360_person_name(s_name , 'c_manager')
                c_peer1        = db.search_hr_360_person_name(s_name , 'c_peer1')
                c_peer2        = db.search_hr_360_person_name(s_name , 'c_peer2')
                c_subordinate1 = db.search_hr_360_person_name(s_name , 'c_subordinate1')
                c_subordinate2 = db.search_hr_360_person_name(s_name , 'c_subordinate2')

                #####################################
                # 對於客戶的服務(包含內部客戶或外部客戶)
                #####################################
                show_pie_pic_self_1_1         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_manager_1_1      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_peer1_1_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_peer2_1_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_subordinate1_1_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_subordinate2_1_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_1_1' , 5 , 'none')

                show_pie_pic_self_1_2         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_manager_1_2      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_peer1_1_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_peer2_1_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_subordinate1_1_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_subordinate2_1_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_1_2' , 5 , 'none')
                
                show_pie_pic_self_1_3         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_manager_1_3      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_peer1_1_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_peer2_1_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_subordinate1_1_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_subordinate2_1_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_1_3' , 5 , 'none')

                show_pie_pic_self_1_4         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_manager_1_4      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_peer1_1_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_peer2_1_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_subordinate1_1_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_subordinate2_1_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_1_4' , 5 , 'none')

                show_pie_pic_self_1_5         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_manager_1_5      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_peer1_1_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_peer2_1_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_subordinate1_1_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_subordinate2_1_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_1_5' , 5 , 'none')
                

                show_pie_pic_self_total_1_1             = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_self_total_avg_1           = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_self_total_avg_1_1         = round(float(show_pie_pic_self_total_avg_1) , 2) if show_pie_pic_self_total_avg_1 is not None else 0 
                show_pie_pic_manager_total_1_1          = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_manager_total_avg_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_manager_total_avg_1_1      = round(float(show_pie_pic_manager_total_avg_1) , 2) if show_pie_pic_manager_total_avg_1 is not None else 0
                show_pie_pic_peer1_total_1_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_peer1_total_avg_1          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_peer1_total_avg_1_1        = round(float(show_pie_pic_peer1_total_avg_1) , 2) if show_pie_pic_peer1_total_avg_1 is not None else 0
                show_pie_pic_peer2_total_1_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_peer2_total_avg_1          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_peer2_total_avg_1_1        = round(float(show_pie_pic_peer2_total_avg_1) , 2) if show_pie_pic_peer2_total_avg_1 is not None else 0
                show_pie_pic_subordinate1_total_1_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_1   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_subordinate1_total_avg_1_1 = round(float(show_pie_pic_subordinate1_total_avg_1) , 2) if show_pie_pic_subordinate1_total_avg_1 is not None else 0
                show_pie_pic_subordinate2_total_1_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_1   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_subordinate2_total_avg_1_1 = round(float(show_pie_pic_subordinate2_total_avg_1) , 2) if show_pie_pic_subordinate2_total_avg_1 is not None else 0
                show_pie_pic_total_avg_1                = (
                                                           float(show_pie_pic_self_total_avg_1_1)     +
                                                           float(show_pie_pic_manager_total_avg_1_1)  + 
                                                           float(show_pie_pic_peer1_total_avg_1_1)     + 
                                                           float(show_pie_pic_peer2_total_avg_1_1)     + 
                                                           float(show_pie_pic_subordinate1_total_avg_1_1)   + 
                                                           float(show_pie_pic_subordinate2_total_avg_1_1))/6 
                show_pie_pic_total_avg_1_1              = round(show_pie_pic_total_avg_1 , 2)
                
                ####################
                # 溝通與待人接物能力
                ####################
                show_pie_pic_self_2_1         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_manager_2_1      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_peer1_2_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_peer2_2_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_subordinate1_2_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_subordinate2_2_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_2_1' , 5 , 'none')

                show_pie_pic_self_2_2         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_manager_2_2      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_peer1_2_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_peer2_2_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_subordinate1_2_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_subordinate2_2_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_2_2' , 5 , 'none')
                
                show_pie_pic_self_2_3         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_manager_2_3      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_peer1_2_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_peer2_2_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_subordinate1_2_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_subordinate2_2_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_2_3' , 5 , 'none')

                show_pie_pic_self_2_4         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_manager_2_4      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_peer1_2_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_peer2_2_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_subordinate1_2_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_subordinate2_2_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_2_4' , 5 , 'none')

                show_pie_pic_self_2_5         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_manager_2_5      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_peer1_2_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_peer2_2_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_subordinate1_2_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_subordinate2_2_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_2_5' , 5 , 'none')

                show_pie_pic_self_total_2_1             = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_self_total_avg_2           = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_self_total_avg_2_1         = round(float(show_pie_pic_self_total_avg_2) if show_pie_pic_self_total_avg_2 is not None else 0  , 2)
                show_pie_pic_manager_total_2_1          = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_manager_total_avg_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_manager_total_avg_2_1      = round(float(show_pie_pic_manager_total_avg_2) if show_pie_pic_manager_total_avg_2 is not None else 0  , 2)
                show_pie_pic_peer1_total_2_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_peer1_total_avg_2          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_peer1_total_avg_2_1        = round(float(show_pie_pic_peer1_total_avg_2) if show_pie_pic_peer1_total_avg_2 is not None else 0  , 2)
                show_pie_pic_peer2_total_2_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_peer2_total_avg_2          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_peer2_total_avg_2_1        = round(float(show_pie_pic_peer2_total_avg_2) if show_pie_pic_peer2_total_avg_2 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_2_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_2   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_subordinate1_total_avg_2_1 = round(float(show_pie_pic_subordinate1_total_avg_2) if show_pie_pic_subordinate1_total_avg_2 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_2_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_2   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_subordinate2_total_avg_2_1 = round(float(show_pie_pic_subordinate2_total_avg_2) if show_pie_pic_subordinate2_total_avg_2 is not None else 0  , 2 )
                show_pie_pic_total_avg_2                = (float(show_pie_pic_self_total_avg_2_1)    + 
                                                           float(show_pie_pic_manager_total_avg_2_1) + 
                                                           float(show_pie_pic_peer1_total_avg_2_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_2_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_2_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_2_1) )/6 
                show_pie_pic_total_avg_2_1              = round(show_pie_pic_total_avg_2 , 2)

                ############
                # 工作品質
                ############
                show_pie_pic_self_3_1         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_manager_3_1      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_peer1_3_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_peer2_3_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_subordinate1_3_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_subordinate2_3_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_3_1' , 5 , 'none')

                show_pie_pic_self_3_2         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_manager_3_2      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_peer1_3_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_peer2_3_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_subordinate1_3_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_subordinate2_3_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_3_2' , 5 , 'none')
                
                show_pie_pic_self_3_3         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_manager_3_3      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_peer1_3_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_peer2_3_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_subordinate1_3_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_subordinate2_3_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_3_3' , 5 , 'none')

                show_pie_pic_self_3_4         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_manager_3_4      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_peer1_3_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_peer2_3_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_subordinate1_3_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_subordinate2_3_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_3_4' , 5 , 'none')

                show_pie_pic_self_3_5         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_manager_3_5      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_peer1_3_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_peer2_3_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_subordinate1_3_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_subordinate2_3_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_3_5' , 5 , 'none')

                show_pie_pic_self_total_3_1             = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_self_total_avg_3           = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_self_total_avg_3_1         = round(float(show_pie_pic_self_total_avg_3) if show_pie_pic_self_total_avg_3 is not None else 0  , 2)
                show_pie_pic_manager_total_3_1          = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_manager_total_avg_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_manager_total_avg_3_1      = round(float(show_pie_pic_manager_total_avg_3) if show_pie_pic_manager_total_avg_3 is not None else 0  , 2)
                show_pie_pic_peer1_total_3_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_peer1_total_avg_3          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_peer1_total_avg_3_1        = round(float(show_pie_pic_peer1_total_avg_3) if show_pie_pic_peer1_total_avg_3 is not None else 0  , 2)
                show_pie_pic_peer2_total_3_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_peer2_total_avg_3          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_peer2_total_avg_3_1        = round(float(show_pie_pic_peer2_total_avg_3) if show_pie_pic_peer2_total_avg_3 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_3_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_3   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_subordinate1_total_avg_3_1 = round(float(show_pie_pic_subordinate1_total_avg_3) if show_pie_pic_subordinate1_total_avg_3 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_3_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_3   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_subordinate2_total_avg_3_1 = round(float(show_pie_pic_subordinate2_total_avg_3) if show_pie_pic_subordinate2_total_avg_3 is not None else 0  , 2 )
                show_pie_pic_total_avg_3                = (float(show_pie_pic_self_total_avg_3_1)    + 
                                                           float(show_pie_pic_manager_total_avg_3_1) + 
                                                           float(show_pie_pic_peer1_total_avg_3_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_3_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_3_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_3_1) )/6 
                show_pie_pic_total_avg_3_1              = round(show_pie_pic_total_avg_3 , 2)
                
                ##################
                # 判斷力和決策能力
                ##################
                show_pie_pic_self_4_1         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_manager_4_1      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_peer1_4_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_peer2_4_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_subordinate1_4_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_subordinate2_4_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_4_1' , 5 , 'none')

                show_pie_pic_self_4_2         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_manager_4_2      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_peer1_4_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_peer2_4_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_subordinate1_4_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_subordinate2_4_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_4_2' , 5 , 'none')
                
                show_pie_pic_self_4_3         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_manager_4_3      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_peer1_4_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_peer2_4_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_subordinate1_4_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_subordinate2_4_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_4_3' , 5 , 'none')

                show_pie_pic_self_4_4         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_manager_4_4      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_peer1_4_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_peer2_4_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_subordinate1_4_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_subordinate2_4_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_4_4' , 5 , 'none')

                show_pie_pic_self_4_5         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_4_5' , 5 , 'none')
                show_pie_pic_manager_4_5      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_4_5' , 5 , 'none')
                show_pie_pic_peer1_4_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_4_5' , 5 , 'none')
                show_pie_pic_peer2_4_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_4_5' , 5 , 'none')
                show_pie_pic_subordinate1_4_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_4_5' , 5 , 'none')
                show_pie_pic_subordinate2_4_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_4_5' , 5 , 'none')

                show_pie_pic_self_total_4_1             = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_self_total_avg_4           = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_self_total_avg_4_1         = round(float(show_pie_pic_self_total_avg_4) if show_pie_pic_self_total_avg_4 is not None else 0  , 2)
                show_pie_pic_manager_total_4_1          = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_manager_total_avg_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_manager_total_avg_4_1      = round(float(show_pie_pic_manager_total_avg_4) if show_pie_pic_manager_total_avg_4 is not None else 0  , 2)
                show_pie_pic_peer1_total_4_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_peer1_total_avg_4          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_peer1_total_avg_4_1        = round(float(show_pie_pic_peer1_total_avg_4) if show_pie_pic_peer1_total_avg_4 is not None else 0  , 2)
                show_pie_pic_peer2_total_4_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_peer2_total_avg_4          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_peer2_total_avg_4_1        = round(float(show_pie_pic_peer2_total_avg_4) if show_pie_pic_peer2_total_avg_4 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_4_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_4   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_subordinate1_total_avg_4_1 = round(float(show_pie_pic_subordinate1_total_avg_4) if show_pie_pic_subordinate1_total_avg_4 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_4_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_4   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_subordinate2_total_avg_4_1 = round(float(show_pie_pic_subordinate2_total_avg_4) if show_pie_pic_subordinate2_total_avg_4 is not None else 0  , 2 )
                show_pie_pic_total_avg_4                = (float(show_pie_pic_self_total_avg_4_1)    + 
                                                           float(show_pie_pic_manager_total_avg_4_1) + 
                                                           float(show_pie_pic_peer1_total_avg_4_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_4_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_4_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_4_1) )/6 
                show_pie_pic_total_avg_4_1              = round(show_pie_pic_total_avg_4 , 2)
                
                ############
                # 其他能力
                ############
                show_pie_pic_self_5_1         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_manager_5_1      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_peer1_5_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_peer2_5_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_subordinate1_5_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_subordinate2_5_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_5_1' , 5 , 'none')

                show_pie_pic_self_5_2         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_manager_5_2      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_peer1_5_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_peer2_5_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_subordinate1_5_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_subordinate2_5_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_5_2' , 5 , 'none')
                
                show_pie_pic_self_5_3         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_manager_5_3      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_peer1_5_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_peer2_5_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_subordinate1_5_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_subordinate2_5_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_5_3' , 5 , 'none')

                show_pie_pic_self_5_4         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_5_4' , 5 , 'none')
                show_pie_pic_manager_5_4      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_5_4' , 5 , 'none')
                show_pie_pic_peer1_5_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_5_4' , 5 , 'none')
                show_pie_pic_peer2_5_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_5_4' , 5 , 'none')
                show_pie_pic_subordinate1_5_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_5_4' , 5 , 'none')
                show_pie_pic_subordinate2_5_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_5_4' , 5 , 'none')

                show_pie_pic_self_5_5         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_5_5' , 5 , 'none')
                show_pie_pic_manager_5_5      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_5_5' , 5 , 'none')
                show_pie_pic_peer1_5_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_5_5' , 5 , 'none')
                show_pie_pic_peer2_5_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_5_5' , 5 , 'none')
                show_pie_pic_subordinate1_5_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_5_5' , 5 , 'none')
                show_pie_pic_subordinate2_5_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_5_5' , 5 , 'none')

                show_pie_pic_self_5_6         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_5_6' , 5 , 'none')
                show_pie_pic_manager_5_6      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_5_6' , 5 , 'none')
                show_pie_pic_peer1_5_6        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_5_6' , 5 , 'none')
                show_pie_pic_peer2_5_6        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_5_6' , 5 , 'none')
                show_pie_pic_subordinate1_5_6 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_5_6' , 5 , 'none')
                show_pie_pic_subordinate2_5_6 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_5_6' , 5 , 'none')

                show_pie_pic_self_total_5_1             = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_self_total_avg_5           = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_self_total_avg_5_1         = round(float(show_pie_pic_self_total_avg_5) if show_pie_pic_self_total_avg_5 is not None else 0  , 2)
                show_pie_pic_manager_total_5_1          = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_manager_total_avg_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_manager_total_avg_5_1      = round(float(show_pie_pic_manager_total_avg_5) if show_pie_pic_manager_total_avg_5 is not None else 0  , 2)
                show_pie_pic_peer1_total_5_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_peer1_total_avg_5          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_peer1_total_avg_5_1        = round(float(show_pie_pic_peer1_total_avg_5) if show_pie_pic_peer1_total_avg_5 is not None else 0  , 2)
                show_pie_pic_peer2_total_5_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_peer2_total_avg_5          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_peer2_total_avg_5_1        = round(float(show_pie_pic_peer2_total_avg_5) if show_pie_pic_peer2_total_avg_5 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_5_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_5   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_subordinate1_total_avg_5_1 = round(float(show_pie_pic_subordinate1_total_avg_5) if show_pie_pic_subordinate1_total_avg_5 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_5_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_5   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_subordinate2_total_avg_5_1 = round(float(show_pie_pic_subordinate2_total_avg_5) if show_pie_pic_subordinate2_total_avg_5 is not None else 0  , 2 )
                show_pie_pic_total_avg_5                = (float(show_pie_pic_self_total_avg_5_1)    + 
                                                           float(show_pie_pic_manager_total_avg_5_1) + 
                                                           float(show_pie_pic_peer1_total_avg_5_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_5_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_5_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_5_1) )/6 
                show_pie_pic_total_avg_5_1              = round(show_pie_pic_total_avg_5 , 2)
                
                
                

                ############
                # 雷達圖
                ############
                show_radar_pic_num1 = ([float(show_pie_pic_self_total_avg_1_1) , float(show_pie_pic_self_total_avg_2_1) , float(show_pie_pic_self_total_avg_3_1) , float(show_pie_pic_self_total_avg_4_1) , float(show_pie_pic_self_total_avg_5_1) , ])
                show_radar_pic_num2 = ([float(show_pie_pic_manager_total_avg_1_1) , float(show_pie_pic_manager_total_avg_2_1) , float(show_pie_pic_manager_total_avg_3_1) , float(show_pie_pic_manager_total_avg_4_1) , float(show_pie_pic_manager_total_avg_5_1) , ])
                show_radar_pic_num3 = ([float(show_pie_pic_peer1_total_avg_1_1) , float(show_pie_pic_peer1_total_avg_2_1) , float(show_pie_pic_peer1_total_avg_3_1) , float(show_pie_pic_peer1_total_avg_4_1) , float(show_pie_pic_peer1_total_avg_5_1) , ])
                show_radar_pic_num4 = ([float(show_pie_pic_peer2_total_avg_1_1) , float(show_pie_pic_peer2_total_avg_2_1) , float(show_pie_pic_peer2_total_avg_3_1) , float(show_pie_pic_peer2_total_avg_4_1) , float(show_pie_pic_peer2_total_avg_5_1) , ])
                show_radar_pic_num5 = ([float(show_pie_pic_subordinate1_total_avg_1_1) , float(show_pie_pic_subordinate1_total_avg_2_1) , float(show_pie_pic_subordinate1_total_avg_3_1) , float(show_pie_pic_subordinate1_total_avg_4_1) , float(show_pie_pic_subordinate1_total_avg_5_1) , ])
                show_radar_pic_num6 = ([float(show_pie_pic_subordinate2_total_avg_1_1) , float(show_pie_pic_subordinate2_total_avg_2_1) , float(show_pie_pic_subordinate2_total_avg_3_1) , float(show_pie_pic_subordinate2_total_avg_4_1) , float(show_pie_pic_subordinate2_total_avg_5_1) , ])
                show_radar_pic      = db.show_radar_picture2(show_radar_pic_num1 , show_radar_pic_num2 , show_radar_pic_num3 , show_radar_pic_num4 , show_radar_pic_num5 , show_radar_pic_num6)

                return render_template('ajax/load_hr_360_dep_member_process_list_res2_2_print.html' , 
                                    show_hr_360_person_1_check_data=show_hr_360_person_1_check_data , s_name=s_name , 
                                    
                                    #####################################
                                    # 對於客戶的服務(包含內部客戶或外部客戶)
                                    #####################################
                                    show_pie_pic_self_1_1=show_pie_pic_self_1_1 ,
                                    show_pie_pic_manager_1_1=show_pie_pic_manager_1_1 , 
                                    show_pie_pic_peer1_1_1=show_pie_pic_peer1_1_1 , 
                                    show_pie_pic_peer2_1_1=show_pie_pic_peer2_1_1 ,
                                    show_pie_pic_subordinate1_1_1=show_pie_pic_subordinate1_1_1 , 
                                    show_pie_pic_subordinate2_1_1=show_pie_pic_subordinate2_1_1 ,

                                    show_pie_pic_self_1_2=show_pie_pic_self_1_2 , 
                                    show_pie_pic_manager_1_2=show_pie_pic_manager_1_2 , 
                                    show_pie_pic_peer1_1_2=show_pie_pic_peer1_1_2 , 
                                    show_pie_pic_peer2_1_2=show_pie_pic_peer2_1_2 ,
                                    show_pie_pic_subordinate1_1_2=show_pie_pic_subordinate1_1_2 , 
                                    show_pie_pic_subordinate2_1_2=show_pie_pic_subordinate2_1_2 , 

                                    show_pie_pic_self_1_3=show_pie_pic_self_1_3 , 
                                    show_pie_pic_manager_1_3=show_pie_pic_manager_1_3 , 
                                    show_pie_pic_peer1_1_3=show_pie_pic_peer1_1_3 , 
                                    show_pie_pic_peer2_1_3=show_pie_pic_peer2_1_3 ,
                                    show_pie_pic_subordinate1_1_3=show_pie_pic_subordinate1_1_3 , 
                                    show_pie_pic_subordinate2_1_3=show_pie_pic_subordinate2_1_3 ,

                                    show_pie_pic_self_1_4=show_pie_pic_self_1_4 , 
                                    show_pie_pic_manager_1_4=show_pie_pic_manager_1_4 , 
                                    show_pie_pic_peer1_1_4=show_pie_pic_peer1_1_4 , 
                                    show_pie_pic_peer2_1_4=show_pie_pic_peer2_1_4 ,
                                    show_pie_pic_subordinate1_1_4=show_pie_pic_subordinate1_1_4 , 
                                    show_pie_pic_subordinate2_1_4=show_pie_pic_subordinate2_1_4 , 

                                    show_pie_pic_self_1_5=show_pie_pic_self_1_5 , 
                                    show_pie_pic_manager_1_5=show_pie_pic_manager_1_5 , 
                                    show_pie_pic_peer1_1_5=show_pie_pic_peer1_1_5 , 
                                    show_pie_pic_peer2_1_5=show_pie_pic_peer2_1_5 ,
                                    show_pie_pic_subordinate1_1_5=show_pie_pic_subordinate1_1_5 , 
                                    show_pie_pic_subordinate2_1_5=show_pie_pic_subordinate2_1_5 , 

                                    show_pie_pic_self_total_1_1=show_pie_pic_self_total_1_1 ,
                                    show_pie_pic_self_total_avg_1_1=show_pie_pic_self_total_avg_1_1 ,
                                    show_pie_pic_manager_total_1_1=show_pie_pic_manager_total_1_1 ,
                                    show_pie_pic_manager_total_avg_1_1=show_pie_pic_manager_total_avg_1_1 ,
                                    show_pie_pic_peer1_total_1_1=show_pie_pic_peer1_total_1_1 ,
                                    show_pie_pic_peer1_total_avg_1_1=show_pie_pic_peer1_total_avg_1_1 ,
                                    show_pie_pic_peer2_total_1_1=show_pie_pic_peer2_total_1_1 ,
                                    show_pie_pic_peer2_total_avg_1_1=show_pie_pic_peer2_total_avg_1_1 ,
                                    show_pie_pic_subordinate1_total_1_1=show_pie_pic_subordinate1_total_1_1 ,
                                    show_pie_pic_subordinate1_total_avg_1_1=show_pie_pic_subordinate1_total_avg_1_1 ,
                                    show_pie_pic_subordinate2_total_1_1=show_pie_pic_subordinate2_total_1_1 ,
                                    show_pie_pic_subordinate2_total_avg_1_1=show_pie_pic_subordinate2_total_avg_1_1 ,
                                    show_pie_pic_total_avg_1_1=show_pie_pic_total_avg_1_1 ,
                                    
                                    ####################
                                    # 溝通與待人接物能力
                                    ####################
                                    show_pie_pic_self_2_1=show_pie_pic_self_2_1 ,
                                    show_pie_pic_manager_2_1=show_pie_pic_manager_2_1 , 
                                    show_pie_pic_peer1_2_1=show_pie_pic_peer1_2_1 , 
                                    show_pie_pic_peer2_2_1=show_pie_pic_peer2_2_1 ,
                                    show_pie_pic_subordinate1_2_1=show_pie_pic_subordinate1_2_1 , 
                                    show_pie_pic_subordinate2_2_1=show_pie_pic_subordinate2_2_1 ,

                                    show_pie_pic_self_2_2=show_pie_pic_self_2_2 , 
                                    show_pie_pic_manager_2_2=show_pie_pic_manager_2_2 , 
                                    show_pie_pic_peer1_2_2=show_pie_pic_peer1_2_2 , 
                                    show_pie_pic_peer2_2_2=show_pie_pic_peer2_2_2 ,
                                    show_pie_pic_subordinate1_2_2=show_pie_pic_subordinate1_2_2 , 
                                    show_pie_pic_subordinate2_2_2=show_pie_pic_subordinate2_2_2 , 

                                    show_pie_pic_self_2_3=show_pie_pic_self_2_3 , 
                                    show_pie_pic_manager_2_3=show_pie_pic_manager_2_3 , 
                                    show_pie_pic_peer1_2_3=show_pie_pic_peer1_2_3 , 
                                    show_pie_pic_peer2_2_3=show_pie_pic_peer2_2_3 ,
                                    show_pie_pic_subordinate1_2_3=show_pie_pic_subordinate1_2_3 , 
                                    show_pie_pic_subordinate2_2_3=show_pie_pic_subordinate2_2_3 ,

                                    show_pie_pic_self_2_4=show_pie_pic_self_2_4 , 
                                    show_pie_pic_manager_2_4=show_pie_pic_manager_2_4 , 
                                    show_pie_pic_peer1_2_4=show_pie_pic_peer1_2_4 , 
                                    show_pie_pic_peer2_2_4=show_pie_pic_peer2_2_4 ,
                                    show_pie_pic_subordinate1_2_4=show_pie_pic_subordinate1_2_4 , 
                                    show_pie_pic_subordinate2_2_4=show_pie_pic_subordinate2_2_4 , 

                                    show_pie_pic_self_2_5=show_pie_pic_self_2_5 , 
                                    show_pie_pic_manager_2_5=show_pie_pic_manager_2_5 , 
                                    show_pie_pic_peer1_2_5=show_pie_pic_peer1_2_5 , 
                                    show_pie_pic_peer2_2_5=show_pie_pic_peer2_2_5 ,
                                    show_pie_pic_subordinate1_2_5=show_pie_pic_subordinate1_2_5 , 
                                    show_pie_pic_subordinate2_2_5=show_pie_pic_subordinate2_2_5 , 
                                    
                                    show_pie_pic_self_total_2_1=show_pie_pic_self_total_2_1 ,
                                    show_pie_pic_self_total_avg_2_1=show_pie_pic_self_total_avg_2_1 ,
                                    show_pie_pic_manager_total_2_1=show_pie_pic_manager_total_2_1 ,
                                    show_pie_pic_manager_total_avg_2_1=show_pie_pic_manager_total_avg_2_1 ,
                                    show_pie_pic_peer1_total_2_1=show_pie_pic_peer1_total_2_1 ,
                                    show_pie_pic_peer1_total_avg_2_1=show_pie_pic_peer1_total_avg_2_1 ,
                                    show_pie_pic_peer2_total_2_1=show_pie_pic_peer2_total_2_1 ,
                                    show_pie_pic_peer2_total_avg_2_1=show_pie_pic_peer2_total_avg_2_1 ,
                                    show_pie_pic_subordinate1_total_2_1=show_pie_pic_subordinate1_total_2_1 ,
                                    show_pie_pic_subordinate1_total_avg_2_1=show_pie_pic_subordinate1_total_avg_2_1 ,
                                    show_pie_pic_subordinate2_total_2_1=show_pie_pic_subordinate2_total_2_1 ,
                                    show_pie_pic_subordinate2_total_avg_2_1=show_pie_pic_subordinate2_total_avg_2_1 ,
                                    show_pie_pic_total_avg_2_1=show_pie_pic_total_avg_2_1 ,
                                    
                                    ############
                                    # 工作品質
                                    ############
                                    show_pie_pic_self_3_1=show_pie_pic_self_3_1 ,
                                    show_pie_pic_manager_3_1=show_pie_pic_manager_3_1 , 
                                    show_pie_pic_peer1_3_1=show_pie_pic_peer1_3_1 , 
                                    show_pie_pic_peer2_3_1=show_pie_pic_peer2_3_1 ,
                                    show_pie_pic_subordinate1_3_1=show_pie_pic_subordinate1_3_1 , 
                                    show_pie_pic_subordinate2_3_1=show_pie_pic_subordinate2_3_1 ,

                                    show_pie_pic_self_3_2=show_pie_pic_self_3_2 , 
                                    show_pie_pic_manager_3_2=show_pie_pic_manager_3_2 , 
                                    show_pie_pic_peer1_3_2=show_pie_pic_peer1_3_2 , 
                                    show_pie_pic_peer2_3_2=show_pie_pic_peer2_3_2 ,
                                    show_pie_pic_subordinate1_3_2=show_pie_pic_subordinate1_3_2 , 
                                    show_pie_pic_subordinate2_3_2=show_pie_pic_subordinate2_3_2 , 

                                    show_pie_pic_self_3_3=show_pie_pic_self_3_3 , 
                                    show_pie_pic_manager_3_3=show_pie_pic_manager_3_3 , 
                                    show_pie_pic_peer1_3_3=show_pie_pic_peer1_3_3 , 
                                    show_pie_pic_peer2_3_3=show_pie_pic_peer2_3_3 ,
                                    show_pie_pic_subordinate1_3_3=show_pie_pic_subordinate1_3_3 , 
                                    show_pie_pic_subordinate2_3_3=show_pie_pic_subordinate2_3_3 ,

                                    show_pie_pic_self_3_4=show_pie_pic_self_3_4 , 
                                    show_pie_pic_manager_3_4=show_pie_pic_manager_3_4 , 
                                    show_pie_pic_peer1_3_4=show_pie_pic_peer1_3_4 , 
                                    show_pie_pic_peer2_3_4=show_pie_pic_peer2_3_4 ,
                                    show_pie_pic_subordinate1_3_4=show_pie_pic_subordinate1_3_4 , 
                                    show_pie_pic_subordinate2_3_4=show_pie_pic_subordinate2_3_4 , 

                                    show_pie_pic_self_3_5=show_pie_pic_self_3_5 , 
                                    show_pie_pic_manager_3_5=show_pie_pic_manager_3_5 , 
                                    show_pie_pic_peer1_3_5=show_pie_pic_peer1_3_5 , 
                                    show_pie_pic_peer2_3_5=show_pie_pic_peer2_3_5 ,
                                    show_pie_pic_subordinate1_3_5=show_pie_pic_subordinate1_3_5 , 
                                    show_pie_pic_subordinate2_3_5=show_pie_pic_subordinate2_3_5 , 
                                    
                                    show_pie_pic_self_total_3_1=show_pie_pic_self_total_3_1 ,
                                    show_pie_pic_self_total_avg_3_1=show_pie_pic_self_total_avg_3_1 ,
                                    show_pie_pic_manager_total_3_1=show_pie_pic_manager_total_3_1 ,
                                    show_pie_pic_manager_total_avg_3_1=show_pie_pic_manager_total_avg_3_1 ,
                                    show_pie_pic_peer1_total_3_1=show_pie_pic_peer1_total_3_1 ,
                                    show_pie_pic_peer1_total_avg_3_1=show_pie_pic_peer1_total_avg_3_1 ,
                                    show_pie_pic_peer2_total_3_1=show_pie_pic_peer2_total_3_1 ,
                                    show_pie_pic_peer2_total_avg_3_1=show_pie_pic_peer2_total_avg_3_1 ,
                                    show_pie_pic_subordinate1_total_3_1=show_pie_pic_subordinate1_total_3_1 ,
                                    show_pie_pic_subordinate1_total_avg_3_1=show_pie_pic_subordinate1_total_avg_3_1 ,
                                    show_pie_pic_subordinate2_total_3_1=show_pie_pic_subordinate2_total_3_1 ,
                                    show_pie_pic_subordinate2_total_avg_3_1=show_pie_pic_subordinate2_total_avg_3_1 ,
                                    show_pie_pic_total_avg_3_1=show_pie_pic_total_avg_3_1 ,
                                    
                                    ##################
                                    # 判斷力和決策能力
                                    ##################
                                    show_pie_pic_self_4_1=show_pie_pic_self_4_1 ,
                                    show_pie_pic_manager_4_1=show_pie_pic_manager_4_1 , 
                                    show_pie_pic_peer1_4_1=show_pie_pic_peer1_4_1 , 
                                    show_pie_pic_peer2_4_1=show_pie_pic_peer2_4_1 ,
                                    show_pie_pic_subordinate1_4_1=show_pie_pic_subordinate1_4_1 , 
                                    show_pie_pic_subordinate2_4_1=show_pie_pic_subordinate2_4_1 ,

                                    show_pie_pic_self_4_2=show_pie_pic_self_4_2 , 
                                    show_pie_pic_manager_4_2=show_pie_pic_manager_4_2 , 
                                    show_pie_pic_peer1_4_2=show_pie_pic_peer1_4_2 , 
                                    show_pie_pic_peer2_4_2=show_pie_pic_peer2_4_2 ,
                                    show_pie_pic_subordinate1_4_2=show_pie_pic_subordinate1_4_2 , 
                                    show_pie_pic_subordinate2_4_2=show_pie_pic_subordinate2_4_2 , 

                                    show_pie_pic_self_4_3=show_pie_pic_self_4_3 , 
                                    show_pie_pic_manager_4_3=show_pie_pic_manager_4_3 , 
                                    show_pie_pic_peer1_4_3=show_pie_pic_peer1_4_3 , 
                                    show_pie_pic_peer2_4_3=show_pie_pic_peer2_4_3 ,
                                    show_pie_pic_subordinate1_4_3=show_pie_pic_subordinate1_4_3 , 
                                    show_pie_pic_subordinate2_4_3=show_pie_pic_subordinate2_4_3 ,

                                    show_pie_pic_self_4_4=show_pie_pic_self_4_4 , 
                                    show_pie_pic_manager_4_4=show_pie_pic_manager_4_4 , 
                                    show_pie_pic_peer1_4_4=show_pie_pic_peer1_4_4 , 
                                    show_pie_pic_peer2_4_4=show_pie_pic_peer2_4_4 ,
                                    show_pie_pic_subordinate1_4_4=show_pie_pic_subordinate1_4_4 , 
                                    show_pie_pic_subordinate2_4_4=show_pie_pic_subordinate2_4_4 , 

                                    show_pie_pic_self_4_5=show_pie_pic_self_4_5 , 
                                    show_pie_pic_manager_4_5=show_pie_pic_manager_4_5 , 
                                    show_pie_pic_peer1_4_5=show_pie_pic_peer1_4_5 , 
                                    show_pie_pic_peer2_4_5=show_pie_pic_peer2_4_5 ,
                                    show_pie_pic_subordinate1_4_5=show_pie_pic_subordinate1_4_5 , 
                                    show_pie_pic_subordinate2_4_5=show_pie_pic_subordinate2_4_5 , 

                                    show_pie_pic_self_total_4_1=show_pie_pic_self_total_4_1 ,
                                    show_pie_pic_self_total_avg_4_1=show_pie_pic_self_total_avg_4_1 ,
                                    show_pie_pic_manager_total_4_1=show_pie_pic_manager_total_4_1 ,
                                    show_pie_pic_manager_total_avg_4_1=show_pie_pic_manager_total_avg_4_1 ,
                                    show_pie_pic_peer1_total_4_1=show_pie_pic_peer1_total_4_1 ,
                                    show_pie_pic_peer1_total_avg_4_1=show_pie_pic_peer1_total_avg_4_1 ,
                                    show_pie_pic_peer2_total_4_1=show_pie_pic_peer2_total_4_1 ,
                                    show_pie_pic_peer2_total_avg_4_1=show_pie_pic_peer2_total_avg_4_1 ,
                                    show_pie_pic_subordinate1_total_4_1=show_pie_pic_subordinate1_total_4_1 ,
                                    show_pie_pic_subordinate1_total_avg_4_1=show_pie_pic_subordinate1_total_avg_4_1 ,
                                    show_pie_pic_subordinate2_total_4_1=show_pie_pic_subordinate2_total_4_1 ,
                                    show_pie_pic_subordinate2_total_avg_4_1=show_pie_pic_subordinate2_total_avg_4_1 ,
                                    show_pie_pic_total_avg_4_1=show_pie_pic_total_avg_4_1 ,
                                    
                                    ############
                                    # 其他能力
                                    ############
                                    show_pie_pic_self_5_1=show_pie_pic_self_5_1 ,
                                    show_pie_pic_manager_5_1=show_pie_pic_manager_5_1 , 
                                    show_pie_pic_peer1_5_1=show_pie_pic_peer1_5_1 , 
                                    show_pie_pic_peer2_5_1=show_pie_pic_peer2_5_1 ,
                                    show_pie_pic_subordinate1_5_1=show_pie_pic_subordinate1_5_1 , 
                                    show_pie_pic_subordinate2_5_1=show_pie_pic_subordinate2_5_1 ,

                                    show_pie_pic_self_5_2=show_pie_pic_self_5_2 , 
                                    show_pie_pic_manager_5_2=show_pie_pic_manager_5_2 , 
                                    show_pie_pic_peer1_5_2=show_pie_pic_peer1_5_2 , 
                                    show_pie_pic_peer2_5_2=show_pie_pic_peer2_5_2 ,
                                    show_pie_pic_subordinate1_5_2=show_pie_pic_subordinate1_5_2 , 
                                    show_pie_pic_subordinate2_5_2=show_pie_pic_subordinate2_5_2 , 

                                    show_pie_pic_self_5_3=show_pie_pic_self_5_3 , 
                                    show_pie_pic_manager_5_3=show_pie_pic_manager_5_3 , 
                                    show_pie_pic_peer1_5_3=show_pie_pic_peer1_5_3 , 
                                    show_pie_pic_peer2_5_3=show_pie_pic_peer2_5_3 ,
                                    show_pie_pic_subordinate1_5_3=show_pie_pic_subordinate1_5_3 , 
                                    show_pie_pic_subordinate2_5_3=show_pie_pic_subordinate2_5_3 ,

                                    show_pie_pic_self_5_4=show_pie_pic_self_5_4 , 
                                    show_pie_pic_manager_5_4=show_pie_pic_manager_5_4 , 
                                    show_pie_pic_peer1_5_4=show_pie_pic_peer1_5_4 , 
                                    show_pie_pic_peer2_5_4=show_pie_pic_peer2_5_4 ,
                                    show_pie_pic_subordinate1_5_4=show_pie_pic_subordinate1_5_4 , 
                                    show_pie_pic_subordinate2_5_4=show_pie_pic_subordinate2_5_4 ,

                                    show_pie_pic_self_5_5=show_pie_pic_self_5_5 , 
                                    show_pie_pic_manager_5_5=show_pie_pic_manager_5_5 , 
                                    show_pie_pic_peer1_5_5=show_pie_pic_peer1_5_5 , 
                                    show_pie_pic_peer2_5_5=show_pie_pic_peer2_5_5 ,
                                    show_pie_pic_subordinate1_5_5=show_pie_pic_subordinate1_5_5 , 
                                    show_pie_pic_subordinate2_5_5=show_pie_pic_subordinate2_5_5 ,

                                    show_pie_pic_self_5_6=show_pie_pic_self_5_6 , 
                                    show_pie_pic_manager_5_6=show_pie_pic_manager_5_6 , 
                                    show_pie_pic_peer1_5_6=show_pie_pic_peer1_5_6 , 
                                    show_pie_pic_peer2_5_6=show_pie_pic_peer2_5_6 ,
                                    show_pie_pic_subordinate1_5_6=show_pie_pic_subordinate1_5_6 , 
                                    show_pie_pic_subordinate2_5_6=show_pie_pic_subordinate2_5_6 ,

                                    show_pie_pic_self_total_5_1=show_pie_pic_self_total_5_1 ,
                                    show_pie_pic_self_total_avg_5_1=show_pie_pic_self_total_avg_5_1 ,
                                    show_pie_pic_manager_total_5_1=show_pie_pic_manager_total_5_1 ,
                                    show_pie_pic_manager_total_avg_5_1=show_pie_pic_manager_total_avg_5_1 ,
                                    show_pie_pic_peer1_total_5_1=show_pie_pic_peer1_total_5_1 ,
                                    show_pie_pic_peer1_total_avg_5_1=show_pie_pic_peer1_total_avg_5_1 ,
                                    show_pie_pic_peer2_total_5_1=show_pie_pic_peer2_total_5_1 ,
                                    show_pie_pic_peer2_total_avg_5_1=show_pie_pic_peer2_total_avg_5_1 ,
                                    show_pie_pic_subordinate1_total_5_1=show_pie_pic_subordinate1_total_5_1 ,
                                    show_pie_pic_subordinate1_total_avg_5_1=show_pie_pic_subordinate1_total_avg_5_1 ,
                                    show_pie_pic_subordinate2_total_5_1=show_pie_pic_subordinate2_total_5_1 ,
                                    show_pie_pic_subordinate2_total_avg_5_1=show_pie_pic_subordinate2_total_avg_5_1 ,
                                    show_pie_pic_total_avg_5_1=show_pie_pic_total_avg_5_1 ,

                                    #############
                                    # 綜合雷達圖
                                    #############
                                    show_radar_pic=show_radar_pic 
                                    
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

#####################################
# /show_hr_360_person_result2_2
#####################################
@app.route("/show_hr_360_person_result2_2", methods=['GET','POST'])
def show_hr_360_person_result2_2():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                s_name = request.form['s_name']

                ### operation record title
                operation_record_title = f'載入 HR - 360 考評 , 受評人員 : {s_name} 總分數資料'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ############
                # 考評人員
                ############
                show_hr_360_person_1_check_data = db.show_hr_360_person_process_total_data2_2(s_name)
                
                c_name         = db.search_hr_360_person_name(s_name , 'c_name')
                c_manager      = db.search_hr_360_person_name(s_name , 'c_manager')
                c_peer1        = db.search_hr_360_person_name(s_name , 'c_peer1')
                c_peer2        = db.search_hr_360_person_name(s_name , 'c_peer2')
                c_subordinate1 = db.search_hr_360_person_name(s_name , 'c_subordinate1')
                c_subordinate2 = db.search_hr_360_person_name(s_name , 'c_subordinate2')

                #####################################
                # 對於客戶的服務(包含內部客戶或外部客戶)
                #####################################
                show_pie_pic_self_1_1         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_manager_1_1      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_peer1_1_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_peer2_1_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_subordinate1_1_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_subordinate2_1_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_1_1' , 5 , 'none')

                show_pie_pic_self_1_2         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_manager_1_2      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_peer1_1_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_peer2_1_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_subordinate1_1_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_subordinate2_1_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_1_2' , 5 , 'none')
                
                show_pie_pic_self_1_3         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_manager_1_3      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_peer1_1_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_peer2_1_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_subordinate1_1_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_subordinate2_1_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_1_3' , 5 , 'none')

                show_pie_pic_self_1_4         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_manager_1_4      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_peer1_1_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_peer2_1_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_subordinate1_1_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_subordinate2_1_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_1_4' , 5 , 'none')

                show_pie_pic_self_1_5         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_manager_1_5      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_peer1_1_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_peer2_1_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_subordinate1_1_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_subordinate2_1_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_1_5' , 5 , 'none')
                

                show_pie_pic_self_total_1_1             = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_self_total_avg_1           = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_self_total_avg_1_1         = round(float(show_pie_pic_self_total_avg_1) , 2) if show_pie_pic_self_total_avg_1 is not None else 0 
                show_pie_pic_manager_total_1_1          = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_manager_total_avg_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_manager_total_avg_1_1      = round(float(show_pie_pic_manager_total_avg_1) , 2) if show_pie_pic_manager_total_avg_1 is not None else 0
                show_pie_pic_peer1_total_1_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_peer1_total_avg_1          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_peer1_total_avg_1_1        = round(float(show_pie_pic_peer1_total_avg_1) , 2) if show_pie_pic_peer1_total_avg_1 is not None else 0
                show_pie_pic_peer2_total_1_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_peer2_total_avg_1          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_peer2_total_avg_1_1        = round(float(show_pie_pic_peer2_total_avg_1) , 2) if show_pie_pic_peer2_total_avg_1 is not None else 0
                show_pie_pic_subordinate1_total_1_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_1   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_subordinate1_total_avg_1_1 = round(float(show_pie_pic_subordinate1_total_avg_1) , 2) if show_pie_pic_subordinate1_total_avg_1 is not None else 0
                show_pie_pic_subordinate2_total_1_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_1   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_subordinate2_total_avg_1_1 = round(float(show_pie_pic_subordinate2_total_avg_1) , 2) if show_pie_pic_subordinate2_total_avg_1 is not None else 0
                show_pie_pic_total_avg_1                = (
                                                           float(show_pie_pic_self_total_avg_1_1)     +
                                                           float(show_pie_pic_manager_total_avg_1_1)  + 
                                                           float(show_pie_pic_peer1_total_avg_1_1)     + 
                                                           float(show_pie_pic_peer2_total_avg_1_1)     + 
                                                           float(show_pie_pic_subordinate1_total_avg_1_1)   + 
                                                           float(show_pie_pic_subordinate2_total_avg_1_1))/6 
                show_pie_pic_total_avg_1_1              = round(show_pie_pic_total_avg_1 , 2)
                
                ####################
                # 溝通與待人接物能力
                ####################
                show_pie_pic_self_2_1         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_manager_2_1      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_peer1_2_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_peer2_2_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_subordinate1_2_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_subordinate2_2_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_2_1' , 5 , 'none')

                show_pie_pic_self_2_2         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_manager_2_2      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_peer1_2_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_peer2_2_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_subordinate1_2_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_subordinate2_2_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_2_2' , 5 , 'none')
                
                show_pie_pic_self_2_3         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_manager_2_3      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_peer1_2_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_peer2_2_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_subordinate1_2_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_subordinate2_2_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_2_3' , 5 , 'none')

                show_pie_pic_self_2_4         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_manager_2_4      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_peer1_2_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_peer2_2_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_subordinate1_2_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_subordinate2_2_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_2_4' , 5 , 'none')

                show_pie_pic_self_2_5         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_manager_2_5      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_peer1_2_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_peer2_2_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_subordinate1_2_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_subordinate2_2_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_2_5' , 5 , 'none')

                show_pie_pic_self_total_2_1             = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_self_total_avg_2           = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_self_total_avg_2_1         = round(float(show_pie_pic_self_total_avg_2) if show_pie_pic_self_total_avg_2 is not None else 0  , 2)
                show_pie_pic_manager_total_2_1          = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_manager_total_avg_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_manager_total_avg_2_1      = round(float(show_pie_pic_manager_total_avg_2) if show_pie_pic_manager_total_avg_2 is not None else 0  , 2)
                show_pie_pic_peer1_total_2_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_peer1_total_avg_2          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_peer1_total_avg_2_1        = round(float(show_pie_pic_peer1_total_avg_2) if show_pie_pic_peer1_total_avg_2 is not None else 0  , 2)
                show_pie_pic_peer2_total_2_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_peer2_total_avg_2          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_peer2_total_avg_2_1        = round(float(show_pie_pic_peer2_total_avg_2) if show_pie_pic_peer2_total_avg_2 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_2_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_2   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_subordinate1_total_avg_2_1 = round(float(show_pie_pic_subordinate1_total_avg_2) if show_pie_pic_subordinate1_total_avg_2 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_2_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_2   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_subordinate2_total_avg_2_1 = round(float(show_pie_pic_subordinate2_total_avg_2) if show_pie_pic_subordinate2_total_avg_2 is not None else 0  , 2 )
                show_pie_pic_total_avg_2                = (float(show_pie_pic_self_total_avg_2_1)    + 
                                                           float(show_pie_pic_manager_total_avg_2_1) + 
                                                           float(show_pie_pic_peer1_total_avg_2_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_2_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_2_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_2_1) )/6 
                show_pie_pic_total_avg_2_1              = round(show_pie_pic_total_avg_2 , 2)

                ############
                # 工作品質
                ############
                show_pie_pic_self_3_1         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_manager_3_1      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_peer1_3_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_peer2_3_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_subordinate1_3_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_subordinate2_3_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_3_1' , 5 , 'none')

                show_pie_pic_self_3_2         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_manager_3_2      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_peer1_3_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_peer2_3_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_subordinate1_3_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_subordinate2_3_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_3_2' , 5 , 'none')
                
                show_pie_pic_self_3_3         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_manager_3_3      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_peer1_3_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_peer2_3_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_subordinate1_3_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_subordinate2_3_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_3_3' , 5 , 'none')

                show_pie_pic_self_3_4         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_manager_3_4      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_peer1_3_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_peer2_3_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_subordinate1_3_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_subordinate2_3_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_3_4' , 5 , 'none')

                show_pie_pic_self_3_5         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_manager_3_5      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_peer1_3_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_peer2_3_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_subordinate1_3_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_subordinate2_3_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_3_5' , 5 , 'none')

                show_pie_pic_self_total_3_1             = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_self_total_avg_3           = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_self_total_avg_3_1         = round(float(show_pie_pic_self_total_avg_3) if show_pie_pic_self_total_avg_3 is not None else 0  , 2)
                show_pie_pic_manager_total_3_1          = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_manager_total_avg_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_manager_total_avg_3_1      = round(float(show_pie_pic_manager_total_avg_3) if show_pie_pic_manager_total_avg_3 is not None else 0  , 2)
                show_pie_pic_peer1_total_3_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_peer1_total_avg_3          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_peer1_total_avg_3_1        = round(float(show_pie_pic_peer1_total_avg_3) if show_pie_pic_peer1_total_avg_3 is not None else 0  , 2)
                show_pie_pic_peer2_total_3_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_peer2_total_avg_3          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_peer2_total_avg_3_1        = round(float(show_pie_pic_peer2_total_avg_3) if show_pie_pic_peer2_total_avg_3 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_3_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_3   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_subordinate1_total_avg_3_1 = round(float(show_pie_pic_subordinate1_total_avg_3) if show_pie_pic_subordinate1_total_avg_3 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_3_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_3   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_subordinate2_total_avg_3_1 = round(float(show_pie_pic_subordinate2_total_avg_3) if show_pie_pic_subordinate2_total_avg_3 is not None else 0  , 2 )
                show_pie_pic_total_avg_3                = (float(show_pie_pic_self_total_avg_3_1)    + 
                                                           float(show_pie_pic_manager_total_avg_3_1) + 
                                                           float(show_pie_pic_peer1_total_avg_3_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_3_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_3_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_3_1) )/6 
                show_pie_pic_total_avg_3_1              = round(show_pie_pic_total_avg_3 , 2)
                
                ##################
                # 判斷力和決策能力
                ##################
                show_pie_pic_self_4_1         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_manager_4_1      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_peer1_4_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_peer2_4_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_subordinate1_4_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_subordinate2_4_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_4_1' , 5 , 'none')

                show_pie_pic_self_4_2         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_manager_4_2      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_peer1_4_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_peer2_4_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_subordinate1_4_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_subordinate2_4_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_4_2' , 5 , 'none')
                
                show_pie_pic_self_4_3         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_manager_4_3      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_peer1_4_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_peer2_4_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_subordinate1_4_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_subordinate2_4_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_4_3' , 5 , 'none')

                show_pie_pic_self_4_4         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_manager_4_4      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_peer1_4_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_peer2_4_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_subordinate1_4_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_subordinate2_4_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_4_4' , 5 , 'none')

                show_pie_pic_self_4_5         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_4_5' , 5 , 'none')
                show_pie_pic_manager_4_5      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_4_5' , 5 , 'none')
                show_pie_pic_peer1_4_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_4_5' , 5 , 'none')
                show_pie_pic_peer2_4_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_4_5' , 5 , 'none')
                show_pie_pic_subordinate1_4_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_4_5' , 5 , 'none')
                show_pie_pic_subordinate2_4_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_4_5' , 5 , 'none')

                show_pie_pic_self_total_4_1             = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_self_total_avg_4           = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_self_total_avg_4_1         = round(float(show_pie_pic_self_total_avg_4) if show_pie_pic_self_total_avg_4 is not None else 0  , 2)
                show_pie_pic_manager_total_4_1          = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_manager_total_avg_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_manager_total_avg_4_1      = round(float(show_pie_pic_manager_total_avg_4) if show_pie_pic_manager_total_avg_4 is not None else 0  , 2)
                show_pie_pic_peer1_total_4_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_peer1_total_avg_4          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_peer1_total_avg_4_1        = round(float(show_pie_pic_peer1_total_avg_4) if show_pie_pic_peer1_total_avg_4 is not None else 0  , 2)
                show_pie_pic_peer2_total_4_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_peer2_total_avg_4          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_peer2_total_avg_4_1        = round(float(show_pie_pic_peer2_total_avg_4) if show_pie_pic_peer2_total_avg_4 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_4_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_4   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_subordinate1_total_avg_4_1 = round(float(show_pie_pic_subordinate1_total_avg_4) if show_pie_pic_subordinate1_total_avg_4 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_4_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_4   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_subordinate2_total_avg_4_1 = round(float(show_pie_pic_subordinate2_total_avg_4) if show_pie_pic_subordinate2_total_avg_4 is not None else 0  , 2 )
                show_pie_pic_total_avg_4                = (float(show_pie_pic_self_total_avg_4_1)    + 
                                                           float(show_pie_pic_manager_total_avg_4_1) + 
                                                           float(show_pie_pic_peer1_total_avg_4_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_4_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_4_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_4_1) )/6 
                show_pie_pic_total_avg_4_1              = round(show_pie_pic_total_avg_4 , 2)
                
                ############
                # 其他能力
                ############
                show_pie_pic_self_5_1         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_manager_5_1      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_peer1_5_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_peer2_5_1        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_subordinate1_5_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_subordinate2_5_1 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_5_1' , 5 , 'none')

                show_pie_pic_self_5_2         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_manager_5_2      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_peer1_5_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_peer2_5_2        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_subordinate1_5_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_subordinate2_5_2 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_5_2' , 5 , 'none')
                
                show_pie_pic_self_5_3         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_manager_5_3      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_peer1_5_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_peer2_5_3        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_subordinate1_5_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_subordinate2_5_3 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_5_3' , 5 , 'none')

                show_pie_pic_self_5_4         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_5_4' , 5 , 'none')
                show_pie_pic_manager_5_4      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_5_4' , 5 , 'none')
                show_pie_pic_peer1_5_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_5_4' , 5 , 'none')
                show_pie_pic_peer2_5_4        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_5_4' , 5 , 'none')
                show_pie_pic_subordinate1_5_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_5_4' , 5 , 'none')
                show_pie_pic_subordinate2_5_4 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_5_4' , 5 , 'none')

                show_pie_pic_self_5_5         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_5_5' , 5 , 'none')
                show_pie_pic_manager_5_5      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_5_5' , 5 , 'none')
                show_pie_pic_peer1_5_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_5_5' , 5 , 'none')
                show_pie_pic_peer2_5_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_5_5' , 5 , 'none')
                show_pie_pic_subordinate1_5_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_5_5' , 5 , 'none')
                show_pie_pic_subordinate2_5_5 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_5_5' , 5 , 'none')

                show_pie_pic_self_5_6         = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_5_6' , 5 , 'none')
                show_pie_pic_manager_5_6      = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_5_6' , 5 , 'none')
                show_pie_pic_peer1_5_6        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_5_6' , 5 , 'none')
                show_pie_pic_peer2_5_6        = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_5_6' , 5 , 'none')
                show_pie_pic_subordinate1_5_6 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_5_6' , 5 , 'none')
                show_pie_pic_subordinate2_5_6 = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_5_6' , 5 , 'none')

                show_pie_pic_self_total_5_1             = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_self_total_avg_5           = db.show_hr_360_person_process_total_data3_2(s_name , c_name         , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_self_total_avg_5_1         = round(float(show_pie_pic_self_total_avg_5) if show_pie_pic_self_total_avg_5 is not None else 0  , 2)
                show_pie_pic_manager_total_5_1          = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_manager_total_avg_5        = db.show_hr_360_person_process_total_data3_2(s_name , c_manager      , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_manager_total_avg_5_1      = round(float(show_pie_pic_manager_total_avg_5) if show_pie_pic_manager_total_avg_5 is not None else 0  , 2)
                show_pie_pic_peer1_total_5_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_peer1_total_avg_5          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer1        , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_peer1_total_avg_5_1        = round(float(show_pie_pic_peer1_total_avg_5) if show_pie_pic_peer1_total_avg_5 is not None else 0  , 2)
                show_pie_pic_peer2_total_5_1            = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_peer2_total_avg_5          = db.show_hr_360_person_process_total_data3_2(s_name , c_peer2        , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_peer2_total_avg_5_1        = round(float(show_pie_pic_peer2_total_avg_5) if show_pie_pic_peer2_total_avg_5 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_5_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_5   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate1 , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_subordinate1_total_avg_5_1 = round(float(show_pie_pic_subordinate1_total_avg_5) if show_pie_pic_subordinate1_total_avg_5 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_5_1     = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_5   = db.show_hr_360_person_process_total_data3_2(s_name , c_subordinate2 , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_subordinate2_total_avg_5_1 = round(float(show_pie_pic_subordinate2_total_avg_5) if show_pie_pic_subordinate2_total_avg_5 is not None else 0  , 2 )
                show_pie_pic_total_avg_5                = (float(show_pie_pic_self_total_avg_5_1)    + 
                                                           float(show_pie_pic_manager_total_avg_5_1) + 
                                                           float(show_pie_pic_peer1_total_avg_5_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_5_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_5_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_5_1) )/6 
                show_pie_pic_total_avg_5_1              = round(show_pie_pic_total_avg_5 , 2)
                
                
                

                ############
                # 雷達圖
                ############
                show_radar_pic_num1 = ([float(show_pie_pic_self_total_avg_1_1) , float(show_pie_pic_self_total_avg_2_1) , float(show_pie_pic_self_total_avg_3_1) , float(show_pie_pic_self_total_avg_4_1) , float(show_pie_pic_self_total_avg_5_1) , ])
                show_radar_pic_num2 = ([float(show_pie_pic_manager_total_avg_1_1) , float(show_pie_pic_manager_total_avg_2_1) , float(show_pie_pic_manager_total_avg_3_1) , float(show_pie_pic_manager_total_avg_4_1) , float(show_pie_pic_manager_total_avg_5_1) , ])
                show_radar_pic_num3 = ([float(show_pie_pic_peer1_total_avg_1_1) , float(show_pie_pic_peer1_total_avg_2_1) , float(show_pie_pic_peer1_total_avg_3_1) , float(show_pie_pic_peer1_total_avg_4_1) , float(show_pie_pic_peer1_total_avg_5_1) , ])
                show_radar_pic_num4 = ([float(show_pie_pic_peer2_total_avg_1_1) , float(show_pie_pic_peer2_total_avg_2_1) , float(show_pie_pic_peer2_total_avg_3_1) , float(show_pie_pic_peer2_total_avg_4_1) , float(show_pie_pic_peer2_total_avg_5_1) , ])
                show_radar_pic_num5 = ([float(show_pie_pic_subordinate1_total_avg_1_1) , float(show_pie_pic_subordinate1_total_avg_2_1) , float(show_pie_pic_subordinate1_total_avg_3_1) , float(show_pie_pic_subordinate1_total_avg_4_1) , float(show_pie_pic_subordinate1_total_avg_5_1) , ])
                show_radar_pic_num6 = ([float(show_pie_pic_subordinate2_total_avg_1_1) , float(show_pie_pic_subordinate2_total_avg_2_1) , float(show_pie_pic_subordinate2_total_avg_3_1) , float(show_pie_pic_subordinate2_total_avg_4_1) , float(show_pie_pic_subordinate2_total_avg_5_1) , ])
                show_radar_pic      = db.show_radar_picture2(show_radar_pic_num1 , show_radar_pic_num2 , show_radar_pic_num3 , show_radar_pic_num4 , show_radar_pic_num5 , show_radar_pic_num6)

                return render_template('ajax/load_hr_360_dep_member_process_list_res2_2.html' , 
                                    show_hr_360_person_1_check_data=show_hr_360_person_1_check_data , s_name=s_name , 
                                    
                                    #####################################
                                    # 對於客戶的服務(包含內部客戶或外部客戶)
                                    #####################################
                                    show_pie_pic_self_1_1=show_pie_pic_self_1_1 ,
                                    show_pie_pic_manager_1_1=show_pie_pic_manager_1_1 , 
                                    show_pie_pic_peer1_1_1=show_pie_pic_peer1_1_1 , 
                                    show_pie_pic_peer2_1_1=show_pie_pic_peer2_1_1 ,
                                    show_pie_pic_subordinate1_1_1=show_pie_pic_subordinate1_1_1 , 
                                    show_pie_pic_subordinate2_1_1=show_pie_pic_subordinate2_1_1 ,

                                    show_pie_pic_self_1_2=show_pie_pic_self_1_2 , 
                                    show_pie_pic_manager_1_2=show_pie_pic_manager_1_2 , 
                                    show_pie_pic_peer1_1_2=show_pie_pic_peer1_1_2 , 
                                    show_pie_pic_peer2_1_2=show_pie_pic_peer2_1_2 ,
                                    show_pie_pic_subordinate1_1_2=show_pie_pic_subordinate1_1_2 , 
                                    show_pie_pic_subordinate2_1_2=show_pie_pic_subordinate2_1_2 , 

                                    show_pie_pic_self_1_3=show_pie_pic_self_1_3 , 
                                    show_pie_pic_manager_1_3=show_pie_pic_manager_1_3 , 
                                    show_pie_pic_peer1_1_3=show_pie_pic_peer1_1_3 , 
                                    show_pie_pic_peer2_1_3=show_pie_pic_peer2_1_3 ,
                                    show_pie_pic_subordinate1_1_3=show_pie_pic_subordinate1_1_3 , 
                                    show_pie_pic_subordinate2_1_3=show_pie_pic_subordinate2_1_3 ,

                                    show_pie_pic_self_1_4=show_pie_pic_self_1_4 , 
                                    show_pie_pic_manager_1_4=show_pie_pic_manager_1_4 , 
                                    show_pie_pic_peer1_1_4=show_pie_pic_peer1_1_4 , 
                                    show_pie_pic_peer2_1_4=show_pie_pic_peer2_1_4 ,
                                    show_pie_pic_subordinate1_1_4=show_pie_pic_subordinate1_1_4 , 
                                    show_pie_pic_subordinate2_1_4=show_pie_pic_subordinate2_1_4 , 

                                    show_pie_pic_self_1_5=show_pie_pic_self_1_5 , 
                                    show_pie_pic_manager_1_5=show_pie_pic_manager_1_5 , 
                                    show_pie_pic_peer1_1_5=show_pie_pic_peer1_1_5 , 
                                    show_pie_pic_peer2_1_5=show_pie_pic_peer2_1_5 ,
                                    show_pie_pic_subordinate1_1_5=show_pie_pic_subordinate1_1_5 , 
                                    show_pie_pic_subordinate2_1_5=show_pie_pic_subordinate2_1_5 , 

                                    show_pie_pic_self_total_1_1=show_pie_pic_self_total_1_1 ,
                                    show_pie_pic_self_total_avg_1_1=show_pie_pic_self_total_avg_1_1 ,
                                    show_pie_pic_manager_total_1_1=show_pie_pic_manager_total_1_1 ,
                                    show_pie_pic_manager_total_avg_1_1=show_pie_pic_manager_total_avg_1_1 ,
                                    show_pie_pic_peer1_total_1_1=show_pie_pic_peer1_total_1_1 ,
                                    show_pie_pic_peer1_total_avg_1_1=show_pie_pic_peer1_total_avg_1_1 ,
                                    show_pie_pic_peer2_total_1_1=show_pie_pic_peer2_total_1_1 ,
                                    show_pie_pic_peer2_total_avg_1_1=show_pie_pic_peer2_total_avg_1_1 ,
                                    show_pie_pic_subordinate1_total_1_1=show_pie_pic_subordinate1_total_1_1 ,
                                    show_pie_pic_subordinate1_total_avg_1_1=show_pie_pic_subordinate1_total_avg_1_1 ,
                                    show_pie_pic_subordinate2_total_1_1=show_pie_pic_subordinate2_total_1_1 ,
                                    show_pie_pic_subordinate2_total_avg_1_1=show_pie_pic_subordinate2_total_avg_1_1 ,
                                    show_pie_pic_total_avg_1_1=show_pie_pic_total_avg_1_1 ,
                                    
                                    ####################
                                    # 溝通與待人接物能力
                                    ####################
                                    show_pie_pic_self_2_1=show_pie_pic_self_2_1 ,
                                    show_pie_pic_manager_2_1=show_pie_pic_manager_2_1 , 
                                    show_pie_pic_peer1_2_1=show_pie_pic_peer1_2_1 , 
                                    show_pie_pic_peer2_2_1=show_pie_pic_peer2_2_1 ,
                                    show_pie_pic_subordinate1_2_1=show_pie_pic_subordinate1_2_1 , 
                                    show_pie_pic_subordinate2_2_1=show_pie_pic_subordinate2_2_1 ,

                                    show_pie_pic_self_2_2=show_pie_pic_self_2_2 , 
                                    show_pie_pic_manager_2_2=show_pie_pic_manager_2_2 , 
                                    show_pie_pic_peer1_2_2=show_pie_pic_peer1_2_2 , 
                                    show_pie_pic_peer2_2_2=show_pie_pic_peer2_2_2 ,
                                    show_pie_pic_subordinate1_2_2=show_pie_pic_subordinate1_2_2 , 
                                    show_pie_pic_subordinate2_2_2=show_pie_pic_subordinate2_2_2 , 

                                    show_pie_pic_self_2_3=show_pie_pic_self_2_3 , 
                                    show_pie_pic_manager_2_3=show_pie_pic_manager_2_3 , 
                                    show_pie_pic_peer1_2_3=show_pie_pic_peer1_2_3 , 
                                    show_pie_pic_peer2_2_3=show_pie_pic_peer2_2_3 ,
                                    show_pie_pic_subordinate1_2_3=show_pie_pic_subordinate1_2_3 , 
                                    show_pie_pic_subordinate2_2_3=show_pie_pic_subordinate2_2_3 ,

                                    show_pie_pic_self_2_4=show_pie_pic_self_2_4 , 
                                    show_pie_pic_manager_2_4=show_pie_pic_manager_2_4 , 
                                    show_pie_pic_peer1_2_4=show_pie_pic_peer1_2_4 , 
                                    show_pie_pic_peer2_2_4=show_pie_pic_peer2_2_4 ,
                                    show_pie_pic_subordinate1_2_4=show_pie_pic_subordinate1_2_4 , 
                                    show_pie_pic_subordinate2_2_4=show_pie_pic_subordinate2_2_4 , 

                                    show_pie_pic_self_2_5=show_pie_pic_self_2_5 , 
                                    show_pie_pic_manager_2_5=show_pie_pic_manager_2_5 , 
                                    show_pie_pic_peer1_2_5=show_pie_pic_peer1_2_5 , 
                                    show_pie_pic_peer2_2_5=show_pie_pic_peer2_2_5 ,
                                    show_pie_pic_subordinate1_2_5=show_pie_pic_subordinate1_2_5 , 
                                    show_pie_pic_subordinate2_2_5=show_pie_pic_subordinate2_2_5 , 
                                    
                                    show_pie_pic_self_total_2_1=show_pie_pic_self_total_2_1 ,
                                    show_pie_pic_self_total_avg_2_1=show_pie_pic_self_total_avg_2_1 ,
                                    show_pie_pic_manager_total_2_1=show_pie_pic_manager_total_2_1 ,
                                    show_pie_pic_manager_total_avg_2_1=show_pie_pic_manager_total_avg_2_1 ,
                                    show_pie_pic_peer1_total_2_1=show_pie_pic_peer1_total_2_1 ,
                                    show_pie_pic_peer1_total_avg_2_1=show_pie_pic_peer1_total_avg_2_1 ,
                                    show_pie_pic_peer2_total_2_1=show_pie_pic_peer2_total_2_1 ,
                                    show_pie_pic_peer2_total_avg_2_1=show_pie_pic_peer2_total_avg_2_1 ,
                                    show_pie_pic_subordinate1_total_2_1=show_pie_pic_subordinate1_total_2_1 ,
                                    show_pie_pic_subordinate1_total_avg_2_1=show_pie_pic_subordinate1_total_avg_2_1 ,
                                    show_pie_pic_subordinate2_total_2_1=show_pie_pic_subordinate2_total_2_1 ,
                                    show_pie_pic_subordinate2_total_avg_2_1=show_pie_pic_subordinate2_total_avg_2_1 ,
                                    show_pie_pic_total_avg_2_1=show_pie_pic_total_avg_2_1 ,
                                    
                                    ############
                                    # 工作品質
                                    ############
                                    show_pie_pic_self_3_1=show_pie_pic_self_3_1 ,
                                    show_pie_pic_manager_3_1=show_pie_pic_manager_3_1 , 
                                    show_pie_pic_peer1_3_1=show_pie_pic_peer1_3_1 , 
                                    show_pie_pic_peer2_3_1=show_pie_pic_peer2_3_1 ,
                                    show_pie_pic_subordinate1_3_1=show_pie_pic_subordinate1_3_1 , 
                                    show_pie_pic_subordinate2_3_1=show_pie_pic_subordinate2_3_1 ,

                                    show_pie_pic_self_3_2=show_pie_pic_self_3_2 , 
                                    show_pie_pic_manager_3_2=show_pie_pic_manager_3_2 , 
                                    show_pie_pic_peer1_3_2=show_pie_pic_peer1_3_2 , 
                                    show_pie_pic_peer2_3_2=show_pie_pic_peer2_3_2 ,
                                    show_pie_pic_subordinate1_3_2=show_pie_pic_subordinate1_3_2 , 
                                    show_pie_pic_subordinate2_3_2=show_pie_pic_subordinate2_3_2 , 

                                    show_pie_pic_self_3_3=show_pie_pic_self_3_3 , 
                                    show_pie_pic_manager_3_3=show_pie_pic_manager_3_3 , 
                                    show_pie_pic_peer1_3_3=show_pie_pic_peer1_3_3 , 
                                    show_pie_pic_peer2_3_3=show_pie_pic_peer2_3_3 ,
                                    show_pie_pic_subordinate1_3_3=show_pie_pic_subordinate1_3_3 , 
                                    show_pie_pic_subordinate2_3_3=show_pie_pic_subordinate2_3_3 ,

                                    show_pie_pic_self_3_4=show_pie_pic_self_3_4 , 
                                    show_pie_pic_manager_3_4=show_pie_pic_manager_3_4 , 
                                    show_pie_pic_peer1_3_4=show_pie_pic_peer1_3_4 , 
                                    show_pie_pic_peer2_3_4=show_pie_pic_peer2_3_4 ,
                                    show_pie_pic_subordinate1_3_4=show_pie_pic_subordinate1_3_4 , 
                                    show_pie_pic_subordinate2_3_4=show_pie_pic_subordinate2_3_4 , 

                                    show_pie_pic_self_3_5=show_pie_pic_self_3_5 , 
                                    show_pie_pic_manager_3_5=show_pie_pic_manager_3_5 , 
                                    show_pie_pic_peer1_3_5=show_pie_pic_peer1_3_5 , 
                                    show_pie_pic_peer2_3_5=show_pie_pic_peer2_3_5 ,
                                    show_pie_pic_subordinate1_3_5=show_pie_pic_subordinate1_3_5 , 
                                    show_pie_pic_subordinate2_3_5=show_pie_pic_subordinate2_3_5 , 
                                    
                                    show_pie_pic_self_total_3_1=show_pie_pic_self_total_3_1 ,
                                    show_pie_pic_self_total_avg_3_1=show_pie_pic_self_total_avg_3_1 ,
                                    show_pie_pic_manager_total_3_1=show_pie_pic_manager_total_3_1 ,
                                    show_pie_pic_manager_total_avg_3_1=show_pie_pic_manager_total_avg_3_1 ,
                                    show_pie_pic_peer1_total_3_1=show_pie_pic_peer1_total_3_1 ,
                                    show_pie_pic_peer1_total_avg_3_1=show_pie_pic_peer1_total_avg_3_1 ,
                                    show_pie_pic_peer2_total_3_1=show_pie_pic_peer2_total_3_1 ,
                                    show_pie_pic_peer2_total_avg_3_1=show_pie_pic_peer2_total_avg_3_1 ,
                                    show_pie_pic_subordinate1_total_3_1=show_pie_pic_subordinate1_total_3_1 ,
                                    show_pie_pic_subordinate1_total_avg_3_1=show_pie_pic_subordinate1_total_avg_3_1 ,
                                    show_pie_pic_subordinate2_total_3_1=show_pie_pic_subordinate2_total_3_1 ,
                                    show_pie_pic_subordinate2_total_avg_3_1=show_pie_pic_subordinate2_total_avg_3_1 ,
                                    show_pie_pic_total_avg_3_1=show_pie_pic_total_avg_3_1 ,
                                    
                                    ##################
                                    # 判斷力和決策能力
                                    ##################
                                    show_pie_pic_self_4_1=show_pie_pic_self_4_1 ,
                                    show_pie_pic_manager_4_1=show_pie_pic_manager_4_1 , 
                                    show_pie_pic_peer1_4_1=show_pie_pic_peer1_4_1 , 
                                    show_pie_pic_peer2_4_1=show_pie_pic_peer2_4_1 ,
                                    show_pie_pic_subordinate1_4_1=show_pie_pic_subordinate1_4_1 , 
                                    show_pie_pic_subordinate2_4_1=show_pie_pic_subordinate2_4_1 ,

                                    show_pie_pic_self_4_2=show_pie_pic_self_4_2 , 
                                    show_pie_pic_manager_4_2=show_pie_pic_manager_4_2 , 
                                    show_pie_pic_peer1_4_2=show_pie_pic_peer1_4_2 , 
                                    show_pie_pic_peer2_4_2=show_pie_pic_peer2_4_2 ,
                                    show_pie_pic_subordinate1_4_2=show_pie_pic_subordinate1_4_2 , 
                                    show_pie_pic_subordinate2_4_2=show_pie_pic_subordinate2_4_2 , 

                                    show_pie_pic_self_4_3=show_pie_pic_self_4_3 , 
                                    show_pie_pic_manager_4_3=show_pie_pic_manager_4_3 , 
                                    show_pie_pic_peer1_4_3=show_pie_pic_peer1_4_3 , 
                                    show_pie_pic_peer2_4_3=show_pie_pic_peer2_4_3 ,
                                    show_pie_pic_subordinate1_4_3=show_pie_pic_subordinate1_4_3 , 
                                    show_pie_pic_subordinate2_4_3=show_pie_pic_subordinate2_4_3 ,

                                    show_pie_pic_self_4_4=show_pie_pic_self_4_4 , 
                                    show_pie_pic_manager_4_4=show_pie_pic_manager_4_4 , 
                                    show_pie_pic_peer1_4_4=show_pie_pic_peer1_4_4 , 
                                    show_pie_pic_peer2_4_4=show_pie_pic_peer2_4_4 ,
                                    show_pie_pic_subordinate1_4_4=show_pie_pic_subordinate1_4_4 , 
                                    show_pie_pic_subordinate2_4_4=show_pie_pic_subordinate2_4_4 , 

                                    show_pie_pic_self_4_5=show_pie_pic_self_4_5 , 
                                    show_pie_pic_manager_4_5=show_pie_pic_manager_4_5 , 
                                    show_pie_pic_peer1_4_5=show_pie_pic_peer1_4_5 , 
                                    show_pie_pic_peer2_4_5=show_pie_pic_peer2_4_5 ,
                                    show_pie_pic_subordinate1_4_5=show_pie_pic_subordinate1_4_5 , 
                                    show_pie_pic_subordinate2_4_5=show_pie_pic_subordinate2_4_5 , 

                                    show_pie_pic_self_total_4_1=show_pie_pic_self_total_4_1 ,
                                    show_pie_pic_self_total_avg_4_1=show_pie_pic_self_total_avg_4_1 ,
                                    show_pie_pic_manager_total_4_1=show_pie_pic_manager_total_4_1 ,
                                    show_pie_pic_manager_total_avg_4_1=show_pie_pic_manager_total_avg_4_1 ,
                                    show_pie_pic_peer1_total_4_1=show_pie_pic_peer1_total_4_1 ,
                                    show_pie_pic_peer1_total_avg_4_1=show_pie_pic_peer1_total_avg_4_1 ,
                                    show_pie_pic_peer2_total_4_1=show_pie_pic_peer2_total_4_1 ,
                                    show_pie_pic_peer2_total_avg_4_1=show_pie_pic_peer2_total_avg_4_1 ,
                                    show_pie_pic_subordinate1_total_4_1=show_pie_pic_subordinate1_total_4_1 ,
                                    show_pie_pic_subordinate1_total_avg_4_1=show_pie_pic_subordinate1_total_avg_4_1 ,
                                    show_pie_pic_subordinate2_total_4_1=show_pie_pic_subordinate2_total_4_1 ,
                                    show_pie_pic_subordinate2_total_avg_4_1=show_pie_pic_subordinate2_total_avg_4_1 ,
                                    show_pie_pic_total_avg_4_1=show_pie_pic_total_avg_4_1 ,
                                    
                                    ############
                                    # 其他能力
                                    ############
                                    show_pie_pic_self_5_1=show_pie_pic_self_5_1 ,
                                    show_pie_pic_manager_5_1=show_pie_pic_manager_5_1 , 
                                    show_pie_pic_peer1_5_1=show_pie_pic_peer1_5_1 , 
                                    show_pie_pic_peer2_5_1=show_pie_pic_peer2_5_1 ,
                                    show_pie_pic_subordinate1_5_1=show_pie_pic_subordinate1_5_1 , 
                                    show_pie_pic_subordinate2_5_1=show_pie_pic_subordinate2_5_1 ,

                                    show_pie_pic_self_5_2=show_pie_pic_self_5_2 , 
                                    show_pie_pic_manager_5_2=show_pie_pic_manager_5_2 , 
                                    show_pie_pic_peer1_5_2=show_pie_pic_peer1_5_2 , 
                                    show_pie_pic_peer2_5_2=show_pie_pic_peer2_5_2 ,
                                    show_pie_pic_subordinate1_5_2=show_pie_pic_subordinate1_5_2 , 
                                    show_pie_pic_subordinate2_5_2=show_pie_pic_subordinate2_5_2 , 

                                    show_pie_pic_self_5_3=show_pie_pic_self_5_3 , 
                                    show_pie_pic_manager_5_3=show_pie_pic_manager_5_3 , 
                                    show_pie_pic_peer1_5_3=show_pie_pic_peer1_5_3 , 
                                    show_pie_pic_peer2_5_3=show_pie_pic_peer2_5_3 ,
                                    show_pie_pic_subordinate1_5_3=show_pie_pic_subordinate1_5_3 , 
                                    show_pie_pic_subordinate2_5_3=show_pie_pic_subordinate2_5_3 ,

                                    show_pie_pic_self_5_4=show_pie_pic_self_5_4 , 
                                    show_pie_pic_manager_5_4=show_pie_pic_manager_5_4 , 
                                    show_pie_pic_peer1_5_4=show_pie_pic_peer1_5_4 , 
                                    show_pie_pic_peer2_5_4=show_pie_pic_peer2_5_4 ,
                                    show_pie_pic_subordinate1_5_4=show_pie_pic_subordinate1_5_4 , 
                                    show_pie_pic_subordinate2_5_4=show_pie_pic_subordinate2_5_4 ,

                                    show_pie_pic_self_5_5=show_pie_pic_self_5_5 , 
                                    show_pie_pic_manager_5_5=show_pie_pic_manager_5_5 , 
                                    show_pie_pic_peer1_5_5=show_pie_pic_peer1_5_5 , 
                                    show_pie_pic_peer2_5_5=show_pie_pic_peer2_5_5 ,
                                    show_pie_pic_subordinate1_5_5=show_pie_pic_subordinate1_5_5 , 
                                    show_pie_pic_subordinate2_5_5=show_pie_pic_subordinate2_5_5 ,

                                    show_pie_pic_self_5_6=show_pie_pic_self_5_6 , 
                                    show_pie_pic_manager_5_6=show_pie_pic_manager_5_6 , 
                                    show_pie_pic_peer1_5_6=show_pie_pic_peer1_5_6 , 
                                    show_pie_pic_peer2_5_6=show_pie_pic_peer2_5_6 ,
                                    show_pie_pic_subordinate1_5_6=show_pie_pic_subordinate1_5_6 , 
                                    show_pie_pic_subordinate2_5_6=show_pie_pic_subordinate2_5_6 ,

                                    show_pie_pic_self_total_5_1=show_pie_pic_self_total_5_1 ,
                                    show_pie_pic_self_total_avg_5_1=show_pie_pic_self_total_avg_5_1 ,
                                    show_pie_pic_manager_total_5_1=show_pie_pic_manager_total_5_1 ,
                                    show_pie_pic_manager_total_avg_5_1=show_pie_pic_manager_total_avg_5_1 ,
                                    show_pie_pic_peer1_total_5_1=show_pie_pic_peer1_total_5_1 ,
                                    show_pie_pic_peer1_total_avg_5_1=show_pie_pic_peer1_total_avg_5_1 ,
                                    show_pie_pic_peer2_total_5_1=show_pie_pic_peer2_total_5_1 ,
                                    show_pie_pic_peer2_total_avg_5_1=show_pie_pic_peer2_total_avg_5_1 ,
                                    show_pie_pic_subordinate1_total_5_1=show_pie_pic_subordinate1_total_5_1 ,
                                    show_pie_pic_subordinate1_total_avg_5_1=show_pie_pic_subordinate1_total_avg_5_1 ,
                                    show_pie_pic_subordinate2_total_5_1=show_pie_pic_subordinate2_total_5_1 ,
                                    show_pie_pic_subordinate2_total_avg_5_1=show_pie_pic_subordinate2_total_avg_5_1 ,
                                    show_pie_pic_total_avg_5_1=show_pie_pic_total_avg_5_1 ,

                                    #############
                                    # 綜合雷達圖
                                    #############
                                    show_radar_pic=show_radar_pic 
                                    
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###########################################
# /show_hr_360_person_result2_export_pdf
###########################################
@app.route("/show_hr_360_person_result2_export_pdf", methods=['GET'])
def show_hr_360_person_result2_export_pdf():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'GET':

                s_name = request.args.get('s_name')

                ### operation record title
                operation_record_title = f'載入 HR - 360 考評 , 受評人員 : {s_name} 總分數資料'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ############
                # 考評人員
                ############
                show_hr_360_person_1_check_data = db.show_hr_360_person_process_total_data2(s_name)
                
                c_name         = db.search_hr_360_person_name(s_name , 'c_name')
                c_manager      = db.search_hr_360_person_name(s_name , 'c_manager')
                c_peer1        = db.search_hr_360_person_name(s_name , 'c_peer1')
                c_peer2        = db.search_hr_360_person_name(s_name , 'c_peer2')
                c_subordinate1 = db.search_hr_360_person_name(s_name , 'c_subordinate1')
                c_subordinate2 = db.search_hr_360_person_name(s_name , 'c_subordinate2')

                #####################################
                # 管理能力
                #####################################
                show_pie_pic_self_1_1         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_manager_1_1      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_peer1_1_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_peer2_1_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_subordinate1_1_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_subordinate2_1_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_1_1' , 5 , 'none')

                show_pie_pic_self_1_2         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_manager_1_2      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_peer1_1_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_peer2_1_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_subordinate1_1_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_subordinate2_1_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_1_2' , 5 , 'none')
                
                show_pie_pic_self_1_3         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_manager_1_3      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_peer1_1_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_peer2_1_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_subordinate1_1_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_subordinate2_1_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_1_3' , 5 , 'none')

                show_pie_pic_self_1_4         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_manager_1_4      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_peer1_1_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_peer2_1_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_subordinate1_1_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_subordinate2_1_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_1_4' , 5 , 'none')

                show_pie_pic_self_1_5         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_manager_1_5      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_peer1_1_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_peer2_1_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_subordinate1_1_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_subordinate2_1_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_1_5' , 5 , 'none')
                

                show_pie_pic_self_total_1_1             = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_self_total_avg_1           = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_self_total_avg_1_1         = round(float(show_pie_pic_self_total_avg_1) , 2) if show_pie_pic_self_total_avg_1 is not None else 0 
                show_pie_pic_manager_total_1_1          = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_manager_total_avg_1        = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_manager_total_avg_1_1      = round(float(show_pie_pic_manager_total_avg_1) , 2) if show_pie_pic_manager_total_avg_1 is not None else 0
                show_pie_pic_peer1_total_1_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_peer1_total_avg_1          = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_peer1_total_avg_1_1        = round(float(show_pie_pic_peer1_total_avg_1) , 2) if show_pie_pic_peer1_total_avg_1 is not None else 0
                show_pie_pic_peer2_total_1_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_peer2_total_avg_1          = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_peer2_total_avg_1_1        = round(float(show_pie_pic_peer2_total_avg_1) , 2) if show_pie_pic_peer2_total_avg_1 is not None else 0
                show_pie_pic_subordinate1_total_1_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_1   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_subordinate1_total_avg_1_1 = round(float(show_pie_pic_subordinate1_total_avg_1) , 2) if show_pie_pic_subordinate1_total_avg_1 is not None else 0
                show_pie_pic_subordinate2_total_1_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_1   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_subordinate2_total_avg_1_1 = round(float(show_pie_pic_subordinate2_total_avg_1) , 2) if show_pie_pic_subordinate2_total_avg_1 is not None else 0
                show_pie_pic_total_avg_1                = (
                                                           float(show_pie_pic_self_total_avg_1_1)     +
                                                           float(show_pie_pic_manager_total_avg_1_1)  + 
                                                           float(show_pie_pic_peer1_total_avg_1_1)     + 
                                                           float(show_pie_pic_peer2_total_avg_1_1)     + 
                                                           float(show_pie_pic_subordinate1_total_avg_1_1)   + 
                                                           float(show_pie_pic_subordinate2_total_avg_1_1))/6 
                show_pie_pic_total_avg_1_1              = round(show_pie_pic_total_avg_1 , 2)
                
                ####################
                # 提供支援
                ####################
                show_pie_pic_self_2_1         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_manager_2_1      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_peer1_2_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_peer2_2_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_subordinate1_2_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_subordinate2_2_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_2_1' , 5 , 'none')

                show_pie_pic_self_2_2         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_manager_2_2      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_peer1_2_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_peer2_2_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_subordinate1_2_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_subordinate2_2_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_2_2' , 5 , 'none')
                
                show_pie_pic_self_2_3         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_manager_2_3      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_peer1_2_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_peer2_2_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_subordinate1_2_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_subordinate2_2_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_2_3' , 5 , 'none')

                show_pie_pic_self_2_4         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_manager_2_4      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_peer1_2_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_peer2_2_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_subordinate1_2_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_subordinate2_2_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_2_4' , 5 , 'none')

                show_pie_pic_self_2_5         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_manager_2_5      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_peer1_2_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_peer2_2_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_subordinate1_2_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_subordinate2_2_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_2_5' , 5 , 'none')
                
                show_pie_pic_self_2_6         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_2_6' , 5 , 'none')
                show_pie_pic_manager_2_6      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_2_6' , 5 , 'none')
                show_pie_pic_peer1_2_6        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_2_6' , 5 , 'none')
                show_pie_pic_peer2_2_6        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_2_6' , 5 , 'none')
                show_pie_pic_subordinate1_2_6 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_2_6' , 5 , 'none')
                show_pie_pic_subordinate2_2_6 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_2_6' , 5 , 'none')

                show_pie_pic_self_total_2_1             = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_self_total_avg_2           = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_self_total_avg_2_1         = round(float(show_pie_pic_self_total_avg_2) if show_pie_pic_self_total_avg_2 is not None else 0  , 2)
                show_pie_pic_manager_total_2_1          = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_manager_total_avg_2        = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_manager_total_avg_2_1      = round(float(show_pie_pic_manager_total_avg_2) if show_pie_pic_manager_total_avg_2 is not None else 0  , 2)
                show_pie_pic_peer1_total_2_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_peer1_total_avg_2          = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_peer1_total_avg_2_1        = round(float(show_pie_pic_peer1_total_avg_2) if show_pie_pic_peer1_total_avg_2 is not None else 0  , 2)
                show_pie_pic_peer2_total_2_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_peer2_total_avg_2          = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_peer2_total_avg_2_1        = round(float(show_pie_pic_peer2_total_avg_2) if show_pie_pic_peer2_total_avg_2 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_2_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_2   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_subordinate1_total_avg_2_1 = round(float(show_pie_pic_subordinate1_total_avg_2) if show_pie_pic_subordinate1_total_avg_2 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_2_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_2   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_subordinate2_total_avg_2_1 = round(float(show_pie_pic_subordinate2_total_avg_2) if show_pie_pic_subordinate2_total_avg_2 is not None else 0  , 2 )
                show_pie_pic_total_avg_2                = (float(show_pie_pic_self_total_avg_2_1)    + 
                                                           float(show_pie_pic_manager_total_avg_2_1) + 
                                                           float(show_pie_pic_peer1_total_avg_2_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_2_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_2_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_2_1) )/6 
                show_pie_pic_total_avg_2_1              = round(show_pie_pic_total_avg_2 , 2)

                ############
                # 以身作則
                ############
                show_pie_pic_self_3_1         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_manager_3_1      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_peer1_3_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_peer2_3_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_subordinate1_3_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_subordinate2_3_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_3_1' , 5 , 'none')

                show_pie_pic_self_3_2         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_manager_3_2      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_peer1_3_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_peer2_3_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_subordinate1_3_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_subordinate2_3_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_3_2' , 5 , 'none')
                
                show_pie_pic_self_3_3         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_manager_3_3      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_peer1_3_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_peer2_3_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_subordinate1_3_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_subordinate2_3_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_3_3' , 5 , 'none')

                show_pie_pic_self_3_4         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_manager_3_4      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_peer1_3_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_peer2_3_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_subordinate1_3_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_subordinate2_3_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_3_4' , 5 , 'none')

                show_pie_pic_self_3_5         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_manager_3_5      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_peer1_3_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_peer2_3_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_subordinate1_3_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_subordinate2_3_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_3_5' , 5 , 'none')

                show_pie_pic_self_total_3_1             = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_self_total_avg_3           = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_self_total_avg_3_1         = round(float(show_pie_pic_self_total_avg_3) if show_pie_pic_self_total_avg_3 is not None else 0  , 2)
                show_pie_pic_manager_total_3_1          = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_manager_total_avg_3        = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_manager_total_avg_3_1      = round(float(show_pie_pic_manager_total_avg_3) if show_pie_pic_manager_total_avg_3 is not None else 0  , 2)
                show_pie_pic_peer1_total_3_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_peer1_total_avg_3          = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_peer1_total_avg_3_1        = round(float(show_pie_pic_peer1_total_avg_3) if show_pie_pic_peer1_total_avg_3 is not None else 0  , 2)
                show_pie_pic_peer2_total_3_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_peer2_total_avg_3          = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_peer2_total_avg_3_1        = round(float(show_pie_pic_peer2_total_avg_3) if show_pie_pic_peer2_total_avg_3 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_3_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_3   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_subordinate1_total_avg_3_1 = round(float(show_pie_pic_subordinate1_total_avg_3) if show_pie_pic_subordinate1_total_avg_3 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_3_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_3   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_subordinate2_total_avg_3_1 = round(float(show_pie_pic_subordinate2_total_avg_3) if show_pie_pic_subordinate2_total_avg_3 is not None else 0  , 2 )
                show_pie_pic_total_avg_3                = (float(show_pie_pic_self_total_avg_3_1)    + 
                                                           float(show_pie_pic_manager_total_avg_3_1) + 
                                                           float(show_pie_pic_peer1_total_avg_3_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_3_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_3_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_3_1) )/6 
                show_pie_pic_total_avg_3_1              = round(show_pie_pic_total_avg_3 , 2)
                
                ##################
                # 效率導向
                ##################
                show_pie_pic_self_4_1         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_manager_4_1      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_peer1_4_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_peer2_4_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_subordinate1_4_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_subordinate2_4_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_4_1' , 5 , 'none')

                show_pie_pic_self_4_2         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_manager_4_2      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_peer1_4_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_peer2_4_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_subordinate1_4_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_subordinate2_4_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_4_2' , 5 , 'none')
                
                show_pie_pic_self_4_3         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_manager_4_3      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_peer1_4_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_peer2_4_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_subordinate1_4_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_subordinate2_4_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_4_3' , 5 , 'none')

                show_pie_pic_self_4_4         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_manager_4_4      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_peer1_4_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_peer2_4_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_subordinate1_4_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_subordinate2_4_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_4_4' , 5 , 'none')

                show_pie_pic_self_total_4_1             = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_self_total_avg_4           = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_self_total_avg_4_1         = round(float(show_pie_pic_self_total_avg_4) if show_pie_pic_self_total_avg_4 is not None else 0  , 2)
                show_pie_pic_manager_total_4_1          = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_manager_total_avg_4        = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_manager_total_avg_4_1      = round(float(show_pie_pic_manager_total_avg_4) if show_pie_pic_manager_total_avg_4 is not None else 0  , 2)
                show_pie_pic_peer1_total_4_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_peer1_total_avg_4          = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_peer1_total_avg_4_1        = round(float(show_pie_pic_peer1_total_avg_4) if show_pie_pic_peer1_total_avg_4 is not None else 0  , 2)
                show_pie_pic_peer2_total_4_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_peer2_total_avg_4          = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_peer2_total_avg_4_1        = round(float(show_pie_pic_peer2_total_avg_4) if show_pie_pic_peer2_total_avg_4 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_4_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_4   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_subordinate1_total_avg_4_1 = round(float(show_pie_pic_subordinate1_total_avg_4) if show_pie_pic_subordinate1_total_avg_4 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_4_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_4   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_subordinate2_total_avg_4_1 = round(float(show_pie_pic_subordinate2_total_avg_4) if show_pie_pic_subordinate2_total_avg_4 is not None else 0  , 2 )
                show_pie_pic_total_avg_4                = (float(show_pie_pic_self_total_avg_4_1)    + 
                                                           float(show_pie_pic_manager_total_avg_4_1) + 
                                                           float(show_pie_pic_peer1_total_avg_4_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_4_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_4_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_4_1) )/6 
                show_pie_pic_total_avg_4_1              = round(show_pie_pic_total_avg_4 , 2)
                
                ############
                # 培育人才
                ############
                show_pie_pic_self_5_1         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_manager_5_1      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_peer1_5_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_peer2_5_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_subordinate1_5_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_subordinate2_5_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_5_1' , 5 , 'none')

                show_pie_pic_self_5_2         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_manager_5_2      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_peer1_5_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_peer2_5_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_subordinate1_5_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_subordinate2_5_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_5_2' , 5 , 'none')
                
                show_pie_pic_self_5_3         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_manager_5_3      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_peer1_5_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_peer2_5_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_subordinate1_5_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_subordinate2_5_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_5_3' , 5 , 'none')

                show_pie_pic_self_total_5_1             = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_self_total_avg_5           = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_self_total_avg_5_1         = round(float(show_pie_pic_self_total_avg_5) if show_pie_pic_self_total_avg_5 is not None else 0  , 2)
                show_pie_pic_manager_total_5_1          = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_manager_total_avg_5        = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_manager_total_avg_5_1      = round(float(show_pie_pic_manager_total_avg_5) if show_pie_pic_manager_total_avg_5 is not None else 0  , 2)
                show_pie_pic_peer1_total_5_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_peer1_total_avg_5          = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_peer1_total_avg_5_1        = round(float(show_pie_pic_peer1_total_avg_5) if show_pie_pic_peer1_total_avg_5 is not None else 0  , 2)
                show_pie_pic_peer2_total_5_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_peer2_total_avg_5          = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_peer2_total_avg_5_1        = round(float(show_pie_pic_peer2_total_avg_5) if show_pie_pic_peer2_total_avg_5 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_5_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_5   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_subordinate1_total_avg_5_1 = round(float(show_pie_pic_subordinate1_total_avg_5) if show_pie_pic_subordinate1_total_avg_5 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_5_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_5   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_subordinate2_total_avg_5_1 = round(float(show_pie_pic_subordinate2_total_avg_5) if show_pie_pic_subordinate2_total_avg_5 is not None else 0  , 2 )
                show_pie_pic_total_avg_5                = (float(show_pie_pic_self_total_avg_5_1)    + 
                                                           float(show_pie_pic_manager_total_avg_5_1) + 
                                                           float(show_pie_pic_peer1_total_avg_5_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_5_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_5_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_5_1) )/6 
                show_pie_pic_total_avg_5_1              = round(show_pie_pic_total_avg_5 , 2)

                ############
                # 高效溝通
                ############
                show_pie_pic_self_6_1         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_6_1' , 5 , 'none')
                show_pie_pic_manager_6_1      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_6_1' , 5 , 'none')
                show_pie_pic_peer1_6_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_6_1' , 5 , 'none')
                show_pie_pic_peer2_6_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_6_1' , 5 , 'none')
                show_pie_pic_subordinate1_6_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_6_1' , 5 , 'none')
                show_pie_pic_subordinate2_6_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_6_1' , 5 , 'none')

                show_pie_pic_self_6_2         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_6_2' , 5 , 'none')
                show_pie_pic_manager_6_2      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_6_2' , 5 , 'none')
                show_pie_pic_peer1_6_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_6_2' , 5 , 'none')
                show_pie_pic_peer2_6_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_6_2' , 5 , 'none')
                show_pie_pic_subordinate1_6_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_6_2' , 5 , 'none')
                show_pie_pic_subordinate2_6_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_6_2' , 5 , 'none')
                
                show_pie_pic_self_6_3         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_6_3' , 5 , 'none')
                show_pie_pic_manager_6_3      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_6_3' , 5 , 'none')
                show_pie_pic_peer1_6_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_6_3' , 5 , 'none')
                show_pie_pic_peer2_6_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_6_3' , 5 , 'none')
                show_pie_pic_subordinate1_6_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_6_3' , 5 , 'none')
                show_pie_pic_subordinate2_6_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_6_3' , 5 , 'none')

                show_pie_pic_self_6_4         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_6_4' , 5 , 'none')
                show_pie_pic_manager_6_4      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_6_4' , 5 , 'none')
                show_pie_pic_peer1_6_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_6_4' , 5 , 'none')
                show_pie_pic_peer2_6_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_6_4' , 5 , 'none')
                show_pie_pic_subordinate1_6_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_6_4' , 5 , 'none')
                show_pie_pic_subordinate2_6_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_6_4' , 5 , 'none')

                show_pie_pic_self_6_5         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_6_5' , 5 , 'none')
                show_pie_pic_manager_6_5      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_6_5' , 5 , 'none')
                show_pie_pic_peer1_6_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_6_5' , 5 , 'none')
                show_pie_pic_peer2_6_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_6_5' , 5 , 'none')
                show_pie_pic_subordinate1_6_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_6_5' , 5 , 'none')
                show_pie_pic_subordinate2_6_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_6_5' , 5 , 'none')

                show_pie_pic_self_total_6_1             = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_6'     , 25 , 'total')
                show_pie_pic_self_total_avg_6           = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_6_avg' , 5  , 'total')
                show_pie_pic_self_total_avg_6_1         = round(float(show_pie_pic_self_total_avg_6) if show_pie_pic_self_total_avg_6 is not None else 0  , 2)
                show_pie_pic_manager_total_6_1          = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_6'     , 25 , 'total')
                show_pie_pic_manager_total_avg_6        = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_6_avg' , 5  , 'total')
                show_pie_pic_manager_total_avg_6_1      = round(float(show_pie_pic_manager_total_avg_6) if show_pie_pic_manager_total_avg_6 is not None else 0  , 2)
                show_pie_pic_peer1_total_6_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_6'     , 25 , 'total')
                show_pie_pic_peer1_total_avg_6          = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_6_avg' , 5  , 'total')
                show_pie_pic_peer1_total_avg_6_1        = round(float(show_pie_pic_peer1_total_avg_6) if show_pie_pic_peer1_total_avg_6 is not None else 0  , 2)
                show_pie_pic_peer2_total_6_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_6'     , 25 , 'total')
                show_pie_pic_peer2_total_avg_6          = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_6_avg' , 5  , 'total')
                show_pie_pic_peer2_total_avg_6_1        = round(float(show_pie_pic_peer2_total_avg_6) if show_pie_pic_peer2_total_avg_6 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_6_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_6'     , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_6   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_6_avg' , 5  , 'total')
                show_pie_pic_subordinate1_total_avg_6_1 = round(float(show_pie_pic_subordinate1_total_avg_6) if show_pie_pic_subordinate1_total_avg_6 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_6_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_6'     , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_6   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_6_avg' , 5  , 'total')
                show_pie_pic_subordinate2_total_avg_6_1 = round(float(show_pie_pic_subordinate2_total_avg_6) if show_pie_pic_subordinate2_total_avg_6 is not None else 0  , 2 )
                show_pie_pic_total_avg_6                = (float(show_pie_pic_self_total_avg_6_1)    + 
                                                           float(show_pie_pic_manager_total_avg_6_1) + 
                                                           float(show_pie_pic_peer1_total_avg_6_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_6_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_6_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_6_1) )/6 
                show_pie_pic_total_avg_6_1              = round(show_pie_pic_total_avg_6 , 2)

                ############
                # 雷達圖
                ############
                show_radar_pic_num1 = ([float(show_pie_pic_self_total_avg_1_1) , float(show_pie_pic_self_total_avg_2_1) , float(show_pie_pic_self_total_avg_3_1) , float(show_pie_pic_self_total_avg_4_1) , float(show_pie_pic_self_total_avg_5_1) , float(show_pie_pic_self_total_avg_6_1) , ])
                show_radar_pic_num2 = ([float(show_pie_pic_manager_total_avg_1_1) , float(show_pie_pic_manager_total_avg_2_1) , float(show_pie_pic_manager_total_avg_3_1) , float(show_pie_pic_manager_total_avg_4_1) , float(show_pie_pic_manager_total_avg_5_1) , float(show_pie_pic_manager_total_avg_6_1) , ])
                show_radar_pic_num3 = ([float(show_pie_pic_peer1_total_avg_1_1) , float(show_pie_pic_peer1_total_avg_2_1) , float(show_pie_pic_peer1_total_avg_3_1) , float(show_pie_pic_peer1_total_avg_4_1) , float(show_pie_pic_peer1_total_avg_5_1) , float(show_pie_pic_peer1_total_avg_6_1) , ])
                show_radar_pic_num4 = ([float(show_pie_pic_peer2_total_avg_1_1) , float(show_pie_pic_peer2_total_avg_2_1) , float(show_pie_pic_peer2_total_avg_3_1) , float(show_pie_pic_peer2_total_avg_4_1) , float(show_pie_pic_peer2_total_avg_5_1) , float(show_pie_pic_peer2_total_avg_6_1) , ])
                show_radar_pic_num5 = ([float(show_pie_pic_subordinate1_total_avg_1_1) , float(show_pie_pic_subordinate1_total_avg_2_1) , float(show_pie_pic_subordinate1_total_avg_3_1) , float(show_pie_pic_subordinate1_total_avg_4_1) , float(show_pie_pic_subordinate1_total_avg_5_1) , float(show_pie_pic_subordinate1_total_avg_6_1) , ])
                show_radar_pic_num6 = ([float(show_pie_pic_subordinate2_total_avg_1_1) , float(show_pie_pic_subordinate2_total_avg_2_1) , float(show_pie_pic_subordinate2_total_avg_3_1) , float(show_pie_pic_subordinate2_total_avg_4_1) , float(show_pie_pic_subordinate2_total_avg_5_1) , float(show_pie_pic_subordinate2_total_avg_6_1) , ])
                show_radar_pic      = db.show_radar_picture(show_radar_pic_num1 , show_radar_pic_num2 , show_radar_pic_num3 , show_radar_pic_num4 , show_radar_pic_num5 , show_radar_pic_num6)

                return render_template('ajax/load_hr_360_dep_member_process_list_res2_print.html' , 
                                    show_hr_360_person_1_check_data=show_hr_360_person_1_check_data , s_name=s_name , 
                                    
                                    #####################################
                                    # 管理能力
                                    #####################################
                                    show_pie_pic_self_1_1=show_pie_pic_self_1_1 ,
                                    show_pie_pic_manager_1_1=show_pie_pic_manager_1_1 , 
                                    show_pie_pic_peer1_1_1=show_pie_pic_peer1_1_1 , 
                                    show_pie_pic_peer2_1_1=show_pie_pic_peer2_1_1 ,
                                    show_pie_pic_subordinate1_1_1=show_pie_pic_subordinate1_1_1 , 
                                    show_pie_pic_subordinate2_1_1=show_pie_pic_subordinate2_1_1 ,

                                    show_pie_pic_self_1_2=show_pie_pic_self_1_2 , 
                                    show_pie_pic_manager_1_2=show_pie_pic_manager_1_2 , 
                                    show_pie_pic_peer1_1_2=show_pie_pic_peer1_1_2 , 
                                    show_pie_pic_peer2_1_2=show_pie_pic_peer2_1_2 ,
                                    show_pie_pic_subordinate1_1_2=show_pie_pic_subordinate1_1_2 , 
                                    show_pie_pic_subordinate2_1_2=show_pie_pic_subordinate2_1_2 , 

                                    show_pie_pic_self_1_3=show_pie_pic_self_1_3 , 
                                    show_pie_pic_manager_1_3=show_pie_pic_manager_1_3 , 
                                    show_pie_pic_peer1_1_3=show_pie_pic_peer1_1_3 , 
                                    show_pie_pic_peer2_1_3=show_pie_pic_peer2_1_3 ,
                                    show_pie_pic_subordinate1_1_3=show_pie_pic_subordinate1_1_3 , 
                                    show_pie_pic_subordinate2_1_3=show_pie_pic_subordinate2_1_3 ,

                                    show_pie_pic_self_1_4=show_pie_pic_self_1_4 , 
                                    show_pie_pic_manager_1_4=show_pie_pic_manager_1_4 , 
                                    show_pie_pic_peer1_1_4=show_pie_pic_peer1_1_4 , 
                                    show_pie_pic_peer2_1_4=show_pie_pic_peer2_1_4 ,
                                    show_pie_pic_subordinate1_1_4=show_pie_pic_subordinate1_1_4 , 
                                    show_pie_pic_subordinate2_1_4=show_pie_pic_subordinate2_1_4 , 

                                    show_pie_pic_self_1_5=show_pie_pic_self_1_5 , 
                                    show_pie_pic_manager_1_5=show_pie_pic_manager_1_5 , 
                                    show_pie_pic_peer1_1_5=show_pie_pic_peer1_1_5 , 
                                    show_pie_pic_peer2_1_5=show_pie_pic_peer2_1_5 ,
                                    show_pie_pic_subordinate1_1_5=show_pie_pic_subordinate1_1_5 , 
                                    show_pie_pic_subordinate2_1_5=show_pie_pic_subordinate2_1_5 , 

                                    show_pie_pic_self_total_1_1=show_pie_pic_self_total_1_1 ,
                                    show_pie_pic_self_total_avg_1_1=show_pie_pic_self_total_avg_1_1 ,
                                    show_pie_pic_manager_total_1_1=show_pie_pic_manager_total_1_1 ,
                                    show_pie_pic_manager_total_avg_1_1=show_pie_pic_manager_total_avg_1_1 ,
                                    show_pie_pic_peer1_total_1_1=show_pie_pic_peer1_total_1_1 ,
                                    show_pie_pic_peer1_total_avg_1_1=show_pie_pic_peer1_total_avg_1_1 ,
                                    show_pie_pic_peer2_total_1_1=show_pie_pic_peer2_total_1_1 ,
                                    show_pie_pic_peer2_total_avg_1_1=show_pie_pic_peer2_total_avg_1_1 ,
                                    show_pie_pic_subordinate1_total_1_1=show_pie_pic_subordinate1_total_1_1 ,
                                    show_pie_pic_subordinate1_total_avg_1_1=show_pie_pic_subordinate1_total_avg_1_1 ,
                                    show_pie_pic_subordinate2_total_1_1=show_pie_pic_subordinate2_total_1_1 ,
                                    show_pie_pic_subordinate2_total_avg_1_1=show_pie_pic_subordinate2_total_avg_1_1 ,
                                    show_pie_pic_total_avg_1_1=show_pie_pic_total_avg_1_1 ,
                                    
                                    ####################
                                    # 提供支援
                                    ####################
                                    show_pie_pic_self_2_1=show_pie_pic_self_2_1 ,
                                    show_pie_pic_manager_2_1=show_pie_pic_manager_2_1 , 
                                    show_pie_pic_peer1_2_1=show_pie_pic_peer1_2_1 , 
                                    show_pie_pic_peer2_2_1=show_pie_pic_peer2_2_1 ,
                                    show_pie_pic_subordinate1_2_1=show_pie_pic_subordinate1_2_1 , 
                                    show_pie_pic_subordinate2_2_1=show_pie_pic_subordinate2_2_1 ,

                                    show_pie_pic_self_2_2=show_pie_pic_self_2_2 , 
                                    show_pie_pic_manager_2_2=show_pie_pic_manager_2_2 , 
                                    show_pie_pic_peer1_2_2=show_pie_pic_peer1_2_2 , 
                                    show_pie_pic_peer2_2_2=show_pie_pic_peer2_2_2 ,
                                    show_pie_pic_subordinate1_2_2=show_pie_pic_subordinate1_2_2 , 
                                    show_pie_pic_subordinate2_2_2=show_pie_pic_subordinate2_2_2 , 

                                    show_pie_pic_self_2_3=show_pie_pic_self_2_3 , 
                                    show_pie_pic_manager_2_3=show_pie_pic_manager_2_3 , 
                                    show_pie_pic_peer1_2_3=show_pie_pic_peer1_2_3 , 
                                    show_pie_pic_peer2_2_3=show_pie_pic_peer2_2_3 ,
                                    show_pie_pic_subordinate1_2_3=show_pie_pic_subordinate1_2_3 , 
                                    show_pie_pic_subordinate2_2_3=show_pie_pic_subordinate2_2_3 ,

                                    show_pie_pic_self_2_4=show_pie_pic_self_2_4 , 
                                    show_pie_pic_manager_2_4=show_pie_pic_manager_2_4 , 
                                    show_pie_pic_peer1_2_4=show_pie_pic_peer1_2_4 , 
                                    show_pie_pic_peer2_2_4=show_pie_pic_peer2_2_4 ,
                                    show_pie_pic_subordinate1_2_4=show_pie_pic_subordinate1_2_4 , 
                                    show_pie_pic_subordinate2_2_4=show_pie_pic_subordinate2_2_4 , 

                                    show_pie_pic_self_2_5=show_pie_pic_self_2_5 , 
                                    show_pie_pic_manager_2_5=show_pie_pic_manager_2_5 , 
                                    show_pie_pic_peer1_2_5=show_pie_pic_peer1_2_5 , 
                                    show_pie_pic_peer2_2_5=show_pie_pic_peer2_2_5 ,
                                    show_pie_pic_subordinate1_2_5=show_pie_pic_subordinate1_2_5 , 
                                    show_pie_pic_subordinate2_2_5=show_pie_pic_subordinate2_2_5 , 

                                    show_pie_pic_self_2_6=show_pie_pic_self_2_6 , 
                                    show_pie_pic_manager_2_6=show_pie_pic_manager_2_6 , 
                                    show_pie_pic_peer1_2_6=show_pie_pic_peer1_2_6 , 
                                    show_pie_pic_peer2_2_6=show_pie_pic_peer2_2_6 ,
                                    show_pie_pic_subordinate1_2_6=show_pie_pic_subordinate1_2_6 , 
                                    show_pie_pic_subordinate2_2_6=show_pie_pic_subordinate2_2_6 , 
                                    
                                    show_pie_pic_self_total_2_1=show_pie_pic_self_total_2_1 ,
                                    show_pie_pic_self_total_avg_2_1=show_pie_pic_self_total_avg_2_1 ,
                                    show_pie_pic_manager_total_2_1=show_pie_pic_manager_total_2_1 ,
                                    show_pie_pic_manager_total_avg_2_1=show_pie_pic_manager_total_avg_2_1 ,
                                    show_pie_pic_peer1_total_2_1=show_pie_pic_peer1_total_2_1 ,
                                    show_pie_pic_peer1_total_avg_2_1=show_pie_pic_peer1_total_avg_2_1 ,
                                    show_pie_pic_peer2_total_2_1=show_pie_pic_peer2_total_2_1 ,
                                    show_pie_pic_peer2_total_avg_2_1=show_pie_pic_peer2_total_avg_2_1 ,
                                    show_pie_pic_subordinate1_total_2_1=show_pie_pic_subordinate1_total_2_1 ,
                                    show_pie_pic_subordinate1_total_avg_2_1=show_pie_pic_subordinate1_total_avg_2_1 ,
                                    show_pie_pic_subordinate2_total_2_1=show_pie_pic_subordinate2_total_2_1 ,
                                    show_pie_pic_subordinate2_total_avg_2_1=show_pie_pic_subordinate2_total_avg_2_1 ,
                                    show_pie_pic_total_avg_2_1=show_pie_pic_total_avg_2_1 ,
                                    
                                    ############
                                    # 以身作則
                                    ############
                                    show_pie_pic_self_3_1=show_pie_pic_self_3_1 ,
                                    show_pie_pic_manager_3_1=show_pie_pic_manager_3_1 , 
                                    show_pie_pic_peer1_3_1=show_pie_pic_peer1_3_1 , 
                                    show_pie_pic_peer2_3_1=show_pie_pic_peer2_3_1 ,
                                    show_pie_pic_subordinate1_3_1=show_pie_pic_subordinate1_3_1 , 
                                    show_pie_pic_subordinate2_3_1=show_pie_pic_subordinate2_3_1 ,

                                    show_pie_pic_self_3_2=show_pie_pic_self_3_2 , 
                                    show_pie_pic_manager_3_2=show_pie_pic_manager_3_2 , 
                                    show_pie_pic_peer1_3_2=show_pie_pic_peer1_3_2 , 
                                    show_pie_pic_peer2_3_2=show_pie_pic_peer2_3_2 ,
                                    show_pie_pic_subordinate1_3_2=show_pie_pic_subordinate1_3_2 , 
                                    show_pie_pic_subordinate2_3_2=show_pie_pic_subordinate2_3_2 , 

                                    show_pie_pic_self_3_3=show_pie_pic_self_3_3 , 
                                    show_pie_pic_manager_3_3=show_pie_pic_manager_3_3 , 
                                    show_pie_pic_peer1_3_3=show_pie_pic_peer1_3_3 , 
                                    show_pie_pic_peer2_3_3=show_pie_pic_peer2_3_3 ,
                                    show_pie_pic_subordinate1_3_3=show_pie_pic_subordinate1_3_3 , 
                                    show_pie_pic_subordinate2_3_3=show_pie_pic_subordinate2_3_3 ,

                                    show_pie_pic_self_3_4=show_pie_pic_self_3_4 , 
                                    show_pie_pic_manager_3_4=show_pie_pic_manager_3_4 , 
                                    show_pie_pic_peer1_3_4=show_pie_pic_peer1_3_4 , 
                                    show_pie_pic_peer2_3_4=show_pie_pic_peer2_3_4 ,
                                    show_pie_pic_subordinate1_3_4=show_pie_pic_subordinate1_3_4 , 
                                    show_pie_pic_subordinate2_3_4=show_pie_pic_subordinate2_3_4 , 

                                    show_pie_pic_self_3_5=show_pie_pic_self_3_5 , 
                                    show_pie_pic_manager_3_5=show_pie_pic_manager_3_5 , 
                                    show_pie_pic_peer1_3_5=show_pie_pic_peer1_3_5 , 
                                    show_pie_pic_peer2_3_5=show_pie_pic_peer2_3_5 ,
                                    show_pie_pic_subordinate1_3_5=show_pie_pic_subordinate1_3_5 , 
                                    show_pie_pic_subordinate2_3_5=show_pie_pic_subordinate2_3_5 , 
                                    
                                    show_pie_pic_self_total_3_1=show_pie_pic_self_total_3_1 ,
                                    show_pie_pic_self_total_avg_3_1=show_pie_pic_self_total_avg_3_1 ,
                                    show_pie_pic_manager_total_3_1=show_pie_pic_manager_total_3_1 ,
                                    show_pie_pic_manager_total_avg_3_1=show_pie_pic_manager_total_avg_3_1 ,
                                    show_pie_pic_peer1_total_3_1=show_pie_pic_peer1_total_3_1 ,
                                    show_pie_pic_peer1_total_avg_3_1=show_pie_pic_peer1_total_avg_3_1 ,
                                    show_pie_pic_peer2_total_3_1=show_pie_pic_peer2_total_3_1 ,
                                    show_pie_pic_peer2_total_avg_3_1=show_pie_pic_peer2_total_avg_3_1 ,
                                    show_pie_pic_subordinate1_total_3_1=show_pie_pic_subordinate1_total_3_1 ,
                                    show_pie_pic_subordinate1_total_avg_3_1=show_pie_pic_subordinate1_total_avg_3_1 ,
                                    show_pie_pic_subordinate2_total_3_1=show_pie_pic_subordinate2_total_3_1 ,
                                    show_pie_pic_subordinate2_total_avg_3_1=show_pie_pic_subordinate2_total_avg_3_1 ,
                                    show_pie_pic_total_avg_3_1=show_pie_pic_total_avg_3_1 ,
                                    
                                    ##################
                                    # 效率導向
                                    ##################
                                    show_pie_pic_self_4_1=show_pie_pic_self_4_1 ,
                                    show_pie_pic_manager_4_1=show_pie_pic_manager_4_1 , 
                                    show_pie_pic_peer1_4_1=show_pie_pic_peer1_4_1 , 
                                    show_pie_pic_peer2_4_1=show_pie_pic_peer2_4_1 ,
                                    show_pie_pic_subordinate1_4_1=show_pie_pic_subordinate1_4_1 , 
                                    show_pie_pic_subordinate2_4_1=show_pie_pic_subordinate2_4_1 ,

                                    show_pie_pic_self_4_2=show_pie_pic_self_4_2 , 
                                    show_pie_pic_manager_4_2=show_pie_pic_manager_4_2 , 
                                    show_pie_pic_peer1_4_2=show_pie_pic_peer1_4_2 , 
                                    show_pie_pic_peer2_4_2=show_pie_pic_peer2_4_2 ,
                                    show_pie_pic_subordinate1_4_2=show_pie_pic_subordinate1_4_2 , 
                                    show_pie_pic_subordinate2_4_2=show_pie_pic_subordinate2_4_2 , 

                                    show_pie_pic_self_4_3=show_pie_pic_self_4_3 , 
                                    show_pie_pic_manager_4_3=show_pie_pic_manager_4_3 , 
                                    show_pie_pic_peer1_4_3=show_pie_pic_peer1_4_3 , 
                                    show_pie_pic_peer2_4_3=show_pie_pic_peer2_4_3 ,
                                    show_pie_pic_subordinate1_4_3=show_pie_pic_subordinate1_4_3 , 
                                    show_pie_pic_subordinate2_4_3=show_pie_pic_subordinate2_4_3 ,

                                    show_pie_pic_self_4_4=show_pie_pic_self_4_4 , 
                                    show_pie_pic_manager_4_4=show_pie_pic_manager_4_4 , 
                                    show_pie_pic_peer1_4_4=show_pie_pic_peer1_4_4 , 
                                    show_pie_pic_peer2_4_4=show_pie_pic_peer2_4_4 ,
                                    show_pie_pic_subordinate1_4_4=show_pie_pic_subordinate1_4_4 , 
                                    show_pie_pic_subordinate2_4_4=show_pie_pic_subordinate2_4_4 , 

                                    show_pie_pic_self_total_4_1=show_pie_pic_self_total_4_1 ,
                                    show_pie_pic_self_total_avg_4_1=show_pie_pic_self_total_avg_4_1 ,
                                    show_pie_pic_manager_total_4_1=show_pie_pic_manager_total_4_1 ,
                                    show_pie_pic_manager_total_avg_4_1=show_pie_pic_manager_total_avg_4_1 ,
                                    show_pie_pic_peer1_total_4_1=show_pie_pic_peer1_total_4_1 ,
                                    show_pie_pic_peer1_total_avg_4_1=show_pie_pic_peer1_total_avg_4_1 ,
                                    show_pie_pic_peer2_total_4_1=show_pie_pic_peer2_total_4_1 ,
                                    show_pie_pic_peer2_total_avg_4_1=show_pie_pic_peer2_total_avg_4_1 ,
                                    show_pie_pic_subordinate1_total_4_1=show_pie_pic_subordinate1_total_4_1 ,
                                    show_pie_pic_subordinate1_total_avg_4_1=show_pie_pic_subordinate1_total_avg_4_1 ,
                                    show_pie_pic_subordinate2_total_4_1=show_pie_pic_subordinate2_total_4_1 ,
                                    show_pie_pic_subordinate2_total_avg_4_1=show_pie_pic_subordinate2_total_avg_4_1 ,
                                    show_pie_pic_total_avg_4_1=show_pie_pic_total_avg_4_1 ,
                                    
                                    ############
                                    # 培育人才
                                    ############
                                    show_pie_pic_self_5_1=show_pie_pic_self_5_1 ,
                                    show_pie_pic_manager_5_1=show_pie_pic_manager_5_1 , 
                                    show_pie_pic_peer1_5_1=show_pie_pic_peer1_5_1 , 
                                    show_pie_pic_peer2_5_1=show_pie_pic_peer2_5_1 ,
                                    show_pie_pic_subordinate1_5_1=show_pie_pic_subordinate1_5_1 , 
                                    show_pie_pic_subordinate2_5_1=show_pie_pic_subordinate2_5_1 ,

                                    show_pie_pic_self_5_2=show_pie_pic_self_5_2 , 
                                    show_pie_pic_manager_5_2=show_pie_pic_manager_5_2 , 
                                    show_pie_pic_peer1_5_2=show_pie_pic_peer1_5_2 , 
                                    show_pie_pic_peer2_5_2=show_pie_pic_peer2_5_2 ,
                                    show_pie_pic_subordinate1_5_2=show_pie_pic_subordinate1_5_2 , 
                                    show_pie_pic_subordinate2_5_2=show_pie_pic_subordinate2_5_2 , 

                                    show_pie_pic_self_5_3=show_pie_pic_self_5_3 , 
                                    show_pie_pic_manager_5_3=show_pie_pic_manager_5_3 , 
                                    show_pie_pic_peer1_5_3=show_pie_pic_peer1_5_3 , 
                                    show_pie_pic_peer2_5_3=show_pie_pic_peer2_5_3 ,
                                    show_pie_pic_subordinate1_5_3=show_pie_pic_subordinate1_5_3 , 
                                    show_pie_pic_subordinate2_5_3=show_pie_pic_subordinate2_5_3 ,

                                    show_pie_pic_self_total_5_1=show_pie_pic_self_total_5_1 ,
                                    show_pie_pic_self_total_avg_5_1=show_pie_pic_self_total_avg_5_1 ,
                                    show_pie_pic_manager_total_5_1=show_pie_pic_manager_total_5_1 ,
                                    show_pie_pic_manager_total_avg_5_1=show_pie_pic_manager_total_avg_5_1 ,
                                    show_pie_pic_peer1_total_5_1=show_pie_pic_peer1_total_5_1 ,
                                    show_pie_pic_peer1_total_avg_5_1=show_pie_pic_peer1_total_avg_5_1 ,
                                    show_pie_pic_peer2_total_5_1=show_pie_pic_peer2_total_5_1 ,
                                    show_pie_pic_peer2_total_avg_5_1=show_pie_pic_peer2_total_avg_5_1 ,
                                    show_pie_pic_subordinate1_total_5_1=show_pie_pic_subordinate1_total_5_1 ,
                                    show_pie_pic_subordinate1_total_avg_5_1=show_pie_pic_subordinate1_total_avg_5_1 ,
                                    show_pie_pic_subordinate2_total_5_1=show_pie_pic_subordinate2_total_5_1 ,
                                    show_pie_pic_subordinate2_total_avg_5_1=show_pie_pic_subordinate2_total_avg_5_1 ,
                                    show_pie_pic_total_avg_5_1=show_pie_pic_total_avg_5_1 ,

                                    ############
                                    # 高效溝通
                                    ############
                                    show_pie_pic_self_6_1=show_pie_pic_self_6_1 ,
                                    show_pie_pic_manager_6_1=show_pie_pic_manager_6_1 , 
                                    show_pie_pic_peer1_6_1=show_pie_pic_peer1_6_1 , 
                                    show_pie_pic_peer2_6_1=show_pie_pic_peer2_6_1 ,
                                    show_pie_pic_subordinate1_6_1=show_pie_pic_subordinate1_6_1 , 
                                    show_pie_pic_subordinate2_6_1=show_pie_pic_subordinate2_6_1 ,

                                    show_pie_pic_self_6_2=show_pie_pic_self_6_2 , 
                                    show_pie_pic_manager_6_2=show_pie_pic_manager_6_2 , 
                                    show_pie_pic_peer1_6_2=show_pie_pic_peer1_6_2 , 
                                    show_pie_pic_peer2_6_2=show_pie_pic_peer2_6_2 ,
                                    show_pie_pic_subordinate1_6_2=show_pie_pic_subordinate1_6_2 , 
                                    show_pie_pic_subordinate2_6_2=show_pie_pic_subordinate2_6_2 , 

                                    show_pie_pic_self_6_3=show_pie_pic_self_6_3 , 
                                    show_pie_pic_manager_6_3=show_pie_pic_manager_6_3 , 
                                    show_pie_pic_peer1_6_3=show_pie_pic_peer1_6_3 , 
                                    show_pie_pic_peer2_6_3=show_pie_pic_peer2_6_3 ,
                                    show_pie_pic_subordinate1_6_3=show_pie_pic_subordinate1_6_3 , 
                                    show_pie_pic_subordinate2_6_3=show_pie_pic_subordinate2_6_3 ,

                                    show_pie_pic_self_6_4=show_pie_pic_self_6_4 , 
                                    show_pie_pic_manager_6_4=show_pie_pic_manager_6_4 , 
                                    show_pie_pic_peer1_6_4=show_pie_pic_peer1_6_4 , 
                                    show_pie_pic_peer2_6_4=show_pie_pic_peer2_6_4 ,
                                    show_pie_pic_subordinate1_6_4=show_pie_pic_subordinate1_6_4 , 
                                    show_pie_pic_subordinate2_6_4=show_pie_pic_subordinate2_6_4 ,

                                    show_pie_pic_self_6_5=show_pie_pic_self_6_5 , 
                                    show_pie_pic_manager_6_5=show_pie_pic_manager_6_5 , 
                                    show_pie_pic_peer1_6_5=show_pie_pic_peer1_6_5 , 
                                    show_pie_pic_peer2_6_5=show_pie_pic_peer2_6_5 ,
                                    show_pie_pic_subordinate1_6_5=show_pie_pic_subordinate1_6_5 , 
                                    show_pie_pic_subordinate2_6_5=show_pie_pic_subordinate2_6_5 ,

                                    show_pie_pic_self_total_6_1=show_pie_pic_self_total_6_1 ,
                                    show_pie_pic_self_total_avg_6_1=show_pie_pic_self_total_avg_6_1 ,
                                    show_pie_pic_manager_total_6_1=show_pie_pic_manager_total_6_1 ,
                                    show_pie_pic_manager_total_avg_6_1=show_pie_pic_manager_total_avg_6_1 ,
                                    show_pie_pic_peer1_total_6_1=show_pie_pic_peer1_total_6_1 ,
                                    show_pie_pic_peer1_total_avg_6_1=show_pie_pic_peer1_total_avg_6_1 ,
                                    show_pie_pic_peer2_total_6_1=show_pie_pic_peer2_total_6_1 ,
                                    show_pie_pic_peer2_total_avg_6_1=show_pie_pic_peer2_total_avg_6_1 ,
                                    show_pie_pic_subordinate1_total_6_1=show_pie_pic_subordinate1_total_6_1 ,
                                    show_pie_pic_subordinate1_total_avg_6_1=show_pie_pic_subordinate1_total_avg_6_1 ,
                                    show_pie_pic_subordinate2_total_6_1=show_pie_pic_subordinate2_total_6_1 ,
                                    show_pie_pic_subordinate2_total_avg_6_1=show_pie_pic_subordinate2_total_avg_6_1 ,
                                    show_pie_pic_total_avg_6_1=show_pie_pic_total_avg_6_1 ,

                                    #############
                                    # 綜合雷達圖
                                    #############
                                    show_radar_pic=show_radar_pic 
                                    
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 


#####################################
# /show_hr_360_person_result2
#####################################
@app.route("/show_hr_360_person_result2", methods=['GET','POST'])
def show_hr_360_person_result2():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                s_name = request.form['s_name']

                ### operation record title
                operation_record_title = f'載入 HR - 360 考評 , 受評人員 : {s_name} 總分數資料'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ############
                # 考評人員
                ############
                show_hr_360_person_1_check_data = db.show_hr_360_person_process_total_data2(s_name)
                
                c_name         = db.search_hr_360_person_name(s_name , 'c_name')
                c_manager      = db.search_hr_360_person_name(s_name , 'c_manager')
                c_peer1        = db.search_hr_360_person_name(s_name , 'c_peer1')
                c_peer2        = db.search_hr_360_person_name(s_name , 'c_peer2')
                c_subordinate1 = db.search_hr_360_person_name(s_name , 'c_subordinate1')
                c_subordinate2 = db.search_hr_360_person_name(s_name , 'c_subordinate2')

                #####################################
                # 管理能力
                #####################################
                show_pie_pic_self_1_1         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_manager_1_1      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_peer1_1_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_peer2_1_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_subordinate1_1_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_1_1' , 5 , 'none')
                show_pie_pic_subordinate2_1_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_1_1' , 5 , 'none')

                show_pie_pic_self_1_2         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_manager_1_2      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_peer1_1_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_peer2_1_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_subordinate1_1_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_1_2' , 5 , 'none')
                show_pie_pic_subordinate2_1_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_1_2' , 5 , 'none')
                
                show_pie_pic_self_1_3         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_manager_1_3      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_peer1_1_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_peer2_1_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_subordinate1_1_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_1_3' , 5 , 'none')
                show_pie_pic_subordinate2_1_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_1_3' , 5 , 'none')

                show_pie_pic_self_1_4         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_manager_1_4      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_peer1_1_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_peer2_1_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_subordinate1_1_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_1_4' , 5 , 'none')
                show_pie_pic_subordinate2_1_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_1_4' , 5 , 'none')

                show_pie_pic_self_1_5         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_manager_1_5      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_peer1_1_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_peer2_1_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_subordinate1_1_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_1_5' , 5 , 'none')
                show_pie_pic_subordinate2_1_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_1_5' , 5 , 'none')
                

                show_pie_pic_self_total_1_1             = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_self_total_avg_1           = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_self_total_avg_1_1         = round(float(show_pie_pic_self_total_avg_1) , 2) if show_pie_pic_self_total_avg_1 is not None else 0 
                show_pie_pic_manager_total_1_1          = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_manager_total_avg_1        = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_manager_total_avg_1_1      = round(float(show_pie_pic_manager_total_avg_1) , 2) if show_pie_pic_manager_total_avg_1 is not None else 0
                show_pie_pic_peer1_total_1_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_peer1_total_avg_1          = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_peer1_total_avg_1_1        = round(float(show_pie_pic_peer1_total_avg_1) , 2) if show_pie_pic_peer1_total_avg_1 is not None else 0
                show_pie_pic_peer2_total_1_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_peer2_total_avg_1          = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_peer2_total_avg_1_1        = round(float(show_pie_pic_peer2_total_avg_1) , 2) if show_pie_pic_peer2_total_avg_1 is not None else 0
                show_pie_pic_subordinate1_total_1_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_1   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_subordinate1_total_avg_1_1 = round(float(show_pie_pic_subordinate1_total_avg_1) , 2) if show_pie_pic_subordinate1_total_avg_1 is not None else 0
                show_pie_pic_subordinate2_total_1_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_1' , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_1   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_1_avg' , 5 , 'total')
                show_pie_pic_subordinate2_total_avg_1_1 = round(float(show_pie_pic_subordinate2_total_avg_1) , 2) if show_pie_pic_subordinate2_total_avg_1 is not None else 0
                show_pie_pic_total_avg_1                = (
                                                           float(show_pie_pic_self_total_avg_1_1)     +
                                                           float(show_pie_pic_manager_total_avg_1_1)  + 
                                                           float(show_pie_pic_peer1_total_avg_1_1)     + 
                                                           float(show_pie_pic_peer2_total_avg_1_1)     + 
                                                           float(show_pie_pic_subordinate1_total_avg_1_1)   + 
                                                           float(show_pie_pic_subordinate2_total_avg_1_1))/6 
                show_pie_pic_total_avg_1_1              = round(show_pie_pic_total_avg_1 , 2)
                
                ####################
                # 提供支援
                ####################
                show_pie_pic_self_2_1         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_manager_2_1      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_peer1_2_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_peer2_2_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_subordinate1_2_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_2_1' , 5 , 'none')
                show_pie_pic_subordinate2_2_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_2_1' , 5 , 'none')

                show_pie_pic_self_2_2         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_manager_2_2      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_peer1_2_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_peer2_2_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_subordinate1_2_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_2_2' , 5 , 'none')
                show_pie_pic_subordinate2_2_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_2_2' , 5 , 'none')
                
                show_pie_pic_self_2_3         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_manager_2_3      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_peer1_2_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_peer2_2_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_subordinate1_2_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_2_3' , 5 , 'none')
                show_pie_pic_subordinate2_2_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_2_3' , 5 , 'none')

                show_pie_pic_self_2_4         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_manager_2_4      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_peer1_2_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_peer2_2_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_subordinate1_2_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_2_4' , 5 , 'none')
                show_pie_pic_subordinate2_2_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_2_4' , 5 , 'none')

                show_pie_pic_self_2_5         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_manager_2_5      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_peer1_2_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_peer2_2_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_subordinate1_2_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_2_5' , 5 , 'none')
                show_pie_pic_subordinate2_2_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_2_5' , 5 , 'none')
                
                show_pie_pic_self_2_6         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_2_6' , 5 , 'none')
                show_pie_pic_manager_2_6      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_2_6' , 5 , 'none')
                show_pie_pic_peer1_2_6        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_2_6' , 5 , 'none')
                show_pie_pic_peer2_2_6        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_2_6' , 5 , 'none')
                show_pie_pic_subordinate1_2_6 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_2_6' , 5 , 'none')
                show_pie_pic_subordinate2_2_6 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_2_6' , 5 , 'none')

                show_pie_pic_self_total_2_1             = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_self_total_avg_2           = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_self_total_avg_2_1         = round(float(show_pie_pic_self_total_avg_2) if show_pie_pic_self_total_avg_2 is not None else 0  , 2)
                show_pie_pic_manager_total_2_1          = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_manager_total_avg_2        = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_manager_total_avg_2_1      = round(float(show_pie_pic_manager_total_avg_2) if show_pie_pic_manager_total_avg_2 is not None else 0  , 2)
                show_pie_pic_peer1_total_2_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_peer1_total_avg_2          = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_peer1_total_avg_2_1        = round(float(show_pie_pic_peer1_total_avg_2) if show_pie_pic_peer1_total_avg_2 is not None else 0  , 2)
                show_pie_pic_peer2_total_2_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_peer2_total_avg_2          = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_peer2_total_avg_2_1        = round(float(show_pie_pic_peer2_total_avg_2) if show_pie_pic_peer2_total_avg_2 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_2_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_2   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_subordinate1_total_avg_2_1 = round(float(show_pie_pic_subordinate1_total_avg_2) if show_pie_pic_subordinate1_total_avg_2 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_2_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_2' , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_2   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_2_avg' , 5 , 'total')
                show_pie_pic_subordinate2_total_avg_2_1 = round(float(show_pie_pic_subordinate2_total_avg_2) if show_pie_pic_subordinate2_total_avg_2 is not None else 0  , 2 )
                show_pie_pic_total_avg_2                = (float(show_pie_pic_self_total_avg_2_1)    + 
                                                           float(show_pie_pic_manager_total_avg_2_1) + 
                                                           float(show_pie_pic_peer1_total_avg_2_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_2_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_2_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_2_1) )/6 
                show_pie_pic_total_avg_2_1              = round(show_pie_pic_total_avg_2 , 2)

                ############
                # 以身作則
                ############
                show_pie_pic_self_3_1         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_manager_3_1      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_peer1_3_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_peer2_3_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_subordinate1_3_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_3_1' , 5 , 'none')
                show_pie_pic_subordinate2_3_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_3_1' , 5 , 'none')

                show_pie_pic_self_3_2         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_manager_3_2      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_peer1_3_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_peer2_3_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_subordinate1_3_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_3_2' , 5 , 'none')
                show_pie_pic_subordinate2_3_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_3_2' , 5 , 'none')
                
                show_pie_pic_self_3_3         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_manager_3_3      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_peer1_3_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_peer2_3_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_subordinate1_3_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_3_3' , 5 , 'none')
                show_pie_pic_subordinate2_3_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_3_3' , 5 , 'none')

                show_pie_pic_self_3_4         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_manager_3_4      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_peer1_3_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_peer2_3_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_subordinate1_3_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_3_4' , 5 , 'none')
                show_pie_pic_subordinate2_3_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_3_4' , 5 , 'none')

                show_pie_pic_self_3_5         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_manager_3_5      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_peer1_3_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_peer2_3_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_subordinate1_3_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_3_5' , 5 , 'none')
                show_pie_pic_subordinate2_3_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_3_5' , 5 , 'none')

                show_pie_pic_self_total_3_1             = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_self_total_avg_3           = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_self_total_avg_3_1         = round(float(show_pie_pic_self_total_avg_3) if show_pie_pic_self_total_avg_3 is not None else 0  , 2)
                show_pie_pic_manager_total_3_1          = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_manager_total_avg_3        = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_manager_total_avg_3_1      = round(float(show_pie_pic_manager_total_avg_3) if show_pie_pic_manager_total_avg_3 is not None else 0  , 2)
                show_pie_pic_peer1_total_3_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_peer1_total_avg_3          = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_peer1_total_avg_3_1        = round(float(show_pie_pic_peer1_total_avg_3) if show_pie_pic_peer1_total_avg_3 is not None else 0  , 2)
                show_pie_pic_peer2_total_3_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_peer2_total_avg_3          = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_peer2_total_avg_3_1        = round(float(show_pie_pic_peer2_total_avg_3) if show_pie_pic_peer2_total_avg_3 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_3_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_3   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_subordinate1_total_avg_3_1 = round(float(show_pie_pic_subordinate1_total_avg_3) if show_pie_pic_subordinate1_total_avg_3 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_3_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_3'     , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_3   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_3_avg' , 5  , 'total')
                show_pie_pic_subordinate2_total_avg_3_1 = round(float(show_pie_pic_subordinate2_total_avg_3) if show_pie_pic_subordinate2_total_avg_3 is not None else 0  , 2 )
                show_pie_pic_total_avg_3                = (float(show_pie_pic_self_total_avg_3_1)    + 
                                                           float(show_pie_pic_manager_total_avg_3_1) + 
                                                           float(show_pie_pic_peer1_total_avg_3_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_3_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_3_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_3_1) )/6 
                show_pie_pic_total_avg_3_1              = round(show_pie_pic_total_avg_3 , 2)
                
                ##################
                # 效率導向
                ##################
                show_pie_pic_self_4_1         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_manager_4_1      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_peer1_4_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_peer2_4_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_subordinate1_4_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_4_1' , 5 , 'none')
                show_pie_pic_subordinate2_4_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_4_1' , 5 , 'none')

                show_pie_pic_self_4_2         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_manager_4_2      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_peer1_4_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_peer2_4_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_subordinate1_4_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_4_2' , 5 , 'none')
                show_pie_pic_subordinate2_4_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_4_2' , 5 , 'none')
                
                show_pie_pic_self_4_3         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_manager_4_3      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_peer1_4_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_peer2_4_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_subordinate1_4_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_4_3' , 5 , 'none')
                show_pie_pic_subordinate2_4_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_4_3' , 5 , 'none')

                show_pie_pic_self_4_4         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_manager_4_4      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_peer1_4_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_peer2_4_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_subordinate1_4_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_4_4' , 5 , 'none')
                show_pie_pic_subordinate2_4_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_4_4' , 5 , 'none')

                show_pie_pic_self_total_4_1             = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_self_total_avg_4           = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_self_total_avg_4_1         = round(float(show_pie_pic_self_total_avg_4) if show_pie_pic_self_total_avg_4 is not None else 0  , 2)
                show_pie_pic_manager_total_4_1          = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_manager_total_avg_4        = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_manager_total_avg_4_1      = round(float(show_pie_pic_manager_total_avg_4) if show_pie_pic_manager_total_avg_4 is not None else 0  , 2)
                show_pie_pic_peer1_total_4_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_peer1_total_avg_4          = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_peer1_total_avg_4_1        = round(float(show_pie_pic_peer1_total_avg_4) if show_pie_pic_peer1_total_avg_4 is not None else 0  , 2)
                show_pie_pic_peer2_total_4_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_peer2_total_avg_4          = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_peer2_total_avg_4_1        = round(float(show_pie_pic_peer2_total_avg_4) if show_pie_pic_peer2_total_avg_4 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_4_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_4   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_subordinate1_total_avg_4_1 = round(float(show_pie_pic_subordinate1_total_avg_4) if show_pie_pic_subordinate1_total_avg_4 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_4_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_4'     , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_4   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_4_avg' , 5  , 'total')
                show_pie_pic_subordinate2_total_avg_4_1 = round(float(show_pie_pic_subordinate2_total_avg_4) if show_pie_pic_subordinate2_total_avg_4 is not None else 0  , 2 )
                show_pie_pic_total_avg_4                = (float(show_pie_pic_self_total_avg_4_1)    + 
                                                           float(show_pie_pic_manager_total_avg_4_1) + 
                                                           float(show_pie_pic_peer1_total_avg_4_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_4_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_4_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_4_1) )/6 
                show_pie_pic_total_avg_4_1              = round(show_pie_pic_total_avg_4 , 2)
                
                ############
                # 培育人才
                ############
                show_pie_pic_self_5_1         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_manager_5_1      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_peer1_5_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_peer2_5_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_subordinate1_5_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_5_1' , 5 , 'none')
                show_pie_pic_subordinate2_5_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_5_1' , 5 , 'none')

                show_pie_pic_self_5_2         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_manager_5_2      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_peer1_5_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_peer2_5_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_subordinate1_5_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_5_2' , 5 , 'none')
                show_pie_pic_subordinate2_5_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_5_2' , 5 , 'none')
                
                show_pie_pic_self_5_3         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_manager_5_3      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_peer1_5_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_peer2_5_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_subordinate1_5_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_5_3' , 5 , 'none')
                show_pie_pic_subordinate2_5_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_5_3' , 5 , 'none')

                show_pie_pic_self_total_5_1             = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_self_total_avg_5           = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_self_total_avg_5_1         = round(float(show_pie_pic_self_total_avg_5) if show_pie_pic_self_total_avg_5 is not None else 0  , 2)
                show_pie_pic_manager_total_5_1          = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_manager_total_avg_5        = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_manager_total_avg_5_1      = round(float(show_pie_pic_manager_total_avg_5) if show_pie_pic_manager_total_avg_5 is not None else 0  , 2)
                show_pie_pic_peer1_total_5_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_peer1_total_avg_5          = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_peer1_total_avg_5_1        = round(float(show_pie_pic_peer1_total_avg_5) if show_pie_pic_peer1_total_avg_5 is not None else 0  , 2)
                show_pie_pic_peer2_total_5_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_peer2_total_avg_5          = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_peer2_total_avg_5_1        = round(float(show_pie_pic_peer2_total_avg_5) if show_pie_pic_peer2_total_avg_5 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_5_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_5   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_subordinate1_total_avg_5_1 = round(float(show_pie_pic_subordinate1_total_avg_5) if show_pie_pic_subordinate1_total_avg_5 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_5_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_5'     , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_5   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_5_avg' , 5  , 'total')
                show_pie_pic_subordinate2_total_avg_5_1 = round(float(show_pie_pic_subordinate2_total_avg_5) if show_pie_pic_subordinate2_total_avg_5 is not None else 0  , 2 )
                show_pie_pic_total_avg_5                = (float(show_pie_pic_self_total_avg_5_1)    + 
                                                           float(show_pie_pic_manager_total_avg_5_1) + 
                                                           float(show_pie_pic_peer1_total_avg_5_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_5_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_5_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_5_1) )/6 
                show_pie_pic_total_avg_5_1              = round(show_pie_pic_total_avg_5 , 2)

                ############
                # 高效溝通
                ############
                show_pie_pic_self_6_1         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_6_1' , 5 , 'none')
                show_pie_pic_manager_6_1      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_6_1' , 5 , 'none')
                show_pie_pic_peer1_6_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_6_1' , 5 , 'none')
                show_pie_pic_peer2_6_1        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_6_1' , 5 , 'none')
                show_pie_pic_subordinate1_6_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_6_1' , 5 , 'none')
                show_pie_pic_subordinate2_6_1 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_6_1' , 5 , 'none')

                show_pie_pic_self_6_2         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_6_2' , 5 , 'none')
                show_pie_pic_manager_6_2      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_6_2' , 5 , 'none')
                show_pie_pic_peer1_6_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_6_2' , 5 , 'none')
                show_pie_pic_peer2_6_2        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_6_2' , 5 , 'none')
                show_pie_pic_subordinate1_6_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_6_2' , 5 , 'none')
                show_pie_pic_subordinate2_6_2 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_6_2' , 5 , 'none')
                
                show_pie_pic_self_6_3         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_6_3' , 5 , 'none')
                show_pie_pic_manager_6_3      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_6_3' , 5 , 'none')
                show_pie_pic_peer1_6_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_6_3' , 5 , 'none')
                show_pie_pic_peer2_6_3        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_6_3' , 5 , 'none')
                show_pie_pic_subordinate1_6_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_6_3' , 5 , 'none')
                show_pie_pic_subordinate2_6_3 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_6_3' , 5 , 'none')

                show_pie_pic_self_6_4         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_6_4' , 5 , 'none')
                show_pie_pic_manager_6_4      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_6_4' , 5 , 'none')
                show_pie_pic_peer1_6_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_6_4' , 5 , 'none')
                show_pie_pic_peer2_6_4        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_6_4' , 5 , 'none')
                show_pie_pic_subordinate1_6_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_6_4' , 5 , 'none')
                show_pie_pic_subordinate2_6_4 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_6_4' , 5 , 'none')

                show_pie_pic_self_6_5         = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_6_5' , 5 , 'none')
                show_pie_pic_manager_6_5      = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_6_5' , 5 , 'none')
                show_pie_pic_peer1_6_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_6_5' , 5 , 'none')
                show_pie_pic_peer2_6_5        = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_6_5' , 5 , 'none')
                show_pie_pic_subordinate1_6_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_6_5' , 5 , 'none')
                show_pie_pic_subordinate2_6_5 = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_6_5' , 5 , 'none')

                show_pie_pic_self_total_6_1             = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_6'     , 25 , 'total')
                show_pie_pic_self_total_avg_6           = db.show_hr_360_person_process_total_data3(s_name , c_name         , 's_hr_360_total_6_avg' , 5  , 'total')
                show_pie_pic_self_total_avg_6_1         = round(float(show_pie_pic_self_total_avg_6) if show_pie_pic_self_total_avg_6 is not None else 0  , 2)
                show_pie_pic_manager_total_6_1          = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_6'     , 25 , 'total')
                show_pie_pic_manager_total_avg_6        = db.show_hr_360_person_process_total_data3(s_name , c_manager      , 's_hr_360_total_6_avg' , 5  , 'total')
                show_pie_pic_manager_total_avg_6_1      = round(float(show_pie_pic_manager_total_avg_6) if show_pie_pic_manager_total_avg_6 is not None else 0  , 2)
                show_pie_pic_peer1_total_6_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_6'     , 25 , 'total')
                show_pie_pic_peer1_total_avg_6          = db.show_hr_360_person_process_total_data3(s_name , c_peer1        , 's_hr_360_total_6_avg' , 5  , 'total')
                show_pie_pic_peer1_total_avg_6_1        = round(float(show_pie_pic_peer1_total_avg_6) if show_pie_pic_peer1_total_avg_6 is not None else 0  , 2)
                show_pie_pic_peer2_total_6_1            = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_6'     , 25 , 'total')
                show_pie_pic_peer2_total_avg_6          = db.show_hr_360_person_process_total_data3(s_name , c_peer2        , 's_hr_360_total_6_avg' , 5  , 'total')
                show_pie_pic_peer2_total_avg_6_1        = round(float(show_pie_pic_peer2_total_avg_6) if show_pie_pic_peer2_total_avg_6 is not None else 0  , 2)
                show_pie_pic_subordinate1_total_6_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_6'     , 25 , 'total')
                show_pie_pic_subordinate1_total_avg_6   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate1 , 's_hr_360_total_6_avg' , 5  , 'total')
                show_pie_pic_subordinate1_total_avg_6_1 = round(float(show_pie_pic_subordinate1_total_avg_6) if show_pie_pic_subordinate1_total_avg_6 is not None else 0  , 2)
                show_pie_pic_subordinate2_total_6_1     = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_6'     , 25 , 'total')
                show_pie_pic_subordinate2_total_avg_6   = db.show_hr_360_person_process_total_data3(s_name , c_subordinate2 , 's_hr_360_total_6_avg' , 5  , 'total')
                show_pie_pic_subordinate2_total_avg_6_1 = round(float(show_pie_pic_subordinate2_total_avg_6) if show_pie_pic_subordinate2_total_avg_6 is not None else 0  , 2 )
                show_pie_pic_total_avg_6                = (float(show_pie_pic_self_total_avg_6_1)    + 
                                                           float(show_pie_pic_manager_total_avg_6_1) + 
                                                           float(show_pie_pic_peer1_total_avg_6_1)   + 
                                                           float(show_pie_pic_peer2_total_avg_6_1)   + 
                                                           float(show_pie_pic_subordinate1_total_avg_6_1) + 
                                                           float(show_pie_pic_subordinate2_total_avg_6_1) )/6 
                show_pie_pic_total_avg_6_1              = round(show_pie_pic_total_avg_6 , 2)

                ############
                # 雷達圖
                ############
                show_radar_pic_num1 = ([float(show_pie_pic_self_total_avg_1_1) , float(show_pie_pic_self_total_avg_2_1) , float(show_pie_pic_self_total_avg_3_1) , float(show_pie_pic_self_total_avg_4_1) , float(show_pie_pic_self_total_avg_5_1) , float(show_pie_pic_self_total_avg_6_1) , ])
                show_radar_pic_num2 = ([float(show_pie_pic_manager_total_avg_1_1) , float(show_pie_pic_manager_total_avg_2_1) , float(show_pie_pic_manager_total_avg_3_1) , float(show_pie_pic_manager_total_avg_4_1) , float(show_pie_pic_manager_total_avg_5_1) , float(show_pie_pic_manager_total_avg_6_1) , ])
                show_radar_pic_num3 = ([float(show_pie_pic_peer1_total_avg_1_1) , float(show_pie_pic_peer1_total_avg_2_1) , float(show_pie_pic_peer1_total_avg_3_1) , float(show_pie_pic_peer1_total_avg_4_1) , float(show_pie_pic_peer1_total_avg_5_1) , float(show_pie_pic_peer1_total_avg_6_1) , ])
                show_radar_pic_num4 = ([float(show_pie_pic_peer2_total_avg_1_1) , float(show_pie_pic_peer2_total_avg_2_1) , float(show_pie_pic_peer2_total_avg_3_1) , float(show_pie_pic_peer2_total_avg_4_1) , float(show_pie_pic_peer2_total_avg_5_1) , float(show_pie_pic_peer2_total_avg_6_1) , ])
                show_radar_pic_num5 = ([float(show_pie_pic_subordinate1_total_avg_1_1) , float(show_pie_pic_subordinate1_total_avg_2_1) , float(show_pie_pic_subordinate1_total_avg_3_1) , float(show_pie_pic_subordinate1_total_avg_4_1) , float(show_pie_pic_subordinate1_total_avg_5_1) , float(show_pie_pic_subordinate1_total_avg_6_1) , ])
                show_radar_pic_num6 = ([float(show_pie_pic_subordinate2_total_avg_1_1) , float(show_pie_pic_subordinate2_total_avg_2_1) , float(show_pie_pic_subordinate2_total_avg_3_1) , float(show_pie_pic_subordinate2_total_avg_4_1) , float(show_pie_pic_subordinate2_total_avg_5_1) , float(show_pie_pic_subordinate2_total_avg_6_1) , ])
                show_radar_pic      = db.show_radar_picture(show_radar_pic_num1 , show_radar_pic_num2 , show_radar_pic_num3 , show_radar_pic_num4 , show_radar_pic_num5 , show_radar_pic_num6)

                return render_template('ajax/load_hr_360_dep_member_process_list_res2.html' , 
                                    show_hr_360_person_1_check_data=show_hr_360_person_1_check_data , s_name=s_name , 
                                    
                                    #####################################
                                    # 管理能力
                                    #####################################
                                    show_pie_pic_self_1_1=show_pie_pic_self_1_1 ,
                                    show_pie_pic_manager_1_1=show_pie_pic_manager_1_1 , 
                                    show_pie_pic_peer1_1_1=show_pie_pic_peer1_1_1 , 
                                    show_pie_pic_peer2_1_1=show_pie_pic_peer2_1_1 ,
                                    show_pie_pic_subordinate1_1_1=show_pie_pic_subordinate1_1_1 , 
                                    show_pie_pic_subordinate2_1_1=show_pie_pic_subordinate2_1_1 ,

                                    show_pie_pic_self_1_2=show_pie_pic_self_1_2 , 
                                    show_pie_pic_manager_1_2=show_pie_pic_manager_1_2 , 
                                    show_pie_pic_peer1_1_2=show_pie_pic_peer1_1_2 , 
                                    show_pie_pic_peer2_1_2=show_pie_pic_peer2_1_2 ,
                                    show_pie_pic_subordinate1_1_2=show_pie_pic_subordinate1_1_2 , 
                                    show_pie_pic_subordinate2_1_2=show_pie_pic_subordinate2_1_2 , 

                                    show_pie_pic_self_1_3=show_pie_pic_self_1_3 , 
                                    show_pie_pic_manager_1_3=show_pie_pic_manager_1_3 , 
                                    show_pie_pic_peer1_1_3=show_pie_pic_peer1_1_3 , 
                                    show_pie_pic_peer2_1_3=show_pie_pic_peer2_1_3 ,
                                    show_pie_pic_subordinate1_1_3=show_pie_pic_subordinate1_1_3 , 
                                    show_pie_pic_subordinate2_1_3=show_pie_pic_subordinate2_1_3 ,

                                    show_pie_pic_self_1_4=show_pie_pic_self_1_4 , 
                                    show_pie_pic_manager_1_4=show_pie_pic_manager_1_4 , 
                                    show_pie_pic_peer1_1_4=show_pie_pic_peer1_1_4 , 
                                    show_pie_pic_peer2_1_4=show_pie_pic_peer2_1_4 ,
                                    show_pie_pic_subordinate1_1_4=show_pie_pic_subordinate1_1_4 , 
                                    show_pie_pic_subordinate2_1_4=show_pie_pic_subordinate2_1_4 , 

                                    show_pie_pic_self_1_5=show_pie_pic_self_1_5 , 
                                    show_pie_pic_manager_1_5=show_pie_pic_manager_1_5 , 
                                    show_pie_pic_peer1_1_5=show_pie_pic_peer1_1_5 , 
                                    show_pie_pic_peer2_1_5=show_pie_pic_peer2_1_5 ,
                                    show_pie_pic_subordinate1_1_5=show_pie_pic_subordinate1_1_5 , 
                                    show_pie_pic_subordinate2_1_5=show_pie_pic_subordinate2_1_5 , 

                                    show_pie_pic_self_total_1_1=show_pie_pic_self_total_1_1 ,
                                    show_pie_pic_self_total_avg_1_1=show_pie_pic_self_total_avg_1_1 ,
                                    show_pie_pic_manager_total_1_1=show_pie_pic_manager_total_1_1 ,
                                    show_pie_pic_manager_total_avg_1_1=show_pie_pic_manager_total_avg_1_1 ,
                                    show_pie_pic_peer1_total_1_1=show_pie_pic_peer1_total_1_1 ,
                                    show_pie_pic_peer1_total_avg_1_1=show_pie_pic_peer1_total_avg_1_1 ,
                                    show_pie_pic_peer2_total_1_1=show_pie_pic_peer2_total_1_1 ,
                                    show_pie_pic_peer2_total_avg_1_1=show_pie_pic_peer2_total_avg_1_1 ,
                                    show_pie_pic_subordinate1_total_1_1=show_pie_pic_subordinate1_total_1_1 ,
                                    show_pie_pic_subordinate1_total_avg_1_1=show_pie_pic_subordinate1_total_avg_1_1 ,
                                    show_pie_pic_subordinate2_total_1_1=show_pie_pic_subordinate2_total_1_1 ,
                                    show_pie_pic_subordinate2_total_avg_1_1=show_pie_pic_subordinate2_total_avg_1_1 ,
                                    show_pie_pic_total_avg_1_1=show_pie_pic_total_avg_1_1 ,
                                    
                                    ####################
                                    # 提供支援
                                    ####################
                                    show_pie_pic_self_2_1=show_pie_pic_self_2_1 ,
                                    show_pie_pic_manager_2_1=show_pie_pic_manager_2_1 , 
                                    show_pie_pic_peer1_2_1=show_pie_pic_peer1_2_1 , 
                                    show_pie_pic_peer2_2_1=show_pie_pic_peer2_2_1 ,
                                    show_pie_pic_subordinate1_2_1=show_pie_pic_subordinate1_2_1 , 
                                    show_pie_pic_subordinate2_2_1=show_pie_pic_subordinate2_2_1 ,

                                    show_pie_pic_self_2_2=show_pie_pic_self_2_2 , 
                                    show_pie_pic_manager_2_2=show_pie_pic_manager_2_2 , 
                                    show_pie_pic_peer1_2_2=show_pie_pic_peer1_2_2 , 
                                    show_pie_pic_peer2_2_2=show_pie_pic_peer2_2_2 ,
                                    show_pie_pic_subordinate1_2_2=show_pie_pic_subordinate1_2_2 , 
                                    show_pie_pic_subordinate2_2_2=show_pie_pic_subordinate2_2_2 , 

                                    show_pie_pic_self_2_3=show_pie_pic_self_2_3 , 
                                    show_pie_pic_manager_2_3=show_pie_pic_manager_2_3 , 
                                    show_pie_pic_peer1_2_3=show_pie_pic_peer1_2_3 , 
                                    show_pie_pic_peer2_2_3=show_pie_pic_peer2_2_3 ,
                                    show_pie_pic_subordinate1_2_3=show_pie_pic_subordinate1_2_3 , 
                                    show_pie_pic_subordinate2_2_3=show_pie_pic_subordinate2_2_3 ,

                                    show_pie_pic_self_2_4=show_pie_pic_self_2_4 , 
                                    show_pie_pic_manager_2_4=show_pie_pic_manager_2_4 , 
                                    show_pie_pic_peer1_2_4=show_pie_pic_peer1_2_4 , 
                                    show_pie_pic_peer2_2_4=show_pie_pic_peer2_2_4 ,
                                    show_pie_pic_subordinate1_2_4=show_pie_pic_subordinate1_2_4 , 
                                    show_pie_pic_subordinate2_2_4=show_pie_pic_subordinate2_2_4 , 

                                    show_pie_pic_self_2_5=show_pie_pic_self_2_5 , 
                                    show_pie_pic_manager_2_5=show_pie_pic_manager_2_5 , 
                                    show_pie_pic_peer1_2_5=show_pie_pic_peer1_2_5 , 
                                    show_pie_pic_peer2_2_5=show_pie_pic_peer2_2_5 ,
                                    show_pie_pic_subordinate1_2_5=show_pie_pic_subordinate1_2_5 , 
                                    show_pie_pic_subordinate2_2_5=show_pie_pic_subordinate2_2_5 , 

                                    show_pie_pic_self_2_6=show_pie_pic_self_2_6 , 
                                    show_pie_pic_manager_2_6=show_pie_pic_manager_2_6 , 
                                    show_pie_pic_peer1_2_6=show_pie_pic_peer1_2_6 , 
                                    show_pie_pic_peer2_2_6=show_pie_pic_peer2_2_6 ,
                                    show_pie_pic_subordinate1_2_6=show_pie_pic_subordinate1_2_6 , 
                                    show_pie_pic_subordinate2_2_6=show_pie_pic_subordinate2_2_6 , 
                                    
                                    show_pie_pic_self_total_2_1=show_pie_pic_self_total_2_1 ,
                                    show_pie_pic_self_total_avg_2_1=show_pie_pic_self_total_avg_2_1 ,
                                    show_pie_pic_manager_total_2_1=show_pie_pic_manager_total_2_1 ,
                                    show_pie_pic_manager_total_avg_2_1=show_pie_pic_manager_total_avg_2_1 ,
                                    show_pie_pic_peer1_total_2_1=show_pie_pic_peer1_total_2_1 ,
                                    show_pie_pic_peer1_total_avg_2_1=show_pie_pic_peer1_total_avg_2_1 ,
                                    show_pie_pic_peer2_total_2_1=show_pie_pic_peer2_total_2_1 ,
                                    show_pie_pic_peer2_total_avg_2_1=show_pie_pic_peer2_total_avg_2_1 ,
                                    show_pie_pic_subordinate1_total_2_1=show_pie_pic_subordinate1_total_2_1 ,
                                    show_pie_pic_subordinate1_total_avg_2_1=show_pie_pic_subordinate1_total_avg_2_1 ,
                                    show_pie_pic_subordinate2_total_2_1=show_pie_pic_subordinate2_total_2_1 ,
                                    show_pie_pic_subordinate2_total_avg_2_1=show_pie_pic_subordinate2_total_avg_2_1 ,
                                    show_pie_pic_total_avg_2_1=show_pie_pic_total_avg_2_1 ,
                                    
                                    ############
                                    # 以身作則
                                    ############
                                    show_pie_pic_self_3_1=show_pie_pic_self_3_1 ,
                                    show_pie_pic_manager_3_1=show_pie_pic_manager_3_1 , 
                                    show_pie_pic_peer1_3_1=show_pie_pic_peer1_3_1 , 
                                    show_pie_pic_peer2_3_1=show_pie_pic_peer2_3_1 ,
                                    show_pie_pic_subordinate1_3_1=show_pie_pic_subordinate1_3_1 , 
                                    show_pie_pic_subordinate2_3_1=show_pie_pic_subordinate2_3_1 ,

                                    show_pie_pic_self_3_2=show_pie_pic_self_3_2 , 
                                    show_pie_pic_manager_3_2=show_pie_pic_manager_3_2 , 
                                    show_pie_pic_peer1_3_2=show_pie_pic_peer1_3_2 , 
                                    show_pie_pic_peer2_3_2=show_pie_pic_peer2_3_2 ,
                                    show_pie_pic_subordinate1_3_2=show_pie_pic_subordinate1_3_2 , 
                                    show_pie_pic_subordinate2_3_2=show_pie_pic_subordinate2_3_2 , 

                                    show_pie_pic_self_3_3=show_pie_pic_self_3_3 , 
                                    show_pie_pic_manager_3_3=show_pie_pic_manager_3_3 , 
                                    show_pie_pic_peer1_3_3=show_pie_pic_peer1_3_3 , 
                                    show_pie_pic_peer2_3_3=show_pie_pic_peer2_3_3 ,
                                    show_pie_pic_subordinate1_3_3=show_pie_pic_subordinate1_3_3 , 
                                    show_pie_pic_subordinate2_3_3=show_pie_pic_subordinate2_3_3 ,

                                    show_pie_pic_self_3_4=show_pie_pic_self_3_4 , 
                                    show_pie_pic_manager_3_4=show_pie_pic_manager_3_4 , 
                                    show_pie_pic_peer1_3_4=show_pie_pic_peer1_3_4 , 
                                    show_pie_pic_peer2_3_4=show_pie_pic_peer2_3_4 ,
                                    show_pie_pic_subordinate1_3_4=show_pie_pic_subordinate1_3_4 , 
                                    show_pie_pic_subordinate2_3_4=show_pie_pic_subordinate2_3_4 , 

                                    show_pie_pic_self_3_5=show_pie_pic_self_3_5 , 
                                    show_pie_pic_manager_3_5=show_pie_pic_manager_3_5 , 
                                    show_pie_pic_peer1_3_5=show_pie_pic_peer1_3_5 , 
                                    show_pie_pic_peer2_3_5=show_pie_pic_peer2_3_5 ,
                                    show_pie_pic_subordinate1_3_5=show_pie_pic_subordinate1_3_5 , 
                                    show_pie_pic_subordinate2_3_5=show_pie_pic_subordinate2_3_5 , 
                                    
                                    show_pie_pic_self_total_3_1=show_pie_pic_self_total_3_1 ,
                                    show_pie_pic_self_total_avg_3_1=show_pie_pic_self_total_avg_3_1 ,
                                    show_pie_pic_manager_total_3_1=show_pie_pic_manager_total_3_1 ,
                                    show_pie_pic_manager_total_avg_3_1=show_pie_pic_manager_total_avg_3_1 ,
                                    show_pie_pic_peer1_total_3_1=show_pie_pic_peer1_total_3_1 ,
                                    show_pie_pic_peer1_total_avg_3_1=show_pie_pic_peer1_total_avg_3_1 ,
                                    show_pie_pic_peer2_total_3_1=show_pie_pic_peer2_total_3_1 ,
                                    show_pie_pic_peer2_total_avg_3_1=show_pie_pic_peer2_total_avg_3_1 ,
                                    show_pie_pic_subordinate1_total_3_1=show_pie_pic_subordinate1_total_3_1 ,
                                    show_pie_pic_subordinate1_total_avg_3_1=show_pie_pic_subordinate1_total_avg_3_1 ,
                                    show_pie_pic_subordinate2_total_3_1=show_pie_pic_subordinate2_total_3_1 ,
                                    show_pie_pic_subordinate2_total_avg_3_1=show_pie_pic_subordinate2_total_avg_3_1 ,
                                    show_pie_pic_total_avg_3_1=show_pie_pic_total_avg_3_1 ,
                                    
                                    ##################
                                    # 效率導向
                                    ##################
                                    show_pie_pic_self_4_1=show_pie_pic_self_4_1 ,
                                    show_pie_pic_manager_4_1=show_pie_pic_manager_4_1 , 
                                    show_pie_pic_peer1_4_1=show_pie_pic_peer1_4_1 , 
                                    show_pie_pic_peer2_4_1=show_pie_pic_peer2_4_1 ,
                                    show_pie_pic_subordinate1_4_1=show_pie_pic_subordinate1_4_1 , 
                                    show_pie_pic_subordinate2_4_1=show_pie_pic_subordinate2_4_1 ,

                                    show_pie_pic_self_4_2=show_pie_pic_self_4_2 , 
                                    show_pie_pic_manager_4_2=show_pie_pic_manager_4_2 , 
                                    show_pie_pic_peer1_4_2=show_pie_pic_peer1_4_2 , 
                                    show_pie_pic_peer2_4_2=show_pie_pic_peer2_4_2 ,
                                    show_pie_pic_subordinate1_4_2=show_pie_pic_subordinate1_4_2 , 
                                    show_pie_pic_subordinate2_4_2=show_pie_pic_subordinate2_4_2 , 

                                    show_pie_pic_self_4_3=show_pie_pic_self_4_3 , 
                                    show_pie_pic_manager_4_3=show_pie_pic_manager_4_3 , 
                                    show_pie_pic_peer1_4_3=show_pie_pic_peer1_4_3 , 
                                    show_pie_pic_peer2_4_3=show_pie_pic_peer2_4_3 ,
                                    show_pie_pic_subordinate1_4_3=show_pie_pic_subordinate1_4_3 , 
                                    show_pie_pic_subordinate2_4_3=show_pie_pic_subordinate2_4_3 ,

                                    show_pie_pic_self_4_4=show_pie_pic_self_4_4 , 
                                    show_pie_pic_manager_4_4=show_pie_pic_manager_4_4 , 
                                    show_pie_pic_peer1_4_4=show_pie_pic_peer1_4_4 , 
                                    show_pie_pic_peer2_4_4=show_pie_pic_peer2_4_4 ,
                                    show_pie_pic_subordinate1_4_4=show_pie_pic_subordinate1_4_4 , 
                                    show_pie_pic_subordinate2_4_4=show_pie_pic_subordinate2_4_4 , 

                                    show_pie_pic_self_total_4_1=show_pie_pic_self_total_4_1 ,
                                    show_pie_pic_self_total_avg_4_1=show_pie_pic_self_total_avg_4_1 ,
                                    show_pie_pic_manager_total_4_1=show_pie_pic_manager_total_4_1 ,
                                    show_pie_pic_manager_total_avg_4_1=show_pie_pic_manager_total_avg_4_1 ,
                                    show_pie_pic_peer1_total_4_1=show_pie_pic_peer1_total_4_1 ,
                                    show_pie_pic_peer1_total_avg_4_1=show_pie_pic_peer1_total_avg_4_1 ,
                                    show_pie_pic_peer2_total_4_1=show_pie_pic_peer2_total_4_1 ,
                                    show_pie_pic_peer2_total_avg_4_1=show_pie_pic_peer2_total_avg_4_1 ,
                                    show_pie_pic_subordinate1_total_4_1=show_pie_pic_subordinate1_total_4_1 ,
                                    show_pie_pic_subordinate1_total_avg_4_1=show_pie_pic_subordinate1_total_avg_4_1 ,
                                    show_pie_pic_subordinate2_total_4_1=show_pie_pic_subordinate2_total_4_1 ,
                                    show_pie_pic_subordinate2_total_avg_4_1=show_pie_pic_subordinate2_total_avg_4_1 ,
                                    show_pie_pic_total_avg_4_1=show_pie_pic_total_avg_4_1 ,
                                    
                                    ############
                                    # 培育人才
                                    ############
                                    show_pie_pic_self_5_1=show_pie_pic_self_5_1 ,
                                    show_pie_pic_manager_5_1=show_pie_pic_manager_5_1 , 
                                    show_pie_pic_peer1_5_1=show_pie_pic_peer1_5_1 , 
                                    show_pie_pic_peer2_5_1=show_pie_pic_peer2_5_1 ,
                                    show_pie_pic_subordinate1_5_1=show_pie_pic_subordinate1_5_1 , 
                                    show_pie_pic_subordinate2_5_1=show_pie_pic_subordinate2_5_1 ,

                                    show_pie_pic_self_5_2=show_pie_pic_self_5_2 , 
                                    show_pie_pic_manager_5_2=show_pie_pic_manager_5_2 , 
                                    show_pie_pic_peer1_5_2=show_pie_pic_peer1_5_2 , 
                                    show_pie_pic_peer2_5_2=show_pie_pic_peer2_5_2 ,
                                    show_pie_pic_subordinate1_5_2=show_pie_pic_subordinate1_5_2 , 
                                    show_pie_pic_subordinate2_5_2=show_pie_pic_subordinate2_5_2 , 

                                    show_pie_pic_self_5_3=show_pie_pic_self_5_3 , 
                                    show_pie_pic_manager_5_3=show_pie_pic_manager_5_3 , 
                                    show_pie_pic_peer1_5_3=show_pie_pic_peer1_5_3 , 
                                    show_pie_pic_peer2_5_3=show_pie_pic_peer2_5_3 ,
                                    show_pie_pic_subordinate1_5_3=show_pie_pic_subordinate1_5_3 , 
                                    show_pie_pic_subordinate2_5_3=show_pie_pic_subordinate2_5_3 ,

                                    show_pie_pic_self_total_5_1=show_pie_pic_self_total_5_1 ,
                                    show_pie_pic_self_total_avg_5_1=show_pie_pic_self_total_avg_5_1 ,
                                    show_pie_pic_manager_total_5_1=show_pie_pic_manager_total_5_1 ,
                                    show_pie_pic_manager_total_avg_5_1=show_pie_pic_manager_total_avg_5_1 ,
                                    show_pie_pic_peer1_total_5_1=show_pie_pic_peer1_total_5_1 ,
                                    show_pie_pic_peer1_total_avg_5_1=show_pie_pic_peer1_total_avg_5_1 ,
                                    show_pie_pic_peer2_total_5_1=show_pie_pic_peer2_total_5_1 ,
                                    show_pie_pic_peer2_total_avg_5_1=show_pie_pic_peer2_total_avg_5_1 ,
                                    show_pie_pic_subordinate1_total_5_1=show_pie_pic_subordinate1_total_5_1 ,
                                    show_pie_pic_subordinate1_total_avg_5_1=show_pie_pic_subordinate1_total_avg_5_1 ,
                                    show_pie_pic_subordinate2_total_5_1=show_pie_pic_subordinate2_total_5_1 ,
                                    show_pie_pic_subordinate2_total_avg_5_1=show_pie_pic_subordinate2_total_avg_5_1 ,
                                    show_pie_pic_total_avg_5_1=show_pie_pic_total_avg_5_1 ,

                                    ############
                                    # 高效溝通
                                    ############
                                    show_pie_pic_self_6_1=show_pie_pic_self_6_1 ,
                                    show_pie_pic_manager_6_1=show_pie_pic_manager_6_1 , 
                                    show_pie_pic_peer1_6_1=show_pie_pic_peer1_6_1 , 
                                    show_pie_pic_peer2_6_1=show_pie_pic_peer2_6_1 ,
                                    show_pie_pic_subordinate1_6_1=show_pie_pic_subordinate1_6_1 , 
                                    show_pie_pic_subordinate2_6_1=show_pie_pic_subordinate2_6_1 ,

                                    show_pie_pic_self_6_2=show_pie_pic_self_6_2 , 
                                    show_pie_pic_manager_6_2=show_pie_pic_manager_6_2 , 
                                    show_pie_pic_peer1_6_2=show_pie_pic_peer1_6_2 , 
                                    show_pie_pic_peer2_6_2=show_pie_pic_peer2_6_2 ,
                                    show_pie_pic_subordinate1_6_2=show_pie_pic_subordinate1_6_2 , 
                                    show_pie_pic_subordinate2_6_2=show_pie_pic_subordinate2_6_2 , 

                                    show_pie_pic_self_6_3=show_pie_pic_self_6_3 , 
                                    show_pie_pic_manager_6_3=show_pie_pic_manager_6_3 , 
                                    show_pie_pic_peer1_6_3=show_pie_pic_peer1_6_3 , 
                                    show_pie_pic_peer2_6_3=show_pie_pic_peer2_6_3 ,
                                    show_pie_pic_subordinate1_6_3=show_pie_pic_subordinate1_6_3 , 
                                    show_pie_pic_subordinate2_6_3=show_pie_pic_subordinate2_6_3 ,

                                    show_pie_pic_self_6_4=show_pie_pic_self_6_4 , 
                                    show_pie_pic_manager_6_4=show_pie_pic_manager_6_4 , 
                                    show_pie_pic_peer1_6_4=show_pie_pic_peer1_6_4 , 
                                    show_pie_pic_peer2_6_4=show_pie_pic_peer2_6_4 ,
                                    show_pie_pic_subordinate1_6_4=show_pie_pic_subordinate1_6_4 , 
                                    show_pie_pic_subordinate2_6_4=show_pie_pic_subordinate2_6_4 ,

                                    show_pie_pic_self_6_5=show_pie_pic_self_6_5 , 
                                    show_pie_pic_manager_6_5=show_pie_pic_manager_6_5 , 
                                    show_pie_pic_peer1_6_5=show_pie_pic_peer1_6_5 , 
                                    show_pie_pic_peer2_6_5=show_pie_pic_peer2_6_5 ,
                                    show_pie_pic_subordinate1_6_5=show_pie_pic_subordinate1_6_5 , 
                                    show_pie_pic_subordinate2_6_5=show_pie_pic_subordinate2_6_5 ,

                                    show_pie_pic_self_total_6_1=show_pie_pic_self_total_6_1 ,
                                    show_pie_pic_self_total_avg_6_1=show_pie_pic_self_total_avg_6_1 ,
                                    show_pie_pic_manager_total_6_1=show_pie_pic_manager_total_6_1 ,
                                    show_pie_pic_manager_total_avg_6_1=show_pie_pic_manager_total_avg_6_1 ,
                                    show_pie_pic_peer1_total_6_1=show_pie_pic_peer1_total_6_1 ,
                                    show_pie_pic_peer1_total_avg_6_1=show_pie_pic_peer1_total_avg_6_1 ,
                                    show_pie_pic_peer2_total_6_1=show_pie_pic_peer2_total_6_1 ,
                                    show_pie_pic_peer2_total_avg_6_1=show_pie_pic_peer2_total_avg_6_1 ,
                                    show_pie_pic_subordinate1_total_6_1=show_pie_pic_subordinate1_total_6_1 ,
                                    show_pie_pic_subordinate1_total_avg_6_1=show_pie_pic_subordinate1_total_avg_6_1 ,
                                    show_pie_pic_subordinate2_total_6_1=show_pie_pic_subordinate2_total_6_1 ,
                                    show_pie_pic_subordinate2_total_avg_6_1=show_pie_pic_subordinate2_total_avg_6_1 ,
                                    show_pie_pic_total_avg_6_1=show_pie_pic_total_avg_6_1 ,

                                    #############
                                    # 綜合雷達圖
                                    #############
                                    show_radar_pic=show_radar_pic 
                                    
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#####################################
# /show_hr_360_person_result
#####################################
@app.route("/show_hr_360_person_result", methods=['GET','POST'])
def show_hr_360_person_result():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                s_user = request.form['s_user']
                s_name = request.form['s_name']

                ### operation record title
                operation_record_title = f'載入 HR - 360 考評 , 受評人員 : {s_name} 總分數資料'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_hr_360_person_1_check_data = db.show_hr_360_person_process_total_data(s_user , s_name)
                
                return render_template('ajax/load_hr_360_dep_member_process_list_res2.html' , 
                                    show_hr_360_person_1_check_data=show_hr_360_person_1_check_data
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#####################################
# /show_hr_360_result
#####################################
@app.route("/show_hr_360_result", methods=['GET','POST'])
def show_hr_360_result():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                s_user = request.form['s_user']
                s_name = request.form['s_name']

                ### operation record title
                operation_record_title = f'載入 HR - 360 考評 , 考評人員 : {s_user} , 受評人員 : {s_name} 分數資料'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_hr_360_person_1_check_data = db.show_hr_360_person_process_data(s_user , s_name)
                
                return render_template('ajax/load_hr_360_dep_member_process_list_res.html' , 
                                    show_hr_360_person_1_check_data=show_hr_360_person_1_check_data
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#####################################
# /del_hr_360_manager_process_list
#####################################
@app.route("/del_hr_360_manager_process_list", methods=['GET','POST'])
def del_hr_360_manager_process_list():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                s_user  = request.form['s_user']
                s_name = request.form['s_name']

                ### operation record title
                operation_record_title = f'刪除 HR - 360 考評 , 考評人員 : {s_user} , 受評人員 : {s_name} 已送出資料'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_hr_360_person_1_check_data = db.del_hr_360_person_process_data(s_user , s_name)
                
                return render_template('ajax/load_hr_360_dep_member_process_list.html' , 
                                    show_hr_360_person_1_check_data=show_hr_360_person_1_check_data
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 


##############################
# /del_hr_360_manager_list2
##############################
@app.route("/del_hr_360_manager_list2", methods=['GET','POST'])
def del_hr_360_manager_list2():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                d_dep  = request.form['d_dep']
                d_name = request.form['d_name']

                ### operation record title
                operation_record_title = f'刪除 HR - 360 考評 {d_dep} / {d_name} 資料'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_hr_360_person_1_data = db.del_hr_360_person_data(d_dep , d_name)
                
                return render_template('ajax/load_hr_360_dep_member_list3_2.html' , 
                                    show_hr_360_person_1_data=show_hr_360_person_1_data
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##############################
# /del_hr_360_manager_list
##############################
@app.route("/del_hr_360_manager_list", methods=['GET','POST'])
def del_hr_360_manager_list():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                d_dep  = request.form['d_dep']
                d_name = request.form['d_name']

                ### operation record title
                operation_record_title = f'刪除 HR - 360 考評 {d_dep} / {d_name} 資料'
            
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### 資料
                show_hr_360_person_1_data = db.del_hr_360_person_data(d_dep , d_name)
                
                return render_template('ajax/load_hr_360_dep_member_list3.html' , 
                                    show_hr_360_person_1_data=show_hr_360_person_1_data
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#########################################
# /load_hr_360_manager_process_list2_2
#########################################
@app.route("/load_hr_360_manager_process_list2_2", methods=['GET','POST'])
def load_hr_360_manager_process_list2_2():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '載入 HR - 360 未考評員工人員清單'

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                ### 資料
                show_hr_360_person_1_check_data = db.show_hr_360_person_1_check_data2()
                
                return render_template('ajax/load_hr_360_dep_member_process_list2.html' , 
                                    show_hr_360_person_1_check_data=show_hr_360_person_1_check_data
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

######################################
# /load_hr_360_manager_process_list2
######################################
@app.route("/load_hr_360_manager_process_list2", methods=['GET','POST'])
def load_hr_360_manager_process_list2():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '載入 HR - 360 未考評主管人員清單'

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                ### 資料
                show_hr_360_person_1_check_data = db.show_hr_360_person_1_check_data2()
                
                return render_template('ajax/load_hr_360_dep_member_process_list2.html' , 
                                    show_hr_360_person_1_check_data=show_hr_360_person_1_check_data
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))


#########################################
# /load_hr_360_manager_process_list2_3
#########################################
@app.route("/load_hr_360_manager_process_list2_3", methods=['GET','POST'])
def load_hr_360_manager_process_list2_3():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '載入 HR - 360 考評員工進度清單'

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                ### 資料
                show_hr_360_person_1_check_data = db.show_hr_360_person_1_check_data2_3()
                
                return render_template('ajax/load_hr_360_dep_member_process_list.html' , 
                                    show_hr_360_person_1_check_data=show_hr_360_person_1_check_data
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

######################################
# /load_hr_360_manager_process_list
######################################
@app.route("/load_hr_360_manager_process_list", methods=['GET','POST'])
def load_hr_360_manager_process_list():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '載入 HR - 360 考評主管進度清單'

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                ### 資料
                show_hr_360_person_1_check_data = db.show_hr_360_person_1_check_data()
                
                return render_template('ajax/load_hr_360_dep_member_process_list.html' , 
                                    show_hr_360_person_1_check_data=show_hr_360_person_1_check_data
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

##############################
# /load_hr_360_manager_list2
##############################
@app.route("/load_hr_360_manager_list2", methods=['GET','POST'])
def load_hr_360_manager_list2():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '載入 HR - 360 考評員工清單'

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                ### 資料
                show_hr_360_person_1_data = db.show_hr_360_person_1_data_2()
                
                return render_template('ajax/load_hr_360_dep_member_list3_2.html' , 
                                    show_hr_360_person_1_data=show_hr_360_person_1_data
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

##############################
# /load_hr_360_manager_list
##############################
@app.route("/load_hr_360_manager_list", methods=['GET','POST'])
def load_hr_360_manager_list():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '載入 HR - 360 考評主管清單'

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                ### 資料
                show_hr_360_person_1_data = db.show_hr_360_person_1_data()
                
                return render_template('ajax/load_hr_360_dep_member_list3.html' , 
                                    show_hr_360_person_1_data=show_hr_360_person_1_data
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

####################################
# /update_erp_bom_data
####################################
@app.route("/update_erp_bom_data", methods=['GET', 'POST'])
def update_erp_bom_data():
    
    if 'user' in session:
        
        ### session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']
        dep_id = session['department_id']

        r_date = time.strftime("%Y-%m-%d", time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        r_year = time.strftime("%Y", time.localtime())
        r_month = time.strftime("%m", time.localtime())

        if request.method == 'POST':
            
            m_no = request.form.get('m_no')
            m_license = request.form.get('m_license')
            e_no = request.form.get('e_no')
            p_amount = request.form.get('p_amount')

            m_no = m_no.strip()
            m_license = m_license.strip()
            e_no = e_no.strip()
            p_amount = p_amount.strip()
            
            operation_record_title = f'更新 ERP BOM , 主件品號 : {m_no} , 序號 {m_license} , 元件品號 {e_no} , 組成用量 {p_amount} 資料'
            db.operation_record(r_time, user, login_code, operation_record_title)
            
            update_status = db.update_erp_bom(m_no, m_license, e_no, p_amount)
            
            if update_status == 'ok':  
                f_bom_query_1 = db.factory_erp_bom_query1(m_no)
                f_bom_query_2 = db.factory_erp_bom_query2(m_no)
                
                return render_template('ajax/load_factory_erp_bom_list.html', 
                                       user=user, lv=lv, operation_record_title=operation_record_title, 
                                       r_date=r_date, dep_id=dep_id, f_bom_query_1=f_bom_query_1, 
                                       f_bom_query_2=f_bom_query_2
                                      )
            else:
                return "Failed to update BOM data", 500  

        return redirect(url_for('logout'))

    return redirect(url_for('login'))

####################################
# /reload_hr_360_person_member_list
####################################
@app.route("/reload_hr_360_person_member_list", methods=['GET','POST'])
def reload_hr_360_person_member_list():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '重新載入 HR - 360 考評人員員工清單'

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### 資料
            hr_360_manager_question1 = db.hr_360_member_question(c_name , 'self')
            
            
            
            return render_template('ajax/reload_hr_360_person_list.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name ,
                                   hr_360_manager_question1 = hr_360_manager_question1 
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

####################################
# /reload_hr_360_person_list
####################################
@app.route("/reload_hr_360_person_list", methods=['GET','POST'])
def reload_hr_360_person_list():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '重新載入 HR - 360 考評人員主管清單'

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### 資料
            hr_360_manager_question1 = db.hr_360_manager_question(c_name , 'self')
            
            
            
            return render_template('ajax/reload_hr_360_person_list.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name ,
                                   hr_360_manager_question1 = hr_360_manager_question1 
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

#############################
# /hr_360_manager_question2
#############################
@app.route("/hr_360_manager_question2")
def hr_360_manager_question2():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'HR - 360 考評員工題目'

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### 資料
            hr_360_manager_question1 = db.hr_360_member_question(c_name , 'self')
            
            return render_template('hr_360_manager_question2.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name ,
                                   hr_360_manager_question1 = hr_360_manager_question1
                                   
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

#############################
# /hr_360_manager_question
#############################
@app.route("/hr_360_manager_question")
def hr_360_manager_question():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'HR - 360 考評主管題目'

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### 資料
            hr_360_manager_question1 = db.hr_360_manager_question(c_name , 'self')
            
            return render_template('hr_360_manager_question.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name ,
                                   hr_360_manager_question1 = hr_360_manager_question1
                                   
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

##########################
# /hr_360_content_setup
##########################
@app.route("/hr_360_content_setup")
def hr_360_content_setup():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'HR - 360 考評項目設定'

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### 資料
            hr_360_dep = db.HR_360_department()
            show_hr_360_person_1_data = db.show_hr_360_person_1_data()
            show_HR_360_employee = db.HR_360_employee()
            
            
            return render_template('hr_360_content_setup.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name ,
                                   hr_360_dep=hr_360_dep , show_hr_360_person_1_data=show_hr_360_person_1_data , 
                                   show_HR_360_employee=show_HR_360_employee
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

######################################################
# /hr_360_manager_process_list
######################################################
@app.route("/hr_360_manager_process_list")
def hr_360_manager_process_list():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'HR - 360 考評主管進度'

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### 資料
            hr_360_dep                      = db.HR_360_department()
            show_hr_360_person_1_data       = db.show_hr_360_person_1_data()
            show_hr_360_person_1_check_data = db.show_hr_360_person_1_check_data()
            show_HR_360_employee            = db.HR_360_employee()
            
            
            return render_template('hr_360_process_list.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name ,
                                   hr_360_dep=hr_360_dep , show_hr_360_person_1_data=show_hr_360_person_1_data , 
                                   show_HR_360_employee=show_HR_360_employee , show_hr_360_person_1_check_data=show_hr_360_person_1_check_data
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##########################
# /hr_360_manager_setup
##########################
@app.route("/hr_360_manager_setup")
def hr_360_manager_setup():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'HR - 360 考評人員設定'

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### 資料
            hr_360_dep                = db.HR_360_department()
            show_hr_360_person_1_data = db.show_hr_360_person_1_data()
            show_HR_360_employee      = db.HR_360_employee()
            
            
            return render_template('hr_360_setup.html' , 
                                   user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name ,
                                   hr_360_dep=hr_360_dep , show_hr_360_person_1_data=show_hr_360_person_1_data , 
                                   show_HR_360_employee=show_HR_360_employee
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 



##########################
# /bpm_expenditure_form
##########################
@app.route("/bpm_expenditure_form")
def bpm_expenditure_form():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'BPM 開支證明單'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### BPM 開支證明單
            bpm_information_form_list_account = db.bpm_information_form_record_list_account(dep_name , c_name) # 本帳號
            bpm_expenditure_form_list_done    = db.bpm_expenditure_form_record_list(dep_name , 'true') # 已結案
            bpm_expenditure_form_list_running = db.bpm_expenditure_form_record_list(dep_name , 'false') # 未結案

            ### BPM 開支證明單圖表
            bpm_expenditure_chart             = 'BPM 開支證明單統計圖表'
            bpm_expenditure_by_dep_kind_img1  = db.show_bpm_expenditure_by_dep_kind_img(dep_name)
            
            ### BPM 開支證明單圖表
            bpm_statistics_list            = db.show_bpm_expenditure_by_dep_kind_statistics_list(dep_name)
            #bpm_statistics_by_account_list = db.show_bpm_expenditure_by_dep_kind_statistics_by_account_list(dep_name , c_name)

            ### BPM 開支證明單各部門統計圖表
            show_bpm_expenditure_each_dep_img  = db.show_bpm_expenditure_each_dep_img()
            show_bpm_expenditure_each_dep_list = db.show_bpm_expenditure_each_dep_list()
            show_bpm_expenditure_deplist       = db.show_bpm_expenditure_each_dep_list()
            
            
            return render_template('bpm_expenditure_form.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name , bpm_expenditure_form_list_done=bpm_expenditure_form_list_done ,
                                   bpm_expenditure_form_list_running=bpm_expenditure_form_list_running , 
                                   bpm_expenditure_chart=bpm_expenditure_chart ,
                                   bpm_expenditure_by_dep_kind_img1=bpm_expenditure_by_dep_kind_img1 ,
                                   show_bpm_expenditure_each_dep_img=show_bpm_expenditure_each_dep_img ,
                                   show_bpm_expenditure_each_dep_list=show_bpm_expenditure_each_dep_list ,
                                   bpm_statistics_list=bpm_statistics_list , show_bpm_expenditure_deplist=show_bpm_expenditure_deplist , 
                                   
                                   bpm_information_form_list_account=bpm_information_form_list_account
                                   #bpm_statistics_by_account_list=bpm_statistics_by_account_list 
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))  

##########################
# /bpm_information_form
##########################
@app.route("/bpm_information_form")
def bpm_information_form():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'BPM 資訊需求單'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### department name & updepartment name
            dep_name     = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id     = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name   = db.bpm_account_up_department(updep_id)
            c_name       = db.bpm_account_data(user,'EmployeeName')

            ### BPM 資訊需求單
            bpm_information_form_list_account = db.bpm_information_form_record_list_account(dep_name , c_name) # 本帳號
            bpm_information_form_list_done    = db.bpm_information_form_record_list(dep_name , 'true') # 已結案
            bpm_information_form_list_running = db.bpm_information_form_record_list(dep_name , 'false') # 未結案

            ### BPM 資訊需求單圖表
            bpm_information_chart           = 'BPM 資訊需求單統計圖表'
            bpm_information_by_dep_kind_list1 = db.show_bpm_information_by_dep_kind_list(dep_name , '硬體,')
            bpm_information_by_dep_kind_sum1  = db.show_bpm_information_by_dep_kind_sum(dep_name , '硬體,')
            bpm_information_by_dep_kind_img1  = db.show_bpm_information_by_dep_kind_img(dep_name , '硬體,')
            
            bpm_information_by_dep_kind_by_account_list1 = db.show_bpm_information_by_dep_kind_by_account_list(dep_name , '硬體,' , c_name)
            bpm_information_by_dep_kind_by_account_sum1  = db.show_bpm_information_by_dep_kind_by_account_sum(dep_name , '硬體,' , c_name)
            bpm_information_by_dep_kind_by_account_img1  = db.show_bpm_information_by_dep_kind_by_account_img(dep_name , '硬體,' , c_name)
            
            bpm_information_by_dep_kind_list2 = db.show_bpm_information_by_dep_kind_list(dep_name , '軟體,')
            bpm_information_by_dep_kind_sum2  = db.show_bpm_information_by_dep_kind_sum(dep_name , '軟體,')
            bpm_information_by_dep_kind_img2  = db.show_bpm_information_by_dep_kind_img(dep_name , '軟體,')

            bpm_information_by_dep_kind_by_account_list2 = db.show_bpm_information_by_dep_kind_by_account_list(dep_name , '軟體,' , c_name)
            bpm_information_by_dep_kind_by_account_sum2  = db.show_bpm_information_by_dep_kind_by_account_sum(dep_name , '軟體,' , c_name)
            bpm_information_by_dep_kind_by_account_img2  = db.show_bpm_information_by_dep_kind_by_account_img(dep_name , '軟體,' , c_name)

            ### BPM 資訊需求單本帳號圖表
            bpm_statistics_list            = db.show_bpm_information_by_dep_kind_statistics_list(dep_name)
            bpm_statistics_by_account_list = db.show_bpm_information_by_dep_kind_statistics_by_account_list(dep_name , c_name)

            ### BPM 各部門統計圖表
            show_bpm_information_each_dep_img  = db.show_bpm_information_each_dep_img()
            
            
            return render_template('bpm_information_form.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name , bpm_information_form_list_done=bpm_information_form_list_done ,
                                   bpm_information_form_list_running=bpm_information_form_list_running , bpm_information_form_list_account=bpm_information_form_list_account ,
                                   bpm_information_chart=bpm_information_chart , bpm_information_by_dep_kind_img1=bpm_information_by_dep_kind_img1,
                                   bpm_information_by_dep_kind_img2=bpm_information_by_dep_kind_img2 , bpm_information_by_dep_kind_list1=bpm_information_by_dep_kind_list1,
                                   bpm_information_by_dep_kind_list2=bpm_information_by_dep_kind_list2 , bpm_information_by_dep_kind_sum1=bpm_information_by_dep_kind_sum1 ,
                                   bpm_information_by_dep_kind_sum2=bpm_information_by_dep_kind_sum2 , bpm_statistics_list=bpm_statistics_list ,
                                   bpm_statistics_by_account_list=bpm_statistics_by_account_list , bpm_information_by_dep_kind_by_account_list1=bpm_information_by_dep_kind_by_account_list1 ,
                                   bpm_information_by_dep_kind_by_account_sum1=bpm_information_by_dep_kind_by_account_sum1 , bpm_information_by_dep_kind_by_account_img1=bpm_information_by_dep_kind_by_account_img1 ,
                                   bpm_information_by_dep_kind_by_account_list2=bpm_information_by_dep_kind_by_account_list2 , bpm_information_by_dep_kind_by_account_sum2=bpm_information_by_dep_kind_by_account_sum2 ,
                                   bpm_information_by_dep_kind_by_account_img2=bpm_information_by_dep_kind_by_account_img2 , 
                                   show_bpm_information_each_dep_img=show_bpm_information_each_dep_img
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))  

##########################
# /ss2_order_form
##########################
@app.route("/ss2_order_form")
def ss2_order_form():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'SS2 注文單'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### SS2 注文單清單
            ss2_order_form_list = db.ss2_order_form_record_list()

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
            
            
            return render_template('ss2_order_form.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name , ss2_order_form_list=ss2_order_form_list)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))    

##########################
# /otsuka_query_device
##########################
@app.route("/otsuka_query_device")
def otsuka_query_device():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '固資查詢'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### 固資清單
            #device_list = db.erp_query_device()

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
            
            
            return render_template('query_device.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , r_date=r_date , dep_id=dep_name ,
                                    updep_name=updep_name)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))    

##########################
# /otsuka_account
##########################
@app.route("/otsuka_account")
def otsuka_account():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '帳號查詢'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            
            ### 帳號清單
            account_list        = db.bpm_account_list()
            account_list_by_dep = db.bpm_account_list_by_dep()

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
            
            return render_template('account_list.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , r_date=r_date , dep_id=dep_name ,
                                    updep_name=updep_name , account_list=account_list , account_list_by_dep=account_list_by_dep)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))    


#######################################
# /alter_work_record_by_title
#######################################
@app.route("/alter_work_record_by_title", methods=['GET','POST']) 
def alter_work_record_by_title():
    
    if 'user' in session:
        
        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                title  = request.form['title']
                dep_id = request.form['dep_id']
                
                ### operation record title
                operation_record_title = f'修改工作進度表 - {title}'    
                
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                ### 載入工作紀錄清單
                res_list = db.alter_work_record_list_detail(title , dep_id)

                ### department name & updepartment name
                dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
                updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
                updep_name         = db.bpm_account_up_department(updep_id)
                
                return render_template('ajax/alter_new_work_record_form.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                        r_date=r_date , dep_id=dep_name , updep_name=updep_name , res_list=res_list
                                        )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))  

#######################################
# /del_work_record_title
#######################################
@app.route("/del_work_record_title", methods=['GET','POST']) 
def del_work_record_title():
    
    if 'user' in session:
        
        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                title = request.form['title']
                
                ### operation record title
                operation_record_title = f'刪除工作進度表 - {title}'    
                
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                ### 刪除工作紀錄
                db.del_work_record_list_detail(title)

                ### 載入工作紀錄清單
                res_list = db.load_work_record_list(dep_id)

                ### department name & updepartment name
                dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
                updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
                updep_name         = db.bpm_account_up_department(updep_id)
                
                return render_template('ajax/work_record_form_list.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                        r_date=r_date , dep_id=dep_name , updep_name=updep_name , res_list=res_list
                                        )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))  


#######################################
# /load_work_record_form_list_detail
#######################################
@app.route("/load_work_record_form_list_detail", methods=['GET','POST']) 
def load_work_record_form_list_detail():
    
    if 'user' in session:
        
        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                title  = request.form['title']
                dep_id = request.form['dep_id']
                
                ### operation record title
                operation_record_title = f'載入工作進度表 - {title}'    
                
                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                res_list = db.load_work_record_list_detail(title , dep_id)

                ### department name & updepartment name
                dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
                updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
                updep_name         = db.bpm_account_up_department(updep_id)
                
                return render_template('ajax/work_record_form_list_detail.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                    r_date=r_date , dep_id=dep_name , updep_name=updep_name , res_list=res_list , w_dep_id=dep_id
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))  

################################
# /load_work_record_form_list
################################
@app.route("/load_work_record_form_list", methods=['GET','POST']) 
def load_work_record_form_list():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '載入工作進度表清單'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                dep_id = request.form['dep_id']

                res_list = db.load_work_record_list(dep_id)

                ### department name & updepartment name
                dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
                updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
                updep_name         = db.bpm_account_up_department(updep_id)
                
                return render_template('ajax/work_record_form_list.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                    r_date=r_date , dep_id=dep_name , updep_name=updep_name , res_list=res_list
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))  

#############################
# /search_work_record_list
#############################
@app.route("/search_work_record_list", methods=['GET','POST']) 
def search_work_record_list():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '搜尋工作進度表'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                s_s_date  = request.form['s_s_date']
                s_e_date  = request.form['s_e_date']
                s_w_kind  = request.form['s_w_kind']

                ### department name & updepartment name
                dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
                updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
                updep_name         = db.bpm_account_up_department(updep_id)

                w_r_l_res = db.search_work_record(s_s_date , s_e_date , s_w_kind , dep_name)
                
                return render_template('ajax/search_work_record_form_list.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                        r_date=r_date , dep_id=dep_name , updep_name=updep_name , w_r_l_res=w_r_l_res
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))  

##########################
# /load_work_record_form
##########################
@app.route("/load_work_record_form", methods=['GET','POST']) 
def load_work_record_form():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '新增工作進度表'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                ### 日當月報表
                day_money_by_year  = r_year
                day_money_by_month = db.bpm_day_money_by_month(r_year)

                ### department name & updepartment name
                dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
                updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
                updep_name         = db.bpm_account_up_department(updep_id)
                
                return render_template('ajax/add_new_work_record_form.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                    r_date=r_date , dep_id=dep_name , updep_name=updep_name , day_money_by_year=day_money_by_year , 
                                    day_money_by_month=day_money_by_month 
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))  

###################################
# /bpm_information_account_detail
###################################
@app.route("/bpm_information_account_detail" , methods=['GET','POST'])
def bpm_information_account_detail():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            if request.method == 'POST':
                
                dep  = request.form['dep']
                kind = request.form['kind']
                user = request.form['user']

                ### operation record title
                operation_record_title = 'BPM 電子清單 - ' + dep  + ' , ' + kind + ' , ' + user + ' 資料統計圖'    

                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    
                
                #################
                # main content 
                #################
                c_name                                      = db.bpm_account_search('EmployeeName',user)
                bpm_information_by_dep_kind_user            = db.bpm_information_finish_by_dep_kind_user(dep , kind , c_name)
                bpm_information_by_dep_kind_total_cost_user = db.bpm_information_finish_by_dep_kind_total_cost_user(dep , kind , c_name)
                bpm_information_by_dep_kind_user_img        = db.show_bpm_information_by_dep_kind_detail_by_account_img(dep , kind , c_name)

                
                return render_template('ajax/load_bpm_information_record_user.html' , user=user ,dep=dep , kind=kind ,
                                       bpm_information_by_dep_kind_user=bpm_information_by_dep_kind_user , 
                                       bpm_information_by_dep_kind_total_cost_user=bpm_information_by_dep_kind_total_cost_user , 
                                       bpm_information_by_dep_kind_user_img=bpm_information_by_dep_kind_user_img
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###################################
# /bpm_expenditure_detail
###################################
@app.route("/bpm_expenditure_detail" , methods=['GET','POST'])
def bpm_expenditure_detail():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            if request.method == 'POST':
                
                dep  = request.form['dep']
                kind = request.form['kind']

                ### operation record title
                operation_record_title = 'BPM 電子清單 - ' + dep  + ' , ' + kind + ' 資料統計圖'    

                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    
                
                #################
                # main content 
                #################
                bpm_expenditure_by_dep_kind            = db.bpm_expenditure_finish_by_dep_kind(dep , kind)
                bpm_information_by_dep_kind_total_cost = db.bpm_information_finish_by_dep_kind_total_cost(dep , kind)
                bpm_information_by_dep_kind_img   = db.show_bpm_information_by_dep_kind_detail_img(dep , kind)
                
                return render_template('ajax/load_bpm_expenditure_record.html' , user=user ,dep=dep , kind=kind ,
                                       bpm_expenditure_by_dep_kind=bpm_expenditure_by_dep_kind , 
                                       bpm_information_by_dep_kind_total_cost=bpm_information_by_dep_kind_total_cost ,
                                       bpm_information_by_dep_kind_img=bpm_information_by_dep_kind_img
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###################################
# /bpm_information_detail
###################################
@app.route("/bpm_information_detail" , methods=['GET','POST'])
def bpm_information_detail():
    
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            if request.method == 'POST':
                
                dep  = request.form['dep']
                kind = request.form['kind']

                ### operation record title
                operation_record_title = 'BPM 電子清單 - ' + dep  + ' , ' + kind + ' 資料統計圖'    

                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    
                
                #################
                # main content 
                #################
                bpm_information_by_dep_kind            = db.bpm_information_finish_by_dep_kind(dep , kind)
                bpm_information_by_dep_kind_total_cost = db.bpm_information_finish_by_dep_kind_total_cost(dep , kind)
                bpm_information_by_dep_kind_img   = db.show_bpm_information_by_dep_kind_detail_img(dep , kind)
                
                return render_template('ajax/load_bpm_information_record.html' , user=user ,dep=dep , kind=kind ,
                                       bpm_information_by_dep_kind=bpm_information_by_dep_kind , 
                                       bpm_information_by_dep_kind_total_cost=bpm_information_by_dep_kind_total_cost ,
                                       bpm_information_by_dep_kind_img=bpm_information_by_dep_kind_img
                                    )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###################################
# /final_update_work_record_list
###################################
@app.route("/final_update_work_record_list" , methods=['GET','POST'])
def final_update_work_record_list():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '最後更新工作進度表清單'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            
            ### 工作進度清單
            res_list = db.work_record_list(dep_id)
            
            ### 工作進度清單 - 最新更新五筆
            final_res_list = db.work_record_final_list(dep_id , user)
            ### 工作進度清單 - 部門最新更新五筆
            final_res_list_by_dep = db.work_record_final_list_by_dep(dep_id)
            
            return render_template('ajax/reload_work_record_final_update.html' , user=user , final_res_list=final_res_list ,
                                   final_res_list_by_dep=final_res_list_by_dep
                                   
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##########################
# /work_record_form
##########################
@app.route("/work_record_form")
def work_record_form():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '工作進度表'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### 日當月報表
            day_money_by_year  = r_year
            day_money_by_month = db.bpm_day_money_by_month(r_year)

            ### 合約清單
            contract_list_by_date = db.otsuka_contract_by_date()
            contract_list_by_kind = db.otsuka_contract_by_kind()
            contract_list_summary = db.otsuka_contract_summary()

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
            
            ### 工作進度清單
            res_list = db.work_record_list(dep_id)
            
            ### 工作進度清單 - 帳號最新更新五筆
            final_res_list = db.work_record_final_list(dep_id , user)

            ### 工作進度清單 - 部門最新更新五筆
            final_res_list_by_dep = db.work_record_final_list_by_dep(dep_id)
            
            return render_template('work_record_form.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , 
                                   r_date=r_date , dep_id=dep_name , updep_name=updep_name , day_money_by_year=day_money_by_year , 
                                   day_money_by_month=day_money_by_month , contract_list_by_date=contract_list_by_date , 
                                   contract_list_by_kind=contract_list_by_kind , contract_list_summary=contract_list_summary , res_list=res_list ,
                                   final_res_list=final_res_list , final_res_list_by_dep=final_res_list_by_dep
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))    


##########################
# /otsuka_contract
##########################
@app.route("/otsuka_contract")
def otsuka_contract():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '合約查詢'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### 日當月報表
            day_money_by_year  = r_year
            day_money_by_month = db.bpm_day_money_by_month(r_year)

            ### 合約清單
            contract_list_by_date = db.otsuka_contract_by_date()
            contract_list_by_kind = db.otsuka_contract_by_kind()
            contract_list_summary = db.otsuka_contract_summary()

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
            
            return render_template('it_contract.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , r_date=r_date , dep_id=dep_name , updep_name=updep_name , day_money_by_year=day_money_by_year , day_money_by_month=day_money_by_month , contract_list_by_date=contract_list_by_date , contract_list_by_kind=contract_list_by_kind , contract_list_summary=contract_list_summary)
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))    

##########################
# /department_no_search
##########################
@app.route("/department_no_search")
def department_no_search():
    
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '部門代號查詢'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### 部門清單
            department_list = db.department_account_list()

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)
            
            return render_template('search_department_id.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , r_date=r_date , 
                                   dep_id=dep_name , updep_name=updep_name , department_list=department_list
                                   )
        
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##################################
# /submit_add_check_member_data
##################################
@app.route("/submit_add_check_member_data" , methods=['GET','POST'])
def submit_add_check_member_data():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '生產二部 - 新增人員考評表資料'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                employee_id     = request.form['employee_id']
                employee_name   = request.form['employee_name']
                department_id   = request.form['department_id']
                department_name = request.form['department_name']
                job_title       = request.form['job_title']
                b_date          = request.form['b_date']
                end_date        = request.form['end_date']
                check_year      = request.form['check_year']
                check_month     = request.form['check_month']
                self_num1_1     = request.form['self_num1_1']
                self_num1_2     = request.form['self_num1_2']
                self_num1_3     = request.form['self_num1_3']
                self_num1_4     = request.form['self_num1_4']
                self_num2_1     = request.form['self_num2_1']
                self_num2_2     = request.form['self_num2_2']
                self_num2_3     = request.form['self_num2_3']
                self_num3_1     = request.form['self_num3_1']
                self_num3_2     = request.form['self_num3_2']
                self_num3_3     = request.form['self_num3_3']
                self_num4_1     = request.form['self_num4_1']
                self_num4_2     = request.form['self_num4_2']
                self_num4_3     = request.form['self_num4_3']
                self_num4_4     = request.form['self_num4_4']
                self_num5_1     = request.form['self_num5_1']
                self_num5_2     = request.form['self_num5_2']
                self_num5_3     = request.form['self_num5_3']
                self_num6_1     = request.form['self_num6_1']
                self_num6_2     = request.form['self_num6_2']
                self_num6_3     = request.form['self_num6_3']
                self_total      = request.form['self_total']

                session['employee_id']   = request.form['employee_id']
                session['end_date']      = request.form['end_date']

                db.submit_add_check_member_data(employee_id , employee_name , department_id , department_name , job_title , b_date , end_date , check_year , check_month , self_num1_1 , self_num1_2 , self_num1_3 , self_num1_4 , self_num2_1 , self_num2_2 , self_num2_3 , self_num3_1 , self_num3_2 , self_num3_3 , self_num4_1 , self_num4_2 , self_num4_3 , self_num4_4 , self_num5_1 , self_num5_2 , self_num5_3 , self_num6_1 , self_num6_2 , self_num6_3  , self_total)
            
                #################
                # main content 
                #################
                factory_work_station = db.factory_work_station()
                a_work_no            = session['employee_id']
                a_name               = session['user']
                a_end_date           = db.search_item('end_date' , session['user']) 
                a_check_year         = db.search_member_item('check_year' , user)
                a_check_month        = db.search_member_item('check_month' , user)
                a_job_title          = db.factory_check_form_item(user)
                a_member_check_list  = db.factory_check_form_list()
                res_check_list       = db.check_add_check_member_list(user)

                return render_template('production_2_work_check_record.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , a_end_date=a_end_date , dep_id=dep_id , check_year=r_year , check_month=r_month , a_job_title=a_job_title , a_member_check_list=a_member_check_list , res_check_list=res_check_list)
                
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##############################
# /submit_add_check_account
##############################
@app.route("/submit_add_check_account" , methods=['GET','POST'])
def submit_add_check_account():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '生產二部 - 新增人員考評帳號表資料'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                employee_id     = request.form['employee_id']
                employee_name   = request.form['employee_name']
                login_id        = request.form['login_id']
                mobile          = request.form['mobile']
                department_name = request.form['department_name']
                department_code = request.form['department_code']
                company_id      = request.form['company_id']
                end_date        = request.form['end_date']

                res = db.submit_add_check_account(employee_id , employee_name , login_id , mobile , department_name , department_code , company_id , end_date)
                
                if res == 'ok':
                    success_msg = '新增帳密完成.'
                    return render_template('ajax/add_check_member_account.html' , user=user , lv=lv , title=title , r_date=r_date , success_msg=success_msg)
                
                elif res == 'no':
                    error_msg = '姓名已被使用 , 重新輸入 !!!'
                    return render_template('ajax/add_check_member_account.html' , user=user , lv=lv , title=title , r_date=r_date , error_msg=error_msg , employee_id=employee_id , employee_name=employee_name , login_id=login_id , mobile=mobile , end_date=end_date)
                
                elif res == 'no_login_id':
                    error_msg = '帳號已被使用 , 重新輸入 !!!'
                    return render_template('ajax/add_check_member_account.html' , user=user , lv=lv , title=title , r_date=r_date , error_msg=error_msg , employee_id=employee_id , employee_name=employee_name , login_id=login_id , mobile=mobile , end_date=end_date)
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##############################
# /add_check_member_account
##############################
@app.route("/add_check_member_account" , methods=['GET','POST'])
def add_check_member_account():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '生產二部 - 載入新增人員考評帳號表'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            return render_template('ajax/add_check_member_account.html' , user=user , lv=lv , title=title , r_date=r_date)
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#################################
# /load_check_member_self_list
#################################
@app.route("/load_check_member_self_list" , methods=['GET','POST'])
def load_check_member_self_list():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '生產二部 - 載入人員考評表資料'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
            
                employee_id     = request.form['employee_id']
                employee_name   = request.form['employee_name']
                check_year      = request.form['check_year']
                check_month     = request.form['check_month']
                a_job_title     = db.factory_check_form_item(user)

                res = db.load_account_data_form_self_item(employee_id , employee_name , check_year , check_month)

                return render_template('ajax/load_account_data_list.html' , user=user , lv=lv , title=title , r_date=r_date , res=res , a_job_title=a_job_title)
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

######################
# /submit_work_time
######################
@app.route("/submit_work_time" , methods=['GET','POST'])
def submit_work_time():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '新增液劑工時紀錄單資料'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                a_work_no           = request.form['a_work_no']
                a_name              = request.form['a_name']
                dep_id              = request.form['dep_id']
                b_date              = request.form['b_date']
                total_time          = request.form['total_time']
                normal_time         = request.form['normal_time']
                over_time           = request.form['over_time']
                availability_time   = request.form['availability_time']
                
                a_work_station_1            = request.form['a_work_station_1'] 
                a_production_1              = request.form['a_production_1']
                a_product_no_1              = request.form['a_product_no_1']
                a_work_normal_time_1        = request.form['a_work_normal_time_1']
                a_work_over_time_1          = request.form['a_work_over_time_1']
                a_work_availability_time_1  = request.form['a_work_availability_time_1'] 
                a_work_remark_1             = request.form['a_work_remark_1']

                a_work_station_2            = request.form['a_work_station_2'] 
                a_production_2              = request.form['a_production_2']
                a_product_no_2              = request.form['a_product_no_2']
                a_work_normal_time_2        = request.form['a_work_normal_time_2']
                a_work_over_time_2          = request.form['a_work_over_time_2']
                a_work_availability_time_2  = request.form['a_work_availability_time_2'] 
                a_work_remark_2             = request.form['a_work_remark_2']

                a_work_station_3            = request.form['a_work_station_3'] 
                a_production_3              = request.form['a_production_3']
                a_product_no_3              = request.form['a_product_no_3']
                a_work_normal_time_3        = request.form['a_work_normal_time_3']
                a_work_over_time_3          = request.form['a_work_over_time_3']
                a_work_availability_time_3  = request.form['a_work_availability_time_3'] 
                a_work_remark_3             = request.form['a_work_remark_3']

                a_work_station_4            = request.form['a_work_station_4'] 
                a_production_4              = request.form['a_production_4']
                a_product_no_4              = request.form['a_product_no_4']
                a_work_normal_time_4        = request.form['a_work_normal_time_4']
                a_work_over_time_4          = request.form['a_work_over_time_4']
                a_work_availability_time_4  = request.form['a_work_availability_time_4'] 
                a_work_remark_4             = request.form['a_work_remark_4']

                a_work_station_5            = request.form['a_work_station_5'] 
                a_production_5              = request.form['a_production_5']
                a_product_no_5              = request.form['a_product_no_5']
                a_work_normal_time_5        = request.form['a_work_normal_time_5']
                a_work_over_time_5          = request.form['a_work_over_time_5']
                a_work_availability_time_5  = request.form['a_work_availability_time_5'] 
                a_work_remark_5             = request.form['a_work_remark_5']

                a_work_station_6            = request.form['a_work_station_6'] 
                a_production_6              = request.form['a_production_6']
                a_product_no_6              = request.form['a_product_no_6']
                a_work_normal_time_6        = request.form['a_work_normal_time_6']
                a_work_over_time_6          = request.form['a_work_over_time_6']
                a_work_availability_time_6  = request.form['a_work_availability_time_6'] 
                a_work_remark_6             = request.form['a_work_remark_6']

                a_work_station_7            = request.form['a_work_station_7'] 
                a_production_7              = request.form['a_production_7']
                a_product_no_7              = request.form['a_product_no_7']
                a_work_normal_time_7        = request.form['a_work_normal_time_7']
                a_work_over_time_7          = request.form['a_work_over_time_7']
                a_work_availability_time_7  = request.form['a_work_availability_time_7'] 
                a_work_remark_7             = request.form['a_work_remark_7']

                a_work_station_8            = request.form['a_work_station_8'] 
                a_production_8              = request.form['a_production_8']
                a_product_no_8              = request.form['a_product_no_8']
                a_work_normal_time_8        = request.form['a_work_normal_time_8']
                a_work_over_time_8          = request.form['a_work_over_time_8']
                a_work_availability_time_8  = request.form['a_work_availability_time_8'] 
                a_work_remark_8             = request.form['a_work_remark_8']

                a_work_station_9            = request.form['a_work_station_9'] 
                a_production_9              = request.form['a_production_9']
                a_product_no_9              = request.form['a_product_no_9']
                a_work_normal_time_9        = request.form['a_work_normal_time_9']
                a_work_over_time_9          = request.form['a_work_over_time_9']
                a_work_availability_time_9  = request.form['a_work_availability_time_9'] 
                a_work_remark_9             = request.form['a_work_remark_9']

                a_work_station_10            = request.form['a_work_station_10'] 
                a_production_10              = request.form['a_production_10']
                a_product_no_10              = request.form['a_product_no_10']
                a_work_normal_time_10        = request.form['a_work_normal_time_10']
                a_work_over_time_10          = request.form['a_work_over_time_10']
                a_work_availability_time_10  = request.form['a_work_availability_time_10'] 
                a_work_remark_10             = request.form['a_work_remark_10']

                a_work_station_11            = request.form['a_work_station_11'] 
                a_production_11              = request.form['a_production_11']
                a_product_no_11              = request.form['a_product_no_11']
                a_work_normal_time_11        = request.form['a_work_normal_time_11']
                a_work_over_time_11          = request.form['a_work_over_time_11']
                a_work_availability_time_11  = request.form['a_work_availability_time_11'] 
                a_work_remark_11             = request.form['a_work_remark_11']

                a_work_station_12            = request.form['a_work_station_12'] 
                a_production_12              = request.form['a_production_12']
                a_product_no_12              = request.form['a_product_no_12']
                a_work_normal_time_12        = request.form['a_work_normal_time_12']
                a_work_over_time_12          = request.form['a_work_over_time_12']
                a_work_availability_time_12  = request.form['a_work_availability_time_12'] 
                a_work_remark_12             = request.form['a_work_remark_12']
                
                res = db.submit_work_time_form(a_work_no , a_name , dep_id , b_date , total_time , normal_time , over_time , availability_time , a_work_station_1 , a_production_1 , a_product_no_1 , a_work_normal_time_1 , a_work_over_time_1 , a_work_availability_time_1 , a_work_remark_1 , a_work_station_2 , a_production_2 , a_product_no_2 , a_work_normal_time_2 , a_work_over_time_2 , a_work_availability_time_2 , a_work_remark_2 , a_work_station_3 , a_production_3 , a_product_no_3 , a_work_normal_time_3 , a_work_over_time_3 , a_work_availability_time_3 , a_work_remark_3 , a_work_station_4 , a_production_4 , a_product_no_4 , a_work_normal_time_4 , a_work_over_time_4 , a_work_availability_time_4 , a_work_remark_4 , a_work_station_5 , a_production_5 , a_product_no_5 , a_work_normal_time_5 , a_work_over_time_5 , a_work_availability_time_5 , a_work_remark_5 , a_work_station_6 , a_production_6 , a_product_no_6 , a_work_normal_time_6 , a_work_over_time_6 , a_work_availability_time_6 , a_work_remark_6 , a_work_station_7 , a_production_7 , a_product_no_7 , a_work_normal_time_7 , a_work_over_time_7 , a_work_availability_time_7 , a_work_remark_7 , a_work_station_8 , a_production_8 , a_product_no_8 , a_work_normal_time_8 , a_work_over_time_8 , a_work_availability_time_8 , a_work_remark_8 , a_work_station_9 , a_production_9 , a_product_no_9 , a_work_normal_time_9 , a_work_over_time_9 , a_work_availability_time_9 , a_work_remark_9 , a_work_station_10 , a_production_10 , a_product_no_10 , a_work_normal_time_10 , a_work_over_time_10 , a_work_availability_time_10 , a_work_remark_10 , a_work_station_11 , a_production_11 , a_product_no_11 , a_work_normal_time_11 , a_work_over_time_11 , a_work_availability_time_11 , a_work_remark_11 , a_work_station_12 , a_production_12 , a_product_no_12 , a_work_normal_time_12 , a_work_over_time_12 , a_work_availability_time_12 , a_work_remark_12)

                if res == 'ok':
                    return render_template('/production_2_work_time_record.html')
                
                elif res == 'no':
                    logging.info(f"< Error > {b_date} - {a_name} , 液劑工時紀錄表 已被建立  !!! ")
            
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

############################
# /load_check_member_data
############################
@app.route("/load_check_member_data" , methods=['GET','POST'])
def load_check_member_data():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '生產二部 - 重新載入人員考評資料'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                check_year    = request.form['check_year']
                check_month   = request.form['check_month']
                employee_name = request.form['employee_name']

                res = db.load_check_member_data_list(check_year , check_month , employee_name)

                return render_template('ajax/load_check_member_data_list.html' , res=res)
            
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#######################
# /load_account_data
#######################
@app.route("/load_account_data" , methods=['GET','POST'])
def load_account_data():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '生產二部 - 載入人員考評資料'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        #if check_repeat_login == 'ok':
            
        ### operation record
        db.operation_record(r_time,user,login_code,operation_record_title)    
        
        #################
        # main content 
        #################
        if request.method == 'POST':
            
            load_user = request.form['user']
            
            a_job_title         = db.factory_check_form_item(user)
            a_member_check_list = db.factory_check_form_list()
            res                 = db.load_account_data_item(load_user)
            check_year          = db.load_account_data_form_item('check_year' , load_user)
            check_month         = db.load_account_data_form_item('check_month' , load_user)

            return render_template('ajax/load_account_data.html' , user=user , lv=lv , title=title , r_date=r_date , res=res , a_job_title=a_job_title , a_member_check_list=a_member_check_list , check_year=check_year , check_month=check_month)
            #return render_template('ajax/load_account_data_none.html')
        
        #else:
        #    return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##################################
# /update_submit_check_member_2
##################################
@app.route("/update_submit_check_member_2" , methods=['GET','POST'])
def update_submit_check_member_2():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '生產二部 - 主管評 人員考評表'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                employee_id     = request.form['employee_id']
                employee_name   = request.form['employee_name']
                check_year      = request.form['check_year']
                check_month     = request.form['check_month']

                sir_num1_1      = request.form['sir_num1_1']
                sir_num1_2      = request.form['sir_num1_2']
                sir_num1_3      = request.form['sir_num1_3']
                sir_num1_4      = request.form['sir_num1_4']

                sir_num2_1      = request.form['sir_num2_1']
                sir_num2_2      = request.form['sir_num2_2']
                sir_num2_3      = request.form['sir_num2_3']
                
                sir_num3_1      = request.form['sir_num3_1']
                sir_num3_2      = request.form['sir_num3_2']
                sir_num3_3      = request.form['sir_num3_3']

                sir_num4_1      = request.form['sir_num4_1']
                sir_num4_2      = request.form['sir_num4_2']
                sir_num4_3      = request.form['sir_num4_3']
                sir_num4_4      = request.form['sir_num4_4']

                sir_num5_1      = request.form['sir_num5_1']
                sir_num5_2      = request.form['sir_num5_2']
                sir_num5_3      = request.form['sir_num5_3']

                sir_num6_1      = request.form['sir_num6_1']
                sir_num6_2      = request.form['sir_num6_2']
                sir_num6_3      = request.form['sir_num6_3']

                sir_num7_1      = request.form['sir_num7_1']
                sir_num7_2      = request.form['sir_num7_2']
                sir_num7_3      = request.form['sir_num7_3']
                sir_num7_4      = request.form['sir_num7_4']

                sir_num8_1      = request.form['sir_num8_1']
                sir_num8_2      = request.form['sir_num8_2']
                sir_num8_3      = request.form['sir_num8_3']
                sir_num8_4      = request.form['sir_num8_4']
                sir_num8_5      = request.form['sir_num8_5']
                
                comment         = request.form['comment']
                other_total     = request.form['other_total']
                sir_total       = request.form['sir_total']
                other_plus_total = request.form['other_plus_total']
                final_total      = request.form['final_total']
                final_comment    = request.form['final_comment']
                
                res = db.update_submit_check_member_2(employee_id , employee_name , check_year , check_month , sir_num1_1 , sir_num1_2 , sir_num1_3 , sir_num1_4 , sir_num2_1 , sir_num2_2 , sir_num2_3 , sir_num3_1 , sir_num3_2 , sir_num3_3 , sir_num4_1 , sir_num4_2 , sir_num4_3 , sir_num4_4 , sir_num5_1 , sir_num5_2 , sir_num5_3 , sir_num6_1 , sir_num6_2 , sir_num6_3 , sir_num7_1 , sir_num7_2 , sir_num7_3 , sir_num7_4 , sir_num8_1 , sir_num8_2 , sir_num8_3 , sir_num8_4 , sir_num8_5 , comment , other_total , sir_total , other_plus_total , final_total , final_comment)
                
                if res == 'ok':
                    factory_work_station = db.factory_work_station()
                    a_work_no            = session['employee_id']
                    a_name               = session['user']
                    a_end_date           = session['end_date']
                    a_check_year         = db.search_member_item('check_year' , user)
                    a_check_month        = db.search_member_item('check_month' , user)
                    a_job_title          = db.factory_check_form_item(user)
                    a_member_check_list  = db.factory_check_form_list()
                    res_check_list       = db.check_add_check_member_list(user)
                    res_check_self_list  = db.check_add_check_member_self_list()

                    return render_template('production_2_work_check_record.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , a_end_date=a_end_date , dep_id=dep_id , check_year=r_year , check_month=r_month , a_job_title=a_job_title , a_member_check_list=a_member_check_list , res_check_list=res_check_list , res_check_self_list=res_check_self_list)    
                
                else:
                    return render_template('logout')    
                
                
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 



####################################
# /prouuction_2_work_check_record
####################################
@app.route("/production_2_work_check_record")
def production_2_work_check_record():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '生產二部 - 人員考評表'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date  = time.strftime("%Y-%m-%d" , time.localtime())
        r_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
        r_year  = time.strftime("%Y" , time.localtime())
        r_month = time.strftime("%m" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            session['employee_id'] = db.search_item('employee_id' , user)
            session['end_date']    = db.search_item('end_date' , user)

            ### 日當月報表
            day_money_by_year  = r_year
            day_money_by_month = db.bpm_day_money_by_month(r_year)

            factory_work_station = db.factory_work_station()
            a_work_no            = session['employee_id']
            a_name               = session['user']
            a_end_date           = session['end_date']
            a_check_year         = db.search_member_item('check_year' , user)
            a_check_month        = db.search_member_item('check_month' , user)
            a_job_title          = db.factory_check_form_item(user)
            a_member_check_list  = db.factory_check_form_list()
            res_check_list       = db.check_add_check_member_list(user)
            res_check_self_list  = db.check_add_check_member_self_list()

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)

            return render_template('production_2_work_check_record.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , 
                                    a_work_no=a_work_no , a_name=a_name , a_end_date=a_end_date , dep_id=dep_name , updep_name=updep_name , check_year=r_year , check_month=r_month ,
                                    a_job_title=a_job_title , a_member_check_list=a_member_check_list , res_check_list=res_check_list , res_check_self_list=res_check_self_list , 
                                    day_money_by_yea=day_money_by_year , day_money_by_month=day_money_by_month
                                     )
            
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##################################
# /load_card_reader_list_detail
##################################
@app.route("/load_card_reader_list_detail" , methods=['GET','POST'])
def load_card_reader_list_detail():
    if 'user' in session:
        
        ### operation record title
        #operation_record_title = '工廠 - 部門人員位置刷卡詳細資料'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        #check_repeat_login = db.check_login_code(user,login_code)

        #if check_repeat_login == 'ok':
        
        ### operation record
        #db.operation_record(r_time,user,login_code,operation_record_title)    
        
        #################
        # main content 
        #################
        if request.method == 'POST':
            
            e_name = request.form['e_name']
            
            ### operation record title
            operation_record_title = f'工廠 - {e_name}人員刷卡詳細資料'    

            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    

            card_reader_dep_res = db.load_card_reader_member_list_detail(e_name)

            return render_template('ajax/load_card_reader_list_detail.html' , e_name=e_name , card_reader_dep_res=card_reader_dep_res)

        #else:
            #return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###########################
# /search_card_reader_list
###########################
@app.route("/search_card_reader_list" , methods=['GET','POST'])
def search_card_reader_list():
    if 'user' in session:
        
        ### operation record title
        #operation_record_title = '工廠 - 部門人員位置'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        #check_repeat_login = db.check_login_code(user,login_code)

        #if check_repeat_login == 'ok':
            
        ### operation record
        #db.operation_record(r_time,user,login_code,operation_record_title)    
        
        #################
        # main content 
        #################
        if request.method == 'POST':
            
            
            dep = request.form['dep']

            ### operation record title
            operation_record_title = f'工廠 - {dep} 正職 , 派遣人員'    

            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    

            ### 正職人員
            card_reader_dep_res  = db.load_card_reader_member_list(dep)
            ### 正職人員 上班狀態
            card_reader_check_status_res = db.load_card_reader_member_check_status_list(dep)
            ### 正職人員 未上班人員
            card_reader_check_status_res2 = db.load_card_reader_member_check_status_list2(dep)
            ### 正職人員 應到
            card_reader_dep_total_res  = db.load_card_reader_member_list_total(dep)
            ### 正職人員 實到
            card_reader_dep_real_total_res  = db.load_card_reader_member_list_real_total(dep)
            ### 派遣人員
            card_reader_dep_res2 = db.load_card_reader_member_list2(dep)

            return render_template('ajax/load_card_reader_list.html' , dep=dep , card_reader_dep_res=card_reader_dep_res , card_reader_dep_total_res=card_reader_dep_total_res , card_reader_dep_real_total_res=card_reader_dep_real_total_res , card_reader_check_status_res=card_reader_check_status_res)

        #else:
            #return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##################################
# /card_reader_download_excel
##################################
@app.route("/card_reader_download_excel" , methods=['GET','POST'])
def card_reader_download_excel():
    if 'user' in session:
        
        ### operation record title
        #operation_record_title = '工廠 - 部門人員位置'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        #check_repeat_login = db.check_login_code(user,login_code)

        #if check_repeat_login == 'ok':
            
        ### operation record
        #db.operation_record(r_time,user,login_code,operation_record_title)    
        
        #################
        # main content 
        #################
        if request.method == 'POST':
            
            
            position = request.form['position']
            day      = request.form['day']

            ### operation record title
            operation_record_title = f'工廠 - {day} {position} 門禁刷卡紀錄 Excel 下載'    

            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    

            
            ### 本日
            card_reader_download_pdf_by_day  = db.card_reader_download_pdf(position , day)

            return render_template('ajax/load_card_reader_list_detail.html' , 
                                   position=position , card_reader_download_pdf_by_day=card_reader_download_pdf_by_day
                                   )

        #else:
            #return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#######################################
# /card_reader_download_pdf_by_month
#######################################
@app.route("/card_reader_download_pdf_by_month" , methods=['GET','POST'])
def card_reader_download_pdf_by_month():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '工廠 - 部門人員位置下載月清單'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                
                position = request.form['position']
                month    = request.form['month']

                ### operation record title
                operation_record_title = f'工廠 - {position} 門禁刷卡紀錄 {month} 月 , Excel 下載'    

                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    

                
                ### save to pdf and excel file
                db.card_reader_download_pdf_excel_by_month(position , month)

                #return render_template('ajax/load_card_reader_list_detail.html' , 
                #                      position=position
                #                       )

            else:
                return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##########################################
# /bpm_expenditure_download_excel
##########################################
@app.route("/bpm_expenditure_download_excel" , methods=['GET','POST'])
def bpm_expenditure_download_excel():
    if 'user' in session:
        
        ### operation record title
        #operation_record_title = '工廠 - 部門人員位置'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
        
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                q_s_date         = request.form['q_s_date']
                q_e_date         = request.form['q_e_date']
                q_b_e_dep        = request.form['q_b_e_dep']
                q_b_e_d_member   = request.form['q_b_e_d_member']
                q_b_e_status     = request.form['q_b_e_status']
                q_b_b_s_b_budget = request.form['q_b_b_s_b_budget']

                #print(f"msg : {q_s_date} {q_e_date} {q_b_e_dep} {q_b_e_d_member} {q_b_e_status}")

                ### operation record title
                operation_record_title = f'BPM 開支證明單 - {q_b_e_dep} {q_b_e_d_member} {q_b_e_status} Excel 下載'    

                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    
                
                ### save to pdf and excel file
                db.bpm_expenditure_form_download_excel_pdf(q_s_date , q_e_date , q_b_e_dep , q_b_e_d_member , q_b_e_status , q_b_b_s_b_budget)

                #return render_template('ajax/load_card_reader_list_detail.html' , 
                #                      position=position
                #                       )

            else:
                return redirect(url_for('logout'))

    return redirect(url_for('login')) 


##########################################
# /card_reader_download_pdf_every_month
##########################################
@app.route("/card_reader_download_pdf_every_month" , methods=['GET','POST'])
def card_reader_download_pdf_every_month():
    if 'user' in session:
        
        ### operation record title
        #operation_record_title = '工廠 - 部門人員位置'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
        
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                position = request.form['position']
                tb       = request.form['tb']

                ### operation record title
                operation_record_title = f'工廠 - {tb} {position} 門禁刷卡紀錄 Excel 下載'    

                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    
                
                ### save to pdf and excel file
                db.card_reader_download_pdf_excel_every_month(position , tb)

                #return render_template('ajax/load_card_reader_list_detail.html' , 
                #                      position=position
                #                       )

            else:
                return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##################################
# /hr_360_download_excel
##################################
@app.route("/hr_360_download_excel" , methods=['GET','POST'])
def hr_360_download_excel():
    if 'user' in session:
        
        ### operation record title
        #operation_record_title = '工廠 - 部門人員位置'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        #check_repeat_login = db.check_login_code(user,login_code)

        #if check_repeat_login == 'ok':
            
        ### operation record
        #db.operation_record(r_time,user,login_code,operation_record_title)    
        
        #################
        # main content 
        #################
        if request.method == 'POST':
            
            
            position = request.form['position']
            day      = request.form['day']

            ### operation record title
            operation_record_title = f'HR 360 - 考評紀錄 Excel 下載'    

            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    

            
            ### save to pdf and excel file
            db.card_reader_download_pdf_excel(position , day)

            #return render_template('ajax/load_card_reader_list_detail.html' , 
            #                      position=position
            #                       )

        #else:
            #return redirect(url_for('logout'))

    return redirect(url_for('login')) 

####################################
# /submit_finish_e_board
####################################
@app.route("/submit_finish_e_board" , methods=['GET','POST'])
def submit_finish_e_board():
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        #check_repeat_login = db.check_login_code(user,login_code)

        #if check_repeat_login == 'ok':
            
        ### operation record
        #db.operation_record(r_time,user,login_code,operation_record_title)    
        
        #################
        # main content 
        #################
        if request.method == 'POST':
            
            e_f_a_date = request.form['e_f_a_date']
            e_f_s_date = request.form['e_f_s_date']
            e_f_e_date = request.form['e_f_e_date']
            e_f_date   = request.form['e_f_date']
            e_f_name   = request.form['e_f_name']

            ### operation record title
            operation_record_title = f'送出回覆 - {e_f_date} {e_f_name} 電子看板申請單...'    

            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)   
            
            ### save to pdf and json file
            e_board_res = db.submit_finish_e_board(e_f_a_date , e_f_s_date , e_f_e_date , e_f_date , e_f_name)

            return render_template('ajax/reload_e_board_list.html' ,
                                    e_board_res=e_board_res
                                   )

####################################
# /submit_response_e_board
####################################
@app.route("/submit_response_e_board" , methods=['GET','POST'])
def submit_response_e_board():
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        #check_repeat_login = db.check_login_code(user,login_code)

        #if check_repeat_login == 'ok':
            
        ### operation record
        #db.operation_record(r_time,user,login_code,operation_record_title)    
        
        #################
        # main content 
        #################
        if request.method == 'POST':
            
            a_date = request.form['a_date']
            s_time = request.form['s_time']
            e_time = request.form['e_time']

            ### operation record title
            operation_record_title = f'回覆 - {a_date} {s_time} {e_time} 電子看板申請單完成時間...'    

            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    

            
            ### save to pdf and json file
            e_board_res_data = db.submit_response_e_board(a_date , s_time , e_time)

            return render_template('ajax/alter_e_board_list.html' ,
                                    e_board_res_data=e_board_res_data
                                   )


####################################
# /submit_e_board
####################################
@app.route("/submit_e_board" , methods=['GET','POST'])
def submit_e_board():
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        #check_repeat_login = db.check_login_code(user,login_code)

        #if check_repeat_login == 'ok':
            
        ### operation record
        #db.operation_record(r_time,user,login_code,operation_record_title)    
        
        #################
        # main content 
        #################
        if request.method == 'POST':
            
            e_a_date = request.form['e_a_date']
            e_s_date = request.form['e_s_date']
            e_e_date = request.form['e_e_date']
            e_c_name = request.form['e_c_name']
            e_title  = request.form['e_title']
            e_name   = request.form['e_name']
            e_other  = request.form['e_other']

            ### operation record title
            operation_record_title = f'送出 - {e_a_date} 電子看板申請單...'    

            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    

            
            ### save to pdf and json file
            e_board_res = db.submit_e_board(e_a_date , e_s_date , e_e_date , e_c_name , e_title , e_name , e_other)

            return render_template('ajax/reload_e_board_list.html' ,
                                    e_board_res=e_board_res
                                   )

####################################
# /factory_erp_ss2_download_json
####################################
@app.route("/factory_erp_ss2_download_json" , methods=['GET','POST'])
def factory_erp_ss2_download_json():
    if 'user' in session:
        
        ### operation record title
        #operation_record_title = '工廠 - 部門人員位置'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        #check_repeat_login = db.check_login_code(user,login_code)

        #if check_repeat_login == 'ok':
            
        ### operation record
        #db.operation_record(r_time,user,login_code,operation_record_title)    
        
        #################
        # main content 
        #################
        if request.method == 'POST':
            
            q_s_date = request.form['q_s_date']
            q_e_date = request.form['q_e_date']
            q_c_name = request.form['q_c_name']
            q_p_name = request.form['q_p_name']

            ### operation record title
            operation_record_title = f'工廠 ERP / SS2 - {q_s_date} ~ {q_e_date} 紀錄 json 下載'    

            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    

            
            ### save to pdf and json file
            db.factory_erp_ss2_download_pdf_json(q_s_date , q_e_date , q_c_name , q_p_name)

            #return render_template('ajax/load_card_reader_list_detail.html' , 
            #                      position=position
            #                       )

        #else:
            #return redirect(url_for('logout'))

    return redirect(url_for('login'))

########################################
# /factory_erp_subform_download_excel
########################################
@app.route("/factory_erp_subform_download_excel" , methods=['GET','POST'])
def factory_erp_subform_download_excel():
    if 'user' in session:
        
        ### operation record title
        #operation_record_title = '工廠 - 部門人員位置'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        #check_repeat_login = db.check_login_code(user,login_code)

        #if check_repeat_login == 'ok':
            
        ### operation record
        #db.operation_record(r_time,user,login_code,operation_record_title)    
        
        #################
        # main content 
        #################
        if request.method == 'POST':
            
            q_s_date = request.form['q_s_date']
            q_e_date = request.form['q_e_date']

            ### operation record title
            operation_record_title = f'工廠 ERP 子單身 - {q_s_date} ~ {q_e_date} 資料 Excel 下載'    

            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            ### save to pdf and excel file
            db.factory_erp_subform_download_pdf_excel(q_s_date , q_e_date)


    return redirect(url_for('login'))

####################################
# /factory_erp_ss2_download_excel
####################################
@app.route("/factory_erp_ss2_download_excel" , methods=['GET','POST'])
def factory_erp_ss2_download_excel():
    if 'user' in session:
        
        ### operation record title
        #operation_record_title = '工廠 - 部門人員位置'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        #check_repeat_login = db.check_login_code(user,login_code)

        #if check_repeat_login == 'ok':
            
        ### operation record
        #db.operation_record(r_time,user,login_code,operation_record_title)    
        
        #################
        # main content 
        #################
        if request.method == 'POST':
            
            q_s_date = request.form['q_s_date']
            q_e_date = request.form['q_e_date']
            q_c_name = request.form['q_c_name']
            q_p_name = request.form['q_p_name']

            ### operation record title
            operation_record_title = f'工廠 ERP / SS2 - {q_s_date} ~ {q_e_date} 紀錄 Excel 下載'    

            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    

            
            ### save to pdf and excel file
            db.factory_erp_ss2_download_pdf_excel(q_s_date , q_e_date , q_c_name , q_p_name)

            #return render_template('ajax/load_card_reader_list_detail.html' , 
            #                      position=position
            #                       )

        #else:
            #return redirect(url_for('logout'))

    return redirect(url_for('login'))

##################################
# /hr_360_download_excel_2
##################################
@app.route("/hr_360_download_excel_2" , methods=['GET','POST'])
def hr_360_download_excel_2():
    if 'user' in session:
        
        ### operation record title
        #operation_record_title = '工廠 - 部門人員位置'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        #check_repeat_login = db.check_login_code(user,login_code)

        #if check_repeat_login == 'ok':
            
        ### operation record
        #db.operation_record(r_time,user,login_code,operation_record_title)    
        
        #################
        # main content 
        #################
        if request.method == 'POST':
            
            job = request.form['job']

            ### operation record title
            operation_record_title = f'HR 360 - {job} 紀錄 Excel 下載'    

            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    

            
            ### save to pdf and excel file
            db.hr_360_download_pdf_excel(job)

            #return render_template('ajax/load_card_reader_list_detail.html' , 
            #                      position=position
            #                       )

        #else:
            #return redirect(url_for('logout'))

    return redirect(url_for('login'))

##################################
# /card_reader_download_pdf
##################################
@app.route("/card_reader_download_pdf" , methods=['GET','POST'])
def card_reader_download_pdf():
    if 'user' in session:
        
        ### operation record title
        #operation_record_title = '工廠 - 部門人員位置'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        #check_repeat_login = db.check_login_code(user,login_code)

        #if check_repeat_login == 'ok':
            
        ### operation record
        #db.operation_record(r_time,user,login_code,operation_record_title)    
        
        #################
        # main content 
        #################
        if request.method == 'POST':
            
            
            position = request.form['position']
            day      = request.form['day']

            ### operation record title
            operation_record_title = f'工廠 - {day} {position} 門禁刷卡紀錄 Excel 下載'    

            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    

            
            ### save to pdf and excel file
            db.card_reader_download_pdf_excel(position , day)

            #return render_template('ajax/load_card_reader_list_detail.html' , 
            #                      position=position
            #                       )

        #else:
            #return redirect(url_for('logout'))

    return redirect(url_for('login')) 


##########################################
# /load_card_reader_list_by_every_month
##########################################
@app.route("/load_card_reader_list_by_every_month" , methods=['GET','POST'])
def load_card_reader_list_by_every_month():
    if 'user' in session:

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                position = request.form['position']
                tb       = request.form['tb']

                ### operation record title
                operation_record_title = '工廠 - 部門人員位置'    

                ### operation record title
                operation_record_title = f'工廠 - {position} {tb} 門禁刷卡紀錄'    

                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    
                
                ### 月份
                card_reader_door_list_by_every_month  = db.load_card_reader_door_list_by_every_month_detail(position , tb)

                return render_template('ajax/load_card_reader_list_detail_every_month.html' , 
                                    position=position , card_reader_door_list_by_every_month=card_reader_door_list_by_every_month
                                    )

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##################################
# /load_card_reader_list_by_day
##################################
@app.route("/load_card_reader_list_by_day" , methods=['GET','POST'])
def load_card_reader_list_by_day():
    if 'user' in session:
        
        ### operation record title
        #operation_record_title = '工廠 - 部門人員位置'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        #check_repeat_login = db.check_login_code(user,login_code)

        #if check_repeat_login == 'ok':
            
        ### operation record
        #db.operation_record(r_time,user,login_code,operation_record_title)    
        
        #################
        # main content 
        #################
        if request.method == 'POST':
            
            
            position = request.form['position']
            day      = request.form['day']

            ### operation record title
            operation_record_title = f'工廠 - {day} {position} 門禁刷卡紀錄'    

            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    

            
            ### 本日
            card_reader_door_list_by_day  = db.load_card_reader_door_list_by_day(position , day)

            return render_template('ajax/load_card_reader_list_detail.html' , 
                                   position=position , card_reader_door_list_by_day=card_reader_door_list_by_day
                                   )

        #else:
            #return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###########################
# /load_card_reader_list
###########################
@app.route("/load_card_reader_list" , methods=['GET','POST'])
def load_card_reader_list():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '工廠 - 部門人員刷卡位置'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_month = time.strftime("%Y%m" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
        
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                position = request.form['dep']

                ### operation record title
                operation_record_title = f'工廠 - {position} 門禁刷卡紀錄'    

                ### operation record
                db.operation_record(r_time,user,login_code,operation_record_title)    


                ### 月份
                card_reader_door_list_by_every_month = db.load_card_reader_door_list_by_every_month(position)

                ### 本月
                card_reader_door_list_by_month = db.load_card_reader_door_list_by_month(position)
                ### 本日
                card_reader_door_list_by_day  = db.load_card_reader_door_list(position)
                
                ### 正職人員 上班狀態
                #card_reader_check_status_res = db.load_card_reader_member_check_status_list(dep)
                ### 正職人員 未上班人員
                #card_reader_check_status_res2 = db.load_card_reader_member_check_status_list2(dep)
                ### 正職人員 應到
                #card_reader_dep_total_res  = db.load_card_reader_member_list_total(dep)
                ### 正職人員 實到
                #card_reader_dep_real_total_res  = db.load_card_reader_member_list_real_total(dep)
                ### 派遣人員
                #card_reader_dep_res2 = db.load_card_reader_member_list2(dep)

                return render_template('ajax/load_card_reader_list.html' , 
                                    position=position , 
                                    card_reader_door_list_by_day=card_reader_door_list_by_day , 
                                    card_reader_door_list_by_month=card_reader_door_list_by_month , 
                                    r_month=r_month , card_reader_door_list_by_every_month=card_reader_door_list_by_every_month
                                    )

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###############################
# /card_reader_member_search
###############################
@app.route("/card_reader_member_search")
def card_reader_member_search():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '工廠 - 人員位置查詢'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            
            ### 日當月報表
            day_money_by_year  = r_year
            day_money_by_month = db.bpm_day_money_by_month(r_year)

            factory_work_station = db.factory_work_station()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            res_work_time_list      = db.show_work_time_list(a_name , a_work_no)
            normal_total_time       = db.show_work_time_total_val(a_name , a_work_no , 'normal_time')
            over_total_time         = db.show_work_time_total_val(a_name , a_work_no , 'over_time')
            availability_total_time = db.show_work_time_total_val(a_name , a_work_no , 'availability_time')
            total_time              = db.show_work_time_total_val(a_name , a_work_no , 'total_time')

            # load_work_time_data = db.load_work_time_data_list(e_id , e_name , b_date)
            card_reader_res  = db.load_check_member_data_list2(user)

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)


            return render_template('search_card_reader_member.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , 
                                    a_work_no=a_work_no , a_name=a_name , dep_id=dep_name , updep_name=updep_name , res_work_time_list=res_work_time_list , 
                                    normal_total_time=normal_total_time ,over_total_time=over_total_time , availability_total_time=availability_total_time , total_time=total_time , 
                                    card_reader_res=card_reader_res , day_money_by_year=day_money_by_year , day_money_by_month=day_money_by_month)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#########################
# /load_work_time_data
#########################
@app.route("/load_work_time_data" , methods=['GET','POST'])
def load_work_time_data():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '生產二部 - 載入液劑工時時間記錄表資料'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':
                
                b_date = request.form['b_date']
                e_id   = request.form['e_id']
                e_name = request.form['e_name']

                factory_work_station = db.factory_work_station()
                a_work_no = db.search_item('employee_id' , user)
                a_name    = db.search_item('employee_name' , user)

                res_work_time_list      = db.show_work_time_list(a_name , a_work_no)
                normal_total_time       = db.show_work_time_total_val(a_name , a_work_no , 'normal_time')
                over_total_time         = db.show_work_time_total_val(a_name , a_work_no , 'over_time')
                availability_total_time = db.show_work_time_total_val(a_name , a_work_no , 'availability_time')
                total_time              = db.show_work_time_total_val(a_name , a_work_no , 'total_time')

                load_work_time_data = db.load_work_time_data_list(e_id , e_name , b_date)

                return render_template('ajax/load_work_time_data.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , res_work_time_list=res_work_time_list , normal_total_time=normal_total_time , over_total_time=over_total_time , availability_total_time=availability_total_time , total_time=total_time , load_work_time_data=load_work_time_data)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###################################
# /production_2_work_time_record
###################################
@app.route("/production_2_work_time_record")
def production_2_work_time_record():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '生產二部 - 液劑工時時間記錄表'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id']

        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            factory_work_station = db.factory_work_station()
            a_work_no = db.search_item('employee_id' , user)
            a_name    = db.search_item('employee_name' , user)

            ### 日當月報表
            day_money_by_year  = r_year
            day_money_by_month = db.bpm_day_money_by_month(r_year)

            res_work_time_list      = db.show_work_time_list(a_name , a_work_no)
            normal_total_time       = db.show_work_time_total_val(a_name , a_work_no , 'normal_time')
            over_total_time         = db.show_work_time_total_val(a_name , a_work_no , 'over_time')
            availability_total_time = db.show_work_time_total_val(a_name , a_work_no , 'availability_time')
            total_time              = db.show_work_time_total_val(a_name , a_work_no , 'total_time')

            return render_template('production_2_work_time_record.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , res_work_time_list=res_work_time_list , normal_total_time=normal_total_time , over_total_time=over_total_time , availability_total_time=availability_total_time , total_time=total_time , day_money_by_year=day_money_by_year , day_money_by_month=day_money_by_month)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

######
# /
######
@app.route("/")
def index():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = 'Otsuak 主頁'    

        ### session 
        user       = session['user']
        lv         = session['lv']
        login_code = session['login_code']
        dep_id     = session['department_id'] if session['department_id'] is not None else None

        
        ### r_time
        r_year = time.strftime("%Y" , time.localtime())
        r_date = time.strftime("%Y-%m-%d" , time.localtime())
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################

            ### 月報表
            day_money_by_year  = r_year
            day_money_by_month = db.bpm_day_money_by_month(r_year)

            ### department name & updepartment name
            dep_name           = db.bpm_account_department(user , 'DepartmentName')
            updep_id           = db.bpm_account_department(user , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)

            ### HR data
            hr_data1 = db.hr_data(session['user'])
            hr_data1 = 'no data' if hr_data1 is None else hr_data1

            hr_data2 = db.hr_data_2(session['user'])
            hr_data2 = 'no data' if hr_data2 is None else hr_data2

            hr_data3 = db.hr_data_3(session['user'] , '2023')
            hr_data3 = 'no data' if hr_data3 is None else hr_data3

            hr_data4 = db.hr_data_3(session['user'] , '2024')
            hr_data4 = 'no data' if hr_data4 is None else hr_data4

            return render_template('index.html' ,  user=user , lv=lv , title=title , dep_id=dep_name , 
                                   updep_name=updep_name , day_money_by_year=day_money_by_year , day_money_by_month=day_money_by_month ,
                                   hr_data1=hr_data1 , hr_data2=hr_data2 , hr_data3=hr_data3 , hr_data4=hr_data4
                                   )

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

########################
# /wms_picking_list_3
########################
@app.route("/wms_picking_list_3" , methods=['GET'])
def wms_picking_list_3():
    
    #################
    # main content
    #################
    if request.method == 'GET':

        tb  = request.args.get('tb')
        i1  = request.args.get('i1')
        i2  = request.args.get('i2')
        i3  = request.args.get('i3')
        i4  = request.args.get('i4')
        
        ### operation record title
        operation_record_title  = f"WMS 倉儲系統 - 刪除調撥單,領料單,製令單 api {tb}/{i1}/{i2}/{i3}/{i4}"

        ### main content
        try:
            ##################
            # 調撥單 & 退料單
            ##################
                res = db.wms_add_erp_picking_list_data_1(i1,i2,i3,i4)
                return jsonify({"msg": res})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

########################
# /wms_picking_list_2
########################
@app.route("/wms_picking_list_2" , methods=['GET'])
def wms_picking_list_2():
    
    #################
    # main content
    #################
    if request.method == 'GET':

        tb  = request.args.get('tb')
        i1  = request.args.get('i1')
        i2  = request.args.get('i2')
        i3  = request.args.get('i3')
        i4  = request.args.get('i4')
        
        ### operation record title
        operation_record_title  = f"WMS 倉儲系統 - 新增調撥單,領料單,製令單 api {tb}/{i1}/{i2}/{i3}/{i4}"

        ### main content
        try:
            ##################
            # 調撥單 & 退料單
            ##################
                res = db.wms_add_erp_picking_list_data_1(i1,i2,i3,i4)
                return jsonify({"msg": res})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

########################
# /wms_picking_list_1
########################
@app.route("/wms_picking_list_1",methods=['GET'])
def wms_picking_list_1():
    
    #################
    # main content
    #################
    if request.method == 'GET':

        f_h = request.args.get('form_head')
        f_b = request.args.get('form_body')
        
        ### operation record title
        operation_record_title = f"WMS 倉儲系統 - 領料單查詢 api 1 {f_h}-{f_b}"

        ### main content
        try:
            res = db.wms_query_erp_picking_list_query(f_h, f_b)

            return res

        except Exception as e:
            return jsonify({"error": str(e)}), 500

###############
# /wms_login
###############
@app.route("/wms_login" , methods=['GET','POST'])
def wms_login():

    if request.method == 'POST':
        
        check_account = db.wms_login(request.form['user'] , request.form['pwd'])
        dep_id        = db.dep_id(request.form['user'] , request.form['pwd'])

        ### link mysql
        #if check_account is not None: 
        ### link AD Server
        if check_account == 1:  
            
            ### r_time
            r_year = time.strftime("%Y" , time.localtime())
            r_date = time.strftime("%Y-%m-%d" , time.localtime())
            r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
            
            ### operation record title
            operation_record_title = f"WMS 倉儲系統 , {request.form['user']} 登入成功."    
            
            ### session  
            #session['user'] = request.form['user']
            
            ### mysql 
            #session['user'] = check_account[0]
            
            ### AD Server 
            #session['user'] = request.form['user']
            session['user'] = db.login_ad_user(request.form['user'])
            
            ### for python3 md5 use method
            m = hashlib.md5()
            m.update(r_time.encode('utf-8'))
            h = m.hexdigest()
            session['login_code']    = h
            session['ip']            = request.remote_addr
            session['lv']            = 3
            session['department_id'] = dep_id
            
            ### login record
            db.login_record(session['user'],session['login_code'],r_time,session['ip'])
            
            ### operation record
            db.operation_record(r_time , session['user'] , session['login_code'] , operation_record_title)    

            #################
            # main content
            #################
            #res_data           = db.realtime_modbus_sensor()
            
            day_money_by_year  = r_year
            day_money_by_month = db.bpm_day_money_by_month(r_year)
            
            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)

            msg = "login success"
            res_data = json.dumps({"Otsuak AD Server": msg})
            return res_data

        else:
            msg = "login fail"
            res_data = json.dumps({"Otsuka AD Server": msg})
            return res_data

    else:
        return render_template('wms_login.html' , title=title)

##########
# /login
##########
@app.route("/login" , methods=['GET','POST'])
def login():
    if request.method == 'POST':
        check_account = db.login(request.form['user'] , request.form['pwd'])
        dep_id        = db.dep_id(request.form['user'] , request.form['pwd'])

        ### link mysql
        #if check_account is not None: 
        ### link AD Server
        if check_account == 1:  
            
            ### r_time
            r_year = time.strftime("%Y" , time.localtime())
            r_date = time.strftime("%Y-%m-%d" , time.localtime())
            r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
            
            ### operation record title
            operation_record_title = '登入成功'    
            
            ### session  
            #session['user'] = request.form['user']
            
            ### mysql 
            #session['user'] = check_account[0]
            
            ### AD Server 
            #session['user'] = request.form['user']
            session['user'] = db.login_ad_user(request.form['user'])
            
            ### for python3 md5 use method
            m = hashlib.md5()
            m.update(r_time.encode('utf-8'))
            h = m.hexdigest()
            session['login_code']    = h
            session['ip']            = request.remote_addr
            session['lv']            = 3
            session['department_id'] = dep_id
            
            ### login record
            db.login_record(session['user'],session['login_code'],r_time,session['ip'])
            
            ### operation record
            db.operation_record(r_time , session['user'] , session['login_code'] , operation_record_title)    

            #################
            # main content
            #################
            #res_data           = db.realtime_modbus_sensor()
            
            day_money_by_year  = r_year
            day_money_by_month = db.bpm_day_money_by_month(r_year)
            
            ### department name & updepartment name
            dep_name           = db.bpm_account_department(session['user'] , 'DepartmentName')
            updep_id           = db.bpm_account_department(session['user'] , 'UpperDepartmentID')
            updep_name         = db.bpm_account_up_department(updep_id)

            ### HR data
            hr_data1 = db.hr_data(session['user'])
            hr_data1 = 'no data' if hr_data1 is None else hr_data1

            hr_data2 = db.hr_data_2(session['user'])
            hr_data2 = 'no data' if hr_data2 is None else hr_data2

            hr_data3 = db.hr_data_3(session['user'] , '2023')
            hr_data3 = 'no data' if hr_data3 is None else hr_data3

            hr_data4 = db.hr_data_3(session['user'] , '2024')
            hr_data4 = 'no data' if hr_data4 is None else hr_data4

            return render_template('index.html' ,  user=session['user'] , lv=session['lv'] , title=title , dep_id=dep_name , updep_name=updep_name , 
                                   day_money_by_year=day_money_by_year , day_money_by_month=day_money_by_month ,
                                   hr_data1=hr_data1 , hr_data2=hr_data2 , hr_data3=hr_data3 , hr_data4=hr_data4
                                   )

        else:
            res_data = "登入失敗，帳密有錯，重新輸入 !!!"
            return render_template('login.html' , login_msg=res_data , title=title)

    else:
        return render_template('login.html' , title=title)

#############
# /logout2 
#############
@app.route("/logout2",methods=['POST','GET'])
def logout2():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '登出成功'

        ### session 
        user = session['user']

        ### r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        if request.method == 'GET':
            ### logout record
            try:
                db.logout_record(session['user'] , session['login_code'] , r_time)
            except Exception as e:
                logging.info("< Error > logout record : " + str(e))
            finally:
                pass
            
            ### operation record
            db.operation_record(r_time , user , session['login_code'] , operation_record_title)    

            ### clean up session param
            session.pop('user',None)
            session.pop('login_code',None)
            session.pop('ip',None)
            session.pop('lv',None)
            session.pop('department_id',None)

    return redirect(url_for('index'))

###########
# /logout 
###########
@app.route("/logout")
def logout():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '登出成功'

        ### session 
        user = session['user']

        ### r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
    
        ### logout record
        try:
            db.logout_record(session['user'] , session['login_code'] , r_time)
        except Exception as e:
            logging.info("< Error > logout record : " + str(e))
        finally:
            pass
        
        ### operation record
        db.operation_record(r_time , user , session['login_code'] , operation_record_title)    

        ### clean up session param
        session.pop('user',None)
        session.pop('login_code',None)
        session.pop('ip',None)
        session.pop('lv',None)
        session.pop('department_id',None)

    return redirect(url_for('index'))

#####################
# /account_manager
#####################
@app.route("/account_manager",methods=['POST','GET'])
def account_manager():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '帳號管理'    

        ### session
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            ### operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == 'POST':
                
                del_no = request.form['del_no']
                res = db.del_menu_money_record(user , del_no)
                
                if res == 'ok':
                    data = db.menu_money_record(user)
                    return render_template('ajax/reload_menu_money_record.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))


#####################
# error 404 page
#####################
@app.errorhandler(404)
def page_not_found(e):
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '404 錯誤 , 頁面未找到 !'    

        ### session
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            ### operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            return render_template('404.html' , user=session['user'] , lv=session['lv'] , title=title) , 404

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

#####################
# error 500 page
#####################
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html' , title=title) , 500

#####################
# error 502 page
#####################
@app.errorhandler(502)
def page_not_found(e):
    return render_template('502.html' , title=title) , 502

########################################################################################################################################
#
# start
#
########################################################################################################################################
if __name__ == "__main__":
    
    ##########
    # Flask
    ##########
    asyncio.run(app.run(host="0.0.0.0" , port=9095 , debug=True))
    
    
    
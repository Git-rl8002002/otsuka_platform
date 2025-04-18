#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author   : JasonHung
# Date     : 20221102
# Update   : 20230720
# Function : otsuka factory work time record

from argparse import Namespace
from dataclasses import dataclass
from distutils.log import debug
from email import charset
from hashlib import md5
import hashlib , time , logging , random , openpyxl , csv , os , mimetypes , pymysql
from tabnanny import check
from flask import Flask,render_template,request,session,url_for,redirect , Response , send_file 
from flask_socketio import SocketIO , emit 
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO


### matplotlib 
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from control.config import *
from control.web_cloud_dao import web_cloud_dao 

db = web_cloud_dao()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

########
# log
########
log_format = "%(asctime)s %(message)s"
logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")

##############
# variables
##############
title  = parm['title']



##############################
# /test2
##############################
@app.route("/test2")
def test2():
    return render_template('test2.html')    

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
                s_c_kind                 = m_device[s_kind]
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

            
            return render_template('factory_monitor_record.html' , 
                                   user=user , title=title , dep_id=dep_id , kind_position=kind_position , 
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
                
            return render_template('computer_used_record.html' , user=user , title=title , dep_id=dep_id , d_name=d_name , day_money_by_year=day_money_by_year, day_money_by_month=day_money_by_month)

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

            return render_template('production_3_work_time_record.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , day_money_by_year=day_money_by_year , day_money_by_month=day_money_by_month)

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

            ### 日當月報表
            day_money_by_year  = r_year
            day_money_by_month = db.bpm_day_money_by_month(r_year)

            ### 部門清單
            department_list = db.department_account_list()
            
            return render_template('search_department_id.html' , user=user , lv=lv , title=title , operation_record_title=operation_record_title , r_date=r_date , dep_id=dep_id , day_money_by_year=day_money_by_year , day_money_by_month=day_money_by_month , department_list=department_list)
        
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
        operation_record_title = '生產二部 - 新增人員考核表資料'    

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
        operation_record_title = '生產二部 - 新增人員考核帳號表資料'    

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
        operation_record_title = '生產二部 - 載入新增人員考核帳號表'    

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
        operation_record_title = '生產二部 - 載入人員考核表資料'    

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
        operation_record_title = '生產二部 - 重新載入人員考核資料'    

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
        operation_record_title = '生產二部 - 載入人員考核資料'    

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
        operation_record_title = '生產二部 - 主管評 人員考核表'    

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
        operation_record_title = '生產二部 - 人員考核表'    

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

            return render_template('production_2_work_check_record.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , a_end_date=a_end_date , dep_id=dep_id , check_year=r_year , check_month=r_month , a_job_title=a_job_title , a_member_check_list=a_member_check_list , res_check_list=res_check_list , res_check_self_list=res_check_self_list , day_money_by_yea=day_money_by_year , day_money_by_month=day_money_by_month)
            
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

###########################
# /load_card_reader_list
###########################
@app.route("/load_card_reader_list" , methods=['GET','POST'])
def load_card_reader_list():
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

            #load_work_time_data = db.load_work_time_data_list(e_id , e_name , b_date)
            card_reader_res  = db.load_check_member_data_list2(user)
            card_reader_res2 = db.load_check_member_data_list3(user)
            card_reader_res3 = db.load_group_member_list(user)


            return render_template('search_card_reader_member.html' , user=user , lv=lv , title=title , r_date=r_date , factory_work_station=factory_work_station , a_work_no=a_work_no , a_name=a_name , dep_id=dep_id , res_work_time_list=res_work_time_list , normal_total_time=normal_total_time , over_total_time=over_total_time , availability_total_time=availability_total_time , total_time=total_time , card_reader_res=card_reader_res , day_money_by_year=day_money_by_year , day_money_by_month=day_money_by_month)

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
        operation_record_title = '主頁'    

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

            return render_template('index.html' ,  user=session['user'] , lv=session['lv'] , title=title , dep_id=session['department_id'] , day_money_by_year=day_money_by_year , day_money_by_month=day_money_by_month)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##########
# /login
##########
@app.route("/login" , methods=['GET','POST'])
def login():
    if request.method == 'POST':
        check_account = db.login(request.form['user'] , request.form['pwd'])
        dep_id        = db.dep_id(request.form['user'] , request.form['pwd'])

        if check_account is not None:
            
            ### r_time
            r_year = time.strftime("%Y" , time.localtime())
            r_date = time.strftime("%Y-%m-%d" , time.localtime())
            r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
            
            ### operation record title
            operation_record_title = '登入成功'    
            
            ### session  
            #session['user'] = request.form['user']
            session['user'] = check_account[0]
            
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

            return render_template('index.html' ,  user=session['user'] , lv=session['lv'] , title=title , dep_id=session['department_id'] , day_money_by_year=day_money_by_year , day_money_by_month=day_money_by_month)

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

########################################################################################################################################
#
# start
#
########################################################################################################################################
if __name__ == "__main__":
    
    ##########
    # Flask
    ##########
    app.run(host="0.0.0.0" , port=9095 , debug=True)
    
    
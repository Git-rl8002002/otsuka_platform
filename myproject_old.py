#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author   : JasonHung
# Date     : 20221102
# Update   : 20240118
# Function : otsuka project 1 - all platform

###################
# import package
###################
import hashlib , time , logging , random , csv , os , mimetypes 
from flask import Flask,render_template,request,session,url_for,redirect , Response , send_file 

#################
# import class
#################
from control.config import *
from control.web_cloud_dao import web_cloud_dao 

db = web_cloud_dao()

##############
# variables
##############
title  = parm['title']

#################
# python Flask 
#################
app = Flask(__name__)

########
# log
########
log_format = "%(asctime)s %(message)s"
logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")

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
        #dep_id        = db.dep_id(request.form['user'] , request.form['pwd'])

        if check_account is not None:
            
            ### r_time
            r_year = time.strftime("%Y" , time.localtime())
            r_date = time.strftime("%Y-%m-%d" , time.localtime())
            r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
            
            ### operation record title
            operation_record_title = '登入成功'    
            
            ### session  
            #session['user'] = request.form['user']
            session['user']  = check_account[0]
            
            ### for python3 md5 use method
            m = hashlib.md5()
            m.update(r_time.encode('utf-8'))
            h = m.hexdigest()
            session['login_code']    = h
            session['ip']            = request.remote_addr
            session['lv']            = 3
            #session['department_id'] = dep_id
            
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

########################################################################################################################################
#
# main 
#
########################################################################################################################################
if __name__ == "__main__":
    
    ##########
    # Flask
    ##########
    app.run(host='0.0.0.0' , port=9095 , debug=True)

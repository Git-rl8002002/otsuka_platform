/*****************************************************************
*
* Author   : JasonHung
* Date     : 20221102
* Update   : 20230908
* Function : otsuka for factory work time system
*
******************************************************************/

/****************************** 
 *
 * database : otsuka_factory
 *
 ******************************/
create database otsuka_factory DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
use otsuka_factory;

/************************************************************  
 *
 * WMS 商品基本檔 EPR 對應 SS2
 * DB : MSSQL
 *
 ************************************************************/
CREATE TABLE wms_product_erp_ss2 (
    no INT NOT NULL PRIMARY KEY IDENTITY(1,1),  
    c_date DATE NULL,
    c_time TIME NULL,
    c_d_time DATETIME NULL,
    p_c_name nvarchar(100) NULL,
    ss2_p_c_num nvarchar(100) NULL,
    erp_p_c_num nvarchar(255) NULL
);

/************************************************************  
 *
 * WMS 商品基本檔
 * DB : MSSQL
 *
 ************************************************************/
CREATE TABLE wms_product_basic_data (
    no INT NOT NULL PRIMARY KEY IDENTITY(1,1),  
    c_date DATE NULL,
    c_time TIME NULL,
    c_d_time DATETIME NULL,
    f_b_num nvarchar(100) NULL,
    f_ss2_b_num nvarchar(100) NULL,
    f_b_name nvarchar(255) NULL,
    f_spec nvarchar(255) NULL,
    f_limit nvarchar(1) NULL,
    f_b_limit nvarchar(1) NULL,
    f_a_temp nvarchar(1) NULL,
    f_l_medicial nvarchar(1) NULL,
    f_l_cool nvarchar(1) NULL,
    f_b_package int NULL,
    f_b_p_unit nvarchar(5) NULL,
    f_m_package int NULL,
    f_m_p_unit nvarchar(5) NULL,
    f_m_unit nvarchar(30) NULL,
    f_b_p_amount int NULL,
    f_b_p_unit2 nvarchar(5) NULL,
    f_i_barcode nvarchar(15) NULL,
    f_p_type nvarchar(10) NULL,
    f_rw_barcode nvarchar(1) NULL
);

/************************************************************  
 *
 * WMS AD account 帳號管理 
 * DB : MSSQL
 *
 ************************************************************/
CREATE TABLE wms_ad_account (
    no INT NOT NULL PRIMARY KEY IDENTITY(1,1),  
    c_date DATE NULL,
    c_time TIME NULL,
    c_d_time DATETIME NULL,
    u_name VARCHAR(100) NULL,
    u_email VARCHAR(300) NULL,
    u_e_name VARCHAR(100) NULL,
    u_c_name VARCHAR(100) NULL,
    w_dep VARCHAR(80) NULL,
    w_title VARCHAR(80) NULL,
    w_status VARCHAR(40) NULL
);


/************************************************************  
 *
 * 工作進度表
 *
 ************************************************************/
create table work_record_form(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_time time null,
c_d_time datetime null,
w_dep varchar(50) null,
w_dep_id varchar(50) null,
w_kind varchar(30) null,
w_title varchar(300) null,
w_place varchar(50) null,
w_start date null,
w_content text,
w_end date null,
w_update datetime null,
w_status varchar(30) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


/************************************************************  
 *
 * mrd 8 政府公告
 *
 ************************************************************/
create table mrd_8_government_bulletin_relase(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_time time null,
c_d_time datetime null,
b_from varchar(200) null,
b_year varchar(200) null,
b_kind varchar(200) null,
b_title text,
b_url text null,
b_relase_date date null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************************************************  
 *
 * mrd 8 公告自動 email 通知 
 *
 ************************************************************/
create table mrd_8_auto_email_push(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_time time null,
c_d_time datetime null,
login_id varchar(100) null,
dep varchar(100) null,
email varchar(100) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


/************************************************************  
 *
 * warehouse - export form 出貨單 (轉倉到豐田外倉) 
 *
 ************************************************************/
create table w_export_form(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_time time null,
c_d_time datetime null,
item_1 varchar(100) null,
item_2 varchar(100) null,
item_3 varchar(100) null,
item_4 varchar(100) null,
item_5 varchar(100) null,
item_6 varchar(100) null,
item_7 varchar(100) null,
item_8 varchar(100) null,
item_9 varchar(100) null,
item_10 varchar(100) null,
item_11 varchar(100) null,
item_12 varchar(100) null,
item_13 varchar(100) null,
item_14 varchar(100) null,
item_15 varchar(100) null,
item_16 varchar(100) null,
item_17 varchar(100) null,
item_18 varchar(100) null,
item_19 varchar(100) null,
item_20 varchar(100) null,
item_21 varchar(100) null,
item_22 varchar(100) null,
item_23 varchar(100) null,
item_24 varchar(100) null,
item_25 varchar(100) null,
item_26 varchar(100) null,
item_27 varchar(100) null,
item_28 varchar(100) null,
d_from varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************************************************  
 *
 * warehouse - import form 進貨單 (轉倉到豐田外倉) 
 *
 ************************************************************/
create table w_import_form(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_time time null,
c_d_time datetime null,
item_1 varchar(100) null,
item_2 varchar(100) null,
item_3 varchar(100) null,
item_4 varchar(100) null,
item_5 varchar(100) null,
item_6 varchar(100) null,
item_7 varchar(100) null,
item_8 varchar(100) null,
item_9 varchar(100) null,
item_10 varchar(100) null,
item_11 varchar(100) null,
item_12 varchar(100) null,
item_13 varchar(100) null,
d_from varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


/************************************************************  
 *
 * warehouse - basic product form 商品基本檔單 (轉倉到豐田外倉) 
 *
 ************************************************************/
create table w_basic_product_form(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_time time null,
c_d_time datetime null,
item_1 varchar(100) null,
item_2 varchar(100) null,
item_3 varchar(100) null,
item_4 varchar(100) null,
item_5 varchar(100) null,
item_6 varchar(100) null,
item_7 varchar(100) null,
item_8 varchar(100) null,
item_9 varchar(100) null,
item_10 varchar(100) null,
item_11 varchar(100) null,
item_12 varchar(100) null,
item_13 varchar(100) null,
item_14 varchar(100) null,
item_15 varchar(100) null,
item_16 varchar(100) null,
item_17 varchar(100) null,
item_18 varchar(100) null,
d_from varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


/***********************************************  
 *
 * warehouse - shipment form 出貨單 (轉倉到豐田外倉) 
 *
 ***********************************************/
create table w_shipment_form(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_time time null,
c_d_time datetime null,
o_p_no varchar(10) null,
ord_date varchar(20) null,
ship_date varchar(20) null,
ord_no varchar(20) null,
cust_id varchar(20) null,
cust_name varchar(100) null,
ship_address varchar(200) null,
cnt_tel varchar(40) null,
remark varchar(300) null,
wh_id varchar(10) null,
ord_no2 varchar(20) null,
desp varchar(100) null,
lot_no varchar(20) null,
expire_no varchar(20) null,
qty_amount varchar(10) null,
po varchar(100) null,
d_from varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************* 
 *
 * work_record
 *
 *************************/
create table work_record(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_time time null,
c_d_time datetime null,
kind varchar(300) null,
title varchar(300) null,
content text null,
c_state varchar(30) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************* 
 *
 * spam_maillog
 *
 *************************/
create table spam_maillog(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_time time null,
c_d_time datetime null,
a_mail varchar(200) null,
spam_log text null 
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************* 
 *
 * otsuka_vmware
 *
 *************************/
create table otsuka_vmware(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_time time null,
c_d_time datetime null,
vm_position varchar(50) null , 
vm_name varchar(50) null ,  
vm_power varchar(10) null , 
vm_os varchar(50) null , 
vm_os_state varchar(20) null , 
vm_state varchar(50) null , 
vm_boot_time varchar(100) null , 
vm_ip varchar(50) null , 
vm_cpu varchar(50) null , 
vm_ram varchar(50) null , 
vm_hdd text null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************* 
 *
 * otsuka_contract
 *
 *************************/
create table otsuka_contract(
no int not null primary key AUTO_INCREMENT,
b_date Date null,
kind varchar(20) null , 
title varchar(200) null , 
cost varchar(30) null , 
t_s_e varchar(100) null , 
company varchar(20) null , 
comment varchar(100) null 
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*************************** 
 *
 * factory_monitor_device
 *
 ***************************/
create table factory_monitor_device(
no int not null primary key AUTO_INCREMENT,
d_name varchar(50) null,
d_c_name varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
insert into factory_monitor_device(d_name , d_c_name) value('S-1','製品倉庫(一)25°C');
insert into factory_monitor_device(d_name , d_c_name) value('S-2','製品倉庫(一)30°C');
insert into factory_monitor_device(d_name , d_c_name) value('S-3','原料庫(一)');
insert into factory_monitor_device(d_name , d_c_name) value('S-4','製品倉庫(三)30° C');
insert into factory_monitor_device(d_name , d_c_name) value('S-5','原料庫(三)30° B');
insert into factory_monitor_device(d_name , d_c_name) value('S-6','製品倉庫(三)25° C');
insert into factory_monitor_device(d_name , d_c_name) value('S-7','原料庫(三)30° A');
insert into factory_monitor_device(d_name , d_c_name) value('S-8','製品倉庫(二)');
insert into factory_monitor_device(d_name , d_c_name) value('S-9','原料庫(二)');
insert into factory_monitor_device(d_name , d_c_name) value('S-10','物料倉庫');
insert into factory_monitor_device(d_name , d_c_name) value('S-11-1','樣品室-1(25°C)');
insert into factory_monitor_device(d_name , d_c_name) value('S-11-2','樣品室-1(冰箱)');
insert into factory_monitor_device(d_name , d_c_name) value('S-12','樣品室-2(20°C)');
insert into factory_monitor_device(d_name , d_c_name) value('S-13','樣品室-3(30°C)');
insert into factory_monitor_device(d_name , d_c_name) value('S-14','退貨品倉庫');
insert into factory_monitor_device(d_name , d_c_name) value('S-15-1','安全性實驗箱-1');
insert into factory_monitor_device(d_name , d_c_name) value('S-15-2','安全性實驗箱-2');
insert into factory_monitor_device(d_name , d_c_name) value('S-15-3','安全性實驗箱-3');
insert into factory_monitor_device(d_name , d_c_name) value('S-15-4','安全性實驗箱-4');
insert into factory_monitor_device(d_name , d_c_name) value('S-15-5','安全性實驗箱-5');
insert into factory_monitor_device(d_name , d_c_name) value('S-15-6','安全性實驗箱-6');
insert into factory_monitor_device(d_name , d_c_name) value('S-16','中間品室');
insert into factory_monitor_device(d_name , d_c_name) value('S-17','製品三倉-溫度');
insert into factory_monitor_device(d_name , d_c_name) value('S-18','製品二倉-溫度');
insert into factory_monitor_device(d_name , d_c_name) value('S-19','安定性試驗室');

/************************
 *
 * check_device_record
 *
 ************************/
create table check_device_record(
no int not null primary key AUTO_INCREMENT,
r_date date null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
d_os varchar(30) null,
d_status varchar(30) null,
d_name varchar(30) null,
d_client_security_status varchar(30) null,
d_patch_status varchar(30) null,
d_available_patches_count varchar(30) null,
d_customer varchar(30) null,
d_group varchar(30) null,
d_last_logged_in_user varchar(100) null,
d_owner varchar(30) null,
d_last_activity varchar(100) null,
d_os_name varchar(100) null,
d_os_version varchar(30) null,
d_ccs_version varchar(30) null,
d_ccc_version varchar(40) null,
d_external_ip varchar(50) null,
d_internal_ip varchar(50) null,
d_ad_ldap varchar(30) null,
d_domain_workgroup varchar(50) null,
d_model varchar(50) null,
d_process varchar(50) null,
d_serial_num varchar(50) null,
d_system_model varchar(50) null,
d_system_manufacturer varchar(50) null,
d_ownership_type varchar(50) null,
d_registered varchar(50) null,
d_local_time_zone varchar(50) null,
d_service_pack varchar(50) null,
d_reboot_time varchar(50) null,
d_reboot_reason text null,
d_cpu_usage varchar(10) null,
d_cpu_frequency varchar(10) null,
d_ram_usage_1 varchar(10) null,
d_ram_usage_2 varchar(10) null,
d_total_ram varchar(10) null,
d_network_usage text null,
d_disk_free_GB varchar(30) null,
d_disk_used_GB varchar(30) null,
d_security_profiles varchar(30) null,
d_tags varchar(30) null,
d_notes varchar(30) null

)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/**************
 *
 * device_list
 *
 **************/
create table device_list(
no int not null primary key AUTO_INCREMENT,
r_date date null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
r_now_time varchar(10) null,
os varchar(50) null,
d_status varchar(50) null,
d_name varchar(50) null,
c_s_status varchar(50) null,
p_status varchar(50) null,
a_p_count varchar(10) null,
customer varchar(10) null,
d_group varchar(100) null,
l_l_i_user varchar(50) null,
d_owner varchar(50) null,
l_activity varchar(100) null,
o_name varchar(100) null,
o_ver varchar(50) null,
ccs_ver varchar(50) null,
ccc_ver varchar(50) null,
e_ip varchar(200) null,
i_ip varchar(200) null,
a_ldap varchar(50) null,
d_workgroup varchar(50) null,
model varchar(50) null,
processor varchar(100) null,
s_number varchar(100) null,
s_model varchar(100) null,
s_manu varchar(100) null,
o_type varchar(100) null,
registered varchar(100) null,
l_t_zone varchar(100) null,
s_pack varchar(100) null,
r_time varchar(100) null,
r_reason text null,
cpu_usage varchar(300) null,
ram_usage varchar(300) null,
net_usage varchar(300) null,
disk_usage varchar(300) null,
s_profiles varchar(100) null

)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/********************
 *
 * day_money_oil
 *
 ********************/
create table day_money_oil(
no int not null primary key AUTO_INCREMENT,
r_date date null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
f_name varchar(30) null,
a_name varchar(30) null,
e_name varchar(40) null,
d_name varchar(40) null,
t_money varchar(40) null,
c_t_money varchar(40) null,
erp_num varchar(40) null,
form_num varchar(40) null,
day_r_date date null,
day_r_year varchar(10) null,
day_r_month varchar(10) null,
day_t_money varchar(40) null DEFAULT 0,
day_t_money1 varchar(40) null DEFAULT 0,
day_t_money2 varchar(40) null DEFAULT 0,
day_t_money3 varchar(40) null DEFAULT 0,
day_t_money4 varchar(40) null DEFAULT 0,
day_t_money5 varchar(40) null DEFAULT 0,
day_t_money6 varchar(40) null DEFAULT 0,
day_t_money7 varchar(40) null DEFAULT 0,
day_t_money8 varchar(40) null DEFAULT 0,
day_t_money9 varchar(40) null DEFAULT 0,
day_t_money10 varchar(40) null DEFAULT 0,
day_t_money11 varchar(40) null DEFAULT 0,
day_t_money12 varchar(40) null DEFAULT 0,
day_t_money13 varchar(40) null DEFAULT 0,
day_t_money14 varchar(40) null DEFAULT 0,
day_t_money15 varchar(40) null DEFAULT 0,
day_t_money16 varchar(40) null DEFAULT 0,
day_t_money17 varchar(40) null DEFAULT 0,
day_t_money18 varchar(40) null DEFAULT 0,
day_t_money19 varchar(40) null DEFAULT 0,
day_t_money20 varchar(40) null DEFAULT 0,
day_t_money21 varchar(40) null DEFAULT 0,
day_t_money22 varchar(40) null DEFAULT 0,
day_t_money23 varchar(40) null DEFAULT 0,
day_t_money24 varchar(40) null DEFAULT 0,
day_t_money25 varchar(40) null DEFAULT 0,
day_t_money26 varchar(40) null DEFAULT 0,
day_t_money27 varchar(40) null DEFAULT 0,
day_t_money28 varchar(40) null DEFAULT 0,
day_t_money29 varchar(40) null DEFAULT 0,
day_t_money30 varchar(40) null DEFAULT 0,
day_t_money31 varchar(40) null DEFAULT 0,
day_t_total varchar(40) null DEFAULT 0,
day_money_mark text null,
day_money_diff varchar(40) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/********************
 *
 * day_money_other
 *
 ********************/
create table day_money_other(
no int not null primary key AUTO_INCREMENT,
r_date date null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
f_name varchar(30) null,
a_name varchar(30) null,
e_name varchar(40) null,
d_name varchar(40) null,
t_money varchar(40) null,
c_t_money varchar(40) null,
erp_num varchar(40) null,
form_num varchar(40) null,
day_r_date date null,
day_r_year varchar(10) null,
day_r_month varchar(10) null,
day_t_money varchar(40) null DEFAULT 0,
day_t_money1 varchar(40) null DEFAULT 0,
day_t_money2 varchar(40) null DEFAULT 0,
day_t_money3 varchar(40) null DEFAULT 0,
day_t_money4 varchar(40) null DEFAULT 0,
day_t_money5 varchar(40) null DEFAULT 0,
day_t_money6 varchar(40) null DEFAULT 0,
day_t_money7 varchar(40) null DEFAULT 0,
day_t_money8 varchar(40) null DEFAULT 0,
day_t_money9 varchar(40) null DEFAULT 0,
day_t_money10 varchar(40) null DEFAULT 0,
day_t_money11 varchar(40) null DEFAULT 0,
day_t_money12 varchar(40) null DEFAULT 0,
day_t_money13 varchar(40) null DEFAULT 0,
day_t_money14 varchar(40) null DEFAULT 0,
day_t_money15 varchar(40) null DEFAULT 0,
day_t_money16 varchar(40) null DEFAULT 0,
day_t_money17 varchar(40) null DEFAULT 0,
day_t_money18 varchar(40) null DEFAULT 0,
day_t_money19 varchar(40) null DEFAULT 0,
day_t_money20 varchar(40) null DEFAULT 0,
day_t_money21 varchar(40) null DEFAULT 0,
day_t_money22 varchar(40) null DEFAULT 0,
day_t_money23 varchar(40) null DEFAULT 0,
day_t_money24 varchar(40) null DEFAULT 0,
day_t_money25 varchar(40) null DEFAULT 0,
day_t_money26 varchar(40) null DEFAULT 0,
day_t_money27 varchar(40) null DEFAULT 0,
day_t_money28 varchar(40) null DEFAULT 0,
day_t_money29 varchar(40) null DEFAULT 0,
day_t_money30 varchar(40) null DEFAULT 0,
day_t_money31 varchar(40) null DEFAULT 0,
day_t_total varchar(40) null DEFAULT 0,
day_money_mark text null,
day_money_diff varchar(40) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/********************
 *
 * day_money_stay
 *
 ********************/
create table day_money_stay(
no int not null primary key AUTO_INCREMENT,
r_date date null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
f_name varchar(30) null,
a_name varchar(30) null,
e_name varchar(40) null,
d_name varchar(40) null,
t_money varchar(40) null,
c_t_money varchar(40) null,
erp_num varchar(40) null,
form_num varchar(40) null,
day_r_date date null,
day_r_year varchar(10) null,
day_r_month varchar(10) null,
day_t_money varchar(40) null DEFAULT 0,
day_t_money1 varchar(40) null DEFAULT 0,
day_t_money2 varchar(40) null DEFAULT 0,
day_t_money3 varchar(40) null DEFAULT 0,
day_t_money4 varchar(40) null DEFAULT 0,
day_t_money5 varchar(40) null DEFAULT 0,
day_t_money6 varchar(40) null DEFAULT 0,
day_t_money7 varchar(40) null DEFAULT 0,
day_t_money8 varchar(40) null DEFAULT 0,
day_t_money9 varchar(40) null DEFAULT 0,
day_t_money10 varchar(40) null DEFAULT 0,
day_t_money11 varchar(40) null DEFAULT 0,
day_t_money12 varchar(40) null DEFAULT 0,
day_t_money13 varchar(40) null DEFAULT 0,
day_t_money14 varchar(40) null DEFAULT 0,
day_t_money15 varchar(40) null DEFAULT 0,
day_t_money16 varchar(40) null DEFAULT 0,
day_t_money17 varchar(40) null DEFAULT 0,
day_t_money18 varchar(40) null DEFAULT 0,
day_t_money19 varchar(40) null DEFAULT 0,
day_t_money20 varchar(40) null DEFAULT 0,
day_t_money21 varchar(40) null DEFAULT 0,
day_t_money22 varchar(40) null DEFAULT 0,
day_t_money23 varchar(40) null DEFAULT 0,
day_t_money24 varchar(40) null DEFAULT 0,
day_t_money25 varchar(40) null DEFAULT 0,
day_t_money26 varchar(40) null DEFAULT 0,
day_t_money27 varchar(40) null DEFAULT 0,
day_t_money28 varchar(40) null DEFAULT 0,
day_t_money29 varchar(40) null DEFAULT 0,
day_t_money30 varchar(40) null DEFAULT 0,
day_t_money31 varchar(40) null DEFAULT 0,
day_t_total varchar(40) null DEFAULT 0,
day_money_mark text null,
day_money_diff varchar(40) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/********************
 *
 * day_money_taxi
 *
 ********************/
create table day_money_taxi(
no int not null primary key AUTO_INCREMENT,
r_date date null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
f_name varchar(30) null,
a_name varchar(30) null,
e_name varchar(40) null,
d_name varchar(40) null,
t_money varchar(40) null,
c_t_money varchar(40) null,
erp_num varchar(40) null,
form_num varchar(40) null,
day_r_date date null,
day_r_year varchar(10) null,
day_r_month varchar(10) null,
day_t_money varchar(40) null DEFAULT 0,
day_t_money1 varchar(40) null DEFAULT 0,
day_t_money2 varchar(40) null DEFAULT 0,
day_t_money3 varchar(40) null DEFAULT 0,
day_t_money4 varchar(40) null DEFAULT 0,
day_t_money5 varchar(40) null DEFAULT 0,
day_t_money6 varchar(40) null DEFAULT 0,
day_t_money7 varchar(40) null DEFAULT 0,
day_t_money8 varchar(40) null DEFAULT 0,
day_t_money9 varchar(40) null DEFAULT 0,
day_t_money10 varchar(40) null DEFAULT 0,
day_t_money11 varchar(40) null DEFAULT 0,
day_t_money12 varchar(40) null DEFAULT 0,
day_t_money13 varchar(40) null DEFAULT 0,
day_t_money14 varchar(40) null DEFAULT 0,
day_t_money15 varchar(40) null DEFAULT 0,
day_t_money16 varchar(40) null DEFAULT 0,
day_t_money17 varchar(40) null DEFAULT 0,
day_t_money18 varchar(40) null DEFAULT 0,
day_t_money19 varchar(40) null DEFAULT 0,
day_t_money20 varchar(40) null DEFAULT 0,
day_t_money21 varchar(40) null DEFAULT 0,
day_t_money22 varchar(40) null DEFAULT 0,
day_t_money23 varchar(40) null DEFAULT 0,
day_t_money24 varchar(40) null DEFAULT 0,
day_t_money25 varchar(40) null DEFAULT 0,
day_t_money26 varchar(40) null DEFAULT 0,
day_t_money27 varchar(40) null DEFAULT 0,
day_t_money28 varchar(40) null DEFAULT 0,
day_t_money29 varchar(40) null DEFAULT 0,
day_t_money30 varchar(40) null DEFAULT 0,
day_t_money31 varchar(40) null DEFAULT 0,
day_t_total varchar(40) null DEFAULT 0,
day_money_mark text null,
day_money_diff varchar(40) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/********************
 *
 * day_money_trick
 *
 ********************/
create table day_money_trick(
no int not null primary key AUTO_INCREMENT,
r_date date null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
f_name varchar(30) null,
a_name varchar(30) null,
e_name varchar(40) null,
d_name varchar(40) null,
t_money varchar(40) null,
c_t_money varchar(40) null,
erp_num varchar(40) null,
form_num varchar(40) null,
day_r_date date null,
day_r_year varchar(10) null,
day_r_month varchar(10) null,
day_t_money varchar(40) null DEFAULT 0,
day_t_money1 varchar(40) null DEFAULT 0,
day_t_money2 varchar(40) null DEFAULT 0,
day_t_money3 varchar(40) null DEFAULT 0,
day_t_money4 varchar(40) null DEFAULT 0,
day_t_money5 varchar(40) null DEFAULT 0,
day_t_money6 varchar(40) null DEFAULT 0,
day_t_money7 varchar(40) null DEFAULT 0,
day_t_money8 varchar(40) null DEFAULT 0,
day_t_money9 varchar(40) null DEFAULT 0,
day_t_money10 varchar(40) null DEFAULT 0,
day_t_money11 varchar(40) null DEFAULT 0,
day_t_money12 varchar(40) null DEFAULT 0,
day_t_money13 varchar(40) null DEFAULT 0,
day_t_money14 varchar(40) null DEFAULT 0,
day_t_money15 varchar(40) null DEFAULT 0,
day_t_money16 varchar(40) null DEFAULT 0,
day_t_money17 varchar(40) null DEFAULT 0,
day_t_money18 varchar(40) null DEFAULT 0,
day_t_money19 varchar(40) null DEFAULT 0,
day_t_money20 varchar(40) null DEFAULT 0,
day_t_money21 varchar(40) null DEFAULT 0,
day_t_money22 varchar(40) null DEFAULT 0,
day_t_money23 varchar(40) null DEFAULT 0,
day_t_money24 varchar(40) null DEFAULT 0,
day_t_money25 varchar(40) null DEFAULT 0,
day_t_money26 varchar(40) null DEFAULT 0,
day_t_money27 varchar(40) null DEFAULT 0,
day_t_money28 varchar(40) null DEFAULT 0,
day_t_money29 varchar(40) null DEFAULT 0,
day_t_money30 varchar(40) null DEFAULT 0,
day_t_money31 varchar(40) null DEFAULT 0,
day_t_total varchar(40) null DEFAULT 0,
day_money_mark text null,
day_money_diff varchar(40) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/********************
 *
 * day_money_tolls
 *
 ********************/
create table day_money_tolls(
no int not null primary key AUTO_INCREMENT,
r_date date null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
f_name varchar(30) null,
a_name varchar(30) null,
e_name varchar(40) null,
d_name varchar(40) null,
t_money varchar(40) null,
c_t_money varchar(40) null,
erp_num varchar(40) null,
form_num varchar(40) null,
day_r_date date null,
day_r_year varchar(10) null,
day_r_month varchar(10) null,
day_t_money varchar(40) null DEFAULT 0,
day_t_money1 varchar(40) null DEFAULT 0,
day_t_money2 varchar(40) null DEFAULT 0,
day_t_money3 varchar(40) null DEFAULT 0,
day_t_money4 varchar(40) null DEFAULT 0,
day_t_money5 varchar(40) null DEFAULT 0,
day_t_money6 varchar(40) null DEFAULT 0,
day_t_money7 varchar(40) null DEFAULT 0,
day_t_money8 varchar(40) null DEFAULT 0,
day_t_money9 varchar(40) null DEFAULT 0,
day_t_money10 varchar(40) null DEFAULT 0,
day_t_money11 varchar(40) null DEFAULT 0,
day_t_money12 varchar(40) null DEFAULT 0,
day_t_money13 varchar(40) null DEFAULT 0,
day_t_money14 varchar(40) null DEFAULT 0,
day_t_money15 varchar(40) null DEFAULT 0,
day_t_money16 varchar(40) null DEFAULT 0,
day_t_money17 varchar(40) null DEFAULT 0,
day_t_money18 varchar(40) null DEFAULT 0,
day_t_money19 varchar(40) null DEFAULT 0,
day_t_money20 varchar(40) null DEFAULT 0,
day_t_money21 varchar(40) null DEFAULT 0,
day_t_money22 varchar(40) null DEFAULT 0,
day_t_money23 varchar(40) null DEFAULT 0,
day_t_money24 varchar(40) null DEFAULT 0,
day_t_money25 varchar(40) null DEFAULT 0,
day_t_money26 varchar(40) null DEFAULT 0,
day_t_money27 varchar(40) null DEFAULT 0,
day_t_money28 varchar(40) null DEFAULT 0,
day_t_money29 varchar(40) null DEFAULT 0,
day_t_money30 varchar(40) null DEFAULT 0,
day_t_money31 varchar(40) null DEFAULT 0,
day_t_total varchar(40) null DEFAULT 0,
day_money_mark text null,
day_money_diff varchar(40) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/**************************
 *
 * day_money_parking_fee
 *
 **************************/
create table day_money_parking_fee(
no int not null primary key AUTO_INCREMENT,
r_date date null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
f_name varchar(30) null,
a_name varchar(30) null,
e_name varchar(40) null,
d_name varchar(40) null,
t_money varchar(40) null,
c_t_money varchar(40) null,
erp_num varchar(40) null,
form_num varchar(40) null,
day_r_date date null,
day_r_year varchar(10) null,
day_r_month varchar(10) null,
day_t_money varchar(40) null DEFAULT 0,
day_t_money1 varchar(40) null DEFAULT 0,
day_t_money2 varchar(40) null DEFAULT 0,
day_t_money3 varchar(40) null DEFAULT 0,
day_t_money4 varchar(40) null DEFAULT 0,
day_t_money5 varchar(40) null DEFAULT 0,
day_t_money6 varchar(40) null DEFAULT 0,
day_t_money7 varchar(40) null DEFAULT 0,
day_t_money8 varchar(40) null DEFAULT 0,
day_t_money9 varchar(40) null DEFAULT 0,
day_t_money10 varchar(40) null DEFAULT 0,
day_t_money11 varchar(40) null DEFAULT 0,
day_t_money12 varchar(40) null DEFAULT 0,
day_t_money13 varchar(40) null DEFAULT 0,
day_t_money14 varchar(40) null DEFAULT 0,
day_t_money15 varchar(40) null DEFAULT 0,
day_t_money16 varchar(40) null DEFAULT 0,
day_t_money17 varchar(40) null DEFAULT 0,
day_t_money18 varchar(40) null DEFAULT 0,
day_t_money19 varchar(40) null DEFAULT 0,
day_t_money20 varchar(40) null DEFAULT 0,
day_t_money21 varchar(40) null DEFAULT 0,
day_t_money22 varchar(40) null DEFAULT 0,
day_t_money23 varchar(40) null DEFAULT 0,
day_t_money24 varchar(40) null DEFAULT 0,
day_t_money25 varchar(40) null DEFAULT 0,
day_t_money26 varchar(40) null DEFAULT 0,
day_t_money27 varchar(40) null DEFAULT 0,
day_t_money28 varchar(40) null DEFAULT 0,
day_t_money29 varchar(40) null DEFAULT 0,
day_t_money30 varchar(40) null DEFAULT 0,
day_t_money31 varchar(40) null DEFAULT 0,
day_t_total varchar(40) null DEFAULT 0,
day_money_mark text null,
day_money_diff varchar(40) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/***************************
 *
 * day_money_over_traffic
 *
 ***************************/
create table day_money_over_traffic(
no int not null primary key AUTO_INCREMENT,
r_date date null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
f_name varchar(30) null,
a_name varchar(30) null,
e_name varchar(40) null,
d_name varchar(40) null,
t_money varchar(40) null,
c_t_money varchar(40) null,
erp_num varchar(40) null,
form_num varchar(40) null,
day_r_date date null,
day_r_year varchar(10) null,
day_r_month varchar(10) null,
day_t_money varchar(40) null DEFAULT 0,
day_t_money1 varchar(40) null DEFAULT 0,
day_t_money2 varchar(40) null DEFAULT 0,
day_t_money3 varchar(40) null DEFAULT 0,
day_t_money4 varchar(40) null DEFAULT 0,
day_t_money5 varchar(40) null DEFAULT 0,
day_t_money6 varchar(40) null DEFAULT 0,
day_t_money7 varchar(40) null DEFAULT 0,
day_t_money8 varchar(40) null DEFAULT 0,
day_t_money9 varchar(40) null DEFAULT 0,
day_t_money10 varchar(40) null DEFAULT 0,
day_t_money11 varchar(40) null DEFAULT 0,
day_t_money12 varchar(40) null DEFAULT 0,
day_t_money13 varchar(40) null DEFAULT 0,
day_t_money14 varchar(40) null DEFAULT 0,
day_t_money15 varchar(40) null DEFAULT 0,
day_t_money16 varchar(40) null DEFAULT 0,
day_t_money17 varchar(40) null DEFAULT 0,
day_t_money18 varchar(40) null DEFAULT 0,
day_t_money19 varchar(40) null DEFAULT 0,
day_t_money20 varchar(40) null DEFAULT 0,
day_t_money21 varchar(40) null DEFAULT 0,
day_t_money22 varchar(40) null DEFAULT 0,
day_t_money23 varchar(40) null DEFAULT 0,
day_t_money24 varchar(40) null DEFAULT 0,
day_t_money25 varchar(40) null DEFAULT 0,
day_t_money26 varchar(40) null DEFAULT 0,
day_t_money27 varchar(40) null DEFAULT 0,
day_t_money28 varchar(40) null DEFAULT 0,
day_t_money29 varchar(40) null DEFAULT 0,
day_t_money30 varchar(40) null DEFAULT 0,
day_t_money31 varchar(40) null DEFAULT 0,
day_t_total varchar(40) null DEFAULT 0,
day_money_mark text null,
day_money_diff varchar(40) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/**********************
 *
 * day_money_traffic
 *
 **********************/
create table day_money_traffic(
no int not null primary key AUTO_INCREMENT,
r_date date null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
f_name varchar(30) null,
a_name varchar(30) null,
e_name varchar(40) null,
d_name varchar(40) null,
t_money varchar(40) null,
c_t_money varchar(40) null,
erp_num varchar(40) null,
form_num varchar(40) null,
day_r_date date null,
day_r_year varchar(10) null,
day_r_month varchar(10) null,
day_t_money varchar(40) null DEFAULT 0,
day_t_money1 varchar(40) null DEFAULT 0,
day_t_money2 varchar(40) null DEFAULT 0,
day_t_money3 varchar(40) null DEFAULT 0,
day_t_money4 varchar(40) null DEFAULT 0,
day_t_money5 varchar(40) null DEFAULT 0,
day_t_money6 varchar(40) null DEFAULT 0,
day_t_money7 varchar(40) null DEFAULT 0,
day_t_money8 varchar(40) null DEFAULT 0,
day_t_money9 varchar(40) null DEFAULT 0,
day_t_money10 varchar(40) null DEFAULT 0,
day_t_money11 varchar(40) null DEFAULT 0,
day_t_money12 varchar(40) null DEFAULT 0,
day_t_money13 varchar(40) null DEFAULT 0,
day_t_money14 varchar(40) null DEFAULT 0,
day_t_money15 varchar(40) null DEFAULT 0,
day_t_money16 varchar(40) null DEFAULT 0,
day_t_money17 varchar(40) null DEFAULT 0,
day_t_money18 varchar(40) null DEFAULT 0,
day_t_money19 varchar(40) null DEFAULT 0,
day_t_money20 varchar(40) null DEFAULT 0,
day_t_money21 varchar(40) null DEFAULT 0,
day_t_money22 varchar(40) null DEFAULT 0,
day_t_money23 varchar(40) null DEFAULT 0,
day_t_money24 varchar(40) null DEFAULT 0,
day_t_money25 varchar(40) null DEFAULT 0,
day_t_money26 varchar(40) null DEFAULT 0,
day_t_money27 varchar(40) null DEFAULT 0,
day_t_money28 varchar(40) null DEFAULT 0,
day_t_money29 varchar(40) null DEFAULT 0,
day_t_money30 varchar(40) null DEFAULT 0,
day_t_money31 varchar(40) null DEFAULT 0,
day_t_total varchar(40) null DEFAULT 0,
day_money_mark text null,
day_money_diff varchar(40) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/**************
 *
 * day_money
 *
 **************/
create table day_money(
no int not null primary key AUTO_INCREMENT,
r_date date null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
f_name varchar(30) null,
a_name varchar(30) null,
e_name varchar(40) null,
d_name varchar(40) null,
t_money varchar(40) null,
c_t_money varchar(40) null,
erp_num varchar(40) null,
form_num varchar(40) null,
day_r_date date null,
day_r_year varchar(10) null,
day_r_month varchar(10) null,
day_t_money varchar(40) null DEFAULT 0,
day_t_money1 varchar(40) null DEFAULT 0,
day_t_money2 varchar(40) null DEFAULT 0,
day_t_money3 varchar(40) null DEFAULT 0,
day_t_money4 varchar(40) null DEFAULT 0,
day_t_money5 varchar(40) null DEFAULT 0,
day_t_money6 varchar(40) null DEFAULT 0,
day_t_money7 varchar(40) null DEFAULT 0,
day_t_money8 varchar(40) null DEFAULT 0,
day_t_money9 varchar(40) null DEFAULT 0,
day_t_money10 varchar(40) null DEFAULT 0,
day_t_money11 varchar(40) null DEFAULT 0,
day_t_money12 varchar(40) null DEFAULT 0,
day_t_money13 varchar(40) null DEFAULT 0,
day_t_money14 varchar(40) null DEFAULT 0,
day_t_money15 varchar(40) null DEFAULT 0,
day_t_money16 varchar(40) null DEFAULT 0,
day_t_money17 varchar(40) null DEFAULT 0,
day_t_money18 varchar(40) null DEFAULT 0,
day_t_money19 varchar(40) null DEFAULT 0,
day_t_money20 varchar(40) null DEFAULT 0,
day_t_money21 varchar(40) null DEFAULT 0,
day_t_money22 varchar(40) null DEFAULT 0,
day_t_money23 varchar(40) null DEFAULT 0,
day_t_money24 varchar(40) null DEFAULT 0,
day_t_money25 varchar(40) null DEFAULT 0,
day_t_money26 varchar(40) null DEFAULT 0,
day_t_money27 varchar(40) null DEFAULT 0,
day_t_money28 varchar(40) null DEFAULT 0,
day_t_money29 varchar(40) null DEFAULT 0,
day_t_money30 varchar(40) null DEFAULT 0,
day_t_money31 varchar(40) null DEFAULT 0,
day_t_total varchar(40) null DEFAULT 0,
day_money_mark text null,
day_money_diff varchar(40) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


/************************* 
 *
 * in_out_20230920
 *
 *************************/
create table in_out_20230920(
no int not null primary key AUTO_INCREMENT,
r_date varchar(20) null,
r_time varchar(20) null,
d_id varchar(50) null,
d_name varchar(50) null,
e_id varchar(50) null,
e_name varchar(50) null,
p_id varchar(50) null,
p_name varchar(50) null,
c_id varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************* 
 *
 * factory_hr_a
 *
 *************************/
create table factory_hr_a(
no int not null primary key AUTO_INCREMENT,
d_name varchar(50) null,
d_id varchar(50) null,
d_name2 varchar(50) null,
e_id varchar(50) null,
e_name varchar(50) null,
l_account varchar(50) null,
sex varchar(50) null,
j_name varchar(50) null,
j_date varchar(50) null,
email varchar(200) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************* 
 *
 * card_reader_position
 *
 *************************/
create table card_reader_p(
no int not null primary key AUTO_INCREMENT,
p_id int null,
p_name varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/***************** 
 *
 * work_time
 *
 *****************/
create table work_time(
no int not null primary key AUTO_INCREMENT,
e_id int null,
e_name varchar(50) null,
dep_id varchar(10) null,
b_date varchar(30) null , 
r_year varchar(10) null , 
r_month varchar(10) null , 
r_day varchar(10) null , 
total_time varchar(50) null,
normal_time varchar(50) null,
over_time varchar(50) null,
availability_time varchar(50) null,

w_s_1 varchar(100) null,
w_s_1_product varchar(100) null,
w_s_1_num varchar(100) null,
w_s_1_normal_time varchar(100) null,
w_s_1_over_time varchar(100) null,
w_s_1_avail_time varchar(100) null,
w_s_1_remark varchar(100) null,

w_s_2 varchar(100) null,
w_s_2_product varchar(100) null,
w_s_2_num varchar(100) null,
w_s_2_normal_time varchar(100) null,
w_s_2_over_time varchar(100) null,
w_s_2_avail_time varchar(100) null,
w_s_2_remark varchar(100) null,

w_s_3 varchar(100) null,
w_s_3_product varchar(100) null,
w_s_3_num varchar(100) null,
w_s_3_normal_time varchar(100) null,
w_s_3_over_time varchar(100) null,
w_s_3_avail_time varchar(100) null,
w_s_3_remark varchar(100) null,

w_s_4 varchar(100) null,
w_s_4_product varchar(100) null,
w_s_4_num varchar(100) null,
w_s_4_normal_time varchar(100) null,
w_s_4_over_time varchar(100) null,
w_s_4_avail_time varchar(100) null,
w_s_4_remark varchar(100) null,

w_s_5 varchar(100) null,
w_s_5_product varchar(100) null,
w_s_5_num varchar(100) null,
w_s_5_normal_time varchar(100) null,
w_s_5_over_time varchar(100) null,
w_s_5_avail_time varchar(100) null,
w_s_5_remark varchar(100) null,

w_s_6 varchar(100) null,
w_s_6_product varchar(100) null,
w_s_6_num varchar(100) null,
w_s_6_normal_time varchar(100) null,
w_s_6_over_time varchar(100) null,
w_s_6_avail_time varchar(100) null,
w_s_6_remark varchar(100) null,

w_s_7 varchar(100) null,
w_s_7_product varchar(100) null,
w_s_7_num varchar(100) null,
w_s_7_normal_time varchar(100) null,
w_s_7_over_time varchar(100) null,
w_s_7_avail_time varchar(100) null,
w_s_7_remark varchar(100) null,

w_s_8 varchar(100) null,
w_s_8_product varchar(100) null,
w_s_8_num varchar(100) null,
w_s_8_normal_time varchar(100) null,
w_s_8_over_time varchar(100) null,
w_s_8_avail_time varchar(100) null,
w_s_8_remark varchar(100) null,

w_s_9 varchar(100) null,
w_s_9_product varchar(100) null,
w_s_9_num varchar(100) null,
w_s_9_normal_time varchar(100) null,
w_s_9_over_time varchar(100) null,
w_s_9_avail_time varchar(100) null,
w_s_9_remark varchar(100) null,

w_s_10 varchar(100) null,
w_s_10_product varchar(100) null,
w_s_10_num varchar(100) null,
w_s_10_normal_time varchar(100) null,
w_s_10_over_time varchar(100) null,
w_s_10_avail_time varchar(100) null,
w_s_10_remark varchar(100) null,

w_s_11 varchar(100) null,
w_s_11_product varchar(100) null,
w_s_11_num varchar(100) null,
w_s_11_normal_time varchar(100) null,
w_s_11_over_time varchar(100) null,
w_s_11_avail_time varchar(100) null,
w_s_11_remark varchar(100) null,

w_s_12 varchar(100) null,
w_s_12_product varchar(100) null,
w_s_12_num varchar(100) null,
w_s_12_normal_time varchar(100) null,
w_s_12_over_time varchar(100) null,
w_s_12_avail_time varchar(100) null,
w_s_12_remark varchar(100) null

)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/***************** 
 *
 * check_member
 *
 *****************/
create table check_member(
no int not null primary key AUTO_INCREMENT,
employee_id int null,
employee_name varchar(50) null,
department_id varchar(50) null,
department_name varchar(50) null,
b_date varchar(10) null , 
end_date varchar(10) null,
check_year varchar(10) null,
check_month varchar(10) null,
self_item_1_1 int null,
self_item_1_2 int null,
self_item_1_3 int null,
self_item_1_4 int null,
other_item_1_1 int null,
other_item_1_2 int null,
other_item_1_3 int null,
other_item_1_4 int null,
sir_item_1_1 int null,
sir_item_1_2 int null,
sir_item_1_3 int null,
sir_item_1_4 int null,

self_item_2_1 int null,
self_item_2_2 int null,
self_item_2_3 int null,
other_item_2_1 int null,
other_item_2_2 int null,
other_item_2_3 int null,
sir_item_2_1 int null,
sir_item_2_2 int null,
sir_item_2_3 int null,

self_item_3_1 int null,
self_item_3_2 int null,
self_item_3_3 int null,
other_item_3_1 int null,
other_item_3_2 int null,
other_item_3_3 int null,
sir_item_3_1 int null,
sir_item_3_2 int null,
sir_item_3_3 int null,

self_item_4_1 int null,
self_item_4_2 int null,
self_item_4_3 int null,
self_item_4_4 int null,
other_item_4_1 int null,
other_item_4_2 int null,
other_item_4_3 int null,
other_item_4_4 int null,
sir_item_4_1 int null,
sir_item_4_2 int null,
sir_item_4_3 int null,
sir_item_4_4 int null,

self_item_5_1 int null,
self_item_5_2 int null,
self_item_5_3 int null,
other_item_5_1 int null,
other_item_5_2 int null,
other_item_5_3 int null,
sir_item_5_1 int null,
sir_item_5_2 int null,
sir_item_5_3 int null,

self_item_6_1 int null,
self_item_6_2 int null,
self_item_6_3 int null,
other_item_6_1 int null,
other_item_6_2 int null,
other_item_6_3 int null,
sir_item_6_1 int null,
sir_item_6_2 int null,
sir_item_6_3 int null,

sir_item_7_1 int null,
sir_item_7_2 int null,
sir_item_7_3 int null,
sir_item_7_4 int null,

sir_item_8_1 int null,
sir_item_8_2 int null,
sir_item_8_3 int null,
sir_item_8_4 int null,
sir_item_8_5 int null,

comment text null,

self_total int null,
other_total int null,
sir_total int null,
other_plus_total int null,
final_total int null,
final_comment text null,

self_check varchar(5) null,
other_check varchar(5) null,
sir_check varchar(5) null

)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/***************** 
 *
 * hr_a
 *
 *****************/
create table hr_a(
no int not null primary key AUTO_INCREMENT,
employee_id int null,
employee_name varchar(50) null,
employee_eng_name varchar(50) null,
login_id varchar(50) null,
company_id varchar(50) null,
department_id varchar(50) null,
department_code varchar(10) null,
department_name varchar(30) null,
identity_id varchar(50) null,
sex varchar(5) null,
email varchar(300) null,
mobile varchar(50) null,
birthday varchar(50) null,
job_title_code varchar(50) null,
job_title_name varchar(50) null,
job_grade varchar(50) null,
job_rank varchar(50) null,
job_code varchar(50) null,
job_type varchar(50) null,
end_date varchar(50) null,
work_place varchar(50) null,
area_code varchar(50) null,
home_phone varchar(50) null,
office_phone varchar(50) null,
addresses varchar(300) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/***************** 
 *
 * work_station_3
 *
 *****************/
create table work_station_3(
no int not null primary key AUTO_INCREMENT,
e_name varchar(10) null,
c_content varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

insert into work_station_3 (e_name , c_content) VALUES('W','W-倉庫相關');
insert into work_station_3 (e_name , c_content) VALUES('W1','W1-領料');
insert into work_station_3 (e_name , c_content) VALUES('W2','W2-稱料');
insert into work_station_3 (e_name , c_content) VALUES('W3','W3-退料');

insert into work_station_3 (e_name , c_content) VALUES('Y','Y-設備相關');
insert into work_station_3 (e_name , c_content) VALUES('Y1','Y1-裝機');
insert into work_station_3 (e_name , c_content) VALUES('Y2','Y2-調機');
insert into work_station_3 (e_name , c_content) VALUES('Y3','Y3-試機');

insert into work_station_3 (e_name , c_content) VALUES('K','故障相關');
insert into work_station_3 (e_name , c_content) VALUES('K1','K1-設備故障');
insert into work_station_3 (e_name , c_content) VALUES('K2','K2-支援系統異常');

insert into work_station_3 (e_name , c_content) VALUES('V','V1-機器拆卸 / 清機');

insert into work_station_3 (e_name , c_content) VALUES('F','F-充填作業');

insert into work_station_3 (e_name , c_content) VALUES('ST','ST-滅菌作業');

insert into work_station_3 (e_name , c_content) VALUES('Q','Q-檢視作業');

insert into work_station_3 (e_name , c_content) VALUES('T','T-教育訓練');
insert into work_station_3 (e_name , c_content) VALUES('T1','T1-部內教育訓練');
insert into work_station_3 (e_name , c_content) VALUES('T2','T2-部外教育訓練');

insert into work_station_3 (e_name , c_content) VALUES('L','L-其他');
insert into work_station_3 (e_name , c_content) VALUES('L1','L1-其它 - 5S活動');
insert into work_station_3 (e_name , c_content) VALUES('L2','L2-其它 - 參觀活動');
insert into work_station_3 (e_name , c_content) VALUES('L3','L3-其它 - 部內會議');
insert into work_station_3 (e_name , c_content) VALUES('L4','L4-其它 - 部外會議');

insert into work_station_3 (e_name , c_content) VALUES('U','U-休息');

insert into work_station_3 (e_name , c_content) VALUES('A','A-調製相關');
insert into work_station_3 (e_name , c_content) VALUES('A1','A1-預備工作');
insert into work_station_3 (e_name , c_content) VALUES('A2','A2-調製過程');

insert into work_station_3 (e_name , c_content) VALUES('PW','PW-制水 , 鹽滅');

insert into work_station_3 (e_name , c_content) VALUES('M','M-蓋印 / 打印 / 貼標');

insert into work_station_3 (e_name , c_content) VALUES('P','P-包裝作業');

insert into work_station_3 (e_name , c_content) VALUES('RE','RE-再檢作業');

insert into work_station_3 (e_name , c_content) VALUES('S','S-停工待料');

insert into work_station_3 (e_name , c_content) VALUES('R','R-支援工作');

insert into work_station_3 (e_name , c_content) VALUES('D','D-請假');

insert into work_station_3 (e_name , c_content) VALUES('J','J-確效驗證 , 校正');

insert into work_station_3 (e_name , c_content) VALUES('C','C-環境清潔');

/***************** 
 *
 * work_station_1
 *
 *****************/
create table work_station_1(
no int not null primary key AUTO_INCREMENT,
e_name varchar(10) null,
c_content varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

insert into work_station_3 (e_name , c_content) VALUES('W','W-倉庫相關');
insert into work_station_1 (e_name , c_content) VALUES('W1','W1-領料');
insert into work_station_1 (e_name , c_content) VALUES('W2','W2-稱料');
insert into work_station_1 (e_name , c_content) VALUES('W3','W3-退料');

insert into work_station_1 (e_name , c_content) VALUES('Y','Y-設備相關');
insert into work_station_1 (e_name , c_content) VALUES('Y1','Y1-裝機');
insert into work_station_1 (e_name , c_content) VALUES('Y2','Y2-調機');
insert into work_station_1 (e_name , c_content) VALUES('Y3','Y3-試機');

insert into work_station_1 (e_name , c_content) VALUES('K','故障相關');
insert into work_station_1 (e_name , c_content) VALUES('K1','K1-設備故障');
insert into work_station_1 (e_name , c_content) VALUES('K2','K2-支援系統異常');

insert into work_station_1 (e_name , c_content) VALUES('V','V1-機器拆卸 / 清機');

insert into work_station_1 (e_name , c_content) VALUES('F','F-充填作業');

insert into work_station_1 (e_name , c_content) VALUES('ST','ST-滅菌作業');

insert into work_station_1 (e_name , c_content) VALUES('Q','Q-檢視作業');

insert into work_station_1 (e_name , c_content) VALUES('T','T-教育訓練');
insert into work_station_1 (e_name , c_content) VALUES('T1','T1-部內教育訓練');
insert into work_station_1 (e_name , c_content) VALUES('T2','T2-部外教育訓練');

insert into work_station_1 (e_name , c_content) VALUES('L','L-其他');
insert into work_station_1 (e_name , c_content) VALUES('L1','L1-其它 - 5S活動');
insert into work_station_1 (e_name , c_content) VALUES('L2','L2-其它 - 參觀活動');
insert into work_station_1 (e_name , c_content) VALUES('L3','L3-其它 - 部內會議');
insert into work_station_1 (e_name , c_content) VALUES('L4','L4-其它 - 部外會議');

insert into work_station_1 (e_name , c_content) VALUES('P','P-包裝作業');

insert into work_station_1 (e_name , c_content) VALUES('RE','RE-再檢作業');

insert into work_station_1 (e_name , c_content) VALUES('C','C-環境清潔');

insert into work_station_1 (e_name , c_content) VALUES('U','U-休息');

insert into work_station_1 (e_name , c_content) VALUES('B','B-中栓');
insert into work_station_1 (e_name , c_content) VALUES('B1','B1-栓');
insert into work_station_1 (e_name , c_content) VALUES('B2','B2-外蓋');

insert into work_station_1 (e_name , c_content) VALUES('I','I-成型');
insert into work_station_1 (e_name , c_content) VALUES('I1','I1-吊具');
insert into work_station_1 (e_name , c_content) VALUES('I2','I2-無吊具');

insert into work_station_1 (e_name , c_content) VALUES('A','A-調製相關');
insert into work_station_1 (e_name , c_content) VALUES('A1','A1-預備工作');
insert into work_station_1 (e_name , c_content) VALUES('A2','A2-調製過程');

insert into work_station_1 (e_name , c_content) VALUES('PW','PW-制水 , 鹽滅');

insert into work_station_1 (e_name , c_content) VALUES('M','M-蓋印 / 打印 / 貼標');

insert into work_station_1 (e_name , c_content) VALUES('S','S-停工待料');

insert into work_station_1 (e_name , c_content) VALUES('R','R-支援工作');

insert into work_station_1 (e_name , c_content) VALUES('D','D-請假');

insert into work_station_1 (e_name , c_content) VALUES('J','J-確效驗證 , 校正');

/***************** 
 *
 * work_position
 *
 *****************/
create table work_position(
no int not null primary key AUTO_INCREMENT,
e_name varchar(10) null,
c_content varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

insert into work_position (e_name , c_content) VALUES('p1','生一部');
insert into work_position (e_name , c_content) VALUES('p2','生二部');
insert into work_position (e_name , c_content) VALUES('p3','生三部');

/***************** 
 *
 * work_station
 *
 *****************/
create table work_station(
no int not null primary key AUTO_INCREMENT,
e_name varchar(10) null,
c_content varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

insert into work_station_3 (e_name , c_content) VALUES('W','W-倉庫相關');
insert into work_station (e_name , c_content) VALUES('W1','W1-領料');
insert into work_station (e_name , c_content) VALUES('W2','W2-稱料');
insert into work_station (e_name , c_content) VALUES('W3','W3-退料');

insert into work_station (e_name , c_content) VALUES('A','A-造粒');
insert into work_station (e_name , c_content) VALUES('A1','A1-結合劑調製');
insert into work_station (e_name , c_content) VALUES('A2','A2-濕式造粒');
insert into work_station (e_name , c_content) VALUES('A3','A3-乾式整粒');

insert into work_station (e_name , c_content) VALUES('E','E-打錠');

insert into work_station (e_name , c_content) VALUES('Y1','Y1-裝機');
insert into work_station (e_name , c_content) VALUES('Y2','Y2-調機');
insert into work_station (e_name , c_content) VALUES('Y3','Y3-試機');

insert into work_station (e_name , c_content) VALUES('V1','V1-機器拆卸');
insert into work_station (e_name , c_content) VALUES('V2','V2-清機');

insert into work_station (e_name , c_content) VALUES('K1','K1-機械故障');
insert into work_station (e_name , c_content) VALUES('K2','K2-維修');

insert into work_station (e_name , c_content) VALUES('M1','M1-蓋印');
insert into work_station (e_name , c_content) VALUES('M2','M2-打印');

insert into work_station (e_name , c_content) VALUES('O','O-泡殼分裝');

insert into work_station (e_name , c_content) VALUES('P','P-包裝作業');

insert into work_station (e_name , c_content) VALUES('Q','Q-檢視作業');

insert into work_station (e_name , c_content) VALUES('S','S-停工待料');

insert into work_station (e_name , c_content) VALUES('C','C-環境清潔');

insert into work_station (e_name , c_content) VALUES('J','J-確效驗證');

insert into work_station (e_name , c_content) VALUES('R','R-支援工作');

insert into work_station (e_name , c_content) VALUES('T','T-教育訓練');
insert into work_station (e_name , c_content) VALUES('T1','T1-部內教育訓練');
insert into work_station (e_name , c_content) VALUES('T2','T2-部外教育訓練');

insert into work_station (e_name , c_content) VALUES('U','U-休息');

insert into work_station (e_name , c_content) VALUES('D','D-請假');

insert into work_station (e_name , c_content) VALUES('L','L-其他');
insert into work_station (e_name , c_content) VALUES('L1','L1-其它 - 5S活動');
insert into work_station (e_name , c_content) VALUES('L2','L2-其它 - 參觀活動');
insert into work_station (e_name , c_content) VALUES('L3','L3-其它 - 部內會議');
insert into work_station (e_name , c_content) VALUES('L4','L4-其它 - 部外會議');

/***************** 
 *
 * operation_record
 *
 *****************/
create table operation_record(
no int not null primary key AUTO_INCREMENT,
a_user varchar(200) null,
login_code varchar(200) null,
r_time datetime null,
item varchar(200) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/********************* 
 *
 * login_out_record
 *
 *********************/
create table login_out_record(
no int not null primary key AUTO_INCREMENT,
a_user varchar(200) null,
login_code varchar(200) null,
login_ip varchar(100) null,
login_time datetime null,
logout_time datetime null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/********************* 
 *
 * account
 *
 *********************/
create table account(
no int not null primary key AUTO_INCREMENT,
r_year varchar(100) null,
r_month varchar(100) null,
r_day varchar(100) null,
r_time time null,
a_work_no int null,
a_user varchar(100) null,
a_name varchar(100) null,
a_pwd varchar(100) null,
a_lv varchar(10) null,
a_position varchar(10) null,
a_status varchar(50) null,
a_comment text null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

insert into account (a_work_no , a_user , a_pwd , a_lv , a_status , a_position) VALUES('1','admin','1qaz#123','1','run' , 'all');
insert into account (a_work_no , a_user , a_pwd , a_lv , a_status , a_position) VALUES('2','otsuka','otsuka','2','run' , 'all');
insert into account (a_work_no , a_user , a_pwd , a_lv , a_status , a_position) VALUES('3','normal','normal','3','run' , 'all');
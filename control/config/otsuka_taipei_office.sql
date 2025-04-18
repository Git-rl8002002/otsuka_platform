/*****************************************************************
*
* Author   : JasonHung
* Date     : 20221102
* Update   : 20240330
* Function : otsuka for taipei office work time system
*
******************************************************************/

/************************************ 
 *
 * database : otsuka_taipei_office
 *
 ************************************/
create database otsuka_taipei_office DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
use otsuka_taipei_office;

/************************************************************  
 *
 * 人資部 - 360 考核主管測試資料
 *
 ************************************************************/
INSERT INTO `hr_360_submit_manager_content` (`c_date`, `c_year`, `c_month`, `c_day`, `c_time`, `c_d_time`, `s_date`, `s_user`, `s_name`, `s_hr_360_1_1`, `s_hr_360_1_2`, `s_hr_360_1_3`, `s_hr_360_1_4`, `s_hr_360_1_5`, `s_hr_360_2_1`, `s_hr_360_2_2`, `s_hr_360_2_3`, `s_hr_360_2_4`, `s_hr_360_2_5`, `s_hr_360_2_6`, `s_hr_360_3_1`, `s_hr_360_3_2`, `s_hr_360_3_3`, `s_hr_360_3_4`, `s_hr_360_3_5`, `s_hr_360_4_1`, `s_hr_360_4_2`, `s_hr_360_4_3`, `s_hr_360_4_4`, `s_hr_360_5_1`, `s_hr_360_5_2`, `s_hr_360_5_3`, `s_hr_360_6_1`, `s_hr_360_6_2`, `s_hr_360_6_3`, `s_hr_360_6_4`, `s_hr_360_6_5`, `s_hr_360_total_1`, `s_hr_360_total_1_avg`, `s_hr_360_total_2`, `s_hr_360_total_2_avg`, `s_hr_360_total_3`, `s_hr_360_total_3_avg`, `s_hr_360_total_4`, `s_hr_360_total_4_avg`, `s_hr_360_total_5`, `s_hr_360_total_5_avg`, `s_hr_360_total_6`, `s_hr_360_total_6_avg`) VALUES
(NULL, '2024', '08', '26', NULL, NULL, '2024-08-26', '張啟真', '洪毅明', '4', '4', '4', '4', '4', '5', '4', '4', '4', '4', '4', '3', '4', '4', '4', '4', '4', '4', '5', '3', '4', '4', '3', '4', '4', '4', '4', '3', '20', '4', '25', '4.166', '19', '3.8', '16', '4', '11', '3.666', '19', '3.8');


/************************************************************  
 *
 * 人資部 - 360 考核主管清單測試資料
 *
 ************************************************************/
insert into hr_360_submit_manager_content_person(c_date , s_dep , s_user , s_lv , s_name) value('2024-09-02','NO1-C1','江晏如','自己','江晏如');
insert into hr_360_submit_manager_content_person(c_date , s_dep , s_user , s_lv , s_name) value('2024-09-02','NO1-C1','林雅雪','主管','江晏如');
insert into hr_360_submit_manager_content_person(c_date , s_dep , s_user , s_lv , s_name) value('2024-09-02','NO1-C1','陳緯綺','同輩1','江晏如');
insert into hr_360_submit_manager_content_person(c_date , s_dep , s_user , s_lv , s_name) value('2024-09-02','NO1-C1','王耀鋒','同輩2','江晏如');
insert into hr_360_submit_manager_content_person(c_date , s_dep , s_user , s_lv , s_name) value('2024-09-02','NO1-C1','黃秀菁','下屬1','江晏如');
insert into hr_360_submit_manager_content_person(c_date , s_dep , s_user , s_lv , s_name) value('2024-09-02','NO1-C1','劉嘉鈴','下屬2','江晏如');

/************************************************************  
 *
 * 電子看板
 *
 ************************************************************/
create table e_board(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_year varchar(10) null,
c_month varchar(10) null,
c_day varchar(10) null,
c_time time null,
c_d_time datetime null,
s_date Date null,

e_date Date null,
e_s_time time null,
e_e_time time null,

e_company varchar(30) null,
e_title varchar(50) null,
e_name varchar(50) null,
e_instructions text null,
e_unit varchar(50) null,
e_finish date null,
e_other text null,
e_c_name varchar(30) null,
e_c_finish_date date null


)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************************************************  
 *
 * 最新公告
 *
 ************************************************************/
create table new_latest_announcement(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_year varchar(10) null,
c_month varchar(10) null,
c_day varchar(10) null,
c_time time null,
c_d_time datetime null,
s_date Date null,

s_dep varchar(30) null,
s_user varchar(30) null,

news_title varchar(300) null,
news_content text null,
s_status varchar(30) null


)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************************************************  
 *
 * 人資部 - 360 考核主管清單
 *
 ************************************************************/
create table hr_360_submit_manager_content_person(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_year varchar(10) null,
c_month varchar(10) null,
c_day varchar(10) null,
c_time time null,
c_d_time datetime null,
s_date Date null,
s_dep varchar(30) null,
s_user varchar(30) null,
s_lv varchar(30) null,
s_name varchar(30) null,
s_status varchar(30) null


)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************************************************  
 *
 * 人資部 - 360 考核員工內容
 *
 ************************************************************/
create table hr_360_submit_member_content(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_year varchar(10) null,
c_month varchar(10) null,
c_day varchar(10) null,
c_time time null,
c_d_time datetime null,
s_date Date null,
s_user varchar(30) null,
s_name varchar(30) null,
s_lv varchar(30) null,
s_hr_360_1_1 varchar(5) null,
s_hr_360_1_2 varchar(5) null,
s_hr_360_1_3 varchar(5) null,
s_hr_360_1_4 varchar(5) null,
s_hr_360_1_5 varchar(5) null,
s_hr_360_2_1 varchar(5) null,
s_hr_360_2_2 varchar(5) null,
s_hr_360_2_3 varchar(5) null,
s_hr_360_2_4 varchar(5) null,
s_hr_360_2_5 varchar(5) null,
s_hr_360_3_1 varchar(5) null,
s_hr_360_3_2 varchar(5) null,
s_hr_360_3_3 varchar(5) null,
s_hr_360_3_4 varchar(5) null,
s_hr_360_3_5 varchar(5) null,
s_hr_360_4_1 varchar(5) null,
s_hr_360_4_2 varchar(5) null,
s_hr_360_4_3 varchar(5) null,
s_hr_360_4_4 varchar(5) null,
s_hr_360_4_5 varchar(5) null,
s_hr_360_5_1 varchar(5) null,
s_hr_360_5_2 varchar(5) null,
s_hr_360_5_3 varchar(5) null,
s_hr_360_5_4 varchar(5) null,
s_hr_360_5_5 varchar(5) null,
s_hr_360_5_6 varchar(5) null,
s_hr_360_total_1 varchar(5) null,
s_hr_360_total_1_avg varchar(5) null,
s_hr_360_total_2 varchar(5) null,
s_hr_360_total_2_avg varchar(5) null,
s_hr_360_total_3 varchar(5) null,
s_hr_360_total_3_avg varchar(5) null,
s_hr_360_total_4 varchar(5) null,
s_hr_360_total_4_avg varchar(5) null,
s_hr_360_total_5 varchar(5) null,
s_hr_360_total_5_avg varchar(5) null,
s_hr_360_total_6 varchar(5) null,
s_hr_360_total_6_avg varchar(5) null

)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


/************************************************************  
 *
 * 人資部 - 360 考核主管內容
 *
 ************************************************************/
create table hr_360_submit_manager_content(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_year varchar(10) null,
c_month varchar(10) null,
c_day varchar(10) null,
c_time time null,
c_d_time datetime null,
s_date Date null,
s_user varchar(30) null,
s_name varchar(30) null,
s_lv varchar(30) null,
s_hr_360_1_1 varchar(5) null,
s_hr_360_1_2 varchar(5) null,
s_hr_360_1_3 varchar(5) null,
s_hr_360_1_4 varchar(5) null,
s_hr_360_1_5 varchar(5) null,
s_hr_360_2_1 varchar(5) null,
s_hr_360_2_2 varchar(5) null,
s_hr_360_2_3 varchar(5) null,
s_hr_360_2_4 varchar(5) null,
s_hr_360_2_5 varchar(5) null,
s_hr_360_2_6 varchar(5) null,
s_hr_360_3_1 varchar(5) null,
s_hr_360_3_2 varchar(5) null,
s_hr_360_3_3 varchar(5) null,
s_hr_360_3_4 varchar(5) null,
s_hr_360_3_5 varchar(5) null,
s_hr_360_4_1 varchar(5) null,
s_hr_360_4_2 varchar(5) null,
s_hr_360_4_3 varchar(5) null,
s_hr_360_4_4 varchar(5) null,
s_hr_360_5_1 varchar(5) null,
s_hr_360_5_2 varchar(5) null,
s_hr_360_5_3 varchar(5) null,
s_hr_360_6_1 varchar(5) null,
s_hr_360_6_2 varchar(5) null,
s_hr_360_6_3 varchar(5) null,
s_hr_360_6_4 varchar(5) null,
s_hr_360_6_5 varchar(5) null,
s_hr_360_total_1 varchar(5) null,
s_hr_360_total_1_avg varchar(5) null,
s_hr_360_total_2 varchar(5) null,
s_hr_360_total_2_avg varchar(5) null,
s_hr_360_total_3 varchar(5) null,
s_hr_360_total_3_avg varchar(5) null,
s_hr_360_total_4 varchar(5) null,
s_hr_360_total_4_avg varchar(5) null,
s_hr_360_total_5 varchar(5) null,
s_hr_360_total_5_avg varchar(5) null,
s_hr_360_total_6 varchar(5) null,
s_hr_360_total_6_avg varchar(5) null

)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************************************************  
 *
 * 人資部 - 360 考核設定
 *
 ************************************************************/
create table hr_360_person_setup(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_year varchar(10) null,
c_month varchar(10) null,
c_day varchar(10) null,
c_time time null,
c_d_time datetime null,

c_dep varchar(30) null,
c_name varchar(30) null,
c_name_status varchar(30) null,
c_manager varchar(30) null,
c_manager_status varchar(30) null,
c_peer1 varchar(30) null,
c_peer1_status varchar(30) null,
c_peer2 varchar(30) null,
c_peer2_status varchar(30) null,
c_subordinate1 varchar(30) null,
c_subordinate1_status varchar(30) null,
c_subordinate2 varchar(30) null
c_subordinate2_status varchar(30) null

)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************************************************  
 *
 * 財務部 - SS2 注文單對接豐田外倉
 *
 ************************************************************/
create table ss2_export_record(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_year varchar(10) null,
c_month varchar(10) null,
c_day varchar(10) null,
c_time time null,
c_d_time datetime null,

ss2_form Date null,
email varchar(300) null,
e_status varchar(30) null

)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


/************************************************************  
 *
 * 醫藥法規開發處 - 08.政府公開資料庫比對查詢
 *
 ************************************************************/
create table mrd_8_food(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_year varchar(10) null,
c_month varchar(10) null,
c_day varchar(10) null,
c_time time null,
c_d_time datetime null,

kind varchar(100) null,
ch varchar(300) null,
en varchar(300) null,
content text null,
usage_limit varchar(100) null,
spec varchar(100) null

)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************************************************  
 *
 * 財務部 - IT 年度預算 目前剩餘費用
 *
 ************************************************************/
create table it_annual_budget_kind_remaining_cost(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_year varchar(10) null,
c_month varchar(10) null,
c_day varchar(10) null,
c_time time null,
c_d_time datetime null,

kind varchar(100) null,
total_cost varchar(300) null,
use_cost varchar(300) null,
remaining_cost varchar(300) null,
comment text null

)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************************************************  
 *
 * 財務部 - IT 年度預算 目前支出費用
 *
 ************************************************************/
create table it_annual_budget_kind_use_cost(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_year varchar(10) null,
c_month varchar(10) null,
c_day varchar(10) null,
c_time time null,
c_d_time datetime null,
kind varchar(100) null,
title varchar(100) null,
manufacturer varchar(100) null,
use_cost varchar(300) null,
comment text null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/************************************************************  
 *
 * 財務部 - IT 年度預算
 *
 ************************************************************/
create table it_annual_budget(
no int not null primary key AUTO_INCREMENT,
c_date Date null,
c_year varchar(10) null,
c_month varchar(10) null,
c_day varchar(10) null,
c_time time null,
c_d_time datetime null,
kind varchar(100) null,
title varchar(300) null,
otsuka_holdings varchar(100) null,
annual_budget_year varchar(30) null,
remaining_now_annual_budget varchar(30) null,
comment text null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



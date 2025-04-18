function submit_hr_360_manager(){
        
        // 受評人員
        var check_hr_360_name = $.trim($("#check_hr_360_name").val());           

        // 管理能力
        var hr_360_total_1_1 = parseInt($('input[name="options1_1"]:checked').val(), 10) || 0;
        var hr_360_total_1_2 = parseInt($('input[name="options1_2"]:checked').val(), 10) || 0;
        var hr_360_total_1_3 = parseInt($('input[name="options1_3"]:checked').val(), 10) || 0;
        var hr_360_total_1_4 = parseInt($('input[name="options1_4"]:checked').val(), 10) || 0;
        var hr_360_total_1_5 = parseInt($('input[name="options1_5"]:checked').val(), 10) || 0;
        var total_1        = hr_360_total_1_1 + hr_360_total_1_2 + hr_360_total_1_3 + hr_360_total_1_4 + hr_360_total_1_5; 

        // 提供支援
        var hr_360_total_2_1 = parseInt($('input[name="options2_1"]:checked').val(), 10) || 0;
        var hr_360_total_2_2 = parseInt($('input[name="options2_2"]:checked').val(), 10) || 0;
        var hr_360_total_2_3 = parseInt($('input[name="options2_3"]:checked').val(), 10) || 0;
        var hr_360_total_2_4 = parseInt($('input[name="options2_4"]:checked').val(), 10) || 0;
        var hr_360_total_2_5 = parseInt($('input[name="options2_5"]:checked').val(), 10) || 0;
        var hr_360_total_2_6 = parseInt($('input[name="options2_6"]:checked').val(), 10) || 0;
        var total_2        = hr_360_total_2_1 + hr_360_total_2_2 + hr_360_total_2_3 + hr_360_total_2_4 + hr_360_total_2_5 + hr_360_total_2_6; 

        // 以身作則
        var hr_360_total_3_1 = parseInt($('input[name="options3_1"]:checked').val(), 10) || 0;
        var hr_360_total_3_2 = parseInt($('input[name="options3_2"]:checked').val(), 10) || 0;
        var hr_360_total_3_3 = parseInt($('input[name="options3_3"]:checked').val(), 10) || 0;
        var hr_360_total_3_4 = parseInt($('input[name="options3_4"]:checked').val(), 10) || 0;
        var hr_360_total_3_5 = parseInt($('input[name="options3_5"]:checked').val(), 10) || 0;
        var total_3        = hr_360_total_3_1 + hr_360_total_3_2 + hr_360_total_3_3 + hr_360_total_3_4 + hr_360_total_3_5; 

        // 效率導向
        var hr_360_total_4_1 = parseInt($('input[name="options4_1"]:checked').val(), 10) || 0;
        var hr_360_total_4_2 = parseInt($('input[name="options4_2"]:checked').val(), 10) || 0;
        var hr_360_total_4_3 = parseInt($('input[name="options4_3"]:checked').val(), 10) || 0;
        var hr_360_total_4_4 = parseInt($('input[name="options4_4"]:checked').val(), 10) || 0;
        var total_4        = hr_360_total_4_1 + hr_360_total_4_2 + hr_360_total_4_3 + hr_360_total_4_4; 

        // 培育人才
        var hr_360_total_5_1 = parseInt($('input[name="options5_1"]:checked').val(), 10) || 0;
        var hr_360_total_5_2 = parseInt($('input[name="options5_2"]:checked').val(), 10) || 0;
        var hr_360_total_5_3 = parseInt($('input[name="options5_3"]:checked').val(), 10) || 0;
        var total_5        = hr_360_total_5_1 + hr_360_total_5_2 + hr_360_total_5_3; 

        // 高效溝通
        var hr_360_total_6_1 = parseInt($('input[name="options6_1"]:checked').val(), 10) || 0;
        var hr_360_total_6_2 = parseInt($('input[name="options6_2"]:checked').val(), 10) || 0;
        var hr_360_total_6_3 = parseInt($('input[name="options6_3"]:checked').val(), 10) || 0;
        var hr_360_total_6_4 = parseInt($('input[name="options6_4"]:checked').val(), 10) || 0;
        var hr_360_total_6_5 = parseInt($('input[name="options6_5"]:checked').val(), 10) || 0;
        var total_6        = hr_360_total_6_1 + hr_360_total_6_2 + hr_360_total_6_3 + hr_360_total_6_4 + hr_360_total_6_5; 

        alert(check_hr_360_name + ' / ' + total_1 + ' / ' + total_2 + ' / ' + total_3 + ' / ' + total_4 + ' / ' + total_5 + ' / ' + total_6);

}

function select_hr_360_content(id){

        var hr_360_content_name = id;

        $.ajax({
                type:"POST",
                url:"/hr_360_content_name",
                data:{
                        'hr_360_content_name':hr_360_content_name
                },
                dataType:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        /*************
                         * 
                         * res show 
                         * 
                         **************/ 
                        $('#hr_360_content').show(1000).html(res);
                        
                        /***********************************
                         * 
                         * scroll page bottom to page top
                         * 
                         ***********************************/ 
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("載入 HR 360 考評人員 " + hr_360_content_name + " 項目內容 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
                }); 

}


function select_hr_name_data_5(){

        var res_hr_360_name = $.trim($("#res_hr_360_name_5").val());   
        $("#hr_360_check_subordinate_2_name").val(res_hr_360_name); 
   
   }
   
function keyin_hr_name_5(){
         
         // 平行 1 姓名 
         var h_360_hr_name = $.trim($("#hr_360_check_subordinate_2_name").val());  
   
         $.ajax({
           type:"POST",
           url:"/hr_360_employee_hr_name_5",
           data:{
                   'h_360_hr_name':h_360_hr_name
           },
           dataType:"html",
           error:function(xhr , ajaxError , throwError){
                   $('#click_show_msg').click();
                   $('#show_msg').show(1000).html(xhr.responseText);
           },
           success:function(res){
                   
                   /*************
                    * 
                    * res show 
                    * 
                    **************/ 
                   $('#show_hr_360_name_data_5').show(1000).html(res);

                   $('#hr_360_check_subordinate_2_name').attr('data-bs-content', 'searching ...').popover({
                        trigger: 'hover',
                        placement: 'top'
                        });
                   
                   
                   /***********************************
                    * 
                    * scroll page bottom to page top
                    * 
                    ***********************************/ 
                   goto_top();
                   
                   //location.reload(true);
           },
           beforeSend:function(){
                   $('#status').html("搜尋 HR 360 考評人員 " + h_360_hr_name + " 姓名 ...").css({'color':'red'});
           },
           complete:function(){
                   $('#status').css({'color':'#f8f9fa'});
           }
           }); 
   
}

function select_hr_name_data_4(){

        var res_hr_360_name = $.trim($("#res_hr_360_name_4").val());   
        $("#hr_360_check_subordinate_1_name").val(res_hr_360_name); 
   
   }
   
function keyin_hr_name_4(){
         
         // 平行 1 姓名 
         var h_360_hr_name = $.trim($("#hr_360_check_subordinate_1_name").val());  
   
         $.ajax({
           type:"POST",
           url:"/hr_360_employee_hr_name_4",
           data:{
                   'h_360_hr_name':h_360_hr_name
           },
           dataType:"html",
           error:function(xhr , ajaxError , throwError){
                   $('#click_show_msg').click();
                   $('#show_msg').show(1000).html(xhr.responseText);
           },
           success:function(res){
                   
                   /*************
                    * 
                    * res show 
                    * 
                    **************/ 
                   $('#show_hr_360_name_data_4').show(1000).html(res);

                   $('#hr_360_check_subordinate_1_name').attr('data-bs-content', 'searching ...').popover({
                        trigger: 'hover',
                        placement: 'top'
                        });
                   
                   
                   /***********************************
                    * 
                    * scroll page bottom to page top
                    * 
                    ***********************************/ 
                   goto_top();
                   
                   //location.reload(true);
           },
           beforeSend:function(){
                   $('#status').html("搜尋 HR 360 考評人員 " + h_360_hr_name + " 姓名 ...").css({'color':'red'});
           },
           complete:function(){
                   $('#status').css({'color':'#f8f9fa'});
           }
           }); 
   
}

function select_hr_name_data_3(){

        var res_hr_360_name = $.trim($("#res_hr_360_name_3").val());   
        $("#hr_360_check_peer_2_name").val(res_hr_360_name); 
   
   }
   
function keyin_hr_name_3(){
         
         // 平行 1 姓名 
         var h_360_hr_name = $.trim($("#hr_360_check_peer_2_name").val());  
   
         $.ajax({
           type:"POST",
           url:"/hr_360_employee_hr_name_3",
           data:{
                   'h_360_hr_name':h_360_hr_name
           },
           dataType:"html",
           error:function(xhr , ajaxError , throwError){
                   $('#click_show_msg').click();
                   $('#show_msg').show(1000).html(xhr.responseText);
           },
           success:function(res){
                   
                   /*************
                    * 
                    * res show 
                    * 
                    **************/ 
                   $('#show_hr_360_name_data_3').show(1000).html(res);

                   $('#hr_360_check_peer_2_name').attr('data-bs-content', 'searching ...').popover({
                        trigger: 'hover',
                        placement: 'top'
                        });
                   
                   
                   /***********************************
                    * 
                    * scroll page bottom to page top
                    * 
                    ***********************************/ 
                   goto_top();
                   
                   //location.reload(true);
           },
           beforeSend:function(){
                   $('#status').html("搜尋 HR 360 考評人員 " + h_360_hr_name + " 姓名 ...").css({'color':'red'});
           },
           complete:function(){
                   $('#status').css({'color':'#f8f9fa'});
           }
           }); 
   
}

function select_hr_name_data_2(){

        var res_hr_360_name = $.trim($("#res_hr_360_name_2").val());   
        $("#hr_360_check_peer_1_name").val(res_hr_360_name); 
   
}
   
function keyin_hr_name_2(){
         
         // 平行 1 姓名 
         var h_360_hr_name = $.trim($("#hr_360_check_peer_1_name").val());  
   
         $.ajax({
           type:"POST",
           url:"/hr_360_employee_hr_name_2",
           data:{
                   'h_360_hr_name':h_360_hr_name
           },
           dataType:"html",
           error:function(xhr , ajaxError , throwError){
                   $('#click_show_msg').click();
                   $('#show_msg').show(1000).html(xhr.responseText);
           },
           success:function(res){
                   
                   /*************
                    * 
                    * res show 
                    * 
                    **************/ 
                   $('#show_hr_360_name_data_2').show(1000).html(res);
                   
                   $('#hr_360_check_peer_1_name').attr('data-bs-content', 'searching ...').popover({
                        trigger: 'hover',
                        placement: 'top'
                        });
                   
                   
                   /***********************************
                    * 
                    * scroll page bottom to page top
                    * 
                    ***********************************/ 
                   goto_top();
                   
                   //location.reload(true);
           },
           beforeSend:function(){
                   $('#status').html("搜尋 HR 360 考評人員 " + h_360_hr_name + " 姓名 ...").css({'color':'red'});
           },
           complete:function(){
                   $('#status').css({'color':'#f8f9fa'});
           }
           }); 
   
}

function select_hr_name_data_1(){

     var res_hr_360_name = $.trim($("#res_hr_360_name").val());   
     $("#hr_360_check_manager_name").val(res_hr_360_name); 

}

function keyin_hr_name_1(){
      
      // 姓名 
      var h_360_hr_name = $.trim($("#hr_360_check_manager_name").val());  

      $.ajax({
        type:"POST",
        url:"/hr_360_employee_hr_name",
        data:{
                'h_360_hr_name':h_360_hr_name
        },
        dataType:"html",
        error:function(xhr , ajaxError , throwError){
                $('#click_show_msg').click();
                $('#show_msg').show(1000).html(xhr.responseText);
        },
        success:function(res){
                
                /*************
                 * 
                 * res show 
                 * 
                 **************/ 
                $('#show_hr_360_name_data_1').show(1000).html(res);
                
                $('#hr_360_check_manager_name').attr('data-bs-content', 'searching ...').popover({
                trigger: 'hover',
                placement: 'top'
                });
                
                
                /***********************************
                 * 
                 * scroll page bottom to page top
                 * 
                 ***********************************/ 
                goto_top();
                
                //location.reload(true);
        },
        beforeSend:function(){
                $('#status').html("搜尋 HR 360 考評人員 " + h_360_hr_name + " 姓名 ...").css({'color':'red'});
        },
        complete:function(){
                $('#status').css({'color':'#f8f9fa'});
        }
        }); 

}


function alter_hr_360_setup_data(id){
        
        var data   = id.split('/');
        var d_dep  = data[0];
        var d_name = data[1];

        $.ajax({
                type:"POST",
                url:"/alter_hr_360_manager_list",
                data:{
                        'd_dep':d_dep,
                        'd_name':d_name
                },
                dataType:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        /*************
                         * 
                         * res show 
                         * 
                         **************/ 
                        $('#alter_hr_360_setup_data').show(1000).html(res);
                        
                        /*************
                         * 
                         * Toast show 
                         * 
                         **************/ 
                        //$('#click_show_msg').click();
                        //$('#show_msg').show(1000).html(res);
                        
                        //$('#submit_otsuka_contract').toast('show');

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("刪除 HR 360 考評 " + d_dep + " / " + d_name  + " 人員資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        }); 


}

function del_hr_360_setup_data(id){
        
        var data   = id.split('/');
        var d_dep  = data[0];
        var d_name = data[1];

        var check_del = prompt("刪除  HR 360 考評 , " + d_dep + " / " + d_name  + " , 確定刪除 , 再按一次 y ");
        
	if(check_del == 'y'){	        

                $.ajax({
                        type:"POST",
                        url:"/del_hr_360_manager_list",
                        data:{
                                'd_dep':d_dep,
                                'd_name':d_name
                        },
                        dataType:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
                                
                                /*************
                                 * 
                                 * res show 
                                 * 
                                 **************/ 
                                $('#hr_360_setup_list').show(1000).html(res);
                                
                                /*************
                                 * 
                                 * Toast show 
                                 * 
                                 **************/ 
                                //$('#click_show_msg').click();
                                //$('#show_msg').show(1000).html(res);
                                
                                //$('#submit_otsuka_contract').toast('show');

                                //$("#computer_user_detail").show(1000).html(res);
                                //$("#show_day_month_detail").show(1000).html(res);
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("刪除 HR 360 考評 " + d_dep + " / " + d_name  + " 人員資料 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                }); 

        }

}

function load_hr_360_manager_setup_person_list(){
        
        $.ajax({
                type:"POST",
                url:"/load_hr_360_manager_list",
                data:{},
                dataType:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        /*************
                         * 
                         * res show 
                         * 
                         **************/ 
                        $('#hr_360_setup_list').show(1000).html(res);
                        
                        /*************
                         * 
                         * Toast show 
                         * 
                         **************/ 
                        //$('#click_show_msg').click();
                        //$('#show_msg').show(1000).html(res);
                        
                        //$('#submit_otsuka_contract').toast('show');

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("載入 HR 360 考評設定人員資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });   
}

function submit_hr_360_manager_setup_data(){
        
        // 部門  
        var h_360_m_dep = $.trim($("#hr_360_manager_dep").val());
        // 姓名 
        var h_360_m_name = $.trim($("#hr_360_manager_name").val());
        // 主管  
        var h_360_c_m_name = $.trim($("#hr_360_check_manager_name").val());
        // 平行 1  
        var h_360_c_p_1_name = $.trim($("#hr_360_check_peer_1_name").val());
        // 平行 2
        var h_360_c_p_2_name = $.trim($("#hr_360_check_peer_2_name").val());
        // 下屬 1
        var h_360_c_s_1_name = $.trim($("#hr_360_check_subordinate_1_name").val());
        // 下屬 2  
        var h_360_c_s_2_name = $.trim($("#hr_360_check_subordinate_2_name").val());


        // 部門
        if(h_360_m_dep.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i> HR 360 考評 , 部門 , 不能空白 ! </span>');
                exit();
        }
        // 姓名
        else if(h_360_m_name.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i> HR 360 考評 , 姓名 , 不能空白 ! </span>');
                exit();
        }
        // 主管姓名
        else if(h_360_c_m_name.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i> HR 360 考評 , 主管姓名 , 不能空白 ! </span>');
                exit();
        }
        // 平行 1
        else if(h_360_c_p_1_name.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i> HR 360 考評 , 平行姓名 1 , 不能空白 ! </span>');
                exit();
        }
        // 平行 2
        else if(h_360_c_p_2_name.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i> HR 360 考評 , 平行姓名 2 , 不能空白 ! </span>');
                exit();
        }
        // 下屬 1
        else if(h_360_c_s_1_name.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i> HR 360 考評 , 下屬姓名 1 , 不能空白 ! </span>');
                exit();
        }
        // 下屬 2
        else if(h_360_c_s_2_name.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i> HR 360 考評 , 下屬姓名 2 , 不能空白 ! </span>');
                exit();
        }
        else{
                $.ajax({
                        type:"POST",
                        url:"/add_hr_360_setup",
                        data:{
                                'h_360_m_dep':h_360_m_dep,
                                'h_360_m_name':h_360_m_name,
                                'h_360_c_m_name':h_360_c_m_name,
                                'h_360_c_p_1_name':h_360_c_p_1_name,
                                'h_360_c_p_2_name':h_360_c_p_2_name,
                                'h_360_c_s_1_name':h_360_c_s_1_name,
                                'h_360_c_s_2_name':h_360_c_s_2_name
                        },
                        datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
                                
                                /*************
                                 * 
                                 * res show 
                                 * 
                                 **************/ 
                                $('#hr_360_setup_list').show(1000).html(res);
                                
                                // 部門  
                                $("#hr_360_manager_dep").val("");
                                // 姓名 
                                $("#hr_360_manager_name").val("");
                                // 主管  
                                $("#hr_360_check_manager_name").val("");
                                // 平行 1  
                                $("#hr_360_check_peer_1_name").val("");
                                // 平行 2
                                $("#hr_360_check_peer_2_name").val("");
                                // 下屬 1
                                $("#hr_360_check_subordinate_1_name").val("");
                                // 下屬 2  
                                $("#hr_360_check_subordinate_2_name").val("");

                                /***********************************
                                 * 
                                 * scroll page bottom to page top
                                 * 
                                 ***********************************/
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("載入 HR 360 考評設定人員資料 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });
        }

}

function select_dep_name(){
        
        // 部門
        var h_3_m_dep = $.trim($("#hr_360_manager_dep").val());
        
        $.ajax({
                type:"POST",
                url:"/load_hr_360_query_data_name",
                data:{
                        'h_3_m_dep':h_3_m_dep
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // refresh show 
                        $('#load_hr_360_query_data_name').show(1000).html(res);
                        
                        //$('#submit_otsuka_contract').toast('show');

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("即時載入 HR " + h_3_m_dep + " , 人員資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });         
}

function select_erp_realtime_query_product_num(){
        
        // 產品品號
        var q_e_p_num = $.trim($("#query_erp_product_num3").val());
        
        $.ajax({
                type:"POST",
                url:"/select_erp_realtime_query_data3_1",
                data:{
                        'q_e_p_num':q_e_p_num
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // refresh show 
                        $('#load_erp_realtime_query_all_num3_1').show(1000).html(res);
                        
                        //$('#submit_otsuka_contract').toast('show');

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("即時載入 ERP 原物料使用/原物料TO製品/產品品號 : " + q_e_p_num + " , 庫存資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        }); 

}

function bpm_expenditure_download_ecxcel(){
        
        // 起時日期
        var q_s_date       = $.trim($("#query_start_date").val());
        // 結束日期
        var q_e_date       = $.trim($("#query_end_date").val());
        // 申請部門
        var q_b_e_dep      = $.trim($("#query_bpm_expenditure_dep").val());
        // 申請人
        var q_b_e_d_member = $.trim($("#query_bpm_expenditure_dep_member").val());
        // 預算來源
        var q_b_b_s_b_budget = $.trim($("#query_bpm_budget_source_by_dep").val());
        // 狀態
        var q_b_e_status   = $.trim($("#query_bpm_expenditure_status").val());

        var item = 'excel';

        $.ajax({
                type:"POST",
                url:"/bpm_expenditure_download_excel",
                data:{
                        'q_s_date':q_s_date,
                        'q_e_date':q_e_date,
                        'q_b_e_dep':q_b_e_dep,
                        'q_b_e_d_member':q_b_e_d_member,
                        'q_b_e_status':q_b_e_status,
                        'q_b_b_s_b_budget':q_b_b_s_b_budget
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        if (item == 'excel'){
                                var url = "/download_bpm_expenditure_excel?s_date="+q_s_date+"&e_date="+q_e_date+"&dep="+q_b_e_dep+"&member="+q_b_e_d_member+"&status="+q_b_e_status;
                                var fileName = '開支證明單_' + q_b_e_dep + '_' + q_b_e_d_member + '_' + q_b_e_status + '.xlsx';
                                
                                // 创建一个动态链接并触发点击
                                var link = $('<a></a>')
                                        .attr('href', url)
                                        .attr('download', fileName)
                                        .appendTo('body');

                                link[0].click();
                                link.remove(); // 清理动态创建的元素
                        }else if(item == 'pdf'){
                                var url = "/download_bpm_expenditure_excel?s_date="+q_s_date+"&e_date="+q_e_date+"&dep="+q_b_e_dep+"&member="+q_b_e_d_member+"&status="+q_b_e_status;
                                var fileName = '開支證明單_' + q_b_e_dep + '_' + q_b_e_d_member + '_' + q_b_e_status + '.pdf';

                                // 创建一个动态链接并触发点击
                                var link = $('<a></a>')
                                        .attr('href', url)
                                        .attr('download', fileName)
                                        .appendTo('body');

                                link[0].click();
                                link.remove(); // 清理动态创建的元素
                        }
                        
                        //$('#card_reader_detail_list').show(1000).html(res);
                        //alert(position + '_' + day + ' download successful.');

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("匯出 " + q_b_e_dep + ' ' + q_b_e_d_member + ' ' + q_b_e_status + '.xlsx' + " ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function export_bpm_expenditure_form_excel(){

}

function show_msg(msg){
        $('#click_show_msg').click();
        $('#show_msg').show(1000).html(msg);
}

function submit_erp_realtime_query_search3(){
        
        // 產品品號
        var q_e_p_num3 = $.trim($("#query_erp_product_num3").val());
        // 產品批號
        var q_e_p_a_num3 = $.trim($("#query_erp_product_all_num3").val());

        // 產品品號
        if(q_e_p_num3.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i> ERP 原物料使用-原物料TO製品 , 產品品號 , 不能空白 ! </span>');
                exit();
        }
        // 產品批號
        else if(q_e_p_a_num3.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i> ERP 原物料使用-原物料TO製品 , 產品批號 , 不能空白 ! </span>');
                exit();
        }
        else{
                $.ajax({
                        type:"POST",
                        url:"/show_select_erp_realtime_query_search3",
                        data:{
                                'q_e_p_num3':q_e_p_num3 ,
                                'q_e_p_a_num3':q_e_p_a_num3
                        },
                        datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
                                
                                /*************
                                 * 
                                 * res show 
                                 * 
                                 **************/ 
                                $('#f_erp_realtime_query3').show(1000).html(res);
                                
                                /*************
                                 * 
                                 * Toast show 
                                 * 
                                 **************/ 
                                //$('#click_show_msg').click();
                                //$('#show_msg').show(1000).html(res);
                                
                                //$('#submit_otsuka_contract').toast('show');

                                //$("#computer_user_detail").show(1000).html(res);
                                //$("#show_day_month_detail").show(1000).html(res);
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("載入 ERP 原物料使用-原物料TO製品 , 品號 " + q_e_p_num3 , "  批號  "  +  q_e_p_a_num3 +  " , 即時庫存資料 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });
        }

}

function submit_erp_realtime_query_search2(){
        
        // 入庫年月
        var q_e_p_i_y_month = $.trim($("#query_erp_product_import_year_month").val());

        // 入庫年月
        if(q_e_p_i_y_month.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i> ERP 製品庫存&生產實績 , 入庫年月 , 不能空白 ! </span>');
                exit();
        }
        else{
                $.ajax({
                        type:"POST",
                        url:"/show_select_erp_realtime_query_search2",
                        data:{
                                'q_e_p_i_y_month':q_e_p_i_y_month
                        },
                        datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
                                
                                /*************
                                 * 
                                 * res show 
                                 * 
                                 **************/ 
                                $('#f_erp_realtime_query2').show(1000).html(res);
                                
                                /*************
                                 * 
                                 * Toast show 
                                 * 
                                 **************/ 
                                //$('#click_show_msg').click();
                                //$('#show_msg').show(1000).html(res);
                                
                                //$('#submit_otsuka_contract').toast('show');

                                //$("#computer_user_detail").show(1000).html(res);
                                //$("#show_day_month_detail").show(1000).html(res);
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("載入 BPM 開支證明單 , 搜尋資料 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });
        }

}
function submit_login_out_record_query_operation_search(){
        
        
        // 起始時間
        var q_s_date = $.trim($("#query_start_date").val());
        // 結束時間
        var q_e_date = $.trim($("#query_end_date").val());
        // 帳號
        var l_o_a_query = $.trim($("#login_out_account_query").val());
        var l_o_a_query = l_o_a_query.split(" (")[0]

        // 帳號
        if(l_o_a_query.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i> 帳號進出紀錄 , 帳號 , 不能空白 ! </span>');
                exit();
        }
        else{
                /**************
                 * 
                 * 帳號操作紀錄
                 * 
                 ***************/
                $.ajax({
                        type:"POST",
                        url:"/show_select_login_out_account_operation_record",
                        data:{
                                'l_o_a_query':l_o_a_query ,
                                'q_s_date':q_s_date ,
                                'q_e_date':q_e_date
                        },
                        datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
                                
                                /*************
                                 * 
                                 * res show 
                                 * 
                                 **************/ 
                                $('#login_our_record_query_list').show(1000).html(res);
                                
                                /*************
                                 * 
                                 * Toast show 
                                 * 
                                 **************/ 
                                //$('#click_show_msg').click();
                                //$('#show_msg').show(1000).html(res);
                                
                                //$('#submit_otsuka_contract').toast('show');

                                //$("#computer_user_detail").show(1000).html(res);
                                //$("#show_day_month_detail").show(1000).html(res);
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("載入帳號操作紀錄 , 帳號 : " + l_o_a_query + " ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });

        }

}

function submit_login_out_record_query_search(){
        
        
        // 起始時間
        var q_s_date = $.trim($("#query_start_date").val());
        // 結束時間
        var q_e_date = $.trim($("#query_end_date").val());
        // 帳號
        var l_o_a_query = $.trim($("#login_out_account_query").val());
        var l_o_a_query = l_o_a_query.split(" (")[0]

        // 帳號
        if(l_o_a_query.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i> 帳號進出紀錄 , 帳號 , 不能空白 ! </span>');
                exit();
        }
        else{
                /**************
                 * 
                 * 帳號進出紀錄
                 * 
                 ***************/
                $.ajax({
                        type:"POST",
                        url:"/show_select_login_out_account_record",
                        data:{
                                'l_o_a_query':l_o_a_query ,
                                'q_s_date':q_s_date ,
                                'q_e_date':q_e_date
                        },
                        datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
                                
                                /*************
                                 * 
                                 * res show 
                                 * 
                                 **************/ 
                                $('#login_our_record_query_list').show(1000).html(res);
                                
                                /*************
                                 * 
                                 * Toast show 
                                 * 
                                 **************/ 
                                //$('#click_show_msg').click();
                                //$('#show_msg').show(1000).html(res);
                                
                                //$('#submit_otsuka_contract').toast('show');

                                //$("#computer_user_detail").show(1000).html(res);
                                //$("#show_day_month_detail").show(1000).html(res);
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("載入帳號進出紀錄 , 帳號 : " + l_o_a_query + " ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });

        }

}

function submit_erp_realtime_query_search(){
        
        // 產品品號
        var q_e_p_num    = $.trim($("#query_erp_product_num").val());
        // 產品名稱
        var q_e_p_name   = $.trim($("#query_erp_product_name").val());
        // 產品批號
        var q_e_p_a_num  = $.trim($("#query_erp_product_all_num").val());
        // 有效日期
        var q_e_p_l_date = $.trim($("#query_erp_product_limit_date").val());


        // 產品品號
        if(q_e_p_num.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i> ERP 即時庫存查詢 , 產品品號 , 不能空白 ! </span>');
                exit();
        }
        // 產品名稱
        else if(q_e_p_name.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i> ERP 即時庫存查詢 , 產品名稱 , 不能空白 ! </span>');
                exit();
        }
        // 產品批號
        else if(q_e_p_a_num.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i> ERP 即時庫存查詢 , 產品批號 , 不能空白 ! </span>');
                exit();
        }
        // 有效日期
        else if(q_e_p_l_date.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i>  ERP 即時庫存查詢 , 有效日期 , 不能空白 ! </span>');
                exit();
        }
        else{
                $.ajax({
                        type:"POST",
                        url:"/show_select_erp_realtime_query_search",
                        data:{
                                'q_e_p_num':q_e_p_num,
                                'q_e_p_name':q_e_p_name,
                                'q_e_p_a_num':q_e_p_a_num,
                                'q_e_p_l_date':q_e_p_l_date 
                        },
                        datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
                                
                                /*************
                                 * 
                                 * res show 
                                 * 
                                 **************/ 
                                $('#f_erp_realtime_query').show(1000).html(res);
                                
                                /*************
                                 * 
                                 * Toast show 
                                 * 
                                 **************/ 
                                //$('#click_show_msg').click();
                                //$('#show_msg').show(1000).html(res);
                                
                                //$('#submit_otsuka_contract').toast('show');

                                //$("#computer_user_detail").show(1000).html(res);
                                //$("#show_day_month_detail").show(1000).html(res);
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("載入 BPM 開支證明單 , 搜尋資料 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });
        }

}

function submit_bpm_expenditure_form_search(){
        
        // 起時日期
        var q_s_date         = $.trim($("#query_start_date").val());
        // 結束日期
        var q_e_date         = $.trim($("#query_end_date").val());
        // 申請部門
        var q_b_e_dep        = $.trim($("#query_bpm_expenditure_dep").val());
        // 申請人
        var q_b_e_d_member   = $.trim($("#query_bpm_expenditure_dep_member").val());
        // 預算來源
        var q_b_b_s_b_budget = $.trim($("#query_bpm_budget_source_by_dep").val());
        // 狀態
        var q_b_e_status     = $.trim($("#query_bpm_expenditure_status").val());


        // 起始日期
        if(q_s_date.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i>  BPM 開支證明單 , 起始日期 , 不能空白 ! </span>');
                exit();
        }
        // 結束日期
        else if(q_e_date.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i>  BPM 開支證明單 , 結束日期 , 不能空白 ! </span>');
                exit();
        }
        // 申請部門
        else if(q_b_e_dep.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i>  BPM 開支證明單 , 申請部門 , 不能空白 ! </span>');
                exit();
        }
        // 狀態
        else if(q_b_e_status.length == 0){
                show_msg('<span class="text-danger"><i class="bi bi-x-circle"></i>  BPM 開支證明單 , 表單狀態 , 不能空白 ! </span>');
                exit();
        }
        else{
                $.ajax({
                        type:"POST",
                        url:"/show_select_bpm_expenditure_search",
                        data:{
                                'q_s_date':q_s_date, 
                                'q_e_date':q_e_date,
                                'q_b_e_dep':q_b_e_dep,
                                'q_b_e_d_member':q_b_e_d_member,
                                'q_b_e_status':q_b_e_status,
                                'q_b_b_s_b_budget':q_b_b_s_b_budget
                        },
                        datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
                                
                                // refresh show 
                                //$('#query_bpm_expenditure_user').show(1000).html(res);

                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(res);
                                
                                //$('#submit_otsuka_contract').toast('show');

                                //$("#computer_user_detail").show(1000).html(res);
                                //$("#show_day_month_detail").show(1000).html(res);
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("載入 BPM 開支證明單 , 搜尋資料 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });
        }

}

function select_erp_realtime_query3(){
       
        // 產品品號
        var q_e_r_num = $("#query_erp_product_num").val();
        q_e_r_num     = $.trim(q_e_r_num);
        // 產品名稱
        var q_e_p_name = $("#query_erp_product_name").val();
        q_e_p_name     = $.trim(q_e_p_name);
        // 產品名稱
        var q_e_p_a_num = $("#query_erp_product_all_num").val();
        q_e_p_a_num     = $.trim(q_e_p_a_num);

        // 申請人 , 預算來源
        $.ajax({
                type:"POST",
                url:"/select_erp_realtime_query_data3",
                data:{
                        'q_e_r_num':q_e_r_num,
                        'q_e_p_name':q_e_p_name,
                        'q_e_p_a_num':q_e_p_a_num
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // refresh show 
                        $('#load_erp_realtime_query_data3').show(1000).html(res);
                        
                        //$('#submit_otsuka_contract').toast('show');

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("即時載入 ERP " + q_e_r_num + " / " + q_e_p_name + " / 有效日期 , 庫存資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });  

}

function select_erp_realtime_query2(){
       
        // 產品品號
        var q_e_r_num = $("#query_erp_product_num").val();
        q_e_r_num     = $.trim(q_e_r_num);
        // 產品名稱
        var q_e_p_name = $("#query_erp_product_name").val();
        q_e_p_name     = $.trim(q_e_p_name);

        // 申請人 , 預算來源
        $.ajax({
                type:"POST",
                url:"/select_erp_realtime_query_data2",
                data:{
                        'q_e_r_num':q_e_r_num,
                        'q_e_p_name':q_e_p_name
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // refresh show 
                        $('#load_erp_realtime_query_data2').show(1000).html(res);
                        
                        //$('#submit_otsuka_contract').toast('show');

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("即時載入 ERP " + q_e_r_num + " / " + q_e_p_name + " / 產品批號 , 庫存資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });  

}

function select_erp_realtime_query(){
       
        // 產品品號
        var q_e_r_num = $("#query_erp_product_num").val();
        q_e_r_num     = $.trim(q_e_r_num);
        // 產品名稱
        var q_e_p_name = $("#query_erp_product_name").val();
        q_e_p_name     = $.trim(q_e_p_name);

        // 產品批號
        $("#query_erp_product_all_num").val("");
        // 有效日期
        $("#query_erp_product_limit_date").val("");

        // 申請人 , 預算來源
        $.ajax({
                type:"POST",
                url:"/select_erp_realtime_query_data",
                data:{
                        'q_e_r_num':q_e_r_num,
                        'q_e_p_name':q_e_p_name
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // refresh show 
                        $('#load_erp_realtime_query_data').show(1000).html(res);
                        
                        //$('#submit_otsuka_contract').toast('show');

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("即時載入 ERP " + q_e_r_num + " / " + q_e_p_name + " / 產品名稱 , 庫存資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });  

}


function select_bpm_expenditure_dep_user(){
       
        // 申請部門
        var q_b_e_dep = $("#query_bpm_expenditure_dep").val();
        q_b_e_dep     = $.trim(q_b_e_dep);


        // 申請人 , 預算來源
        $.ajax({
                type:"POST",
                url:"/select_bpm_expenditure_dep_user",
                data:{
                        'q_b_e_dep':q_b_e_dep
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // refresh show 
                        $('#query_bpm_expenditure_user').show(1000).html(res);
                        
                        //$('#submit_otsuka_contract').toast('show');

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("載入 BPM 開支證明單 , 申請人資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
        
               
}

function submit_bpm_expenditure_form(){
      
        // 起始日期
        var o_s_date = $("#query_start_date").val();
        o_s_date     = $.trim(o_s_date);
        // 結束日期
        var o_e_date = $("#query_end_date").val();
        o_e_date     = $.trim(o_e_date);
        // 部門
        var o_b_e_d_date = $("#query_bpm_expenditure_dep").val();
        o_b_e_d_date     = $.trim(o_b_e_d_date);
        // 申請人
        var o_b_e_d_date = $("#query_bpm_expenditure_dep").val();
        o_b_e_d_date     = $.trim(o_b_e_d_date);


        // 起始日期
        if(o_s_date == ""){
                $('#click_show_msg').click();
                $('#show_msg').show(1000).html('<span class="text-danger"><i class="bi bi-x-circle"></i>  BPM 開支證明單 , 起始日期 , 不能空白 ! </span>');
                exit()
        }
        // 結束日期
        else if(o_e_date == ""){
                $('#click_show_msg').click();
                $('#show_msg').show(1000).html('<span class="text-danger"><i class="bi bi-x-circle"></i>  BPM 開支證明單 ,  結束日期 , 不能空白 ! </span>');
                exit()
        }
        // submit otsuka contract
        else{

                $.ajax({
                        type:"POST",
                        url:"/submit_otsuka_contract",
                        data:{
                                'o_s_date':o_s_date,
                                'o_e_date':o_e_date,
                                'o_b_e_d_date':o_b_e_d_date
                        },
                        datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
                                
                                // refresh show 
                                //$('#otsuka_contract').show(1000).html(res);
                                
                                $('#submit_otsuka_contract').toast('show');

                                // clean up fields
                                $("#o_c_date").val("");
                                $("#o_c_kind").val("");
                                $("#o_c_title").val("");
                                $("#o_c_cost").val("");
                                $("#o_c_time").val("");
                                $("#o_c_company").val("");
                                $("#o_c_name").val("");
                                $("#o_c_telephone").val("");
                                $("#o_c_phone").val("");
                                $("#o_c_comment").val("");

                                //$("#computer_user_detail").show(1000).html(res);
                                //$("#show_day_month_detail").show(1000).html(res);
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("顯示合約資訊資料 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });
        }
      
}


function bpm_information_account_detail(id){

        var data = id.split("/");
        var dep  = data[0];
        var kind = data[1];
        var user = data[2];
 
        $.ajax({
                type:"POST",
                url:"/bpm_information_account_detail",
                data:{
                        'dep':dep,
                        'kind':kind,
                        'user':user
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // clean value
                        //$('#a_work_no').val('');
                        //$('#a_date').val('');
                        //$('#a_name').val('');
                        //$('#a_user').val('');
                        //$('#a_position').val('');
                        //$('#a_status').val('');
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);
                        //$('#final_update_work_record').show(1000).html(res);
                        // reload account list
                        //reload_menu_account_list();
                },
                beforeSend:function(){
                        $('#status').html("loading BPM 電子表單 , " + id + " , 詳細資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });  
               
}

function bpm_information_detail(id){

        var data = id.split("/");
        var dep  = data[0];
        var kind = data[1];
        
        $.ajax({
                type:"POST",
                url:"/bpm_information_detail",
                data:{
                        'dep':dep,
                        'kind':kind
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // clean value
                        //$('#a_work_no').val('');
                        //$('#a_date').val('');
                        //$('#a_name').val('');
                        //$('#a_user').val('');
                        //$('#a_position').val('');
                        //$('#a_status').val('');
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);
                        //$('#final_update_work_record').show(1000).html(res);
                        // reload account list
                        //reload_menu_account_list();
                },
                beforeSend:function(){
                        $('#status').html("loading BPM 電子表單 , " + id + " , 詳細資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });  
               
}

function query_ss2_order_form(bookmark){
        
      $('#'+ query_ss2_order_form).click();  
}

function update_final_work_record(){

        $.ajax({
                type:"POST",
                url:"/final_update_work_record_list",
                data:{
                        
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // clean value
                        //$('#a_work_no').val('');
                        //$('#a_date').val('');
                        //$('#a_name').val('');
                        //$('#a_user').val('');
                        //$('#a_position').val('');
                        //$('#a_status').val('');

                        $('#final_update_work_record').show(1000).html(res);

                        // reload account list
                        //reload_menu_account_list();
                },
                beforeSend:function(){
                        $('#status').html("loading 更新最後工作進度表清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        }); 

}

function submit_alter_new_work_record(){
        
        var w_date      = $('#w_a_date').val();
        var w_place     = $('#w_a_place').val();
        var w_start     = $('#w_a_start').val();
        var w_end       = $('#w_a_end').val();
        var w_status    = $('#w_a_status').val();
        var w_title     = $('#w_a_title').val();
        var w_dep       = $('#w_a_dep').val();
        var w_user      = $('#w_a_user').val();
        var w_new_work_record_content  = CKEDITOR.instances.w_a_new_work_record_content.getData()
        
        var data  = w_date.split('-');
        var w_year  = data[0];
        var w_month = data[1];
        var w_day   = data[2];

        if(w_title.length == 0){
                exit();
        }else if(w_place.length == 0){
                exit();
        }else if(w_start.length == 0){
                exit();
        }else if(w_status.length == 0){
                exit();
        }else if(w_new_work_record_content == 0){
                exit();
        }else{
                $.ajax({
                        type:"POST",
                        url:"/submit_alter_new_work_record_form",
                        data:{
                               'w_year':w_year,
                               'w_month':w_month,
                               'w_day':w_day,
                               'w_place':w_place,
                               'w_start':w_start,
                               'w_end':w_end,
                               'w_status':w_status,
                               'w_title':w_title,
                               'w_dep':w_dep,
                               'w_user':w_user,
                               'w_new_work_record_content':w_new_work_record_content
                        },
                        datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
                                
                                // clean value
                                //$('#a_work_no').val('');
                                //$('#a_date').val('');
                                //$('#a_name').val('');
                                //$('#a_user').val('');
                                //$('#a_position').val('');
                                //$('#a_status').val('');
                                
                                $('#work_record_form_content').show(1000).html(res);
                                
                                // final update work record
                                update_final_work_record();
                                
                                // reload account list
                                //reload_menu_account_list();
                        },
                        beforeSend:function(){
                                $('#status').html("loading 送出修改新增工作進度表 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });     
        }
        
}

function alter_work_record_title(id){
        
        var title = id;

        $.ajax({
                type:"POST",
                url:"/alter_work_record_by_title",
                data:{
                        'title':title
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // clean value
                        //$('#a_work_no').val('');
                        //$('#a_date').val('');
                        //$('#a_name').val('');
                        //$('#a_user').val('');
                        //$('#a_position').val('');
                        //$('#a_status').val('');
                        $('#click_show_msg').click();
                        $('#show_msg').hide();
                        $('#work_record_form_content').show(1000).html(res);

                        // reload account list
                        //reload_menu_account_list();
                },
                beforeSend:function(){
                        $('#status').html("loading 修改工作進度表 - " + title + " ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        }); 

}

function del_work_record_title(id){
        
        var title = id;

        var check_del = prompt("刪除 " + title + " , 確定刪除 , 再按一次 y ");
        
	if(check_del == 'y'){	

                $.ajax({
                        type:"POST",
                        url:"/del_work_record_title",
                        data:{
                        'title':title
                        },
                        datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
                                
                                // clean value
                                //$('#a_work_no').val('');
                                //$('#a_date').val('');
                                //$('#a_name').val('');
                                //$('#a_user').val('');
                                //$('#a_position').val('');
                                //$('#a_status').val('');
                                $('#click_show_msg').click();
                                $('#show_msg').hide();
                                $('#work_record_form_content').show(1000).html(res);

                                
                                // reload account list
                                //reload_menu_account_list();
                        },
                        beforeSend:function(){
                                $('#status').html("loading 刪除工作進度表 - " + title + " ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                }); 
        }

}

function load_work_record_list_by_detail(id){
        
        var title = id;
        
        $.ajax({
                type:"POST",
                url:"/load_work_record_form_list_detail",
                data:{
                       'title':title
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // clean value
                        //$('#a_work_no').val('');
                        //$('#a_date').val('');
                        //$('#a_name').val('');
                        //$('#a_user').val('');
                        //$('#a_position').val('');
                        //$('#a_status').val('');
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);
                        //$('#work_record_form_content').show(1000).html(res);
                        
                        // reload account list
                        //reload_menu_account_list();
                },
                beforeSend:function(){
                        $('#status').html("loading 工作進度表 - " + title + " ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        }); 
}

function load_work_record_list_by_dep(id){
       
       var dep_id = id;

        $.ajax({
                type:"POST",
                url:"/load_work_record_form_list",
                data:{
                       'dep_id':dep_id
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // clean value
                        //$('#a_work_no').val('');
                        //$('#a_date').val('');
                        //$('#a_name').val('');
                        //$('#a_user').val('');
                        //$('#a_position').val('');
                        //$('#a_status').val('');
                        
                        $('#work_record_form_content').show(1000).html(res);
                        
                        // reload account list
                        //reload_menu_account_list();
                },
                beforeSend:function(){
                        $('#status').html("loading 工作進度表清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });           
}

function submit_add_new_work_record(){
        
        var w_date      = $('#w_date').val();
        var w_place     = $('#w_place').val();
        var w_start     = $('#w_start').val();
        var w_end       = $('#w_end').val();
        var w_status    = $('#w_status').val();
        var w_title     = $('#w_title').val();
        var w_dep       = $('#w_dep').val();
        var w_user      = $('#w_user').val();
        var w_new_work_record_content  = CKEDITOR.instances.w_new_work_record_content.getData()
        
        var data  = w_date.split('-');
        var w_year  = data[0];
        var w_month = data[1];
        var w_day   = data[2];

        if(w_title.length == 0){
                exit();
        }else if(w_place.length == 0){
                exit();
        }else if(w_start.length == 0){
                exit();
        }else if(w_status.length == 0){
                exit();
        }else if(w_new_work_record_content == 0){
                exit();
        }else{
                $.ajax({
                        type:"POST",
                        url:"/submit_add_new_work_record_form",
                        data:{
                               'w_year':w_year,
                               'w_month':w_month,
                               'w_day':w_day,
                               'w_place':w_place,
                               'w_start':w_start,
                               'w_end':w_end,
                               'w_status':w_status,
                               'w_title':w_title,
                               'w_dep':w_dep,
                               'w_user':w_user,
                               'w_new_work_record_content':w_new_work_record_content
                        },
                        datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
                                
                                // clean value
                                //$('#a_work_no').val('');
                                //$('#a_date').val('');
                                //$('#a_name').val('');
                                //$('#a_user').val('');
                                //$('#a_position').val('');
                                //$('#a_status').val('');
                                
                                $('#work_record_form_content').show(1000).html(res);
                                
                                // reload account list
                                //reload_menu_account_list();
                        },
                        beforeSend:function(){
                                $('#status').html("loading 建立新增工作進度表 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });     
        }
        
}

function load_work_record_form(){

        $.ajax({
                type:"POST",
                url:"/load_work_record_form",
                data:{
                        
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // go to top
                        goto_top()
                        
                        // show response content
                        $('#work_record_form_content').show(1000).html(res);
                        //$('#click_show_msg').click();
                        //$('#show_msg').show(1000).html(res);

                        // clean up
                        //$('#mrd_8_food_t').val("");
                        //$('#mrd_8_food_k').val("");
                },
                beforeSend:function(){
                        $('#status').html("loading 新增工作進度表 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });  

}

function mrd_8_del_auto_email_submit(){
        
        var mrd_8_add_auto_email  = $('#mrd_8_add_auto_email').val();    

        check_mail = validateEmail(mrd_8_add_auto_email);

        if(check_mail == true){

                $.ajax({
                        type:"POST",
                        url:"/mrd_8_del_auto_email_push",
                        data:{
                                'mrd_8_add_auto_email':mrd_8_add_auto_email                        
                        },
                        datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
                                
                                // go to top
                                goto_top()
                                
                                // show response content
                                //$('#data_list').show(1000).html(res);
                                $('#click_show_msg2').click();
                                $('#show_msg2').show(1000).html(res);

                                // clean up
                                //$('#mrd_8_food_t').val("");
                                //$('#mrd_8_food_k').val("");
                        },
                        beforeSend:function(){
                                $('#status').html("loading MRD 8 , 政府公開資料庫比對 , 公告自動 Email 通知 , 新增 Email 完成。").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                }); 
        }
        else{
                $('#show_msg3').show(1000).html("<span class='text-danger'><i class='bi bi-x-circle'></i> Email 格式錯誤 ! 請修正。</span>");
        }

}


function validateEmail(email) {
        let emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        return emailRegex.test(email);
}

function mrd_8_add_auto_email_submit(){
        
        var mrd_8_add_auto_email  = $('#mrd_8_add_auto_email').val();    

        check_mail = validateEmail(mrd_8_add_auto_email);

        if(check_mail == true){

                $.ajax({
                        type:"POST",
                        url:"/mrd_8_add_auto_email_push2",
                        data:{
                                'mrd_8_add_auto_email':mrd_8_add_auto_email                        
                        },
                        datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                                $('#click_show_msg').click();
                                $('#show_msg').show(1000).html(xhr.responseText);
                        },
                        success:function(res){
                                
                                // go to top
                                goto_top()
                                
                                // show response content
                                //$('#data_list').show(1000).html(res);
                                $('#click_show_msg2').click();
                                $('#show_msg2').show(1000).html(res);

                                // clean up
                                //$('#mrd_8_food_t').val("");
                                //$('#mrd_8_food_k').val("");
                        },
                        beforeSend:function(){
                                $('#status').html("loading MRD 8 , 政府公開資料庫比對 , 公告自動 Email 通知 , 新增 Email 完成。").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                }); 
        }
        else{
                $('#show_msg3').show(1000).html("<span class='text-danger'><i class='bi bi-x-circle'></i> Email 格式錯誤 ! 請修正。</span>");
        }

}

function mrd_8_add_auto_email_push(){

        $.ajax({
                type:"POST",
                url:"/mrd_8_add_auto_email_push",
                data:{
                        
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // go to top
                        goto_top()
                        
                        // show response content
                        //$('#data_list').show(1000).html(res);
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);

                        // clean up
                        //$('#mrd_8_food_t').val("");
                        //$('#mrd_8_food_k').val("");
                },
                beforeSend:function(){
                        $('#status').html("loading MRD 8 , 政府公開資料庫比對 , 公告自動 Email 通知 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });  
}

function mrd_8_food_8_all_search_submit(){

        var mrd_8_food_8_all_search_k  = $('#mrd_8_food_8_all_search_k').val();

        $.ajax({
                type:"POST",
                url:"/mrd_8_food_8_all_search_submit",
                data:{
                        'mrd_8_food_8_all_search_k':mrd_8_food_8_all_search_k 
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // go to top
                        goto_top()
                        
                        // show response content
                        //$('#data_list').show(1000).html(res);
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);

                        // clean up
                        //$('#mrd_8_food_t').val("");
                        //$('#mrd_8_food_k').val("");
                },
                beforeSend:function(){
                        $('#status').html("loading MRD 8 , 統一搜尋入口 整合查詢服務 , 搜尋清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function query_account(){
        
        var query_account = $('#query_account').val();

        $.ajax({
                type:"POST",
                url:"/query_account",
                data:{
                        'query_account':query_account
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // go to top
                        goto_top()
                        
                        // show response content
                        $('#search_val').show(1000).html(res);
                        //$('#click_show_msg').click();
                        //$('#show_msg').show(1000).html(res);

                        // clean up
                        //$('#mrd_8_food_t').val("");
                        //$('#mrd_8_food_k').val("");
                },
                beforeSend:function(){
                        $('#status').html("loading 帳號 : " + query_account  +  " ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });                 
}

function close_page(){
        window.close();
}

function mrd_8_query_announcement_submit(){
        var mrd_8_query_announcement_year    = $('#mrd_8_query_announcement_year').val();
        var mrd_8_query_announcement_item    = $('#mrd_8_query_announcement_item').val();
        var mrd_8_query_announcement_keyword = $('#mrd_8_query_announcement_keyword').val();

        $.ajax({
                type:"POST",
                url:"/mrd_8_query_announcement_submit",
                data:{
                        'mrd_8_query_announcement_year':mrd_8_query_announcement_year,
                        'mrd_8_query_announcement_item':mrd_8_query_announcement_item, 
                        'mrd_8_query_announcement_keyword':mrd_8_query_announcement_keyword
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // go to top
                        goto_top()
                        
                        // show response content
                        //$('#data_list').show(1000).html(res);
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);

                        // clean up
                        //$('#mrd_8_food_t').val("");
                        //$('#mrd_8_food_k').val("");
                },
                beforeSend:function(){
                        $('#status').html("loading MRD 8 , 衛生福利部食品藥物管理署 公告 , 搜尋清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });                 
}

function mrd_8_cosmetic_query_ingredients_prohibited_submit(){
        
        var mrd_8_cosmetic_query_ingredients_prohibited_k   = $('#mrd_8_cosmetic_query_ingredients_prohibited_k').val();

        $.ajax({
                type:"POST",
                url:"/mrd_8_cosmetic_query_ingredients_prohibited_submit",
                data:{
                        'mrd_8_cosmetic_query_ingredients_prohibited_k':mrd_8_cosmetic_query_ingredients_prohibited_k
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // go to top
                        goto_top()
                        
                        // show response content
                        //$('#data_list').show(1000).html(res);
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);

                        // clean up
                        //$('#mrd_8_food_t').val("");
                        //$('#mrd_8_food_k').val("");
                },
                beforeSend:function(){
                        $('#status').html("loading MRD 8 , 化粧品禁限用成分管理規定 , 搜尋清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });         
}

function mrd_8_food_query_infant_formula_submit(){
        
        var mrd_8_food_query_infant_formula_ct  = $('#mrd_8_food_query_infant_formula_ct').val();
        var mrd_8_food_query_infant_formula_cn  = $('#mrd_8_food_query_infant_formula_cn').val();
        var mrd_8_food_query_infant_formula_en  = $('#mrd_8_food_query_infant_formula_en').val();
        var mrd_8_food_query_infant_formula_cp  = $('#mrd_8_food_query_infant_formula_cp').val();
        var mrd_8_food_query_infant_formula_ph1 = $('#mrd_8_food_query_infant_formula_ph1').val();
        var mrd_8_food_query_infant_formula_ph2 = $('#mrd_8_food_query_infant_formula_ph2').val();
        var mrd_8_food_query_infant_formula_ph3 = $('#mrd_8_food_query_infant_formula_ph3').val();
        var mrd_8_food_query_infant_formula_k   = $('#mrd_8_food_query_infant_formula_k').val();

        $.ajax({
                type:"POST",
                url:"/mrd_8_food_query_infant_formula_submit",
                data:{
                        'mrd_8_food_query_infant_formula_ct':mrd_8_food_query_infant_formula_ct, 
                        'mrd_8_food_query_infant_formula_cn':mrd_8_food_query_infant_formula_cn, 
                        'mrd_8_food_query_infant_formula_en':mrd_8_food_query_infant_formula_en, 
                        'mrd_8_food_query_infant_formula_cp':mrd_8_food_query_infant_formula_cp, 
                        'mrd_8_food_query_infant_formula_ph1':mrd_8_food_query_infant_formula_ph1, 
                        'mrd_8_food_query_infant_formula_ph2':mrd_8_food_query_infant_formula_ph2, 
                        'mrd_8_food_query_infant_formula_ph3':mrd_8_food_query_infant_formula_ph3, 
                        'mrd_8_food_query_infant_formula_k':mrd_8_food_query_infant_formula_k
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // go to top
                        goto_top()
                        
                        // show response content
                        //$('#data_list').show(1000).html(res);
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);

                        // clean up
                        //$('#mrd_8_food_t').val("");
                        //$('#mrd_8_food_k').val("");
                },
                beforeSend:function(){
                        $('#status').html("loading MRD 8 , 嬰兒與較大嬰兒配方食品許可資料查詢 , 搜尋清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });        
}

function mrd_8_food_query_genetic_modification_submit(){

        var mrd_8_food_query_genetic_modification_t  = $('#mrd_8_food_query_genetic_modification_t').val();
        var mrd_8_food_query_genetic_modification_t2 = $('#mrd_8_food_query_genetic_modification_t2').val();
        var mrd_8_food_query_genetic_modification_pn = $('#mrd_8_food_query_genetic_modification_pn').val();
        var mrd_8_food_query_genetic_modification_an = $('#mrd_8_food_query_genetic_modification_an').val();
        var mrd_8_food_query_genetic_modification_sd = $('#mrd_8_food_query_genetic_modification_sd').val();
        var mrd_8_food_query_genetic_modification_ed = $('#mrd_8_food_query_genetic_modification_ed').val();
        var mrd_8_food_query_genetic_modification_k  = $('#mrd_8_food_query_genetic_modification_k').val();

        $.ajax({
                type:"POST",
                url:"/mrd_8_food_query_genetic_modification_submit",
                data:{
                        'mrd_8_food_query_genetic_modification_t':mrd_8_food_query_genetic_modification_t, 
                        'mrd_8_food_query_genetic_modification_t2':mrd_8_food_query_genetic_modification_t2, 
                        'mrd_8_food_query_genetic_modification_pn':mrd_8_food_query_genetic_modification_pn, 
                        'mrd_8_food_query_genetic_modification_an':mrd_8_food_query_genetic_modification_an, 
                        'mrd_8_food_query_genetic_modification_sd':mrd_8_food_query_genetic_modification_sd, 
                        'mrd_8_food_query_genetic_modification_ed':mrd_8_food_query_genetic_modification_ed, 
                        'mrd_8_food_query_genetic_modification_k':mrd_8_food_query_genetic_modification_k
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // go to top
                        goto_top()
                        
                        // show response content
                        //$('#data_list').show(1000).html(res);
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);

                        // clean up
                        //$('#mrd_8_food_t').val("");
                        //$('#mrd_8_food_k').val("");
                },
                beforeSend:function(){
                        $('#status').html("loading MRD 8 , 衛生福利部審核通過之基因改造食品原料之查詢 , 搜尋清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function mrd_8_food_query_domestic_vitamins_submit(){

        var mrd_8_food_query_domestic_vitamins_ct  = $('#mrd_8_food_query_domestic_vitamins_ct').val();
        var mrd_8_food_query_domestic_vitamins_cn  = $('#mrd_8_food_query_domestic_vitamins_cn').val();
        var mrd_8_food_query_domestic_vitamins_en  = $('#mrd_8_food_query_domestic_vitamins_en').val();
        var mrd_8_food_query_domestic_vitamins_cp  = $('#mrd_8_food_query_domestic_vitamins_cp').val();
        var mrd_8_food_query_domestic_vitamins_ph1 = $('#mrd_8_food_query_domestic_vitamins_ph1').val();
        var mrd_8_food_query_domestic_vitamins_ph2 = $('#mrd_8_food_query_domestic_vitamins_ph2').val();
        var mrd_8_food_query_domestic_vitamins_ph3 = $('#mrd_8_food_query_domestic_vitamins_ph3').val();
        var mrd_8_food_query_domestic_vitamins_k   = $('#mrd_8_food_query_domestic_vitamins_k').val();

        $.ajax({
                type:"POST",
                url:"/mrd_8_food_query_domestic_vitamins_submit",
                data:{
                        'mrd_8_food_query_domestic_vitamins_ct':mrd_8_food_query_domestic_vitamins_ct, 
                        'mrd_8_food_query_domestic_vitamins_cn':mrd_8_food_query_domestic_vitamins_cn,
                        'mrd_8_food_query_domestic_vitamins_en':mrd_8_food_query_domestic_vitamins_en,
                        'mrd_8_food_query_domestic_vitamins_cp':mrd_8_food_query_domestic_vitamins_cp,
                        'mrd_8_food_query_domestic_vitamins_ph1':mrd_8_food_query_domestic_vitamins_ph1,
                        'mrd_8_food_query_domestic_vitamins_ph2':mrd_8_food_query_domestic_vitamins_ph2,
                        'mrd_8_food_query_domestic_vitamins_ph3':mrd_8_food_query_domestic_vitamins_ph3,
                        'mrd_8_food_query_domestic_vitamins_k':mrd_8_food_query_domestic_vitamins_k
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // go to top
                        goto_top()
                        
                        // show response content
                        //$('#data_list').show(1000).html(res);
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);

                        // clean up
                        //$('#mrd_8_food_t').val("");
                        //$('#mrd_8_food_k').val("");
                },
                beforeSend:function(){
                        $('#status').html("loading MRD 8 , 國產維生素類錠狀膠囊狀食品查驗登記證資料查詢 , 搜尋清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });

}

function mrd_8_food_query_enter_capsule_submit(){
        
        var mrd_8_food_query_enter_capsule_ct  = $('#mrd_8_food_query_enter_capsule_ct').val();
        var mrd_8_food_query_enter_capsule_cn  = $('#mrd_8_food_query_enter_capsule_cn').val();
        var mrd_8_food_query_enter_capsule_en  = $('#mrd_8_food_query_enter_capsule_en').val();
        var mrd_8_food_query_enter_capsule_cp  = $('#mrd_8_food_query_enter_capsule_cp').val();
        var mrd_8_food_query_enter_capsule_ph1 = $('#mrd_8_food_query_enter_capsule_ph1').val();
        var mrd_8_food_query_enter_capsule_ph2 = $('#mrd_8_food_query_enter_capsule_ph2').val();
        var mrd_8_food_query_enter_capsule_ph3 = $('#mrd_8_food_query_enter_capsule_ph3').val();
        var mrd_8_food_query_enter_capsule_k   = $('#mrd_8_food_query_enter_capsule_k').val();

        $.ajax({
                type:"POST",
                url:"/mrd_8_food_query_enter_capsule_submit",
                data:{
                        'mrd_8_food_query_enter_capsule_ct':mrd_8_food_query_enter_capsule_ct, 
                        'mrd_8_food_query_enter_capsule_cn':mrd_8_food_query_enter_capsule_cn,
                        'mrd_8_food_query_enter_capsule_en':mrd_8_food_query_enter_capsule_en,
                        'mrd_8_food_query_enter_capsule_cp':mrd_8_food_query_enter_capsule_cp,
                        'mrd_8_food_query_enter_capsule_ph1':mrd_8_food_query_enter_capsule_ph1,
                        'mrd_8_food_query_enter_capsule_ph2':mrd_8_food_query_enter_capsule_ph2,
                        'mrd_8_food_query_enter_capsule_ph3':mrd_8_food_query_enter_capsule_ph3,
                        'mrd_8_food_query_enter_capsule_k':mrd_8_food_query_enter_capsule_k
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // go to top
                        goto_top()
                        
                        // show response content
                        //$('#data_list').show(1000).html(res);
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);

                        // clean up
                        //$('#mrd_8_food_t').val("");
                        //$('#mrd_8_food_k').val("");
                },
                beforeSend:function(){
                        $('#status').html("loading MRD 8 , 輸入膠囊錠狀食品核備查詢 , 搜尋清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });

}


function mrd_8_food_query_disease_recipe_submit(){
        
        var mrd_8_food_query_disease_recipe_t   = $('#mrd_8_food_query_disease_recipe_t').val();
        var mrd_8_food_query_disease_recipe_ct  = $('#mrd_8_food_query_disease_recipe_ct').val();
        var mrd_8_food_query_disease_recipe_cn  = $('#mrd_8_food_query_disease_recipe_cn').val();
        var mrd_8_food_query_disease_recipe_en  = $('#mrd_8_food_query_disease_recipe_en').val();
        var mrd_8_food_query_disease_recipe_cp  = $('#mrd_8_food_query_disease_recipe_cp').val();
        var mrd_8_food_query_disease_recipe_ph1 = $('#mrd_8_food_query_disease_recipe_ph1').val();
        var mrd_8_food_query_disease_recipe_ph2 = $('#mrd_8_food_query_disease_recipe_ph2').val();
        var mrd_8_food_query_disease_recipe_ph3 = $('#mrd_8_food_query_disease_recipe_ph3').val();
        var mrd_8_food_query_disease_recipe_k   = $('#mrd_8_food_query_disease_recipe_k').val();

        $.ajax({
                type:"POST",
                url:"/mrd_8_food_query_disease_recipe_submit",
                data:{
                        'mrd_8_food_query_disease_recipe_t':mrd_8_food_query_disease_recipe_t,
                        'mrd_8_food_query_disease_recipe_ct':mrd_8_food_query_disease_recipe_ct,
                        'mrd_8_food_query_disease_recipe_cn':mrd_8_food_query_disease_recipe_cn,
                        'mrd_8_food_query_disease_recipe_en':mrd_8_food_query_disease_recipe_en,
                        'mrd_8_food_query_disease_recipe_cp':mrd_8_food_query_disease_recipe_cp,
                        'mrd_8_food_query_disease_recipe_ph1':mrd_8_food_query_disease_recipe_ph1,
                        'mrd_8_food_query_disease_recipe_ph2':mrd_8_food_query_disease_recipe_ph2,
                        'mrd_8_food_query_disease_recipe_ph3':mrd_8_food_query_disease_recipe_ph3,
                        'mrd_8_food_query_disease_recipe_k':mrd_8_food_query_disease_recipe_k
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // go to top
                        goto_top()
                        
                        // show response content
                        //$('#data_list').show(1000).html(res);
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);

                        // clean up
                        //$('#mrd_8_food_t').val("");
                        //$('#mrd_8_food_k').val("");
                },
                beforeSend:function(){
                        $('#status').html("loading MRD 8 , 特定疾病配方食品 , 搜尋清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });

}

function mrd_8_food_query_pass_submit(){
        
        var mrd_8_food_query_pass_t   = $('#mrd_8_food_query_pass_t').val();
        var mrd_8_food_query_pass_Tid = $('#mrd_8_food_query_pass_Tid').val();
        var mrd_8_food_query_pass_Cop = $('#mrd_8_food_query_pass_Cop').val();
        var mrd_8_food_query_pass_Cna = $('#mrd_8_food_query_pass_Cna').val();
        var mrd_8_food_query_pass_t2  = $('#mrd_8_food_query_pass_t2').val();
        var mrd_8_food_query_pass_k   = $('#mrd_8_food_query_pass_k').val();

        $.ajax({
                type:"POST",
                url:"/mrd_8_food_query_pass_submit",
                data:{
                        'mrd_8_food_query_pass_t':mrd_8_food_query_pass_t,
                        'mrd_8_food_query_pass_Tid':mrd_8_food_query_pass_Tid,
                        'mrd_8_food_query_pass_Cop':mrd_8_food_query_pass_Cop,
                        'mrd_8_food_query_pass_Cna':mrd_8_food_query_pass_Cna,
                        'mrd_8_food_query_pass_t2':mrd_8_food_query_pass_t2,
                        'mrd_8_food_query_pass_k':mrd_8_food_query_pass_k
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // go to top
                        goto_top()
                        
                        // show response content
                        //$('#data_list').show(1000).html(res);
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);

                        // clean up
                        //$('#mrd_8_food_t').val("");
                        //$('#mrd_8_food_k').val("");
                },
                beforeSend:function(){
                        $('#status').html("loading MRD 8 , 食品原料整合查詢平臺 , 搜尋清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });

}

function mrd_8_food_query_platform_submit(){
        
        var mrd_8_food_query_platform_c  = $('#mrd_8_food_query_platform_c').val();
        var mrd_8_food_query_platform_t  = $('#mrd_8_food_query_platform_t').val();
        var mrd_8_food_query_platform_k  = $('#mrd_8_food_query_platform_k').val();

        $.ajax({
                type:"POST",
                url:"/mrd_8_food_query_platform_submit",
                data:{
                        'mrd_8_food_query_platform_c':mrd_8_food_query_platform_c,
                        'mrd_8_food_query_platform_t':mrd_8_food_query_platform_t,
                        'mrd_8_food_query_platform_k':mrd_8_food_query_platform_k
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // go to top
                        goto_top()
                        
                        // show response content
                        //$('#data_list').show(1000).html(res);

                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);
                        
                        // clean up
                        //$('#mrd_8_food_t').val("");
                        //$('#mrd_8_food_k').val("");
                },
                beforeSend:function(){
                        $('#status').html("loading MRD 8 , 食品原料整合查詢平臺 , 搜尋清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });

}

function mrd_8_license_submit(){
        
        var mrd_8_license_ct  = $('#mrd_8_license_ct').val();
        var mrd_8_license_cn  = $('#mrd_8_license_cn').val();
        var mrd_8_license_en  = $('#mrd_8_license_en').val();
        var mrd_8_license_cp  = $('#mrd_8_license_cp').val();
        var mrd_8_license_ph1 = $('#mrd_8_license_ph1').val();
        var mrd_8_license_ph2 = $('#mrd_8_license_ph2').val();
        var mrd_8_license_ph3 = $('#mrd_8_license_ph3').val();
        var mrd_8_license_k   = $('#mrd_8_license_k').val();

        $.ajax({
                type:"POST",
                url:"/mrd_8_license_submit",
                data:{
                        'mrd_8_license_ct':mrd_8_license_ct,
                        'mrd_8_license_cn':mrd_8_license_cn,
                        'mrd_8_license_en':mrd_8_license_en,
                        'mrd_8_license_cp':mrd_8_license_cp,
                        'mrd_8_license_ph1':mrd_8_license_ph1,
                        'mrd_8_license_ph2':mrd_8_license_ph2,
                        'mrd_8_license_ph3':mrd_8_license_ph3,
                        'mrd_8_license_k':mrd_8_license_k
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // go to top
                        goto_top()
                        
                        // show response content
                        //$('#data_list').show(1000).html(res);
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);

                        // clean up
                        //$('#mrd_8_food_t').val("");
                        //$('#mrd_8_food_k').val("");
                },
                beforeSend:function(){
                        $('#status').html("loading MRD 8 , 食品添加物許可證資料查詢 , 搜尋清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });

}

function mrd_8_food_submit(){
        
        var mrd_8_food_t = $('#mrd_8_food_t').val();
        var mrd_8_food_k = $('#mrd_8_food_k').val();

        $.ajax({
                type:"POST",
                url:"/mrd_8_food_submit",
                data:{
                        'mrd_8_food_t':mrd_8_food_t,
                        'mrd_8_food_k':mrd_8_food_k
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // go to top
                        goto_top()
                        
                        // show response content
                        //$('#data_list').show(1000).html(res);
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);

                        // clean up
                        //$('#mrd_8_food_t').val("");
                        //$('#mrd_8_food_k').val("");
                },
                beforeSend:function(){
                        $('#status').html("loading MRD 8 , 食品添加物使用範圍及限量暨規格標準 , 搜尋清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });

}

function load_dep_detail2(val){
        
        var data = val.split('_');
        var show_dep_detail2 = '#dep2_' + data[0];
        var dep2 = data[0];
        var dep2_name = data[1];

        $.ajax({
                type:"POST",
                url:"/load_dep_detail2",
                data:{
                        'dep2':dep2,
                        'dep2_name':dep2_name
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
                        
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                      
                        //alert(xhr.status);
                        //alert(xhr.responseText);
                        //alert(throwError);
                        //alert(ajaxError);
                },
                success:function(res){
                        
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(res);
                        //$(show_dep_detail2).show(1000).html(res);
                },
                beforeSend:function(){
                        $('#status').html("load department 清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function load_dep_detail(dep){
        
        var show_dep_detail = '#dep_' + dep;

        $.ajax({
                type:"POST",
                url:"/load_dep_detail",
                data:{
                        'dep':dep
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $(show_dep_detail).show(1000).html(res);
                },
                beforeSend:function(){
                        $('#status').html("load department 清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function annual_budget_year_detail(val){
        
        var show = "#" + val + "_detail";

        $.ajax({
                type:"POST",
                url:"/load_annual_budget_year_detail",
                data:{
                        'year':val
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        // refresh it annual budget year total
                        $(show).show(1000).html(res);
                },
                beforeSend:function(){
                        $('#status').html("load IT 年度預算清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });                
}

function reload_it_annual_budget_add_form(){
        $.ajax({
                type:"GET",
                url:"/reload_it_annual_budget_add_form",
                data:{},
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                },
                success:function(res){
                        
                        // refresh it annual budget year total
                        $('#it_annual_budget_add_form').show(1000).html(res);
                },
                beforeSend:function(){
                        $('#status').html("reload IT 年度預算表新增表 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });                
}

function reload_it_annual_budget_year_total(){
        $.ajax({
                type:"POST",
                url:"/reload_it_annual_budget_year_total",
                data:{},
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                },
                success:function(res){
                        
                        // refresh it annual budget year total
                        $('#it_annual_budget_year_total').show(1000).html(res);
                },
                beforeSend:function(){
                        $('#status').html("reload IT 年度預算表總計 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });                
}

function select_it_annual_budget_otsuka_holdings(){
        
        var select_otsuka_holdings = $('#it_annual_budget_select_otsuka_holdings').val();
        $('#it_annual_budget_otsuka_holdings').val(select_otsuka_holdings);
        
}

function select_it_annual_budget_kind(){
        
        var select_kind = $('#it_annual_budget_select_kind').val();
        $('#it_annual_budget_kind').val(select_kind);

}

function submit_it_annual_budget(){
      
        // IT 年度預算日期
        var it_annual_budget_date = $("#it_annual_budget_date").val();
        it_annual_budget_date     = $.trim(it_annual_budget_date);
        // IT 年度預算年度
        var it_annual_budget_build_year = $("#it_annual_budget_build_year").val();
        it_annual_budget_build_year     = $.trim(it_annual_budget_build_year);
        // IT 年度預算種類
        var it_annual_budget_kind = $("#it_annual_budget_kind").val();
        it_annual_budget_kind     = $.trim(it_annual_budget_kind);
        // IT 年度預算項目
        var it_annual_budget_title = $("#it_annual_budget_title").val();
        it_annual_budget_title     = $.trim(it_annual_budget_title);
        // IT 年度預算 otsuka holdings
        var it_annual_budget_otsuka_holdings = $("#it_annual_budget_otsuka_holdings").val();
        it_annual_budget_otsuka_holdings     = $.trim(it_annual_budget_otsuka_holdings);
        // IT 年度預算
        var it_annual_budget_year = $("#it_annual_budget_year").val();
        it_annual_budget_year     = $.trim(it_annual_budget_year);
        // IT 年度預算 目前剩餘金額
        var it_annual_budget_remaining_now = $("#it_annual_budget_remaining_now").val();
        it_annual_budget_remaining_now     = $.trim(it_annual_budget_remaining_now);
        // IT 年度預算 備註
        var it_annual_budget_comment = $("#it_annual_budget_comment").val();
        it_annual_budget_comment     = $.trim(it_annual_budget_comment);

        // IT 年度預算日期
        if (it_annual_budget_date == ""){
                $('#check_it_annual_budget_date').toast('show');
                exit()
        }
        // IT 年度預算年度
        else if (it_annual_budget_build_year == ""){
                $('#check_it_annual_budget_build_year').toast('show');
                exit()
        }
        // IT 年度預算種類
        else if (it_annual_budget_kind == ""){
                $('#check_it_annual_budget_kind').toast('show');
                exit()
        }
        // IT 年度預算項目
        else if (it_annual_budget_title == ""){
                $('#check_it_annual_budget_title').toast('show');
                exit()
        }
        // IT 年度預算 otsuka holdings
        else if (it_annual_budget_otsuka_holdings == ""){
                $('#check_it_annual_budget_otsuka_holdings').toast('show');
                exit()
        }
        // IT 年度預算
        else if (it_annual_budget_year == ""){
                $('#check_it_annual_budget_year').toast('show');
                exit()
        }
        // IT 年度預算 目前剩餘金額
        else if (it_annual_budget_remaining_now == ""){
                $('#check_it_annual_budget_remaining_now').toast('show');
                exit()
        }
        // submit 
        else{
                
                $.ajax({
                        type:"POST",
                        url:"/submit_it_annual_budget",
                        data:{
                                'it_annual_budget_date':it_annual_budget_date,   
                                'it_annual_budget_build_year':it_annual_budget_build_year,   
                                'it_annual_budget_kind':it_annual_budget_kind,   
                                'it_annual_budget_title':it_annual_budget_title,   
                                'it_annual_budget_otsuka_holdings':it_annual_budget_otsuka_holdings,   
                                'it_annual_budget_year':it_annual_budget_year,   
                                'it_annual_budget_remaining_now':it_annual_budget_remaining_now,
                                'it_annual_budget_comment':it_annual_budget_comment
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
                                alert(xhr.status);
                                alert(xhr.responseText);
                                alert(throwError);
                                alert(ajaxError);
                        },
                        success:function(res){
                                
                                // refresh 
                                reload_it_annual_budget_year_total(); // reload IT 年度預算表總計
                                reload_it_annual_budget_add_form();   // reload IT 年度預算表新增表
                                
                                $('#submit_it_annual_budget').toast('show');

                                // clean up fields
                                $("#it_annual_budget_date").val("");
                                $("#it_annual_budget_kind").val("");
                                $("#it_annual_budget_title").val("");
                                $("#it_annual_budget_otsuka_holdings").val("");
                                $("#it_annual_budget_year").val("");
                                $("#it_annual_budget_remaining_now").val("");
                                $("#it_annual_budget_comment").val("");

                                //$("#computer_user_detail").show(1000).html(res);
                                //$("#show_day_month_detail").show(1000).html(res);
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("顯示 IT 年度預算資料 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });
        }
      
}

function card_reader_download_excel(val){
        
        var data      = val.split('/');
        var position  = data[0];
        var day       = data[1];

        $.ajax({
                type:"POST",
                url:"/card_reader_download_excel",
                data:{
                        'position':position,
                        'day':day
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $('#card_reader_detail_list').show(1000).html(res);

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示 " + position + "  " + day  + " 門禁刷卡資訊資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function card_reader_download_pdf_by_month(val){
        
        var data      = val.split('/');
        var position  = data[0];
        var month     = data[1];
        var item      = data[2];
        
        $.ajax({
                type:"POST",
                url:"/card_reader_download_pdf_by_month",
                data:{
                        'position':position,
                        'month':month
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        if (item == 'excel'){
                                var url = "/download_card_reader_excel_by_month?position="+position+"&month="+month;
                                var fileName = 'card_reader_' + position + '_' + month + '.xlsx';

                                // 创建一个动态链接并触发点击
                                var link = $('<a></a>')
                                        .attr('href', url)
                                        .attr('download', fileName)
                                        .appendTo('body');

                                link[0].click();
                                link.remove(); // 清理动态创建的元素
                        }else if(item == 'pdf'){
                                var url = "/download_card_reader_excel_by_month?position="+position+"&month="+month;
                                var fileName = 'card_reader_' + position + '_' + month + '.pdf';

                                // 创建一个动态链接并触发点击
                                var link = $('<a></a>')
                                        .attr('href', url)
                                        .attr('download', fileName)
                                        .appendTo('body');

                                link[0].click();
                                link.remove(); // 清理动态创建的元素
                        }
                        
                        //$('#card_reader_detail_list').show(1000).html(res);
                        //alert(position + '_' + day + ' download successful.');

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示 " + position + "  " + month  + " 月 , 門禁刷卡資訊資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function card_reader_download_pdf_every_month(val){
        
        var data      = val.split('/');
        var position  = data[0];
        var tb        = data[1];
        var item      = data[2];

        $.ajax({
                type:"POST",
                url:"/card_reader_download_pdf_every_month",
                data:{
                        'position':position,
                        'tb':tb
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        var data = tb.split('_');
                        
                        if (item == 'excel'){
                                var url = "/download_card_reader_excel_every_month?position="+position+"&tb="+tb;
                                var fileName = tb + '_' + position + '.xlsx';

                                // 创建一个动态链接并触发点击
                                var link = $('<a></a>')
                                        .attr('href', url)
                                        .attr('download', fileName)
                                        .appendTo('body');

                                link[0].click();
                                link.remove(); // 清理动态创建的元素
                        }else if(item == 'pdf'){
                                var url = "/download_card_reader_excel_every_month?position="+position+"&tb="+tb;
                                var fileName = tb + '_' + position + '.pdf';

                                // 创建一个动态链接并触发点击
                                var link = $('<a></a>')
                                        .attr('href', url)
                                        .attr('download', fileName)
                                        .appendTo('body');

                                link[0].click();
                                link.remove(); // 清理动态创建的元素
                        }
                        
                        //$('#card_reader_detail_list').show(1000).html(res);
                        //alert(position + '_' + day + ' download successful.');

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示 " + tb + '_' + position + " 門禁刷卡資訊資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function card_reader_download_pdf(val){
        
        var data      = val.split('/');
        var position  = data[0];
        var day       = data[1];
        var item      = data[2];

        $.ajax({
                type:"POST",
                url:"/card_reader_download_pdf",
                data:{
                        'position':position,
                        'day':day
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        if (item == 'excel'){
                                var url = "/download_card_reader_excel?position="+position+"&day="+day;
                                var fileName = 'card_reader_' + position + '_' + day + '.xlsx';

                                // 创建一个动态链接并触发点击
                                var link = $('<a></a>')
                                        .attr('href', url)
                                        .attr('download', fileName)
                                        .appendTo('body');

                                link[0].click();
                                link.remove(); // 清理动态创建的元素
                        }else if(item == 'pdf'){
                                var url = "/download_card_reader_excel?position="+position+"&day="+day;
                                var fileName = 'card_reader_' + position + '_' + day + '.pdf';

                                // 创建一个动态链接并触发点击
                                var link = $('<a></a>')
                                        .attr('href', url)
                                        .attr('download', fileName)
                                        .appendTo('body');

                                link[0].click();
                                link.remove(); // 清理动态创建的元素
                        }
                        
                        //$('#card_reader_detail_list').show(1000).html(res);
                        //alert(position + '_' + day + ' download successful.');

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示 " + position + "  " + day  + " 門禁刷卡資訊資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function load_card_reader_list_by_every_month(val){
        
        var data      = val.split('/');
        var position  = data[0];
        var tb        = data[1];

        $.ajax({
                type:"POST",
                url:"/load_card_reader_list_by_every_month",
                data:{
                        'position':position,
                        'tb':tb
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $('#card_reader_detail_list').show(1000).html(res);

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示 " + position + " , " + tb  + " 門禁刷卡資訊資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function load_card_reader_list_by_day(val){
        
        var data      = val.split('/');
        var position  = data[0];
        var day       = data[1];

        $.ajax({
                type:"POST",
                url:"/load_card_reader_list_by_day",
                data:{
                        'position':position,
                        'day':day
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $('#card_reader_detail_list').show(1000).html(res);

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示 " + position + "  " + day  + " 門禁刷卡資訊資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function vmware_detail(val){
        
        var vm_name = val;

        $.ajax({
                type:"POST",
                url:"/vmware_detail",
                data:{
                        'vm_name':vm_name
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $('#vmware_detail').show(1000).html(res);

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示VMware " + vm_name + " 資訊資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function query_device(){
        
        // query device
        var query_device_no = $("#query_device").val();

        if(query_device_no.length > 1){
                $.ajax({
                        type:"POST",
                        url:"/show_query_device",
                        data:{
                                'query_device_no':query_device_no
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
                                alert(xhr.status);
                                alert(xhr.responseText);
                                alert(throwError);
                                alert(ajaxError);
                        },
                        success:function(res){
                                
                                $('#query_device_list').show(1000).html(res);
        
                                //$("#computer_user_detail").show(1000).html(res);
                                //$("#show_day_month_detail").show(1000).html(res);
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("顯示固資清單資料 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });
        }
        
}



function query_contract(){
        
        // query contract
        var query_contract = $("#query_contract").val();
        query_contract = $.trim(query_contract); 

        $.ajax({
                type:"POST",
                url:"/query_otsuka_contract",
                data:{
                        'query_contract':query_contract
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $('#submit_otsuka_contract').toast('show');

                        // clean up fields
                        $("#o_c_date").val("");
                        $("#o_c_kind").val("");
                        $("#o_c_title").val("");
                        $("#o_c_cost").val("");
                        $("#o_c_time").val("");
                        $("#o_c_company").val("");
                        $("#o_c_name").val("");
                        $("#o_c_telephone").val("");
                        $("#o_c_phone").val("");
                        $("#o_c_comment").val("");

                        //$("#computer_user_detail").show(1000).html(res);
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示合約資訊資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function submit_otsuka_contract(){
      
        // 合約日期
        var o_c_date = $("#o_c_date").val();
        o_c_date = $.trim(o_c_date);
        // 合約種類
        var o_c_kind = $("#o_c_kind").val();
        o_c_kind = $.trim(o_c_kind);
        // 合約名稱
        var o_c_title = $("#o_c_title").val();
        o_c_title = $.trim(o_c_title);
        // 合約金額
        var o_c_cost = $("#o_c_cost").val();
        o_c_cost = $.trim(o_c_cost);
        // 合約時間
        var o_c_time = $("#o_c_time").val();
        o_c_time = $.trim(o_c_time);
        // 合約公司
        var o_c_company = $("#o_c_company").val();
        o_c_company = $.trim(o_c_company);
        // 合約窗口
        var o_c_name = $("#o_c_name").val();
        o_c_name = $.trim(o_c_name);
        // 合約窗口電話
        var o_c_telephone = $("#o_c_telephone").val();
        o_c_telephone = $.trim(o_c_telephone);
        // 合約窗口手機
        var o_c_phone = $("#o_c_phone").val();
        o_c_phone = $.trim(o_c_phone);
        // 合約備註
        var o_c_comment = $("#o_c_comment").val();
        o_c_comment = $.trim(o_c_comment);
        

        // 合約日期
        if (o_c_date == ""){
                $('#check_o_c_date').toast('show');
                exit()
        }
        // 合約種類
        else if (o_c_kind == ""){
                $('#check_o_c_kind').toast('show');
                exit()
        }
        // 合約名稱
        else if (o_c_title == ""){
                $('#check_o_c_title').toast('show');
                exit()
        }
        // 合約金額
        else if (o_c_cost == ""){
                $('#check_o_c_cost').toast('show');
                exit()
        }
        // 合約時間
        else if (o_c_time == ""){
                $('#check_o_c_time').toast('show');
                exit()
        }
        // 合約公司
        else if (o_c_company == ""){
                $('#check_o_c_company').toast('show');
                exit()
        }
        // 合約窗口
        else if (o_c_name == ""){
                $('#check_o_c_name').toast('show');
                exit()
        }
        // 合約窗口電話
        else if (o_c_telephone == ""){
                $('#check_o_c_telephone').toast('show');
                exit()
        }
        // 合約窗口手機
        else if (o_c_phone == ""){
                $('#check_o_c_phone').toast('show');
                exit()
        }
        // 合約備註
        else if (o_c_comment == ""){
                $('#check_o_c_comment').toast('show');
                exit()
        }
        // submit otsuka contract
        else{

                $.ajax({
                        type:"POST",
                        url:"/submit_otsuka_contract",
                        data:{
                                'o_c_date':o_c_date,   
                                'o_c_kind':o_c_kind,   
                                'o_c_title':o_c_title,   
                                'o_c_cost':o_c_cost,   
                                'o_c_time':o_c_time,   
                                'o_c_company':o_c_company,
                                'o_c_name':o_c_name,      
                                'o_c_telephone':o_c_telephone,      
                                'o_c_phone':o_c_phone,      
                                'o_c_comment':o_c_comment   
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
                                alert(xhr.status);
                                alert(xhr.responseText);
                                alert(throwError);
                                alert(ajaxError);
                        },
                        success:function(res){
                                
                                // refresh show 
                                //$('#otsuka_contract').show(1000).html(res);
                                
                                $('#submit_otsuka_contract').toast('show');

                                // clean up fields
                                $("#o_c_date").val("");
                                $("#o_c_kind").val("");
                                $("#o_c_title").val("");
                                $("#o_c_cost").val("");
                                $("#o_c_time").val("");
                                $("#o_c_company").val("");
                                $("#o_c_name").val("");
                                $("#o_c_telephone").val("");
                                $("#o_c_phone").val("");
                                $("#o_c_comment").val("");

                                //$("#computer_user_detail").show(1000).html(res);
                                //$("#show_day_month_detail").show(1000).html(res);
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("顯示合約資訊資料 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });
        }
      
}

function show_sensor_position_list(){

        $.ajax({
                type:"POST",
                url:"/show_sensor_position_list",
                data:{
                        
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        //$("#computer_user_detail").show(1000).html(res);
                        $("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示電腦序號詳細資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function show_factory_monitor_detail(val){
        var d_position  = val;

        $.ajax({
                type:"POST",
                url:"/show_factory_monitor_detail",
                data:{
                        's_kind':d_position
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        //$("#computer_user_detail").show(1000).html(res);
                        $("#show_day_month_detail").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示電腦使用者詳細資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function show_computer_serial_name_list(){

        $.ajax({
                type:"POST",
                url:"/show_computer_serial_name_list",
                data:{
                        
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        //$("#computer_user_detail").show(1000).html(res);
                        $("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示電腦序號詳細資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function search_show_computer_user_detail(val){
        var s_number  = val;

        $.ajax({
                type:"POST",
                url:"/search_show_computer_user_detail",
                data:{
                        's_number':s_number
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        //$("#computer_user_detail").show(1000).html(res);
                        $("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示電腦使用者詳細資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function show_computer_user_detail(val){
        var d_name  = val;

        $.ajax({
                type:"POST",
                url:"/show_computer_user_detail",
                data:{
                        'd_name':d_name
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        //$("#computer_user_detail").show(1000).html(res);
                        $("#show_day_month_detail").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示電腦使用者詳細資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function download_excel(val){
        var data  = val.split('/');
        var year  = data[0];
        var month = data[1];

        $.ajax({
                type:"POST",
                url:"/download_day_money_excel",
                data:{
                        'year':year,
                        'month':month
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        //$("#show_day_month_detail").show(1000).html(res);
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("下載日當月報表資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function show_day_month_over_traffic_detail(val){
        var data  = val.split('/');
        var year  = data[0];
        var month = data[1];

        $.ajax({
                type:"POST",
                url:"/show_day_month_over_traffic_detail",
                data:{
                        'year':year,
                        'month':month
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#show_day_month_detail").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示日當超里程月報表資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function show_day_month_traffic_detail(val){
        var data  = val.split('/');
        var year  = data[0];
        var month = data[1];

        $.ajax({
                type:"POST",
                url:"/show_day_month_traffic_detail",
                data:{
                        'year':year,
                        'month':month
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#show_day_month_detail").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示日當交通費月報表資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function show_day_month_parking_fee_detail(val){
        var data  = val.split('/');
        var year  = data[0];
        var month = data[1];

        $.ajax({
                type:"POST",
                url:"/show_day_month_parking_fee_detail",
                data:{
                        'year':year,
                        'month':month
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#show_day_month_detail").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示日當停車費月報表資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function show_day_month_tolls_detail(val){
        var data  = val.split('/');
        var year  = data[0];
        var month = data[1];

        $.ajax({
                type:"POST",
                url:"/show_day_month_tolls_detail",
                data:{
                        'year':year,
                        'month':month
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#show_day_month_detail").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示日當過路費月報表資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function show_day_month_trick_detail(val){
        var data  = val.split('/');
        var year  = data[0];
        var month = data[1];

        $.ajax({
                type:"POST",
                url:"/show_day_month_trick_detail",
                data:{
                        'year':year,
                        'month':month
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#show_day_month_detail").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示日當車票月報表資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function show_day_month_taxi_detail(val){
        var data  = val.split('/');
        var year  = data[0];
        var month = data[1];

        $.ajax({
                type:"POST",
                url:"/show_day_month_taxi_detail",
                data:{
                        'year':year,
                        'month':month
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#show_day_month_detail").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示日當計程車月報表資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function show_day_month_stay_detail(val){
        var data  = val.split('/');
        var year  = data[0];
        var month = data[1];

        $.ajax({
                type:"POST",
                url:"/show_day_month_stay_detail",
                data:{
                        'year':year,
                        'month':month
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#show_day_month_detail").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示日當住宿月報表資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function show_day_month_other_detail(val){
        var data  = val.split('/');
        var year  = data[0];
        var month = data[1];

        $.ajax({
                type:"POST",
                url:"/show_day_month_other_detail",
                data:{
                        'year':year,
                        'month':month
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#show_day_month_detail").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示日當其他月報表資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function show_day_month_oil_detail(val){
        var data  = val.split('/');
        var year  = data[0];
        var month = data[1];

        $.ajax({
                type:"POST",
                url:"/show_day_month_oil_detail",
                data:{
                        'year':year,
                        'month':month
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#show_day_month_detail").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示日當油單月報表資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function show_day_month_detail(val){
        var data  = val.split('/');
        var year  = data[0];
        var month = data[1];

        $.ajax({
                type:"POST",
                url:"/show_day_month_detail",
                data:{
                        'year':year,
                        'month':month
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#show_day_month_detail").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("顯示日當月報表資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function load_card_reader_list_detail(value){
        var e_name = value;
        
        $.ajax({
                type:"POST",
                url:"/load_card_reader_list_detail",
                data:{
                        'e_name':e_name
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#card_reader_dep_list_detail").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("loading 部門人員刷卡紀錄資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });

}

function search_card_reader_list(value){
        var name = value;

        alert(name);
        exit();



        $.ajax({
                type:"POST",
                url:"/search_card_reader_list",
                data:{
                        'dep':dep
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#card_reader_dep_list").show(1000).html(res);

                        //$("#card_reader_dep_list_detail").show(1000).html(" ");
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("loading search 人員刷卡紀錄資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function load_card_reader_list(value){
        
        var dep = value;

        $.ajax({
                type:"POST",
                url:"/load_card_reader_list",
                data:{
                        'dep':dep
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);

                        /*
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                        */
                },
                success:function(res){
                        
                        $("#card_reader_dep_list").show(1000).html(res);
                        $("#card_reader_dep_list_detail").show(1000).html(" ");

                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("loading 工廠各門刷卡紀錄資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function load_work_time_data(value){
        var data = value.split('_');
        var b_date = data[0];
        var e_id   = data[1];
        var e_name = data[2];

        $.ajax({
                type:"POST",
                url:"/load_work_time_data",
                data:{
                        'b_date':b_date,
                        'e_id':e_id,
                        'e_name':e_name
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#load_work_time_data").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("loading 液劑工時紀錄資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function submit_check_member_2(){
       var employee_id   = $('#employee_id').val();
       var employee_name = $('#employee_name').val();
       var check_year    = $('#check_year').val();
       var check_month   = $('#check_month').val();

       var sir_num1_1 = $('#sir_num1_1').val();
       var sir_num1_2 = $('#sir_num1_2').val();
       var sir_num1_3 = $('#sir_num1_3').val();
       var sir_num1_4 = $('#sir_num1_4').val();

       var sir_num2_1 = $('#sir_num2_1').val();
       var sir_num2_2 = $('#sir_num2_2').val();
       var sir_num2_3 = $('#sir_num2_3').val();
       
       var sir_num3_1 = $('#sir_num3_1').val();
       var sir_num3_2 = $('#sir_num3_2').val();
       var sir_num3_3 = $('#sir_num3_3').val();

       var sir_num4_1 = $('#sir_num4_1').val();
       var sir_num4_2 = $('#sir_num4_2').val();
       var sir_num4_3 = $('#sir_num4_3').val();
       var sir_num4_4 = $('#sir_num4_4').val();

       var sir_num5_1 = $('#sir_num5_1').val();
       var sir_num5_2 = $('#sir_num5_2').val();
       var sir_num5_3 = $('#sir_num5_3').val();

       var sir_num6_1 = $('#sir_num6_1').val();
       var sir_num6_2 = $('#sir_num6_2').val();
       var sir_num6_3 = $('#sir_num6_3').val();

       var sir_num7_1 = $('#sir_num7_1').val();
       var sir_num7_2 = $('#sir_num7_2').val();
       var sir_num7_3 = $('#sir_num7_3').val();
       var sir_num7_4 = $('#sir_num7_4').val();

       var sir_num8_1 = $('#sir_num8_1').val();
       var sir_num8_2 = $('#sir_num8_2').val();
       var sir_num8_3 = $('#sir_num8_3').val();
       var sir_num8_4 = $('#sir_num8_4').val();
       var sir_num8_5 = $('#sir_num8_5').val();

       var comment          = $('#comment').val();
       var other_total      = $('#other_total').val();
       var sir_total        = $('#sir_total').val();
       var other_plus_total = $('#other_plus_total').val();
       var final_total      = $('#final_total').val();
       var final_comment    = $('#final_comment').val();
       
       // check sir_num1_1
       if(sir_num1_1.length == 0){
                alert('一.責任及態度 - 是否主動積極 , 主評不能空白 !');
                exit();
        }
        // check sir_num1_2
        else if(sir_num1_2.length == 0){
                alert('一.責任及態度 - 主管交代是否配合 , 主評不能空白 !');
                exit();
        }
        // check sir_num1_3
        else if(sir_num1_3.length == 0){
                alert('一.責任及態度 - 專注力 , 主評不能空白 !');
                exit();
        }
        // check sir_num1_4
        else if(sir_num1_4.length == 0){
                alert('一.責任及態度 - 不浮誇 , 不欺騙 , 主評不能空白 !');
                exit();
        }
        // check sir_num2_1
        else if(sir_num2_1.length == 0){
                alert('二.工作能力 - 對主身工作是否嚴謹 , 主評不能空白 !');
                exit();
        }
        // check sir_num2_2
        else if(sir_num2_2.length == 0){
                alert('二.工作能力 - 對專業技能是否專精 , 主評不能空白 !');
                exit();
        }
        // check sir_num2_3
        else if(sir_num2_3.length == 0){
                alert('二.工作能力 - 對產品與技術是否全盤了解 , 主評不能空白 !');
                exit();
        }
        // check sir_num3_1
        else if(sir_num3_1.length == 0){
                alert('三.學習狀況 - 是否願接受新事務及挑戰 , 主評不能空白 !');
                exit();
        }
        // check sir_num3_2
        else if(sir_num3_2.length == 0){
                alert('三.學習狀況 - 進入新事務的快慢 , 主評不能空白 !');
                exit();
        }
        // check sir_num3_3
        else if(sir_num3_3.length == 0){
                alert('三.學習狀況 - 對學習專業是否認真 , 主評不能空白 !');
                exit();
        }
        // check sir_num4_1
        else if(sir_num4_1.length == 0){
                alert('四.自主行為 - 服裝儀容及衛生管理 , 主評不能空白 !');
                exit();
        }
        // check sir_num4_2
        else if(sir_num4_2.length == 0){
                alert('四.自主行為 - 對品質觀念是否落實 , 主評不能空白 !');
                exit();
        }
        // check sir_num4_3
        else if(sir_num4_3.length == 0){
                alert('四.自主行為 - 對清潔設備是否落實 , 主評不能空白 !');
                exit();
        }
        // check sir_num4_4
        else if(sir_num4_4.length == 0){
                alert('四.自主行為 - 對器材機具是否愛護 , 主評不能空白 !');
                exit();
        }
        // check sir_num5_1
        else if(sir_num5_1.length == 0){
                alert('五.工作狀態 - 成本意識(不浪費) , 主評不能空白 !');
                exit();
        }
        // check sir_num5_2
        else if(sir_num5_2.length == 0){
                alert('五.工作狀態 - 動作是否俐落 , 主評不能空白 !');
                exit();
        }
        // check sir_num5_3
        else if(sir_num5_3.length == 0){
                alert('五.工作狀態 - 對SOP是否遵從 , 主評不能空白 !');
                exit();
        }
        // check sir_num6_1
        else if(sir_num6_1.length == 0){
                alert('六.團隊默契 - 對同儕及上級相處 , 主評不能空白 !');
                exit();
        }
        // check sir_num6_2
        else if(sir_num6_2.length == 0){
                alert('六.團隊默契 - 主動協助 , 主評不能空白 !');
                exit();
        }
        // check sir_num6_3
        else if(sir_num6_3.length == 0){
                alert('六.團隊默契 - 溝通協調 , 主評不能空白 !');
                exit();
        }
        // check sir_num7_1
        else if(sir_num7_1.length == 0){
                alert('六.團隊默契 - 對同儕及上級相處 , 主評不能空白 !');
                exit();
        }
        // check sir_num7_2
        else if(sir_num7_2.length == 0){
                alert('六.團隊默契 - 主動協助 , 主評不能空白 !');
                exit();
        }
        // check sir_num7_3
        else if(sir_num7_3.length == 0){
                alert('六.團隊默契 - 溝通協調 , 主評不能空白 !');
                exit();
        }
        // check sir_num7_4
        else if(sir_num7_4.length == 0){
                alert('六.團隊默契 - 溝通協調 , 主評不能空白 !');
                exit();
        }
        // check sir_num8_1
        else if(sir_num8_1.length == 0){
                alert('六.團隊默契 - 對同儕及上級相處 , 主評不能空白 !');
                exit();
        }
        // check sir_num8_2
        else if(sir_num8_2.length == 0){
                alert('六.團隊默契 - 主動協助 , 主評不能空白 !');
                exit();
        }
        // check sir_num8_3
        else if(sir_num8_3.length == 0){
                alert('六.團隊默契 - 溝通協調 , 主評不能空白 !');
                exit();
        }
        // check sir_num8_4
        else if(sir_num8_4.length == 0){
                alert('六.團隊默契 - 溝通協調 , 主評不能空白 !');
                exit();
        }
        // check sir_num8_5
        else if(sir_num8_5.length == 0){
                alert('六.團隊默契 - 溝通協調 , 主評不能空白 !');
                exit();
        }
        // check comment
        else if(comment.length == 0){
                alert('六.團隊默契 - 溝通協調 , 主評不能空白 !');
                exit();
        }
        // check final_comment
        else if(final_comment.length == 0){
                alert('六.團隊默契 - 溝通協調 , 主評不能空白 !');
                exit();
        }
        
        else{

                 $.ajax({
                        type:"POST",
                        url:"/update_submit_check_member_2",
                        data:{
                                'employee_id':employee_id,
                                'employee_name':employee_name,
                                'check_year':check_year,
                                'check_month':check_month,
                                'sir_num1_1':sir_num1_1,
                                'sir_num1_2':sir_num1_2,
                                'sir_num1_3':sir_num1_3,
                                'sir_num1_4':sir_num1_4,
                                'sir_num2_1':sir_num2_1,
                                'sir_num2_2':sir_num2_2,
                                'sir_num2_3':sir_num2_3,
                                
                                'sir_num3_1':sir_num3_1,
                                'sir_num3_2':sir_num3_2,
                                'sir_num3_3':sir_num3_3,

                                'sir_num4_1':sir_num4_1,
                                'sir_num4_2':sir_num4_2,
                                'sir_num4_3':sir_num4_3,
                                'sir_num4_4':sir_num4_4,

                                'sir_num5_1':sir_num5_1,
                                'sir_num5_2':sir_num5_2,
                                'sir_num5_3':sir_num5_3,

                                'sir_num6_1':sir_num6_1,
                                'sir_num6_2':sir_num6_2,
                                'sir_num6_3':sir_num6_3,

                                'sir_num7_1':sir_num7_1,
                                'sir_num7_2':sir_num7_2,
                                'sir_num7_3':sir_num7_3,
                                'sir_num7_4':sir_num7_4,

                                'sir_num8_1':sir_num8_1,
                                'sir_num8_2':sir_num8_2,
                                'sir_num8_3':sir_num8_3,
                                'sir_num8_4':sir_num8_4,
                                'sir_num8_5':sir_num8_5,
                                
                                'comment':comment,
                                'sir_total':sir_total,
                                'other_total':other_total,
                                'other_plus_total':other_plus_total,
                                'final_total':final_total,
                                'final_comment':final_comment
                                
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
                                alert(xhr.status);
                                alert(xhr.responseText);
                                alert(throwError);
                                alert(ajaxError);
                        },
                        success:function(res){
                                
                                $("#load_check_form2").show(1000).html(res);
                                
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("save 主官評分 考評表資料 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });
        }
}

function load_check_member_list(){
        var employee_id         = $('#employee_id').val();
        var employee_name       = $('#employee_name').val();
        var check_year          = $('#check_year').val();
        var check_month         = $('#check_month').val();

        $.ajax({
                type:"POST",
                url:"/load_check_member_self_list",
                data:{
                        'employee_id':employee_id,
                        'employee_name':employee_name,
                        'check_year':check_year,
                        'check_month':check_month
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#load_check_member_list").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("search 員工姓名資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function department_list_detail(val){

        var d_code = val;

        $.ajax({
                type:"POST",
                url:"/department_list_detail",
                data:{
                        'd_code':d_code
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#department_list_detail").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("員工姓名清單資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
        
}

function department_name_search(){
        var search_name = $('#department_name').val();

        $.ajax({
                type:"POST",
                url:"/department_no_search_val",
                data:{
                        'search_name':search_name
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#search_val").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("search 員工姓名資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
        
}

function submit_work_check_member(){
        var employee_id      = $('#employee_id').val();
        var employee_name    = $('#employee_name').val();
        var department_id    = $('#department_id').val();
        var department_name  = $('#department_name').val();
        var job_title        = $('#job_title').val();
        var b_date           = $('#b_date').val();
        var end_date         = $('#end_date').val();
        var check_year       = $('#check_year').val();
        var check_month      = $('#check_month').val();

        // 1
        var self_num1_1 = $('#self_num1_1').val();
        var self_num1_2 = $('#self_num1_2').val();
        var self_num1_3 = $('#self_num1_3').val();
        var self_num1_4 = $('#self_num1_4').val();
        
        var other_num1_1 = $('#other_num1_1').val();
        var other_num1_2 = $('#other_num1_2').val();
        var other_num1_3 = $('#other_num1_3').val();
        var other_num1_4 = $('#other_num1_4').val();
        
        var sir_num1_1 = $('#sir_num1_1').val();
        var sir_num1_2 = $('#sir_num1_2').val();
        var sir_num1_3 = $('#sir_num1_3').val();
        var sir_num1_4 = $('#sir_num1_4').val();

        // 2
        var self_num2_1 = $('#self_num2_1').val();
        var self_num2_2 = $('#self_num2_2').val();
        var self_num2_3 = $('#self_num2_3').val();
        
        var other_num2_1 = $('#other_num2_1').val();
        var other_num2_2 = $('#other_num2_2').val();
        var other_num2_3 = $('#other_num2_3').val();
        
        var sir_num2_1 = $('#sir_num2_1').val();
        var sir_num2_2 = $('#sir_num2_2').val();
        var sir_num2_3 = $('#sir_num2_3').val();

        // 3
        var self_num3_1 = $('#self_num3_1').val();
        var self_num3_2 = $('#self_num3_2').val();
        var self_num3_3 = $('#self_num3_3').val();
        
        var other_num3_1 = $('#other_num3_1').val();
        var other_num3_2 = $('#other_num3_2').val();
        var other_num3_3 = $('#other_num3_3').val();
        
        var sir_num3_1 = $('#sir_num3_1').val();
        var sir_num3_2 = $('#sir_num3_2').val();
        var sir_num3_3 = $('#sir_num3_3').val();

        // 4
        var self_num4_1 = $('#self_num4_1').val();
        var self_num4_2 = $('#self_num4_2').val();
        var self_num4_3 = $('#self_num4_3').val();
        var self_num4_4 = $('#self_num4_4').val();
        
        var other_num4_1 = $('#other_num4_1').val();
        var other_num4_2 = $('#other_num4_2').val();
        var other_num4_3 = $('#other_num4_3').val();
        var other_num4_4 = $('#other_num4_3').val();
        
        var sir_num4_1 = $('#sir_num4_1').val();
        var sir_num4_2 = $('#sir_num4_2').val();
        var sir_num4_3 = $('#sir_num4_3').val();
        var sir_num4_4 = $('#sir_num4_3').val();

        // 5
        var self_num5_1 = $('#self_num5_1').val();
        var self_num5_2 = $('#self_num5_2').val();
        var self_num5_3 = $('#self_num5_3').val();
        
        var other_num5_1 = $('#other_num5_1').val();
        var other_num5_2 = $('#other_num5_2').val();
        var other_num5_3 = $('#other_num5_3').val();
        
        var sir_num5_1 = $('#sir_num5_1').val();
        var sir_num5_2 = $('#sir_num5_2').val();
        var sir_num5_3 = $('#sir_num5_3').val();

        // 6
        var self_num6_1 = $('#self_num6_1').val();
        var self_num6_2 = $('#self_num6_2').val();
        var self_num6_3 = $('#self_num6_3').val();
        
        var other_num6_1 = $('#other_num6_1').val();
        var other_num6_2 = $('#other_num6_2').val();
        var other_num6_3 = $('#other_num6_3').val();
        
        var sir_num6_1 = $('#sir_num6_1').val();
        var sir_num6_2 = $('#sir_num6_2').val();
        var sir_num6_3 = $('#sir_num6_3').val();

        // 7
        var sir_num7_1 = $('#sir_num7_1').val();
        var sir_num7_2 = $('#sir_num7_2').val();
        var sir_num7_3 = $('#sir_num7_3').val();
        var sir_num7_3 = $('#sir_num7_3').val();
        // 8
        var sir_num8_1 = $('#sir_num8_1').val();
        var sir_num8_2 = $('#sir_num8_2').val();
        var sir_num8_3 = $('#sir_num8_3').val();
        var sir_num8_3 = $('#sir_num8_3').val();

        var comment = $('#comment').val();

        var  self_total         = $('#self_total').val();
        var  other_total        = $('#other_total').val();
        var  sir_total          = $('#sir_total').val();
        var  other_plus_total   = $('#other_plus_total').val();
        var  final_total        = $('#final_total').val();
        var  final_comment      = $('#final_comment').val();

        
        // check self_num1_1
        if(self_num1_1.length == 0){
                //alert('一.責任及態度 - 是否主動積極 , 自評不能空白 !');
                exit();
        }
        // check self_num1_2
        else if(self_num1_2.length == 0){
                //alert('一.責任及態度 - 主管交代是否配合 , 自評不能空白 !');
                exit();
        }
        // check self_num1_3
        else if(self_num1_3.length == 0){
                //alert('一.責任及態度 - 專注力 , 自評不能空白 !');
                exit();
        }
        // check self_num1_4
        else if(self_num1_4.length == 0){
                //alert('一.責任及態度 - 不浮誇 , 不欺騙 , 自評不能空白 !');
                exit();
        }
        // check self_num2_1
        else if(self_num2_1.length == 0){
                //alert('二.工作能力 - 對自身工作是否嚴謹 , 自評不能空白 !');
                exit();
        }
        // check self_num2_2
        else if(self_num2_2.length == 0){
                //alert('二.工作能力 - 對專業技能是否專精 , 自評不能空白 !');
                exit();
        }
        // check self_num2_3
        else if(self_num2_3.length == 0){
                //alert('二.工作能力 - 對產品與技術是否全盤了解 , 自評不能空白 !');
                exit();
        }
        // check self_num3_1
        else if(self_num3_1.length == 0){
                //alert('三.學習狀況 - 是否願接受新事務及挑戰 , 自評不能空白 !');
                exit();
        }
        // check self_num3_2
        else if(self_num3_2.length == 0){
                //alert('三.學習狀況 - 進入新事務的快慢 , 自評不能空白 !');
                exit();
        }
        // check self_num3_3
        else if(self_num3_3.length == 0){
                //alert('三.學習狀況 - 對學習專業是否認真 , 自評不能空白 !');
                exit();
        }
        // check self_num4_1
        else if(self_num4_1.length == 0){
                //alert('四.自主行為 - 服裝儀容及衛生管理 , 自評不能空白 !');
                exit();
        }
        // check self_num4_2
        else if(self_num4_2.length == 0){
                //alert('四.自主行為 - 對品質觀念是否落實 , 自評不能空白 !');
                exit();
        }
        // check self_num4_3
        else if(self_num4_3.length == 0){
                //alert('四.自主行為 - 對清潔設備是否落實 , 自評不能空白 !');
                exit();
        }
        // check self_num4_4
        else if(self_num4_4.length == 0){
                //alert('四.自主行為 - 對器材機具是否愛護 , 自評不能空白 !');
                exit();
        }
        // check self_num5_1
        else if(self_num5_1.length == 0){
                //alert('五.工作狀態 - 成本意識(不浪費) , 自評不能空白 !');
                exit();
        }
        // check self_num5_2
        else if(self_num5_2.length == 0){
                //alert('五.工作狀態 - 動作是否俐落 , 自評不能空白 !');
                exit();
        }
        // check self_num5_3
        else if(self_num5_3.length == 0){
                //alert('五.工作狀態 - 對SOP是否遵從 , 自評不能空白 !');
                exit();
        }
        // check self_num6_1
        else if(self_num6_1.length == 0){
                //alert('六.團隊默契 - 對同儕及上級相處 , 自評不能空白 !');
                exit();
        }
        // check self_num6_2
        else if(self_num6_2.length == 0){
                //alert('六.團隊默契 - 主動協助 , 自評不能空白 !');
                exit();
        }
        // check self_num6_3
        else if(self_num6_3.length == 0){
                //alert('六.團隊默契 - 溝通協調 , 自評不能空白 !');
                exit();
        }
        else if(job_title == '經理') {
                //alert(self_total);
                exit();
        }
        else if(job_title == '課長') {
                //alert(self_total);
                exit();
        }
        else{
                $.ajax({
                        type:"POST",
                        url:"/submit_add_check_member_data",
                        data:{
                                'employee_id':employee_id,
                                'employee_name':employee_name,
                                'department_id':department_id,
                                'department_name':department_name,
                                'job_title':job_title,
                                'b_date':b_date,
                                'end_date':end_date,
                                'check_year':check_year,
                                'check_month':check_month,
                                'self_num1_1':self_num1_1,
                                'self_num1_2':self_num1_2,
                                'self_num1_3':self_num1_3,
                                'self_num1_4':self_num1_4,
                                'self_num2_1':self_num2_1,
                                'self_num2_2':self_num2_2,
                                'self_num2_3':self_num2_3,
                                'self_num3_1':self_num3_1,
                                'self_num3_2':self_num3_2,
                                'self_num3_3':self_num3_3,
                                'self_num4_1':self_num4_1,
                                'self_num4_2':self_num4_2,
                                'self_num4_3':self_num4_3,
                                'self_num4_4':self_num4_4,
                                'self_num5_1':self_num5_1,
                                'self_num5_2':self_num5_2,
                                'self_num5_3':self_num5_3,
                                'self_num6_1':self_num6_1,
                                'self_num6_2':self_num6_2,
                                'self_num6_3':self_num6_3,
                                'self_total':self_total
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
                                alert(xhr.status);
                                alert(xhr.responseText);
                                alert(throwError);
                                alert(ajaxError);
                        },
                        success:function(res){
                                
                                $("#load_check_form2").show(1000).html(res);
                                
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("loading 新增考評人員表單資料 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });
        }
        

}

function submit_add_check_account(){
        
        var employee_id     = $('#employee_id').val()
        var employee_name   = $('#employee_name').val()
        var login_id        = $('#login_id').val()
        var mobile          = $('#mobile').val()
        var department_name = $('#department_name').val()
        var department_code = $('#department_code').val()
        var compyany_id     = $('#company_id').val()
        var end_date        = $('#end_date').val()
        
        
        // check employee_id
        if(employee_id.length == 0){
        //        alert('工號不能空白 !');
                exit();        
        }
        // check employee_name
        else if(employee_name.length == 0){
                //alert('姓名不能空白 !');
                exit();        
        }
        // check login_id
        else if(login_id.length == 0){
                //alert('帳號不能空白 !');
                exit();        
        }
        // check mobile
        else if(mobile.length == 0){
                //alert('密碼不能空白 !');
                exit();        
        }
        // check end_date
        else if(end_date.length == 0){
                //alert('到職不能空白 !');
                exit();        
        }
        else{
                $.ajax({
                        type:"POST",
                        url:"/submit_add_check_account",
                        data:{
                                'employee_id':employee_id,
                                'employee_name':employee_name,
                                'login_id':login_id,
                                'mobile':mobile,
                                'department_name':department_name,
                                'department_code':department_code,
                                'company_id':compyany_id,
                                'end_date':end_date
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
                                alert(xhr.status);
                                alert(xhr.responseText);
                                alert(throwError);
                                alert(ajaxError);
                        },
                        success:function(res){
                                
                                $("#load_check_form").show(1000).html(res);
                                
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("loading 新增考評人員帳號表單資料 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });
        }
        
}

function add_check_member_account(){
        $.ajax({
                type:"POST",
                url:"/add_check_member_account",
                data:{
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#load_check_form").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("loading 新增考評人員帳號表單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function load_account_data(user){
        
        $.ajax({
                type:"POST",
                url:"/load_account_data",
                data:{
                        'user':user
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#load_check_form").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        //goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("loading " + user + " 考評資料 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function auto_plus_other_plus_num(){
        var sir_num1       = $('#sir_num1_1').val();
        var sir_num2       = $('#sir_num1_2').val();
        var sir_num3       = $('#sir_num1_3').val();
        var sir_num4       = $('#sir_num1_4').val();
        var sir_num5       = $('#sir_num2_1').val();
        var sir_num6       = $('#sir_num2_2').val();
        var sir_num7       = $('#sir_num2_3').val();
        var sir_num8       = $('#sir_num3_1').val();
        var sir_num9       = $('#sir_num3_2').val();
        var sir_num10       = $('#sir_num3_2').val();
        var sir_num11       = $('#sir_num4_1').val();
        var sir_num12       = $('#sir_num4_2').val();
        var sir_num13       = $('#sir_num4_3').val();
        var sir_num14       = $('#sir_num4_4').val();
        var sir_num15       = $('#sir_num5_1').val();
        var sir_num16       = $('#sir_num5_2').val();
        var sir_num17       = $('#sir_num5_3').val();
        var sir_num18       = $('#sir_num6_1').val();
        var sir_num19       = $('#sir_num6_2').val();
        var sir_num20       = $('#sir_num6_3').val();
       
        // auto plus normal work time
        var auto_plus_sir_number = (Number(sir_num1) + Number(sir_num2) + Number(sir_num3)  + Number(sir_num4)  + Number(sir_num5)  + Number(sir_num6) + Number(sir_num7) + Number(sir_num8) + Number(sir_num9)  + Number(sir_num10) + Number(sir_num11) + Number(sir_num12) + Number(sir_num13) + Number(sir_num14) + Number(sir_num15) + Number(sir_num16) + Number(sir_num17) + Number(sir_num18) + Number(sir_num19) + Number(sir_num20)).toFixed(0);
        
        var other_plus_num1       = $('#sir_num7_1').val();
        var other_plus_num2       = $('#sir_num7_2').val();
        var other_plus_num3       = $('#sir_num7_3').val();
        var other_plus_num4       = $('#sir_num7_4').val();
        var other_plus_num5       = $('#sir_num8_1').val();
        var other_plus_num6       = $('#sir_num8_2').val();
        var other_plus_num7       = $('#sir_num8_3').val();
        var other_plus_num8       = $('#sir_num8_4').val();
       
        // auto plus normal work time
        var auto_plus_other_plus_number = Number(other_plus_num1) + Number(other_plus_num2) + Number(other_plus_num3) + Number(other_plus_num4) + Number(other_plus_num5) + Number(other_plus_num6) + Number(other_plus_num7) + Number(other_plus_num8);
        
        $('#other_plus_total').val(auto_plus_other_plus_number);
        $('#sir_total').val(auto_plus_sir_number);
        
        // final plus num total
        var final_plus_num_total_val = Number(auto_plus_sir_number) + Number(auto_plus_other_plus_number)
        $('#final_total').val(final_plus_num_total_val);
} 

function auto_plus_sir_num(){
        var sir_num1       = $('#sir_num1_1').val();
        var sir_num2       = $('#sir_num1_2').val();
        var sir_num3       = $('#sir_num1_3').val();
        var sir_num4       = $('#sir_num1_4').val();
        var sir_num5       = $('#sir_num2_1').val();
        var sir_num6       = $('#sir_num2_2').val();
        var sir_num7       = $('#sir_num2_3').val();
        var sir_num8       = $('#sir_num3_1').val();
        var sir_num9       = $('#sir_num3_2').val();
        var sir_num10       = $('#sir_num3_2').val();
        var sir_num11       = $('#sir_num4_1').val();
        var sir_num12       = $('#sir_num4_2').val();
        var sir_num13       = $('#sir_num4_3').val();
        var sir_num14       = $('#sir_num4_4').val();
        var sir_num15       = $('#sir_num5_1').val();
        var sir_num16       = $('#sir_num5_2').val();
        var sir_num17       = $('#sir_num5_3').val();
        var sir_num18       = $('#sir_num6_1').val();
        var sir_num19       = $('#sir_num6_2').val();
        var sir_num20       = $('#sir_num6_3').val();
        
       
        // auto plus normal work time
        var auto_plus_sir_number = (Number(sir_num1) + Number(sir_num2) + Number(sir_num3)  + Number(sir_num4)  + Number(sir_num5)  + Number(sir_num6) + Number(sir_num7) + Number(sir_num8) + Number(sir_num9)  + Number(sir_num10) + Number(sir_num11) + Number(sir_num12) + Number(sir_num13) + Number(sir_num14) + Number(sir_num15) + Number(sir_num16) + Number(sir_num17) + Number(sir_num18) + Number(sir_num19) + Number(sir_num20)).toFixed(0);
        
        var other_plus_num1       = $('#sir_num7_1').val();
        var other_plus_num2       = $('#sir_num7_2').val();
        var other_plus_num3       = $('#sir_num7_3').val();
        var other_plus_num4       = $('#sir_num7_4').val();
        var other_plus_num5       = $('#sir_num8_1').val();
        var other_plus_num6       = $('#sir_num8_2').val();
        var other_plus_num7       = $('#sir_num8_3').val();
        var other_plus_num8       = $('#sir_num8_4').val();
       
        // auto plus normal work time
        var auto_plus_other_plus_number = Number(other_plus_num1) + Number(other_plus_num2) + Number(other_plus_num3) + Number(other_plus_num4) + Number(other_plus_num5) + Number(other_plus_num6) + Number(other_plus_num7) + Number(other_plus_num8);

        $('#other_plus_total').val(auto_plus_other_plus_number);
        $('#sir_total').val(auto_plus_sir_number);
        
        // final plus num total
        var final_plus_num_total_val = Number(auto_plus_sir_number) + Number(auto_plus_other_plus_number)
        $('#final_total').val(final_plus_num_total_val);
} 

function auto_plus_self_num(){
        var self_num1       = $('#self_num1_1').val();
        var self_num2       = $('#self_num1_2').val();
        var self_num3       = $('#self_num1_3').val();
        var self_num4       = $('#self_num1_4').val();
        var self_num5       = $('#self_num2_1').val();
        var self_num6       = $('#self_num2_2').val();
        var self_num7       = $('#self_num2_3').val();
        var self_num8       = $('#self_num3_1').val();
        var self_num9       = $('#self_num3_2').val();
        var self_num10       = $('#self_num3_3').val();
        var self_num11       = $('#self_num4_1').val();
        var self_num12       = $('#self_num4_2').val();
        var self_num13       = $('#self_num4_3').val();
        var self_num14       = $('#self_num4_4').val();
        var self_num15       = $('#self_num5_1').val();
        var self_num16       = $('#self_num5_2').val();
        var self_num17       = $('#self_num5_3').val();
        var self_num18       = $('#self_num6_1').val();
        var self_num19       = $('#self_num6_2').val();
        var self_num20       = $('#self_num6_3').val();
       
        // auto plus normal work time
        var auto_plus_self_number = (Number(self_num1) + Number(self_num2) + Number(self_num3)  + Number(self_num4)  + Number(self_num5)  + Number(self_num6) + Number(self_num7) + Number(self_num8) + Number(self_num9)  + Number(self_num10) + Number(self_num11) + Number(self_num12) + Number(self_num13) + Number(self_num14) + Number(self_num15) + Number(self_num16) + Number(self_num17) + Number(self_num18) + Number(self_num19) + Number(self_num20)).toFixed(0);
        
        $('#self_total').val(auto_plus_self_number);
} 

function submit_work_time_3(){

        // 工號
        var a_work_no = $('#a_work_no').val();                                          
        // 姓名
        var a_name    = $('#a_name').val();                                             
        // 日期
        var a_date    = $('#a_date').val();                                             
        // 稼動工時
        var availability_time = $('#auto_plus_availability_work_time').text();          
        // 加班工時
        var over_time         = $('#auto_plus_over_work_time').text();                  
        // 一般工時
        var normal_tima       = $('#auto_plus_normal_work_time').text();                
        // 總工時
        var total_time        = $('#auto_plus_total_work_time').val();                  
        
        // 第1筆
        var a_work_station_1           = $('#a_work_station_1').val();                  
        var a_production_1             = $('#a_production_1').val();
        var a_product_no_1             = $('#a_product_no_1').val();
        var a_work_normal_time_1       = $('#a_work_normal_time_1').val();
        var a_work_over_time_1         = $('#a_work_over_time_1').val();
        var a_work_availability_time_1 = $('#a_work_availability_time_1').val();
        var a_work_remark_1            = $('#a_work_remark_1').val();

        // 第2筆
        var a_work_station_2           = $('#a_work_station_2').val();                  
        var a_production_2             = $('#a_production_2').val();
        var a_product_no_2             = $('#a_product_no_2').val();
        var a_work_normal_time_2       = $('#a_work_normal_time_2').val();
        var a_work_over_time_2         = $('#a_work_over_time_2').val();
        var a_work_availability_time_2 = $('#a_work_availability_time_2').val();
        var a_work_remark_2            = $('#a_work_remark_2').val();

        // 第3筆
        var a_work_station_3           = $('#a_work_station_3').val();                  
        var a_production_3             = $('#a_production_3').val();
        var a_product_no_3             = $('#a_product_no_3').val();
        var a_work_normal_time_3       = $('#a_work_normal_time_3').val();
        var a_work_over_time_3         = $('#a_work_over_time_3').val();
        var a_work_availability_time_3 = $('#a_work_availability_time_3').val();
        var a_work_remark_3            = $('#a_work_remark_3').val();

        // 第4筆
        var a_work_station_4           = $('#a_work_station_4').val();                  
        var a_production_4             = $('#a_production_4').val();
        var a_product_no_4             = $('#a_product_no_4').val();
        var a_work_normal_time_4       = $('#a_work_normal_time_4').val();
        var a_work_over_time_4         = $('#a_work_over_time_4').val();
        var a_work_availability_time_4 = $('#a_work_availability_time_4').val();
        var a_work_remark_4            = $('#a_work_remark_4').val();

        // 第5筆
        var a_work_station_5           = $('#a_work_station_5').val();                  
        var a_production_5             = $('#a_production_5').val();
        var a_product_no_5             = $('#a_product_no_5').val();
        var a_work_normal_time_5       = $('#a_work_normal_time_5').val();
        var a_work_over_time_5         = $('#a_work_over_time_5').val();
        var a_work_availability_time_5 = $('#a_work_availability_time_5').val();
        var a_work_remark_5            = $('#a_work_remark_5').val();
        
        // 第6筆
        var a_work_station_6           = $('#a_work_station_6').val();                  
        var a_production_6             = $('#a_production_6').val();
        var a_product_no_6             = $('#a_product_no_6').val();
        var a_work_normal_time_6       = $('#a_work_normal_time_6').val();
        var a_work_over_time_6         = $('#a_work_over_time_6').val();
        var a_work_availability_time_6 = $('#a_work_availability_time_6').val();
        var a_work_remark_6            = $('#a_work_remark_6').val();

        // 第7筆
        var a_work_station_7           = $('#a_work_station_7').val();                   
        var a_production_7             = $('#a_production_7').val();
        var a_product_no_7             = $('#a_product_no_7').val();
        var a_work_normal_time_7       = $('#a_work_normal_time_7').val();
        var a_work_over_time_7         = $('#a_work_over_time_7').val();
        var a_work_availability_time_7 = $('#a_work_availability_time_7').val();
        var a_work_remark_7            = $('#a_work_remark_7').val();

        // 第8筆
        var a_work_station_8           = $('#a_work_station_8').val();                   
        var a_production_8             = $('#a_production_8').val();
        var a_product_no_8             = $('#a_product_no_8').val();
        var a_work_normal_time_8       = $('#a_work_normal_time_8').val();
        var a_work_over_time_8         = $('#a_work_over_time_8').val();
        var a_work_availability_time_8 = $('#a_work_availability_time_8').val();
        var a_work_remark_8            = $('#a_work_remark_8').val();
        
        // 第9筆
        var a_work_station_9           = $('#a_work_station_9').val();                   
        var a_production_9             = $('#a_production_9').val();
        var a_product_no_9             = $('#a_product_no_9').val();
        var a_work_normal_time_9       = $('#a_work_normal_time_9').val();
        var a_work_over_time_9         = $('#a_work_over_time_9').val();
        var a_work_availability_time_9 = $('#a_work_availability_time_9').val();
        var a_work_remark_9            = $('#a_work_remark_9').val();

        // 第10筆
        var a_work_station_10           = $('#a_work_station_10').val();                 
        var a_production_10             = $('#a_production_10').val();
        var a_product_no_10             = $('#a_product_no_10').val();
        var a_work_normal_time_10       = $('#a_work_normal_time_10').val();
        var a_work_over_time_10         = $('#a_work_over_time_10').val();
        var a_work_availability_time_10 = $('#a_work_availability_time_10').val();
        var a_work_remark_10            = $('#a_work_remark_10').val();

        // 第11筆
        var a_work_station_11           = $('#a_work_station_11').val();                 
        var a_production_11             = $('#a_production_11').val();
        var a_product_no_11             = $('#a_product_no_11').val();
        var a_work_normal_time_11       = $('#a_work_normal_time_11').val();
        var a_work_over_time_11         = $('#a_work_over_time_11').val();
        var a_work_availability_time_11 = $('#a_work_availability_time_11').val();
        var a_work_remark_11            = $('#a_work_remark_11').val();

        // 第12筆
        var a_work_station_12           = $('#a_work_station_12').val();                 
        var a_production_12             = $('#a_production_12').val();
        var a_product_no_12             = $('#a_product_no_12').val();
        var a_work_normal_time_12       = $('#a_work_normal_time_12').val();
        var a_work_over_time_12         = $('#a_work_over_time_12').val();
        var a_work_availability_time_12 = $('#a_work_availability_time_12').val();
        var a_work_remark_12            = $('#a_work_remark_12').val();

        
        // check 工號
        if(a_work_no.length == 0){
                alert('工號不能空白 !');
                exit();        
        }
        // check 姓名
        else if(a_name == 0){
                alert('姓名不能空白 !');
                exit()
        }
        else{
                alert(  '工號 : ' + a_work_no + ' , 姓名 : ' + a_name + ' , 日期 : ' + a_date + ' , 總工時 : ' + total_time + '\n' +
                        '總一般工時  : ' + normal_tima + ' , 總加班工時 : ' + over_time + ' , 總價動工時 : ' + availability_time + '\n' +
                        a_work_station_1 + ' , ' + a_production_1 + ' , ' + a_product_no_1 + ' , ' + a_work_normal_time_1 + ' , ' + a_work_over_time_1 + ' , ' + a_work_availability_time_1 + ' , ' + a_work_remark_1 + '\n' +
                        a_work_station_2 + ' , ' + a_production_2 + ' , ' + a_product_no_2 + ' , ' + a_work_normal_time_2 + ' , ' + a_work_over_time_2 + ' , ' + a_work_availability_time_2 + ' , ' + a_work_remark_2 + '\n' +
                        a_work_station_3 + ' , ' + a_production_3 + ' , ' + a_product_no_3 + ' , ' + a_work_normal_time_3 + ' , ' + a_work_over_time_3 + ' , ' + a_work_availability_time_3 + ' , ' + a_work_remark_3 + '\n' +
                        a_work_station_4 + ' , ' + a_production_4 + ' , ' + a_product_no_4 + ' , ' + a_work_normal_time_4 + ' , ' + a_work_over_time_4 + ' , ' + a_work_availability_time_4 + ' , ' + a_work_remark_4 + '\n' +
                        a_work_station_5 + ' , ' + a_production_5 + ' , ' + a_product_no_5 + ' , ' + a_work_normal_time_5 + ' , ' + a_work_over_time_5 + ' , ' + a_work_availability_time_5 + ' , ' + a_work_remark_5 + '\n' +
                        a_work_station_6 + ' , ' + a_production_6 + ' , ' + a_product_no_6 + ' , ' + a_work_normal_time_6 + ' , ' + a_work_over_time_6 + ' , ' + a_work_availability_time_6 + ' , ' + a_work_remark_6 + '\n' +
                        a_work_station_7 + ' , ' + a_production_7 + ' , ' + a_product_no_7 + ' , ' + a_work_normal_time_7 + ' , ' + a_work_over_time_7 + ' , ' + a_work_availability_time_7 + ' , ' + a_work_remark_7 + '\n' +
                        a_work_station_8 + ' , ' + a_production_8 + ' , ' + a_product_no_8 + ' , ' + a_work_normal_time_8 + ' , ' + a_work_over_time_8 + ' , ' + a_work_availability_time_8 + ' , ' + a_work_remark_8 + '\n' +
                        a_work_station_9 + ' , ' + a_production_9 + ' , ' + a_product_no_9 + ' , ' + a_work_normal_time_9 + ' , ' + a_work_over_time_9 + ' , ' + a_work_availability_time_9 + ' , ' + a_work_remark_9 + '\n' +
                        a_work_station_10 + ' , ' + a_production_10 + ' , ' + a_product_no_10 + ' , ' + a_work_normal_time_10 + ' , ' + a_work_over_time_10 + ' , ' + a_work_availability_time_10 + ' , ' + a_work_remark_10 + '\n' +
                        a_work_station_11 + ' , ' + a_production_11 + ' , ' + a_product_no_11 + ' , ' + a_work_normal_time_11 + ' , ' + a_work_over_time_11 + ' , ' + a_work_availability_time_11 + ' , ' + a_work_remark_11 + '\n' +
                        a_work_station_12 + ' , ' + a_production_12 + ' , ' + a_product_no_12 + ' , ' + a_work_normal_time_12 + ' , ' + a_work_over_time_12 + ' , ' + a_work_availability_time_12+ ' , ' + a_work_remark_12 + '\n' 
                );
                exit();
        }
        
        $.ajax({
                type:"POST",
                url:"/load_menu_money_record_by_kind",
                data:{
                        'kind':kind
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#menu_money_record_list").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("loading " + kind + " 種類記帳本清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });

}

function submit_work_time_1(){
        
        // 工號
        var a_work_no = $('#a_work_no').val();                                          
        // 姓名
        var a_name    = $('#a_name').val();                                             
        // 日期
        var a_date    = $('#a_date').val();                                             
        // 稼動工時
        var availability_time = $('#auto_plus_availability_work_time').text();          
        // 加班工時
        var over_time         = $('#auto_plus_over_work_time').text();                  
        // 一般工時
        var normal_tima       = $('#auto_plus_normal_work_time').text();                
        // 總工時
        var total_time        = $('#auto_plus_total_work_time').val();                  
        
        // 第1筆
        var a_work_station_1           = $('#a_work_station_1').val();                  
        var a_production_1             = $('#a_production_1').val();
        var a_product_no_1             = $('#a_product_no_1').val();
        var a_work_normal_time_1       = $('#a_work_normal_time_1').val();
        var a_work_over_time_1         = $('#a_work_over_time_1').val();
        var a_work_availability_time_1 = $('#a_work_availability_time_1').val();
        var a_work_remark_1            = $('#a_work_remark_1').val();

        // 第2筆
        var a_work_station_2           = $('#a_work_station_2').val();                  
        var a_production_2             = $('#a_production_2').val();
        var a_product_no_2             = $('#a_product_no_2').val();
        var a_work_normal_time_2       = $('#a_work_normal_time_2').val();
        var a_work_over_time_2         = $('#a_work_over_time_2').val();
        var a_work_availability_time_2 = $('#a_work_availability_time_2').val();
        var a_work_remark_2            = $('#a_work_remark_2').val();

        // 第3筆
        var a_work_station_3           = $('#a_work_station_3').val();                  
        var a_production_3             = $('#a_production_3').val();
        var a_product_no_3             = $('#a_product_no_3').val();
        var a_work_normal_time_3       = $('#a_work_normal_time_3').val();
        var a_work_over_time_3         = $('#a_work_over_time_3').val();
        var a_work_availability_time_3 = $('#a_work_availability_time_3').val();
        var a_work_remark_3            = $('#a_work_remark_3').val();

        // 第4筆
        var a_work_station_4           = $('#a_work_station_4').val();                  
        var a_production_4             = $('#a_production_4').val();
        var a_product_no_4             = $('#a_product_no_4').val();
        var a_work_normal_time_4       = $('#a_work_normal_time_4').val();
        var a_work_over_time_4         = $('#a_work_over_time_4').val();
        var a_work_availability_time_4 = $('#a_work_availability_time_4').val();
        var a_work_remark_4            = $('#a_work_remark_4').val();

        // 第5筆
        var a_work_station_5           = $('#a_work_station_5').val();                  
        var a_production_5             = $('#a_production_5').val();
        var a_product_no_5             = $('#a_product_no_5').val();
        var a_work_normal_time_5       = $('#a_work_normal_time_5').val();
        var a_work_over_time_5         = $('#a_work_over_time_5').val();
        var a_work_availability_time_5 = $('#a_work_availability_time_5').val();
        var a_work_remark_5            = $('#a_work_remark_5').val();
        
        // 第6筆
        var a_work_station_6           = $('#a_work_station_6').val();                  
        var a_production_6             = $('#a_production_6').val();
        var a_product_no_6             = $('#a_product_no_6').val();
        var a_work_normal_time_6       = $('#a_work_normal_time_6').val();
        var a_work_over_time_6         = $('#a_work_over_time_6').val();
        var a_work_availability_time_6 = $('#a_work_availability_time_6').val();
        var a_work_remark_6            = $('#a_work_remark_6').val();

        // 第7筆
        var a_work_station_7           = $('#a_work_station_7').val();                   
        var a_production_7             = $('#a_production_7').val();
        var a_product_no_7             = $('#a_product_no_7').val();
        var a_work_normal_time_7       = $('#a_work_normal_time_7').val();
        var a_work_over_time_7         = $('#a_work_over_time_7').val();
        var a_work_availability_time_7 = $('#a_work_availability_time_7').val();
        var a_work_remark_7            = $('#a_work_remark_7').val();

        // 第8筆
        var a_work_station_8           = $('#a_work_station_8').val();                   
        var a_production_8             = $('#a_production_8').val();
        var a_product_no_8             = $('#a_product_no_8').val();
        var a_work_normal_time_8       = $('#a_work_normal_time_8').val();
        var a_work_over_time_8         = $('#a_work_over_time_8').val();
        var a_work_availability_time_8 = $('#a_work_availability_time_8').val();
        var a_work_remark_8            = $('#a_work_remark_8').val();
        
        // 第9筆
        var a_work_station_9           = $('#a_work_station_9').val();                   
        var a_production_9             = $('#a_production_9').val();
        var a_product_no_9             = $('#a_product_no_9').val();
        var a_work_normal_time_9       = $('#a_work_normal_time_9').val();
        var a_work_over_time_9         = $('#a_work_over_time_9').val();
        var a_work_availability_time_9 = $('#a_work_availability_time_9').val();
        var a_work_remark_9            = $('#a_work_remark_9').val();

        // 第10筆
        var a_work_station_10           = $('#a_work_station_10').val();                 
        var a_production_10             = $('#a_production_10').val();
        var a_product_no_10             = $('#a_product_no_10').val();
        var a_work_normal_time_10       = $('#a_work_normal_time_10').val();
        var a_work_over_time_10         = $('#a_work_over_time_10').val();
        var a_work_availability_time_10 = $('#a_work_availability_time_10').val();
        var a_work_remark_10            = $('#a_work_remark_10').val();

        // 第11筆
        var a_work_station_11           = $('#a_work_station_11').val();                 
        var a_production_11             = $('#a_production_11').val();
        var a_product_no_11             = $('#a_product_no_11').val();
        var a_work_normal_time_11       = $('#a_work_normal_time_11').val();
        var a_work_over_time_11         = $('#a_work_over_time_11').val();
        var a_work_availability_time_11 = $('#a_work_availability_time_11').val();
        var a_work_remark_11            = $('#a_work_remark_11').val();

        // 第12筆
        var a_work_station_12           = $('#a_work_station_12').val();                 
        var a_production_12             = $('#a_production_12').val();
        var a_product_no_12             = $('#a_product_no_12').val();
        var a_work_normal_time_12       = $('#a_work_normal_time_12').val();
        var a_work_over_time_12         = $('#a_work_over_time_12').val();
        var a_work_availability_time_12 = $('#a_work_availability_time_12').val();
        var a_work_remark_12            = $('#a_work_remark_12').val();

        
        // check 工號
        if(a_work_no.length == 0){
                alert('工號不能空白 !');
                exit();        
        }
        // check 姓名
        else if(a_name == 0){
                alert('姓名不能空白 !');
                exit()
        }
        else{
                alert(  '工號 : ' + a_work_no + ' , 姓名 : ' + a_name + ' , 日期 : ' + a_date + ' , 總工時 : ' + total_time + '\n' +
                        '總一般工時  : ' + normal_tima + ' , 總加班工時 : ' + over_time + ' , 總價動工時 : ' + availability_time + '\n' +
                        a_work_station_1 + ' , ' + a_production_1 + ' , ' + a_product_no_1 + ' , ' + a_work_normal_time_1 + ' , ' + a_work_over_time_1 + ' , ' + a_work_availability_time_1 + ' , ' + a_work_remark_1 + '\n' +
                        a_work_station_2 + ' , ' + a_production_2 + ' , ' + a_product_no_2 + ' , ' + a_work_normal_time_2 + ' , ' + a_work_over_time_2 + ' , ' + a_work_availability_time_2 + ' , ' + a_work_remark_2 + '\n' +
                        a_work_station_3 + ' , ' + a_production_3 + ' , ' + a_product_no_3 + ' , ' + a_work_normal_time_3 + ' , ' + a_work_over_time_3 + ' , ' + a_work_availability_time_3 + ' , ' + a_work_remark_3 + '\n' +
                        a_work_station_4 + ' , ' + a_production_4 + ' , ' + a_product_no_4 + ' , ' + a_work_normal_time_4 + ' , ' + a_work_over_time_4 + ' , ' + a_work_availability_time_4 + ' , ' + a_work_remark_4 + '\n' +
                        a_work_station_5 + ' , ' + a_production_5 + ' , ' + a_product_no_5 + ' , ' + a_work_normal_time_5 + ' , ' + a_work_over_time_5 + ' , ' + a_work_availability_time_5 + ' , ' + a_work_remark_5 + '\n' +
                        a_work_station_6 + ' , ' + a_production_6 + ' , ' + a_product_no_6 + ' , ' + a_work_normal_time_6 + ' , ' + a_work_over_time_6 + ' , ' + a_work_availability_time_6 + ' , ' + a_work_remark_6 + '\n' +
                        a_work_station_7 + ' , ' + a_production_7 + ' , ' + a_product_no_7 + ' , ' + a_work_normal_time_7 + ' , ' + a_work_over_time_7 + ' , ' + a_work_availability_time_7 + ' , ' + a_work_remark_7 + '\n' +
                        a_work_station_8 + ' , ' + a_production_8 + ' , ' + a_product_no_8 + ' , ' + a_work_normal_time_8 + ' , ' + a_work_over_time_8 + ' , ' + a_work_availability_time_8 + ' , ' + a_work_remark_8 + '\n' +
                        a_work_station_9 + ' , ' + a_production_9 + ' , ' + a_product_no_9 + ' , ' + a_work_normal_time_9 + ' , ' + a_work_over_time_9 + ' , ' + a_work_availability_time_9 + ' , ' + a_work_remark_9 + '\n' +
                        a_work_station_10 + ' , ' + a_production_10 + ' , ' + a_product_no_10 + ' , ' + a_work_normal_time_10 + ' , ' + a_work_over_time_10 + ' , ' + a_work_availability_time_10 + ' , ' + a_work_remark_10 + '\n' +
                        a_work_station_11 + ' , ' + a_production_11 + ' , ' + a_product_no_11 + ' , ' + a_work_normal_time_11 + ' , ' + a_work_over_time_11 + ' , ' + a_work_availability_time_11 + ' , ' + a_work_remark_11 + '\n' +
                        a_work_station_12 + ' , ' + a_production_12 + ' , ' + a_product_no_12 + ' , ' + a_work_normal_time_12 + ' , ' + a_work_over_time_12 + ' , ' + a_work_availability_time_12+ ' , ' + a_work_remark_12 + '\n' 
                );
                exit();
        }
        
        $.ajax({
                type:"POST",
                url:"/load_menu_money_record_by_kind",
                data:{
                        'kind':kind
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        $("#menu_money_record_list").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("loading " + kind + " 種類記帳本清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });

}
   
function submit_work_time(){

        // 工號
        var a_work_no = $('#a_work_no').val();                                          
        // 姓名
        var a_name    = $('#a_name').val();                                             
        // 日期
        var a_date    = $('#a_date').val();                                             
        // 部門代號
        var dep_id    = $('#department_id').val();                                             
        // 稼動工時
        var availability_time = $('#auto_plus_availability_work_time').text();          
        // 加班工時
        var over_time         = $('#auto_plus_over_work_time').text();              
        // 一般工時
        var normal_time       = $('#auto_plus_normal_work_time').text();                
        // 總工時
        var total_time        = $('#auto_plus_total_work_time').val();                  
        
        // 第1筆
        var a_work_station_1           = $('#a_work_station_1').val();                  
        var a_production_1             = $('#a_production_1').val();
        var a_product_no_1             = $('#a_product_no_1').val();
        var a_work_normal_time_1       = $('#a_work_normal_time_1').val();
        var a_work_over_time_1         = $('#a_work_over_time_1').val();
        var a_work_availability_time_1 = $('#a_work_availability_time_1').val();
        var a_work_remark_1            = $('#a_work_remark_1').val();

        // 第2筆
        var a_work_station_2           = $('#a_work_station_2').val();                  
        var a_production_2             = $('#a_production_2').val();
        var a_product_no_2             = $('#a_product_no_2').val();
        var a_work_normal_time_2       = $('#a_work_normal_time_2').val();
        var a_work_over_time_2         = $('#a_work_over_time_2').val();
        var a_work_availability_time_2 = $('#a_work_availability_time_2').val();
        var a_work_remark_2            = $('#a_work_remark_2').val();

        // 第3筆
        var a_work_station_3           = $('#a_work_station_3').val();                  
        var a_production_3             = $('#a_production_3').val();
        var a_product_no_3             = $('#a_product_no_3').val();
        var a_work_normal_time_3       = $('#a_work_normal_time_3').val();
        var a_work_over_time_3         = $('#a_work_over_time_3').val();
        var a_work_availability_time_3 = $('#a_work_availability_time_3').val();
        var a_work_remark_3            = $('#a_work_remark_3').val();

        // 第4筆
        var a_work_station_4           = $('#a_work_station_4').val();                  
        var a_production_4             = $('#a_production_4').val();
        var a_product_no_4             = $('#a_product_no_4').val();
        var a_work_normal_time_4       = $('#a_work_normal_time_4').val();
        var a_work_over_time_4         = $('#a_work_over_time_4').val();
        var a_work_availability_time_4 = $('#a_work_availability_time_4').val();
        var a_work_remark_4            = $('#a_work_remark_4').val();

        // 第5筆
        var a_work_station_5           = $('#a_work_station_5').val();                  
        var a_production_5             = $('#a_production_5').val();
        var a_product_no_5             = $('#a_product_no_5').val();
        var a_work_normal_time_5       = $('#a_work_normal_time_5').val();
        var a_work_over_time_5         = $('#a_work_over_time_5').val();
        var a_work_availability_time_5 = $('#a_work_availability_time_5').val();
        var a_work_remark_5            = $('#a_work_remark_5').val();
        
        // 第6筆
        var a_work_station_6           = $('#a_work_station_6').val();                  
        var a_production_6             = $('#a_production_6').val();
        var a_product_no_6             = $('#a_product_no_6').val();
        var a_work_normal_time_6       = $('#a_work_normal_time_6').val();
        var a_work_over_time_6         = $('#a_work_over_time_6').val();
        var a_work_availability_time_6 = $('#a_work_availability_time_6').val();
        var a_work_remark_6            = $('#a_work_remark_6').val();

        // 第7筆
        var a_work_station_7           = $('#a_work_station_7').val();                   
        var a_production_7             = $('#a_production_7').val();
        var a_product_no_7             = $('#a_product_no_7').val();
        var a_work_normal_time_7       = $('#a_work_normal_time_7').val();
        var a_work_over_time_7         = $('#a_work_over_time_7').val();
        var a_work_availability_time_7 = $('#a_work_availability_time_7').val();
        var a_work_remark_7            = $('#a_work_remark_7').val();

        // 第8筆
        var a_work_station_8           = $('#a_work_station_8').val();                   
        var a_production_8             = $('#a_production_8').val();
        var a_product_no_8             = $('#a_product_no_8').val();
        var a_work_normal_time_8       = $('#a_work_normal_time_8').val();
        var a_work_over_time_8         = $('#a_work_over_time_8').val();
        var a_work_availability_time_8 = $('#a_work_availability_time_8').val();
        var a_work_remark_8            = $('#a_work_remark_8').val();
        
        // 第9筆
        var a_work_station_9           = $('#a_work_station_9').val();                   
        var a_production_9             = $('#a_production_9').val();
        var a_product_no_9             = $('#a_product_no_9').val();
        var a_work_normal_time_9       = $('#a_work_normal_time_9').val();
        var a_work_over_time_9         = $('#a_work_over_time_9').val();
        var a_work_availability_time_9 = $('#a_work_availability_time_9').val();
        var a_work_remark_9            = $('#a_work_remark_9').val();

        // 第10筆
        var a_work_station_10           = $('#a_work_station_10').val();                 
        var a_production_10             = $('#a_production_10').val();
        var a_product_no_10             = $('#a_product_no_10').val();
        var a_work_normal_time_10       = $('#a_work_normal_time_10').val();
        var a_work_over_time_10         = $('#a_work_over_time_10').val();
        var a_work_availability_time_10 = $('#a_work_availability_time_10').val();
        var a_work_remark_10            = $('#a_work_remark_10').val();

        // 第11筆
        var a_work_station_11           = $('#a_work_station_11').val();                 
        var a_production_11             = $('#a_production_11').val();
        var a_product_no_11             = $('#a_product_no_11').val();
        var a_work_normal_time_11       = $('#a_work_normal_time_11').val();
        var a_work_over_time_11         = $('#a_work_over_time_11').val();
        var a_work_availability_time_11 = $('#a_work_availability_time_11').val();
        var a_work_remark_11            = $('#a_work_remark_11').val();

        // 第12筆
        var a_work_station_12           = $('#a_work_station_12').val();                 
        var a_production_12             = $('#a_production_12').val();
        var a_product_no_12             = $('#a_product_no_12').val();
        var a_work_normal_time_12       = $('#a_work_normal_time_12').val();
        var a_work_over_time_12         = $('#a_work_over_time_12').val();
        var a_work_availability_time_12 = $('#a_work_availability_time_12').val();
        var a_work_remark_12            = $('#a_work_remark_12').val();

        
        // check 工號
        if(a_work_station_1.length == 0){
                alert('工號不能空白 !');
                exit();        
        }
        else{
                /*
                alert(  '工號 : ' + a_work_no + ' , 姓名 : ' + a_name + ' , 部門代號 : ' + dep_id + ' , 日期 : ' + a_date + ' , 總工時 : ' + total_time + '\n' +
                        '總一般工時  : ' + normal_time + ' , 總加班工時 : ' + over_time + ' , 總價動工時 : ' + availability_time + '\n' +
                        a_work_station_1 + ' , ' + a_production_1 + ' , ' + a_product_no_1 + ' , ' + a_work_normal_time_1 + ' , ' + a_work_over_time_1 + ' , ' + a_work_availability_time_1 + ' , ' + a_work_remark_1 + '\n' +
                        a_work_station_2 + ' , ' + a_production_2 + ' , ' + a_product_no_2 + ' , ' + a_work_normal_time_2 + ' , ' + a_work_over_time_2 + ' , ' + a_work_availability_time_2 + ' , ' + a_work_remark_2 + '\n' +
                        a_work_station_3 + ' , ' + a_production_3 + ' , ' + a_product_no_3 + ' , ' + a_work_normal_time_3 + ' , ' + a_work_over_time_3 + ' , ' + a_work_availability_time_3 + ' , ' + a_work_remark_3 + '\n' +
                        a_work_station_4 + ' , ' + a_production_4 + ' , ' + a_product_no_4 + ' , ' + a_work_normal_time_4 + ' , ' + a_work_over_time_4 + ' , ' + a_work_availability_time_4 + ' , ' + a_work_remark_4 + '\n' +
                        a_work_station_5 + ' , ' + a_production_5 + ' , ' + a_product_no_5 + ' , ' + a_work_normal_time_5 + ' , ' + a_work_over_time_5 + ' , ' + a_work_availability_time_5 + ' , ' + a_work_remark_5 + '\n' +
                        a_work_station_6 + ' , ' + a_production_6 + ' , ' + a_product_no_6 + ' , ' + a_work_normal_time_6 + ' , ' + a_work_over_time_6 + ' , ' + a_work_availability_time_6 + ' , ' + a_work_remark_6 + '\n' +
                        a_work_station_7 + ' , ' + a_production_7 + ' , ' + a_product_no_7 + ' , ' + a_work_normal_time_7 + ' , ' + a_work_over_time_7 + ' , ' + a_work_availability_time_7 + ' , ' + a_work_remark_7 + '\n' +
                        a_work_station_8 + ' , ' + a_production_8 + ' , ' + a_product_no_8 + ' , ' + a_work_normal_time_8 + ' , ' + a_work_over_time_8 + ' , ' + a_work_availability_time_8 + ' , ' + a_work_remark_8 + '\n' +
                        a_work_station_9 + ' , ' + a_production_9 + ' , ' + a_product_no_9 + ' , ' + a_work_normal_time_9 + ' , ' + a_work_over_time_9 + ' , ' + a_work_availability_time_9 + ' , ' + a_work_remark_9 + '\n' +
                        a_work_station_10 + ' , ' + a_production_10 + ' , ' + a_product_no_10 + ' , ' + a_work_normal_time_10 + ' , ' + a_work_over_time_10 + ' , ' + a_work_availability_time_10 + ' , ' + a_work_remark_10 + '\n' +
                        a_work_station_11 + ' , ' + a_production_11 + ' , ' + a_product_no_11 + ' , ' + a_work_normal_time_11 + ' , ' + a_work_over_time_11 + ' , ' + a_work_availability_time_11 + ' , ' + a_work_remark_11 + '\n' +
                        a_work_station_12 + ' , ' + a_production_12 + ' , ' + a_product_no_12 + ' , ' + a_work_normal_time_12 + ' , ' + a_work_over_time_12 + ' , ' + a_work_availability_time_12+ ' , ' + a_work_remark_12 + '\n' 
                );
                exit();
                */
                
                $.ajax({
                        type:"POST",
                        url:"/submit_work_time",
                        data:{
                                'a_work_no':a_work_no,
                                'a_name':a_name,
                                'dep_id':dep_id,
                                'b_date':a_date,
                                'total_time':total_time,
                                'normal_time':normal_time,
                                'over_time':over_time,
                                'availability_time':availability_time,
                                
                                'a_work_station_1':a_work_station_1, 
                                'a_production_1':a_production_1,
                                'a_product_no_1':a_product_no_1,
                                'a_work_normal_time_1':a_work_normal_time_1,
                                'a_work_over_time_1':a_work_over_time_1,
                                'a_work_availability_time_1':a_work_availability_time_1, 
                                'a_work_remark_1':a_work_remark_1,

                                'a_work_station_2':a_work_station_2, 
                                'a_production_2':a_production_2,
                                'a_product_no_2':a_product_no_2,
                                'a_work_normal_time_2':a_work_normal_time_2,
                                'a_work_over_time_2':a_work_over_time_2,
                                'a_work_availability_time_2':a_work_availability_time_2, 
                                'a_work_remark_2':a_work_remark_2,
                                
                                'a_work_remark_3':a_work_remark_3,
                                'a_work_station_3':a_work_station_3, 
                                'a_production_3':a_production_3,
                                'a_product_no_3':a_product_no_3,
                                'a_work_normal_time_3':a_work_normal_time_3,
                                'a_work_over_time_3':a_work_over_time_3,
                                'a_work_availability_time_3':a_work_availability_time_3, 
                                'a_work_remark_3':a_work_remark_3,

                                'a_work_remark_4':a_work_remark_4,
                                'a_work_station_4':a_work_station_4, 
                                'a_production_4':a_production_4,
                                'a_product_no_4':a_product_no_4,
                                'a_work_normal_time_4':a_work_normal_time_4,
                                'a_work_over_time_4':a_work_over_time_4,
                                'a_work_availability_time_4':a_work_availability_time_4, 
                                'a_work_remark_4':a_work_remark_4,

                                'a_work_remark_5':a_work_remark_5,
                                'a_work_station_5':a_work_station_5, 
                                'a_production_5':a_production_5,
                                'a_product_no_5':a_product_no_5,
                                'a_work_normal_time_5':a_work_normal_time_5,
                                'a_work_over_time_5':a_work_over_time_5,
                                'a_work_availability_time_5':a_work_availability_time_5, 
                                'a_work_remark_5':a_work_remark_5,

                                'a_work_remark_6':a_work_remark_6,
                                'a_work_station_6':a_work_station_6, 
                                'a_production_6':a_production_6,
                                'a_product_no_6':a_product_no_6,
                                'a_work_normal_time_6':a_work_normal_time_6,
                                'a_work_over_time_6':a_work_over_time_6,
                                'a_work_availability_time_6':a_work_availability_time_6, 
                                'a_work_remark_6':a_work_remark_6,

                                'a_work_remark_7':a_work_remark_7,
                                'a_work_station_7':a_work_station_7, 
                                'a_production_7':a_production_7,
                                'a_product_no_7':a_product_no_7,
                                'a_work_normal_time_7':a_work_normal_time_7,
                                'a_work_over_time_7':a_work_over_time_7,
                                'a_work_availability_time_7':a_work_availability_time_7, 
                                'a_work_remark_7':a_work_remark_7,

                                'a_work_remark_8':a_work_remark_8,
                                'a_work_station_8':a_work_station_8, 
                                'a_production_8':a_production_8,
                                'a_product_no_8':a_product_no_8,
                                'a_work_normal_time_8':a_work_normal_time_8,
                                'a_work_over_time_8':a_work_over_time_8,
                                'a_work_availability_time_8':a_work_availability_time_8, 
                                'a_work_remark_8':a_work_remark_8,

                                'a_work_remark_9':a_work_remark_9,
                                'a_work_station_9':a_work_station_9, 
                                'a_production_9':a_production_9,
                                'a_product_no_9':a_product_no_9,
                                'a_work_normal_time_9':a_work_normal_time_9,
                                'a_work_over_time_9':a_work_over_time_9,
                                'a_work_availability_time_9':a_work_availability_time_9, 
                                'a_work_remark_9':a_work_remark_9,

                                'a_work_remark_10':a_work_remark_10,
                                'a_work_station_10':a_work_station_10, 
                                'a_production_10':a_production_10,
                                'a_product_no_10':a_product_no_10,
                                'a_work_normal_time_10':a_work_normal_time_10,
                                'a_work_over_time_10':a_work_over_time_10,
                                'a_work_availability_time_10':a_work_availability_time_10, 
                                'a_work_remark_10':a_work_remark_10,

                                'a_work_remark_11':a_work_remark_11,
                                'a_work_station_11':a_work_station_11, 
                                'a_production_11':a_production_11,
                                'a_product_no_11':a_product_no_11,
                                'a_work_normal_time_11':a_work_normal_time_11,
                                'a_work_over_time_11':a_work_over_time_11,
                                'a_work_availability_time_11':a_work_availability_time_11, 
                                'a_work_remark_11':a_work_remark_11,

                                'a_work_remark_12':a_work_remark_12,
                                'a_work_station_12':a_work_station_12, 
                                'a_production_12':a_production_12,
                                'a_product_no_12':a_product_no_12,
                                'a_work_normal_time_12':a_work_normal_time_12,
                                'a_work_over_time_12':a_work_over_time_12,
                                'a_work_availability_time_12':a_work_availability_time_12, 
                                'a_work_remark_12':a_work_remark_12
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
                                alert(xhr.status);
                                alert(xhr.responseText);
                                alert(throwError);
                                alert(ajaxError);
                        },
                        success:function(res){
                                
                                $("#menu_money_record_list").show(1000).html(res);
                                alert(b_date + ' , 新增完成。');
                                
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("submit 液劑工時紀錄清單 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });
        }

}

function auto_plus_availability_work_time(){
        var a_work_availability_time_1       = $('#a_work_availability_time_1').val();
        var a_work_availability_time_2       = $('#a_work_availability_time_2').val();
        var a_work_availability_time_3       = $('#a_work_availability_time_3').val();
        var a_work_availability_time_4       = $('#a_work_availability_time_4').val();
        var a_work_availability_time_5       = $('#a_work_availability_time_5').val();
        var a_work_availability_time_6       = $('#a_work_availability_time_6').val();
        var a_work_availability_time_7       = $('#a_work_availability_time_7').val();
        var a_work_availability_time_8       = $('#a_work_availability_time_8').val();
        var a_work_availability_time_9       = $('#a_work_availability_time_9').val();
        var a_work_availability_time_10       = $('#a_work_availability_time_10').val();
        var a_work_availability_time_11       = $('#a_work_availability_time_11').val();
        var a_work_availability_time_12       = $('#a_work_availability_time_12').val();

        // auto plus availability work time
        var auto_plus_availability_work_time_val = (Number(a_work_availability_time_1) + Number(a_work_availability_time_2) + Number(a_work_availability_time_3)  + Number(a_work_availability_time_4)  + Number(a_work_availability_time_5)  + Number(a_work_availability_time_6) + 
                                             Number(a_work_availability_time_7) + Number(a_work_availability_time_8) + Number(a_work_availability_time_9)  + Number(a_work_availability_time_10)  + Number(a_work_availability_time_11)  + Number(a_work_availability_time_12)).toFixed(1);
        $('#auto_plus_availability_work_time').show().html(auto_plus_availability_work_time_val);
        
        // auto plus total work time
        //var auto_plus_total_work_time_val = (Number($('#auto_plus_over_work_time').text()) + Number($('#auto_plus_normal_work_time').text()) + Number($('#auto_plus_availability_work_time').text())).toFixed(1)
        var auto_plus_total_work_time_val = (Number($('#auto_plus_over_work_time').text()) + Number($('#auto_plus_normal_work_time').text())).toFixed(1)

        $('#auto_plus_total_work_time').val(auto_plus_total_work_time_val);
}

function auto_plus_over_work_time(){
        var a_work_over_time_1       = $('#a_work_over_time_1').val();
        var a_work_over_time_2       = $('#a_work_over_time_2').val();
        var a_work_over_time_3       = $('#a_work_over_time_3').val();
        var a_work_over_time_4       = $('#a_work_over_time_4').val();
        var a_work_over_time_5       = $('#a_work_over_time_5').val();
        var a_work_over_time_6       = $('#a_work_over_time_6').val();
        var a_work_over_time_7       = $('#a_work_over_time_7').val();
        var a_work_over_time_8       = $('#a_work_over_time_8').val();
        var a_work_over_time_9       = $('#a_work_over_time_9').val();
        var a_work_over_time_10       = $('#a_work_over_time_10').val();
        var a_work_over_time_11       = $('#a_work_over_time_11').val();
        var a_work_over_time_12       = $('#a_work_over_time_12').val();

        // auto plus over work time
        var auto_plus_over_work_time_val = (Number(a_work_over_time_1) + Number(a_work_over_time_2) + Number(a_work_over_time_3)  + Number(a_work_over_time_4)  + Number(a_work_over_time_5)  + Number(a_work_over_time_6) + 
                                             Number(a_work_over_time_7) + Number(a_work_over_time_8) + Number(a_work_over_time_9)  + Number(a_work_over_time_10)  + Number(a_work_over_time_11)  + Number(a_work_over_time_12)).toFixed(1);
        
        $('#auto_plus_over_work_time').show().html(auto_plus_over_work_time_val);


        // auto plus total work time
        //var auto_plus_total_work_time_val = (Number($('#auto_plus_over_work_time').text()) + Number($('#auto_plus_normal_work_time').text()) + Number($('#auto_plus_availability_work_time').text())).toFixed(1)
        var auto_plus_total_work_time_val = (Number($('#auto_plus_over_work_time').text()) + Number($('#auto_plus_normal_work_time').text())).toFixed(1)

        $('#auto_plus_total_work_time').val(auto_plus_total_work_time_val);
}  

function auto_plus_normal_work_time(){
        var a_work_normal_time_1       = $('#a_work_normal_time_1').val();
        var a_work_normal_time_2       = $('#a_work_normal_time_2').val();
        var a_work_normal_time_3       = $('#a_work_normal_time_3').val();
        var a_work_normal_time_4       = $('#a_work_normal_time_4').val();
        var a_work_normal_time_5       = $('#a_work_normal_time_5').val();
        var a_work_normal_time_6       = $('#a_work_normal_time_6').val();
        var a_work_normal_time_7       = $('#a_work_normal_time_7').val();
        var a_work_normal_time_8       = $('#a_work_normal_time_8').val();
        var a_work_normal_time_9       = $('#a_work_normal_time_9').val();
        var a_work_normal_time_10      = $('#a_work_normal_time_10').val();
        var a_work_normal_time_11      = $('#a_work_normal_time_11').val();
        var a_work_normal_time_12      = $('#a_work_normal_time_12').val();

        // auto plus normal work time
        var auto_plus_normal_work_time_val = (Number(a_work_normal_time_1) + Number(a_work_normal_time_2) + Number(a_work_normal_time_3)  + Number(a_work_normal_time_4)  + Number(a_work_normal_time_5)  + Number(a_work_normal_time_6) + 
                                             Number(a_work_normal_time_7) + Number(a_work_normal_time_8) + Number(a_work_normal_time_9)  + Number(a_work_normal_time_10)  + Number(a_work_normal_time_11)  + Number(a_work_normal_time_12)).toFixed(1);

        $('#auto_plus_normal_work_time').show().html(auto_plus_normal_work_time_val);

        // auto plus total work time
        //var auto_plus_total_work_time_val = (Number($('#auto_plus_over_work_time').text()) + Number($('#auto_plus_normal_work_time').text()) + Number($('#auto_plus_availability_work_time').text())).toFixed(1)
        var auto_plus_total_work_time_val = (Number($('#auto_plus_over_work_time').text()) + Number($('#auto_plus_normal_work_time').text())).toFixed(1)

        $('#auto_plus_total_work_time').val(auto_plus_total_work_time_val);

}    

function submit_add_account_form(){
        
        var a_work_no  = $('#a_work_no').val();
        var a_date     = $('#a_date').val();
        var a_name     = $('#a_name').val();
        var a_user     = $('#a_user').val();
        var a_position = $('#a_position').val();
        var a_status   = $('#a_status').val();
        
        var data    = a_date.split('-')
        var r_year  = data[0];
        var r_month = data[1];
        var r_day   = data[2];

        // check 帳號
	if(a_user.length == 0){
	        /// show msg
                alert('帳號不能空白 !!!')
	        exit;
	}
        // check 工號
	if(a_work_no.length == 0){
	        /// show msg
                alert('工號不能空白 !!!')
	        exit;
	}
        // check 姓名 
	if(a_name.length == 0){
	        /// show msg
                alert('姓名不能空白 !!!')
	        exit;
	}
        // check 部門 
	if(a_position.length == 0){
	        /// show msg
                alert('部門不能空白 !!!')
	        exit;
	}
        // check 帳號狀態
	if(a_status.length == 0){
	        /// show msg
                alert('狀態不能空白 !!!')
	        exit;
	}

        //alert(a_work_no + ' / ' +  a_date + ' / ' + a_name + ' / ' + a_position + ' / ' + a_status)
        //exit();

        $.ajax({
                type:"POST",
                url:"/submit_add_account_form",
                data:{
                        'a_user':a_user,
                        'a_name':a_name,
                        'a_date':a_date,
                        'a_work_no':a_work_no,
                        'a_position':a_position,
                        'a_status':a_status
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                      alert(ajaxError)
                },
                success:function(res){
                        
                        // clean value
                        $('#a_work_no').val('');
                        $('#a_date').val('');
                        $('#a_name').val('');
                        $('#a_user').val('');
                        $('#a_position').val('');
                        $('#a_status').val('');
                        
                        // reload account list
                        reload_menu_account_list();
                },
                beforeSend:function(){
                        //$('#show_msg').html('載入操作紀錄管理中...').css({'color':'red'}).show();
                        //$('#add_content').show(1000);
                },
                complete:function(){
                        //$('#show_msg').hide();
                }
        });     
}

function logout2(){
        
        // scroll to top 
        jQuery("html,body").animate({scrollTop:0},1000);

        $.ajax({
                type:"GET",
                url:"/logout2",
                data:{},
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
                        
                        alert("超過10分鐘沒任何度動作 , 系統已將您已自動登出 !");
                        window.location.href="/login"
                        //$("#add_account_form").show(1000).html(res);
                },
                beforeSend:function(){
                        $('#status').html("now logout...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function add_account_form(){
        
        // scroll to top 
        jQuery("html,body").animate({scrollTop:0},1000);

        $.ajax({
                type:"POST",
                url:"/load_account_form",
                data:{},
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      $('#click_show_msg').click();
                        $('#show_msg').show(1000).html(xhr.responseText);
                },
                success:function(res){
        	       	$("#add_account_form").show(1000).html(res);
                },
                beforeSend:function(){
                        $('#status').html("loading 新增帳號表 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function reload_menu_account_list(){
        $.ajax({
                type:"GET",
                url:"/reload_menu_account_list",
                data:{},
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                },
                success:function(res){
                        
                        //location.reload(true);
                        $("#otsuka_account_list").show(1000).html(res);  
                },
                beforeSend:function(){
                        $('#status').html("loading 帳號清單 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });                
}

function load_menu_money_record_by_kind(val){
        var kind = val;
        
                $.ajax({
                        type:"POST",
                        url:"/load_menu_money_record_by_kind",
                        data:{
                                'kind':kind
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
         	                alert(xhr.status);
               	                alert(xhr.responseText);
	                        alert(throwError);
                                alert(ajaxError);
                        },
                        success:function(res){
                                
                                $("#menu_money_record_list").show(1000).html(res);
                                
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("loading " + kind + " 種類記帳本清單 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });

}

function load_menu_money_record_by_day(val){
        var day = val;
        
                $.ajax({
                        type:"POST",
                        url:"/load_menu_money_record_by_day",
                        data:{
                                'day':day
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
         	                alert(xhr.status);
               	                alert(xhr.responseText);
	                        alert(throwError);
                                alert(ajaxError)
                        },
                        success:function(res){
                                
                                $("#menu_money_record_list").show(1000).html(res);
                                
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("loading " + day + " 日記帳本清單 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });

}

function load_menu_money_record_by_month(val){
        var month = val;
        
                $.ajax({
                        type:"POST",
                        url:"/load_menu_money_record_by_month",
                        data:{
                                'month':month
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
         	                alert(xhr.status);
               	                alert(xhr.responseText);
	                        alert(throwError);
                                alert(ajaxError)
                        },
                        success:function(res){
                                
                                $("#menu_money_record_list").show(1000).html(res);
                                
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("loading " + month + " 月記帳本清單 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });

}

function load_menu_car_record_by_day(val){
        var day = val;
        
                $.ajax({
                        type:"POST",
                        url:"/load_menu_car_record_by_day",
                        data:{
                                'day':day
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
         	                alert(xhr.status);
               	                alert(xhr.responseText);
	                        alert(throwError);
                                alert(ajaxError)
                        },
                        success:function(res){
                                
                                $("#menu_car_record_list").show(1000).html(res);
                                
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("loading " + day + " 日用車記錄 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });

}

function load_menu_car_record_by_month(val){
        var month = val;
        
                $.ajax({
                        type:"POST",
                        url:"/load_menu_car_record_by_month",
                        data:{
                                'month':month
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
         	                alert(xhr.status);
               	                alert(xhr.responseText);
	                        alert(throwError);
                                alert(ajaxError)
                        },
                        success:function(res){
                                
                                $("#menu_car_record_list").show(1000).html(res);
                                
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("loading " + month + " 月用車記錄 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });

}

function load_menu_car_record_by_year(val){
        var year = val;
        
                $.ajax({
                        type:"POST",
                        url:"/load_menu_car_record_by_year",
                        data:{
                                'year':year
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
         	                alert(xhr.status);
               	                alert(xhr.responseText);
	                        alert(throwError);
                                alert(ajaxError)
                        },
                        success:function(res){
                                
                                $("#menu_car_record_list").show(1000).html(res);
                                
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("loading " + year + " 年用車記錄 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });

}

function load_menu_money_record_by_year(val){
        var year = val;
        
                $.ajax({
                        type:"POST",
                        url:"/load_menu_money_record_by_year",
                        data:{
                                'year':year
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
         	                alert(xhr.status);
               	                alert(xhr.responseText);
	                        alert(throwError);
                                alert(ajaxError)
                        },
                        success:function(res){
                                
                                $("#menu_money_record_list").show(1000).html(res);
                                
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("loading " + year + " 年記帳本清單 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });

}

function load_menu_calendar_record_by_month(val){
        var month = val;
        
                $.ajax({
                        type:"POST",
                        url:"/load_menu_calendar_record_by_month",
                        data:{
                                'month':month
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
         	                alert(xhr.status);
               	                alert(xhr.responseText);
	                        alert(throwError);
                                alert(ajaxError)
                        },
                        success:function(res){
                                
                                $("#menu_calendar_record_content").show(1000).html(res);
                                
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("loading " + month + " 月工作日誌 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });

}

function load_menu_work_record_by_kind(val){
        var kind = val;
        
                $.ajax({
                        type:"POST",
                        url:"/load_menu_work_record_by_kind",
                        data:{
                                'kind':kind
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
         	                alert(xhr.status);
               	                alert(xhr.responseText);
	                        alert(throwError);
                                alert(ajaxError)
                        },
                        success:function(res){
                                
                                $("#menu_work_record_content").show(1000).html(res);
                                
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("loading " + kind + " 工作記錄 ...").css({'color':'red'});
                        },
                        complete:function(){
                                $('#status').css({'color':'#f8f9fa'});
                        }
                });

}

function del_menu_car_record(val){
        
        var del_no = val;
        
        var check_del = prompt("刪除 No." + del_no + " , 確定刪除 , 再按一次 y ");
        
	if(check_del == 'y'){	
                $.ajax({
                        type:"POST",
                        url:"/del_menu_car_record",
                        data:{
                                'del_no':del_no
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
         	                alert(xhr.status);
               	                alert(xhr.responseText);
	                        alert(throwError);
                                alert(ajaxError)
                        },
                        success:function(res){
                                location.reload(true);
                        },
                        beforeSend:function(){
                                $('#menu_money_record_list').show(1000);
                        },
                        complete:function(){
                        }
                });
	}else{
                exit();
        }
}

function del_menu_money_record(val){
        
        var del_no = val;
        
        var check_del = prompt("刪除 No." + del_no + " , 確定刪除 , 再按一次 y ");
        
	if(check_del == 'y'){	
                $.ajax({
                        type:"POST",
                        url:"/del_menu_money_record",
                        data:{
                                'del_no':del_no
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
         	                alert(xhr.status);
               	                alert(xhr.responseText);
	                        alert(throwError);
                                alert(ajaxError)
                        },
                        success:function(res){
                                
                                //$('#menu_money_record_list').show(1000).html(res);
                                
                                // reload menu money record
                                reload_menu_money_record();
                        },
                        beforeSend:function(){
                                //$('#show_msg').html('載入操作紀錄管理中...').css({'color':'red'}).show();
                                $('#menu_money_record_list').show(1000);
                        },
                        complete:function(){
                                //$('#show_msg').hide();
                        }
                });
	}else{
                exit();
        }
}

function goto_top(){
        
        // scroll page bottom to page top
        jQuery("html,body").animate({scrollTop:0},0);
        $('#goto_top').css({'cursor':'pointer'});

}

function submit_alter_calendar_record_form(){
        
        var no      = $('#no').val();
        var r_time  = $('#record_time').val();
        var title   = $('#title').val();
        var content = CKEDITOR.instances.content.getData();

        $.ajax({
                type:"POST",
                url:"/submit_alter_calendar_record",
                data:{
                        'no':no,
                        'r_time':r_time,
                        'title':title,
                        'content':content
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                      alert(ajaxError)
                },
                success:function(res){
			
                        alert(title + '  , 修改完成。');
                        location.reload(true);
                },
                beforeSend:function(){
                        //$('#show_msg').html('載入操作紀錄管理中...').css({'color':'red'}).show();
                        $('#detail_calendar_record_content').show(1000);
                },
                complete:function(){
                        //$('#show_msg').hide();
                }
        });
}

function submit_alter_work_record_form(){
        
        var no      = $('#no').val();
        var r_time  = $('#record_time').val();
        var kind    = $('#kind').val();
        var title   = $('#title').val();
        var content = CKEDITOR.instances.content.getData();

        $.ajax({
                type:"POST",
                url:"/submit_alter_work_record",
                data:{
                        'no':no,
                        'r_time':r_time,
                        'kind':kind,
                        'title':title,
                        'content':content
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                      alert(ajaxError)
                },
                success:function(res){
			//$("#content").css({'border':'#cccccc 1px solid'});
        	       	//$("#detail_work_record_content").show(1000).html(res);
                        
                        alert(kind + ' - ' + title + '  , 修改完成。');

                        location.reload(true);
                        // load alter  detail work record
                        //detail_work_record(no);

                        // reload menu work record
                        //reload_menu_work_record();
                },
                beforeSend:function(){
                        //$('#show_msg').html('載入操作紀錄管理中...').css({'color':'red'}).show();
                        $('#detail_work_record_content').show(1000);
                },
                complete:function(){
                        //$('#show_msg').hide();
                }
        });
        

}

function detail_calendar_record(val){
        
        var no = val;
        
        // scroll to top 
        jQuery("html,body").animate({scrollTop:0},1000);

        $.ajax({
                type:"POST",
                url:"/detail_calendar_record",
                data:{
                        'no':no
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                      alert(ajaxError)
                },
                success:function(res){
			//$("#content").css({'border':'#cccccc 1px solid'});
                        
        	       	$("#detail_calendar_record_content").show(1000).html(res);
                },
                beforeSend:function(){
                        //$('#show_msg').html('載入操作紀錄管理中...').css({'color':'red'}).show();
                        $('#detail_calendar_record_content').show(1000);
                },
                complete:function(){
                        //$('#show_msg').hide();
                }
        });
}

function detail_work_record(val){

        var no = val;
        
        // scroll to top 
        jQuery("html,body").animate({scrollTop:0},1000);

        $.ajax({
                type:"POST",
                url:"/detail_work_record",
                data:{
                        'no':no
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                      alert(ajaxError)
                },
                success:function(res){
			//$("#content").css({'border':'#cccccc 1px solid'});
        	       	$("#detail_work_record_content").show(1000).html(res);
                },
                beforeSend:function(){
                        $('#status').html("loading " + no + " 工作記錄 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });
}

function submit_add_work_record_form(){
        
        var user = $('#user').val();
        var date = $('#date').val();
        var kind = $('#kind').val();
        var title = $('#title').val();
        var content = CKEDITOR.instances.content.getData();

        //alert(user + ' / ' + date + ' / ' + kind + ' / ' + money + ' / ' + content + ' / ' + record_year + ' / ' + record_month + ' / ' + record_day)
        
        // check kind 
	if(kind.length == 0){
	        /// show msg
                $("#kind").css({'border-bottom-color':'red'});
		$("#show_msg").css({'color':'red'}).html("<i class='bi bi-x-circle-fill'></i> 工作記錄種類不能空白 !!!");
	        exit;
	}
        // check title
	if(title.length == 0){
	        /// show msg
                $("#title").css({'border-bottom-color':'red'});
		$("#show_msg").css({'color':'red'}).html("<i class='bi bi-x-circle-fill'></i> 工作記錄標體不能空白 !!!");
	        exit;
	}
        // check content 
	if(content.length == 0){
	        /// show msg
                $("#content").css({'border-bottom-color':'red'});
		$("#show_msg").css({'color':'red'}).html("<i class='bi bi-x-circle-fill'></i> 工作記錄內容不能空白 !!!");
	        exit;
	}

        $.ajax({
                type:"POST",
                url:"/submit_add_work_record_form",
                data:{
                        'user':user,
                        'date':date,
                        'kind':kind,
                        'title':title,
                        'content':content
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                      alert(ajaxError)
                },
                success:function(res){
                        //console.log(res.validate);
			//$("#content").css({'border':'#cccccc 1px solid'});
        	       	//$("#add_content").show(1000).html(res);
                        
                        // clean show msg value
                        $("#show_msg").val('');
                        
                        // reload menu work record
                        reload_menu_work_record();
                },
                beforeSend:function(){
                        //$('#show_msg').html('載入操作紀錄管理中...').css({'color':'red'}).show();
                        $('#add_content').show(1000);
                },
                complete:function(){
                        //$('#show_msg').hide();
                }
        });        

}

function submit_add_car_record_form(){
        
        var user = $('#user').val();
        var date = $('#date').val();
        var kind = $('#kind').val();
        var go_out_km = $('#go_out_km').val();
        var go_home_km = $('#go_home_km').val();
        var total_used_km = go_home_km - go_out_km;
        var destination = $('#destination').val();
        var data = date.split('-');
        var r_year = data[0];
        var r_month = data[0]+'-'+data[1];
        var r_day = data[2];

        
        // check kind 
	if(kind.length == 0){
	        /// show msg
                $("#kind").css({'border-bottom-color':'red'});
		$("#show_msg").css({'color':'red'}).html("<i class='bi bi-x-circle-fill'></i> 用車種類不能空白 !!!");
	        exit;
	}
        // check go_home_km
	if(go_home_km.length == 0){
	        /// show msg
                $("#go_home_km").css({'border-bottom-color':'red'});
		$("#show_msg").css({'color':'red'}).html("<i class='bi bi-x-circle-fill'></i> 入庫里程不能空白 !!!");
	        exit;
	}
        // check destination
	if(destination.length == 0){
	        /// show msg
                $("#destination").css({'border-bottom-color':'red'});
		$("#show_msg").css({'color':'red'}).html("<i class='bi bi-x-circle-fill'></i> 用車記錄內容不能空白 !!!");
	        exit;
	}



        $.ajax({
                type:"POST",
                url:"/submit_add_car_record_form",
                data:{
                        'user':user,
                        'date':date,
                        'kind':kind,
                        'go_out_km':go_out_km,
                        'go_home_km':go_home_km,
                        'total_used_km':total_used_km,
                        'destination':destination,
                        'r_year':r_year,
                        'r_month':r_month,
                        'r_day':r_day
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                      alert(ajaxError)
                },
                success:function(res){
                        
                        //alert('ok');
                        //$("#add_content").show(1000).html(res);
                        
                        // clean show msg value
                        //$("#show_msg").val('');
                        
                        // reload menu money record
                        //reload_menu_money_record();
                        location.reload(true);
                        
                },
                beforeSend:function(){
                        //$('#show_msg').html('載入操作紀錄管理中...').css({'color':'red'}).show();
                        $('#add_content').show(1000);
                },
                complete:function(){
                        //$('#show_msg').hide();
                }
        });        

}

function submit_add_money_record_form(){
        
        var user = $('#user').val();
        var date = $('#date').val();
        var kind = $('#kind').val();
        var money = $('#money').val();
        var content = $('#content').val();
        var data1 = date.split(' ')
        var data2 = data1[0].split('-')
        var record_year = data2[0];
        var record_month = data2[1];
        var record_day = data2[2];

        //alert(user + ' / ' + date + ' / ' + kind + ' / ' + money + ' / ' + content + ' / ' + record_year + ' / ' + record_month + ' / ' + record_day)
        
        // check kind 
	if(kind.length == 0){
	        /// show msg
                $("#kind").css({'border-bottom-color':'red'});
		$("#show_msg").css({'color':'red'}).html("<i class='bi bi-x-circle-fill'></i> 記帳表種類不能空白 !!!");
	        exit;
	}
        // check money
	if(money.length == 0){
	        /// show msg
                $("#money").css({'border-bottom-color':'red'});
		$("#show_msg").css({'color':'red'}).html("<i class='bi bi-x-circle-fill'></i> 記帳表花費不能空白 !!!");
	        exit;
	}
        // check content 
	if(content.length == 0){
	        /// show msg
                $("#content").css({'border-bottom-color':'red'});
		$("#show_msg").css({'color':'red'}).html("<i class='bi bi-x-circle-fill'></i> 記帳表內容不能空白 !!!");
	        exit;
	}

        $.ajax({
                type:"POST",
                url:"/submit_add_money_record_form",
                data:{
                        'user':user,
                        'date':date,
                        'kind':kind,
                        'money':money,
                        'content':content,
                        'record_year':record_year,
                        'record_month':record_month,
                        'record_day':record_day
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                      alert(ajaxError)
                },
                success:function(res){
                        
                        $("#add_content").show(1000).html(res);
                        
                        // clean show msg value
                        $("#show_msg").val('');
                        
                        // reload menu money record
                        //reload_menu_money_record();

                        location.reload(true);
                },
                beforeSend:function(){
                        //$('#show_msg').html('載入操作紀錄管理中...').css({'color':'red'}).show();
                        $('#add_content').show(1000);
                },
                complete:function(){
                        //$('#show_msg').hide();
                }
        });        

}

function reload_menu_money_record_by_day(){
        $.ajax({
                type:"GET",
                url:"/reload_menu_money_record_by_day",
                //url:"/menu_calendar_record",
                data:{},
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                },
                success:function(res){
                        
                        location.reload(true);
                        $("#money_record_by_day").show(1000).html(res);  
                },
                beforeSend:function(){
                        $('#status').html("loading 記帳本 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });                
}

function reload_menu_car_record(){
        $.ajax({
                type:"GET",
                url:"/reload_menu_car_record",
                //url:"/menu_calendar_record",
                data:{},
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                },
                success:function(res){
                        
                        location.reload(true);
                        $("#menu_car_record_list").show(1000).html(res);  
                },
                beforeSend:function(){
                        $('#status').html("loading 用車記錄 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });                
}

function reload_menu_money_record(){
        $.ajax({
                type:"GET",
                url:"/reload_menu_money_record",
                //url:"/menu_calendar_record",
                data:{},
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                },
                success:function(res){
                        
                        location.reload(true);
                        $("#menu_money_record_list").show(1000).html(res);  
                },
                beforeSend:function(){
                        $('#status').html("loading 記帳本 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });                
}

function reload_menu_calendar_record(){
        $.ajax({
                type:"GET",
                url:"/reload_menu_calendar_record",
                //url:"/menu_calendar_record",
                data:{},
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                },
                success:function(res){
                        
                        location.reload(true);
                        $("#main_content").show(1000).html(res);  
                },
                beforeSend:function(){
                        $('#status').html("loading 工作日誌 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });                
}

function reload_menu_work_record(){
        $.ajax({
                type:"GET",
                url:"/reload_menu_work_record",
                data:{},
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                },
                success:function(res){
                        
                        $("#menu_work_record_content").html(res);  
                        location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("loading 工作記錄 ...").css({'color':'red'});
                },
                complete:function(){
                        $('#status').css({'color':'#f8f9fa'});
                }
        });                
}

function select_car_record_kind(val){
        var data = val;
        $('#kind').val(data);

        // select go out km 
        $.ajax({
                type:"POST",
                url:"/select_car_record_by_go_out_km",
                data:{
                        'kind':val
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                      alert(ajaxError)
                },
                success:function(res){

                        $('#go_out_km').val(res);
                },
                beforeSend:function(){
                        $('#detail_calendar_record_content').show(1000);
                },
                complete:function(){
                        
                }
        });

}

function select_money_record_kind(val){
        var data = val;
        $('#kind').val(data);
}

function del_alter_calendar_record_form(){
        
        var no = $('#no').val();

        var check_del = prompt("刪除 No." + no + " ， 確定請再按一次 y : ");
	if(check_del != 'y'){	
                exit();
	}else{

                $.ajax({
                type:"POST",
                url:"/del_alter_calendar_record_form",
                data:{
                        'no':no
                },
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                      alert(ajaxError)
                },
                success:function(res){

                        $('#detail_calendar_record_content').hide(1000);
                        
                        // reload menu calendar record
                        reload_menu_calendar_record();
                },
                beforeSend:function(){
                        //$('#show_msg').html('載入操作紀錄管理中...').css({'color':'red'}).show();
                        $('#detail_calendar_record_content').show(1000);
                },
                complete:function(){
                        //$('#show_msg').hide();
                }
                });
        }
}

function cancel_add_work_record_form(){
        $('#kind').val('');
        $('#content').val('');
        $('#title').val('');

        $("#add_work_form").hide(1000);
        location.reload(true);
}

function cancel_add_money_record_form(){
        $('#kind').val('');
        $('#content').val('');
        $('#money').val('');

        $("#add_money_form").hide(1000);
        location.reload(true);
}

function add_calendar_record(){
        
        // scroll page bottom to page top 
        jQuery("html,body").animate({scrollTop:0},1000);

        $.ajax({
                type:"GET",
                url:"/add_calendar_record_form",
                data:{},
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                },
                success:function(res){
			
                        //$("#content").css({'border':'#cccccc 1px solid'});
        	       	$("#add_content").show(1000).html(res);

                        // hide alter work record form content
                        $('#detail_work_record_content').hide(1000);
                },
                beforeSend:function(){
                        //$('#show_msg').html('載入操作紀錄管理中...').css({'color':'red'}).show();
                        $('#add_content').show(1000);
                },
                complete:function(){
                        //$('#show_msg').hide();
                }
        });        
}

function add_work_record(){
        
        // scroll to top 
        jQuery("html,body").animate({scrollTop:0},1000);

        $.ajax({
                type:"GET",
                url:"/add_work_record_form",
                data:{},
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                },
                success:function(res){
			
                        //$("#content").css({'border':'#cccccc 1px solid'});
        	       	$("#add_content").show(1000).html(res);

                        // hide alter work record form content
                        $('#detail_work_record_content').hide(1000);
                },
                beforeSend:function(){
                        //$('#show_msg').html('載入操作紀錄管理中...').css({'color':'red'}).show();
                        $('#add_content').show(1000);
                },
                complete:function(){
                        //$('#show_msg').hide();
                }
        });        
}

function add_car_record(){
        $.ajax({
                type:"GET",
                url:"/add_car_record_form",
                data:{},
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                },
                success:function(res){
			//$("#content").css({'border':'#cccccc 1px solid'});
        	       	$("#add_content").show(1000).html(res);
                               
                },
                beforeSend:function(){
                        //$('#show_msg').html('載入操作紀錄管理中...').css({'color':'red'}).show();
                        $('#add_content').show(1000);
                },
                complete:function(){
                        //$('#show_msg').hide();
                }
        });        
}

function add_website_record(){
        $.ajax({
                type:"GET",
                url:"/add_website_record_form",
                data:{},
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                },
                success:function(res){
			//$("#content").css({'border':'#cccccc 1px solid'});
        	       	$("#add_content").show(1000).html(res);
                               
                },
                beforeSend:function(){
                        //$('#show_msg').html('載入操作紀錄管理中...').css({'color':'red'}).show();
                        $('#add_content').show(1000);
                },
                complete:function(){
                        //$('#show_msg').hide();
                }
        });        
}

function add_money_record(){
        $.ajax({
                type:"GET",
                url:"/add_money_record_form",
                data:{},
                datatype:"html",
                error:function(xhr , ajaxError , throwError){
         	      alert(xhr.status);
               	      alert(xhr.responseText);
	              alert(throwError);
                },
                success:function(res){
			//$("#content").css({'border':'#cccccc 1px solid'});
        	       	$("#add_content").show(1000).html(res);
                               
                },
                beforeSend:function(){
                        //$('#show_msg').html('載入操作紀錄管理中...').css({'color':'red'}).show();
                        $('#add_content').show(1000);
                },
                complete:function(){
                        //$('#show_msg').hide();
                }
        });        
}

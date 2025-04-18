/************************************************************************************************************************* 
 *
 * ERP - 進銷明細查詢
 * 
 *************************************************************************************************************************/ 
const p_s_detail_list = Vue.createApp({
    delimiters: ['[[', ']]'],  // Custom delimiters if needed
    data() {
        return {
            p_s_date: '',  
            p_s_person: '',  
            q_c_name:'',
            q_p_name:'',
            msg: '',
            status: '',
            l_status: '',
            show_msg:'',
            f_erp_realtime_query3:'',
            i_q_c_name:'',
            i_q_p_name:''
        };
    },
    methods: {

        /**************
         * 匯出 Excel
         **************/ 
        e_f_excel(){

            // 起始日期
            if(!this.q_s_date || this.q_s_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> ERP 子單身 - 起始日期不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            // 結束日期
            else if(!this.q_e_date || this.q_e_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> ERP 子單身 - 結束日期不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }else{
                
                const params = new URLSearchParams();
                params.append('q_s_date', this.q_s_date);
                params.append('q_e_date', this.q_e_date);

                // l_status
                this.l_status = '匯出 ' + this.q_s_name + ' ~ ' + this.q_e_date + ' ERP 子單身 Excel 資料...';
                
                // ajax - axioss
                axios.post('/factory_erp_subform_download_excel', params , {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })
                .then(response => {
                    
                    const s_date = this.q_s_date;
                    const e_date = this.q_e_date;

                    const s_d = s_date.replace(/-/g, "");
                    const e_d = e_date.replace(/-/g, "");

                    var url      = "/download_factory_erp_subform_excel?q_s_date=" + s_d + "&q_e_date=" + e_d;
                    var fileName = 'factory_erp_subform_' + s_d + '_' + e_d + '.xlsx';


                    // 创建一个动态链接并触发点击
                    var link = $('<a></a>')
                            .attr('href', url)
                            .attr('download', fileName)
                            .appendTo('body');

                    link[0].click();
                    link.remove(); // 清理动态创建的元素
                    
                    this.goto_top();  // Assuming this is defined
                })
                .catch(error => {
                    if (error.response) {
                        console.error('Server responded with an error:', error.response);
                        this.show_msg = error.response.data;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else if (error.request) {
                        console.error('No response received:', error.request);
                        this.show_msg = 'No response from server.';
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else {
                        console.error('Error:', error.message);
                        this.show_msg = 'An error occurred: ' + error.message;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    }
                })
                .finally(() => {
                    
                    setTimeout(() => {
                        this.l_status = '';
                    } , 1000);
                    
                });
            }
        },
        /**********
         * 搜尋
         **********/ 
        p_s_q_s_submit() {
            
            // 建立人
            if(!this.q_s_date || this.q_s_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> ERP - 查詢進銷明細建立人不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            // 申報年月
            else if(!this.q_e_date || this.q_e_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> ERP - 查詢進銷明細申報年月不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            else{
                const params = new URLSearchParams();
                params.append('p_s_date', this.p_s_date);
                params.append('p_s_person', this.p_s_person);
                
                // l_status
                this.l_status = '搜尋 ' + this.q_s_name + ' ~ ' + this.q_e_date + ' ERP 進銷明細查詢 資料...';

                alert(p_s_date + '/' + p_s_person);

                // ajax - axios
                axios.post('/load_factory_erp_subform_list', params , {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })
                .then(response => {
                    
                    document.getElementById('p_s_show_content2').innerHTML = response.data;
                    
                    this.goto_top();  
                })
                .catch(error => {
                    if (error.response) {
                        console.error('Server responded with an error:', error.response);
                        this.show_msg = error.response.data;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else if (error.request) {
                        console.error('No response received:', error.request);
                        this.show_msg = 'No response from server.';
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else {
                        console.error('Error:', error.message);
                        this.show_msg = 'An error occurred: ' + error.message;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    }
                })
                .finally(() => {
                    setTimeout(() => {
                        this.l_status = '';
                    } , 1000);
                });
            }
            
        },
        goto_top() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        },
    },
    mounted() {
        // Initialize flatpickr for start date
        flatpickr(this.$refs.q_s_date, {
            dateFormat: "Y-m-d", // Customize as needed
            onChange: (selectedDates, dateStr) => {
                this.q_s_date = dateStr;  // Update the Vue data model
            }
        });

        // Initialize flatpickr for end date
        flatpickr(this.$refs.q_e_date, {
            dateFormat: "Y-m-d",  // Customize as needed
            onChange: (selectedDates, dateStr) => {
                this.q_e_date = dateStr;  // Update the Vue data model
            }
        });
    }
}).mount('#p_s_detail_list');
/************************************************************************************************************************* 
 *
 * 工廠 ERP - 子單身查詢
 * 
 *************************************************************************************************************************/ 
const search_erp_subform = Vue.createApp({
    delimiters: ['[[', ']]'],  // Custom delimiters if needed
    data() {
        return {
            q_s_date: '',  
            q_e_date: '',  
            q_c_name:'',
            q_p_name:'',
            msg: '',
            status: '',
            l_status: '',
            show_msg:'',
            f_erp_realtime_query3:'',
            i_q_c_name:'',
            i_q_p_name:''
        };
    },
    methods: {

        /**************
         * 匯出 Excel
         **************/ 
        e_f_excel(){

            // 起始日期
            if(!this.q_s_date || this.q_s_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> ERP 子單身 - 起始日期不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            // 結束日期
            else if(!this.q_e_date || this.q_e_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> ERP 子單身 - 結束日期不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }else{
                
                const params = new URLSearchParams();
                params.append('q_s_date', this.q_s_date);
                params.append('q_e_date', this.q_e_date);

                // l_status
                this.l_status = '匯出 ' + this.q_s_name + ' ~ ' + this.q_e_date + ' ERP 子單身 Excel 資料...';
                
                // ajax - axioss
                axios.post('/factory_erp_subform_download_excel', params , {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })
                .then(response => {
                    
                    const s_date = this.q_s_date;
                    const e_date = this.q_e_date;

                    const s_d = s_date.replace(/-/g, "");
                    const e_d = e_date.replace(/-/g, "");

                    var url      = "/download_factory_erp_subform_excel?q_s_date=" + s_d + "&q_e_date=" + e_d;
                    var fileName = 'factory_erp_subform_' + s_d + '_' + e_d + '.xlsx';


                    // 创建一个动态链接并触发点击
                    var link = $('<a></a>')
                            .attr('href', url)
                            .attr('download', fileName)
                            .appendTo('body');

                    link[0].click();
                    link.remove(); // 清理动态创建的元素
                    
                    this.goto_top();  // Assuming this is defined
                })
                .catch(error => {
                    if (error.response) {
                        console.error('Server responded with an error:', error.response);
                        this.show_msg = error.response.data;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else if (error.request) {
                        console.error('No response received:', error.request);
                        this.show_msg = 'No response from server.';
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else {
                        console.error('Error:', error.message);
                        this.show_msg = 'An error occurred: ' + error.message;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    }
                })
                .finally(() => {
                    
                    setTimeout(() => {
                        this.l_status = '';
                    } , 1000);
                    
                });
            }
        },
        /**********
         * 搜尋
         **********/ 
        q_s_submit() {
            
            // 起始日期
            if(!this.q_s_date || this.q_s_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> ERP 子單身 - 起始日期不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            // 結束日期
            else if(!this.q_e_date || this.q_e_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> ERP 子單身 - 結束日期不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            else{
                const params = new URLSearchParams();
                params.append('q_s_date', this.q_s_date);
                params.append('q_e_date', this.q_e_date);
                
                // l_status
                this.l_status = '搜尋 ' + this.q_s_name + ' ~ ' + this.q_e_date + ' ERP 子單身查詢 資料...';

                // ajax - axios
                axios.post('/load_factory_erp_subform_list', params , {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })
                .then(response => {
                    
                    document.getElementById('f_erp_realtime_query6').innerHTML = response.data;
                    
                    this.goto_top();  
                })
                .catch(error => {
                    if (error.response) {
                        console.error('Server responded with an error:', error.response);
                        this.show_msg = error.response.data;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else if (error.request) {
                        console.error('No response received:', error.request);
                        this.show_msg = 'No response from server.';
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else {
                        console.error('Error:', error.message);
                        this.show_msg = 'An error occurred: ' + error.message;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    }
                })
                .finally(() => {
                    setTimeout(() => {
                        this.l_status = '';
                    } , 1000);
                });
            }
            
        },
        goto_top() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        },
    },
    mounted() {
        // Initialize flatpickr for start date
        flatpickr(this.$refs.q_s_date, {
            dateFormat: "Y-m-d", // Customize as needed
            onChange: (selectedDates, dateStr) => {
                this.q_s_date = dateStr;  // Update the Vue data model
            }
        });

        // Initialize flatpickr for end date
        flatpickr(this.$refs.q_e_date, {
            dateFormat: "Y-m-d",  // Customize as needed
            onChange: (selectedDates, dateStr) => {
                this.q_e_date = dateStr;  // Update the Vue data model
            }
        });
    }
}).mount('#search_erp_subform');
/************************************************************************************************************************* 
 *
 * 工廠 ERP - BOM 維護 2
 * 
 *************************************************************************************************************************/ 
const search_erp_bom2 = Vue.createApp({
    delimiters: ['[[', ']]'],  // Custom delimiters if needed
    data() {
        return {
            q_s_date: '',  
            q_e_date: '',  
            q_c_name:'',
            q_p_name:'',
            msg: '',
            status: '',
            l_status: '',
            show_msg:'',
            f_erp_realtime_query3:'',
            i_q_c_name:'',
            i_q_p_name:''
        };
    },
    methods: {

        /****************
         * BOM 維護清單
         ****************/ 
        bom_list_q_s_submit(l_q_c_name) {
            
            const params = new URLSearchParams();
            params.append('q_c_name', l_q_c_name);
            
            // l_status
            this.l_status = '搜尋 ' + this.q_c_name + ' ERP BOM 資料...';

            // ajax - axios
            axios.post('/load_factory_erp_bom_list', params , {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            })
            .then(response => {
                
                document.getElementById('f_erp_realtime_query3').innerHTML = response.data;
                
                this.goto_top();  
            })
            .catch(error => {
                if (error.response) {
                    console.error('Server responded with an error:', error.response);
                    this.show_msg = error.response.data;
                    document.getElementById('click_show_msg').click(); 
                    document.getElementById('show_msg').innerHTML = this.show_msg; 
                } else if (error.request) {
                    console.error('No response received:', error.request);
                    this.show_msg = 'No response from server.';
                    document.getElementById('click_show_msg').click(); 
                    document.getElementById('show_msg').innerHTML = this.show_msg; 
                } else {
                    console.error('Error:', error.message);
                    this.show_msg = 'An error occurred: ' + error.message;
                    document.getElementById('click_show_msg').click(); 
                    document.getElementById('show_msg').innerHTML = this.show_msg; 
                }
            })
            .finally(() => {
                setTimeout(() => {
                    this.l_status = '';
                } , 1000);
            });
        },
        goto_top() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        },
    },
    mounted() {
        // Initialize flatpickr for start date
        flatpickr(this.$refs.q_s_date, {
            dateFormat: "Y-m-d", // Customize as needed
            onChange: (selectedDates, dateStr) => {
                this.q_s_date = dateStr;  // Update the Vue data model
            }
        });

        // Initialize flatpickr for end date
        flatpickr(this.$refs.q_e_date, {
            dateFormat: "Y-m-d",  // Customize as needed
            onChange: (selectedDates, dateStr) => {
                this.q_e_date = dateStr;  // Update the Vue data model
            }
        });
    }
}).mount('#search_erp_bom2');

/************************************************************************************************************************* 
 *
 * 工廠 ERP - BOM 維護 1
 * 
 *************************************************************************************************************************/ 
const search_erp_bom = Vue.createApp({
    delimiters: ['[[', ']]'],  // Custom delimiters if needed
    data() {
        return {
            q_s_date: '',  
            q_e_date: '',  
            q_c_name:'',
            q_p_name:'',
            msg: '',
            status: '',
            l_status: '',
            show_msg:'',
            f_erp_realtime_query3:'',
            i_q_c_name:'',
            i_q_p_name:''
        };
    },
    methods: {

        /**************
         * 
         * 選擇 產品品號
         * 
         **************/ 
        select_q_c_name(){
            const data = this.q_c_name.split('_');
            this.i_q_c_name = (data[0]).trim();
        },
        /***************
         * BOM 品號搜尋
         ***************/ 
        async bom_q_s_submit() {
                
            const data = this.q_c_name.split('_');
            this.i_q_c_name = (data[0]).trim();

            // 品號
            if(!this.i_q_c_name || this.i_q_c_name.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> ERP - BOM品號不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }else{
                
                const params = new URLSearchParams();
                params.append('q_c_name', this.i_q_c_name);
                
                // l_status
                this.l_status = '搜尋 ' + this.q_c_name + ' ERP BOM 資料...';

                // ajax - axios
                const response = await axios.post('/load_factory_erp_bom_list', params , {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })
                .then(response => {
                    
                    document.getElementById('f_erp_realtime_query3').innerHTML = response.data;
                    
                    this.goto_top();  
                })
                .catch(error => {
                    if (error.response) {
                        console.error('Server responded with an error:', error.response);
                        this.show_msg = error.response.data;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else if (error.request) {
                        console.error('No response received:', error.request);
                        this.show_msg = 'No response from server.';
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else {
                        console.error('Error:', error.message);
                        this.show_msg = 'An error occurred: ' + error.message;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    }
                })
                .finally(() => {
                    setTimeout(() => {
                        this.l_status = '';
                    } , 1000);
                });
            }
            
        },
        goto_top() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        },
    },
    mounted() {
        // Initialize flatpickr for start date
        flatpickr(this.$refs.q_s_date, {
            dateFormat: "Y-m-d", // Customize as needed
            onChange: (selectedDates, dateStr) => {
                this.q_s_date = dateStr;  // Update the Vue data model
            }
        });

        // Initialize flatpickr for end date
        flatpickr(this.$refs.q_e_date, {
            dateFormat: "Y-m-d",  // Customize as needed
            onChange: (selectedDates, dateStr) => {
                this.q_e_date = dateStr;  // Update the Vue data model
            }
        });
    }
}).mount('#search_erp_bom');


/************************************************************************************************************************* 
 *
 * 電子看板
 * 
 *************************************************************************************************************************/ 
/***********  
 *
 * e_b_form
 * 
 ***********/ 
const e_b_form = Vue.createApp({
    delimiters: ['[[', ']]'],  // Custom delimiters if needed
    data() {
        return {
            e_a_date:'',
            f_a_date:'',
            e_s_date:'',
            e_e_date:'',
            e_c_name:'',
            e_s_title:'',
            e_f_date:'',
            e_f_name:'',
            e_name:'',
            e_other:''
        };
    },
    methods: {
        /**************
         * 
         * 選擇 產品名稱
         * 
         **************/ 
        select_q_p_name(){
            this.i_q_p_name = this.q_p_name;
        },
        /**************
         * 
         * 選擇 客戶名稱
         * 
         **************/ 
        select_q_c_name(){
            this.i_q_c_name = this.q_c_name;
        },
        /**************
         * 
         * goto top
         * 
         **************/ 
        goto_top() {
            // Scroll to the top of the page
            window.scrollTo({ top: 0, behavior: 'smooth' });  // Use smooth scrolling
      
            // If you need to change the style of an element, use refs
            if (this.$refs.gotoTopButton) {
              this.$refs.gotoTopButton.style.cursor = 'pointer';
            }
        },
        /**************
         * 
         * 送出申請單
         * 
         **************/ 
        e_b_submit(){

            // 申請日期
            if(!this.e_a_date || this.e_a_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> 電子看板 - 申請日期不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            // 播放開始
            else if(!this.e_s_date || this.e_s_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> 電子看板 - 播放開始時間不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            // 播放結束
            else if(!this.e_e_date || this.e_e_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> 電子看板 - 播放結束時間不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            // 貴賓公司
            else if(!this.e_c_name || this.e_c_name.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> 電子看板 - 貴賓公司不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            // 貴賓職稱
            else if(!this.e_title || this.e_title.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> 電子看板 - 貴賓職稱不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            // 貴賓姓名
            else if(!this.e_name || this.e_name.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> 電子看板 - 貴賓姓名不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            // 其它說明 
            else if(!this.e_other || this.e_other.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> 電子看板 - 其它說明不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            else{
                
                const params = new URLSearchParams();
                params.append('e_a_date', this.e_a_date);
                params.append('e_s_date', this.e_s_date);
                params.append('e_e_date', this.e_e_date);
                params.append('e_c_name', this.e_c_name);
                params.append('e_title', this.e_title);
                params.append('e_name', this.e_name);
                params.append('e_other', this.e_other);

                // l_status
                this.l_status = "載入電子看板申請單 ...";
                
                // ajax - axioss
                axios.post('/submit_e_board', params , {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })
                .then(response => {

                    document.getElementById('e_board_list').innerHTML = response.data;
                    
                    this.goto_top();  // Assuming this is defined
                })
                .catch(error => {
                    if (error.response) {
                        console.error('Server responded with an error:', error.response);
                        this.show_msg = error.response.data;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else if (error.request) {
                        console.error('No response received:', error.request);
                        this.show_msg = 'No response from server.';
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else {
                        console.error('Error:', error.message);
                        this.show_msg = 'An error occurred: ' + error.message;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    }
                })
                .finally(() => {
                    
                    setTimeout(() => {
                        this.l_status = '';
                    } , 1000);
                    
                });
            }
        }
    },
    mounted() {
        // Initialize flatpickr for start date
        flatpickr(this.$refs.e_a_date, {
            dateFormat: "Y-m-d", // Customize as needed
            onChange: (selectedDates, dateStr) => {
                this.q_s_date = dateStr;  // Update the Vue data model
            }
        });
        flatpickr(this.$refs.f_a_date, {
            dateFormat: "Y-m-d", // Customize as needed
            onChange: (selectedDates, dateStr) => {
                this.f_a_date = dateStr;  // Update the Vue data model
            }
        });
        flatpickr(this.$refs.e_s_date, {
            enableTime: true,           // Enable time selection
            noCalendar: true,           // Disable calendar view, only time picker
            dateFormat: "H:i",          // Set time format to "HH:MM"
            time_24hr: true,            // Use 24-hour format (optional)
            onChange: (selectedDates, dateStr) => {
                this.q_e_date = dateStr;  // Update the Vue data model
            }
        });
        flatpickr(this.$refs.e_e_date, {
            enableTime: true,           // Enable time selection
            noCalendar: true,           // Disable calendar view, only time picker
            dateFormat: "H:i",          // Set time format to "HH:MM"
            time_24hr: true,            // Use 24-hour format (optional)
            onChange: (selectedDates, dateStr) => {
                this.q_e_date = dateStr;  // Update the Vue data model
            }
        });
    }
}).mount('#e_b_form');

/***********  
 *
 * e_f_form
 * 
 ***********/ 
const e_f_form = Vue.createApp({
    delimiters: ['[[', ']]'],  // Custom delimiters if needed
    data() {
        return {
            e_a_date:'',
            f_a_date:'',
            e_s_date:'',
            e_e_date:'',
            e_c_name:'',
            e_s_title:'',
            e_f_date:'',
            e_f_name:'',
            e_name:'',
            e_other:''
        };
    },
    methods: {
        /**************
         * 
         * 送出回覆
         * 
         **************/ 
        e_f_submit_res(a_date , s_time , e_time){

            const params = new URLSearchParams();
                params.append('a_date', this.a_date);
                params.append('s_time', this.s_time);
                params.append('e_time', this.e_time);

                // l_status
                this.l_status = "回覆電子看板申請單 ...";
                
                // ajax - axioss
                axios.post('/submit_response_e_board', params , {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })
                .then(response => {

                    document.getElementById('e_board_list').innerHTML = response.data;
                    
                    this.goto_top();  // Assuming this is defined
                })
                .catch(error => {
                    if (error.response) {
                        console.error('Server responded with an error:', error.response);
                        this.show_msg = error.response.data;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else if (error.request) {
                        console.error('No response received:', error.request);
                        this.show_msg = 'No response from server.';
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else {
                        console.error('Error:', error.message);
                        this.show_msg = 'An error occurred: ' + error.message;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    }
                })
                .finally(() => {
                    
                    setTimeout(() => {
                        this.l_status = '';
                    } , 1000);
                    
                });


        }
        
    },
    mounted() {
        // Initialize flatpickr for start date
        flatpickr(this.$refs.e_f_date, {
            dateFormat: "Y-m-d", // Customize as needed
            onChange: (selectedDates, dateStr) => {
                this.e_f_date = dateStr;  // Update the Vue data model
            }
        });
        flatpickr(this.$refs.f_a_date, {
            dateFormat: "Y-m-d", // Customize as needed
            onChange: (selectedDates, dateStr) => {
                this.f_a_date = dateStr;  // Update the Vue data model
            }
        });
    }
}).mount('#e_f_form');


/************************************************************************************************************************* 
 *
 * 工廠 ERP - 銷售實績 
 * 
 *************************************************************************************************************************/ 
    const search_ss2 = Vue.createApp({
    delimiters: ['[[', ']]'],  // Custom delimiters if needed
    data() {
        return {
            q_s_date: '',  
            q_e_date: '',  
            q_c_name:'',
            q_p_name:'',
            msg: '',
            status: '',
            l_status: '',
            show_msg:'',
            f_erp_realtime_query3:'',
            i_q_c_name:'',
            i_q_p_name:''
        };
    },
    methods: {
        /**************
         * 
         * 選擇 產品名稱
         * 
         **************/ 
        select_q_p_name(){
            this.i_q_p_name = this.q_p_name;
        },
        /**************
         * 
         * 選擇 客戶名稱
         * 
         **************/ 
        select_q_c_name(){
            this.i_q_c_name = this.q_c_name;
        },

        /**************
         * 
         * 匯出 json
         * 
         **************/ 
        e_f_json(){

            // 起始日期
            if(!this.q_s_date || this.q_s_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> 銷售實績 - 起始日期不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            // 結束日期
            else if(!this.q_e_date || this.q_e_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> 銷售實績 - 結束日期不能為空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }else{
                
                const params = new URLSearchParams();
                params.append('q_s_date', this.q_s_date);
                params.append('q_e_date', this.q_e_date);
                params.append('q_c_name', this.i_q_c_name);
                params.append('q_p_name', this.i_q_p_name);

                // l_status
                this.l_status = "匯出 " + this.q_s_date + " ~ " + this.q_e_date  + " json ...";
                
                // ajax - axioss
                axios.post('/factory_erp_ss2_download_json', params , {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })
                .then(response => {

                    var url      = "/download_factory_erp_ss2_json?q_s_date="+this.q_s_date+'&q_e_date='+this.q_e_date;
                    var fileName = 'factory_erp_ss2_' + this.q_s_date + '_' + this.q_e_date + '.json';


                    // 创建一个动态链接并触发点击
                    var link = $('<a></a>')
                            .attr('href', url)
                            .attr('download', fileName)
                            .appendTo('body');

                    link[0].click();
                    link.remove(); // 清理动态创建的元素

                    
                    this.goto_top();  // Assuming this is defined
                })
                .catch(error => {
                    if (error.response) {
                        console.error('Server responded with an error:', error.response);
                        this.show_msg = error.response.data;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else if (error.request) {
                        console.error('No response received:', error.request);
                        this.show_msg = 'No response from server.';
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else {
                        console.error('Error:', error.message);
                        this.show_msg = 'An error occurred: ' + error.message;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    }
                })
                .finally(() => {
                    
                    setTimeout(() => {
                        this.l_status = '';
                    } , 1000);
                    
                });
            }
        },

        /**************
         * 
         * 匯出 Excel
         * 
         **************/ 
        e_f_excel(){

            // 起始日期
            if(!this.q_s_date || this.q_s_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> 銷售實績 - 起始日期不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            // 結束日期
            else if(!this.q_e_date || this.q_e_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> 銷售實績 - 結束日期不能為空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }else{
                
                const params = new URLSearchParams();
                params.append('q_s_date', this.q_s_date);
                params.append('q_e_date', this.q_e_date);
                params.append('q_c_name', this.i_q_c_name);
                params.append('q_p_name', this.i_q_p_name);

                // l_status
                this.l_status = "匯出 " + this.q_s_date + " ~ " + this.q_e_date  + " excel ...";
                
                // ajax - axioss
                axios.post('/factory_erp_ss2_download_excel', params , {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })
                .then(response => {
                    
                    var url      = "/download_factory_erp_ss2_excel?q_s_date="+this.q_s_date+'&q_e_date='+this.q_e_date;
                    var fileName = 'factory_erp_ss2_' + this.q_s_date + '_' + this.q_e_date + '.xlsx';


                    // 创建一个动态链接并触发点击
                    var link = $('<a></a>')
                            .attr('href', url)
                            .attr('download', fileName)
                            .appendTo('body');

                    link[0].click();
                    link.remove(); // 清理动态创建的元素
                    
                    this.goto_top();  // Assuming this is defined
                })
                .catch(error => {
                    if (error.response) {
                        console.error('Server responded with an error:', error.response);
                        this.show_msg = error.response.data;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else if (error.request) {
                        console.error('No response received:', error.request);
                        this.show_msg = 'No response from server.';
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else {
                        console.error('Error:', error.message);
                        this.show_msg = 'An error occurred: ' + error.message;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    }
                })
                .finally(() => {
                    
                    setTimeout(() => {
                        this.l_status = '';
                    } , 1000);
                    
                });
            }
        },
        
        /**********
         * 
         * 搜尋
         * 
         **********/ 
        q_s_submit() {
            
            // 起始日期
            if(!this.q_s_date || this.q_s_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> 銷售實績 - 起始日期不能空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }
            // 結束日期
            else if(!this.q_e_date || this.q_e_date.trim() === '') {
                
                this.show_msg = "<i class='bi bi-x-circle text-danger'></i> 銷售實績 - 結束日期不能為空白！";  
                document.getElementById('click_show_msg').click(); 
                document.getElementById('show_msg').innerHTML = this.show_msg; 
                return;  

            }else{
                
                const params = new URLSearchParams();
                params.append('q_s_date', this.q_s_date);
                params.append('q_e_date', this.q_e_date);
                params.append('q_c_name', this.i_q_c_name);
                params.append('q_p_name', this.i_q_p_name);
                
                // l_status
                this.l_status = '搜尋 ' + this.q_s_date + ' ~ ' + this.q_e_date + ' ' + this.q_c_name + ' ' + this.q_p_name + ' 資料...';

                // ajax - axios
                axios.post('/load_factory_erp_ss2_list', params , {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })
                .then(response => {
                    
                    document.getElementById('f_erp_realtime_query3').innerHTML = response.data;
                    
                    this.goto_top();  
                })
                .catch(error => {
                    if (error.response) {
                        console.error('Server responded with an error:', error.response);
                        this.show_msg = error.response.data;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else if (error.request) {
                        console.error('No response received:', error.request);
                        this.show_msg = 'No response from server.';
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    } else {
                        console.error('Error:', error.message);
                        this.show_msg = 'An error occurred: ' + error.message;
                        document.getElementById('click_show_msg').click(); 
                        document.getElementById('show_msg').innerHTML = this.show_msg; 
                    }
                })
                .finally(() => {
                    setTimeout(() => {
                        this.l_status = '';
                    } , 1000);
                });
            }
            
        },
        goto_top() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        },
    },
    mounted() {
        // Initialize flatpickr for start date
        flatpickr(this.$refs.q_s_date, {
            dateFormat: "Y-m-d", // Customize as needed
            onChange: (selectedDates, dateStr) => {
                this.q_s_date = dateStr;  // Update the Vue data model
            }
        });

        // Initialize flatpickr for end date
        flatpickr(this.$refs.q_e_date, {
            dateFormat: "Y-m-d",  // Customize as needed
            onChange: (selectedDates, dateStr) => {
                this.q_e_date = dateStr;  // Update the Vue data model
            }
        });
    }
}).mount('#search_ss2');

/************************************************************************************************************************* 
 *
 * 最新公告
 * 
 *************************************************************************************************************************/ 
const latest_announcement = Vue.createApp({
    delimiters:['[[' , ']]'],
    data(){
        return{
            msg:{
                show:'load_data',
                status:''
            }
        }
    },
    methods:{
        load_news(){
            axios.post('/ajax/load_latest_announcement.html' , this.msg , {
                Headers:{
                    'ContentType':'application/json'
                }
            }).then(Response=>{
                
                this.status = {
                    msg:'load ajax success.'
                }

                setTimeout(() => {
                    this.status = '';
                }, 2000);

            }).catch(error=>{
                this.status = {
                    msg:'<Error> load ajax failed.'
                }

                setTimeout(() => {
                    this.status = '';
                } , 2000);
            });
        }
    }
}).mount('#latest_announcement');



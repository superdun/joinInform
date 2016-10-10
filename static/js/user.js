$(window).load(function()
{   
    // 对Date的扩展，将 Date 转化为指定格式的String   
    // 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，   
    // 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)   
    // 例子：   
    // (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423   
    // (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18   
    Date.prototype.Format = function(fmt)   
    {    
      var o = {   
        "M+" : this.getMonth()+1,                 //月份   
        "d+" : this.getDate(),                    //日   
        "h+" : this.getHours(),                   //小时   
        "m+" : this.getMinutes(),                 //分   
        "s+" : this.getSeconds(),                 //秒   
        "q+" : Math.floor((this.getMonth()+3)/3), //季度   
        "S"  : this.getMilliseconds()             //毫秒   
      };   
      if(/(y+)/.test(fmt))   
        fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));   
      for(var k in o)   
        if(new RegExp("("+ k +")").test(fmt))   
      fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));   
      return fmt;   
    }  

    var today = new Date();

    var y = today.getFullYear();
    var dates = '';
    var id=0;
    if($('#dates_tmp').val()){
            //array ["12/16/2016"]
        dates = $('#dates_tmp').val().split(',');
    };

    if ($('#records_tmp').val()){
            //json，{"12/16/2016":{"students":[1],"comment":"江苏苏州"}}
        var records = JSON.parse($('#records_tmp').val());
    };

    if ($('#id_tmp').val()){
        id = $('#id_tmp').val()
    };

    $('#dates').multiDatesPicker({
        addDates: dates,
        numberOfMonths: [3,4],
        defaultDate: '1/1/'+y
    }) ; 

    if ($('#checkdates')){
        var  specialDates = [];
        var  recordedDates = [];

         for (var i=0;i<dates.length;i++){
            dates[i]=$.trim(dates[i])
            var year = dates[i].split('/')[2];
            var month = dates[i].split('/')[0]-1;
            var day = dates[i].split('/')[1];
            if (dates[i] in records){
                //标记有课并登记的日期，与上面分开有益于拓展
                var recordedDate = {
                    date: new Date(year,month,day),
                    data: {
                        select_date :dates[i],
                        comment:records[dates[i]]['comment'],
                        students:records[dates[i]]['students']
                    },
                    repeatMonth: false                  
                }
                recordedDates.push(recordedDate)
            }
            else{
                //标记有课的日期
                var specialDate = {
                    date: new Date(year,month,day),
                    data: { message: '这堂课还没有登记' },
                    repeatMonth: false    
                }

                specialDates.push(specialDate)
            }

  
            console.log (specialDates)
         }
            
        
        $('#checkdates').glDatePicker({
            specialDates:specialDates,
            recordedDates:recordedDates,
            onClick: function(target, cell, date, data) {
                target.val(date.getFullYear() + ' - ' +
                date.getMonth() + ' - ' +
                date.getDate());
                if(data != null && ('message' in data)) {
                     alert(data.message + '\n' + date);
                }
                else{
                    if (data != null){
                        var url = '/admin/courses/api/detail/'+id;
                        $.ajax({
                            url:url,
                            type:'GET',
                            dataType:'json',
                            // async:false
                            success:function(response){
                                if (response.status ==='OK'){
                                    var inform = response.data
                                    var attend_list = inform.records[date.Format("MM/dd/yyyy")].students
                                    var attend_num = attend_list.length
                                    var total_list = inform.students
                                    var total_num = total_list.length

                                    $("#modal-title").text(data.select_date+'   '+inform.name+' 班登记详情')
                                    $('#check_process').attr('aria-valuenow',attend_num*100/total_num)
                                    .css('width',attend_num*100/total_num+'%')
                                    .text(attend_num+'人/'+total_num+'人')
                                    $.each(total_list,function(l){
                                        //出席
                                        if ($.inArray(this.id.toString(),l)>=0){
                                            $('#check_list').append("<a href ='/admin/students/detail/"+this.id+"' class='list-group-item list-group-item-success'>"+this.name +'</a>')
                                        }
                                        //未出席
                                        else{
                                            $('#check_list').append("<a href ='{{url_for('students.details_view', id='"+this.id+"' class='list-group-item list-group-item-danger'>"+this.name +'</a>')

                                        }
                                    },[attend_list])
                                    $('#comment').val(inform.records[date.Format("MM/dd/yyyy")].comment).attr('disabled','disabled');

                                }
                                else {
                                    alert ('')
                                }
                            }
                        });

                        $('#myModal').modal()
                        $('#myModal').on('hidden.bs.modal', function (e) {
                            $('#check_list').html('')
                        })

                    }
                    
                }
            }

        });
    };

    //check in
    if ($('#checkin_dates')){
        var  specialDates = [];
        var  recordedDates = [];

         for (var i=0;i<dates.length;i++){
            dates[i]=$.trim(dates[i])
            var year = dates[i].split('/')[2];
            var month = dates[i].split('/')[0]-1;
            var day = dates[i].split('/')[1];
            if (dates[i] in records){
                //标记有课并登记的日期，与上面分开有益于拓展
                var recordedDate = {
                    date: new Date(year,month,day),
                    data: {
                        select_date :dates[i],
                        comment:records[dates[i]]['comment'],
                        students:records[dates[i]]['students']
                    },
                    repeatMonth: false                  
                }
                recordedDates.push(recordedDate)
            }
            else{
                //标记有课的日期
                var specialDate = {
                    date: new Date(year,month,day),
                    data: { message: '这堂课还没有登记' },
                    repeatMonth: false    
                }

                specialDates.push(specialDate)
            }

  
            console.log (specialDates)
         }
            
        
        $('#checkin_dates').glDatePicker({
            specialDates:specialDates,
            recordedDates:recordedDates,
            onClick: function(target, cell, date, data) {
                target.val(date.getFullYear() + ' - ' +
                date.getMonth() + ' - ' +
                date.getDate());
                if(data != null && ('message' in data)) {
                    alert(data.message + '\n' + date);
                        var url = '/admin/courses/api/detail/'+id;
                        $.ajax({
                            url:url,
                            type:'GET',
                            dataType:'json',
                            // async:false
                            success:function(response){
                                if (response.status ==='OK'){
                                    var inform = response.data
                                    var attend_list = []
                                    var attend_num = 0
                                    var total_list = inform.students
                                    var total_num = total_list.length
                                    $.each(total_list,function(){
                                        $('#check_list').append("<li class='list-group-item list-group-item-danger student-status' status='not-checkin' student_id='"+this.id+"'>"+this.name +'</a>')                             
                                    })
                                    $('.student-status').click(function(e){
                                        if ($(this).attr('status')=='not-checkin'){
                                           $(this).attr({'class':'list-group-item list-group-item-success student-status','status':'checkin'})
                                            attend_num ++;
                                            attend_list.push($(this).attr('student_id')); 
                                        }
                                        else{
                                           $(this).attr({'class':'list-group-item list-group-item-danger student-status','status':'not-checkin'})
                                            attend_num --;
                                            attend_list.splice($.inArray($(this).attr('student_id'),attend_list),1);                                             
                                        }
                                        
                                        $('#check_process').attr('aria-valuenow',attend_num*100/total_num)
                                        .css('width',attend_num*100/total_num+'%')
                                        .text(attend_num+'人/'+total_num+'人')

                                    })

                                    $("#modal-title").text(data.select_date+'   '+inform.name+' 班登记表')
                                    $('#check_process').attr('aria-valuenow',attend_num*100/total_num)
                                    .css('width',attend_num*100/total_num+'%')
                                    .text(attend_num+'人/'+total_num+'人')

                                    $('#submit').css('display','inline')
                                    $('#submit').click(function(e){
                                        url = '/admin/courses/api/checkin/'+id;
                                        var comment = $('#comment').val()
                                        $.ajax({
                                            url:url,
                                            type:'POST',
                                            dataType:'json',
                                            traditional:true,
                                            data:{'date':date.Format("MM/dd/yyyy"),'attend_list':attend_list,'total_list':total_list,'comment':comment},
                                            success:function(response){
                                                if(response.status=='OK'){
                                                    $('#submit').css('display','none')
                                                    $('#check_list').html('<h2>success</h2>')
                                                    alert('success!')
                                                     location.reload() ;
                                                }
                                                else{
                                                    alert('checking-in failed')
                                                }
                                            }
                                        })
                                    })                                    
                                    
                                }
                                else {
                                    alert ('')
                                }
                            }
                        });
                    $('#myModal').modal()
                    $('#myModal').on('hidden.bs.modal', function (e) {
                        $('#check_list').html('')
                        $('#submit').css('display','none')
                    })
                }
                else{
                    if (data != null){
                        var url = '/admin/courses/api/detail/'+id;
                        $.ajax({
                            url:url,
                            type:'GET',
                            dataType:'json',
                            // async:false
                            success:function(response){
                                if (response.status ==='OK'){
                                    var inform = response.data
                                    var attend_list = inform.records[date.Format("MM/dd/yyyy")].students
                                    var attend_num = attend_list.length
                                    var total_list = inform.students
                                    var total_num = total_list.length

                                    $("#modal-title").text(data.select_date+'   '+inform.name+' 班登记详情')
                                    $('#comment').val(inform.records[date.Format("MM/dd/yyyy")].comment).attr('disabled','disabled');
    
                                    $('#check_process').attr('aria-valuenow',attend_num*100/total_num)
                                    .css('width',attend_num*100/total_num+'%')
                                    .text(attend_num+'人/'+total_num+'人')
                                    $.each(total_list,function(l){
                                        //出席

                                        if ($.inArray(this.id.toString(),l)>=0){
                                            $('#check_list').append("<a href ='/admin/students/detail/"+this.id+"' class='list-group-item list-group-item-success'>"+this.name +'</a>')
                                        }
                                        //未出席
                                        else{
                                            $('#check_list').append("<a href ='{{url_for('students.details_view', id='"+this.id+"' class='list-group-item list-group-item-danger'>"+this.name +'</a>')

                                        }
                                    },[attend_list])
                                    

                                }
                                else {
                                    alert ('')
                                }
                            }
                        });

                        $('#myModal').modal()
                        $('#myModal').on('hidden.bs.modal', function (e) {
                            $('#check_list').html('')

                        })

                    }
                    
                }
            }

        });
    };


    
});
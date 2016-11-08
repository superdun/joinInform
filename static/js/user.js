
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

    var toTimeStamp = function(dateStr){
        var date = new Date(dateStr);
        return date.getTime()/1000;
    }
    var recordsByDate=function(records){
        var recordsBydate={}
        $.each(records,function(key,val){
            recordsBydate[val['date']]=val
        })
        return recordsBydate
    }
    var assistantAndSub = function(record,teachers){

        if (record){
            $('#subteacher').html('')
            $("#issub").bootstrapSwitch('state',Boolean(record.substitute)).bootstrapSwitch('disabled',true);
            $('#subteacher').attr('disabled','disabled')
            if (Boolean(record.substitute)){
                $('#subteacher').append('<option value = '+record.substitute_id+'>'+teachers[record.substitute_id].name+'</option>');
            }
            else{
                $('#subteacher').append('<option>无</option>');
            }
            $("#isas").bootstrapSwitch('state',Boolean(record.assistant)).bootstrapSwitch('disabled',true);
            $('#asteacher').attr('disabled','disabled')
            if (Boolean(record.assistant)){
                $('#asteacher').append('<option value = '+record.assistant_id+'>'+teachers[record.assistant_id].name+'</option>');
            }
            else{
                $('#asteacher').append('<option>无</option>');
            }

        }
        else{
            $("#issub").bootstrapSwitch('state',false).bootstrapSwitch('disabled',false);
            $("#isas").bootstrapSwitch('state',false).bootstrapSwitch('disabled',false);

            $("#issub").on('switchChange.bootstrapSwitch',function(event, state) {
                $('#subteacher').html('')
                if (!state){
                    $('#subteacher').append('<option>无</option>');
                    $('#subteacher').attr('disabled','disabled');
                }
                else{
                    $('#subteacher').removeAttr('disabled');
                    $.each(teachers,function(k,v){
                        $('#subteacher').append('<option value = '+k+'>'+v.name+'</option>');
                    })
                }
            })
            $("#isas").on('switchChange.bootstrapSwitch',function(event, state) {
                $('#asteacher').html('')
                if (!state){
                    $('#asteacher').append('<option>无</option>');
                    $('#asteacher').attr('disabled','disabled');
                }
                else{
                    $('#asteacher').removeAttr('disabled');
                    $.each(teachers,function(k,v){
                        $('#asteacher').append('<option value = '+k+'>'+v.name+'</option>');
                    })
                }
            })
            // $("#issub").bootstrapSwitch('state',Boolean(record.substitute));
            // if (Boolean(record.substitute)){
            //     $('#subteacher').append('<option value = '+record.substitute_id+'>'+teachers[record.substitute_id].name+'</option>');
            // }
            // $("#isas").bootstrapSwitch('state',Boolean(record.assistant)).bootstrapSwitch('disabled','true');
            // $('#asteacher').attr('disabled','disabled')
            // if (Boolean(record.assistant)){
            //     $('#asteacher').append('<option value = '+record.assistant_id+'>'+teachers[record.assistant_id].name+'</option>');
            // }
            // else{
            //     $('#asteacher').append('<option>无</option>');
            // }
        }

    }
var today = new Date();
var y = today.getFullYear();
if($('#dates').val() !=null){
     $('#dates').multiDatesPicker({
         addDates: $('#dates').val().split(', '),
         numberOfMonths: [3,4],
         defaultDate: '1/1/'+y
     }) ;
}


    var getSum = function(record){
        var sum = 0 
        for (var i = 0 ;i<record.count;i++){
            sum+=record.pay[i]*record.time[i]
        }
        return sum
    }

    var payDetailTable = function(record,tableId){ 

        for (var i =0;i<record.count;i++){ 
            $(tableId).append(
                "<tr class='tmp'><td>"+record.date[i]
                +'</td><td>'+record.course[i].name
                +'</td><td>'+record.pay[i]*record.time[i] 
                +'  元</td></tr>'
            )
            
        }
    }


 

    

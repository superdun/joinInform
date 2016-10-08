$(window).load(function()
{   


    var today = new Date();

    var y = today.getFullYear();
    var dates = ''
    if($('#dates_tmp').val()){
            //array ["12/16/2016"]
        dates = $('#dates_tmp').val().split(',');
    }
    if ($('#records_tmp').val()){
            //json，{"12/16/2016":{"students":[1],"comment":"江苏苏州"}}
    var records = JSON.parse($('#records_tmp').val());
    }

    $('#dates').multiDatesPicker({
        addDates: dates,
        numberOfMonths: [3,4],
        defaultDate: '1/1/'+y
    })  
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
                    $("#modal-title").text(data.select_date+'登记记录')
                    if (data != null){$('#myModal').modal()}
                    
                }
            }
        });
    }
    
});
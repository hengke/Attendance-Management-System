var date = new Date();
$('.form_datetime').datetimepicker({
    language:  'zh-CN',
    format: 'yyyy-m-d h:i',
    weekStart: 1,
    todayBtn:  1,
    autoclose: 1,
    todayHighlight: 1,
    startView: 2,
    forceParse: 0,
    showMeridian: 1,
    daysOfWeekDisabled: [0,6]
});
$('.form_start_date').datetimepicker({
    language:  'zh-CN',
    format: 'yyyy-m-d',
    weekStart: 1,
    todayBtn:  1,
    autoclose: 1,
    todayHighlight: 1,
    startView: 2,
    minView: 2,
    forceParse: 0,
    daysOfWeekDisabled: [0,6],
    startDate: date,
    keyboardNavigation: 1
})
.on('hide', function(ev){
    // var a = ev.date.getFullYear() + "-" + (ev.date.getMonth() + 1) + "-" + ev.date.getDate(); // + " " + ev.date.getHours() + ":" + ev.date.getMinutes() + ":" + ev.date.getSeconds();
    $('.form_end_date').datetimepicker('setStartDate', $('.form_start_date').find("input").val());
    $('.form_start_time').datetimepicker('setStartDate', $('.form_start_date').find("input").val());
});
$('.form_end_date').datetimepicker({
    language:  'zh-CN',
    format: 'yyyy-m-d',
    weekStart: 1,
    todayBtn:  1,
    autoclose: 1,
    todayHighlight: 1,
    startView: 2,
    minView: 2,
    forceParse: 0,
    daysOfWeekDisabled: [0,6],
    startDate: date,
    keyboardNavigation: 1
 })
.on('hide', function(ev){
    // alert(ev.date);
    $('.form_start_date').datetimepicker('setEndDate', $('.form_end_date').find("input").val());
    $('.form_end_time').datetimepicker('setStartDate', $('.form_end_date').find("input").val());
});
$('.form_start_time').datetimepicker({
    language:  'zh-CN',
    format: 'hh:ii',
    weekStart: 1,
    todayBtn:  1,
    autoclose: 1,
    todayHighlight: 1,
    startView: 1,
    minView: 0,
    maxView: 1,
    forceParse: 0,
    startDate: date,
    minuteStep: 10
})
.on('hide', function(ev){
    // alert(ev.date);
    // alert($('.form_start_time').find("input").val());
    $('.form_end_time').datetimepicker('setStartDate', $('.form_start_time').find("input").val());
});
$('.form_end_time').datetimepicker({
    language:  'zh-CN',
    format: 'hh:ii',
    weekStart: 1,
    todayBtn:  1,
    autoclose: 1,
    todayHighlight: 1,
    startView: 1,
    minView: 0,
    maxView: 1,
    forceParse: 0,
    startDate: date,
    minuteStep: 10
})
.on('hide', function(ev){
    // alert(ev.date);
    $('.form_start_time').datetimepicker('setEndDate', $('.form_end_time').find("input").val());
});

function checkField(val) {
    if(val === '事假' | val === '病假'){
        document.getElementById('div_start_time').style.display = '';
        document.getElementById('div_end_time').style.display = '';
   }else {
        document.getElementById('div_start_time').style.display = 'none';
        document.getElementById('div_end_time').style.display = 'none';
   }
}
var test_dat;

function create_html_for_std_table(std_info){
    var html = ''; 
    $('#std_len').text(std_info.length);
    for(var i=0; i<std_info.length; i+=4){
        html+='<tr>';
        
        html += '<td std_id='+std_info[i].id+'>';
        html += '<input type="checkbox" /> ';
        html += std_info[i].name+'</td>';
        
        if(i+1 < std_info.length){
            html += '<td std_id='+std_info[i+1].id+'>';
            html += '<input type="checkbox" /> ';
            html += std_info[i+1].name+'</td>';
        } else {
            html += '<td></td>';
        }
        
        if(i+2 < std_info.length){
            html += '<td std_id='+std_info[i+2].id+'>';
            html += '<input type="checkbox" /> ';
            html += std_info[i+2].name+'</td>';
        } else {
            html += '<td></td>';
        }
        
        if(i+3 < std_info.length){
            html += '<td std_id='+std_info[i+3].id+'>';
            html += '<input type="checkbox" /> ';
            html += std_info[i+3].name+'</td>';
        } else {
            html += '<td></td>';
        }
        html+='</tr>';
    }
    return html;
}
function ready_fun(){
    {% autoescape off %}
    var first_clas_stds = JSON.parse('{{first_clas_stds}}');
    {% endautoescape %}
    //test_dat = first_clas_stds;
    $('#sel_std_input_table>tbody').html(create_html_for_std_table(first_clas_stds));
    
    var time_str = $('#assess_start_time_input .input_time').val();
    var time_list = time_str.split(' ');
    if(time_list[1] == 'AM') $('#assess_start_time_input .input_time').val("오전 "+ time_list[0]);
    else $('#assess_start_time_input .input_time').val("오후 "+ time_list[0]);
    
    var time_str = $('#assess_end_time_input .input_time').val();
    var time_list = time_str.split(' ');
    if(time_list[1] == 'AM') $('#assess_end_time_input .input_time').val("오전 "+ time_list[0]);
    else $('#assess_end_time_input .input_time').val("오후 "+ time_list[0]);
    
}
$(document).ready(ready_fun);


function chagnge_assess_set_input_select(){
    //test_dat = this;
    var clas_id = $(this).find('option:selected').attr('grp_id');
    
    $.ajax({
        url:'/tch/create_assesstemp_wiz2',
        dataType:'json',
        data:{
            'method':'get_std_info',
            'clas_id':clas_id,
            //'itemid_str' : $(data).find('Item').text()
        }
    }).done(function(msg){
        //console.log(msg);
        //test_dat = msg;
        if(msg['status'] == 'success'){
            $('#sel_std_input_table>tbody').html(create_html_for_std_table(msg['clas_stds']));
        }
    });
            
}
$(document).on('change', '#assess_set_input>select',chagnge_assess_set_input_select);

$(document).on('click', '#sel_all_std', function(){
    $('#sel_std_input_table>tbody input').prop('checked', true);
});

$(document).on('click', '#sel_cancel', function(){
    $('#sel_std_input_table>tbody input').prop('checked', false);
});

function click_submit(){
    var start_date = $('#assess_start_time_input .input_date').val();
    var start_list = start_date.split('-');
    var start = start_date + ' ';
    if(start_list.length != 3 || 
           Number(start_list[0]) < 1000 ||
           Number(start_list[0]) > 4000 ||
           Number(start_list[1]) > 12 ||
           Number(start_list[2]) > 32){
        $('#assess_start_time_input .input_date').css('border', '1px solid red');
        return false;
    }
    var start_time = $('#assess_start_time_input .input_time').val();
    start_list = start_time.split(/:| /);
    if(start_list.length != 3 || 
           Number(start_list[1]) > 12 ||
           Number(start_list[2]) > 59 ){
        $('#assess_start_time_input .input_time').css('border', '1px solid red');
        return false;
    }
    switch(start_list[0]){
        case '오전':
            start += start_list[1] + ':' + start_list[2];
            break;
        case '오후':
            if(Number(start_list[1]) < 12){
                start += (Number(start_list[1])+12) + ':' + start_list[2];
            } else {
                start += start_list[1] + ':' + start_list[2];
            }
            break;
        default:
            $('#assess_start_time_input .input_time').css('border', '1px solid red');
            return false;
    }
    
    var end_date = $('#assess_end_time_input .input_date').val();
    var end_list = end_date.split('-');
    var end = end_date + ' ';
    if(end_list.length != 3 || 
           Number(end_list[0]) < 1000 ||
           Number(end_list[0]) > 4000 ||
           Number(end_list[1]) > 12 ||
           Number(end_list[2]) > 32){
        $('#assess_end_time_input .input_date').css('border', '1px solid red');
        return false;
    }
    var end_time = $('#assess_end_time_input .input_time').val();
    end_list = end_time.split(/:| /);
    
    if(end_list.length != 3 || 
           Number(end_list[1]) > 12 ||
           Number(end_list[2]) > 59 ){
        $('#assess_end_time_input .input_time').css('border', '1px solid red');
        return false;
    }
    switch(end_list[0]){
        case '오전':
            end_time = end_list[1] + ':' + end_list[2];
            end += end_time;
            break;
        case '오후':
            if(Number(end_list[1]) < 12){
                end_time = (Number(end_list[1])+12) + ':' + end_list[2];
            } else {
                end_time = end_list[1] + ':' + end_list[2];
            }
            end += end_time;
            break;
        default:
            $('#assess_end_time_input .input_time').css('border', '1px solid red');
            return false;
    }
    
    //$('#assess_start_time_input .input_date').css('border', '1px solid red')
    var assess_type = $(':radio[name=assess_type]:checked').val();
    var at_id = $('#assess_name_input select option:selected').attr('at_id');
    var group_unit = $(':radio[name="sel_set_mode"]:checked').val();
    var ids = [];
    switch(group_unit){
        case 'A':
            break;
        case 'C':
            ids.push($('#assess_set_input option:selected').attr('grp_id'));
            break;
        case 'S':
            var sel_std = $('#sel_std_input_table :checkbox:checked');
            for(var i=0; i<sel_std.length; i++){
                ids.push($(sel_std[i]).parent().attr('std_id'));
            }
            break;
    }
   
   $.ajax({
        url:'/tch/create_assesstemp_wiz2',
        dataType:'json',
        data:{
            'method':'get_ctid_and_set_assessment',
            'at_id':at_id,
            'group_unit':group_unit,
            'assess_type':assess_type,
            'ids':JSON.stringify(ids),
            'start':start,
            'end':end,
            //'itemid_str' : $(data).find('Item').text()
        }
    }).done(function(msg){
        console.log(msg);
        //test_dat = msg;
        if(msg['status'] == 'success'){
            if(msg['ct_id'] == 'empty'){
               //msg['item_ids'].join(', ');
               var url = 'http://cafalab.com/asp/CreateCartridgeTemplate.asp?items=';
               url += msg['item_ids'].join(', ')+'&random=101';
               //url += '&finish='+end_date+'%20'+end_time;
               url += '&name='+msg['name'];
               console.log(url);
               
               $.get(url, function (get_data) {
                    console.log(get_data);
                    var ct_id = $($(get_data).find('ID')[0]).text();
                    console.log(ct_id);
                    //var ct_id = 3693;
                    //ci_id = 'KWS9/7/2015-7:35:48 AM-wogud86@naver.com-2627';
                    
                    $.ajax({
                        url : '/tch/create_assesstemp_wiz2',
                        dataType:"json",
                        data : {
                            'method':'set_ct_id_and_at', 
                            'at_id':at_id,
                            'ct_id':ct_id,
                            'group_unit':group_unit,
                            'assess_type':assess_type,
                            'ids':JSON.stringify(ids),
                            'start':start,
                            'end':end,
                        }
                    }).done(function(create_ua_msg){
                        console.log(create_ua_msg);
                        if(create_ua_msg['status'] == 'success'){
                            //$(location).attr('href','/tch');
                            $(location).attr('href','/tch');
                        } else {
                            console.log(create_ua_msg);
                        }
                    });
                });
            } else {
                $(location).attr('href','/tch');
            }
        } else {
            console.log(msg);
        }
    });
}
$(document).on('click', '#submit', click_submit);







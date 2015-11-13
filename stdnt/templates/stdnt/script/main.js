{% include "stdnt/container/base.js" %}
{% include "stdnt/container/manage_probs.js" %}

$(document).ready(function(){
    $('footer').css('top', $('#wrap_lists').position().top+$('#wrap_lists').height()+80);
});
    
var solve_mode='m';
var ua_id;
$(document).on('click', '.exam_m, .exam_p', function(){
    //test_dat = this;
    //return false;
    //console.log($(this).val());
    if($(this).hasClass('exam_m')) solve_mode='m';
    if($(this).hasClass('exam_p')) solve_mode='p';
    
    //at_id = $(this).attr("value");
    var at_id = $(this).parent().parent().attr('at_id');
    var data = {};
    data['method'] = 'call_ua';
    data['at_id'] = at_id;
    //return false;
    $.ajax({
        url : '/stdnt',
        dataType:"json",
        data : data
    }).done(function(msg){
        console.log(msg);
        //return false;
        if(msg['status'] == 'success'){
            if(msg['ua_id'] == 'empty' || msg['start_time'] == 'empty'){
                url = 'http://cafalab.com/asp/CreateCartridgeInstance.asp?ID='+msg['ct_id']+'&user={{ my_info.email }}';
                console.log(url);
                
                $.get(url, function (get_data) {
                    console.log(get_data);
                    var ci_id = $($(get_data).find('ID')[0]).text();
                    //ci_id = 'KWS9/7/2015-7:35:48 AM-wogud86@naver.com-2627';
                    var getci_url = 'http://cafalab.com/asp/GetCartridgeInstance.asp?id='+ci_id;
                    console.log(getci_url);
                    $.get(getci_url, function (getci_data) {
                        console.log(getci_data);
                        var json = getci_to_json(getci_data);
                        console.log(json);
                        var data = {
                            'method':'create_ua', 
                            'items':JSON.stringify(json),
                            'at_id':at_id,
                            'ci_id':ci_id
                        };
                        if(msg['start_time'] == 'empty'){ 
                            data = {
                            'method':'create_gui', 
                            'items':JSON.stringify(json),
                            'at_id':at_id,
                            'ci_id':ci_id,
                            'ua_id':msg['ua_id'],
                            };
                        }
                        console.log(data);
                        $.ajax({
                            url : '/stdnt',
                            dataType:"json",
                            data : data,
                        }).done(function(create_ua_msg){
                            
                            console.log(create_ua_msg);
                            if(msg['status'] == 'success'){
                                ua_id = create_ua_msg['ua_id'];
                                switch(solve_mode){
                                case 'm':
                                    $(location).attr('href','/stdnt/solve_itemeach/'+ua_id);
                                    break;
                                case 'p':
                                    $(location).attr('href','/stdnt/print_assess/'+ua_id);
                                    break;
                                }
                             } else {
                                 console.log(create_ua_msg);
                             }
                        });
                    });
                });
                
            } else {
                ua_id = msg['ua_id'];
                //$("#go_exist_exam_modal").modal('show');
                switch(solve_mode){
                case 'm':
                    $(location).attr('href','/stdnt/solve_itemeach/'+ua_id);
                    break;
                case 'p':
                    $(location).attr('href','/stdnt/print_assess/'+ua_id);
                    break;
                }
            }
        }
    });
    return false;
});
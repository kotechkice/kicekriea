//stdnt/print_assess/?title=함수&itemids=1900,1901

window.params = function(){
    var params = {};
    if(window.location.href.indexOf('?') == -1){
        return params;
    }
    var param_array = window.location.href.split('?')[1].split('&');
    for(var i in param_array){
        x = param_array[i].split('=');
        params[x[0]] = x[1];
    }
    return params;
}();

{% include 'stdnt/container/manage_probs.js' %}

var alphabet = 'ABCDEF';
var circle_num = '①②③④⑤⑥';
var num_from_alpha = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5};
    
var head_html='';
var foot_html ='';
var workbook_probs_html = '';

//var title = decodeURIComponent(window.params.title);
//var itemids = window.params.itemids.split(',');
var title = '{{ua.at.name}}';
var itemids = JSON.parse('{{item_ids}}');

//var one_prob_html = '';
//var making_one_prob_complete_flag = false;
var made_item_num = 0;
var seed=100;
var order_num = 0;
//var lock_cafa_proto_flag = true;
function make_prob_html(itemid, prob_num, selector){
    making_one_prob_complete_flag = false;
    var html = '';
    $.ajax({
        url:'/stdnt/print_assess/'+'{{ ua_id }}',
        dataType:'json',
        data:{
            'method':'get_item_info',
            'itemid':itemid,
            //'itemid_str' : $(data).find('Item').text()
        }
    }).done(function(msg){
        //console.log(msg);
        //test_dat = msg;
        var choices_in_a_row = 1;
        order_num++;
        //console.log(order_num);
        var local_order_num = order_num;
        if(msg['status'] == 'success'){
            if(msg['choices_in_a_row']){
                choices_in_a_row = msg['choices_in_a_row'];
            }
            $.ajax({
                url : '/stdnt/solve_itemeach/{{ua.id}}',
                dataType:"json",
                data : {
                    'method':'get_itemid',
                    'order':prob_num,
                }
            }).done(function(msg){
                //console.log(String(msg['itemid'])+ '-' + String(local_order_num));
                if(msg['status'] == 'success'){
                    var itemid = msg['itemid'];
                    var permutation_str = msg['permutation'];
                    var response = msg['response'];
                    
                    var url = 'http://cafalab.com/asp/GetItem.asp?clientID=XXXX&item='+itemid+'&seed='+msg['seed'];
                    $.get(url, function (data) {
                        var q = getitem_to_json(data);
                        
                        $.ajax({
                            url : '/stdnt/solve_itemeach/{{ua.id}}',
                            dataType:"json",
                            data : {
                                'method':'set_permutation', 
                                'order':prob_num,
                                'permutation_str':q['permutation']
                            }
                        }).done(function(msg){
                            if(msg['status'] == 'success'){
                                //console.log(msg);
                                var item_permutation_str = msg['item_permutation'];
                                //console.log(item_permutation_str);
                                q = change_choices_as_permutation_str(q, permutation_str, item_permutation_str);
                                //getitem_json_to_html(json_one);
                                var per_value = Math.floor(100/choices_in_a_row);
                        
                                html += '<table class="one_prob" width="477px" cellpadding="3px" valign="top">';
                                html += '    <tr><td colspan="'+choices_in_a_row+'">';
                                html += prob_num + '. ' + q['question']; + '</td></tr>';
                                
                                html += '<tr>';
                                for(var j=0; j<5; j++){
                                    html += '<td class="choice width="'+per_value+'%" valign="top">'+circle_num[j] +' ' + q['choice'][j]+'</td>';
                                    if((j+1)%choices_in_a_row === 0){
                                        html += '</tr><tr>';
                                    }
                                }
                                html += '</tr></table>';
                                selector.html(html);
                                //one_prob_html = html;
                                //making_one_prob_complete_flag = true;
                                made_item_num++;
                                if(made_item_num == itemids.length){
                                    MathJax.Hub.Typeset();
                                }
                            }
                        });
                    }).fail(function(msg) {
                        console.log('error');
                        console.log(msg);
                        make_prob_html(itemid, prob_num, selector);
                    });
                }
            });
        } else {
            console.log(msg);
            console.log(itemid);
            console.log(prob_num);
        }
    });
}

function ready_func(){
    var html = '';
    //console.log(window.params.title);
    //console.log(window.params.itemids);
    html += '<div class="header" style="page-break-before:always">';
    html += '    <table width="960px" border="0" style="border-width:1; border-collapse:collapse;font-size:x-large">';
    html += '        <tr>';
    html += '            <td style="border-left:0px gray solid;border-right:0px gray solid;" valign="top" align="left" width="200px"></td>';
    html += '            <td style="border-left:0px gray solid;border-right:0px gray solid;" valign="top" align="center">';
    html += '                <span class="assess-title" style="font-size:xx-large">과제물 (수)</span><br />';
    html += '                <span class="user-email" style="font-size:small">User : {{ ua.user.email }}</span>';
    html += '            </td>';
    html += '            <td style="border-left:0px gray solid;border-right:0px gray solid;" valign="middle" align="right" width="100px">';
    html += '                <span class="page_num" style="font-size:xx-large">1</span>';
    html += '            </td>';
    html += '            <td style="border-left:0px gray solid;border-right:0px gray solid;" valign="middle" align="center" width="100px">';
    html += '                <a class="qr_code_link" href="/stdnt/input_response/{{ua.id}}">';
    html += '                    <img class="response_qr_code" src="http://chart.apis.google.com/chart?chs=100x100&cht=qr&chld=|0&chl=jindan.kice.re.kr/stdnt/input_response/{{ua.id}}" title="Scan this for more information about the standard" width="90px" height="90px" />';
    html += '                </a>';
    html += '            </td>';
    html += '        </tr>';
    html += '    </table>';
    html += '</div>';
    head_html = html;
    
    html = '';
    html += '<table class="workbook_probs"><tr>';
    html += '        <td valign="top" style="border-top:1px gray solid;border-right:1px gray solid;border-bottom:0px gray dashed;border-left:0px gray solid;">';
    html += '            <table class="column prob_left">';
    html += '                <tr class="prob_top"><td valign="top" height="540" style="padding-top:5px"> </td></tr>';
    html += '                <tr class="prob_bottom"><td valign="top" height="540" style="padding-top:5px"></td></tr>';
    html += '            </table>';
    html += '        </td>';
    html += '        <td valign="top" height="540" style="padding-top:5px; border-top:1px gray solid;border-right:0px gray solid;border-bottom:0px gray dashed;border-left:1px gray solid;">';
    html += '            <table class="column prob_right">';
    html += '                <tr class="prob_top"><td valign="top" height="540" style="padding-top:5px"> </td></tr>';
    html += '                <tr class="prob_bottom"><td valign="top" height="540" style="padding-top:5px"> </td></tr>';
    html += '            </table>';
    html += '        </td>';
    html += '</tr></table>';
    workbook_probs_html = html;
    
    html = '';
    html += '<table class="foot" width="954" border="0" style="border-width:1; border-collapse:collapse;">';
    html += '    <tr>';
    html += '        <td width="400px"></td>';
    html += '        <td align="center" valign="top">&nbsp;&nbsp;&nbsp;&nbsp;<span class="page_num">1</span> </td>';
    html += '        <td align="right" valign="top" width="400px" style="padding-right:12px"></td>';
    html += '    </tr>';
    html += '    <tr>';
    html += '        <td colspan="3" align="center">';
    html += '            <div style="display:none" >';
    html += '                <span style="color:blue; font-size:x-small" >이 문제지 및 관련 웹싸이트에 관한 모든 저작권은 한국교육측정연구소 및 eMathTest, Inc.에 있습니다.</span>';
    html += '            </div>';
    html += '        </td>';
    html += '    </tr>';
    html += '</table>';
    foot_html = html;
    
    var page_num = 1;
    for(var i=0; i<itemids.length;i+=4){
        var j=0;
        $('body').append(head_html);
        $('.assess-title:last').text('과제물('+title+')');
        $(".page_num:last").text(page_num);
        
        $('body').append(workbook_probs_html);
        make_prob_html(itemids[i+j], i+j+1, $('.prob_left:last .prob_top>td'));
        j++;
        if(i+j < itemids.length) make_prob_html(itemids[i+j], i+j+1, $('.prob_left:last .prob_bottom>td'));
        j++;
        if(i+j < itemids.length) make_prob_html(itemids[i+j], i+j+1, $('.prob_right:last .prob_top>td'));
        j++;
        if(i+j < itemids.length) make_prob_html(itemids[i+j], i+j+1, $('.prob_right:last .prob_bottom>td'));
        $('body').append(foot_html);
        $(".page_num:last").text(page_num);
        page_num++; 
    }
}
$(document).ready(ready_func);

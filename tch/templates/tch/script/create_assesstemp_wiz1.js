{% include "mngins/container/manage_probs.js" %}
var test_dat;
var choices_num_line;
var alphabet = "ABCDEFGHIJK";
var circle_num = '①②③④⑤⑥';
var num_from_alpha = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5};

function set_footer(){
    $('footer').css('top',$('#wrap_inputs').position().top+$('#wrap_inputs').height()+100);
}

$(document).ready(function(){
    set_footer();
});

function click_search_btn(){
    test_dat = this;
    //console.log(this);
    var selected_id = -1;
    //var selects = $('#select_category_table select');
    var selects = $('select');
    for(var i=0; i<selects.length;i++){
        if( $(selects[i]).find('option:selected').attr('itc_id') != -1){
            selected_id = $(selects[i]).find('option:selected').attr('itc_id');
        }
    }
    //console.log(selected_id);
    //$($('#select_category_table select')[0]).find('option:selected').attr('itc_id');
    $.ajax({
        url:'/tch/create_assesstemp_wiz1',
        dataType:'json',
        data:{
            'method':'get_items',
            'selected_id':selected_id,
            //'itemid_str' : $(data).find('Item').text()
        }
    }).done(function(msg){
        //console.log(msg);
        //test_dat = msg;
        if(msg['status'] == 'success'){
            
            $("#searched_item_list_table>tbody").html("");
            for(var i=0; i<msg['it_infos'].length; i++){
                html = '';
                html += '<tr><td><input type="checkbox" /></td>';
                html += '<td class="td-itemid"><u>'+ msg['it_infos'][i]['itemid'] +'</u></td>';
                
                html += '<td class="td-diff">';
                switch(msg['it_infos'][i]['difficulty']){
                    case 0: html += '쉬움'; break;
                    case 1: html += '보통'; break;
                    case 2: html += '어려움'; break;
                    default: html += '결정안됨';
                }
                html += '</td><td class="td-ability">';
                switch(msg['it_infos'][i]['ability']){
                    case 1: html += '지식'; break;
                    case 2: html += '이해'; break;
                    case 3: html += '적용'; break;
                    case 4: html += '분석'; break;
                    default: html += '결정안됨';
                }
                html += '</td><td class="td-type">선다형</td>';
                html += '<td class="td-mng">';
                html += '<button class="show_item_value">내용보기</button>';
                //html += '<a href="#" class="del_category_one">카테고리에서 삭제</a>';
                html += '</td></tr>';
                //console.log(html);
                $("#searched_item_list_table>tbody").append(html);
                set_footer();
            }
        } else {
            console.log(msg);
        }
    });
    
}
$(document).on('click', '#search_btn', click_search_btn);

function click_show_item_value_link(){
    //test_dat = this;
    var this_var = this;
    var parent_tr = $(this).parent().parent();
    var td_length = parent_tr.find('td').length;
    var itemID = parent_tr.find('.td-itemid').text();
    var choices_in_a_row = Number(parent_tr.find('.td-choices_in_a_row').text());
    var seed = 100;
    
    if(parent_tr.next().hasClass('item_detail_tr')){
        if(parent_tr.next().is(":visible")){
            parent_tr.next().hide();
            $(this).text('내용보기');
        } else {
            parent_tr.next().show();
            $(this).text('내용닫기');
        }
        return false;
    } else {
        $(this).text('내용닫기');
    }
    parent_tr.after('<tr class=item_detail_tr><td colspan="'+td_length+'"><div>loading</div></td></tr>');
    
    url = 'http://cafalab.com/asp/GradeItem.asp?clientID=XXXX&item='+itemID+'&seed='+seed;
    $.get(url, function(data){
        var html_dat = '';
        //var html_dat = '<tr class=item_detail_tr><td colspan="'+td_length+'"><div>';
        var q = getitem_to_json(data);
        //q = change_choices_as_permutation_str(q, item['permutation'], item['item_permutation']);
        //var s = gradeitem_to_json(data);
        html_dat += q['question'];
        var per_value = Math.floor(100/choices_in_a_row);
        html_dat += '<br /><table width="100%"><tr>';
        for(var j=0; j<5; j++){
            html_dat += '<td class="choice width="'+per_value+'%" valign="top">'+circle_num[j] +' ' + q['choice'][j]+'</td>';
            if((j+1)%choices_in_a_row === 0){
                html_dat += '</tr><tr>';
            }
        }
        html_dat += '</tr></table>';
        parent_tr.next().find('div').html(html_dat);
        //html_dat += '</div></td></tr>';
        //console.log(html_dat);
        //html_dat = '<tr class=item_detail_tr><td rowspan="'+td_length+'">hello</td></tr>';
        //$(this_var).parent().parent().after(html_dat);
        MathJax.Hub.Typeset();
        set_footer();
    });
    return false;
}
$(document).on('click','.show_item_value', click_show_item_value_link);

function click_research_btn(){
    //test_dat = this;
    var search_item_tr = $('#searched_item_list_table>tbody>tr');
    var checked_diffs = $('.checked_diff');
    var checked_types = $('.checked_type');
    
    var show_flag = false;
    
    for(var i=0; i<search_item_tr.length; i++){
        //$(search_item_tr[0]).find('.td-diff').text();
        show_flag = false;
        
        for(var j=0; j<checked_diffs.length; j++){
            if($(checked_diffs[j]).find('input').is(':checked')){
                if($(checked_diffs[j]).text()==$(search_item_tr[i]).find('.td-diff').text()){
                    show_flag = true;
                }
            }
        }
        if(show_flag){
            show_flag=false;
            for(var j=0; j<checked_types.length; j++){
                if($(checked_types[j]).find('input').is(':checked')){
                    if($(checked_types[j]).text()==$(search_item_tr[i]).find('.td-type').text()){
                        show_flag = true;
                    }
                }
            }
        }
        if(show_flag){
            $(search_item_tr[i]).show();
        } else {
            $(search_item_tr[i]).find('input').prop('checked',false);
            $(search_item_tr[i]).hide();
        }
    }
    set_footer();
}
$(document).on('click', '#research_btn',click_research_btn);

$(document).on('click', '#searched_item_list_table thead input', function(){
    //test_dat = this;
    //console.log('click');
    $('#searched_item_list_table>tbody>tr:visible input').prop('checked', $(this).is(':checked'));
});

function click_select_searched_items_btn(){
    //test_dat = this;
    var search_item_tr = $('#searched_item_list_table>tbody>tr');
    //var html = '';
    for(var i=0; i<search_item_tr.length; i++){
        if($(search_item_tr[i]).find('input').is(':checked')){
            //console.log($(search_item_tr[i]).html());
            $('#selected_item_list_table>tbody').append('<tr>'+$(search_item_tr[i]).html()+'</tr>');
            $('#selected_item_list_table>tbody>tr:last>td:eq(0)').remove();
            $('#selected_item_list_table>tbody>tr:last>td:last').append(' <button class="btn btn-primary btn-xs del_selected_item">삭제</button>');
        }
    }
    $('#items_in_cart').show();
    set_footer();
}
$(document).on('click', '#select_searched_items_btn', click_select_searched_items_btn);

$(document).on('click', '.del_selected_item',function(){
    //test_dat = this;
    $(this).parent().parent().remove();
});

function click_save_btn(){
    var assess_name = $('#assess_name').val();
    if(assess_name == ''){
        return false;
    }
    item_ids = [];
    var selected_item_tr = $('#selected_item_list_table>tbody>tr');
    for(var i=0; i<selected_item_tr.length; i++){
        item_ids.push($(selected_item_tr[i]).find('.td-itemid').text());
    }
    //console.log(item_ids);
    
    $.ajax({
        url:'/tch/create_assesstemp_wiz1',
        dataType:'json',
        data:{
            'method':'save_assess',
            'assess_name':assess_name,
            'item_ids':JSON.stringify(item_ids),
            'type':$("input[name=assess_type]:checked").val(),
            //'selected_id':selected_id,
            //'itemid_str' : $(data).find('Item').text()
        }
    }).done(function(msg){
        //console.log(msg);
        //test_dat = msg;
        if(msg['status'] == 'success'){
            $(location).attr('href','/tch');
        } else {
            console.log(msg);
        }
    });
}
$(document).on('click', '#save_btn', click_save_btn);

function select_itc(){
    //test_dat = this;
    var itc_id = $(this).find('option:selected').attr('itc_id');
    var id_str = $(this).attr('id');
    $.ajax({
        url:'/tch/create_assesstemp_wiz1',
        dataType:'json',
        data:{
            'method':'sel_itc',
            'itc_id':itc_id,
        }
    }).done(function(msg){
        console.log(msg);
        test_dat = msg;
        if(msg['status'] == 'success'){
        //    $(location).attr('href','/tch');
            var html = '';
            if(msg['belong_itcs'].length == 0){
                html = '<option itc_id="-1">--</option>';
            }
            for(var i=0; i< msg['belong_itcs'].length; i++){
                 html += '<option itc_id='+msg['belong_itcs'][i]['id'] +'>';
                 html += msg['belong_itcs'][i]['name'] + '</option>';
            }
            switch(id_str){
                case 'academy_select':
                    $('#standard_select').html('<option itc_id="-1">--</option>');
                    $('#unit_select').html('<option itc_id="-1">--</option>');
                    $('#course_select').html(html);
                    if(msg['belong_itcs'].length != 0) $('#course_select').change();
                    break;
                case 'course_select':
                    $('#standard_select').html('<option itc_id="-1">--</option>');
                    $('#unit_select').html(html);
                    if(msg['belong_itcs'].length != 0) $('#unit_select').change();
                    break;
                case 'unit_select':
                    $('#standard_select').html(html);
                    if(msg['belong_itcs'].length != 0) $('#standard_select').change();
                    break;
                case 'standard_select':
                    break;
            }
        } else {
            console.log(msg);
        }
    });
}
$(document).on('change', '#academy_select, #course_select, #unit_select', select_itc);


function click_show_assess_preview_btn(){
    //console.log('click');
    //$($('#selected_item_list_table tbody .td-itemid')[0]).text()
    var items = $('#selected_item_list_table tbody .td-itemid');
    var url = '/tch/assess_preview/?';
    url += 'title='+$('#assess_name').val();
    url += '&itemids=';
    for(var i=0; i<items.length; i++){
        url += $(items[i]).text();
        if(i != items.length-1) url += ',';
    }
    window.open(url);
}
$(document).on('click', '#show_assess_preview_btn', click_show_assess_preview_btn);


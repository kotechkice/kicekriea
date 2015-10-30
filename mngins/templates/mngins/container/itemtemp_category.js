var test_dat;

var choices_num_line;
var alphabet = "ABCDEFGHIJK";
var circle_num = '①②③④⑤⑥';
var num_from_alpha = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5};

var category_types = {
    'N': '없음',
    'R': '루트',
    'O': '과목명',
    'U': '단원',
    'A': '학교급',
    'G': '학년',
    'D': '대단원',
    'M': '중단원',
    'C': 'Cluster',
    'S': '성취기준',
    //'E': '기타',
};

var marks = {
    'BRPO':['I.', 'II.', 'III.'], //Big Rome letters with a point
    'SRPO':['i.', 'ii.', 'iii.'], //Small Rome letters with a point
    
    'NMPO':['1.', '2.', '3.'], //Numbers with a point
    'NMAC':['①', '②', '③'], //Numbers in a circle
    'NMAR':['1)', '2)', '3)'], //Numbers with a round bracket
    'NMRB':['(1)', '(2)', '(3)' ], //Numbers in round brackets
    'NMSB':['[1]', '[2]', '[3]' ], //Numbers in square brackets 
    'NMBR':['<1>', '<2>', '<3>'], //Numbers in braces
    
    //'BEPO':['A.'], //Big English with a point
    //'SEPO':['a.'], //Small English with a point//ⓐⓑⓒ
    //'KCPO':['ㄱ.'], //Korean Consonants with a point
    //'KWPO':['가.'], //Korean Words with a point
};

function getitem_to_json(xml_data){
    xml_data = $(xml_data).find('Item')[0];
    var prob_dict = {};       
    var prob_tag = ["seed", "question", "choice", "permutation"];
    for(index in prob_tag){
        if(prob_tag[index] == "choice"){
            prob_dict['choice'] = [];
            for(var j=0; j<$(xml_data).find(">choice").length; j++){
                prob_dict['choice'].push($($(xml_data).find(">choice:eq("+j+")")[0]).text());
            }
        }  else if (prob_tag[index] == "seed") {
            seed = $($(xml_data).find(">seed")).text();
        }  else {
            prob_dict[prob_tag[index]] = $($(xml_data).find(">"+prob_tag[index])).text();
        }
    }
    return prob_dict;
}
function gradeitem_to_json(xml_data){
    xml_data = $(xml_data).find('Item')[0];
    var prob_dict = {};       
    var prob_tag = ["answer", "solution"];
    for(index in prob_tag){
        if (prob_tag[index] == "answer") {//A:1, B:2, C:3, D:4, E:5
            ans = $(xml_data).find(">answer").text();
            //prob_dict["answer"] = ans;
            prob_dict["answer"] = $(xml_data).find(">answer").text().charCodeAt(0) - 'A'.charCodeAt(0) + 1;
            prob_dict["answer_text"] = $($(xml_data).find(">choice:eq("+(prob_dict["answer"]-1)+")")[0]).text();
        } else if(prob_tag[index] == "solution"){
            prob_dict[prob_tag[index]] = $($(xml_data).find(">"+prob_tag[index])).text();
            prob_dict['solutions'] = [];
            for(var j=0; j<$(xml_data).find(">solution").length; j++ ){
                prob_dict['solutions'].push($($(xml_data).find(">solution:eq("+j+")")[0]).text());
            }
        }else {
            prob_dict[prob_tag[index]] = $($(xml_data).find(">"+prob_tag[index])).text();
        }
    }
    return prob_dict;
}
function getiteminfo_to_json(xml_data){
    xml_data = $(xml_data).find('Item')[0];
    var prob_dict = {};       
    var prob_tag = ["ItemID", "ModuleID", "Category1", "Difficulty", "Skill", "AnswerType", "Points", "Ability", "Description", "Exposure", "Correct", "Complexity", "Created", "Institute", "ChoicesPerLine", "Height"];
    for(index in prob_tag){
        prob_dict[prob_tag[index]] = $($(xml_data).find(">"+prob_tag[index])).text();
    }
    return prob_dict;
}

$(document).ready(function(){
    var option_html = "";
    option_html += '<option value="None">없음</option>';
    for(var key in marks){
        //console.log(key);
        //console.log(marks[key]);
        var exam_string = marks[key].join('');
        option_html += '<option value = "'+key+'">'+exam_string+'</option>';
    }
    //marks
    $("#category_label_row>td:eq(0)>.mark_type>select").html(option_html);
    $("#category_label_row>td:eq(0)>.mark_type>select").val("{{ itcll0_s.mark }}").attr("selected", "selected");
    
    option_html = "";
    for(var key in category_types){
        option_html += '<option value = "'+key+'">'+category_types[key]+'</option>';
    }
    $("#category_label_row>td:eq(0)>.category_type_edit>select").html(option_html);
    $("#category_label_row>td:eq(0)>.category_type_edit>select").val("{{ itcll0_s.type }}").attr("selected", "selected");
});

$(document).on('click', '.show_item_detail', function(){
    //test_dat  = this;
    var this_sel = this; 
    
    $(this_sel).parent().parent().find('.item_detail').toggle();
    $(this_sel).parent().parent().find('.show_txt').toggle();
    $(this_sel).parent().parent().find('.close_txt').toggle();
    
    if($(this_sel).parent().parent().find('.item_detail').text() != 'empty'){
        return false;
    }
    $(this_sel).parent().parent().find('.item_detail').text('loading');
    
    var itemID = $(this).parent().parent().attr("itemid");
    var seed = 100;
    var choices_num_line = 5;
    //$(this).parent().parent().find('.td-itemid').append('hi')
    var url = 'http://cafalab.com/asp/GetItemInfo.asp?clientID=XXXX&item='+itemID;
    $.get(url, function (data) {
        var json_one = getiteminfo_to_json(data);
        if(isNaN(json_one['ChoicesPerLine'])){
            choices_num_line = 3;
        } else {
            choices_num_line = Number(json_one['ChoicesPerLine']);
            if(choices_num_line == 0) {
                choices_num_line = 3;
            }
        }
        var url_grade = 'http://cafalab.com/asp/GradeItem.asp?clientID=XXXX&item='+itemID+'&seed='+seed;
        $.get(url_grade, function (data) {
            //console.log(data);
            var prob_q = getitem_to_json(data);
            var prob_s = gradeitem_to_json(data);
            
            var html_dat = prob_q['question'];
            var per_value = Math.floor(100/choices_num_line);
            
            var html_dat = prob_q['question'];
            var per_value = Math.floor(100/choices_num_line);
            
            html_dat += '<br /><table width="100%"><tr>';
            for(var i=0; i<5; i++){
                html_dat += '<td class="choice width="'+per_value+'%" valign="top">'+circle_num[i] +' ' + prob_q['choice'][i]+'</td>';
                if((i+1)%choices_num_line === 0){
                    html_dat += '</tr><tr>';
                }
            }
            html_dat += '</tr></table>';
            $(this_sel).parent().parent().find('.item_detail').html(html_dat);
            MathJax.Hub.Typeset();
        });
    });
    return false;
});
$(document).on('change', '#category_list_row select', function(){
    var itc_id = $(this).find('option:selected').attr('itc_id');
    var level = Number($(this).parent().attr('level'));
    
    var sel_category_exp_val = '';
    for(var i=0; i<=level; i++){
        if(i !=0 ) sel_category_exp_val +='>';
        sel_category_exp_val += $('.select_td[level='+i+']>select>option:selected').text();
    }
    $('#sel_category_exp').text(sel_category_exp_val);
    $('#category_edit_row>td[level='+level+']>input').val($(this).find('option:selected').text());

    $.ajax({
        url:'/mngins/itemtemp_category',
        dataType:'json',
        data:{
            'method':'sel_itc',
            'itc_id':itc_id,
            'level':level,
            //'itemid_str' : $(data).find('Item').text()
        }
    }).done(function(msg){
        //console.log(msg);
        //test_dat = msg;
        if(msg['status'] == 'success'){
            $("td").filter(function(){return $(this).attr('level') > level;}).remove();
            //console.log(msg['itcs'].length);
            if(msg['itcs'].length > 0){
                //set category_label_row
                var html= '<td level="'+(level+1)+'" colspan="2">' + $('#category_label_row>td:eq(0)').html() + '</td>';
                $('#category_label_row').append(html);
                $('#category_label_row>td[level='+(level+1)+']>.category_type_edit>select').val(msg['next_level_label']['type']).attr('selected','selected');
                $('#category_label_row>td[level='+(level+1)+']>.mark_type>select').val(msg['next_level_label']['mark']).attr('selected','selected');
                //$('#category_label_row>td[level=0]>.category_type_edit>select').val('R').attr('selected','selected')
                //#category_list_row
                
                //set category_edit_row
                var add_category_td_html = $("#add_category_td").html(); 
                $("#add_category_td").remove();
                html  = '<td level="'+ (level+1)+'" class="select_td">';
                html += '   <select size="5" style="width: 180px;">';
                for(index in msg['itcs']){
                    html += '<option itc_id="'+msg['itcs'][index]['id']+'">'+msg['itcs'][index]['name']+'</option>';
                    //console.log(msg['itcs'][index]);
                }
                
                html += '   </select>';
                html += '</td>';
                $('#category_list_row').append(html);
                $('#category_list_row').append('<td level="'+ (level+1) +'" class="arrow_td">'+$('.arrow_td:eq(0)').html()+'</td>');
                $('#category_list_row').append('<td id="add_category_td">'+add_category_td_html+'</td>');
                
                //set category_edit_row
                $('#category_edit_row').append('<td level="'+ (level+1) +'" colspan="2">'+$('#category_edit_row>td:eq(0)').html()+'</td>');
                
                //set selected_cate_item_list_table
                $("#selected_cate_item_list_table>tbody").html("");
                
            }
        }
    });
});

$(document).on('change', '.category_type_edit select', function(){
    //console.log('change');
    //test_dat = this;
    var type = $(this).val();
    var level = $(this).parent().parent().attr('level');
    var name = '';
    if(level == 0){
        $(this).val('R');
        return false;
    }
    $.ajax({
        url:'/mngins/itemtemp_category',
        dataType:'json',
        data:{
            'method':'change_category_type',
            'type':type,
            'level':level,
            'name':name
        }
    }).done(function(msg){
        //test_dat = msg;
        //console.log(msg);
        if(msg['status'] == 'success'){
        } else {
            console.log(msg);
        }
    });
});
$(document).on('change', '.mark_type select', function(){
    //console.log('change');
    //test_dat = this;
    var mark = $(this).val();
    var level = $(this).parent().parent().attr('level');
    if(level == 0){
        $(this).val('None');
        return false;
    }
    $.ajax({
        url:'/mngins/itemtemp_category',
        dataType:'json',
        data:{
            'method':'change_category_mark',
            'mark':mark,
            'level':level
        }
    }).done(function(msg){
        //test_dat = msg;
        //console.log(msg);
        if(msg['status'] == 'success'){
        } else {
            console.log(msg);
        }
    });
});
$(document).on('click','.edit_category_btn', function(){
    //test_dat = this;
    var this_val = this;
    var level = $(this).parent().attr('level');
    var name = $(this).parent().find('input').val();
    var upper_itc_id = null;
    if(level != 0){
        upper_itc_id = $('.select_td[level='+(level-1)+']>select>option:selected').attr('itc_id');
    }
    
    if($(this).hasClass('add_category')){
        
        $.ajax({
            url:'/mngins/itemtemp_category',
            dataType:'json',
            data:{
                'method':'add_category',
                'level':level,
                'name':name,
                'upper_itc_id':upper_itc_id
            }
        }).done(function(msg){
            //test_dat = msg;
            //console.log(msg);
            if(msg['status'] == 'success'){
                var html = '';
                for(var i=0; i<msg['itc_lists'].length; i++){
                    html += '<option itc_id="'+msg['itc_lists'][i]['id']+'">'+msg['itc_lists'][i]['name']+'</option>';
                }
                $('.select_td[level='+level+']>select').html(html);
                $(this_val).parent().find('input').val('');
                $("td").filter(function(){return $(this).attr('level') > level;}).remove();
            } else {
                console.log(msg);
            }
        });
    } else if($(this).hasClass('modify_category')){
        var id = $('.select_td[level='+level+']>select>option:selected').attr('itc_id');
        $.ajax({
            url:'/mngins/itemtemp_category',
            dataType:'json',
            data:{
                'method':'modify_category',
                'id':id,
                'name':name,
                'level':level,
                'upper_itc_id':upper_itc_id
            }
        }).done(function(msg){
            //test_dat = msg;
            //console.log(msg);
            if(msg['status'] == 'success'){
                var html = '';
                for(var i=0; i<msg['itc_lists'].length; i++){
                    html += '<option itc_id="'+msg['itc_lists'][i]['id']+'">'+msg['itc_lists'][i]['name']+'</option>';
                }
                $('.select_td[level='+level+']>select').html(html);
                $(this_val).parent().find('input').val('');
                $("td").filter(function(){return $(this).attr('level') > level;}).remove();
            } else {
                console.log(msg);
            }
        });
    } else if($(this).hasClass('del_category')){
        var id = $('.select_td[level='+level+']>select>option:selected').attr('itc_id');
        $.ajax({
            url:'/mngins/itemtemp_category',
            dataType:'json',
            data:{
                'method':'del_category',
                'id':id,
                'level':level,
                'upper_itc_id':upper_itc_id
            }
        }).done(function(msg){
            //test_dat = msg;
            //console.log(msg);
            if(msg['status'] == 'success'){
                var html = '';
                for(var i=0; i<msg['itc_lists'].length; i++){
                    html += '<option itc_id="'+msg['itc_lists'][i]['id']+'">'+msg['itc_lists'][i]['name']+'</option>';
                }
                $('.select_td[level='+level+']>select').html(html);
                $(this_val).parent().find('input').val('');
                
                $("td").filter(function(){return $(this).attr('level') > level;}).remove();
            } else {
                console.log(msg);
            }
        });
    }
});
$(document).on('click','#add_category_td>button', function(){
    //console.log('click');
    if($('.select_td:last>select>option:selected').length == 0){
        return false;
    }
    var level = Number($('#category_label_row>td:last').attr('level'));
    $.ajax({
        url:'/mngins/itemtemp_category',
        dataType:'json',
        data:{
            'method':'get_or_create_levellabel',
            'level':level+1
        }
    }).done(function(msg){
        //test_dat = msg;
        //console.log(msg);
        if(msg['status'] == 'success'){
            //set category_label_row
            var html= '<td level="'+(level+1)+'" colspan="2">' + $('#category_label_row>td:eq(0)').html() + '</td>';
            $('#category_label_row').append(html);
            $('#category_label_row>td[level='+(level+1)+']>.category_type_edit>select').val(msg['type']).attr('selected','selected');
            $('#category_label_row>td[level='+(level+1)+']>.mark_type>select').val(msg['mark']).attr('selected','selected');
            
            //set category_edit_row
            var add_category_td_html = $("#add_category_td").html(); 
            $("#add_category_td").remove();
            html  = '<td level="'+ (level+1)+'" class="select_td">';
            html += '   <select size="5" style="width: 180px;">';
            html += '   </select>';
            html += '</td>';
            $('#category_list_row').append(html);
            $('#category_list_row').append('<td level="'+ (level+1) +'" class="arrow_td">'+$('.arrow_td:eq(0)').html()+'</td>');
            $('#category_list_row').append('<td id="add_category_td">'+add_category_td_html+'</td>');
            
            //set category_edit_row
            $('#category_edit_row').append('<td level="'+ (level+1) +'" colspan="2">'+$('#category_edit_row>td:eq(0)').html()+'</td>');
            
        } else {
            console.log(msg);
        }
    });
});
$(document).on('click','.arrow_btn', function(){
    //test_dat = this;
    //var this_val = this;
    //console.log('click arrow');
    var level = $(this).parent().attr('level');
    
    if($('.select_td[level='+level+']>select>option:selected').length == 0){
        return false;
    }
    var id = $('.select_td[level='+level+']>select>option:selected').attr('itc_id');
    var upper_itc_id = null;
    if(level != 0){
        upper_itc_id = $('.select_td[level='+(level-1)+']>select>option:selected').attr('itc_id');
    }
    
    var direction = 'up';
    if($(this).hasClass('arrow_down')){
        direction = 'down';
    }
    
    $.ajax({
        url:'/mngins/itemtemp_category',
        dataType:'json',
        data:{
            'method':'change_order',
            'direction':direction,
            'id':id,
            'level':level,
            'upper_itc_id':upper_itc_id
        }
    }).done(function(msg){
        //test_dat = msg;
        //console.log(msg);
        if(msg['status'] == 'success'){
            var html = '';
            for(var i=0; i<msg['itc_lists'].length; i++){
                html += '<option itc_id="'+msg['itc_lists'][i]['id'] + '"';
                if(i==msg['changed_order']-1) html += 'selected';
                html +='>'+msg['itc_lists'][i]['name']+'</option>';
            }
            $('.select_td[level='+level+']>select').html(html);
        } else {
            console.log(msg);
        }
    });
});
$(document).on('click','.show_item_value', function(){
    test_dat = this;
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
    });
    return false;
});
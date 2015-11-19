{% include "stdnt/container/base.js" %}
{% include "stdnt/container/manage_probs.js" %}

var alphabet = 'ABCDEF';
var circle_num = '①②③④⑤⑥';
var num_from_alpha = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5};
var num_from_level = {
    '{{ stdnt_string.LEVEL.H }}':4, 
    '{{ stdnt_string.LEVEL.M }}':3, 
    '{{ stdnt_string.LEVEL.L }}':2, 
    '{{ stdnt_string.LEVEL.F }}':1
};
var test_dat;

///stdnt/show_solution/?itemid=1900&seed=200&order=2&correctanswer=3&response=2&permutation=14235&item_permutation=42315&choices_in_a_row=3
    
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

var itemid = window.params.itemid;
var seed = window.params.seed;
var order = window.params.order;
var correctanswer = window.params.correctanswer;
var response = window.params.response;
var permutation = window.params.permutation;
var item_permutation = window.params.item_permutation;
var choices_in_a_row = window.params.choices_in_a_row;

$(document).ready(function(){
    $('#td-order').text(order);
    
    switch(correctanswer){
        case 'A': $('#td-correctanswer').text('1'); break;
        case 'B': $('#td-correctanswer').text('2'); break;
        case 'C': $('#td-correctanswer').text('3'); break;
        case 'D': $('#td-correctanswer').text('4'); break;
        case 'E': $('#td-correctanswer').text('5'); break;
    }
    switch(response){
        case 'A': $('#td-response').text('1'); break;
        case 'B': $('#td-response').text('2'); break;
        case 'C': $('#td-response').text('3'); break;
        case 'D': $('#td-response').text('4'); break;
        case 'E': $('#td-response').text('5'); break;
    }
    set_item_html_from_items();
});



function set_item_html_from_items(){
    url = 'http://cafalab.com/asp/GradeItem.asp?clientID=XXXX&item='+itemid+'&seed='+seed;
    //console.log(url);
    $.get(url, function (data) {
        var q = getitem_to_json(data);
        q = change_choices_as_permutation_str(q, permutation, item_permutation);
        var s = gradeitem_to_json(data);
        var html_dat = '';

        html_dat += q['question'];
        var per_value = Math.floor(100/choices_in_a_row);
        html_dat += '<br /><br /><table width="100%"><tr>';
        for(var j=0; j<5; j++){
            html_dat += '<td class="choice width="'+per_value+'%" valign="top">'+circle_num[j] +' ' + q['choice'][j]+'</td>';
            if((j+1)%choices_in_a_row === 0){
                html_dat += '</tr><tr>';
            }
        }
        html_dat += '</tr></table><br />';
        
        $('#question').html(html_dat);
        $('#solution').html(s['solution']);
        
        MathJax.Hub.Typeset();
    }).done(function(){
    });
}
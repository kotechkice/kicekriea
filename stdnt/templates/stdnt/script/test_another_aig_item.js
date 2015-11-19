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

///stdnt/test_another_aig_item/?itemid=1900&order=2
    
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
var order = window.params.order;
var test_dat;
var answer = '①';

$(document).ready(function(){
    
    $('#order_num').text(order);
    
    var seed = Math.floor(Math.random() * (500 - 1)) + 1;
    var url = 'http://cafalab.com/asp/GradeItem.asp?clientID=XXXX&item='+itemid+'&seed='+seed;
    
    $.get(url, function (data) {
        test_dat = data;
        console.log(data);
        var q = getitem_to_json(data);
        var s = gradeitem_to_json(data);

        answer = s['answer'];
        switch(s['answer']){
            case 1: answer = '①'; break;
            case 2: answer = '②'; break;
            case 3: answer = '③'; break;
            case 4: answer = '④'; break;
            case 5: answer = '⑤'; break;
            
        }
        $("#cop-question").html(q['question']);
        for(var i=1; i<=5; i++){
            $("#choice-"+i).text(q['choice'][i-1]);
        }
        
        $('#answer_text').text(answer);
        MathJax.Hub.Typeset();
    });
});

$(document).on('click', '#repeat_train', function(){
    location.reload();
});

$(document).on('click', '#show_answer_btn', function(){
    $('#answer_text').show();
});

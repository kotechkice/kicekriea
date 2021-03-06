{% include 'stdnt/container/manage_probs.js' %}
    
var ua_id = '{{ ua.id }}';
var ci_id = '{{ ua.ci_id }}';
var order = 1;
var num_of_item = 0;
var clientID = 'clientIDxxx';
var finished_flag = false;
//var init_grade_status = 'wait';
var test_dat;
var start_time;

function init_order(){
    var data = {};
    data['method'] = 'init_order';
    $.ajax({
        url : '/stdnt/solve_itemeach/'+ua_id,
        dataType:"json",
        data : data
    }).done(function(msg){
        //console.log(msg);
        if(msg['status'] == 'success'){
            order = msg['order'];
            getNset_item(order);
            num_of_item = msg['num_item'];
            reponses_str = msg['responses'];
            if(reponses_str.indexOf('x') == -1){
                finished_flag = true;
                $("#submit_responses").removeAttr("disabled");
                $("#submit_responses").show("disabled");
            }
            //init_grade_status = 'ready';
            //$("#cop-count").text(String(order)+'/'+String(num_of_item));
            //$("#cop-count").text('총 '+String(num_of_item)+ ' 문항 중 ' +String(order)+'번 문항');
            $("#cop-count").text(String(order)+'번 문항(총 '+String(num_of_item)+ '문항)');
        }
    });
}
function getNset_item(order_num){
    $("#pre_item").attr("disabled", true);
    $("#submit_responses").attr("disabled", true);
    $("#next_item").attr("disabled", true);
    
    var data = {};
    data['method'] = 'get_itemid';
    data['order'] = order_num;
    $.ajax({
        url : '/stdnt/solve_itemeach/'+ua_id,
        dataType:"json",
        data : data
    }).done(function(msg){
        //.log(msg);
        if(msg['status'] == 'success'){
            var itemid = msg['itemid'];
            var permutation_str = msg['permutation'];
            var response = msg['response'];
            //console.log(itemid);
            var url = 'http://cafalab.com/asp/GetItem.asp?clientID='+clientID+'&item='+itemid+'&seed='+msg['seed'];
            $.get(url, function (data) {
                //console.log(data);
                var json_one = getitem_to_json(data);
                //console.log(json_one);
                
                $.ajax({
                    url : '/stdnt/solve_itemeach/'+ua_id,
                    dataType:"json",
                    data : {
                        'method':'set_permutation', 
                        'order':order_num,
                        'permutation_str':json_one['permutation']
                    }
                }).done(function(msg){
                    if(msg['status'] == 'success'){
                        //console.log(msg);
                        var item_permutation_str = msg['item_permutation'];
                        //console.log(item_permutation_str);
                        json_one = change_choices_as_permutation_str(json_one, permutation_str, item_permutation_str);
                        getitem_json_to_html(json_one);
                        MathJax.Hub.Typeset();
                    }
                });
            });
            order = order_num;
            //$("#cop-count").text(String(order)+'/'+String(num_of_item));
            //$("#cop-count").text('총 '+String(num_of_item)+ ' 문항 중, ' +String(order)+'번 문항');
            $("#cop-count").text(String(order)+'번 문항(총 '+String(num_of_item)+ '문항)');
            switch(response){
                case 'A':
                    $("#cop-choice label:eq(0)").addClass('active');
                    break;
                case 'B':
                    $("#cop-choice label:eq(1)").addClass('active');
                    break;
                case 'C':
                    $("#cop-choice label:eq(2)").addClass('active');
                    break;
                case 'D':
                    $("#cop-choice label:eq(3)").addClass('active');
                    break;
                case 'E':
                    $("#cop-choice label:eq(4)").addClass('active');
                    break;
            }
            //console.log(response);
            if(order >= num_of_item){
                //finished_flag = true;
                $("#submit_responses").show();
            } else if(response != 'x') $("#next_item").removeAttr("disabled");
            
            if(finished_flag) {
                $("#submit_responses").removeAttr("disabled");
                $("#submit_responses").show();
            }
            if(order_num != 1) $("#pre_item").removeAttr("disabled");
            start_time = new Date().getTime();
        }
    });
}
$(document).ready(function(){
    init_order();
    //var order = 1;
    //if($.cookie("order") != undefined){
    //  order = $.cookie("order");
    //} else {
        //init_grade();
    //}
    //getNset_item(order);
    $("#submit_responses").hide();
});
$(document).on('click','#pre_item',function(){
    if(order <= 1){
        return false;
    }
    order--;
    getNset_item(order);
    $(window).scrollTop(0);
    for(var i=0; i<5; i++){
        $("#cop-choice label:eq("+i+")").removeClass("active");
    }
});
$(document).on('click','#next_item',function(){
    if(order >= num_of_item){
        return false;
    }
    order++;
    getNset_item(order);
    $(window).scrollTop(0);
    for(var i=0; i<5; i++){
        $("#cop-choice label:eq("+i+")").removeClass("active");
    }
});

$(document).on('change', '#cop-choice', function(){
    $("#next_item").attr("disabled", true);
    var response = $("input[name='options']:checked").val();
    var data = {};
    var end_time = new Date().getTime();
    
    data['method'] = 'save_response';
    data['order'] = order;
    data['response'] = response;
    data['add_seconds'] = parseInt((end_time - start_time)/1000);
    start_time = new Date().getTime();
    $.ajax({
        url : '/stdnt/solve_itemeach/'+ua_id,
        dataType:"json",
        data : data
    }).done(function(msg){
        //console.log(msg);
        if(msg['status'] == 'success'){
            if(order < num_of_item) $("#next_item").removeAttr("disabled");             
        }
        if(order >= num_of_item){
            finished_flag = true;
        }
        if(finished_flag) {
            $("#submit_responses").removeAttr("disabled");
            $("#submit_responses").show();
        }
    });
    //console.log(this);
});
$(document).on('click', '#submit_responses', function(){
    console.log('submit');
    var data = {};
    data['method'] = 'get_responses';
    $.ajax({
        url : '/stdnt/solve_itemeach/'+ua_id,
        dataType:"json",
        data : data
    }).done(function(msg){
        console.log(msg);
        if(msg['status'] == 'success'){
            //msg['responses'];
            //msg['ci_id'];
            url = 'http://cafalab.com/asp/GradeCartridgeInstance.asp?id='+msg['ci_id']+'&responses='+msg['responses'];
            $.get(url, function (result_data) {
                var correctanswer_str = $($(result_data).find('Keys')[0]).text();
                console.log(result_data);
                console.log(correctanswer_str);
                $.ajax({
                    url : '/stdnt/solve_itemeach/'+ua_id,
                    dataType:"json",
                    data : {'method':'input_correctanswers', 'correctanswers':correctanswer_str}
                }).done(function(final_msg){
                    console.log(final_msg);
                    if(final_msg['status'] == 'success'){
                        $(location).attr('href','/stdnt');
                    }
                });
            });
        }
    });
});
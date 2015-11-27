var test_dat;
    
function set_test_result(num){
    var url = 'http://cafalab.com/asp/TestItemTemplateG.asp?';
    //url += 'Q=What is the value?<br />$@1@^@2@$';
    url += 'Q='+$('#question_input').val();
    url += '&C1='+$('.choices_option:eq(0)').val();
    url += '&C2='+$('.choices_option:eq(1)').val();
    url += '&C3='+$('.choices_option:eq(2)').val();
    url += '&C4='+$('.choices_option:eq(3)').val();
    url += '&C5='+$('.choices_option:eq(4)').val();
    
    for(var i=0; i<12; i++){
        if ($('.option_min:eq('+i+')').val() != "" && $('.option_max:eq('+i+')').val() != ""){
            url += '&PT'+(i+1)+'=N' + '&Min'+(i+1)+'='+$('.option_min:eq('+i+')').val()+'&Max'+(i+1)+'='+$('.option_max:eq('+i+')').val();
            if($('.option_pre:eq('+i+')').val() != ""){
                url += '&Prec'+(i+1)+'='+$('.option_pre:eq('+i+')').val();
            }
        }  
    }
    url += '&S1=' + $('#solution_step_input').val();
    url = encodeURI(url).replace(/\+/g, '%2B').replace(/\#/g,'%23');
    
    console.log(url);
    
    $.get(url, function(data){
        //console.log(data);
        //test_dat = data;
        
        $('.test_prob:eq('+num+') .test_seed').html($(data).find('Seed').text());
        $('.test_prob:eq('+num+') .test_question').html($(data).find('Question').text());
        for(var i=0; i<5; i++){
            $('.test_prob:eq('+num+') .test_choice:eq('+i+')').html($(data).find('Choice:eq('+i+')').text());
        }
        $('.test_prob:eq('+num+') .test_solution').html($(data).find('Solution').text());
        MathJax.Hub.Typeset();
        $('.panel-body div').css('margin-left', '0px');
        
    }).fail(function(msg){
        //test_dat = msg;
        //console.log(msg['responseText']);
        $('.test_prob:eq('+num+') .test_seed').html($(msg['responseText']).find('Seed').text());
        $('.test_prob:eq('+num+') .test_question').html($(msg['responseText']).html());
        for(var i=0; i<5; i++){
            $('.test_prob:eq('+num+') .test_choice:eq('+i+')').html($(msg['responseText']).find('Choice:eq('+i+')').text());
        }
        $('.test_prob:eq('+num+') .test_solution').html($(msg['responseText']).find('Solution').text());
        MathJax.Hub.Typeset();
        $('.panel-body div').css('margin-left', '0px');
    });
}
function click_create_btn(){
    //test_dat = this;
    console.log('start creating');
    set_test_result(0);
    
}
$(document).on('click', '#create_btn', click_create_btn);
function set_percent_data_div(){
    var per_0s = $('.percent_0');
    for(var i=0; i<per_0s.length; i++){
        var per_point = Number($(per_0s[i]).parent().find('.mastery_point').text());
        if( per_point < 25){
            $(per_0s[i]).find('div').css('width', (per_point*4)+'%');
        }
    }
    var per_25s = $('.percent_25');
    for(var i=0; i<per_25s.length; i++){
        var per_point = Number($(per_25s[i]).parent().find('.mastery_point').text());
        if( per_point <= 25){
            $(per_25s[i]).find('div').hide();
        } else if( per_point < 50){
            $(per_25s[i]).find('div').css('width', ((per_point-25)*4)+'%');
        }
    }
    var per_50s = $('.percent_50');
    for(var i=0; i<per_50s.length; i++){
        var per_point = Number($(per_50s[i]).parent().find('.mastery_point').text());
        if( per_point <= 50){
            $(per_50s[i]).find('div').hide();
        } else if( per_point < 75){
            $(per_50s[i]).find('div').css('width', ((per_point-50)*4)+'%');
        }
    }
    var per_75s = $('.percent_75');
    for(var i=0; i<per_75s.length; i++){
        var per_point = Number($(per_75s[i]).parent().find('.mastery_point').text());
        if( per_point <= 75){
            $(per_75s[i]).find('div').hide();
        } else {
            $(per_75s[i]).find('div').css('width', ((per_point-75)*4)+'%');
        }
    }
}
function set_unit_help(){
    /*
    단원 학습을 위해 익혀야 할 성취기준 중에서 

    특별히 강점인 학습요소는 없습니다.
    수학2211, 수학2212에서 강점을 보이고 있습니다. 이러한 자신의 강점을 알고 적극적으로 개발하고 발전하기 바랍니다. 
    
    
    수학2213은 중간 수준이고,
    수학2213은 하 수준이므로 취약점이 되지 않도록 꼼꼼히 복습하는 노력을 기울이기 바랍니다.
    
    
    특별히 취약한 학습요소는 없습니다.
    취약한 학습요소는 수학2213, 수학2213입니다.*/
    //$($('.unit_help')[0]).parent().find('.mastery_point')
    var unit_helps = $('.unit_help');
    for(var i=0; i<unit_helps.length; i++){
        //unit_helps[i]
        var h_standards = [];
        var m_standards = [];
        var l_standards = [];
        var f_standards = [];
        
        var mastery_points = $(unit_helps[i]).parent().find('.mastery_point');
        //var per_points = $($($('.unit_help')[i]).parent().find('.mastery_point')[0]).text();
        for(var j=1; j<mastery_points.length; j++){
            var per_point = Number($(mastery_points[j]).text());
            if(per_point <= 25){
                f_standards.push($(mastery_points[j]).parent().find('.std_name').text());
            } else if(per_point <= 50){
                l_standards.push($(mastery_points[j]).parent().find('.std_name').text());
            } else if(per_point <= 75){
                m_standards.push($(mastery_points[j]).parent().find('.std_name').text());
            } else {
                h_standards.push($(mastery_points[j]).parent().find('.std_name').text());
            }
        }
        var help_str = '단원 학습을 위해 익혀야 할 성취기준 중에서 ';
        if(h_standards.length == 0){
            //help_str += '특별히 강점인 학습요소는 없습니다.';
        } else {
            help_str += h_standards + '에서 강점을 보이고 있습니다. 이러한 자신의 강점을 알고 적극적으로 개발하고 발전하기 바랍니다.';
        }
        if(m_standards.length != 0 && l_standards.length != 0){
            help_str += m_standards + '은 중간 수준이고, ' + l_standards + '은 하 수준이므로 ';
            help_str += '취약점이 되지 않도록 꼼꼼히 복습하는 노력을 기울이기 바랍니다.';
        } else if (m_standards.length == 0 && l_standards.length != 0) {
            help_str +=  l_standards + '은 하 수준이므로 ';
            help_str += '취약점이 되지 않도록 꼼꼼히 복습하는 노력을 기울이기 바랍니다.';
        } else if (m_standards.length != 0 && l_standards.length == 0) {
            help_str +=  m_standards + '은 중간 수준이므로 ';
            help_str += '취약점이 되지 않도록 꼼꼼히 복습하는 노력을 기울이기 바랍니다.';
        } 
        if(f_standards.length == 0){
            help_str += '특별히 취약한 학습요소는 없습니다.';
        } else {
            help_str += '취약한 학습요소는 '+f_standards+'입니다.';
        }
        //'수학2213은 중간 수준이고,'
        //'수학2213은 하 수준이므로 취약점이 되지 않도록 꼼꼼히 복습하는 노력을 기울이기 바랍니다.'
        $(unit_helps[i]).text(help_str);
        
    }
    
}
$(document).ready(function(){
    $('#my_unit_list_name').css('top', $('#my_assess_list_name').position().top+$('#my_assess_list_name').height());
    set_percent_data_div();
    set_unit_help();
});
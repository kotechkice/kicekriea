$(document).on("click", "#add_new_tch", function(){
    $("#add_tch_modal").modal('show');
});
$(document).on("click", "#add_new_tch_btn", function(){
    var data = {};
    data['method'] = 'add_new_tch';
    data['email'] = $("#new_mng_email").val();
    data['firstname'] = $("#new_mng_firstname").val();
    data['lastname'] = $("#new_mng_lastname").val();
    data['comnum'] = $("#new_mng_comnum").val();

    $.ajax({
        url : "/tch/modify_auth/",
        dataType : "json",
        data : data
    }).done(function(msg) {
        //console.log(msg);
        if(msg['status'] == 'success'){
            location.reload();
        }
    });
});

$(document).on('click', "#add_new_class", function(){
    $("#add_class_modal").modal('show');
});
$(document).on('click', "#add_class_btn", function(){
    if($("#new_class_name").val() == ''){
        return false;
    }
    var data = {};
    data['method'] = 'add_new_class';
    data['grade'] = $("#new_grade_name").val();
    data['class'] = $("#new_class_name").val();
    //console.log()
    $.ajax({
        url : "/tch/modify_auth/",
        dataType : "json",
        data : data
    }).done(function(msg) {
        //console.log(msg);
        if(msg['status'] == 'success'){
            location.reload();
        }
    });
});

var changepw_email;
$(document).on("click", ".send_newpw", function(){
    var title_email_ex = "#send_newpw_modal .modal-title .email_section";
    changepw_email = $(this.parentNode.parentNode).find(".email_td").text();
    $(title_email_ex).text(changepw_email);
    $("#send_newpw_modal").modal("show");
    return false;
});
$(document).on("click", "#send_newpw_btn", function(){
    //console.log("enter");
    var input_code = $(this.parentNode.parentNode).find('.input_code').val();
    if(input_code == '{{ input_code }}'){
        //console.log("send");
        var data = {};
        data['method'] = 'send_newpw';
        data['email'] = changepw_email;
        $.ajax({
            url : "/tch/modify_auth/",
            dataType : "json",
            data : data
        }).done(function(msg) {
            //console.log(msg);
            location.reload();
        });
    }
});

var del_email;
$(document).on('click', '.del_auth', function(){
    del_email = $(this.parentNode.parentNode).find(".email_td").text();
    $('#check_del_auth_modal .email_section').text(del_email);
    $("#check_del_auth_modal").modal("show");
    return false;
});
function click_del_auth_btn(){
    var input_code = $('#check_del_auth_modal .input_code').val();
    if(input_code == '{{ input_code }}'){
        //console.log("send");
        $.ajax({
            url : "/tch/modify_auth/",
            dataType : "json",
            data : {
                'method':'del_auth',
                'email' : del_email
            }
        }).done(function(msg) {
            //console.log(msg);
            location.reload();
        });
    }
}
$(document).on('click', '#del_auth_btn', click_del_auth_btn);
//del_auth

var del_email;
$(document).on("click", ".del_tch", function(){
    return false;
});

var class_id = 0;
$(document).on('click','.change_class_info',function(){
    //test_dat = this;
    var parent_tr = $(this).parent().parent();
    class_id =  parent_tr.attr('class_id');
    $('#change_grade_name').val(parent_tr.find('.grade_name').text()).attr("selected", "selected");
    $('#change_class_name').val(parent_tr.find('.class_name').text());
    
    $('#change_class_modal').modal('show');
    return false;
});
function change_class_info(){
    if($("#change_class_name").val() == ''){
        return false;
    }
    //console.log()
    $.ajax({
        url : "/tch/modify_auth/",
        dataType : "json",
        data : {
            'method':'change_class_info',
            'class_id':class_id,
            'grade':$('#change_grade_name').val(),
            'class':$('#change_class_name').val(),
        }
    }).done(function(msg) {
        //console.log(msg);
        if(msg['status'] == 'success'){
            location.reload();
        } else {
            console.log(msg);
        }
    });
}
$(document).on('click','#change_class_btn',change_class_info);

$(document).on('click','.del_class_info',function(){
    //test_dat = this;
    var parent_tr = $(this).parent().parent();
    class_id =  parent_tr.attr('class_id');
    //$('#change_grade_name').val(parent_tr.find('.grade_name').text()).attr("selected", "selected");
    //$('#change_class_name').val(parent_tr.find('.class_name').text());
    $('#class_name_span').text(parent_tr.find('.class_name').text());
    $('#check_del_class_modal').modal('show');
    return false;
});
function del_class(){
    var input_code = $('#check_del_class_modal .input_code').val();
    if(input_code == '{{ input_code }}'){
        $.ajax({
            url : "/tch/modify_auth/",
            dataType : "json",
            data : {
                'method':'del_class',
                'class_id':class_id,
            }
        }).done(function(msg) {
            //console.log(msg);
            if(msg['status'] == 'success'){
                location.reload();
            } else {
                console.log(msg);
            }
        });
    }
}
$(document).on('click', '#del_class_btn', del_class);



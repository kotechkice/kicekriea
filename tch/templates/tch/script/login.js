var test_dat = '';
function do_login(){
    if($("#email").val() =='' || $("#pw").val() == ''){
        return false;
    }
    $.post("/tch/login/", {
            csrfmiddlewaretoken:$.cookie('csrftoken'), 
            email:$("#email").val(), 
            pw : $("#pw").val() 
    }).done(function(data){
        console.log(data);
        //test_dat = data;
        if(data['status'] === "success"){
            $(location).attr('href',data['msg']);
        } else {
            $("#modal .modal-body").html(data['msg']);
            $("#modal").modal('show');
        }
    });
}
$(document).on("click", '#submit', function(){
    do_login();
    return false;
});
$(document).on('keypress', '#pw', function(e){
    //console.log(e);
    if(e.keyCode==13){
        do_login();
    }
});
$(document).on('click', '#find_email_pw_btn', function(){
    $('#email_pw_check_modal').modal('show');
});

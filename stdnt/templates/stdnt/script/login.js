var test_dat = '';
function do_login(){
    if($("#email").val() =='' || $("#pw").val() == ''){
        return false;
    }
    $.post("/stdnt/login/", {
            csrfmiddlewaretoken:$.cookie('csrftoken'), 
            email:$("#email").val(), 
            pw : $("#pw").val() 
    }).done(function(data){
        console.log(data);
        //test_dat = data;
        if(data['status'] === "success"){
            $(location).attr('href','/stdnt');
        } else {
            $("#modal .modal-body").html(data['msg']);
            $("#modal").modal('show');
        }
    });
}
$(document).on("click", '#submit', function(){
    do_login();
});
$(document).on('keypress', '#pw', function(e){
    //console.log(e);
    if(e.keyCode==13){
        do_login();
    }
});

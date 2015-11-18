function set_footer(){
    $('footer').css('top', $('#wrap_lists').position().top+$('#wrap_lists').height()+100);
}
$(document).ready(function(){
   set_footer();
});
$(document).on('change', ':radio[name="assess_type"]:checked', function(){
    console.log('change');
    //$(':radio[name="assess_type"]:checked').val();
    $('#wrap_lists table tbody tr').toggle();
    set_footer();
});

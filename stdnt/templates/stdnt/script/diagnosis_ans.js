function set_footer(){
    $('footer').css('top', $('#wrap_lists').position().top + $('#wrap_lists').height()+50);
    //$('#wrap_lists').position().top
    //$('#wrap_lists').height()
}

$(document).ready(function(){
    //$('.table')
    
    //$($('.table td')[1]).text()
    set_footer();
    
    var tds = $('.table td');
    for(var i=0; i<tds.length; i++){
        console.log($(tds[i]).text());
        switch($(tds[i]).text()){
            case 'A':  $(tds[i]).text('1'); break;
            case 'B':  $(tds[i]).text('2'); break;
            case 'C':  $(tds[i]).text('3'); break;
            case 'D':  $(tds[i]).text('4'); break;
            case 'E':  $(tds[i]).text('5'); break;
        }
    } 
});

//tch/assess_preview/?title=함수&itemids=1900,1901

window.params = function(){
    var params = {};
    var param_array = window.location.href.split('?')[1].split('&');
    for(var i in param_array){
        x = param_array[i].split('=');
        params[x[0]] = x[1];
    }
    return params;
}();

function ready_func(){
    //console.log($_GET('title'));
    //console.log($_GET('itemids'));
    console.log(window.params.title);
    console.log(window.params.itemids);
    
    
}
$(document).ready(ready_func);

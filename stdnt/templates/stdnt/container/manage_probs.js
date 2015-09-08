function unEntity(str){
    return str.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
}
function getitem_json_to_html(prob_json){
    if('question' in prob_json){
            $("#cop-question").html(unEntity(prob_json['question']));
    }
    if('choice' in prob_json){
        for(var i=1; i<=5; i++){
            $("#choice-"+i).text(unEntity(prob_json['choice'][i-1]));
        }
    }
}
function gradeitem_json_to_html(prob_json){
    //console.log(prob_json);
    if('answer' in prob_json){
        $("#cop-answer-contents").html(unEntity(prob_json['answer_text']));
        //$("#cop-answer-contents").html($('#choice-'+prob_json['answer']).html());
    }
    if('solution' in prob_json){
        $("#cop-solution-contents").html(unEntity(prob_json['solution']));
    }
}

function getci_to_json(xml_data){
    var json = {};
    xml_data = $(xml_data).find('Item');
    for(var index=1; index<=xml_data.length; index++){
        json[index] = {
            'ItemID':$($(xml_data[index-1]).find('ItemID')[0]).text(),
            'Seed':$($(xml_data[index-1]).find('Seed')[0]).text(),
            'NumChoices':$($(xml_data[index-1]).find('NumChoices')[0]).text(),
            'Permutation':$($(xml_data[index-1]).find('Permutation')[0]).text(),
        };
    }
    return json;
}
function getitem_to_json(xml_data){
    xml_data = $(xml_data).find('Item')[0];
    var prob_dict = {};       
    var prob_tag = ["seed", "question", "choice"];
    for(index in prob_tag){
        if(prob_tag[index] == "choice"){
            prob_dict['choice'] = [];
            for(var j=0; j<$(xml_data).find(">choice").length; j++){
                prob_dict['choice'].push($($(xml_data).find(">choice:eq("+j+")")[0]).text());
            }
        }  else if (prob_tag[index] == "seed") {
            seed = $($(xml_data).find(">seed")).text();
        }  else {
            prob_dict[prob_tag[index]] = $($(xml_data).find(">"+prob_tag[index])).text();
        }
    }
    return prob_dict;
}
function change_choices_as_permutation_str(json_data, permutation_str){
    var origin_choice_data = [];
    for(var index=0; index<5; index++){
        origin_choice_data.push(json_data['choice'][index]);
    }
    //console.log(origin_choice_data);
    for(var index=0; index<5; index++){
        json_data['choice'][index] = origin_choice_data[Number(permutation_str[index])-1];
    }
    return json_data;
}

function gradeitem_to_json(xml_data){
    xml_data = $(xml_data).find('Item')[0];
    var prob_dict = {};       
    var prob_tag = ["answer", "solution"];
    for(index in prob_tag){
        if (prob_tag[index] == "answer") {//A:1, B:2, C:3, D:4, E:5
            ans = $(xml_data).find(">answer").text();
            //prob_dict["answer"] = ans;
            prob_dict["answer"] = $(xml_data).find(">answer").text().charCodeAt(0) - 'A'.charCodeAt(0) + 1;
            prob_dict["answer_text"] = $($(xml_data).find(">choice:eq("+(prob_dict["answer"]-1)+")")[0]).text();
        } else if(prob_tag[index] == "solution"){
            prob_dict[prob_tag[index]] = $($(xml_data).find(">"+prob_tag[index])).text();
            prob_dict['solutions'] = [];
            for(var j=0; j<$(xml_data).find(">solution").length; j++ ){
                prob_dict['solutions'].push($($(xml_data).find(">solution:eq("+j+")")[0]).text());
            }
        }else {
            prob_dict[prob_tag[index]] = $($(xml_data).find(">"+prob_tag[index])).text();
        }
    }
    return prob_dict;
}
function getiteminfo_to_json(xml_data){
    xml_data = $(xml_data).find('Item')[0];
    var prob_dict = {};       
    var prob_tag = ["ItemID", "ModuleID", "Category1", "Difficulty", "Skill", "AnswerType", "Points", "Ability", "Description", "Exposure", "Correct", "Complexity", "Created", "Institute", "ChoicesPerLine", "Height"];
    for(index in prob_tag){
        prob_dict[prob_tag[index]] = $($(xml_data).find(">"+prob_tag[index])).text();
    }
    return prob_dict;
}

function change_ccss_skill_string_from_cafa(skill_str){
    var ccss_str = skill_str.split('.');
    if(ccss_str[0] == "0"){
        ccss_str[0] = "K";
    } else if(isNaN(ccss_str[0])){
        ccss_str[0] = 'HS'+ccss_str[0];
    }
    ccss_str[2] = alphabet[Number(ccss_str[2])-1];
    if(ccss_str[3][2] == "0"){
        ccss_str[3] = ccss_str[3].slice(0,2);
    } else {
        ccss_str[3] = ccss_str[3].slice(0,2) + '.' + ccss_str[3][2];
    }
    if(ccss_str[3][0] == "0"){
        ccss_str[3] = ccss_str[3].slice(1);
    }
    ccss_str = 'CCSS.Math.Content.'+ccss_str.join('.');
    return ccss_str;
}

function change_ccss_grade_full_str(abb_str){
    if(!isNaN(abb_str)){
        if(Number(abb_str)==0){
            return 'Kindergarten';
        }
        return "Grade "+abb_str;
    } else {
        switch(abb_str){
            case 'K':
                return 'Kindergarten';
            case 'HSN':
            case 'N':
                return 'High School: Number and Quantity';
            case 'HSA':
            case 'A':
                return 'High School: Algebra';
            case 'HSF':
            case 'F':
                return 'High School: Functions';
            case 'HSM':
            case 'M':
                return 'High School: Modeling';
            case 'HSG':
            case 'G':
                return 'High School: Geometry';
            case 'HSS':
            case 'S':
                return 'High School: Statistics & Probability';
        }
    }
    return abb_str;
}

function set_oo(){
    $("#cop-btn-submit").hide();
    
    $('#cop-express-correct').css('color','blue');
    $('#cop-express-correct').css('font-size','170px');
    $('#cop-express-correct').html("O");
    $("#cop-express-correct").show();
    //$("#cop-express-correct").offset({"top":$("#cop-choice").offset().top});
    
    $("#cop-answer").show();
    $("#cop-complete-btns").show();
    
    $("#cop-express-correct").offset({"top":$("#cop-choice").offset().top + $("#cop-choice").height()/2 - $("#cop-express-correct").height()/2});
}
function set_xx(){
    $("#cop-btn-submit").hide();
    
    //$('#cop-express-correct').css('color','red');
    $('#cop-express-correct').css('color','gray');
    $('#cop-express-correct').css('font-size','50px');
    //$('#cop-express-correct').text("X");
    $('#cop-express-correct').html("Oops!<br />Try again");
    $("#cop-express-correct").show();
    
    $("#cop-btn-showans").show();
    
    $("#cop-express-correct").offset({"top":$("#cop-choice").offset().top + $("#cop-choice").height()/2 - $("#cop-express-correct").height()/2});
}
function reset(){
    $("#choice-area").hide();
    $("#cop-express-correct").hide();
    $("#cop-btn-submit").hide();
    $("#cop-img").hide();
    $("#cop-btn-showans").hide();
    $("#cop-answer").hide();
    $("#cop-solution").hide();
    $("#cop-btn-showsolution").show();
    $("#cop-complete-btns").hide();
    $("#cop-btn-showsolution").text("해설보기");
}

$(document).on("click", "#cop-btn-showsolution", function(){ 
    // click the "show solution" button
    if($("#cop-btn-showsolution").text() == "해설보기") {
        $("#cop-btn-showsolution").text("해설닫기");
        $("#cop-solution").show();
    } else {
        $("#cop-btn-showsolution").text("해설보기");
        $("#cop-solution").hide();
    }
    $("#cop-express-correct").offset({"top":$("#cop-choice").offset().top + $("#cop-choice").height()/2 - $("#cop-express-correct").height()/2});
});

$(document).on("click", "#agree_btn", function(){
    $("#showSolutionModal").modal('hide');
    
    $("#cop-btn-showsolution").text("해설닫기");
    $("#cop-solution").show();
    
    $("#cop-express-correct").offset({"top":$("#cop-choice").offset().top + $("#cop-choice").height()/2 - $("#cop-express-correct").height()/2});
});

$(document).on("click", "#cop-btn-showans", function(){
    // click the "show answer" button
    $("#cop-btn-showans").hide();
    $("#cop-answer").show();
    $("#cop-complete-btns").show();
    
    $("#cop-express-correct").offset({"top":$("#cop-choice").offset().top + $("#cop-choice").height()/2 - $("#cop-express-correct").height()/2});
});

if (!Object.keys) {
  Object.keys = function(obj) {
    var keys = [];
    for (var i in obj) {
      if (obj.hasOwnProperty(i)) keys.push(i);
    }
    return keys;
  };
}
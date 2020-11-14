// The values sent to the server at the end.
// These values are the center values.
var XScore = 250;
var YScore = 270;
//Json config
var jsonConfig;


/* -----Functions called from HTML----- */

function startQuiz() {
    $("#intro-text").hide();
    $("#question-container").show();
    loadQuestions()
}





/* -----Private functions----- */

function loadQuestions() {

}

//This function is called from main.html, sets the var jsonConfig to valid json.
// replaces quote symbol from server to actual quotes
function loadJson(jsonData){
    let symbols = (jsonData.match(new RegExp("&#39;", "g")) || []).length;
    for (let i = 0; i < symbols; i++) {
        jsonData = jsonData.replace("&#39;", "\"");
    }
    jsonConfig = jsonData
}



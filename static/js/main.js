// The values sent to the server at the end.
// These values are the center values.
var XScore = 250;
var YScore = 270;

//Json config
var jsonConfig;

// Current question.
var currentQuestionCounter = 0;

// Answer list array. At the start it 
// is filled with 0 of how many questions
// 0 = neutral. 1 = agree. 2 = strongly agree.
//-1 = disagree. -2 = strongly disagree.
var answerList = [];

/* -----Functions called from HTML----- */

function startQuiz() {
    $("#intro-text").hide();
    $("#question-container").show();
    loadQuestions();
}

function nextQuestion() {
    currentQuestionCounter++;
    if(currentQuestionCounter > jsonConfig.question_list.length - 1) {
        currentQuestionCounter = jsonConfig.question_list.length - 1;
        return 0;
    } 

    $("#question-title").text(jsonConfig.question_list[currentQuestionCounter].question_text);
    $("#question-counter").text(currentQuestionCounter + 1);
    setRadioAnswer(answerList[currentQuestionCounter]);
}

function previousQuestion() {
    currentQuestionCounter--;
    if(currentQuestionCounter < 0) {
        currentQuestionCounter = 0;
        return 0;
    }

    $("#question-title").text(jsonConfig.question_list[currentQuestionCounter].question_text);
    $("#question-counter").text(currentQuestionCounter + 1);

    setRadioAnswer(answerList[currentQuestionCounter]);
}

$('input:radio[name="question-radio"]').change(
    function(){
        answerList[currentQuestionCounter] = $('input[name="question-radio"]:checked').val();
    });

/* -----Private functions----- */

function loadQuestions() {
    $("#question-title").text(jsonConfig.question_list[0].question_text);
    $("#question-counter").text("1");
    $("#question-counter-max").text(jsonConfig.question_list.length);

    for(let i = 0; i < jsonConfig.question_list.length; i++) {
        answerList.push(0);
    } 
}

function setRadioAnswer(ans) {
    $('[name="question-radio"]').prop('checked', false);
    if(typeof(ans) != "number") {
        ans = parseInt(ans);
    }
    switch(ans) {
        case -2:
            $('#SD').prop('checked', true);
            break;
        case -1:
            $('#D').prop('checked', true);
            break;
        case 0:
            $('#neutral').prop('checked', true);
            break;
        case 1:
            $('#A').prop('checked', true);
            break;
        case 2:
            console.log("hurrr");
            $('#SA').prop('checked', true);
            break;
    }
}

// This function is called from main.html, sets the var jsonConfig to valid json.
// replaces quote symbol from server to actual quotes
function loadJson(jsonData){
    //let symbols = (jsonData.match(new RegExp("&#39;", "g")) || []).length;
    jsonData = jsonData.replaceAll("&#39;", "\"");
    console.log(jsonData);
    jsonConfig = JSON.parse(jsonData);
}



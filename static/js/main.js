// The values sent to the server at the end.
// These values are the center values.
var XScore = 250;
var YScore = 270;

var jsonConfig;

var jsonQuestionList;

var currentQuestionCounter = 0;

// Map that stores the users answers.
// The map key is just the index on the json array
// values are: ans: -2 up to 2 (strongly disagree upto strongly agree. 0 is neutral).
// Second value is type of question either: economic(x on axis) or social(y on axis)
// third value is sway. Sway is if they agree they go towards the sway.
// sway should be left/right for economic and auth/lib for social.
// behaviour is undefined if that is not met.
var answerMap = new Map();

/* -----Functions called from HTML----- */

function startQuiz() {
    $("#intro-text").hide();
    $("#question-container").show();
    loadQuestions();
}

function nextQuestion() {
    currentQuestionCounter++;
    if (currentQuestionCounter > jsonQuestionList.length - 1) {
        currentQuestionCounter = jsonQuestionList.length - 1;
        return 0;
    }

    if (currentQuestionCounter >= jsonQuestionList.length - 1) {
        $("#next-btn").hide();
        $("#submit-btn").show();
    }

    $("#question-title").text(jsonQuestionList[currentQuestionCounter].question_text);
    $("#question-counter").text(currentQuestionCounter + 1);
    setRadioAnswer(answerMap.get(currentQuestionCounter).ans);
}

function previousQuestion() {
    if (currentQuestionCounter == jsonQuestionList.length - 1) {
        $("#next-btn").show();
        $("#submit-btn").hide();
    }

    currentQuestionCounter--;
    if (currentQuestionCounter < 0) {
        currentQuestionCounter = 0;
        return 0;
    }

    $("#question-title").text(jsonQuestionList[currentQuestionCounter].question_text);
    $("#question-counter").text(currentQuestionCounter + 1);
    setRadioAnswer(answerMap.get(currentQuestionCounter).ans);
}

function submitAnswer() {
    //stop the user messing this up
    $("button").attr('disabled', 'disabled');
    $("input").attr('disabled', 'disabled');
    setRadioAnswer(0);

    console.log(answerMap);
    for (let i = 0; i < answerMap.size; i++) {
        if (answerMap.get(i).type == "social") {
            switch (parseInt(answerMap.get(i).ans)) {
                case -2:
                    if (answerMap.get(i).sway == "auth") {
                        YScore += jsonConfig.big_y_movement;
                    } else {
                        YScore -= jsonConfig.big_y_movement;
                    }
                    break;
                case -1:
                    if (answerMap.get(i).sway == "auth") {
                        YScore += jsonConfig.small_y_movement;
                    } else {
                        YScore -= jsonConfig.small_y_movement;
                    }
                    break;
                case 1:
                    if (answerMap.get(i).sway == "auth") {
                        YScore -= jsonConfig.big_y_movement;
                    } else {
                        YScore += jsonConfig.big_y_movement;
                    }
                    break;
                case 2:
                    if (answerMap.get(i).sway == "auth") {
                        YScore -= jsonConfig.big_y_movement;
                    } else {
                        YScore += jsonConfig.big_y_movement;
                    }
                    break;
            }
        } else if (answerMap.get(i).type == "economic") {
            switch (parseInt(answerMap.get(i).ans)) {
                case -2:
                    if (answerMap.get(i).sway == "left") {
                        XScore += jsonConfig.big_y_movement;
                    } else {
                        XScore -= jsonConfig.big_y_movement;
                    }
                    break;
                case -1:
                    if (answerMap.get(i).sway == "left") {
                        XScore += jsonConfig.small_y_movement;
                    } else {
                        XScore -= jsonConfig.small_y_movement;
                    }
                    break;
                case 1:
                    if (answerMap.get(i).sway == "left") {
                        XScore -= jsonConfig.big_y_movement;
                    } else {
                        XScore += jsonConfig.big_y_movement;
                    }
                    break;
                case 2:
                    if (answerMap.get(i).sway == "left") {
                        XScore -= jsonConfig.big_y_movement;
                    } else {
                        XScore += jsonConfig.big_y_movement;
                    }
                    break;
            }
        }
    }
    window.location.href = "/finish-quiz?x=" + XScore + "&y=" + YScore;
}

$('input:radio[name="question-radio"]').change(
    function () {
        answerMap.get(currentQuestionCounter).ans = $('input[name="question-radio"]:checked').val();
    });

/* -----Private functions----- */

function loadQuestions() {
    $("#question-title").text(jsonQuestionList[0].question_text);
    $("#question-counter").text("1");
    $("#question-counter-max").text(jsonQuestionList.length);

    for (let i = 0; i < jsonQuestionList.length; i++) {
        answerMap.set(i, {
            ans: 0,
            type: jsonQuestionList[i].type,
            sway: jsonQuestionList[i].sway
        })
    }
}

function setRadioAnswer(ans) {
    $('[name="question-radio"]').prop('checked', false);
    if (typeof (ans) != "number") {
        ans = parseInt(ans);
    }
    switch (ans) {
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
            $('#SA').prop('checked', true);
            break;
    }
}

// This function is called from main.html, sets the var jsonConfig to valid json.
// replaces quote symbol from server to actual quotes
function loadJson(jsonData, questionList) {
    jsonData = jsonData.replaceAll("&#39;", "\"");
    questionList = questionList.replaceAll("&#39;", "\"");
    jsonConfig = JSON.parse(jsonData);
    jsonQuestionList = JSON.parse(questionList);
    // formats strings
    for (let i = 0; i < jsonQuestionList.length; i++) {
        jsonQuestionList[i].question_text = jsonQuestionList[i].question_text.replaceAll("&#34;", "\"")
        jsonQuestionList[i].question_text = jsonQuestionList[i].question_text.replaceAll("&#39;", "'")
    }
}
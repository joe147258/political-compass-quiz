const EconomicConst = ['left', 'right']
const SocialConst = ['auth', 'lib']

var WorkingPos = -1;

$('#type_select').change(function () {
    if ($('#type_select').val() == 'social') {
        $('#sway1').val('auth');
        $('#sway1').text('Auth');
        $('#sway2').val('lib');
        $('#sway2').text('Lib');
    } else {
        $('#sway1').val('left');
        $('#sway1').text('Left');
        $('#sway2').val('right');
        $('#sway2').text('Right');
    }
})

$('#edit_type_select').change(function () {
    if ($('#edit_type_select').val() == 'social') {
        $('#edit_sway1').val('auth');
        $('#edit_sway1').text('Auth');
        $('#edit_sway2').val('lib');
        $('#edit_sway2').text('Lib');
    } else {
        $('#edit_sway1').val('left');
        $('#edit_sway1').text('Left');
        $('#edit_sway2').val('right');
        $('#edit_sway2').text('Right');
    }
})

$("#new_ques").submit(function (e) {
    e.preventDefault();
    let form = $(this);
    $.ajax({
        type: "POST",
        url: "/submit-question",
        data: form.serialize(),
        success: function (data) {
            $("table").load(" table > *");
            $('#new_ques').trigger("reset");
            $('#add-modal').modal('hide');
            $("#type_select").val($("#type_select option:first").val());
            $('#sway1').val('left');
            $('#sway1').text('Left');
            $('#sway2').val('right');
            $('#sway2').text('Right');
        },
        error: function (data) {
            alert("Something went wrong!");
        }
    });
});

function deleteQuestion(pos) {
    $.ajax({
        type: "POST",
        url: "/delete-question",
        data: {
            "pos": pos
        },
        success: function (data) {
            $("table").load(" table > *");
            $('#new_ques').trigger("reset");
            $("#undo-amount").text(data.undo_amount)
        },
        error: function (data) {
            showAlertMessage("Unable to delete.");
        }
    });
}

function editQuestion(pos) {
    $('#edit-modal').modal('show');
    $.ajax({
        type: "GET",
        url: "/get-question-info?pos=" + pos,
        success: function (data) {
            $("#edit_ques_text").val(data.question_text)
            setTypeAndSway(data.type, data.sway)
            WorkingPos = pos;
        },
        error: function (data) {
            alert("Something went wrong!");
        }
    });
    

}

function undo() {
    $.ajax({
        type: "POST",
        url: "/undo",
        success: function (data) {
            $("table").load(" table > *");  
            $("#undo-amount").text(data.undo_amount)
            $("#redo-amount").text(data.redo_amount)
        },
        error: function () {
            showAlertMessage("Nothing to undo.");
        }
    });
}

function redo() {
    console.log("jere");
    $.ajax({
        type: "POST",
        url: "/redo",
        success: function (data) {
            $("table").load(" table > *");
            $("#undo-amount").text(data.undo_amount)  
            $("#redo-amount").text(data.redo_amount)
        },
        error: function () {
            showAlertMessage("Nothing to redo.");
        }
    });
}

$("#edit_ques").submit(function (e) {
    e.preventDefault();
    let form = $(this);
    let requestForm = form.serializeArray();
    requestForm.push({"name": "pos", "value": WorkingPos})
    requestForm = serializeData(requestForm);
    $.ajax({
        type: "POST",
        url: "/edit-question",
        data: requestForm,
        success: function (data) {
            $("table").load(" table > *");
            $('#edit_ques').trigger("reset");
            $('#edit-modal').modal('hide');
            $("#undo-amount").text(data.undo_amount)
        },
        error: function (data) {
            alert("Something went wrong!");
        }
    });
});

function setTypeAndSway(type, sway) {
    if(type === 'economic') {
        $('#edit_sway1').val('left');
        $('#edit_sway1').text('Left');
        $('#edit_sway2').val('right');
        $('#edit_sway2').text('Right');
        if(!EconomicConst.includes(sway)) {
            return 0;
        } else {
            $("#edit_type_select").val($("#edit_type_select option:first").val());
            if(sway == "left") {
                $("#edit_sway_select").val($("#edit_sway_select option:first").val());
            } else {
                $("#edit_sway_select").val($("#edit_sway_select option:eq(1)").val());
            }
        }
    } else if(type === 'social') {
        $('#edit_sway1').val('auth');
        $('#edit_sway1').text('Auth');
        $('#edit_sway2').val('lib');
        $('#edit_sway2').text('Lib');
        if(!SocialConst.includes(sway)) {
            return 0;
        } else {
            $("#edit_type_select").val($("#edit_type_select option:eq(1)").val());
            if(sway == "auth") {
                $("#edit_sway_select").val($("#edit_sway_select option:first").val());
            } else {
                $("#edit_sway_select").val($("#edit_sway_select option:eq(1)").val());
            }
        }
    } else {
        return 0;
    }
}

function serializeData(formArray) {
    //serialize data function
    var returnArray = {};
    for (var i = 0; i < formArray.length; i++){
        returnArray[formArray[i]['name']] = formArray[i]['value'];
    }
    return returnArray;
}

async function showAlertMessage(text){
    $("#alert-message").text(text);
    $("#alert-message").css('visibility', 'visible');
    setTimeout(function() { $("#alert-message").css('visibility', 'hidden'); }, 2000);

}
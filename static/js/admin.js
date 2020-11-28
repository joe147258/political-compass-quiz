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

$("#new_ques").submit(function (e) {
    e.preventDefault();
    var form = $(this);
    $.ajax({
        type: "POST",
        url: "/submit-question",
        data: form.serialize(),
        success: function (data) {
            $("table").load(" table > *");
            $('#new_ques').trigger("reset");
            $('#form-modal').modal('hide');
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
        },
        error: function (data) {
            alert("Something went wrong!");
        }
    });
}
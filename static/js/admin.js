$('#type_select').change(function(){

    if($('#type_select').val() == 'social') {
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

$("#new_ques").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');
    
    $.ajax({
           type: "POST",
           url: "/submit-question",
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
               alert(data.success); // show response from the php script.
           }
         });

    
});
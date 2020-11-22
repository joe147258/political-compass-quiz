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
    e.preventDefault(); 
    var form = $(this);
    $.ajax({
           type: "POST",
           url: "/submit-question",
           data: form.serialize(), 
           success: function(data)
           {
               alert(data.success); 
               $("table").load(" table > *");
           }
         });
});
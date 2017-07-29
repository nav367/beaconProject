$(document).ready(function() {
      var date_input=$('input[name="date"]'); //our date input has the name "date"

      var options={
        format: 'mm/dd/yyyy',
        todayHighlight: true,
        autoclose: true,
      };
      date_input.datepicker(options);

      $('#date-form').submit(function(event){
           var date = $('#date').val();
            event.preventDefault();
        $.ajax({
            type: 'GET',
            url: '/app/get-meetings',
            data: {date:date},
            success: function(response) {

                $("#meeting-details").html(response);
            }
        });
      })
})
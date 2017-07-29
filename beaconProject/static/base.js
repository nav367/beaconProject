$(document).ready(function() {

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
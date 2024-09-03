$('#send-button').on('click', function() {
    var humanMessage = $('#humanMessage').val();
    console.log("to send:" + humanMessage)

    $('#chtbox').append(`
    <li class="repaly">
      <p>`+ humanMessage +`</p>
      
    </li>
  `);
  
    $.ajax({
      type: 'POST',
      url: '/chatx',
      contentType: 'application/json', // Add this line
      data: JSON.stringify({ message: humanMessage }), // Convert the object to a JSON string
    
      success: function(data) {
        console.log(data);
        $('#chtbox').append(`
        <li class="sender">
          <p>`+ data.message +`</p>
          
        </li>
      `);
      },
      error: function(xhr, status, error) {
        console.error(error);
      }
    });

    

    $('.modal-body').animate({ scrollTop: $('.modal-body')[0].scrollHeight }, 500);


console.log('done');
});

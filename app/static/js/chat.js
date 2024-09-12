$(document).ready(function() {
  // prevent default form submission on enter key press
  $('#myForm').submit(function(event) {
      event.preventDefault();
  });

  // clear input box and trigger send-button event on enter key press
  $('#humanMessage').keypress(function(event) {
      if (event.key === 'Enter') {
          $('#send-button').click();
          $('#humanMessage').val('');
          $('#humanMessage').focus();
      }
  });

  $('#send-button').on('click', function() {
      var humanMessage = $('#humanMessage').val();
      console.log("to send:" + humanMessage)
      $('#humanMessage').val('');
      $('#humanMessage').focus();
      $('#chtbox').append(`
        <li class="repaly">
          <p>`+ humanMessage +`</p>
          
        </li>
      `);

      $('#typingli').appendTo('#chtbox');
      $('#typingli').show();
      $.ajax({
        type: 'POST',
        url: '/chatx',
        contentType: 'application/json', // Add this line
        data: JSON.stringify({ message: humanMessage }), // Convert the object to a JSON string
      
        success: function(data) {
          console.log(data);
          $('#typingli').hide();
          $('#chtbox').append(`
          <li class="sender">
            <p>`+ data.message +` &nbsp;&nbsp;</p>
            
          </li>
        `);
        $('.modal-body').animate({ scrollTop: $('.modal-body')[0].scrollHeight }, 500);
        },
        error: function(xhr, status, error) {
          console.error(error);
        }
      });

      

      $('.modal-body').animate({ scrollTop: $('.modal-body')[0].scrollHeight }, 500);


  console.log('done');
  });
  var typingText = $('#typing-text');
  var dots = 0;

  setInterval(function() {
    if (dots === 5) {
      typingText.text('Chesa is typing something');
      dots = 0;
    } else {
      typingText.text(typingText.text() + '.');
      dots++;
    }
  }, 1000); // 1000 milliseconds = 1 second
    
});



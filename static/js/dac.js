$(document).ready(function() {


	$(":file").filestyle({buttonBefore: true});


    $('#dac').on('submit', function(event){

        event.preventDefault();

        if ($('#changeAvatarButton').hasClass('disabled')) {
            return;
        }

        var formData = new FormData($(this)[0]);

        $.ajax({
                url: '/avatar/',
                type: 'POST',
                data: formData,
                beforeSend: function( jqXHR ){
                    $('#changeAvatarButton').addClass('disabled');
                },
                complete: function(){
                    $('#changeAvatarButton').removeClass('disabled');
                },
                success: function(data, textStatus, jqXHR){
                    console.log("Status: "+textStatus+" Data: "+data);
                    $('.g-recaptcha').remove();
                    $('#alertMessage').remove();
                    $('#alertContainer').html("<div id='alertMessage' class='alert alert-success alert-dismissible' role='alert'>" +
                        "<button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>" +
                        "&times;</span></button>Avatar Successfully Changed.</div>");

                    $('#resultMessage').remove();
                    $('#resultContainer').html("<div id='resultMessage'><h4>Response:</h4><pre>"+data+"</pre></div>");

                },
                error: function(data, textStatus, errorThrown) {
                    console.log("Status: "+textStatus+" Data: "+data.responseText);
                    $('#resultMessage').remove();
                    $('#alertMessage').remove();
                    $('#alertContainer').html("<div id='alertMessage' class='alert alert-danger alert-dismissible' role='alert'>" +
                        "<button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>" +
                        "&times;</span></button> Error: "+data.responseText+"</div>");

                },
                cache: false,
                contentType: false,
                processData: false
        });

        return false;

    });
    
    $('.resetButton').click(function() {
        $('#dac')[0].reset();
        $('#resultMessage').remove();
        $('#alertMessage').remove();
    });
    
});

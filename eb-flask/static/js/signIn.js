$(function(){
	$('#btnSignIn').click(function(){
		console.log("This is working so far");
		$.ajax({
			url: '/validateLogin',
			type: 'POST',
			data: $('form').serialize(),
			success: function(response){
                var parsedData = JSON.parse(response);

                if (parsedData.message.includes("success")) {
                    location.href = "/showUserNavPage"
                } else {
                    location.href = "/showErrorPage"
                }
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
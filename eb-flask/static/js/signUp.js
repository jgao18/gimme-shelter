$(function(){
	$('#btnSignUp').click(function(){
		console.log("This is working so far");
		$.ajax({
			url: '/signUp',
			type: 'POST',
			data: $('form').serialize(),
			success: function(response){
                console.log("success");
                var parsedData = JSON.parse(response);
                console.log(parsedData);
                var firstName = parsedData.firstName
                var lastName = parsedData.lastName
                var username = parsedData.username
                if (parsedData.message.includes("missing fields")) {
                    alert("You haven't filled out all of the fields!");
                } else if(parsedData.message.includes("Username Already Exists")) {
                    alert("Sorry, that username is already taken!");
                } else {
                    alert("You have successfully registered! Log in using your username and password in the top right corner");
                }
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
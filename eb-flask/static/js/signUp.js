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
                } else {
                    alert("You have successfully registered!");
                    var c = "username=" + username + ";" + "firstName=" + firstName + ";" + "lastName=" + lastName + ";"
                    document.cookie = "username=" + username + ";" + "firstName=" + firstName + ";" + "lastName=" + lastName + ";";
                    alert(c);
                    location.href = "/showUserNavPage";
                }
				console.log(response);
			},
			error: function(error){
                console.log("failure");
				console.log(error);
			}
		});
	});
});

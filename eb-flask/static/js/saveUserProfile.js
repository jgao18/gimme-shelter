$(function(){
	$('#btnSaveProfile').click(function(){
		console.log("This is working so far");
		$.ajax({
			url: '/saveUserProfile',
			type: 'POST',
			data: $('form').serialize(),
			success: function(response){
                
                var parsedData = JSON.parse(response);
 
                if (parsedData.message.includes("success")) {
                    alert("Profile successfully saved!");
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
$(function(){
	$('#btnReserve').click(function(){
		console.log("This is working so far");
		$.ajax({
			url: '/reserve',
			type: 'POST',
			data: $('form').serialize(),
			success: function(response){
                var parsedData = JSON.parse(response);

                if(parsedData.message.includes("Resident Already Registered")) {
                    alert("You're already registered for a shelter!");
                } else {
                    alert("You have successfully registered!");
                    location.href = "/";
                }
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
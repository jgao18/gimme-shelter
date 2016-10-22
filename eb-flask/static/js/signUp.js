// test
$(function(){
	$('#btnSignUp').click(function(){
		console.log("This is working so far");
		$.ajax({
			url: '/signUp',
			type: 'POST',
			data: $('form').serialize(),
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log("This is NOT NOT NOT working so far");
				console.log(error);
			}
		});
	});
});

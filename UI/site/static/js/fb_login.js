FB.getLoginStatus(function(response) {
	statusChangeCallback(response);
});

process.stdout.write(response)


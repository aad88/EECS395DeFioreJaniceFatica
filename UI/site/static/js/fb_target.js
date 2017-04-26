function FBUserFriendList() {
	console.log("Getting login status");
	FB.getLoginStatus(function (response) {
		if (response.status === 'connected') {
			console.log("Logged in. Attempting friend call");
			FB.api(
				'/me/friends',
				function (response) {
					console.log("Got our response");
					if (response && !response.error) {
						console.log("List retrieved successfuly");
						console.log(response.data);
						
						var data_length = response.data.length;
						if (data_length > 0) {
							document.getElementById('friend_text').innerHTML = 'You are able to search for the following friends:'
							for (var index = 0; index < data_length; index++) {
								document.getElementById('friend_text').innerHTML += '\n' + response.data[index]
							}
						}
						else {
							document.getElementById('friend_text').innerHTML = 'Sorry, no friends of yours are available for search using this feature.';
						}
					}
					else {
						console.log(response.error.message);
					}
				}
			);
		}
	});
}


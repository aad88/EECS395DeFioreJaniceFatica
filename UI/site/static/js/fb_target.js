function FBUserFriendList(access_token) {
	FB.api(
		'/me/friends',
		{
			access_token: access_token
		},
		function (response2) {
			if (response2 && !response2.error) {
				var data_length = response2.data.length;
				if (data_length > 0) {
					document.getElementById('friend_text').innerHTML = 'You are able to search for the following friends:'
					for (var index = 0; index < data_length; index++) {
						document.getElementById('friend_text').innerHTML += '\n' + response2.data[index]
					}
				}
				else {
					document.getElementById('friend_text').innerHTML = 'Sorry, no friends of yours are available for search using this feature.';
				}
			}
			else {
				console.log(response2.error.message);
			}
		}
	);
}


function FBUserFriendList(access_token) {
	FB.api(
		'/me/friends',
		{
			access_token: access_token
		},
		function (response) {
			if (response && !response.error) {
				var data_length = response.data.length;
				if (data_length > 0) {
					document.getElementById('friend_text').innerHTML = 'You are able to search for the following friends:'
					for (var index = 0; index < data_length; index++) {
						document.getElementById('friend_text').innerHTML += '<br> - ' + response.data[index].name
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

function GetFBUserFriendInfo(access_token) {
	FB.api(
		'/me/friends',
		{
			access_token: access_token
		},
		function (response) {
			if (response && !response.error) {
				var data_length = response.data.length;
				
				var input_name = document.getElementById('target_name').value;
				console.log(input_name);
				
				var current_name = null;
				var current_id = null;
				var found = false;
				for (var index = 0; index < data_length; index++) {
					current_name = response.data[index].name;
					current_id = response.data[index].id;
					
					if (current_name == input_name) {
						found = true;
						
						FB.api(
							//'/' + current_id + '?metadata=1',
							'/' + current_id + '/posts',
							{
								access_token: access_token
							},
							function (response) {
								console.log(response);
								console.log(response.data);
								var data_len = response.data.length;
								for (var i = 0; i < data_len; i++) {
									console.log(response.data[i]);
								}
								console.log(response.error);
							}
						);
					}
				}
				
				if (!found) {
					alert('The individual specified by name is not available for search via Facebook.');
				}
			}
		}
	);
}


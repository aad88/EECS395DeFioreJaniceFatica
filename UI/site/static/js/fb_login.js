// Authored by twtrubiks on 2016/11/27

function FBLogin() {
	FB.login(function (response) {
		var obj = {
			userID: response.authResponse.userID,
			accessToken: response.authResponse.accessToken
		};
		var data_json = JSON.stringify(obj);
		$.ajax({
			url: "/login/facebook",
			type: "POST",
			data: data_json,
			async: false,
			contentType: "application/json",
			success: function (data, textStatus, jqXHR) {
				if (data == "11") {
					location.replace("/");
				}
			}
		});
	}, {
		scope: 'publish_actions,email,user_friends',
		return_scopes: true
	});
}

function fetchUserDetail() {
	FB.api('/me', function (response) {
		console.log('Successful login for: ' + response.name);
	});
}

function checkFBLogin() {
	FB.getLoginStatus(function (response) {
		if (response.status ==='connected') {
			fetchUserDetail();
		}
		else if (response.status === 'not_authorized') {
			FBLogin();
			console.log("Please log into this app.")
		}
		else {
			FBLogin();
			console.log("Please log into Facebook.")
		}
	});
}


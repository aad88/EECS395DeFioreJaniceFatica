// Authored by twtrubiks on 2016/11/27

function FBLogin() {
	FB.login(function (response) {
		var data_obj = {
			userID: response.authResponse.userID,
			accessToken: response.authResponse.accessToken,
			firstName: null
		};
		var data_json = JSON.stringify(data_obj);
		$.ajax({
			url: "/login/facebook",
			type: "POST",
			data: data_json,
			async: false,
			contentType: "application/json",
			success: function (data, textStatus, jqXHR) {
				if (data == "SUCCESS") {
					location.replace("http://localhost:5000/account");
				}
			}
		});
	}, {
		scope: 'user_friends',
		return_scopes: true
	});
}

function FBLogout() {
	FB.getLoginStatus(function (response) {
		if (response.status === 'connected') {
			FB.logout(function (response) {
				var data_obj = {};
				var data_json = JSON.stringify(data_obj);
				$.ajax({
					url: "/logout/facebook",
					type: "POST",
					data: data_json,
					async: false,
					contentType: "application/json",
					success: function (data, textStatus, jqXHR) {
						if (data == "SUCCESS") {
							location.replace("http://localhost:5000/login");
						}
					}
				});
			});
		}
	});
}

function fetchUserID() {
	FB.api('/me', function (response) {
		return response.id;
	});
}

function fetchUserName() {
	FB.api('/me', function (response) {
		return response.first_name;
	});
}

function checkFBLogin() {
	FB.getLoginStatus(function (response) {
		if (response.status ==='connected') {
			var data_obj = {
				userID: response.authResponse.userID,
				accessToken: response.authResponse.accessToken,
				firstName: null
			};
			var data_json = JSON.stringify(data_obj);
			$.ajax({
				url: "/login/facebook",
				type: "POST",
				data: data_json,
				async: false,
				contentType: "application/json",
				success: function (data, textStatus, jqXHR) {
					if (data == "SUCCESS") {
						location.replace("http://localhost:5000/account");
					}
				}
			});
		}
		else if (response.status === 'not_authorized') {
			FBLogin();
		}
		else {
			FBLogin();
		}
	});
}


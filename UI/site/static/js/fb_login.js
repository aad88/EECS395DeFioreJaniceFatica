// Authored by twtrubiks on 2016/11/27

function FBLogin() {
	FB.login(function (response) {
		FB.api(
			'/me',
			function (response2) {
				var data_obj = {
					status: response.status,
					userID: response.authResponse.userID,
					accessToken: response.authResponse.accessToken,
					name: response2.name
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
		);
	}, {
		scope: 'email,user_friends',
		return_scopes: true
	});
}

function FBLogout() {
	FB.getLoginStatus(function (response) {
		if (response.status === 'connected') {
			console.log('Logged in!');
			FB.logout(function (response) {
				var data_obj = {};
				var data_json = JSON.stringify(data_obj);
				
				document.location.reload();
				
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

function checkFBLogin() {
	FB.getLoginStatus(function (response) {
		if (response.status ==='connected') {
			FB.api(
				'/me',
				function (response2) {
					var data_obj = {
						status: response.status,
						userID: response.authResponse.userID,
						accessToken: response.authResponse.accessToken,
						name: response2.name
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
			);
		}
		else if (response.status === 'not_authorized') {
			FBLogin();
		}
		else {
			FBLogin();
		}
	});
}


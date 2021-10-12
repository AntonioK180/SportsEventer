var mainContainer = $("#main_container");

var logout = function() {
    firebase
        .auth()
        .signOut()
        .then(
            function() {
                console.log("success");
                window.location.replace("login.html");
            },
            function() {}
        );
};

var init = function() {
    firebase.auth().onAuthStateChanged(function(user) {
        if (user) {
            const userId = user.uid;
            const userName = user.displayName;
            var UID = "UID";
            CometChat.getUser(UID).then(
                user => {
                    console.log("User details fetched for user:", user);
                    CometChatWidget.login({
                        "uid": "UID"
                    }).then(response => {
                        CometChatWidget.launch({
                            "widgetID": "cb24f737-99c8-49b8-b684-5d00062b0e6f",
                            "docked": "true",
                            "alignment": "left", //left or right
                            "roundedCorners": "true",
                            "height": "450px",
                            "width": "400px",
                            "defaultID": 'superhero1', //default UID (user) or GUID (group) to show,
                            "defaultType": 'user' //user or group
                        });
                    }, error => {
                        console.log("User login failed with error:", error);
                        //Check the reason for error and take appropriate action.
                    });
                },
                response => {
                    CometChatWidget.login({
                        uid: superhero5,
                    }).then(
                        (response) => {
                            console.log("User login successful:", response);
                        },
                        (error) => {
                            console.log("User login failed with error:", error);
                            //Check the reason for error and take appropriate action.
                        },
                        CometChatWidget.launch({
                            "widgetID": "cb24f737-99c8-49b8-b684-5d00062b0e6f",
                            "target": "#cometchat",
                            "roundedCorners": "true",
                            "height": "600px",
                            "width": "800px",
                            "defaultID": 'superhero1', //default UID (user) or GUID (group) to show,
                            "defaultType": 'user' //user or group
                        });
                    );
                },
                error => {
                    console.log("User details fetching failed with error:", error);
                    let apiKey = "d3d780970146dbe3563760dea74023bb112b6f19";
                    var uid = userId;
                    var name = userDisplayName;

                    var user = new CometChat.User(uid);

                    user.setName(name);

                    CometChat.createUser(user, apiKey).then(
                        user => {
                            console.log("user created", user);
                        }, error => {
                            console.log("error", error);
                        }
                    )
                }
            );
            console.log("stay");
            mainContainer.css("display", "");
        } else {
            CometChat.logout().then(
                () => {
                    //Logout completed successfully
                    console.log("Logout completed successfully");
                },
                (error) => {
                    //Logout failed with exception
                    console.log("Logout failed with exception:", { error });
                }
            );
            mainContainer.css("display", "none");
            console.log("redirect");
            window.location.replace("login.html");
        }
    });
};

init();
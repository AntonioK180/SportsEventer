var fireBase = fireBase || firebase;
var hasInit = false;
var config = {
  apiKey: "AIzaSyDKFyActVdqhKKaWk4uyUoaXx41Hq0xvAU",
  authDomain: "sportseventer.firebaseapp.com",
  projectId: "sportseventer",
  storageBucket: "sportseventer.appspot.com",
  messagingSenderId: "958064997296",
  appId: "1:958064997296:web:0143396b2b80a2eb731c75",
  measurementId: "G-R3YGWV19TG"
  };

if(!hasInit){
    firebase.initializeApp(config);
    hasInit = true;
}
(function () {
  // cometchat initialization
  var appID = "33445dbeae9e1a3";
  var region = "eu";
  var appSetting = new CometChat.AppSettingsBuilder()
    .subscribePresenceForAllUsers()
    .setRegion(region)
    .build();
  CometChat.init(appID, appSetting).then(
    () => {
      console.log("Initialization completed successfully");
      // You can now call login function.
    },
    (error) => {
      console.log("Initialization failed with error:", error);
      // Check the reason for error and take appropriate action.
    }
  );
})();

// cometchat widget initialization
window.addEventListener("DOMContentLoaded", (event) => {
  CometChatWidget.init({
    appID: "33445dbeae9e1a3",
    appRegion: "eu",
    authKey: "69bbe8b391b18085542c82234f21164b52577336",
  }).then(
    (response) => {
      console.log("Initialization (CometChatWidget) completed successfully");
    },
    (error) => {
      console.log("Initialization (CometChatWidget) failed with error:", error);
      //Check the reason for error and take appropriate action.
    }
  );
});

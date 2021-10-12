let data;

function isUsernameRegistered(username) {
    let deferred = $.Deferred();
    $.ajax({
        url: "http://localhost:5000/rest/users?username=" + username,
        dataType: "json",
        type: "GET",
        success: function(result) {
            data = result;
            deferred.resolve();
        }
    });
    return deferred.promise();
}


$(document).ready(function() {
    $('#sign_button').click(function() {
        $(".error").hide();
        var hasError = false;

        var usernameVal = $("#username").val();
        var usernameFree = true;
        $.when(isUsernameRegistered(usernameVal)).done(function() {
            console.log(data["nameFree"]);

            if (data["nameFree"] == 0) {
                $("#username").after('<span class="error" id="error">This username is already taken.</span>');
                console.log("USERNAME IS TAKEN");
                hasError = true;
            }
        });

        var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;

        var emailVal = $("#email").val();
        if (emailVal == '') {
            $("#email").after('<span class="error" id="error">Please enter your email address.</span>');
            console.log("EMPTY EMAIL");
            hasError = true;
        } else if (!emailReg.test(emailVal)) {
            $("#email").after('<span class="error" id="error">Enter a valid email address.</span>');
            console.log("INVALID EMAIL");
            hasError = true;
        }

        if (hasError == true) { return false; }
    });
});
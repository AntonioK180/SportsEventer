$(document).ready(function(){
  $("#submit_btn").click(function(){
    $(".error").hide();
    var hasError = false;

    var selectedDate = new Date($("#date").val());
    var currentDate = new Date();
    if(selectedDate < currentDate){
      $("#date").after('<span class="error">You cannot chose a previous date!</span>');
      hasError = true;
    }

    var participatingVal = $("#participating").val();
    if(participatingVal <= 0){
      $("#participating").after('<span class="error">The amount of people cannot be negative or 0!</span>');
      hasError = true;
    }

    var neededVal = $("#needed").val();
    if(neededVal <= 0){
      $("#needed").after('<span class="error">The amount of people cannot be negative or 0!</span>');
      hasError = true;
    }

    var priceVal = $("#price").val();
    if(priceVal < 0){
      $("#price").after('<span class="error">The price cannot be negative!</span>');
      hasError = true;
    }

    if(hasError == true){return false;}
  });
});

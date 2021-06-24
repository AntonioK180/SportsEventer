let data;

function loadAllEvents(allEvents){
  var tableObject = $('table');
  $.each(allEvents, function(i, item){
    var str = '<tr class = "item" id="'+item.event_id+'">"';
    var btn = '<button class = "details" id="btn_'+item.event_id+'">Details</button>';
    var btn_join = '<button class = "join" id="btn_join_'+item.event_id+'">Join Event</button>';
    var tr = $(str).append(
      $('<td class="event_id">').text(item.event_id),
      $('<td class="created_by">').text(item.created_by + "'s "),
      $('<td class="sport">').text(item.sport + " event "),
      $('<td class="people_participating" hidden>').text("People participating: " + item.people_participating),
      $('<td class="people_needed"        hidden>').text("People needed: " + item.people_needed),
      $('<td class="date"                 hidden>').text("Date: " + item.date),
      $('<td class="time"                 hidden>').text("Time: " + item.time),
      $('<td class="loacation"            hidden>').text("Location: " + item.location),
      $('<td class="price"                hidden>').text("Price: " + item.price),
      $('<td class="description"          hidden>').text("Description: " + item.description),
      $('<td class="button">').append(btn),
      $('<td class="button_join">').append(btn_join)
    );
    $("table").append(tr);

    $("#btn_"+item.event_id).click(function(){
      console.log('Button ' + item.event_id + ' clicked');
      $("#"+item.event_id+" > .people_participating").toggle();
      $("#"+item.event_id+" > .people_needed").toggle();
      $("#"+item.event_id+" > .date").toggle();
      $("#"+item.event_id+" > .time").toggle();
      $("#"+item.event_id+" > .location").toggle();
      $("#"+item.event_id+" > .price").toggle();
      $("#"+item.event_id+" > .description").toggle();
    })

    $("#btn_join_"+item.event_id).click(function(){
      console.log("Join Button" + item.event_id + " was pressed");
      console.log(allEvents[i].people_participating);

      if(allEvents[i].people_participating >= allEvents[i].people_needed){
        alert("YOU CANNOT JOIN THIS EVENT, BECAUSE IT IS FULL!");
      }  else {
        $.ajax({
          url: "http://localhost:5000/rest/events/join?event_id=" + item.event_id + "&user_id=" + {{user_id}},
          dataType: "json",
          type: "PUT",
          async: false
        });
        alert("YOU SUCCESSFULLY JOINED " + allEvents[i].created_by + "'s " + allEvents[i].sport + " EVENT!");
        location.reload();
      }

    })
  })
}


function getData(){
  let deferred = $.Deferred();
  $.ajax({
    url: "http://localhost:5000/rest/events",
    dataType: "json",
    type: "GET",
    success: function(result){
      data = result;
      deferred.resolve();
    }
  });
  return deferred.promise();
}

$(document).ready(function(){
  $.when(getData()).done(function(){
    loadAllEvents(data);
  });
});

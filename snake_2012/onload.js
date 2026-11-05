//
// Begin
//
$(document).ready(function () {
  _game = new Core();
  _game.load();
  _game.start();

  $(document).keydown(function (evt) {
    // document.onkeypress didn't work in Chrome

    var evt = evt ? evt : window.event;
    var code = evt.charCode ? evt.charCode : evt.keyCode;

    switch (code) {
      case 37: // Left
        _game.cmdLeft();
        break;
      case 38: // Up
        _game.cmdUp();
        break;
      case 39: // Right
        _game.cmdRight();
        break;
      case 40: // Down
        _game.cmdDown();
        break;
    }
  });

  function showResults(playersList) {
    $("#showResults").html("");
    var htmlList = "";
    for (var i = 0; i < playersList.length; i++) {
      htmlList +=
        "<li>" +
        playersList[i][1] +
        "&nbsp;......&nbsp;" +
        playersList[i][0] +
        "</li>";
    }
    $("#showResults").html("<ol>" + htmlList + "</ol>");
  }
});

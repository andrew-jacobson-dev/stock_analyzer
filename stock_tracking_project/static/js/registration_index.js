$(document).ready(function(){

    $('#registration-list a').on('click', function (e) {
      e.preventDefault()
      $(this).tab('show')
    });

    $('#go-to-register').click(function() {
      var value = $("[aria-controls='register']");
      $(value).tab('show');
    });

    $('#go-to-log-in').click(function() {
      var value = $("[aria-controls='log-in']");
      $(value).tab('show');
    });

});
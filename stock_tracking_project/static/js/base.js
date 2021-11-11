$(document).ready(function(){

    $(".nav-bar.nav-link").on("click", function(){

        $(".nav-bar.nav-link.active").removeClass('active');
        $(this).addClass('active');

    });

});
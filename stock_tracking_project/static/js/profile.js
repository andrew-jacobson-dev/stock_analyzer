$(document).ready(function(){

    $('#id_first_name').keyup(function() {

        if( $(this).val() ) {
            $('#save-user-info').prop("disabled", false);
        }
        else {
            $('#save-user-info').prop("disabled", true);
        }

    });

    $('#id_last_name').keyup(function() {

        if( $(this).val() ) {
            $('#save-user-info').prop("disabled", false);
        }
        else {
            $('#save-user-info').prop("disabled", true);
        }

    });

    $('#id_email').keyup(function() {

        if( $(this).val() ) {
            $('#save-user-info').prop("disabled", false);
        }
        else {
            $('#save-user-info').prop("disabled", true);
        }

    });

    $('#id_username').keyup(function() {

        if( $(this).val() ) {
            $('#save-user-info').prop("disabled", false);
        }
        else {
            $('#save-user-info').prop("disabled", true);
        }

    });

////SETTINGS SECTION

    $('#save-notification-settings').click(function() {

        var valid_form = true;

        if ( $('#id_expert_rec_send_email').is(':checked') || $('#id_expert_rec_send_text').is(':checked') ) {

            if ( !$('#id_expert_rec_buy').is(':checked') && !$('#id_expert_rec_sell').is(':checked') && !$('#id_expert_rec_other').is(':checked') ) {

                var x = document.getElementById("error-expert-rec");
                $(x).text("select an alert type");
                $(x).show();

                valid_form = false;
            }

            if ( $('#id_expert_rec_buy').is(':checked') || $('#id_expert_rec_sell').is(':checked') || $('#id_expert_rec_other').is(':checked') ) {

                var x = document.getElementById("error-expert-rec");
                $(x).hide();
            }
        }

        if ( $('#id_expert_rec_buy').is(':checked') || $('#id_expert_rec_sell').is(':checked') || $('#id_expert_rec_other').is(':checked') ) {

            if (!$('#id_expert_rec_send_email').is(':checked') && !$('#id_expert_rec_send_text').is(':checked')) {

                var x = document.getElementById("error-expert-rec");
                $(x).text("select a communication method");
                $(x).show();

                valid_form = false;
            }
        }

        if ( $('#id_custom_alerts_send_email').is(':checked') || $('#id_custom_alerts_send_text').is(':checked') ) {

            if (!$('#id_custom_alerts_buy').is(':checked') && !$('#id_custom_alerts_sell').is(':checked') && !$('#id_custom_alerts_other').is(':checked')) {

                var x = document.getElementById("error-custom-alerts");
                $(x).text("select an alert type");
                $(x).show();

                valid_form = false;
            }

            if ( $('#id_custom_alerts_buy').is(':checked') || $('#id_custom_alerts_sell').is(':checked') || $('#id_custom_alerts_other').is(':checked') ) {

                var x = document.getElementById("error-custom-alerts");
                $(x).hide();
            }
        }

        if ( $('#id_custom_alerts_buy').is(':checked') || $('#id_custom_alerts_sell').is(':checked') || $('#id_custom_alerts_other').is(':checked') ) {

            if (!$('#id_custom_alerts_send_email').is(':checked') && !$('#id_custom_alerts_send_text').is(':checked')) {

                var x = document.getElementById("error-custom-alerts");
                $(x).text("select a communication method");
                $(x).show();

                valid_form = false;
            }
        }

        return valid_form;

    })

});
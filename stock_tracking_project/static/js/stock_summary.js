$(document).ready(function(){

////ALERTS SECTION STUFF

    $('#alerts-header').click(function($e) {

        $e.preventDefault();
        $('i', this).toggleClass('fa-chevron-circle-down fa-chevron-circle-right');
        $('.alert-section-body').toggle();

    })

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

////TRANSACTION SECTION STUFF

    $('#transactions-header').click(function($e) {

        $e.preventDefault();
        $('i', this).toggleClass('fa-chevron-circle-down fa-chevron-circle-right');
        $('.transactions-section-body').toggle();

    })

    $('#id_transaction_choice_field').change(function() {

          var x = document.getElementById("total-transaction-amount-label");

          if( $(this).val() == 3 || $(this).val() == 3 ) {
              $(x).text("total sold");
          }
          else {
              $(x).text("total invested");
          }

          var x = document.getElementById("buy-sell-only");

          if( $(this).val() == 1 || $(this).val() == 2 || $(this).val() == 3 || $(this).val() == 4 ) {
              $(x).show();
          }
          else {
              $(x).hide();
          }

    })

    $('#id_ticker_symbol_choice').change(function() {

        if( $(this).val() ) {
            $('#id_ticker_symbol_text').prop("disabled", true);
        }
        else {
            $('#id_ticker_symbol_text').prop("disabled", false);
        }

    })

    $('#id_ticker_symbol_text').keyup(function() {

        if( $(this).val() ) {
            $('#id_ticker_symbol_choice').prop("disabled", true);
        }
        else {
            $('#id_ticker_symbol_choice').prop("disabled", false);
        }

    })

////PORTFOLIO SECTION STUFF

    $('#portfolio-header').click(function($e) {

        $e.preventDefault();
        $('i', this).toggleClass('fa-chevron-circle-down fa-chevron-circle-right');
        $('.portfolio-section-body').toggle();

    })

});
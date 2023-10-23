odoo.define('event_management.event_booking_template', function (require) {
'use strict';

var ajax = require('web.ajax');
var publicWidget = require('web.public.widget');
publicWidget.registry.portalDetails = publicWidget.Widget.extend({
    selector: '#booking_form',
        events: {
            'change #customer_ids': '_onChangeField',
            'change #type_ids': '_onChangeField',
            'change #start_date': '_onChangeField',
            'change #end_date': '_onChangeField',
        },
        _onChangeField: function (e) {
           var event_type = $('#type_ids').val();
           var customer = $('#customer_ids').val();
           var start_date = $('#start_date').val();
           var end_date = $('#end_date').val();
           console.log(end_date)
           var time_duration = $('#time_duration');
           if(event_type && customer && start_date && end_date){
                    submitButton.removeAttribute('disabled');
           }else{submitButton.setAttribute('disabled', 'disabled');}
           if(event_type && customer && start_date && end_date){
                if(event_type != '' && customer != ''){
                    ajax.jsonRpc('/booking_data', 'call', {
                    event_type: event_type,
                    customer: customer,
                    start_date: start_date,
                    end_date: end_date,
                }).then(function (data) {
                    var NewName = `${data.event_type}:${data.customer}/${data.start_date}:${data.end_date}`
                    $('#name').val(NewName)
                });
                }
           }

           if (start_date && end_date){
                var start_date = new Date(start_date);
                var end_date = new Date(end_date);
                if (start_date > end_date) {
                    $('#error_message').html("The end date must be greater than the start date.");
                    $('#end_date').val("")
                    $('#time_duration').val("")
                    return false;}
                else{$('#error_message').html("");}
                console.log(start_date,end_date)
                var millisecond_per_day = 24*60*60*1000;
                time_duration = (end_date.getTime() - start_date.getTime()) / millisecond_per_day;
                if (time_duration == 0){
                    $('#time_duration').val(1);}
                else{
                    $('#time_duration').val(time_duration);}
           }
        },
    });
});


odoo.define('event_booking_snippet.snippet', function(require) {
'use strict';
var PublicWidget = require('web.public.widget');
var rpc = require('web.rpc');
var core = require('web.core');
var qweb = core.qweb;
var Dynamic = PublicWidget.Widget.extend({
    selector: '.dynamic_snippet_blog',
    start: function() {
        var self = this;
        rpc.query({
            route: '/latest_booking'
        }).then(function(data) {
        var chunks = _.chunk(data, 4)
//        chunks[0].is_active = true
            var snippet = qweb.render('event_management.event_booking_snippet_carousel', {'chunks':chunks, 'new_id': Date.now()})
            self.$('#courosel').html(snippet)
        })
    },

});
PublicWidget.registry.dynamic_snippet_blog = Dynamic;
return Dynamic;
});
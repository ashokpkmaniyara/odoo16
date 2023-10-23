from odoo import http
from odoo.http import Controller, request, route


class Booking(Controller):
    @route(route='/booking-form', auth='user', website=True)
    def booking(self):
        customer_ids = request.env['res.partner'].search([])
        type_ids = request.env['event.type'].search([])
        return request.render('event_management.event_booking_template',
                              {'customer_ids': customer_ids,
                               'type_ids': type_ids,
                               })

    @route('/create/event_booking', auth='public', website=True, csrf=False)
    def create_booking(self, **kw):
        try:
            request.env['event.booking'].create({
                'partner_id': kw.get('customer'),
                'event_type_id': kw.get('type'),
                'event_start_date': kw.get('start_date'),
                'event_end_date': kw.get('end_date'),
            })
        except:
            return request.redirect('/event_booking_failed')
        return request.render('event_management.event_booking_success')

    @route('/event_booking_failed', auth='user', website='true')
    def event_booking_failed(self):
        return request.render('event_management.event_booking_failed')

    @route(route='/customer-form', auth='user', website=True)
    def customer(self):
        country_ids = request.env['res.country'].search([])
        return request.render('event_management.customer_template',
                              {'country_ids': country_ids})

    @route('/create/customer', auth='public', website=True, csrf=False)
    def create_customer(self, **kw):
        request.env['res.partner'].create({
            'name': kw.get('name'),
            'email': kw.get('email'),
            'country_id': kw.get('country')
        })
        return request.redirect('/booking-form')

    @http.route('/booking_data', type='json', auth='user', methods=['POST'],
                website=True, csrf=False)
    def data_fetch(self, **kw):
        event_type = kw.get('event_type')
        customer = kw.get('customer')
        start_date = kw.get('start_date')
        end_date = kw.get('end_date')
        event = request.env['event.type'].browse(int(event_type))
        customer = request.env['res.partner'].browse(int(customer))
        return {
            'event_type': event.name,
            'customer': customer.name,
            'start_date': start_date,
            'end_date': end_date,
        }

    @http.route(['/latest_booking'], type="json", auth="public",
                website=True)
    def latest_booking(self):
        booking_ids = request.env['event.booking'].search_read([],
                                                               ['id', 'name',
                                                                'event_type_id',
                                                                'partner_id',
                                                                'booking_date',
                                                                'event_start_date',
                                                                'event_end_date'],
                                                               limit=10,
                                                               order='create_date desc')
        for booking in booking_ids:
            event_type_id = booking.get('event_type_id')
            if event_type_id:
                event_type = request.env['event.type'].browse(
                    int(event_type_id[0]))
                booking['event_type_image'] = event_type.image

        return booking_ids

    @route(['/slides/<id>'], auth="public", website=True)
    def booked_details(self, id):
        booked_id = request.env['event.booking'].browse(int(id))

        return request.render('event_management.event_booked_template', {
            'booked_id': booked_id,
        })

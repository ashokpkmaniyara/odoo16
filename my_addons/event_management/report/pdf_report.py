# -*- coding: utf-8 -*-
from odoo import models, api


class PDFReport(models.AbstractModel):
    """abstract model for pdf report"""
    _name = 'report.event_management.event_pdf_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """function to print the pdf reports by taking the data from database
        using the query"""
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        type = data.get('type')

        query = """select b.name as name,t.name as type,p.name as customer,
        b.booking_date,b.booking_state, (select c.catering_grand_total from 
        event_catering as c where b.id = c.catering_event_id limit 1) as 
        catering_grand_total, (select c.id from event_catering as c where 
        b.id = c.catering_event_id limit 1) as catering_id from event_booking 
        as b join event_type as t on b.event_type_id=t.id join res_partner as 
        p on b.partner_id=p.id"""

        params = []

        if from_date:
            query += """ and b.booking_date >= %s """
            params.append(from_date)
        if to_date:
            query += """ and b.booking_date <= %s """
            params.append(to_date)
        if type:
            query += """ and t.name = %s """
            params.append(type)

        self.env.cr.execute(query, tuple(params))
        report = self.env.cr.dictfetchall()
        print(report)

        if not report:
            raise models.ValidationError('There is nothing to print')

        result = []
        if data.get('include_catering'):
            for event in report:
                query2 = """select ct.catering_type_name,
                cp.event_catering_page_description,
                cp.event_catering_page_quantity,ct.catering_type_unit_price,
                cp.event_catering_page_subtotal from event_catering_pages as 
                cp join event_catering_type as ct on 
                cp.event_catering_page_item_id=ct.id where 
                parent_welcome_drink_id=%s or parent_breakfast_id=%s or 
                parent_lunch_id=%s or parent_dinner_id=%s or 
                parent_snacks_and_drinks_id=%s or parent_beverages_id=%s"""

                self.env.cr.execute(query2, (
                    event['catering_id'], event['catering_id'],
                    event['catering_id'], event['catering_id'],
                    event['catering_id'], event['catering_id']))
                report2 = self.env.cr.dictfetchall()
                event['items'] = report2
                result.append(event)

        return {
            'data': data,
            'report': report if not data.get('include_catering') else result
        }

# -*- coding: utf-8 -*-
import io
from datetime import date

from odoo import models, fields
import json
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class ReportWizard(models.TransientModel):
    """created model of event.wizard to crate a wizard view"""
    _name = 'event.wizard'

    from_date = fields.Date(string='From Date', help='specify the start date')
    to_date = fields.Date(string='To Date', help='specify the end date')
    type = fields.Many2one('event.type', string='Type', help='select the type')
    include_catering = fields.Boolean(string='Include Catering',
                                      help='enable field to add catering')

    def query(self):
        """function for executing the main query and to check there is any
        records to print otherwise raise an exception"""
        from_date = self.from_date
        to_date = self.to_date
        type = self.type.name

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
        if not report:
            raise models.ValidationError('There is no data to print')
        return report

    def action_done(self):
        """function for pdf button inside the menu report. By clicking this
        button the data will pass into the report"""
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'type': self.type.name,
            'include_catering': self.include_catering,
        }
        return self.env.ref(
            'event_management.report_event_management').report_action(None,
                                                                      data=data)

    def action_xlsx(self):
        """function for xlsx button inside the menu report. By clicking this
        button the data will pass into the report"""
        report = self.query()
        data = {
            'report': report,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'type': self.type.name,
            'include_catering': self.include_catering,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'event.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """function to print xlsx report with different conditions"""
        from_date = data.get('from_data')
        to_date = data.get('to_date')
        type = data.get('type')
        report = data.get('report')
        user_obj = self.env.user
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

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '11px', 'align': 'center'})
        heading = workbook.add_format(
            {'font_size': '13px', 'align': 'center', 'bold': True})
        sub_head = workbook.add_format(
            {'font_size': '10px', 'align': 'center', 'bold': True})
        date_style = workbook.add_format(
            {'text_wrap': True, 'num_format': 'dd-mm-yyyy', 'align': 'center'})
        sheet.merge_range('A2:G3', 'Event Management', head)
        sheet.write('B4', user_obj.company_id.name, txt)
        sheet.write('B5', user_obj.company_id.street, txt)
        sheet.write('B6', user_obj.company_id.city, txt)
        sheet.write('B7', user_obj.company_id.zip, txt)
        sheet.write('B8', user_obj.company_id.state_id.name, txt)
        sheet.write('B9', user_obj.company_id.country_id.name, txt)
        sheet.write('C5', 'From Date:', cell_format)
        sheet.write('C6', 'To Date:', cell_format)
        if from_date:
            sheet.write('D5', from_date, date_style)
        else:
            sheet.write('D5', date.today(), date_style)
        if to_date:
            sheet.write('D6', to_date, date_style)
        else:
            sheet.write('D6', date.today(), date_style)
        if type:
            sheet.write('C7', 'Type:', cell_format)
            sheet.write('D7', type, txt)

        sheet.set_column(0, 0, 10)
        sheet.set_column(1, 1, 50)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 20)
        sheet.set_column(4, 4, 20)
        sheet.set_column(5, 5, 20)
        sheet.set_column(6, 6, 20)

        row = 12
        col = 0
        slno = 1
        if data.get('include_catering'):
            if not type:
                sheet.write('A11', 'SL.NO:', heading)
                sheet.write('B11', 'NAME', heading)
                sheet.write('C11', 'TYPE', heading)
                sheet.write('D11', 'CUSTOMER', heading)
                sheet.write('E11', 'BOOKING DATE', heading)
                sheet.write('F11', 'STATUS', heading)
                sheet.write('G11', 'AMOUNT', heading)
                for rec in result:
                    sheet.write(row, col, slno, txt)
                    sheet.write(row, col + 1, rec.get('name'), txt)
                    sheet.write(row, col + 2, rec.get('type'), txt)
                    sheet.write(row, col + 3, rec.get('customer'), txt)
                    sheet.write(row, col + 4, rec.get('booking_date'),
                                date_style)
                    sheet.write(row, col + 5, rec.get('booking_state'), txt)
                    sheet.write(row, col + 6, rec.get('catering_grand_total'),
                                txt)
                    row += 1
                    col = 0
                    if rec.get('items'):
                        sheet.write(row, col + 1, 'NAME', sub_head)
                        sheet.write(row, col + 2, 'DESCRIPTION', sub_head)
                        sheet.write(row, col + 3, 'QUANTITY', sub_head)
                        sheet.write(row, col + 4, 'PRICE', sub_head)
                        sheet.write(row, col + 5, 'TOTAL', sub_head)
                        row += 1
                        value = rec.get('items')
                        for item in value:
                            col = 0
                            sheet.write(row, col + 1,
                                        item.get('catering_type_name'), txt)
                            sheet.write(row, col + 2,
                                        item.get(
                                            'event_catering_page_description'),
                                        txt)
                            sheet.write(row, col + 3,
                                        item.get(
                                            'event_catering_page_quantity'),
                                        txt)
                            sheet.write(row, col + 4,
                                        item.get('catering_type_unit_price'),
                                        txt)
                            sheet.write(row, col + 5,
                                        item.get(
                                            'event_catering_page_subtotal'),
                                        txt)
                            row += 1
                        row += 1
                        slno += 1
                sheet.write(row + 2, 5, 'Total:', heading)
                sheet.write(row + 2, 6,
                            sum([r.get('catering_grand_total') or 0.0 for r in
                                 report]), txt)

            else:
                sheet.write('A11', 'SL.NO:', heading)
                sheet.write('B11', 'NAME', heading)
                sheet.write('C11', 'CUSTOMER', heading)
                sheet.write('D11', 'BOOKING DATE', heading)
                sheet.write('E11', 'STATUS', heading)
                sheet.write('F11', 'AMOUNT', heading)
                for rec in report:
                    sheet.write(row, col, slno, txt)
                    sheet.write(row, col + 1, rec.get('name'), txt)
                    sheet.write(row, col + 2, rec.get('customer'), txt)
                    sheet.write(row, col + 3, rec.get('booking_date'),
                                date_style)
                    sheet.write(row, col + 4, rec.get('booking_state'), txt)
                    sheet.write(row, col + 5, rec.get('catering_grand_total'),
                                txt)
                    row += 1
                    col = 0
                    if rec.get('items'):
                        sheet.write(row, col + 1, 'NAME', sub_head)
                        sheet.write(row, col + 2, 'DESCRIPTION', sub_head)
                        sheet.write(row, col + 3, 'QUANTITY', sub_head)
                        sheet.write(row, col + 4, 'PRICE', sub_head)
                        sheet.write(row, col + 5, 'TOTAL', sub_head)
                        row += 1
                        value = rec.get('items')
                        for item in value:
                            col = 0
                            sheet.write(row, col + 1,
                                        item.get('catering_type_name'), txt)
                            sheet.write(row, col + 2,
                                        item.get(
                                            'event_catering_page_description'),
                                        txt)
                            sheet.write(row, col + 3,
                                        item.get(
                                            'event_catering_page_quantity'),
                                        txt)
                            sheet.write(row, col + 4,
                                        item.get('catering_type_unit_price'),
                                        txt)
                            sheet.write(row, col + 5,
                                        item.get(
                                            'event_catering_page_subtotal'),
                                        txt)
                            row += 1
                        row += 1
                        slno += 1
                sheet.write(row + 2, 4, 'Total:', heading)
                sheet.write(row + 2, 5,
                            sum([r.get('catering_grand_total') or 0.0 for r in
                                 report]), txt)

        else:
            if not type:
                sheet.write('A11', 'SL.NO:', heading)
                sheet.write('B11', 'NAME', heading)
                sheet.write('C11', 'TYPE', heading)
                sheet.write('D11', 'CUSTOMER', heading)
                sheet.write('E11', 'BOOKING DATE', heading)
                sheet.write('F11', 'STATUS', heading)
                sheet.write('G11', 'AMOUNT', heading)
                for rec in report:
                    sheet.write(row, col, slno, txt)
                    sheet.write(row, col + 1, rec.get('name'), txt)
                    sheet.write(row, col + 2, rec.get('type'), txt)
                    sheet.write(row, col + 3, rec.get('customer'), txt)
                    sheet.write(row, col + 4, rec.get('booking_date'),
                                date_style)
                    sheet.write(row, col + 5, rec.get('booking_state'), txt)
                    sheet.write(row, col + 6, rec.get('catering_grand_total'),
                                txt)
                    row += 1
                    slno += 1
                sheet.write(row + 2, 5, 'Total:', heading)
                sheet.write(row + 2, 6,
                            sum([r.get('catering_grand_total') or 0.0 for r in
                                 report]), txt)
            else:
                sheet.write('A11', 'SL.NO:', heading)
                sheet.write('B11', 'NAME', heading)
                sheet.write('C11', 'CUSTOMER', heading)
                sheet.write('D11', 'BOOKING DATE', heading)
                sheet.write('E11', 'STATUS', heading)
                sheet.write('F11', 'AMOUNT', heading)
                for rec in report:
                    sheet.write(row, col, slno, txt)
                    sheet.write(row, col + 1, rec.get('name'), txt)
                    sheet.write(row, col + 2, rec.get('customer'), txt)
                    sheet.write(row, col + 3, rec.get('booking_date'),
                                date_style)
                    sheet.write(row, col + 4, rec.get('booking_state'), txt)
                    sheet.write(row, col + 5, rec.get('catering_grand_total'),
                                txt)
                    row += 1
                    slno += 1
                sheet.write(row + 2, 4, 'Total:', heading)
                sheet.write(row + 2, 5,
                            sum([r.get('catering_grand_total') or 0.0 for r in
                                 report]), txt)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

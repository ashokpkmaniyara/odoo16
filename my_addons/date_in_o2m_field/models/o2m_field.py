# -*- coding: utf-8 -*-
from datetime import datetime
import calendar

from odoo import models, fields


class AddField(models.Model):
    _inherit = 'project.project'

    s_date_ids = fields.One2many('date.fields', 'o2m_field_id', string='S-Date',
                                 help='select the fields')

    def schedule_btn(self):
        """button function to create o2m field records"""
        self.s_date_ids = [fields.Command.clear()]
        line = {}
        for month in range(1, 13):
            # Get the current year
            created_year = self.create_date.year

            # Calculate the first and last day of the month
            first_day = datetime(created_year, month, 1).strftime(
                '%d-%m-%Y')
            last_day = (datetime(created_year, month,
                                 calendar.monthrange(self.create_date.year,
                                                     month)[1])).strftime(
                '%d-%m-%Y')

            # Create a new Schedule Date record
            line[month] = {
                'month': str(month),
                'year': str(created_year),
                'from_date': datetime.strptime(first_day, '%d-%m-%Y'),
                'to_date': datetime.strptime(last_day, '%d-%m-%Y')
            }
        self.s_date_ids = [fields.Command.create(value) for value in
                           line.values()]

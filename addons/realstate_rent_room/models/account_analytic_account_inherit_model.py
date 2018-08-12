# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class AccountAnalyticAccountModel(models.Model):
    _name = 'account.analytic.account'
    _inherit = ['account.analytic.account',
                'account.analytic.contract',
                ]

    init_datetime = fields.Datetime(string='Inicio')
    end_datetime = fields.Datetime(string='Fin')
    rent_place_id = fields.Many2one(comodel_name='realstate_rent_room.rent_place')

    @api.multi
    def single_create_invoice(self):
        """Create invoices from contracts

        :return: invoices created
        """
        invoices = self.env['account.invoice']
        for contract in self:
            ref_date = fields.Date.today()

            if contract.init_datetime >= contract.end_datetime:
                raise ValidationError(
                    _("You must review start and end dates!\n%s") %
                    contract.name
                )
            ctx = self.env.context.copy()
            ctx.update({
                # Force company for correct evaluation of domain access rules
                'force_company': contract.company_id.id,
            })
            invoices |= contract._create_invoice()

        return invoices

    # @api.multi
    # def recurring_create_invoice(self):
    #     """Create invoices from contracts
    #
    #     :return: invoices created
    #     """
    #     invoices = self.env['account.invoice']
    #     for contract in self:
    #         ref_date = contract.recurring_next_date or fields.Date.today()
    #         if (contract.date_start > ref_date or
    #                 contract.date_end and contract.date_end < ref_date):
    #             if self.env.context.get('cron'):
    #                 continue  # Don't fail on cron jobs
    #             raise ValidationError(
    #                 _("You must review start and end dates!\n%s") %
    #                 contract.name
    #             )
    #         old_date = fields.Date.from_string(ref_date)
    #         new_date = old_date + self.get_relative_delta(
    #             contract.recurring_rule_type, contract.recurring_interval)
    #         ctx = self.env.context.copy()
    #         ctx.update({
    #             'old_date': old_date,
    #             'next_date': new_date,
    #             # Force company for correct evaluation of domain access rules
    #             'force_company': contract.company_id.id,
    #         })
    #         # Re-read contract with correct company
    #         invoices |= contract.with_context(ctx)._create_invoice()
    #         contract.write({
    #             'recurring_next_date': fields.Date.to_string(new_date)
    #         })
    #     return invoices

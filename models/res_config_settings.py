# -*- coding: utf-8 -*-
from openerp import models, fields


class ConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    group_release_dates = fields.Boolean(
        "Manage book release dates",
        group='base.group_user',
        implied_group='igloo-test.group_release_dates')
    module_note = fields.Boolean("Install Notes app")

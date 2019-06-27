# -*- coding: utf-8 -*-
from openerp import models, fields, api

# Chapitre 4

# Using Abstract Models for reusable Model features
class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    active = fields.Boolean(default=True)
   
    def do_archive(self):
        for record in self:
            record.active = not record.active
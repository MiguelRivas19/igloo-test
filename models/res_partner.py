# -*- coding: utf-8 -*-
from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    book_ids = fields.One2many(
        'library.book', 'publisher_id',
        string='Published')

    authored_book_ids = fields.Many2many(
        'library.book',
        string='Authored Books',
        # relation='library_book_res_partner_rel'
        ) 
    
    # Chapitre 4
    
    # Adding features to a Model using inheritance
    _order = 'name'
    
    count_books = fields.Integer(
        'Number of Authored Books',
        compute='_compute_count_books'
        )
    
    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)
    
    # Chapitre 5
    
    # Creating new records
#     name = fields.Char('Name', required=True)
#     email = fields.Char('Email')
#     date = fields.Date('Date')
#     is_company = fields.Boolean('Is a company')
#     parent_id = fields.Many2one('res.partner', 'Related Company')
#     child_ids = fields.One2many('res.partner', 'parent_id',
#                                 'Contacts')
#     
#     val1 = {'name': u'Eric Idle',
#         'email': u'eric.idle@example.com'
#         'date': today_str}
#     
#     val2 = {'name': u'John Cleese',
#         'email': u'john.cleese@example.com',
#         'date': today_str}
#     
#     partner_val = {
#         'name': u'Flying Circus',
#         'email': u'm.python@example.com',
#         'date': today_str,
#         'is_company': True,
#         'child_ids': [(0, 0, val1),
#                         (0, 0, val2),
#                         ]
#         }
#     
#     record = self.env['res.partner'].create(partner_val)

    # Updating values of recordset records
    @api.model
    def add_contacts(self, partner, contacts):
        partner.ensure_one()
        if contacts:
            partner.date = fields.Date.context_today()
            partner.child_ids |= contacts

    # Searching for records
    @api.model
    def find_partners_and_contacts(self, name):
        partner = self.env['res.partner']
        domain = ['|',
            '&',
            ('is_company', '=', True),
            ('name', 'like', name),
            '&',
            ('is_company', '=', False),
            ('parent_id.name', 'like', name)
            ]
        return partner.search(domain)
    
    # Filtering recordsets
    @api.model
    def partners_with_email(self, partners):
        def predicate(partner):
            if partner.email:
                return True
            return False
        return partners.filter(predicate)
        # return partners.filter(lambda p: p.email)
    
    # Traversing recordset relations
    @api.model
    def get_email_addresses(self, partner):
        partner.ensure_one()
        return partner.mapped('child_ids.email')
    
    @api.model
    def get_companies(self, partners):
        return partners.mapped('parent_id')
    
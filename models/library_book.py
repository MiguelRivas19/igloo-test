# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.fields import Date as fDate
from datetime import timedelta as td


class LibraryBook(models.Model):
    _name = 'library.book'

    name = fields.Char('Title', required=True)
    date_release = fields.Date(
        'Release Date',
        groups='igloo-test.group_release_dates')
    author_ids = fields.Many2many('res.partner',
                                  string='Authors')

    short_name = fields.Char(
        string='Short Title',
        size=100,
        translate=False)
    notes = fields.Text('Internal Notes')
    description = fields.Html(
        string='Description',
        sanitize=True,
        strip_style=False,
        translate=False)
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date')
    date_updated = fields.Datetime('Last Updated')
    pages = fields.Integer('Number of Pages')
    reader_rating = fields.Float(
        'Reader Average Rating',
        (14, 4))
    
    # Adding relational fields to a Model
    publisher_id = fields.Many2one(
        'res.partner', string='Publisher',
        # optional:
        ondelete='set null',
        context={},
        domain=[],
        )
    
    author_ids = fields.Many2many(
        'res.partner', string='Authors')
    
    # Adding constraint validations to a Model
    @api.constrains('date_release')
    def _check_release_date(self):
        for r in self:
            if r.date_release > fields.Date.today():
                raise models.ValidationError(
                    'Release date must be in the past')
                
    # Adding computed fields to a Model
    age_days = fields.Float(
        string='Days Since Release',
        compute='_compute_age',
        inverse='_inverse_age',
        search='_search_age',
        store=False,
        compute_sudo=False,
        )
    
    @api.depends('date_release')
    def _compute_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            delta = (fDate.from_string(book.date_release -
                                       today))
            book.age_days = delta.days

    def _inverse_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            d = td(days=book.age_days) - today
            book.date_release = fDate.to_string(d)
        
    def _search_age(self, operator, value):
        today = fDate.from_string(fDate.today())
        value_days = td(days=value)
        value_date = fDate.to_string(today - value_days)
        return [('date_release', operator, value_date)]
    
    # Exposing Related fields stored in other models
    publisher_city = fields.Char(
        'Publisher City',
        related='publisher_id.city')
    
    # Adding dynamic relations using Reference fields
    @api.model
    def _referencable_models(self):
        models = self.env['res.request.link'].search([])
        return [(x.object, x.name) for x in models]
        
    ref_doc_id = fields.Reference(
        selection='_referencable_models',
        string='Reference Document')
    
    # Using Abstract Models for reusable Model features
    _inherit = ['base.archive']
    
    # Chapitre 5: Basic Server Side Development
    
    # Defining model methods and use the API decorators
    state = fields.Selection([('draft', 'Unavailable'),
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost')],
        'State')
    
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed= [('draft', 'available'),
            ('available', 'borrowed'),
            ('borrowed', 'available'),
            ('available', 'lost'),
            ('borrowed', 'lost'),
            ('lost', 'available')]
        return (old_state, new_state) in allowed
    
    @api.multi
    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                continue
            
    # Obtaining an empty recordset for a different model
    @api.model
    def get_all_library_members(self):
        library_member_model = self.env['library.member']
        return library_member_model.search([])


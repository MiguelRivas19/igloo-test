# -*- coding: utf-8 -*-
from openerp import models, fields, api


class LibraryLoanWizard(models.TransientModel):
    _name = 'library.loan.wizard'
    member_id = fields.Many2one('library.member', 'Member')
    book_ids = fields.Many2many('library.book', 'Books')
    
    @api.multi
    def record_loans(self):
        for wizard in self:
            member = wizard.member_id
            books = wizard.book_ids
            loan = self.env['library.book.loan']
            for book in books:
                loan.create({'member_id': member.id,
                             'book_id': book.id})

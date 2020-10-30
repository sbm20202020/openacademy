# -*- coding: utf-8 -*-

# from odoo import models, fields, api

# class openacademy_starly(models.Model):
#     _name = 'openacademy_starly.openacademy_starly'
#     _description = 'openacademy_starly.openacademy_starly'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from datetime import timedelta
from odoo import models,fields,api,exceptions

class Course(models.Model):
    _name = 'openacademy.course'
    _description = "OpenAcademy Courses"

    name = fields.Char(string="Titre", required=True)
    description = fields.Text()

    responsable_id = fields.Many2one('res.users',ondelete='set null', string="Responsable", index=True)
    session_ids = fields.One2many('openacademy.session', 'cours_id', string="Sessions")
        
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count([('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "Le Titre du cours et La Description ne doivent pas etre identique "),

        ('name_unique',
         'UNIQUE(name)',
         "Le titre du cours doit etre unique"),
    ]

class Professeur(models.Model):
    _name = 'openacademy.professeur'
    _telephone = "OpenAcademy Telephone"

    name = fields.Char(string="nom", required=True)
    telephone = fields.Char(string="telephone", required=True)
    adresse = fields.Text(string="adresse")

class Session(models.Model):
    _name = 'openacademy.session'
    _description = "OpenAcademy Sessions"

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)
    color = fields.Integer()    

    instructor_id = fields.Many2one('res.partner', string="Professeur_instructeur")
    cours_id = fields.Many2one('openacademy.course',ondelete='cascade', string="COURS OPENACADEMY", required=True)
    participants_ids = fields.Many2many('res.partner', string="Participants")

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    end_date = fields.Date(string="End Date", store=True,compute='_get_end_date', inverse='_set_end_date')
    attendees_count = fields.Integer(string="PARTICIPATION PAR COURS", compute='_get_attendees_count', store=True)

    @api.depends('seats', 'participants_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.participants_ids) / r.seats
    
    @api.onchange('seats', 'participants_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            
            return {
                'warning': {
                    'title': "Nombre de Place Incorrect",
                    'message': "Le nombre de place disponible ne doit pas etre Negatif !",
                },  
            }

        if self.seats < len(self.participants_ids):
            return {
                'warning': {
                    'title': "Participants en surnombre",
                    'message': "Augmenter la capacite d'accueil ou Réduisez le nombre de participants !",
              },
            }
        
    @api.constrains('instructor_id', 'participants_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.participants_ids:
                raise exceptions.ValidationError("L'instructeur de la session ne peut pas etre participant")
    
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            r.duration = (r.end_date - r.start_date).days + 1
            
    @api.depends('participants_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.participants_ids)
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class Pantalla(models.Model):
    _name = 'plaiaundi.pantalla'
    _description = 'plaiaundi.pantalla'
    _rec_name = "code"

    code = fields.Char(String="Code")
    brand = fields.Char(String="Brand")
    resolution = fields.Float(String="Resolution")
    alumno_id = fields.Many2one("plaiaundi.alumno", "Alumno", ondelete='set null', inverse_name="pantalla_id")
    incidencias = fields.Text()
    _sql_constraints = [('pantalla_module_uniq', 'unique(code)', "Ya existe una pantalla con este código.")]

class Pc(models.Model):
    _name = 'plaiaundi.pc'
    _description = 'plaiaundi.pc'
    _rec_name = "code"

    code = fields.Char(string="Code")
    type = fields.Selection([("Portatil", "Portatil"),("Sobremesa","Sobremesa")],string="Tipo")
    alumno_id = fields.Many2one("plaiaundi.alumno", "Alumno", ondelete='cascade', inverse_name="pc_id")
    incidencias = fields.Text()
    _sql_constraints = [('pc_module_uniq', 'unique(code)', "Ya existe una pc con este código.")]
    
class Alumno(models.Model):
    _name = 'plaiaundi.alumno'
    _description = 'plaiaundi.alumno'

    name = fields.Char()
    surname = fields.Char()
    email = fields.Char()
    age = fields.Integer()
    pantalla_id = fields.Many2one('plaiaundi.pantalla', 'Pantalla', ondelete="set null")
    pc_id = fields.Many2one('plaiaundi.pc', 'Pc', ondelete="set null")
    aula_id = fields.Many2one('plaiaundi.aula', 'Aula', ondelete="set null")
    _sql_constraints = [('pantalla_id_module_uniq', 'unique(pantalla_id)', "Ya existe un alumno con esta pantalla."), ('pc_id_module_uniq', 'unique(pc_id)', "Ya existe un alumno con este pc.")] 

    @api.model
    def create(self, vals):
        record = super(Alumno, self).create(vals)
        pantalla = self.env['plaiaundi.pantalla']
        if pantalla:
            pantalla.write({'alumno_id': record.id})
        return record
    @api.model
    def create(self, vals):
        if 'age' in vals and (vals['age'] < 0):
            raise exceptions.ValidationError("Age must be higher than 0.")
        return super().create(vals)

    def write(self, vals):
        if 'age' in vals and (vals['age'] < 0):
            raise exceptions.ValidationError("Age must be higher than 0.")
        return super().write(vals)   

class Aula(models.Model):
    _name = 'plaiaundi.aula'
    _description = 'plaiaundi.aula'
    _rec_name = "code"

    code = fields.Char()
    capacity = fields.Integer()
    _sql_constraints = [('aula_module_uniq', 'unique(code)', "Ya existe un aula con este código.")]

class Faltas(models.Model):
    _name='plaiaundi.faltas'
    _description = 'plaiaundi.faltas'
    _rec_name = "alumno_id"

    alumno_id = fields.Many2one("plaiaundi.alumno", "Alumno", ondelete='cascade')
    term = fields.Selection([("Primer trimestre", 'Primer trimestre'), ('Segundo trimestre', 'Segundo trimestre'), ('Tercer trimestre', 'Tercer trimestre')],string = "Term")
    subject = fields.Selection([("Matematicas", 'Matematicas'), ('Literatura', 'Literatura'), ('Ciencia', 'Ciencia'), ('PE', 'PE'), ('IT', 'IT')],string = "Asignatura")
    num_faltas = fields.Integer()
    _sql_constraints = [('alummo_term_asignaturas_faltas', 'unique(subject,alumno_id, term)', "You can olny put one term per student!")
    ]
    @api.model
    def create(self, vals):
        if 'num_faltas' in vals and (vals['num_faltas'] < 0):
            vals['maths']=0
            raise exceptions.ValidationError("Can`t be a negative number")
        return super().create(vals)

    def write(self, vals):
        if 'num_faltas' in vals and (vals['num_faltas'] < 0):
            vals['maths']=0
            raise exceptions.ValidationError("Can`t be a negative number")
        return super().write(vals)

class Calificaciones(models.Model):
    _name = 'plaiaundi.calificaciones'
    _description = 'plaiaundi.calificaciones'
    _rec_name = "alumno_id"

    alumno_id = fields.Many2one("plaiaundi.alumno", "Alumno", ondelete='set null')
    term = fields.Selection([("Primer trimestre", 'Primer trimestre'), ('Segundo trimestre', 'Segundo trimestre'), ('Tercer trimestre', 'Tercer trimestre')],string = "Term")
    maths = fields.Float(string="Matematicas",min=0.0, max=10.0)
    literature = fields.Float(string ="Literatura",min=0.0, max=10.0)
    science = fields.Float(string ="Ciencia",min=0.0, max=10.0)
    pe = fields.Float(string="Educacion Fisica",min=0.0, max=10.0)
    it = fields.Float(string="Infor",min=0.0, max=10.0)
    
    avg = fields.Float(string ="Media", compute="_value_avg", store=True)
    _sql_constraints = [
        ('unique_alumno_id_term', 'unique(alumno_id, term)', "You can olny put one term per student!")
    ]
    @api.depends('maths','literature','science','pe','it')
    def _value_avg(self):
        for record in self:
            record.avg = round((float(record.maths)+float(record.literature)+float(record.science)+float(record.pe)+float(record.it)) / 5 , 2)

    @api.model
    def create(self, vals):
        if 'maths' in vals and (vals['maths'] < 0 or vals['maths'] > 10):
            vals['maths']=0
            raise exceptions.ValidationError("The marks must be between 0 and 10.")
        elif 'literature' in vals and (vals['literature'] < 0 or vals['literature'] > 10):
            vals['literature']=0
            raise exceptions.ValidationError("The marks must be between 0 and 10.")
        elif 'science' in vals and (vals['science'] < 0 or vals['science'] > 10):
            vals['science']=0
            raise exceptions.ValidationError("The marks must be between 0 and 10.")
        elif 'pe' in vals and (vals['pe'] < 0 or vals['pe'] > 10):
            vals['pe']=0
            raise exceptions.ValidationError("The marks must be between 0 and 10.")
        elif 'it' in vals and (vals['it'] < 0 or vals['it'] > 10):
            vals['it']=0
            raise exceptions.ValidationError("The marks must be between 0 and 10.")
        return super().create(vals)

    def write(self, vals):
        if 'maths' in vals and (vals['maths'] < 0 or vals['maths'] > 10):
            vals['maths']=0
            raise exceptions.ValidationError("The marks must be between 0 and 10.")
        elif 'literature' in vals and (vals['literature'] < 0 or vals['literature'] > 10):
            vals['literature']=0
            raise exceptions.ValidationError("The marks must be between 0 and 10.")
        elif 'science' in vals and (vals['science'] < 0 or vals['science'] > 10):
            vals['science']=0
            raise exceptions.ValidationError("The marks must be between 0 and 10.")
        elif 'pe' in vals and (vals['pe'] < 0 or vals['pe'] > 10):
            vals['pe']=0
            raise exceptions.ValidationError("The marks must be between 0 and 10.")
        elif 'it' in vals and (vals['it'] < 0 or vals['it'] > 10):
            vals['it']=0
            raise exceptions.ValidationError("The marks must be between 0 and 10.")
        return super().write(vals)
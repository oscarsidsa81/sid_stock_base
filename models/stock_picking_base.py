from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    sid_asignado = fields.Many2one("res.users", string="Asignado")
    sid_completado = fields.Boolean(string="Completado")
    sid_enviar = fields.Boolean(string="Enviar")
    sid_modifica = fields.Text(string="Modifica")
    sid_motivo = fields.Text(string="Motivo")
    sid_pagina_final = fields.Boolean(string="Página final")

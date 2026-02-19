from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    sid_asignado = fields.Many2one("res.users", string="Asignado (SID)")
    sid_completado = fields.Boolean(string="Completado (SID)")
    sid_enviar = fields.Boolean(string="Enviar (SID)")
    sid_modifica = fields.Text(string="Modifica (SID)")
    sid_motivo = fields.Text(string="Motivo (SID)")
    sid_pagina_final = fields.Boolean(string="Página final (SID)")

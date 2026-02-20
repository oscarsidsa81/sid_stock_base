# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    # --- Campos base (sin prefijo x_) ---
    # Nota: si en BD existen campos Studio (x_*) equivalentes, el módulo legacy se encarga de copiar valores.

    sid_ayudante = fields.Many2one(
        comodel_name="res.users",
        string="Ayudante",
    )
    sid_coladas = fields.Char(string="Coladas")
    sid_color = fields.Integer(string="Color")

    sid_tags_activities = fields.Many2many (
        comodel_name="sid.stock.move.tag",
        relation="stock_move_sid_tags_rel",
        column1="move_id",
        column2="tag_id",
        string="Tags actividades",
    )

    # Campos de ubicación heredados del producto (para filtros/searchpanel)
    # (readonly/store porque vienen del producto)
    sid_pasillo = fields.Many2one (
        comodel_name="sid.location.option",
        related="product_id.product_tmpl_id.sid_pasillo",
        store=True,
        readonly=True,
        string="Pasillo",
    )
    sid_alto = fields.Many2one (
        comodel_name="sid.location.option",
        related="product_id.product_tmpl_id.sid_alto",
        store=True,
        readonly=True,
        string="Alto",
    )
    sid_lado = fields.Many2one (
        comodel_name="sid.location.option",
        related="product_id.product_tmpl_id.sid_lado",
        store=True,
        readonly=True,
        string="Lado",
    )
    sid_largo = fields.Many2one (
        comodel_name="sid.location.option",
        related="product_id.product_tmpl_id.sid_largo",
        store=True,
        readonly=True,
        string="Largo",
    )

    @api.depends(
        "product_id",
        "product_id.product_tmpl_id",
        "product_id.product_tmpl_id.sid_pasillo",
        "product_id.product_tmpl_id.sid_alto",
        "product_id.product_tmpl_id.sid_lado",
        "product_id.product_tmpl_id.sid_largo",
    )
    def _compute_sid_dimensions(self):
        for m in self:
            tmpl = m.product_id.product_tmpl_id
            m.sid_pasillo = tmpl.sid_pasillo if tmpl else False
            m.sid_alto = tmpl.sid_alto if tmpl else False
            m.sid_lado = tmpl.sid_lado if tmpl else False
            m.sid_largo = tmpl.sid_largo if tmpl else False

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
        tracking=False,
    )
    sid_coladas = fields.Char(string="Coladas", tracking=False)
    sid_color = fields.Integer(string="Color", tracking=False)
    sid_item = fields.Char(string="Item", tracking=False)

    sid_tags_activities = fields.Many2many(
        comodel_name="x_stock.move.tags",
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

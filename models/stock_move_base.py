# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = "stock.move"

    family = fields.Char(string="Familia", store=True, readonly=True, related="product_id.family.display_name")
    sid_AXI = fields.Char(string="Referencia AXI", readonly=True, related="product_id.product_tmpl_id.sid_AXI", store=True )
    sid_ayudante = fields.Many2one(
        comodel_name="res.users",
        string="Ayudante",
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



# class StockMoveSidLine(models.Model): TODO hay que ver meter esto en un módulo individual aparte
#     _inherit = "stock.move.line"
#
#     desc_picking = fields.Text(string="Desc. en Albarán", readonly=True, tracking=True, related="move_id.description_picking")
#     item = fields.Char(string="Item", store=True,readonly=True, tracking=True, related="move_id.item")
#     move_demanda = fields.Float(string="Demanda", readonly=True, help="Trae el valor demandado de stock.move", related="move_id.product_uom_qty")
#     related_purchase = fields.Many2one("purchase.order", string="Compra", store=True, readonly=True, related="move_id.purchase_line_id.order_id")
#     proveedor = fields.Many2one("res.partner", string="Proveedor", store=True, readonly=True, related="move_id.purchase_line_id.order_id.partner_id")

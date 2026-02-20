# -*- coding: utf-8 -*-

from odoo import fields, models


class SidStockMoveTag(models.Model):
    """Sustituto "normal" del modelo Studio x_stock.move.tags.

    Lo dejamos deliberadamente simple: sólo el nombre.
    """

    _name = "sid.stock.move.tag"
    _description = "SID Stock Move Tag"
    _order = "name"

    name = fields.Char(required=True, index=True)
    color = fields.Integer(stored=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("name_uniq", "unique(name)", "El nombre del tag debe ser único."),
    ]

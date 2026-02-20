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

    def _sid_prioridad_linea_selection(self):
        """Intenta reutilizar la selección real del campo Studio x_prioridad_linea.

        - Si existe x_prioridad_linea y tiene selection_ids (Studio), devolvemos exactamente esos valores.
        - Si no, devolvemos una selección mínima para que el campo sea instalable.
        """
        try:
            fld = self.env["ir.model.fields"].sudo().search(
                [("model", "=", "stock.move"), ("name", "=", "x_prioridad_linea")],
                limit=1,
            )
            if fld and fld.selection_ids:
                return [(s.value, s.name) for s in fld.selection_ids.sorted("sequence")]
        except Exception:
            _logger.exception("No se pudo leer la selección de x_prioridad_linea desde ir.model.fields")

        _logger.warning(
            "No se encontraron selection_ids para stock.move.x_prioridad_linea. "
            "Se usa selección mínima de fallback para permitir instalación."
        )
        return [("normal", "Normal"), ("alta", "Alta")]

    sid_prioridad_linea = fields.Selection(
        selection=_sid_prioridad_linea_selection,
        string="Prioridad",
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
    sid_pasillo = fields.Selection(
        related="product_id.product_tmpl_id.sid_pasillo",
        store=True,
        readonly=True,
        string="Pasillo",
    )
    sid_alto = fields.Selection(
        related="product_id.product_tmpl_id.sid_alto",
        store=True,
        readonly=True,
        string="Alto",
    )
    sid_lado = fields.Selection(
        related="product_id.product_tmpl_id.sid_lado",
        store=True,
        readonly=True,
        string="Lado",
    )
    sid_largo = fields.Selection(
        related="product_id.product_tmpl_id.sid_largo",
        store=True,
        readonly=True,
        string="Largo",
    )

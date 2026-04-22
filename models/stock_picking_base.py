from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    sid_asignado = fields.Many2one("res.users", string="Asignado", help="Campo para asociar un usuario a completar el albarán", domain=lambda self: [('department_id', '=', self.env.ref('hr.department_warehouse').id)])
    sid_completado = fields.Boolean(string="Completado", help="Se utiliza para indicar que el albarán continuará con el alcance parcial definido en ese momento")
    sid_enviar = fields.Boolean(string="Enviar", help="Campo para indicar que está listo para enviar, y permite emitir un albarán al chatter con el botón Agencias PDF")
    pedido_cliente = fields.Char(string="Ref. Pedido", store=True, readonly=True, related="sale_id.client_order_ref")
    sid_cliente = fields.Many2one(string="Cliente", store=True, tracking=True, readonly=True, comodel_name="res.partner", related="sale_id.partner_id")
    sid_motivo = fields.Text(string="Motivo", help="Campo para describir el motivo de una devolución")
    sid_motivo_requerido = fields.Boolean(string="Boleano de Motivo", compute="_compute_motivo_required", store=False)
    qty_done_pct = fields.Float(string="Progreso Picking", readonly=True, help="Muestra el % de sid_hecho vs sid_demandada", compute="_compute_sid_qty_done")
    is_return = fields.Boolean(compute="_compute_is_return", store=False)
    sid_scope_summary = fields.Text(string="Resumen de Alcance", compute="_compute_sid_scope_summary", store=False, readonly=True)

    @api.depends ( "state", "move_ids_without_package.product_uom_qty",
                   "move_ids_without_package.quantity_done",
                   "move_ids_without_package.product_id.family",
                   "move_ids_without_package.product_id.categ_id",
                   "move_ids_without_package.product_id.categ_id.name" )
    def _compute_sid_scope_summary(self) :
        for record in self :
            if record.state in ("done", "draft") :
                record.sid_scope_summary = ""
                continue

            moves = record.move_ids_without_package

            groups = [
                ("PIPES", lambda m : "pipe" in (
                            m.product_id.categ_id.name or "").lower (), "m",
                 2),
                ("FLANGES", lambda m : "flange" in (
                            m.product_id.categ_id.name or "").lower (), "ud",
                 0),
                ("BW", lambda m : "bw" in (
                            m.product_id.categ_id.name or "").lower (), "ud",
                 0),
                ("FORGED", lambda m : "forged" in (
                            m.product_id.categ_id.name or "").lower (), "ud",
                 0),
                ("OTHERS",
                 lambda m : (m.product_id.family or "") not in ("FORGED", "BW",
                                                                "PIPE",
                                                                "FLANGE"),
                 "ud", 0),
            ]

            lines = []
            for label, predicate, unit, decimals in groups :
                filtered = moves.filtered ( predicate )
                if not filtered :
                    continue

                qty_plan = round (
                    sum ( filtered.mapped ( "product_uom_qty" ) ), decimals )
                qty_done = round ( sum ( filtered.mapped ( "quantity_done" ) ),
                                   decimals )

                # Si quieres ocultar cuando qty_plan = 0:
                if qty_plan == 0 :
                    continue

                count = len ( filtered )
                lines.append (
                    f"({qty_plan}/{qty_done} {unit}) {count} {label}" )

            record.sid_scope_summary = "\n".join ( lines )


    @api.depends ("picking_type_id")
    def _compute_is_return(self):
        # Tipos que son "return_picking_type_id" de algún picking type
        return_types = self.env["stock.picking.type"].search([
            ("return_picking_type_id", "!=", False)
        ]).mapped("return_picking_type_id")

        return_type_ids = set(return_types.ids)

        for picking in self:
            picking.is_return = picking.picking_type_id.id in return_type_ids

    @api.depends ( "state", "picking_type_id", "is_return" )
    def _compute_motivo_required(self) :
        for rec in self :
            rec.sid_motivo_requerido = (
                    rec.state not in ("draft", "done", "cancel")
                    and rec.is_return is True
            )

    @api.depends ( "move_lines.picking_id", "move_lines.quantity_done")
    def _compute_sid_qty_done (self) :
        for record in self :
            if record.state not in ('done', 'draft','cancel'):
                sid_hecho = (round ( sum ( self.env['stock.move'].search (
                    [('picking_id', "=", record.id), ] ).mapped (
                    'quantity_done' ) ), 2 ))
                sid_demandada = (round ( sum ( self.env['stock.move'].search (
                    [('picking_id', "=", record.id), ] ).mapped (
                    'product_uom_qty' ) ), 2 ))
                if sid_hecho != 0 and sid_demandada != 0 :
                    record['qty_done_pct'] = sid_hecho / sid_demandada * 100
                else :
                    record['qty_done_pct'] = 0
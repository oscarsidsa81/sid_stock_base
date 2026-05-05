from odoo import SUPERUSER_ID, api


def post_init_register_warehouse_xmlid(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    legacy = env["ir.model.data"].sudo().search(
        [("module", "=", "hr.department"), ("name", "=", "warehouse")],
        limit=1,
    )
    if not legacy or not legacy.res_id:
        return

    dept = env["hr.department"].browse(legacy.res_id)
    env["ir.model.data"]._update_xmlids(
        [
            {
                "xml_id": "sid_stock_base.department_warehouse",
                "record": dept,
                "noupdate": True,
            }
        ]
    )

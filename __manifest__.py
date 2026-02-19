# -*- coding: utf-8 -*-
{
    "name": "sid_stock_base",
    "summary": "Campos base y estructura mínima para personalizaciones de Stock (sin Studio).",
    "description": """
SID Stock Base
==============

Módulo base para centralizar campos y estructura mínima de stock, con filosofía migrable:
- Campos base con prefijo sid_
- Sin vistas ni acciones (solo modelo)
- Preparado para módulos legacy/views/logic posteriores
""",
    "version": "15.0.1.0.1",
    "category": "Inventory/Inventory",
    "author": "SIDSA",
    "website": "",
    "license": "LGPL-3",
    "depends": [
        "stock",
        "mail",
        "sale_stock",
        "purchase_stock",
        "sid_product_base",
        "oct_product_extra_fields",
    ],
    "data": [
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}

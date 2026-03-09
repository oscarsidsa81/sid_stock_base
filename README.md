# sid_stock_base

## Propósito
Módulo base que centraliza **campos estructurales y lógica auxiliar de Stock** evitando dependencias de campos creados con Studio.

Amplía principalmente los modelos:

- `stock.move`
- `stock.move.line`
- `stock.picking`

El objetivo es proporcionar una **estructura mínima estable para personalizaciones de inventario**, reutilizable por otros módulos del proyecto.

---

## Modelos extendidos

### `stock.move`

Campos principales añadidos:

- `family`  
  Familia del producto (related a `product_id.family.display_name`).

- `sid_coladas_masivo`  
  Campo de entrada masiva para coladas que permite generar múltiples `stock.move.line`.

- `sid_AXI`  
  Referencia AXI del producto (related al template del producto).

- `sid_ayudante`  
  Usuario ayudante asociado al movimiento.

- `sid_color`  
  Campo auxiliar para codificación o clasificación visual.

- `sid_tags_activities`  
  Etiquetas de actividad asociadas al movimiento (`Many2many` con `sid.stock.move.tag`).

Campos de ubicación heredados del producto (para filtros y searchpanel):

- `sid_pasillo`
- `sid_alto`
- `sid_lado`
- `sid_largo`

Estos campos se almacenan (`store=True`) para permitir:

- filtros
- agrupaciones
- searchpanel en vistas

---

### `stock.move.line`

Campos auxiliares derivados del movimiento:

- `desc_picking`  
  Descripción mostrada en el albarán.

- `item`  
  Identificador de ítem del movimiento.

- `move_demanda`  
  Cantidad demandada en el movimiento.

- `family`  
  Familia del producto.

- `related_purchase`  
  Pedido de compra relacionado.

- `proveedor`  
  Proveedor asociado al pedido de compra.

---

### `stock.picking`

Campos funcionales para gestión operativa de albaranes:

- `sid_asignado`  
  Usuario responsable del albarán.

- `sid_completado`  
  Indicador de que el albarán se gestionará parcialmente.

- `sid_enviar`  
  Flag para indicar que el albarán está listo para enviar.

- `sid_modifica`  
  Campo de seguimiento para modificaciones.

- `pedido_cliente`  
  Referencia de pedido del cliente (related).

- `sid_cliente`  
  Cliente del albarán.

- `sid_motivo`  
  Motivo de devolución.

- `sid_motivo_requerido`  
  Campo calculado que obliga a indicar motivo en devoluciones.

- `sid_pagina_final`  
  Indica si se debe mostrar la página final en el PDF del albarán.

- `sid_address`  
  Dirección de entrega calculada a partir del partner.

- `qty_done_pct`  
  Porcentaje de progreso del picking.

- `is_return`  
  Identificador de albaranes de devolución.

- `sid_scope_summary`  
  Resumen automático del contenido del albarán agrupado por tipo de producto.

---

## Seguridad

Incluye permisos básicos en:

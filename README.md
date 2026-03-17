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

---

## Migracion de datos legacy

Este modulo define la estructura final en codigo, pero no ejecuta automaticamente la migracion de datos historicos desde campos Studio (`x_*`).

Para migrar esos datos existe el fichero:

`sql/backfill_sid_stock_base.sql`

### Cuando ejecutarlo

Debe ejecutarse unicamente:

1. despues de instalar `sid_stock_base`
2. despues de comprobar que las columnas `sid_*` ya existen
3. antes de eliminar los campos `x_*`

### Que hace

Copia los siguientes campos:

#### `stock.picking`
- `x_asignado -> sid_asignado`
- `x_completado -> sid_completado`
- `x_enviar -> sid_enviar`
- `x_modifica -> sid_modifica`
- `x_motivo -> sid_motivo`
- `x_pagina_final -> sid_pagina_final`

#### `stock.move`
- `x_ayudante -> sid_ayudante`

### Que no hace

No migra automaticamente:

- campos related
- campos calculados por relaciones
- otros campos `x_*` que no tengan destino real en `sid_stock_base`

### Orden recomendado

1. actualizar codigo del modulo
2. actualizar lista de apps
3. instalar `sid_stock_base`
4. ejecutar `sql/backfill_sid_stock_base.sql`
5. revisar validaciones finales
6. solo despues plantear limpieza de Studio

### Ejecucion manual del SQL

El fichero SQL se guarda dentro del modulo para dejar trazabilidad y versionado, pero **Odoo no lo ejecuta automaticamente**.

Se puede lanzar, por ejemplo, con `psql`:

```bash
psql -h <host> -U <usuario> -d <base_de_datos> -f /ruta/addons/sid_stock_base/sql/backfill_sid_stock_base.sql
```

Tambien puede ejecutarse por bloques desde DBeaver, pgAdmin u otra herramienta SQL. Se recomienda ejecutar primero los `SELECT` de validacion, luego los `UPDATE` y finalmente las validaciones posteriores.

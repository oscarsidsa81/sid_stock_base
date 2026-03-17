-- =========================================================
-- sid_stock_base - migracion legacy x_* -> sid_*
-- =========================================================
--
-- Objetivo:
--   Copiar valores historicos de campos Studio (x_*)
--   a campos definidos en codigo (sid_*) despues de instalar
--   el modulo sid_stock_base.
--
-- Importante:
--   - Este fichero NO se ejecuta automaticamente por Odoo.
--   - Debe ejecutarse manualmente sobre la base de datos.
--   - Ejecutar solo DESPUES de instalar sid_stock_base.
--
-- Flujo recomendado:
--   1) instalar sid_stock_base
--   2) ejecutar primero los SELECT de validacion
--   3) ejecutar los UPDATE
--   4) revisar validaciones finales
--
-- =========================================================

-- =========================================================
-- 1. VALIDACION PREVIA
-- =========================================================

SELECT count(*) AS pending_sid_asignado
FROM stock_picking
WHERE x_asignado IS NOT NULL
  AND sid_asignado IS NULL;

SELECT count(*) AS pending_sid_completado
FROM stock_picking
WHERE x_completado IS NOT NULL
  AND sid_completado IS NULL;

SELECT count(*) AS pending_sid_enviar
FROM stock_picking
WHERE x_enviar IS NOT NULL
  AND sid_enviar IS NULL;

SELECT count(*) AS pending_sid_modifica
FROM stock_picking
WHERE x_modifica IS NOT NULL
  AND (sid_modifica IS NULL OR sid_modifica = '');

SELECT count(*) AS pending_sid_motivo
FROM stock_picking
WHERE x_motivo IS NOT NULL
  AND (sid_motivo IS NULL OR sid_motivo = '');

SELECT count(*) AS pending_sid_pagina_final
FROM stock_picking
WHERE x_pagina_final IS NOT NULL
  AND sid_pagina_final IS NULL;

SELECT count(*) AS pending_sid_ayudante
FROM stock_move
WHERE x_ayudante IS NOT NULL
  AND sid_ayudante IS NULL;

-- =========================================================
-- 2. MIGRACION stock.picking
-- =========================================================

UPDATE stock_picking
SET sid_asignado = x_asignado
WHERE x_asignado IS NOT NULL
  AND sid_asignado IS NULL;

UPDATE stock_picking
SET sid_completado = x_completado
WHERE x_completado IS NOT NULL
  AND sid_completado IS NULL;

UPDATE stock_picking
SET sid_enviar = x_enviar
WHERE x_enviar IS NOT NULL
  AND sid_enviar IS NULL;

UPDATE stock_picking
SET sid_modifica = x_modifica
WHERE x_modifica IS NOT NULL
  AND (sid_modifica IS NULL OR sid_modifica = '');

UPDATE stock_picking
SET sid_motivo = x_motivo
WHERE x_motivo IS NOT NULL
  AND (sid_motivo IS NULL OR sid_motivo = '');

UPDATE stock_picking
SET sid_pagina_final = x_pagina_final
WHERE x_pagina_final IS NOT NULL
  AND sid_pagina_final IS NULL;

-- =========================================================
-- 3. MIGRACION stock.move
-- =========================================================

UPDATE stock_move
SET sid_ayudante = x_ayudante
WHERE x_ayudante IS NOT NULL
  AND sid_ayudante IS NULL;

-- =========================================================
-- 4. VALIDACION POSTERIOR
-- =========================================================

SELECT count(*) AS remaining_sid_asignado
FROM stock_picking
WHERE x_asignado IS NOT NULL
  AND sid_asignado IS NULL;

SELECT count(*) AS remaining_sid_completado
FROM stock_picking
WHERE x_completado IS NOT NULL
  AND sid_completado IS NULL;

SELECT count(*) AS remaining_sid_enviar
FROM stock_picking
WHERE x_enviar IS NOT NULL
  AND sid_enviar IS NULL;

SELECT count(*) AS remaining_sid_modifica
FROM stock_picking
WHERE x_modifica IS NOT NULL
  AND (sid_modifica IS NULL OR sid_modifica = '');

SELECT count(*) AS remaining_sid_motivo
FROM stock_picking
WHERE x_motivo IS NOT NULL
  AND (sid_motivo IS NULL OR sid_motivo = '');

SELECT count(*) AS remaining_sid_pagina_final
FROM stock_picking
WHERE x_pagina_final IS NOT NULL
  AND sid_pagina_final IS NULL;

SELECT count(*) AS remaining_sid_ayudante
FROM stock_move
WHERE x_ayudante IS NOT NULL
  AND sid_ayudante IS NULL;

-- =========================================================
-- 5. MUESTRAS DE CONTROL
-- =========================================================

SELECT id, name, x_asignado, sid_asignado, x_completado, sid_completado
FROM stock_picking
WHERE x_asignado IS NOT NULL
   OR x_completado IS NOT NULL
ORDER BY id DESC
LIMIT 20;

SELECT id, x_ayudante, sid_ayudante
FROM stock_move
WHERE x_ayudante IS NOT NULL
ORDER BY id DESC
LIMIT 20;

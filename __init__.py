from . import models
from .hooks import post_init_register_warehouse_xmlid

# Backward-compatible alias for databases or manifests that still reference the
# generic hook name.
post_init_hook = post_init_register_warehouse_xmlid

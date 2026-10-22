"""Utilidades compartidas del backend."""

from __future__ import annotations

import re

# Formato seguro para nombres de schema de tenant: tenant_<12 caracteres hex>
SAFE_SCHEMA_PATTERN = r"^tenant_[a-f0-9]{12}$"
SAFE_SCHEMA_REGEX = re.compile(SAFE_SCHEMA_PATTERN)

# Formato de slug de restaurante: ^[a-z0-9-]{3,40}$
SAFE_SLUG_PATTERN = r"^[a-z0-9-]{3,40}$"
SAFE_SLUG_REGEX = re.compile(SAFE_SLUG_PATTERN)


def is_valid_schema_name(schema_name: str) -> bool:
    return bool(SAFE_SCHEMA_REGEX.match(schema_name))


def is_valid_tenant_slug(slug: str) -> bool:
    return bool(SAFE_SLUG_REGEX.match(slug))


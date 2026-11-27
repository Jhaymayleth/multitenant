"""Pruebas unitarias de validación del catálogo."""

import uuid

import pytest
from pydantic import ValidationError

from app.menus.schemas import CategoryCreate, ProductCreate, ProductUpdate


def test_price_must_be_greater_than_zero():
    category_id = uuid.uuid4()
    ProductCreate(category_id=category_id, name="Café", price_cents=1)
    with pytest.raises(ValidationError):
        ProductCreate(category_id=category_id, name="Café", price_cents=0)
    with pytest.raises(ValidationError):
        ProductUpdate(category_id=category_id, name="Café", price_cents=0)


def test_name_length_is_enforced():
    with pytest.raises(ValidationError):
        CategoryCreate(name="A")
    with pytest.raises(ValidationError):
        ProductCreate(category_id=uuid.uuid4(), name="", price_cents=100)

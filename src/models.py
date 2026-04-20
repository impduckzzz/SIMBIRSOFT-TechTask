from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True)
class ProductCard:
    name: str
    price: Decimal
    url: str


@dataclass(frozen=True)
class CartItem:
    name: str
    unit_price: Decimal
    quantity: int
    total_price: Decimal
    quantity_input_id: str
    remove_url: str
    options: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class CartSummary:
    subtotal: Decimal
    adjustments: Decimal
    total: Decimal
    breakdown: dict[str, Decimal] = field(default_factory=dict)

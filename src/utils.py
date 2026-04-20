from __future__ import annotations

from decimal import Decimal
from typing import Iterable, TypeVar


MONEY_ZERO = Decimal("0.00")
T = TypeVar("T")


def normalize_space(value: str) -> str:
    """Схлопывает повторяющиеся пробелы и обрезает строку по краям."""
    return " ".join(value.split())


def parse_money(value: str) -> Decimal:
    """Преобразует строку с ценой из интерфейса магазина в Decimal."""
    normalized = (
        value.replace("$", "")
        .replace(",", "")
        .replace("\xa0", "")
        .strip()
    )
    return Decimal(normalized or "0").quantize(Decimal("0.01"))


def sum_money(values: Iterable[Decimal]) -> Decimal:
    """Суммирует денежные значения Decimal с точностью до двух знаков."""
    return sum(values, start=MONEY_ZERO).quantize(Decimal("0.01"))


def unique_by_url(items: Iterable[T], get_url) -> list[T]:
    """Оставляет только первый объект для каждого уникального непустого url."""
    seen: set[str] = set()
    result: list[T] = []
    for item in items:
        url = get_url(item)
        if url and url not in seen:
            seen.add(url)
            result.append(item)
    return result

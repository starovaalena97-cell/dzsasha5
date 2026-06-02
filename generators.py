"""
Модуль generators содержит функции-генераторы для обработки транзакций.
"""

from typing import Any, Dict, Generator, Iterator, List


def filter_by_currency(
    transactions: List[Dict[str, Any]], currency: str
) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по валюте.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты (например, "USD", "RUB")

    Returns:
        Итератор, выдающий транзакции с указанной валютой

    Пример:
        >>> usd_trans = filter_by_currency(transactions, "USD")
        >>> first_usd = next(usd_trans)
    """
    for transaction in transactions:
        if (
            transaction.get("operationAmount", {})
            .get("currency", {})
            .get("code") == currency
        ):
            yield transaction


def transaction_descriptions(
    transactions: List[Dict[str, Any]]
) -> Generator[str, None, None]:
    """
    Возвращает описание каждой транзакции по очереди.

    Args:
        transactions: Список словарей с транзакциями

    Returns:
        Генератор строк с описаниями транзакций

    Пример:
        >>> descriptions = transaction_descriptions(transactions)
        >>> print(next(descriptions))
        "Перевод организации"
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Генерирует номера карт в диапазоне от start до stop.

    Args:
        start: Начальное значение (включительно)
        stop: Конечное значение (включительно)

    Returns:
        Генератор отформатированных номеров карт

    Пример:
        >>> for card in card_number_generator(1, 3):
        ...     print(card)
        0000 0000 0000 0001
        0000 0000 0000 0002
        0000 0000 0000 0003
    """
    for number in range(start, stop + 1):
        card_str = str(number).zfill(16)
        formatted = " ".join(
            card_str[i:i+4] for i in range(0, 16, 4)
        )
        yield formatted
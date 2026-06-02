"""
Тесты для модуля generators.
"""

import pytest

from generators import (card_number_generator, filter_by_currency,
                        transaction_descriptions)


@pytest.fixture
def sample_transactions():
    """Фикстура: возвращает список тестовых транзакций."""
    return [
        {
            "id": 1,
            "description": "Перевод другу",
            "operationAmount": {
                "amount": "100.50",
                "currency": {"code": "USD", "name": "USD"}
            },
        },
        {
            "id": 2,
            "description": "Покупка продуктов",
            "operationAmount": {
                "amount": "2500.00",
                "currency": {"code": "RUB", "name": "Рубль"}
            },
        },
        {
            "id": 3,
            "description": "Оплата подписки",
            "operationAmount": {
                "amount": "15.99",
                "currency": {"code": "USD", "name": "USD"}
            },
        },
        {
            "id": 4,
            "description": "Кофе с собой",
            "operationAmount": {
                "amount": "350.50",
                "currency": {"code": "RUB", "name": "Рубль"}
            },
        },
    ]


# ========== ТЕСТЫ ДЛЯ filter_by_currency ==========

def test_filter_by_currency_returns_iterator(sample_transactions):
    """Проверяет, что функция возвращает итератор."""
    result = filter_by_currency(sample_transactions, "USD")
    assert hasattr(result, "__iter__")
    assert hasattr(result, "__next__")


def test_filter_by_currency_filters_correctly(sample_transactions):
    """Проверяет корректность фильтрации по валюте."""
    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
    assert len(usd_transactions) == 2
    for trans in usd_transactions:
        assert trans["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_no_matches(sample_transactions):
    """Проверяет случай, когда нет транзакций в нужной валюте."""
    eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
    assert eur_transactions == []


def test_filter_by_currency_empty_list():
    """Проверяет обработку пустого списка."""
    result = list(filter_by_currency([], "USD"))
    assert result == []


@pytest.mark.parametrize("currency, expected_count", [
    ("USD", 2),
    ("RUB", 2),
    ("EUR", 0),
    ("GBP", 0),
])
def test_filter_by_currency_parametrized(sample_transactions, currency, expected_count):
    """Параметризованный тест фильтрации по валюте."""
    result = list(filter_by_currency(sample_transactions, currency))
    assert len(result) == expected_count


# ========== ТЕСТЫ ДЛЯ transaction_descriptions ==========

def test_transaction_descriptions_returns_generator(sample_transactions):
    """Проверяет, что функция возвращает генератор."""
    result = transaction_descriptions(sample_transactions)
    assert hasattr(result, "__iter__")
    assert hasattr(result, "__next__")


def test_transaction_descriptions_yields_correct_values(sample_transactions):
    """Проверяет, что генератор возвращает правильные описания."""
    gen = transaction_descriptions(sample_transactions)
    assert next(gen) == "Перевод другу"
    assert next(gen) == "Покупка продуктов"
    assert next(gen) == "Оплата подписки"
    assert next(gen) == "Кофе с собой"


def test_transaction_descriptions_empty_list():
    """Проверяет обработку пустого списка."""
    gen = transaction_descriptions([])
    with pytest.raises(StopIteration):
        next(gen)


def test_transaction_descriptions_missing_description():
    """Проверяет случай, когда у транзакции нет поля description."""
    transactions = [
        {"id": 1},
        {"id": 2, "description": "Есть описание"}
    ]
    gen = transaction_descriptions(transactions)
    assert next(gen) == ""
    assert next(gen) == "Есть описание"


# ========== ТЕСТЫ ДЛЯ card_number_generator ==========

def test_card_number_generator_returns_generator():
    """Проверяет, что функция возвращает генератор."""
    result = card_number_generator(1, 5)
    assert hasattr(result, "__iter__")
    assert hasattr(result, "__next__")


def test_card_number_generator_single_number():
    """Проверяет генерацию одного номера карты."""
    gen = card_number_generator(1, 1)
    assert next(gen) == "0000 0000 0000 0001"


def test_card_number_generator_range():
    """Проверяет генерацию диапазона номеров."""
    result = list(card_number_generator(10, 12))
    expected = [
        "0000 0000 0000 0010",
        "0000 0000 0000 0011",
        "0000 0000 0000 0012",
    ]
    assert result == expected


def test_card_number_generator_formatting():
    """Проверяет правильность форматирования."""
    test_cases = [
        (1, "0000 0000 0000 0001"),
        (123, "0000 0000 0000 0123"),
        (12345, "0000 0000 0001 2345"),
        (123456789, "0000 0001 2345 6789"),
    ]
    for number, expected in test_cases:
        gen = card_number_generator(number, number)
        assert next(gen) == expected


@pytest.mark.parametrize("start, stop, expected_first, expected_last", [
    (1, 3, "0000 0000 0000 0001", "0000 0000 0000 0003"),
    (100, 101, "0000 0000 0000 0100", "0000 0000 0000 0101"),
    (9999, 10000, "0000 0000 0000 9999", "0000 0000 0001 0000"),
    (9999999999999999, 9999999999999999, "9999 9999 9999 9999", "9999 9999 9999 9999"),
])
def test_card_number_generator_parametrized(start, stop, expected_first, expected_last):
    """Параметризованный тест генератора номеров карт."""
    result = list(card_number_generator(start, stop))
    assert result[0] == expected_first
    assert result[-1] == expected_last
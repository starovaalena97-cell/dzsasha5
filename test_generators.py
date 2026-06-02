"""
Модуль с тестами для функций-генераторов.
"""

import pytest
from generators import filter_by_currency, transaction_descriptions, card_number_generator


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    def test_filter_usd_currency(self, sample_transactions):
        """Тест фильтрации транзакций по валюте USD."""
        usd_transactions = filter_by_currency(sample_transactions, "USD")
        result = list(usd_transactions)

        assert len(result) == 3
        for transaction in result:
            assert transaction["operationAmount"]["currency"]["code"] == "USD"

    def test_filter_rub_currency(self, sample_transactions):
        """Тест фильтрации транзакций по валюте RUB."""
        rub_transactions = filter_by_currency(sample_transactions, "RUB")
        result = list(rub_transactions)

        assert len(result) == 2
        for transaction in result:
            assert transaction["operationAmount"]["currency"]["code"] == "RUB"

    @pytest.mark.parametrize(
        "currency_code,expected_count",
        [
            ("USD", 3),
            ("RUB", 2),
            ("EUR", 0),
            ("GBP", 0),
            ("JPY", 0),
        ],
    )
    def test_filter_different_currencies(
            self, sample_transactions, currency_code, expected_count
    ):
        """Параметризованный тест фильтрации различных валют."""
        filtered = filter_by_currency(sample_transactions, currency_code)
        result = list(filtered)
        assert len(result) == expected_count

    def test_filter_empty_list(self, empty_transactions):
        """Тест фильтрации пустого списка."""
        filtered = filter_by_currency(empty_transactions, "USD")
        assert list(filtered) == []

    def test_filter_no_matching_currency(self, sample_transactions):
        """Тест фильтрации, когда нет транзакций с нужной валютой."""
        filtered = filter_by_currency(sample_transactions, "EUR")
        assert list(filtered) == []

    def test_filter_missing_currency_fields(self, transactions_without_currency):
        """Тест фильтрации транзакций с отсутствующими полями валюты."""
        filtered = filter_by_currency(transactions_without_currency, "USD")
        result = list(filtered)
        assert len(result) == 0  # Нет корректных транзакций с USD

    def test_filter_generator_lazy_property(self, sample_transactions):
        """Тест ленивости генератора."""
        generator = filter_by_currency(sample_transactions, "USD")

        # Проверяем, что это генератор
        assert hasattr(generator, "__iter__")
        assert hasattr(generator, "__next__")

        # Получаем первый элемент
        first = next(generator)
        assert first["id"] == 939719570

        # Получаем второй элемент
        second = next(generator)
        assert second["id"] == 142264268

    def test_filter_generator_stop_iteration(self, sample_transactions):
        """Тест обработки StopIteration."""
        generator = filter_by_currency(sample_transactions, "USD")

        # Получаем все 3 элемента
        next(generator)
        next(generator)
        next(generator)

        # При попытке получить четвертый элемент должно быть StopIteration
        with pytest.raises(StopIteration):
            next(generator)


class TestTransactionDescriptions:
    """Тесты для функции transaction_descriptions."""

    def test_descriptions_generation(self, sample_transactions):
        """Тест генерации описаний транзакций."""
        descriptions = transaction_descriptions(sample_transactions)
        result = list(descriptions)

        expected_descriptions = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ]
        assert result == expected_descriptions

    def test_descriptions_empty_list(self, empty_transactions):
        """Тест генерации описаний для пустого списка."""
        descriptions = transaction_descriptions(empty_transactions)
        assert list(descriptions) == []

    @pytest.mark.parametrize(
        "transactions,expected",
        [
            ([{"description": "Тест"}], ["Тест"]),
            ([{"description": "Перевод"}], ["Перевод"]),
            ([{"description": "Оплата"}, {"description": "Вывод"}], ["Оплата", "Вывод"]),
        ],
    )
    def test_descriptions_parameterized(self, transactions, expected):
        """Параметризованный тест генерации описаний."""
        descriptions = transaction_descriptions(transactions)
        assert list(descriptions) == expected

    def test_descriptions_single_transaction(self):
        """Тест генерации описаний для одной транзакции."""
        transactions = [{"description": "Тестовый перевод"}]
        descriptions = transaction_descriptions(transactions)
        assert list(descriptions) == ["Тестовый перевод"]

    def test_descriptions_with_missing_field(self, transactions_without_descriptions):
        """Тест генерации описаний при отсутствии поля description."""
        descriptions = transaction_descriptions(transactions_without_descriptions)
        result = list(descriptions)
        assert result == ["Описание 1", "Описание 3"]

    def test_descriptions_generator_lazy_property(self, sample_transactions):
        """Тест ленивости генератора описаний."""
        generator = transaction_descriptions(sample_transactions)

        # Получаем первое описание
        first = next(generator)
        assert first == "Перевод организации"

        # Получаем второе описание
        second = next(generator)
        assert second == "Перевод со счета на счет"

    def test_descriptions_generator_stop_iteration(self, sample_transactions):
        """Тест StopIteration для генератора описаний."""
        generator = transaction_descriptions(sample_transactions)

        # Получаем все 5 описаний
        for _ in range(5):
            next(generator)

        # При попытке получить шестое описание должно быть StopIteration
        with pytest.raises(StopIteration):
            next(generator)


class TestCardNumberGenerator:
    """Тесты для генератора card_number_generator."""

    @pytest.mark.parametrize(
        "start,stop,expected",
        [
            (1, 1, ["0000 0000 0000 0001"]),
            (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
            (9999, 10001, ["0000 0000 0000 9999", "0000 0000 0001 0000", "0000 0000 0001 0001"]),
            (1, 5, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003", "0000 0000 0000 0004",
                    "0000 0000 0000 0005"]),
            (100, 102, ["0000 0000 0000 0100", "0000 0000 0000 0101", "0000 0000 0000 0102"]),
            (999999, 1000001, ["0000 0000 0099 9999", "0000 0000 0100 0000", "0000 0000 0100 0001"]),
        ],
    )
    def test_card_number_range(self, start, stop, expected):
        """Параметризованный тест генерации номеров карт в диапазоне."""
        result = list(card_number_generator(start, stop))
        assert result == expected

    def test_card_number_format(self):
        """Тест правильности форматирования номера карты."""
        generator = card_number_generator(1, 5)
        cards = list(generator)

        for card in cards:
            # Проверяем формат: 4 группы цифр по 4 символа
            parts = card.split()
            assert len(parts) == 4
            for part in parts:
                assert len(part) == 4
                assert part.isdigit()

    def test_card_number_single_value(self):
        """Тест генерации одного номера карты."""
        generator = card_number_generator(42, 42)
        result = list(generator)
        assert result == ["0000 0000 0000 0042"]

    @pytest.mark.parametrize(
        "number,expected",
        [
            (1, "0000 0000 0000 0001"),
            (9999, "0000 0000 0000 9999"),
            (10000, "0000 0000 0001 0000"),
            (12345678, "0000 0000 1234 5678"),
            (9999999999999999, "9999 9999 9999 9999"),
        ],
    )
    def test_card_number_specific_values(self, number, expected):
        """Параметризованный тест конкретных номеров карт."""
        generator = card_number_generator(number, number)
        assert list(generator) == [expected]

    def test_card_number_large_numbers(self):
        """Тест генерации больших номеров карт."""
        generator = card_number_generator(9999999999999999, 9999999999999999)
        result = list(generator)
        assert result == ["9999 9999 9999 9999"]

    def test_card_number_generator_lazy_property(self):
        """Тест ленивости генератора номеров карт."""
        generator = card_number_generator(1, 1000000)

        # Генератор не создает все числа в памяти
        first = next(generator)
        assert first == "0000 0000 0000 0001"

        second = next(generator)
        assert second == "0000 0000 0000 0002"

    def test_card_number_edge_values(self):
        """Тест граничных значений."""
        # Минимальное значение
        generator_min = card_number_generator(1, 1)
        assert next(generator_min) == "0000 0000 0000 0001"

        # Максимальное значение
        generator_max = card_number_generator(9999999999999999, 9999999999999999)
        assert next(generator_max) == "9999 9999 9999 9999"

    def test_card_number_range_large_gap(self):
        """Тест генерации большого диапазона."""
        generator = card_number_generator(1, 10)
        result = list(generator)
        assert len(result) == 10
        assert result[0] == "0000 0000 0000 0001"
        assert result[9] == "0000 0000 0000 0010"
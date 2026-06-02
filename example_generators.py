"""
Пример использования генераторов для обработки транзакций.
"""

from generators import filter_by_currency, transaction_descriptions, card_number_generator


def main():
    """Демонстрация работы всех генераторов."""

    # Транзакции из задания
    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]

    print("=" * 60)
    print("1. Демонстрация filter_by_currency (USD транзакции)")
    print("=" * 60)
    usd_transactions = filter_by_currency(transactions, "USD")
    for i in range(2):
        transaction = next(usd_transactions)
        print(f"\nТранзакция {i + 1}:")
        print(f"  ID: {transaction['id']}")
        print(f"  Сумма: {transaction['operationAmount']['amount']} "
              f"{transaction['operationAmount']['currency']['code']}")
        print(f"  Описание: {transaction['description']}")

    print("\n" + "=" * 60)
    print("2. Демонстрация transaction_descriptions")
    print("=" * 60)
    descriptions = transaction_descriptions(transactions)
    for i in range(5):
        print(f"  {i + 1}. {next(descriptions)}")

    print("\n" + "=" * 60)
    print("3. Демонстрация card_number_generator")
    print("=" * 60)
    for card_number in card_number_generator(1, 5):
        print(f"  {card_number}")

    print("\n" + "=" * 60)
    print("4. Демонстрация обработки больших данных (ленивость)")
    print("=" * 60)
    print("Генерация 1 миллиона номеров карт без создания списка в памяти...")
    large_generator = card_number_generator(1, 1000000)
    print(f"Первый номер: {next(large_generator)}")
    print(f"Второй номер: {next(large_generator)}")
    print("Генератор продолжает работу без загрузки всех номеров в память!")


if __name__ == "__main__":
    main()
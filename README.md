# Проект по обработке транзакций

## Модуль generators

Модуль с генераторами для обработки транзакций.

### Функции

#### 1. filter_by_currency(transactions, currency)

Фильтрует транзакции по валюте. Возвращает итератор.

**Пример использования:**

```python
from generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
first_usd = next(usd_transactions)
print(first_usd)
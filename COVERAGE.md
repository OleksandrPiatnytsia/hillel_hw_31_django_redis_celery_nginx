# Покриття тестами

Звіт згенеровано командою:

```bash
pytest                                                  # тести + дані покриття у файлі .coverage
coverage report --format=markdown --precision=2         # таблиця нижче, у форматі Markdown
```

Налаштування в `.coveragerc`: рахується лише власний код (без `.venv`,
тестів, міграцій і файлів налаштувань). `pytest.ini` вимагає щонайменше 70%.

Загалом **98.36%**, 362 тести. Код цього ДЗ — **100%** кожен файл:
`inventory/` (склад), `books/cache.py`, `api/cache.py` (кеш), `config/celery.py`,
`orders/tasks.py`, `orders/reports.py`, `payments/tasks.py`, `users/tasks.py`
(Celery), `config/sentry.py`, `users/tools.py`.

Детальний звіт з підсвіченими непокритими рядками: `htmlcov/index.html`
(створюється при кожному `pytest`, у git не потрапляє).

| Name                                                 |    Stmts |     Miss |      Cover |
|----------------------------------------------------- | -------: | -------: | ---------: |
| api/\_\_init\_\_.py                                  |        0 |        0 |    100.00% |
| api/apps.py                                          |        6 |        0 |    100.00% |
| api/cache.py                                         |       35 |        0 |    100.00% |
| api/docs.py                                          |       25 |        0 |    100.00% |
| api/exceptions.py                                    |       11 |        0 |    100.00% |
| api/filters.py                                       |       31 |        0 |    100.00% |
| api/permissions.py                                   |        6 |        0 |    100.00% |
| api/serializers/\_\_init\_\_.py                      |        0 |        0 |    100.00% |
| api/serializers/catalog.py                           |       67 |        0 |    100.00% |
| api/serializers/orders.py                            |       67 |        0 |    100.00% |
| api/signals.py                                       |       17 |        0 |    100.00% |
| api/urls.py                                          |       15 |        0 |    100.00% |
| api/views/\_\_init\_\_.py                            |        0 |        0 |    100.00% |
| api/views/auth.py                                    |       26 |        0 |    100.00% |
| api/views/catalog.py                                 |       65 |        0 |    100.00% |
| api/views/orders.py                                  |       81 |        0 |    100.00% |
| books/\_\_init\_\_.py                                |        0 |        0 |    100.00% |
| books/admin.py                                       |       90 |        5 |     94.44% |
| books/apps.py                                        |        7 |        0 |    100.00% |
| books/cache.py                                       |       35 |        0 |    100.00% |
| books/forms.py                                       |       61 |        0 |    100.00% |
| books/management/\_\_init\_\_.py                     |        0 |        0 |    100.00% |
| books/management/commands/\_\_init\_\_.py            |        0 |        0 |    100.00% |
| books/management/commands/book\_stats.py             |       72 |        0 |    100.00% |
| books/management/commands/seed\_books.py             |       26 |        0 |    100.00% |
| books/models.py                                      |       99 |        0 |    100.00% |
| books/signals.py                                     |       29 |        0 |    100.00% |
| books/urls.py                                        |        4 |        0 |    100.00% |
| books/views.py                                       |      132 |        3 |     97.73% |
| cart/\_\_init\_\_.py                                 |        0 |        0 |    100.00% |
| cart/apps.py                                         |        5 |        0 |    100.00% |
| cart/cart.py                                         |       63 |        0 |    100.00% |
| cart/context\_processors.py                          |        3 |        0 |    100.00% |
| cart/forms.py                                        |        4 |        0 |    100.00% |
| cart/urls.py                                         |        4 |        0 |    100.00% |
| cart/views.py                                        |       40 |        0 |    100.00% |
| config/\_\_init\_\_.py                               |        2 |        0 |    100.00% |
| config/celery.py                                     |       17 |        0 |    100.00% |
| config/i18n.py                                       |        6 |        0 |    100.00% |
| config/logging\_filters.py                           |        8 |        0 |    100.00% |
| config/middleware.py                                 |       47 |        1 |     97.87% |
| config/sentry.py                                     |       30 |        0 |    100.00% |
| config/urls.py                                       |       11 |        3 |     72.73% |
| config/views.py                                      |       52 |        1 |     98.08% |
| inventory/\_\_init\_\_.py                            |        0 |        0 |    100.00% |
| inventory/admin.py                                   |       15 |        0 |    100.00% |
| inventory/apps.py                                    |        7 |        0 |    100.00% |
| inventory/models.py                                  |       32 |        0 |    100.00% |
| inventory/services.py                                |       12 |        0 |    100.00% |
| inventory/signals.py                                 |        9 |        0 |    100.00% |
| orders/\_\_init\_\_.py                               |        0 |        0 |    100.00% |
| orders/admin.py                                      |      104 |       10 |     90.38% |
| orders/apps.py                                       |        5 |        0 |    100.00% |
| orders/emails.py                                     |       30 |        0 |    100.00% |
| orders/forms.py                                      |       14 |        0 |    100.00% |
| orders/management/\_\_init\_\_.py                    |        0 |        0 |    100.00% |
| orders/management/commands/\_\_init\_\_.py           |        0 |        0 |    100.00% |
| orders/management/commands/cancel\_unpaid\_orders.py |       47 |        0 |    100.00% |
| orders/models.py                                     |       80 |        0 |    100.00% |
| orders/reports.py                                    |       65 |        0 |    100.00% |
| orders/services.py                                   |       69 |        4 |     94.20% |
| orders/tasks.py                                      |       23 |        0 |    100.00% |
| orders/urls.py                                       |        4 |        0 |    100.00% |
| orders/views.py                                      |       76 |        0 |    100.00% |
| payments/\_\_init\_\_.py                             |        0 |        0 |    100.00% |
| payments/admin.py                                    |       65 |        1 |     98.46% |
| payments/apps.py                                     |        5 |        0 |    100.00% |
| payments/emails.py                                   |        5 |        0 |    100.00% |
| payments/models.py                                   |       30 |        0 |    100.00% |
| payments/providers/\_\_init\_\_.py                   |        0 |        0 |    100.00% |
| payments/providers/base.py                           |       19 |        3 |     84.21% |
| payments/providers/manual.py                         |        4 |        0 |    100.00% |
| payments/providers/registry.py                       |       10 |        0 |    100.00% |
| payments/providers/stripe\_checkout.py               |       83 |        1 |     98.80% |
| payments/services.py                                 |      133 |        3 |     97.74% |
| payments/tasks.py                                    |        6 |        0 |    100.00% |
| payments/urls.py                                     |        4 |        0 |    100.00% |
| payments/views.py                                    |       40 |        0 |    100.00% |
| users/\_\_init\_\_.py                                |        0 |        0 |    100.00% |
| users/admin.py                                       |        8 |        0 |    100.00% |
| users/apps.py                                        |        7 |        0 |    100.00% |
| users/forms.py                                       |       22 |        0 |    100.00% |
| users/models.py                                      |       20 |        0 |    100.00% |
| users/phone.py                                       |       11 |        0 |    100.00% |
| users/signals.py                                     |       18 |        1 |     94.44% |
| users/tasks.py                                       |        8 |        0 |    100.00% |
| users/tools.py                                       |       27 |        0 |    100.00% |
| users/urls.py                                        |        4 |        0 |    100.00% |
| users/views.py                                       |       81 |        5 |     93.83% |
| **TOTAL**                                            | **2501** |   **41** | **98.36%** |

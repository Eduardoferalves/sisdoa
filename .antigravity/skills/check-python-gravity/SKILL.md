---
name: check-python-gravity
description: Impede a contaminação cruzada de configurações de Node.js/Prisma em ambiente Python.
---
Garanta que parâmetros como 'prepared_statements' nunca sejam injetados em strings de conexão do psycopg2.

---
name: infraestrutura-supabase-serverless
description: Restrições mandatórias para prevenção de connection exhaustion e crashes de dialeto.
---
1. Pooling Serverless: É PROIBIDO manter o pool padrão do SQLAlchemy em instâncias efêmeras da Vercel. Use obrigatoriamente `poolclass=NullPool` da biblioteca `sqlalchemy.pool` para conexões PostgreSQL.
2. Transaction Pooler (Porta 6543): O modo transacional do Supavisor não suporta prepared statements persistentes. Garanta que strings Postgres desativem statements preparados.
3. Dialeto Estrito: Intercepte e trate dinamicamente na inicialização as URLs que comecem com `postgres://` ou `postgresql://`, convertendo-as para `postgresql+psycopg2://`.
4. Isolamento de Argumentos: O parâmetro `connect_args={"check_same_thread": False}` causa crash no Postgres. Ele só pode ser injetado condicionalmente se o banco for SQLite.
5. Fuso Horário: O PostgreSQL exige tipagem explícita de timezone. Altere campos DateTime para `DateTime(timezone=True)`.

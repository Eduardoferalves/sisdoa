---
name: infraestrutura-supabase-serverless
description: Restrições mandatórias para prevenção de connection exhaustion e crashes de dialeto.
---
Use poolclass=NullPool e pool_pre_ping=True no create_engine se a URL iniciar com postgresql.
Substitua dinamicamente postgres:// ou postgresql:// por postgresql+psycopg2:// no arquivo config.py.
O argumento connect_args={"check_same_thread": False} é PROIBIDO no Postgres; use apenas em SQLite.
Desative o DDL automático (Base.metadata.create_all) em tempo de execução normal se engine.dialect.name != "sqlite".

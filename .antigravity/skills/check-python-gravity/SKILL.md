# Skill: Validação de Ecossistema Python / SQLAlchemy

**Propósito:**
Prevenir a injeção de parâmetros e configurações alucinadas oriundas de outros ecossistemas (ex: Node.js, Prisma, TypeORM) em nossa base Python.

**Regras de Auditoria:**
1. **Dialeto Postgres e Bindings:** O Python (via `psycopg2`) gerencia os prepared statements no *client-side* por padrão.
2. **Proibição de Argumentos DSN Inválidos:** É terminantemente PROIBIDO adicionar strings como `?prepared_statements=false` ou `?pgbouncer=true` na connection string (`DATABASE_URL`) quando utilizada com `psycopg2`. Tais flags são nativas do ecossistema Node.js/Prisma e causarão o erro fatal `invalid connection option` na library *libpq* via `psycopg2.ProgrammingError`.
3. **Desativação de DDL Serverless:** O SQLAlchemy NÃO DEVE executar `Base.metadata.create_all()` em tempo de inicialização (*startup*) se a URL apontar para o Postgres. Checar metadados de tabelas em runtime (via poolers transacionais) mata a performance em ambientes Serverless como a Vercel. Garanta que o método de criação execute de modo in-memory/restrito verificando se `self.engine.url.drivername.startswith("sqlite")`. Em produção/banco real, a gestão de schema deverá ser guiada estritamente via `alembic`.

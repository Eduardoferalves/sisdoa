# Audit Infraestrutura Serverless

Esta skill verifica se as modificações do projeto estão compatíveis com a arquitetura Vercel + Supabase Transaction Pooler (Porta 6543).

## Instruções de Auditoria
1. Verificar `pyproject.toml`:
   - [ ] Confirmar a presença de `psycopg2-binary`.
   - [ ] Confirmar a presença de `python-dotenv`.
2. Verificar `src/sisdoa/config.py`:
   - [ ] Confirmar se há interceptação dinâmica convertendo URLs `postgres://` ou `postgresql://` para `postgresql+psycopg2://`.
3. Verificar `src/sisdoa/repository/database.py`:
   - [ ] Confirmar o uso explícito de `poolclass=NullPool` quando a URL do banco inicia com `postgresql`.
   - [ ] Confirmar o isolamento do parâmetro `connect_args={"check_same_thread": False}` apenas para instâncias SQLite.

## Resultados Esperados
- Uma tabela comparativa com o Critério, Arquivo, e o Status (Pass / Fail) evidenciando que as regras foram seguidas corretamente com base nas mudanças expostas pelo `git diff`.

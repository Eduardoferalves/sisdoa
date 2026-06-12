---
name: web-api-fastapi-serverless
description: Padrões de inversão de controle, gerenciamento de sessões e concorrência HTTP.
---
1. Inversão de Controle: É PROIBIDO que os métodos do repositório instanciem ou fechem sessões do SQLAlchemy internamente. Eles devem receber e usar uma sessão ativa injetada.
2. Ciclo de Vida do Banco: Use a dependência `get_db` do FastAPI com padrão gerador (`yield`) para abrir e fechar sessões por requisição HTTP.
3. Rotas Síncronas: Como o gateway OpenFoodFacts é síncrono, as rotas que o chamam devem ser declaradas com `def`, nunca com `async def`.
4. Serialização: Todos os endpoints devem utilizar esquemas do Pydantic v2 configurados com `from_attributes=True` para respostas JSON.

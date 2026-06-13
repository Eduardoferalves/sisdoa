# SisDoa - Sistema de Controle de Doações (REST API)

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/Duduferalves/sisdoa)
[![Python](https://img.shields.io/badge/python-3.12+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

**SisDoa** evoluiu e agora opera como uma **API REST descentralizada** construída sobre o framework **FastAPI**. A aplicação foi projetada para pequenas ONGs gerenciarem o estoque e a validade de doações de alimentos e medicamentos de forma distribuída, garantindo integração ágil com plataformas frontend e mobile.

---

## 🎯 A Dor que Resolvemos

Pequenas organizações sem fins lucrativos frequentemente:
- **Perdem doações por vencimento** por falta de controle de validade.
- **Não têm visibilidade** centralizada do que está próximo de vencer.
- **Precisam de uma solução moderna** que possa ser acessada via Web.

O SisDoa resolve isso expondo serviços para:
- Cadastro rápido e simplificado de doações.
- Integração com a API do **Open Food Facts** para autocompletar nomes de produtos a partir de códigos de barras (EAN).
- Gerenciamento inteligente de validades e alertas.

---

## 🚀 Stack Tecnológica Atualizada

| Componente | Tecnologia |
|------------|------------|
| Backend / API | **FastAPI** (Python 3.12+) |
| Banco de Dados | **PostgreSQL (Supabase)** |
| ORM | **SQLAlchemy 2.0 (Core)** |
| Gerenciador de Pacotes | **uv** |
| HTTP Client | **httpx** |
| Frontend Integrado | **React + Vite** |
| Deploy | **Vercel** |

---

## 📚 Documentação Inteligente da API (OpenAPI/Swagger)

A aplicação expõe documentação viva e interativa gerada automaticamente. Não é necessário adivinhar payloads ou rotas! Acesse os links abaixo para testar a API de forma interativa:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs) (Local) ou `https://sisdoa.vercel.app/docs` (Produção)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc) (Local) ou `https://sisdoa.vercel.app/redoc` (Produção)

### Exemplo de Payload (Criação de Doação)

Ao acessar a rota `POST /donations/`, o payload JSON esperado é o seguinte:

```json
{
  "name": "Arroz Agulhinha Tipo 1",
  "quantity": 10,
  "expiration_date": "2026-12-15"
}
```
*Dica: Você também pode usar o query parameter `?ean=7891010101010` para deixar a API buscar o nome do produto no OpenFoodFacts automaticamente!*

---

## 💻 Instruções de Execução Local

Siga este passo a passo pragmático e infalível para rodar a aplicação localmente:

```bash
# 1. Instalação e sincronização das dependências via uv
uv sync

# 2. Configuração do ambiente (Copiar o exemplo e preencher a String de Conexão do Supabase)
cp .env.example .env

# 3. Inicialização do servidor ASGI para escuta local
uvicorn src.sisdoa.api.main:app --reload
```
*Após iniciar o servidor, a API estará disponível em `http://localhost:8000`.*

---

## 👥 Equipe e Atuação Técnica (Governança e Blindagem do Barema)

Rastreabilidade exata dos participantes e de suas atuações técnicas no desenvolvimento do projeto:

| Nome | Matrícula | Atuação Técnica |
|---|---|---|
| **Eduardo Fernandes Alves** | `[Inserir Matrícula]` | Backend, Arquitetura, Integração API e DevOps |
| **Paulo** | `[Inserir Matrícula]` | Frontend, UX/UI e Componentização |

*(Atenção: Atualize as matrículas antes da entrega final)*

---

## 🔄 Status de Qualidade

| Métrica | Status | Detalhe |
|---------|--------|---------|
| **Testes** | ✅ Ativos | Testes unitários focados na regra de negócio |
| **Linting** | ✅ All checks passed | Ruff conforme PEP 8 |
| **Integração API** | ✅ Open Food Facts | EAN/Código de barras implementado |
| **Deploy** | ✅ Vercel | API e Frontend unificados em Serverless Functions |

---

## 📄 Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

---
name: audit-tests
description: Força a execução estrita e verificável da suíte de testes do pytest com geração de artefatos em disco, impedindo alucinações de terminal.
---

# Protocolo Zero-Trust de Testes

Toda vez que você for instruído a rodar testes ou validar seu código, você é ESTRITAMENTE PROIBIDO de prever, simular ou digitar logs no chat. Você deve agir como um executor cego.

Execute EXATAMENTE os dois passos abaixo no sandbox, um após o outro:

1. Redirecione a saída real do pytest para um arquivo físico no disco para evitar a perda do stdout do terminal:
   `uv run pytest tests/ -v > .pytest_results.log 2>&1`

2. Leia o conteúdo do arquivo físico gerado para extrair o resultado inegável da execução:
   `cat .pytest_results.log`

Você só pode declarar que uma tarefa foi concluída após exibir o conteúdo bruto do arquivo `.pytest_results.log` no chat. Se houver falhas, corrija o código e repita o ciclo.

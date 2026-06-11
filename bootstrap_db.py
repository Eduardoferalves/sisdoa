from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

load_dotenv()

from rich.console import Console  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402

from sisdoa.config import DATABASE_URL  # noqa: E402
from sisdoa.domain.models import Base  # noqa: E402

console = Console()

def main():
    console.print("[bold blue]Iniciando o Bootstrap do banco de dados remoto...[/bold blue]")

    if not DATABASE_URL:
        console.print("[bold red]ERRO: DATABASE_URL não está definida![/bold red]")
        return

    engine = create_engine(DATABASE_URL)

    if engine.dialect.name != "postgresql":
        console.print(f"[bold red]ERRO CRÍTICO: Execução abortada. O script foi desviado para o fallback local ({engine.url}). Certifique-se de que o arquivo .env real está configurado.[/bold red]")
        sys.exit(1)

    try:
        console.print("[yellow]Injetando Schema DDL...[/yellow]")
        console.print(f"[cyan]Rastreamento de Alvo: host={engine.url.host}, database={engine.url.database}[/cyan]")
        Base.metadata.create_all(bind=engine)
        console.print("[bold green]✅ Sucesso! Tabelas injetadas no cluster remoto com perfeição.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Erro ao criar o schema DDL: {e}[/bold red]")

if __name__ == "__main__":
    main()

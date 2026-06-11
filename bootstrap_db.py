import os
from dotenv import load_dotenv

load_dotenv()

from rich.console import Console
from sqlalchemy import create_engine

from sisdoa.config import DATABASE_URL
from sisdoa.domain.models import Base

console = Console()

def main():
    console.print("[bold blue]Iniciando o Bootstrap do banco de dados remoto...[/bold blue]")
    
    if not DATABASE_URL:
        console.print("[bold red]ERRO: DATABASE_URL nÃ£o estÃ¡ definida![/bold red]")
        return
        
    engine = create_engine(DATABASE_URL)
    
    try:
        console.print("[yellow]Injetando Schema DDL...[/yellow]")
        Base.metadata.create_all(bind=engine)
        console.print("[bold green]âœ… Sucesso! Tabelas injetadas no cluster remoto com perfeiÃ§Ã£o.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Erro ao criar o schema DDL: {e}[/bold red]")

if __name__ == "__main__":
    main()

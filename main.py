import logging

logging.basicConfig(level=logging.WARNING)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

import typer
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt, IntPrompt
from rich.table import Table
from rich.panel import Panel
from tracker import (
    add_transaction,
    show_transactions as _show_transactions,
    delete_transaction,
    edit_transaction
)
import time

app = typer.Typer()
console = Console()

def typewriter(text: str, delay=0.01):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

@app.command()
def banner():
    typewriter("[bold cyan]>>> SYSTEM ONLINE. READY FOR INPUT...[/bold cyan]", delay=0.02)


@app.command()
def add():
    console.rule("[bold green]# [ ADD TRANSACTION ] #", style="bold magenta")
    tipe = Prompt.ask("[bright_magenta]» TYPE", choices=["income", "expense"], default="expense")
    description = Prompt.ask("[green]» DESCRIPTION")
    amount = FloatPrompt.ask("[cyan]» AMOUNT")

    add_transaction(tipe, description, amount)

    console.print(Panel.fit(
        f"[bold green]✔ TRANSACTION ADDED[/bold green]\n[cyan]{description}[/cyan] - [magenta]{amount:.2f}[/magenta] as [bold]{tipe.upper()}[/bold]",
        border_style="bright_green", title="[ SYSTEM LOG ]"
    ))


@app.command()
def show():
    console.rule("[bold bright_cyan]# [ TRANSACTION LOGS ] #", style="bright_green")
    transactions = _show_transactions()
    
    if not transactions:
        console.print("[bold red]⚠ NO TRANSACTIONS FOUND[/bold red]")
        return

    table = Table(title="💸 SYSTEM LEDGER", show_lines=True, border_style="green")
    table.add_column("ID", justify="right", style="dim")
    table.add_column("TYPE", style="bright_cyan", no_wrap=True)
    table.add_column("DESCRIPTION", style="bright_green")
    table.add_column("AMOUNT", justify="right", style="bright_magenta")

    for idx, txn in enumerate(transactions, 1):
        tipe, description, amount = txn
        table.add_row(str(idx), tipe.upper(), description, f"{amount:.2f}")

    console.print(table)
    console.print("[bold bright_green]>>> END OF LOG <<<[/bold bright_green]")


@app.command()
def delete():
    show()
    trans_id = IntPrompt.ask("Enter transaction ID to delete")
    delete_transaction(trans_id)

@app.command()
def edit():
    show()
    trans_id = IntPrompt.ask("Enter transaction ID to edit")
    new_tipe = Prompt.ask("New Type", choices=["income", "expense"], default="expense")
    new_desc = Prompt.ask("New Description")
    new_amt = FloatPrompt.ask("New Amount")
    edit_transaction(trans_id, new_tipe, new_desc, new_amt)

if __name__ == "__main__":
    app()

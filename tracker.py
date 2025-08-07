from db import Session, Transaction
from rich.console import Console
from rich.table import Table
from rich import box
from rich.prompt import Prompt
from datetime import datetime   

console = Console()


def add_transaction(type_, description, amount):
    session = Session()
    trans = Transaction(
        type=type_,
        description=description,
        amount=amount,
        date=datetime.today()
    )
    session.add(trans)
    session.commit()
    session.close()
    console.print(
        f"✅ Transaksi berhasil ditambahkan: [bold cyan]{type_}[/bold cyan] - [green]{description}[/green] - [magenta]Rp{amount:,.2f}[/magenta] pada {datetime.today().date()}",
        style="bold green"
    )


def show_transactions():
    session = Session()
    transactions = session.query(Transaction).all()
    session.close()

    if not transactions:
        console.print("⚠️ Tidak ada transaksi yang ditemukan.", style="yellow")
        return

    table = Table(title="📒 Daftar Transaksi", box=box.ROUNDED)
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Tipe", style="magenta")
    table.add_column("Deskripsi", style="green")
    table.add_column("Jumlah", justify="right", style="blue")
    table.add_column("Tanggal", justify="center", style="yellow")

    total_income = 0.0
    total_expense = 0.0 

    for t in transactions:
        table.add_row(
            str(t.id),
            t.type.capitalize(),
            t.description,
            f"Rp{t.amount:,.2f}",
            t.date.strftime("%Y-%m-%d")
        )
        if t.type.lower() == 'income':
            total_income += t.amount
        elif t.type.lower() == 'expense':
            total_expense += t.amount

    console.print(table)
    console.print(f"\n -> Total Pemasukan: [bold green]Rp{total_income:,.2f}[/bold green]")
    console.print(f"-> Total Pengeluaran: [bold red]Rp{total_expense:,.2f}[/bold red]")
    console.print(f"=> Saldo Akhir: [bold blue]Rp{total_income - total_expense:,.2f}[/bold blue] <=\n")


def delete_transaction(transaction_id: int):
    session = Session()
    transaction = session.query(Transaction).filter_by(id=transaction_id).first()
    if transaction:
        session.delete(transaction)
        session.commit()
        session.close()
        console.print(f"Transaksi dengan ID {transaction_id} berhasil dihapus.", style="bold green")
        return True
    else:
        session.close()
        console.print(f"Transaksi dengan ID {transaction_id} tidak ditemukan.", style="bold red")
        return False


def edit_transaction(transaction_id: int, new_tipe: int, new_description: str, new_amount: float):
    session = Session()
    transaction = session.query(Transaction).filter_by(id=transaction_id).first()
    if transaction:
        transaction.type = new_tipe
        transaction.description = new_description
        transaction.amount = new_amount
        session.commit()
        session.close()
        console.print(f"Transaksi ID {transaction_id} berhasil diperbarui.", style="bold green")
        return True
    else:
        session.close()
        console.print(f"Transaksi dengan ID {transaction_id} tidak ditemukan.", style="bold red")
        return False

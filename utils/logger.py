import datetime
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

console = Console()

class MessageLogger:
    def __init__(self):
        self.logs = []

    def add_log(self, msg_type, params, direction="sent"):
        log_entry = {
            "id": len(self.logs) + 1,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "type": msg_type,
            "params": params,
            "direction": direction
        }
        self.logs.append(log_entry)
        return log_entry

    def display_all(self):
        if not self.logs:
            console.print("[bold red][!] No messages logged yet.[/bold red]")
            return

        table = Table(title="--- MESSAGE HISTORY ---", header_style="bold magenta")
        table.add_column("ID", justify="center", style="cyan")
        table.add_column("Timestamp", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Direction", style="bright_cyan")

        for log in self.logs:
            direction_style = "[green]" if log['direction'] == "sent" else "[blue]"
            direction_text = f"{direction_style}{log['direction'].upper()}[/green]" if log['direction'] == "sent" else f"{direction_style}{log['direction'].upper()}[/blue]"
            table.add_row(str(log['id']), log['timestamp'], log['type'], direction_text)

        console.print(table)

    def display_details(self, log_id):
        try:
            log = next(l for l in self.logs if l["id"] == int(log_id))
            detail_text = "\n".join([f"[bold cyan]{k.upper()}:[/bold cyan] {v}" for k, v in log['params'].items()])
            console.print(Panel(detail_text, title=f"Message {log['id']} Details", border_style="green", expand=False))
        except (StopIteration, ValueError, KeyError):
            console.print("[bold red][!] Invalid ID or data error.[/bold red]")
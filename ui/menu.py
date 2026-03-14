from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from core.network import NetworkNode
from utils.logger import MessageLogger
import sys

# Critical: Initialize console for Rich output
console = Console()

class AppInterface:
    def __init__(self, mode):
        self.mode = mode
        self.node = NetworkNode()
        self.node.logger = MessageLogger()

    def setup_connection(self):
        try:
            if self.mode == "server":
                console.print(f"[bold blue][*][/bold blue] Server started, listening on port {self.node.port}...")
                self.node.initialize_server()
                console.print(f"[bold green][+] A client has connected![/bold green]")
            else:
                console.print("[bold blue][*][/bold blue] Connecting to server...")
                self.node.initialize_client()
                console.print("[bold green][+] Successfully connected to server![/bold green]")
            
            self.node.start_receiver()
        except Exception as e:
            console.print(f"[bold red][!] Connection error: {e}[/bold red]")
            sys.exit(1)

    def run(self):
        self.setup_connection()
        while True:
            menu_text = (
                "[bold cyan]1.[/bold cyan] Send Message 1 (Personal Info)\n"
                "[bold cyan]2.[/bold cyan] Send Message 2 (Education Info)\n"
                "[bold cyan]3.[/bold cyan] View Message Logs\n"
                "[bold red]0.[/bold red] Exit"
            )
            console.print("\n", Panel(menu_text, title=f"[bold white]{self.mode.upper()} MAIN PAGE[/bold white]", border_style="bright_magenta"))
            
            choice = Prompt.ask("Selection", choices=["1", "2", "3", "0"])
            
            if choice == "1": 
                self.send_type_1()
            elif choice == "2": 
                self.send_type_2()
            elif choice == "3": 
                self.view_logs()
            elif choice == "0": 
                console.print("[bold yellow]Exiting application...[/bold yellow]")
                break

    def send_type_1(self):
        console.print("\n[bold yellow]>>> Message 1 Parameters (Personal)[/bold yellow]")
        p = {
            "name": Prompt.ask("Name"),
            "surname": Prompt.ask("Surname"),
            "age": Prompt.ask("Age"),
            "residence": Prompt.ask("Residence")
        }
        self.node.send_data("MESSAGE_TYPE_1", p)
        console.print("[bold green]✔ Message 1 sent![/bold green]")

    def send_type_2(self):
        console.print("\n[bold yellow]>>> Message 2 Parameters (Education)[/bold yellow]")
        p = {
            "degree": Prompt.ask("Education Degree"),
            "institution": Prompt.ask("Institution Name"),
            "graduation_year": Prompt.ask("Graduation Year")
        }
        self.node.send_data("MESSAGE_TYPE_2", p)
        console.print("[bold green]✔ Message 2 sent![/bold green]")

    def view_logs(self):
        self.node.logger.display_all()
        if self.node.logger.logs:
            log_id = Prompt.ask("\nEnter ID for details (Press 0 to go back)")
            if log_id != "0":
                self.node.logger.display_details(log_id)
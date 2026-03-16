from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from core.network import NetworkNode
from utils.logger import MessageLogger
from utils.validators import (
    validate_string, validate_integer, validate_year,
    prompt_with_validation, prompt_with_selection, DEGREE_OPTIONS
)
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

    def _ask_loop_turns(self):
        """Ask user how many loop turns should happen between sides."""
        console.print("\n[bold cyan]>>> Conversation Loop Settings[/bold cyan]")
        console.print("[dim]Each turn = one full back-and-forth exchange (send + receive).[/dim]")
        while True:
            turns_str = Prompt.ask("How many loop turns should happen? (0 for no auto-response)")
            try:
                turns = int(turns_str)
                if turns < 0:
                    console.print("[bold red]Please enter a non-negative number.[/bold red]")
                    continue
                return turns
            except ValueError:
                console.print("[bold red]Please enter a valid integer.[/bold red]")

    def _warn_missing_opposite_params(self, current_type, loop_turns):
        if loop_turns <= 0:
            return

        opposite_type = "MESSAGE_TYPE_2" if current_type == "MESSAGE_TYPE_1" else "MESSAGE_TYPE_1"
        if opposite_type not in self.node.saved_params:
            console.print(
                f"[bold yellow][Warning][/bold yellow] No saved params for {opposite_type}. "
                "Auto-responses will be skipped until that message type is sent manually."
            )

    def send_type_1(self):
        console.print("\n[bold yellow]>>> Message 1 Parameters (Personal)[/bold yellow]")
        p = {
            "name": prompt_with_validation("Name", validate_string, "Name"),
            "surname": prompt_with_validation("Surname", validate_string, "Surname"),
            "age": prompt_with_validation("Age", validate_integer, "Age"),
            "residence": prompt_with_validation("Residence", validate_string, "Residence")
        }
        loop_turns = self._ask_loop_turns()
        self._warn_missing_opposite_params("MESSAGE_TYPE_1", loop_turns)
        self.node.send_data("MESSAGE_TYPE_1", p, remaining_turns=loop_turns, turn_phase="request")
        console.print(f"[bold green]✔ Message 1 sent with {loop_turns} loop turn(s)![/bold green]")

    def send_type_2(self):
        console.print("\n[bold yellow]>>> Message 2 Parameters (Education)[/bold yellow]")
        p = {
            "degree": prompt_with_selection("Education Degree", DEGREE_OPTIONS),
            "institution": prompt_with_validation("Institution Name", validate_string, "Institution"),
            "graduation_year": prompt_with_validation("Graduation Year", validate_year, "Graduation Year")
        }
        loop_turns = self._ask_loop_turns()
        self._warn_missing_opposite_params("MESSAGE_TYPE_2", loop_turns)
        self.node.send_data("MESSAGE_TYPE_2", p, remaining_turns=loop_turns, turn_phase="request")
        console.print(f"[bold green]✔ Message 2 sent with {loop_turns} loop turn(s)![/bold green]")

    def view_logs(self):
        while True:
            self.node.logger.display_all()
            if not self.node.logger.logs:
                Prompt.ask("\nPress Enter to return to main menu")
                break

            log_id = Prompt.ask("\nEnter ID for details (Press 0 to go back)")
            if log_id == "0":
                break

            self.node.logger.display_details(log_id)

            # Show navigation options after viewing details
            nav_text = (
                "[bold cyan]1.[/bold cyan] Back to message table\n"
                "[bold cyan]2.[/bold cyan] Back to main page"
            )
            console.print("\n", Panel(nav_text, title="[bold white]Navigation[/bold white]", border_style="bright_blue"))
            nav_choice = Prompt.ask("Selection", choices=["1", "2"])

            if nav_choice == "2":
                break
            # If choice is 1, loop continues and shows the table again
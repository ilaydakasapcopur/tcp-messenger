from rich.console import Console
from rich.panel import Panel
from ui.menu import AppInterface

console = Console()

def main():
    banner = """
    [bold cyan]
     _____ ____ ____     __  __ _____ ____ ____  
    |_   _/ ___|  _ \   |  \/  | ____/ ___/ ___| 
      | || |   | |_) |  | |\/| |  _| \___ \___ \ 
      | || |___|  __/   | |  | | |___ ___) |___) |
      |_| \____|_|      |_|  |_|_____|____/|____/ 
    [/bold cyan]
    """
    console.print(Panel(banner, subtitle="TCP Messaging CLI v1.0", border_style="blue"))
    
    console.print("[bold white]1.[/bold white] [green]Server Modu[/green]")
    console.print("[bold white]2.[/bold white] [blue]Client Modu[/blue]")
    
    choice = console.input("\n[bold yellow]Mod Seçiniz:[/bold yellow] ")
    mode = "server" if choice == "1" else "client"
    
    app = AppInterface(mode)
    app.run()

if __name__ == "__main__":
    main()
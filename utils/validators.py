"""Validation utilities for message parameters."""
import re
from rich.console import Console
from rich.prompt import Prompt

console = Console()


def validate_string(value, field_name):
    """Validate that a value is a non-empty string containing only letters and spaces."""
    if not value or not isinstance(value, str):
        return False, f"{field_name} must be a non-empty string."
    # Check if contains only letters and spaces
    if not re.match(r'^[a-zA-Z\s]+$', value.strip()):
        return False, f"{field_name} must contain only letters and spaces."
    return True, None


def validate_integer(value, field_name):
    """Validate that a value is a valid integer."""
    try:
        int(value)
        return True, None
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid integer."


def validate_year(value, field_name="Year"):
    """Validate that a value is a 4-digit year."""
    try:
        year = int(value)
        if len(str(value)) != 4:
            return False, f"{field_name} must be exactly 4 digits."
        return True, None
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid 4-digit integer."


def prompt_with_validation(prompt_text, validator_func, field_name):
    """Prompt user for input with validation, retrying until valid."""
    while True:
        value = Prompt.ask(prompt_text)
        is_valid, error_msg = validator_func(value, field_name)
        if is_valid:
            return value
        console.print(f"[bold red]✗ {error_msg}[/bold red] Please try again.")


def prompt_with_selection(prompt_text, options):
    """Prompt user to select from a list of options."""
    console.print(f"\n[bold cyan]{prompt_text}[/bold cyan]")
    for idx, option in enumerate(options, 1):
        console.print(f"  [bold white]{idx}.[/bold white] {option}")

    while True:
        choice = Prompt.ask("Select option", choices=[str(i) for i in range(1, len(options) + 1)])
        return options[int(choice) - 1]


DEGREE_OPTIONS = ["high school", "bachelor", "master", "PhD"]

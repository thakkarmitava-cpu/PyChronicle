import sys
from pathlib import Path

import click

from tracer.tracer import Tracer
from tracer.runtime_executor import execute_script


def run_tracer(script_path):
    """Run the target Python script with the PyChronicle tracer."""

    script_path = Path(script_path)

    # 1. Check file exists
    if not script_path.exists():
        click.echo(f"Error: File not found: {script_path}")
        return False

    # 2. Check it is a file
    if not script_path.is_file():
        click.echo(f"Error: Target path is not a file: {script_path}")
        return False

    # 3. Check Python extension
    if script_path.suffix.lower() != ".py":
        click.echo(
            "Error: Target file must be a Python (.py) file."
        )
        return False

    # 4. Check empty file
    try:
        if not script_path.read_text(encoding="utf-8").strip():
            click.echo(
                "Error: Target Python file is empty."
            )
            return False
    except OSError as error:
        click.echo(
            f"Error: Unable to read target file: {error}"
        )
        return False

    tracer = Tracer()

    try:
        # Remove previous runtime history
        tracer.storage.clear_table()

        # Start tracing
        sys.settrace(tracer.trace)

        # Execute target Python program
        execute_script(str(script_path))

        return True

    except SyntaxError as error:
        click.echo(
            "Error: The target Python file contains a syntax error."
        )

        if error.lineno:
            click.echo(
                f"Line {error.lineno}: {error.msg}"
            )

        return False

    except Exception as error:
        click.echo(
            f"Error while executing target script: {error}"
        )
        return False

    finally:
        # Always stop tracing
        sys.settrace(None)


@click.group()
def cli():
    """PyChronicle - Python Runtime Execution Visualizer."""
    pass


@cli.command()
@click.argument(
    "script",
    type=click.Path(
        exists=False,
        dir_okay=False,
        path_type=Path
    )
)
@click.option(
    "--no-ui",
    is_flag=True,
    help="Run the tracer without opening the Textual UI."
)
def run(script, no_ui):
    """Trace a Python script and optionally open the Runtime Viewer."""

    click.echo("=" * 55)
    click.echo("PyChronicle")
    click.echo("Python Runtime Execution Visualizer")
    click.echo("=" * 55)
    click.echo()

    click.echo(f"Target file: {script}")
    click.echo()

    success = run_tracer(script)

    if not success:
        raise click.exceptions.Exit(1)

    click.echo("Runtime tracing completed successfully.")
    click.echo()

    if no_ui:
        click.echo("UI disabled (--no-ui).")
        return

    # Start Runtime Viewer
    try:
        from ui.app import PyChronicleUI

        click.echo("Starting PyChronicle Runtime Viewer...")
        app = PyChronicleUI()
        app.run()

    except Exception as error:
        click.echo(
            f"Error starting Runtime Viewer: {error}"
        )
        raise click.exceptions.Exit(1)


if __name__ == "__main__":
    cli()
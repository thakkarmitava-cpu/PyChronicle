import argparse
import os

from main import run_script


def main():
    parser = argparse.ArgumentParser(
        prog="pychronicle",
        description="PyChronicle - Python Runtime Tracing Tool"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    run_parser = subparsers.add_parser(
        "run",
        help="Run a Python script with PyChronicle"
    )

    run_parser.add_argument(
        "script",
        help="Path to the Python script"
    )

    args = parser.parse_args()

    if args.command == "run":

        # Check whether file exists
        if not os.path.isfile(args.script):
            print(f"Error: File not found: {args.script}")
            return

        # Check Python file extension
        if not args.script.endswith(".py"):
            print("Error: Please provide a Python (.py) file.")
            return

        # Check whether file is empty
        if os.path.getsize(args.script) == 0:
            print(f"Error: Python file is empty: {args.script}")
            return

        print(f"Running PyChronicle on: {args.script}")
        run_script(args.script)


if __name__ == "__main__":
    main()
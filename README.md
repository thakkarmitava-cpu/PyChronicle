# PyChronicle

## Description

PyChronicle is a Python AST-based execution analyzer that parses Python source code and stores detected variables in an SQLite database.

## Features

- Parse Python source code
- Detect variable assignments
- Detect tuple assignments
- Detect augmented assignments
- Detect for-loop variables
- Store variables in SQLite

## Week 2

- Runtime Variable Tracing using sys.settrace()
- Runtime Execution using exec()
- Store runtime logs in SQLite
- Textual Terminal UI

## Week 3 Updates

### New Features

- Implemented delta compression for runtime variables.
- Added timeline slider for time-scrubbing.
- Added code highlighting for the current execution line.
- Added line numbers in the code preview.
- Improved runtime viewer UI.
- Refactored UI update logic to reduce duplicate code.
- Added safe handling for empty runtime data.
- Improved navigation button behavior.

## Week 4 Updates

### Team Member 1 – CLI, Testing and Documentation

#### CLI Support

- Added PyChronicle command-line interface.
- Added support for running Python scripts through the CLI.
- Added Python file path validation.
- Added .py file extension validation.
- Added empty Python file validation.
- Added user-friendly error messages for invalid inputs.
- Added CLI help and usage information.

#### CLI Usage

Run a Python script using PyChronicle:

```bash
python cli.py run examples/test.py
```

Show CLI help:

```bash
python cli.py --help
```

### Team Member 2 – Watch Variables and Advanced UI

#### Watch Variables

- Added support for selecting variables to monitor.
- Added filtering to display only selected variables.
- Added a dedicated Watch Variables section.

#### Timeline Integration

- Integrated watched variables with Previous and Next navigation.
- Integrated watched variables with the timeline slider.
- Updated watched variable values when the execution step changes.

#### UI Enhancement

- Improved Runtime Viewer layout.
- Improved spacing and formatting.
- Added a separate Watch Variables panel.
- Improved headers and runtime information display.

#### Integration

- Integrated Watch Variables with Runtime Database.
- Integrated Watch Variables with Timeline Viewer.
- Integrated with Code Highlighting.
- Integrated with Delta Updates.

## Technologies

- Python
- AST
- SQLite3
- Textual
- sys.settrace
- textual-slider

## Current Features

- AST Parsing
- Runtime Tracing
- SQLite Storage
- Delta Compression
- Timeline Navigation
- Code Highlighting
- Runtime Viewer
- CLI Execution
- Input Validation
- Error Handling
- Watch Variables
- Variable Filtering
- Advanced Runtime Viewer UI

## Project Structure

```text
PyChronicle/
├── examples/
├── parser/
├── storage/
├── tracer/
├── ui/
├── cli.py
├── main.py
├── README.md
└── requirements.txt
```

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Run

Run a Python script using PyChronicle:

```bash
python cli.py run examples/test.py
```

Show CLI help:

```bash
python cli.py --help
```

## CLI Help Output

```text
usage: pychronicle [-h] {run} ...

PyChronicle - Python Runtime Tracing Tool

positional arguments:
  {run}
    run       Run a Python script with PyChronicle

options:
  -h, --help  show this help message and exit
```

## Testing

Tested with:

- Variable assignment
- If-Else statements
- For loops
- While loops
- Functions
- Nested functions
- Recursive functions
- Empty Python files
- Invalid file paths
- Invalid file extensions

## Runtime Components Tested

- AST Parser
- Runtime Tracer
- SQLite Storage
- Delta Compression
- CLI Execution
- Error Handling
- Timeline Navigation
- Previous/Next Navigation
- Code Highlighting
- Runtime Viewer
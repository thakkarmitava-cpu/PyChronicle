# PyChronicle

## Overview

PyChronicle is a Python application that traces the execution of a Python program. It records variable changes during runtime, stores them in an SQLite database, and displays the execution history through a Textual Terminal UI.

## Features

### Week 1 – Static Code Analysis

- Parse Python source code using the `ast` module
- Detect variable assignments
- Detect tuple assignments
- Detect augmented assignments
- Detect loop variables
- Store parsed variables in SQLite

### Week 2 – Runtime Execution Tracing

- Execute Python programs dynamically using `exec()`
- Trace program execution using `sys.settrace()`
- Record runtime variable changes (Delta Tracking)
- Store runtime execution history in SQLite
- View execution history using a Textual Terminal UI
- Navigate execution using Previous, Next, and Timeline Slider

## Project Workflow

```text
main.py
    │
    ▼
runtime_executor.py
    │
    ▼
examples/test.py
    │
    ▼
Tracer (sys.settrace)
    │
    ▼
runtime_storage.py
    │
    ▼
SQLite Database
    │
    ▼
Textual UI
```
This workflow shows how the application executes a Python program, traces runtime events, stores them in SQLite, and visualizes the execution history through the Textual UI.

## Technologies Used

- Python
- AST (Abstract Syntax Tree)
- SQLite3
- Textual
- textual-slider

## Running the Project

### Generate Runtime Execution Logs

```bash
python main.py
```
This executes the sample Python program and stores runtime execution history in the SQLite database.


### Launch the Terminal UI

```bash
python -m ui.app
```

The UI displays:

- Runtime Step
- Executed Line Number
- Function Name
- Changed Variables (Delta)
- Current Source Code
- Timeline Slider
- Previous / Next Navigation

## License

This project was developed as part of the Infotact Solutions Internship Program.
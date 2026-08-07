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
### Week 2

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

## Run

```bash
python main.py
 
import sys

from tracer.tracer import Tracer
from parser.ast_parser import parse_file
from storage.sqlite_storage import Storage


# -----------------------------
# Start Runtime Tracer
# -----------------------------
tracer = Tracer()
sys.settrace(tracer.trace)

# Parse Python File
variables = parse_file("examples/test.py")

# Stop Tracer
sys.settrace(None)

# -----------------------------
# Week 1 Database Code
# -----------------------------
storage = Storage()

storage.create_table()

storage.clear_table()

for variable in variables:
    storage.insert_variable(variable)

print("All Variables Saved")

rows = storage.get_all_variables()

for row in rows:
    print(row)
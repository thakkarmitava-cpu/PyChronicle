from parser.ast_parser import parse_file
from storage.sqlite_storage import Storage

variables = parse_file("examples/test.py")

storage = Storage()

storage.create_table()

storage.clear_table()

for variable in variables:
    storage.insert_variable(variable)

print("All Variables Saved")

rows = storage.get_all_variables()

for row in rows:
    print(row)
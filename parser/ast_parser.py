import ast

with open("sample/test.py", "r") as file:
    code = file.read()

tree = ast.parse(code)


variables = []

for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        variables.append({
            "variable": node.targets[0].id,
            "line": node.lineno,
            "type": "Assign"
        })

print(variables)
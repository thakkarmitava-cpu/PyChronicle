import ast


def parse_file(file_path):

    with open(file_path, "r") as file:
        code = file.read()

    tree = ast.parse(code)

    variables = []

    for node in ast.walk(tree):

        # x = 10
        if isinstance(node, ast.Assign):

            target = node.targets[0]

            if isinstance(target, ast.Name):
                variables.append({
                    "variable": target.id,
                    "line": node.lineno,
                    "type": "Assign"
                })

            elif isinstance(target, ast.Tuple):
                for item in target.elts:
                    if isinstance(item, ast.Name):
                        variables.append({
                            "variable": item.id,
                            "line": node.lineno,
                            "type": "Tuple Assign"
                        })

        # count += 1
        elif isinstance(node, ast.AugAssign):

            if isinstance(node.target, ast.Name):
                variables.append({
                    "variable": node.target.id,
                    "line": node.lineno,
                    "type": "AugAssign"
                })

        # for i in range()
        elif isinstance(node, ast.For):

            if isinstance(node.target, ast.Name):
                variables.append({
                    "variable": node.target.id,
                    "line": node.lineno,
                    "type": "For Loop"
                })

    return variables
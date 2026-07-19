def execute_script(file_path):

    with open(file_path, "r") as file:
        code = file.read()

    globals_dict = {
        "__name__": "__main__",
        "__file__": file_path,
    }

    exec(compile(code, file_path, "exec"), globals_dict)
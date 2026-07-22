import os
from storage.runtime_storage import RuntimeStorage

class Tracer:
     def __init__(self):
        self.storage = RuntimeStorage()
        self.storage.create_table()
        self.previous_variables = {}

     def trace(self, frame, event, arg):

        filename = os.path.basename(frame.f_code.co_filename)

        # ફક્ત test.py trace કરવું
        if filename != "test.py":
              return self.trace

        # ફક્ત line event
        if event != "line":
            return self.trace

        print(f"Line : {frame.f_lineno}")
        print(f"Function : {frame.f_code.co_name}")

        variables = {}

        for key, value in frame.f_locals.items():
            if not key.startswith("__"):
                variables[key] = value
        delta = {}

        for key, value in variables.items():
         if (
         key not in self.previous_variables
         or self.previous_variables[key] != value
         ):
          delta[key] = value

        self.previous_variables = variables.copy()
        print("Delta :", delta)
        self.storage.insert_runtime(
                     frame.f_lineno,
                     frame.f_code.co_name,
                    delta
                             )
        print("-" * 40)

        return self.trace
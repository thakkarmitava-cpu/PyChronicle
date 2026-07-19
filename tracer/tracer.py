import os

class Tracer:

    def trace(self, frame, event, arg):
        print("TRACE RUNNING")

        filename = frame.f_code.co_filename

        # if os.path.basename(filename) != "test.py":
        #     return self.trace

        print(f"Event : {event}")
        print(f"Function : {frame.f_code.co_name}")
        print(f"Line : {frame.f_lineno}")
        print("-------------------------")

        return self.trace
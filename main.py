import sys

from tracer.tracer import Tracer
from tracer.runtime_executor import execute_script


def run_script(script_path):
    target_file = script_path.split("/")[-1].split("\\")[-1]

    tracer = Tracer(target_file)

    tracer.storage.clear_table()

    sys.settrace(tracer.trace)

    try:
        execute_script(script_path)
    finally:
        sys.settrace(None)


if __name__ == "__main__":
    run_script("examples/test.py")
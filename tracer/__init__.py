class Tracer:

    def __init__(self):
        self.storage = RuntimeStorage()
        self.storage.create_table()

        self.previous_variables = {}
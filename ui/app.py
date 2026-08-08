import ast

from storage.runtime_storage import RuntimeStorage
from textual.app import App
from textual.widgets import Header, Footer, Static, Button
from textual_slider import Slider
from textual.containers import Horizontal
from pathlib import Path


class PyChronicleUI(App):

    CSS = """
    #viewer {
        width: 100%;
        height: 1fr;
    }

    #content {
        width: 70%;
        height: 1fr;
        padding: 1 2;
        border: round $accent;
    }

    #watch_panel {
        width: 30%;
        height: 1fr;
        padding: 1 2;
        border: round $accent;
    }

    #timeline {
        width: 100%;
        margin: 1 2;
    }

    #navigation {
        width: 100%;
        height: auto;
        align: center middle;
    }
    """

    def __init__(self):
        super().__init__()

        self.storage = RuntimeStorage()

        self.runtime_data = self.storage.get_all_runtime()

        self.current_index = 0

        # Variables we want to monitor
        self.watched_variables = [
            "x",
            "count",
            "total"
        ]

        self.source_lines = (
            Path("examples/test.py")
            .read_text()
            .splitlines()
        )

    def compose(self):
        yield Header()

        if self.runtime_data:

            line, function, variables = (
                self.runtime_data[self.current_index]
            )

            text = (
                "PyChronicle Runtime Viewer\n"
                + "=" * 35
                + "\n\n"

                + f"Step : "
                f"{self.current_index + 1}/"
                f"{len(self.runtime_data)}\n"

                + f"Total Records : "
                f"{len(self.runtime_data)}\n\n"

                + f"Line : {line}\n"
                + f"Function : {function}\n\n"

                + "=" * 30
                + "\n"
                + "Delta\n"
                + "=" * 30
                + "\n"

                + f"{variables}\n\n"

                + "=" * 30
                + "\n"
                + "Code\n"
                + "=" * 30
                + "\n"

                + self.build_code_view(line)
            )

        else:

            text = (
                "PyChronicle Runtime Viewer\n\n"
                "No runtime execution data available.\n\n"
                "Run the tracer first to generate "
                "execution history."
            )

        # Main viewer + separate Watch Variables panel
        yield Horizontal(
            Static(
                text,
                id="content"
            ),

            Static(
                self.build_watch_panel(),
                id="watch_panel"
            ),

            id="viewer"
        )

        # Timeline
        yield Slider(
            min=0,
            max=max(
                0,
                len(self.runtime_data) - 1
            ),
            value=self.current_index,
            id="timeline"
        )

        # Navigation
        yield Horizontal(
            Button(
                "◀ Previous",
                id="prev",
                disabled=(
                    self.current_index == 0
                )
            ),

            Button(
                "Next ▶",
                id="next",
                disabled=(
                    not self.runtime_data
                    or self.current_index
                    == len(self.runtime_data) - 1
                )
            ),

            id="navigation"
        )

        yield Footer()

    def on_button_pressed(
        self,
        event: Button.Pressed
    ):
        if not self.runtime_data:
            return

        if event.button.id == "next":

            if (
                self.current_index
                < len(self.runtime_data) - 1
            ):
                self.current_index += 1

        elif event.button.id == "prev":

            if self.current_index > 0:
                self.current_index -= 1

        # Synchronize slider
        slider = self.query_one(
            "#timeline",
            Slider
        )

        slider.value = self.current_index

        # Update both panels
        self.update_content()

        self.update_buttons()

    def on_slider_changed(
        self,
        event: Slider.Changed
    ):
        if not self.runtime_data:
            return

        self.current_index = int(event.value)

        # Update both panels
        self.update_content()

        self.update_buttons()

    def update_content(self):

        if not self.runtime_data:
            return

        line, function, variables = (
            self.runtime_data[self.current_index]
        )

        text = (
            "PyChronicle Runtime Viewer\n"
            + "=" * 35
            + "\n\n"

            + f"Step : "
            f"{self.current_index + 1}/"
            f"{len(self.runtime_data)}\n"

            + f"Total Records : "
            f"{len(self.runtime_data)}\n\n"

            + f"Line : {line}\n"
            + f"Function : {function}\n\n"

            + "=" * 30
            + "\n"
            + "Delta\n"
            + "=" * 30
            + "\n"

            + f"{variables}\n\n"

            + "=" * 30
            + "\n"
            + "Code\n"
            + "=" * 30
            + "\n"

            + self.build_code_view(line)
        )

        # Update main viewer
        content = self.query_one(
            "#content",
            Static
        )

        content.update(text)

        # Update Watch Variables panel
        watch_panel = self.query_one(
            "#watch_panel",
            Static
        )

        watch_panel.update(
            self.build_watch_panel()
        )

    def update_buttons(self):

        if not self.runtime_data:
            return

        prev = self.query_one(
            "#prev",
            Button
        )

        next_button = self.query_one(
            "#next",
            Button
        )

        prev.disabled = (
            self.current_index == 0
        )

        next_button.disabled = (
            self.current_index
            == len(self.runtime_data) - 1
        )

    def build_code_view(self, current_line):

        code = []

        code.append(
            "Line | Source Code"
        )

        code.append(
            "-------------------------------"
        )

        start = max(
            1,
            current_line - 3
        )

        end = min(
            len(self.source_lines),
            current_line + 3
        )

        for line_no in range(
            start,
            end + 1
        ):

            source_line = (
                self.source_lines[line_no - 1]
            )

            if line_no == current_line:

                code.append(
                    f">>> {line_no:3} | "
                    f"{source_line}"
                )

            else:

                code.append(
                    f"    {line_no:3} | "
                    f"{source_line}"
                )

        return "\n".join(code)

    def build_watch_panel(self):

        panel = []

        panel.append(
            "WATCH VARIABLES"
        )

        panel.append(
            "=" * 25
        )

        # Initially no value
        watched_values = {
            variable: "-"
            for variable
            in self.watched_variables
        }

        # Read runtime history up to
        # the current timeline position
        for i in range(
            self.current_index + 1
        ):

            _, _, variables = (
                self.runtime_data[i]
            )

            try:

                variables = ast.literal_eval(
                    variables
                )

            except (ValueError, SyntaxError):

                variables = {}

            # Update only watched variables
            for variable in (
                self.watched_variables
            ):

                if variable in variables:

                    watched_values[
                        variable
                    ] = variables[variable]

        # Display watched variables
        for variable in (
            self.watched_variables
        ):

            panel.append(
                f"{variable} = "
                f"{watched_values[variable]}"
            )

        return "\n".join(panel)


if __name__ == "__main__":
    app = PyChronicleUI()
    app.run()
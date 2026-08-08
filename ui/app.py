import ast

from storage.runtime_storage import RuntimeStorage
from textual.app import App
from textual.widgets import Header, Footer, Static, Button, Checkbox
from textual_slider import Slider
from textual.containers import Horizontal, VerticalScroll
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

            VerticalScroll(
                Static(
                    text,
                    id="runtime_text"
                ),
                id="content"
    ),

            Static(
                self.build_watch_panel(),
                id="watch_panel",
                expand=True
    ),

    id="viewer"
)

        yield Horizontal(
            Checkbox(
                "x",
                value="x" in self.watched_variables,
                id="watch_x"
    ),

            Checkbox(
                "count",
                value="count" in self.watched_variables,
                id="watch_count"
    ),

            Checkbox(
                "total",
                value="total" in self.watched_variables,
                id="watch_total"
    ),

    id="watch_controls"
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
            "#runtime_text",
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

    def get_watched_values(self):

        watched_values = {
            variable: "-"
            for variable in self.watched_variables
    }

        # No runtime data available
        if not self.runtime_data:
           return watched_values

        # Make sure current index is valid
        end_index = min(
           self.current_index + 1,
           len(self.runtime_data)
    )

        # Read runtime history up to current timeline position
        for i in range(end_index):

            _, _, variables = self.runtime_data[i]

            try:
                variables = ast.literal_eval(variables)

            except (ValueError, SyntaxError, TypeError):
                variables = {}

            # Update only selected variables
            for variable in self.watched_variables:

                 if variable in variables:
                    watched_values[variable] = variables[variable]

        return watched_values


    def build_watch_panel(self):

        panel = []

        panel.append("WATCH VARIABLES")
        panel.append("=" * 25)

        watched_values = self.get_watched_values()

        if not self.watched_variables:
            panel.append("No variables selected.")
            return "\n".join(panel)

        # Display only selected variables
        for variable in self.watched_variables:

            panel.append(
                f"{variable} = {watched_values[variable]}"
        )

        return "\n".join(panel)

    def on_checkbox_changed(self, event: Checkbox.Changed):

        variable_map = {
            "watch_x": "x",
            "watch_count": "count",
            "watch_total": "total"
    }

        variable = variable_map.get(event.checkbox.id)

        if variable is None:
           return

        if event.value:
            if variable not in self.watched_variables:
                self.watched_variables.append(variable)
        else:
            if variable in self.watched_variables:
                self.watched_variables.remove(variable)

        watch_panel = self.query_one("#watch_panel", Static)
        watch_panel.update(self.build_watch_panel())

if __name__ == "__main__":
    app = PyChronicleUI()
    app.run()
from textual.app import App
from textual.widgets import Header, Footer, Static


class PyChronicleUI(App):
    def compose(self):
        yield Header()

        yield Static(
            "PyChronicle\n\n"
            "Code View\n"
            "----------------------\n"
            "Timeline Slider (Coming Soon)"
        )

        yield Footer()


if __name__ == "__main__":
    app = PyChronicleUI()
    app.run()
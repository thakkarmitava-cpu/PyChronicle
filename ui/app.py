from storage.runtime_storage import RuntimeStorage
from textual.app import App
from textual.widgets import Header, Footer, Static, Button
from textual_slider import Slider
from textual.containers import Horizontal
from pathlib import Path


class PyChronicleUI(App):
    def compose(self):
        yield Header()

        if self.runtime_data:
         line, function, variables = self.runtime_data[self.current_index]

         text = (
         "PyChronicle\n\n"
         f"Step : {self.current_index + 1}/{len(self.runtime_data)}\n\n"
         f"Line : {line}\n"
         f"Function : {function}\n\n"
         "Delta\n"
         "----------------------\n"
        f"{variables}\n\n"
        f"Code\n"
        f"----------------------\n"
        f"{self.source_lines[line-1]}"
         )
        else:
         text = "No Runtime Data"

        yield Static(text, id="content")
        yield Slider(min=0, max=len(self.runtime_data)-1, value=0, id="timeline")
        yield Horizontal(
        Button("Previous", id="prev"),
         Button("Next", id="next")
        )


        yield Footer()
    def __init__(self):
     super().__init__()

     self.storage = RuntimeStorage()

     self.runtime_data = self.storage.get_all_runtime()

     self.current_index = 0  
     self.source_lines = Path("examples/test.py").read_text().splitlines()

  


    # content.update(text)
    def on_button_pressed(self, event: Button.Pressed):
      print(event.button.id)

      if event.button.id == "next":
        if self.current_index < len(self.runtime_data) - 1:
            self.current_index += 1

      elif event.button.id == "prev":
        if self.current_index > 0:
            self.current_index -= 1

      content = self.query_one("#content", Static)

      line, function, variables = self.runtime_data[self.current_index]

      text = (
        f"PyChronicle\n\n"
        f"Step : {self.current_index + 1}/{len(self.runtime_data)}\n\n"
        f"Line : {line}\n"
        f"Function : {function}\n\n"
        f"Delta\n"
        f"----------------------\n"
        f"{variables}"
     )
      code = self.source_lines[line - 1]
      text += f"\n\nCode\n----------------------\n{code}"

      content.update(text) 
      slider = self.query_one("#timeline", Slider)
      slider.value = self.current_index
    def on_slider_changed(self, event: Slider.Changed):
      print("Slider moved:", event.value)
      self.current_index = int(event.value)

      row = self.runtime_data[self.current_index]
      line = row[0]
      function = row[1]
      variables = row[2]

      text = (
        f"Step : {self.current_index + 1}/{len(self.runtime_data)}\n\n"
        f"Line : {line}\n"
        f"Function : {function}\n\n"
        f"Delta\n"
        f"----------------------\n"
        f"{variables}"
     )

      code = self.source_lines[line - 1]
      text += f"\n\nCode\n----------------------\n{code}"

      content = self.query_one("#content", Static)
      content.update(text)      



if __name__ == "__main__":
    app = PyChronicleUI()
    app.run()
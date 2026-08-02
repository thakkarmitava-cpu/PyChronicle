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

        #  text = (
        #  "PyChronicle\n\n"
        #  f"Step : {self.current_index + 1}/{len(self.runtime_data)}\n\n"
        #  f"Line : {line}\n"
        #  f"Function : {function}\n\n"
        #  "Delta\n"
        #  "----------------------\n"
        # f"{variables}\n"
        # )
         code = self.build_code_view(line)
         text = (
         "PyChronicle\n\n"
         f"Step : {self.current_index + 1}/{len(self.runtime_data)}\n\n"
         f"Line : {line}\n"
         f"Function : {function}\n\n"
         "Delta\n"
         "----------------------\n"
         f"{variables}\n\n"
         "Code\n"
         "----------------------\n"
        f"{code}"
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

      # content = self.query_one("#content", Static)

    #   line, function, variables = self.runtime_data[self.current_index]

    #   text = (
    #     f"PyChronicle\n\n"
    #     f"Step : {self.current_index + 1}/{len(self.runtime_data)}\n\n"
    #     f"Line : {line}\n"
    #     f"Function : {function}\n\n"
    #     f"Delta\n"
    #     f"----------------------\n"
    #     f"{variables}"
    #  )
    #   code = self.build_code_view(line)
    #   text += f"\n\nCode\n----------------------\n{code}"

    #   content.update(text) 
      slider = self.query_one("#timeline", Slider)
      slider.value = self.current_index
      self.update_content()

    def on_slider_changed(self, event: Slider.Changed):
      print("Slider moved:", event.value)
      self.current_index = int(event.value)

  
      self.update_content()

    def update_content(self):
     line, function, variables = self.runtime_data[self.current_index]
     text = (
        "PyChronicle\n\n"
        f"Step : {self.current_index + 1}/{len(self.runtime_data)}\n\n"
        f"Line : {line}\n"
        f"Function : {function}\n\n"
        "Delta\n"
        "----------------------\n"
        f"{variables}\n\n"
        "Code\n"
        "----------------------\n"
        f"{self.build_code_view(line)}"
     )
     content = self.query_one("#content", Static)
     content.update(text)
    
    def build_code_view(self, current_line):
        code = []

        start = max(1, current_line - 3)
        end = min(len(self.source_lines), current_line + 3)

        for line_no in range(start, end + 1):
          source_line = self.source_lines[line_no - 1]

          if line_no == current_line:
            code.append(f">>>   {line_no:2} |{source_line}")
          else:
            code.append(f"     {line_no:2} |    {source_line}")

        return "\n".join(code)
   



if __name__ == "__main__":
    app = PyChronicleUI()
    app.run()
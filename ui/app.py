import ast
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
         text = (
    "PyChronicle\n\n"
    "No runtime execution data available.\n\n"
    "Run the tracer first to generate execution history."
)


      
        yield Static(text, id="content",  expand=True)
        yield Slider( min=0,max=max(0, len(self.runtime_data) - 1),value=self.current_index, id="timeline",)

        yield  Horizontal(
    Button(
        "◀ Previous",
        id="prev",
        disabled=self.current_index == 0
    ),
    Button(
        "Next ▶",
        id="next",
        disabled=self.current_index == len(self.runtime_data) - 1
    ),
    id="navigation"
)


        yield Footer()
    def __init__(self):
     super().__init__()

     self.storage = RuntimeStorage()

     self.runtime_data = self.storage.get_all_runtime()

     self.current_index = 0  
     self.watched_variables = ["x", "count", "total"]
     self.source_lines = Path("examples/test.py").read_text().splitlines()

  


    # content.update(text)
    def on_button_pressed(self, event: Button.Pressed):
      print("Button pressed:", event.button.id)

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
      
      self.update_buttons()

    def on_slider_changed(self, event: Slider.Changed):
      print("Slider moved:", event.value)
      self.current_index = int(event.value)

      self.update_content()
      
      self.update_buttons()
    
      # Update runtime information and code preview
    def update_content(self):
     line, function, variables = self.runtime_data[self.current_index]
     text = (
        "PyChronicle Runtime Viewer\n"
        + "=" * 35 + "\n\n"

        + f"Step : {self.current_index + 1}/{len(self.runtime_data)}\n"
        + f"Total Records : {len(self.runtime_data)}\n\n"

        + f"Line : {line}\n"
        + f"Function : {function}\n\n"

        + self.build_watch_panel()

        + "\n\n"

        + "=" * 30
        + "\nDelta\n"
        + "=" * 30
        + "\n"

        + f"{variables}"

        + "\n\n"

        + "=" * 30
        + "\nCode\n"
        + "=" * 30
        + "\n"

        + self.build_code_view(line)
     )
     content = self.query_one("#content", Static)
     content.update(text)
    # Enable or disable navigation buttons
    def update_buttons(self):
     prev = self.query_one("#prev", Button)
     next_btn = self.query_one("#next", Button)

     prev.disabled = self.current_index == 0
     next_btn.disabled = (
        self.current_index == len(self.runtime_data) - 1
    )  
     # Build highlighted code preview
    
    def build_code_view(self, current_line):
        code = []
        code.append("Line | Source Code")
        code.append("-------------------------------")

        start = max(1, current_line - 3)
        end = min(len(self.source_lines), current_line + 3)

        for line_no in range(start, end + 1):
          source_line = self.source_lines[line_no - 1]

          if line_no == current_line:
            code.append(f">>>   {line_no:2} |{source_line}")
          else:
            code.append(f"     {line_no:2} |    {source_line}")

        return "\n".join(code)
    def build_watch_panel(self):
        panel = []
        panel.append("=" * 30)
        panel.append(" Watch Variables ")
        panel.append("=" * 30)

        # Stores the latest values of watched variables
        watched_values = {var: "-" for var in self.watched_variables}

        # Read runtime history from the beginning up to current step
        for i in range(self.current_index + 1):
            _, _, variables = self.runtime_data[i]

            try:
               variables = ast.literal_eval(variables)
            except Exception:
               variables = {}

        # Update watched variable values
            for var in self.watched_variables:
              if var in variables:
                watched_values[var] = variables[var]

    # Display the latest values
        for var in self.watched_variables:
            panel.append(f"{var} = {watched_values[var]}")

        return "\n".join(panel)
   

if __name__ == "__main__":
    app = PyChronicleUI()
    app.run()
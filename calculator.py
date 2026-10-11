import tkinter as tk
from tkinter import font


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("420x760")
        self.configure(bg="#000000")
        self.resizable(False, False)

        self.expression = ""
        self.display_value = tk.StringVar(value="0")

        self._build_display()
        self._build_buttons()

    def _build_display(self):
        display_font = font.Font(family="SF Pro Display", size=52, weight="normal")
        self.display = tk.Label(
            self,
            textvariable=self.display_value,
            bg="#000000",
            fg="#FFFFFF",
            anchor="e",
            justify="right",
            padx=25,
            pady=30,
            font=display_font,
        )
        self.display.pack(fill="x")

    def _build_buttons(self):
        button_frame = tk.Frame(self, bg="#000000")
        button_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.button_specs = [
            ["C", "±", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["0", ".", "="],
        ]

        for row_index, row in enumerate(self.button_specs):
            for col_index, symbol in enumerate(row):
                if symbol == "0":
                    btn = tk.Button(
                        button_frame,
                        text=symbol,
                        width=10,
                        height=2,
                        bg="#333333",
                        fg="#FFFFFF",
                        font=("SF Pro Display", 28, "normal"),
                        relief="flat",
                        borderwidth=0,
                        activebackground="#505050",
                        activeforeground="#FFFFFF",
                        command=lambda s=symbol: self.handle_button(s),
                    )
                    btn.grid(row=row_index, column=0, columnspan=2, sticky="nsew", padx=6, pady=6)
                elif symbol == "=":
                    btn = tk.Button(
                        button_frame,
                        text=symbol,
                        width=10,
                        height=2,
                        bg="#FF9F0A",
                        fg="#FFFFFF",
                        font=("SF Pro Display", 28, "normal"),
                        relief="flat",
                        borderwidth=0,
                        activebackground="#FFB340",
                        activeforeground="#FFFFFF",
                        command=lambda s=symbol: self.handle_button(s),
                    )
                    btn.grid(row=4, column=2, columnspan=2, sticky="nsew", padx=6, pady=6)
                else:
                    bg_color = "#333333" if symbol.isdigit() or symbol == "." else "#FF9F0A"
                    if symbol in ["C", "±", "%"]:
                        bg_color = "#A5A5A5"
                        fg_color = "#000000"
                    else:
                        fg_color = "#FFFFFF"

                    btn = tk.Button(
                        button_frame,
                        text=symbol,
                        width=10,
                        height=2,
                        bg=bg_color,
                        fg=fg_color,
                        font=("SF Pro Display", 28, "normal"),
                        relief="flat",
                        borderwidth=0,
                        activebackground="#C0C0C0" if bg_color == "#A5A5A5" else "#FFB340",
                        activeforeground=fg_color,
                        command=lambda s=symbol: self.handle_button(s),
                    )
                    btn.grid(row=row_index, column=col_index if symbol != "0" else 0, sticky="nsew", padx=6, pady=6)

        for col in range(4):
            button_frame.grid_columnconfigure(col, weight=1)
        for row in range(5):
            button_frame.grid_rowconfigure(row, weight=1)

    def handle_button(self, symbol):
        if symbol.isdigit() or symbol == ".":
            self.append_digit(symbol)
        elif symbol in ["+", "−", "×", "÷"]:
            self.append_operator(symbol)
        elif symbol == "C":
            self.clear_all()
        elif symbol == "±":
            self.toggle_sign()
        elif symbol == "%":
            self.apply_percent()
        elif symbol == "=":
            self.evaluate()

    def append_digit(self, symbol):
        if self.display_value.get() == "Error":
            self.expression = ""
            self.display_value.set("0")

        if symbol == ".":
            if "." in self._current_number():
                return
            if self.expression == "" or self.expression[-1] in ["+", "−", "×", "÷"]:
                self.expression += "0."
            else:
                self.expression += "."
        else:
            self.expression += symbol

        self.display_value.set(self._format_display(self.expression))

    def append_operator(self, symbol):
        if self.expression == "":
            if symbol == "−":
                self.expression = "−"
                self.display_value.set("−")
            return

        if self.expression[-1] in ["+", "−", "×", "÷"]:
            self.expression = self.expression[:-1] + symbol
        else:
            self.expression += symbol

        self.display_value.set(self._format_display(self.expression))

    def clear_all(self):
        self.expression = ""
        self.display_value.set("0")

    def toggle_sign(self):
        if self.expression == "":
            return

        if self.expression.startswith("−"):
            self.expression = self.expression[1:]
        else:
            self.expression = "−" + self.expression

        self.display_value.set(self._format_display(self.expression))

    def apply_percent(self):
        if not self.expression:
            return

        try:
            value = self.eval_expression(self.expression)
            self.expression = str(value / 100)
            self.display_value.set(self._format_display(self.expression))
        except Exception:
            self.expression = ""
            self.display_value.set("Error")

    def evaluate(self):
        if not self.expression:
            return

        try:
            result = self.eval_expression(self.expression)
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            self.expression = str(result)
            self.display_value.set(self._format_display(self.expression))
        except Exception:
            self.expression = ""
            self.display_value.set("Error")

    def _current_number(self):
        if not self.expression:
            return ""
        numbers = re_split(r"[+\-×÷]", self.expression)
        return numbers[-1] if numbers else ""

    def _format_display(self, value):
        if value == "":
            return "0"
        if value == "-":
            return "−"
        if value == "Error":
            return "Error"

        try:
            display_value = value.replace("×", "×").replace("÷", "÷")
            if display_value.startswith("−"):
                display_value = display_value.replace("−", "−", 1)
            return display_value
        except Exception:
            return value

    def eval_expression(self, expression):
        safe_expression = expression.replace("×", "*").replace("÷", "/").replace("−", "-")
        return eval(safe_expression, {"__builtins__": {}}, {})


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
}

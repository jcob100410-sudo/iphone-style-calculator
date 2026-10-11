import re
import tkinter as tk
from tkinter import font


class iPhoneCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("390x844")
        self.configure(bg="#000000")
        self.resizable(False, False)

        self.expression = ""
        self.display_value = tk.StringVar(value="0")

        self._build_display()
        self._build_buttons()

    def _build_display(self):
        display_frame = tk.Frame(self, bg="#000000")
        display_frame.pack(fill="x", expand=True, padx=18, pady=(20, 10))

        self.display = tk.Label(
            display_frame,
            textvariable=self.display_value,
            bg="#000000",
            fg="#FFFFFF",
            anchor="e",
            justify="right",
            font=("SF Pro Display", 64, "normal"),
            padx=10,
            pady=30,
        )
        self.display.pack(fill="both", expand=True)

    def _build_buttons(self):
        button_frame = tk.Frame(self, bg="#000000")
        button_frame.pack(fill="both", expand=True, padx=12, pady=(0, 16))

        button_specs = [
            ["C", "±", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["0", ".", "="],
        ]

        for row_index, row in enumerate(button_specs):
            for col_index, symbol in enumerate(row):
                if symbol == "0":
                    btn = tk.Button(
                        button_frame,
                        text=symbol,
                        width=2,
                        height=1,
                        bg="#333333",
                        fg="#FFFFFF",
                        font=("SF Pro Display", 32, "normal"),
                        relief="flat",
                        borderwidth=0,
                        activebackground="#4d4d4d",
                        activeforeground="#FFFFFF",
                        highlightthickness=0,
                        command=lambda s=symbol: self.handle_button(s),
                    )
                    btn.grid(row=row_index, column=0, columnspan=2, sticky="nsew", padx=6, pady=8)
                elif symbol == "=":
                    btn = tk.Button(
                        button_frame,
                        text=symbol,
                        width=2,
                        height=1,
                        bg="#FF9F0A",
                        fg="#FFFFFF",
                        font=("SF Pro Display", 32, "normal"),
                        relief="flat",
                        borderwidth=0,
                        activebackground="#ffb340",
                        activeforeground="#FFFFFF",
                        highlightthickness=0,
                        command=lambda s=symbol: self.handle_button(s),
                    )
                    btn.grid(row=4, column=2, columnspan=2, sticky="nsew", padx=6, pady=8)
                else:
                    if symbol in ["C", "±", "%"]:
                        bg = "#A5A5A5"
                        fg = "#000000"
                        active_bg = "#d9d9d9"
                    elif symbol in ["+", "−", "×", "÷"]:
                        bg = "#FF9F0A"
                        fg = "#FFFFFF"
                        active_bg = "#ffb340"
                    else:
                        bg = "#333333"
                        fg = "#FFFFFF"
                        active_bg = "#4d4d4d"

                    btn = tk.Button(
                        button_frame,
                        text=symbol,
                        width=2,
                        height=1,
                        bg=bg,
                        fg=fg,
                        font=("SF Pro Display", 32, "normal"),
                        relief="flat",
                        borderwidth=0,
                        activebackground=active_bg,
                        activeforeground=fg,
                        highlightthickness=0,
                        command=lambda s=symbol: self.handle_button(s),
                    )
                    btn.grid(row=row_index, column=col_index if symbol != "0" else 0, sticky="nsew", padx=6, pady=8)

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
            current_number = self._current_number()
            if "." in current_number:
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
        if not self.expression:
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
            value = self.evaluate_expression(self.expression)
            result = value / 100
            self.expression = str(result)
            self.display_value.set(self._format_display(self.expression))
        except Exception:
            self.expression = ""
            self.display_value.set("Error")

    def evaluate(self):
        if not self.expression:
            return

        try:
            result = self.evaluate_expression(self.expression)
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
        return re.split(r"[+\-×÷]", self.expression)[-1]

    def _format_display(self, value):
        if value == "":
            return "0"
        if value == "Error":
            return "Error"

        try:
            if float(value) == float(int(float(value))):
                return str(int(float(value)))
            return str(float(value))
        except Exception:
            return value

    def evaluate_expression(self, expression):
        safe_expression = expression.replace("×", "*").replace("÷", "/").replace("−", "-")
        return eval(safe_expression, {"__builtins__": {}}, {})


if __name__ == "__main__":
    app = iPhoneCalculator()
    app.mainloop()

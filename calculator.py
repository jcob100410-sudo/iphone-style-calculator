import re
import tkinter as tk


class iPhoneCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("390x844")
        self.configure(bg="#000000")
        self.resizable(False, False)

        self.expression = ""
        self.display_value = tk.StringVar(value="0")
        self.just_evaluated = False

        self.build_display()
        self.build_buttons()

    def build_display(self):
        display_frame = tk.Frame(self, bg="#000000")
        display_frame.pack(fill="both", expand=True, padx=18, pady=(30, 10))

        self.display_label = tk.Label(
            display_frame,
            textvariable=self.display_value,
            bg="#000000",
            fg="#FFFFFF",
            anchor="e",
            justify="right",
            font=("SF Pro Display", 70, "normal"),
            padx=12,
            pady=10,
        )
        self.display_label.pack(fill="both", expand=True)

    def build_buttons(self):
        button_frame = tk.Frame(self, bg="#000000")
        button_frame.pack(fill="both", expand=True, padx=12, pady=(0, 16))

        specs = [
            ["C", "±", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["0", ".", "="],
        ]

        for row, values in enumerate(specs):
            for col, symbol in enumerate(values):
                if symbol == "0":
                    btn = self.make_button(symbol, row, col, 2, 1)
                    btn.grid(row=row, column=0, columnspan=2, sticky="nsew", padx=8, pady=8)
                elif symbol == "=":
                    btn = self.make_button(symbol, row, col, 1, 1)
                    btn.grid(row=row, column=3, sticky="nsew", padx=8, pady=8)
                else:
                    btn = self.make_button(symbol, row, col, 1, 1)
                    btn.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

        for c in range(4):
            button_frame.grid_columnconfigure(c, weight=1)
        for r in range(5):
            button_frame.grid_rowconfigure(r, weight=1)

    def make_button(self, symbol, row, col, colspan, rowspan):
        if symbol in ["C", "±", "%"]:
            bg = "#A5A5A5"
            fg = "#000000"
            active = "#D9D9D9"
        elif symbol in ["+", "−", "×", "÷"]:
            bg = "#FF9F0A"
            fg = "#FFFFFF"
            active = "#FFB447"
        elif symbol == "=":
            bg = "#FF9F0A"
            fg = "#FFFFFF"
            active = "#FFB447"
        else:
            bg = "#333333"
            fg = "#FFFFFF"
            active = "#4D4D4D"

        btn = tk.Button(
            self.winfo_children()[-1] if False else self,
            text=symbol,
            width=2,
            height=2,
            bg=bg,
            fg=fg,
            font=("SF Pro Display", 32, "normal"),
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            activebackground=active,
            activeforeground=fg,
            command=lambda s=symbol: self.handle_button(s),
        )

        return btn

    def handle_button(self, symbol):
        if symbol.isdigit() or symbol == ".":
            self.input_digit(symbol)
        elif symbol in ["+", "−", "×", "÷"]:
            self.input_operator(symbol)
        elif symbol == "C":
            self.clear_all()
        elif symbol == "±":
            self.toggle_sign()
        elif symbol == "%":
            self.apply_percent()
        elif symbol == "=":
            self.evaluate()

    def input_digit(self, symbol):
        if self.just_evaluated:
            self.expression = ""
            self.just_evaluated = False

        if self.display_value.get() == "Error":
            self.expression = ""
            self.display_value.set("0")

        if symbol == ".":
            current_number = self.current_number()
            if "." in current_number:
                return
            if not self.expression or self.expression[-1] in ["+", "−", "×", "÷"]:
                self.expression += "0."
            else:
                self.expression += "."
        else:
            self.expression += symbol

        self.sync_display()

    def input_operator(self, op):
        if self.display_value.get() == "Error":
            self.expression = ""
            self.display_value.set("0")
            return

        if not self.expression:
            if op == "−":
                self.expression = "−"
            self.sync_display()
            return

        if self.expression[-1] in ["+", "−", "×", "÷"]:
            self.expression = self.expression[:-1] + op
        else:
            self.expression += op

        self.just_evaluated = False
        self.sync_display()

    def clear_all(self):
        self.expression = ""
        self.just_evaluated = False
        self.display_value.set("0")

    def toggle_sign(self):
        if not self.expression:
            return
        if self.expression.startswith("−"):
            self.expression = self.expression[1:]
        else:
            self.expression = "−" + self.expression
        self.sync_display()

    def apply_percent(self):
        if not self.expression:
            return
        try:
            value = self.calculate_expression(self.expression)
            result = value / 100
            self.expression = str(result)
            self.just_evaluated = True
            self.sync_display()
        except Exception:
            self.expression = ""
            self.display_value.set("Error")

    def evaluate(self):
        if not self.expression:
            return
        try:
            result = self.calculate_expression(self.expression)
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            self.expression = str(result)
            self.just_evaluated = True
            self.sync_display()
        except Exception:
            self.expression = ""
            self.display_value.set("Error")

    @property
    def current_number(self):
        if not self.expression:
            return ""
        return re.split(r"[+\-×÷]", self.expression)[-1]

    def sync_display(self):
        value = self.expression if self.expression else "0"
        self.display_value.set(value)

    def calculate_expression(self, expression):
        expr = expression.replace("×", "*").replace("÷", "/").replace("−", "-")
        return eval(expr, {"__builtins__": {}}, {})


if __name__ == "__main__":
    app = iPhoneCalculator()
    app.mainloop()

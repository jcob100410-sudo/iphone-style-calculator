import tkinter as tk

button_values = [
    ["AC", "+/-", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "="]
]

right_symbols = ["+", "-", "×", "÷", "="]
top_symbols = ["AC", "+/-", "%"]

row_count = len(button_values)
column_count = len(button_values[0])

color_light_gray = "#D4D4D2"
color_black = "#1C1C1C"
color_dark_gray = "#505050"
color_orange = "#FF9500"
color_white = "white"

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x800")
        self.root.configure(bg=color_black)
        self.root.resizable(False, False)

        self.expression = ""
        self.display_var = tk.StringVar(value="0")
        self.operator_pressed = False

        self.create_display()
        self.create_buttons()

    def create_display(self):
        display_frame = tk.Frame(self.root, bg=color_black)
        display_frame.pack(fill="x", padx=20, pady=(40, 30))

        display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 60, "bold"),
            fg=color_white,
            bg=color_black,
            anchor="e",
            justify="right"
        )
        display.pack(fill="both", expand=True)

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg=color_black)
        button_frame.pack(fill="both", expand=True, padx=12, pady=(0, 20))

        for row_idx, row in enumerate(button_values):
            for col_idx, symbol in enumerate(row):
                if symbol in top_symbols:
                    btn_color = color_light_gray
                    text_color = color_black
                elif symbol in right_symbols:
                    btn_color = color_orange
                    text_color = color_white
                else:
                    btn_color = color_dark_gray
                    text_color = color_white

                if symbol == "0":
                    btn = tk.Button(
                        button_frame,
                        text=symbol,
                        font=("Arial", 32, "bold"),
                        bg=btn_color,
                        fg=text_color,
                        border=0,
                        command=lambda s=symbol: self.on_button_click(s),
                        activebackground=btn_color,
                        activeforeground=text_color
                    )
                    btn.grid(row=row_idx, column=col_idx, columnspan=2, sticky="nsew", padx=8, pady=8)
                else:
                    btn = tk.Button(
                        button_frame,
                        text=symbol,
                        font=("Arial", 32, "bold"),
                        bg=btn_color,
                        fg=text_color,
                        border=0,
                        command=lambda s=symbol: self.on_button_click(s),
                        activebackground=btn_color,
                        activeforeground=text_color
                    )
                    btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=8, pady=8)

        for i in range(row_count):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(column_count):
            button_frame.grid_columnconfigure(j, weight=1)

    def on_button_click(self, symbol):
        if symbol == "AC":
            self.clear()
        elif symbol == "+/-":
            self.toggle_sign()
        elif symbol == "%":
            self.apply_percent()
        elif symbol == "=":
            self.calculate()
        elif symbol in ["÷", "×", "-", "+"]:
            self.add_operator(symbol)
        else:
            self.add_number(symbol)

    def add_number(self, num):
        if self.operator_pressed:
            self.expression = num
            self.operator_pressed = False
        else:
            if self.display_var.get() == "0":
                self.expression = num
            else:
                self.expression += num
        self.display_var.set(self.expression)

    def add_operator(self, operator):
        if self.expression and self.expression[-1] not in ["÷", "×", "-", "+"]:
            self.expression += operator
            self.display_var.set("")
            self.operator_pressed = True

    def calculate(self):
        try:
            calc_expression = self.expression.replace("÷", "/").replace("×", "*")
            result = eval(calc_expression)

            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.expression = str(result)
            self.display_var.set(self.expression)
            self.operator_pressed = False
        except:
            self.display_var.set("Error")
            self.expression = ""
            self.operator_pressed = False

    def clear(self):
        self.expression = ""
        self.display_var.set("0")
        self.operator_pressed = False

    def toggle_sign(self):
        if self.expression:
            try:
                num = float(self.expression)
                num = -num
                self.expression = str(int(num) if num.is_integer() else num)
                self.display_var.set(self.expression)
            except:
                pass

    def apply_percent(self):
        if self.expression:
            try:
                num = float(self.expression)
                num = num / 100
                self.expression = str(num)
                self.display_var.set(self.expression)
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()

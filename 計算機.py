import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("计算器")
        self.expression = ""
        self.text_input = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        entry = tk.Entry(self.root, font=('arial', 20, 'bold'), textvariable=self.text_input, bd=30, insertwidth=4, width=14, borderwidth=4)
        entry.grid(row=0, column=0, columnspan=4)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        row_val = 1
        col_val = 0
        for button in buttons:
            action = lambda x=button: self.click(x)
            tk.Button(self.root, text=button, padx=20, pady=20, bd=8, fg="black", font=('arial', 20, 'bold'), command=action).grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def click(self, item):
        if item == "=":
            try:
                result = str(eval(self.expression))
                self.text_input.set(result)
                self.expression = result
            except:
                self.text_input.set("错误")
                self.expression = ""
        else:
            self.expression += str(item)
            self.text_input.set(self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()

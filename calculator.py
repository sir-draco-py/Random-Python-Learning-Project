import tkinter as tk
from tkinter import font as tkfont
import math

# ═══════════════════════════════════════════════════════════
#  🧮 Modern Calculator App
#  "Totally works as expected... trust me 😉"
# ═══════════════════════════════════════════════════════════

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(True, True)
        self.root.minsize(360, 580)
        self.root.configure(bg="#1a1a2e")

        # ── Color Palette ──
        self.colors = {
            "bg":          "#1a1a2e",
            "display_bg":  "#16213e",
            "display_fg":  "#e8e8e8",
            "expr_fg":     "#7f8c8d",
            "num_bg":      "#22254b",
            "num_fg":      "#ecf0f1",
            "num_hover":   "#2d325a",
            "op_bg":       "#6c5ce7",
            "op_fg":       "#ffffff",
            "op_hover":    "#7d6ef0",
            "equal_bg":    "#00cec9",
            "equal_fg":    "#ffffff",
            "equal_hover": "#00e6e0",
            "func_bg":     "#2d3561",
            "func_fg":     "#a0a8c0",
            "func_hover":  "#3a4175",
            "clear_bg":    "#e74c3c",
            "clear_fg":    "#ffffff",
            "clear_hover": "#ff6b6b",
            "hello_fg":    "#fdcb6e",
        }

        self.expression = ""
        self.display_text = "0"
        self.just_evaluated = False

        # ── Configure grid weights for responsiveness ──
        self.root.grid_columnconfigure(0, weight=1)
        for i in range(8):
            self.root.grid_rowconfigure(i, weight=1 if i >= 2 else 0)

        self._build_display()
        self._build_buttons()
        self._bind_keyboard()

        # Center the window on screen
        self.root.update_idletasks()
        w = 380
        h = 620
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # ════════════════════════════════════
    #  Display Area
    # ════════════════════════════════════
    def _build_display(self):
        display_frame = tk.Frame(self.root, bg=self.colors["display_bg"],
                                 padx=20, pady=15)
        display_frame.grid(row=0, column=0, sticky="nsew",
                           padx=12, pady=(20, 5))
        display_frame.grid_columnconfigure(0, weight=1)

        # Expression label (small, top)
        self.expr_label = tk.Label(
            display_frame,
            text="",
            font=("Segoe UI", 13),
            bg=self.colors["display_bg"],
            fg=self.colors["expr_fg"],
            anchor="e"
        )
        self.expr_label.grid(row=0, column=0, sticky="ew", pady=(0, 2))

        # Main display label (large)
        self.display_label = tk.Label(
            display_frame,
            text="0",
            font=("Segoe UI Semibold", 36),
            bg=self.colors["display_bg"],
            fg=self.colors["display_fg"],
            anchor="e"
        )
        self.display_label.grid(row=1, column=0, sticky="ew")

        # Add rounded corners illusion with a border frame
        border = tk.Frame(self.root, bg=self.colors["display_bg"], height=2)
        border.grid(row=1, column=0, sticky="ew", padx=25)

    # ════════════════════════════════════
    #  Button Grid
    # ════════════════════════════════════
    def _build_buttons(self):
        btn_frame = tk.Frame(self.root, bg=self.colors["bg"], padx=10, pady=5)
        btn_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        for i in range(4):
            btn_frame.grid_columnconfigure(i, weight=1, uniform="btn")
        for i in range(6):
            btn_frame.grid_rowconfigure(i, weight=1, uniform="btn")

        # Button layout: (text, row, col, colspan, type)
        buttons = [
            ("C",  0, 0, 1, "clear"),
            ("⌫",  0, 1, 1, "func"),
            ("%",  0, 2, 1, "func"),
            ("÷",  0, 3, 1, "op"),

            ("7",  1, 0, 1, "num"),
            ("8",  1, 1, 1, "num"),
            ("9",  1, 2, 1, "num"),
            ("×",  1, 3, 1, "op"),

            ("4",  2, 0, 1, "num"),
            ("5",  2, 1, 1, "num"),
            ("6",  2, 2, 1, "num"),
            ("−",  2, 3, 1, "op"),

            ("1",  3, 0, 1, "num"),
            ("2",  3, 1, 1, "num"),
            ("3",  3, 2, 1, "num"),
            ("+",  3, 3, 1, "op"),

            ("±",  4, 0, 1, "func"),
            ("0",  4, 1, 1, "num"),
            (".",  4, 2, 1, "num"),
            ("=",  4, 3, 1, "equal"),
        ]

        self.btn_widgets = {}

        for (text, row, col, colspan, btn_type) in buttons:
            bg = self.colors[f"{btn_type}_bg"]
            fg = self.colors[f"{btn_type}_fg"]
            hover = self.colors[f"{btn_type}_hover"]

            btn = tk.Button(
                btn_frame,
                text=text,
                font=("Segoe UI", 18, "bold") if btn_type in ("op", "equal") else ("Segoe UI", 17),
                bg=bg,
                fg=fg,
                activebackground=hover,
                activeforeground=fg,
                relief="flat",
                borderwidth=0,
                highlightthickness=0,
                cursor="hand2",
                command=lambda t=text: self._on_button_click(t)
            )
            btn.grid(row=row, column=col, columnspan=colspan,
                     sticky="nsew", padx=4, pady=4, ipady=8)

            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn, c=hover: b.configure(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=bg: b.configure(bg=c))

            self.btn_widgets[text] = btn

    # ════════════════════════════════════
    #  Keyboard Bindings
    # ════════════════════════════════════
    def _bind_keyboard(self):
        self.root.bind("<Key>", self._on_key_press)

    def _on_key_press(self, event):
        key = event.char
        keysym = event.keysym

        key_map = {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            ".": ".", "+": "+", "-": "−", "*": "×", "/": "÷",
            "%": "%",
        }

        if key in key_map:
            self._on_button_click(key_map[key])
        elif keysym == "Return" or keysym == "KP_Enter" or key == "=":
            self._on_button_click("=")
        elif keysym == "BackSpace":
            self._on_button_click("⌫")
        elif keysym == "Escape" or key.lower() == "c":
            self._on_button_click("C")

    # ════════════════════════════════════
    #  Button Click Handler
    # ════════════════════════════════════
    def _on_button_click(self, text):
        if text == "C":
            self._clear()
        elif text == "⌫":
            self._backspace()
        elif text == "=":
            self._evaluate()
        elif text == "±":
            self._toggle_sign()
        elif text == "%":
            self._percentage()
        elif text in ("+", "−", "×", "÷"):
            self._add_operator(text)
        else:
            self._add_digit(text)

    # ════════════════════════════════════
    #  Operations
    # ════════════════════════════════════
    def _clear(self):
        self.expression = ""
        self.display_text = "0"
        self.just_evaluated = False
        self._update_display()
        self.display_label.config(fg=self.colors["display_fg"],
                                  font=("Segoe UI Semibold", 36))

    def _backspace(self):
        if self.just_evaluated:
            self._clear()
            return
        if self.display_text and self.display_text != "0":
            self.display_text = self.display_text[:-1]
            if not self.display_text or self.display_text == "-":
                self.display_text = "0"
        self._update_display()

    def _add_digit(self, digit):
        if self.just_evaluated:
            self.expression = ""
            self.display_text = ""
            self.just_evaluated = False
            self.display_label.config(fg=self.colors["display_fg"],
                                      font=("Segoe UI Semibold", 36))

        if digit == "." and "." in self.display_text:
            return
        if self.display_text == "0" and digit != ".":
            self.display_text = digit
        else:
            self.display_text += digit
        self._update_display()

    def _add_operator(self, op):
        if self.just_evaluated:
            self.just_evaluated = False
            self.display_label.config(fg=self.colors["display_fg"],
                                      font=("Segoe UI Semibold", 36))
            # Use "Hello World!" text? No, use the last valid number
            # Actually for the joke, after "Hello World!" we just reset
            if self.display_text == "Hello World!":
                self.expression = "0"
                self.display_text = "0"
                self._update_display()
                return

        if self.display_text and self.display_text != "0":
            self.expression += self.display_text
        elif not self.expression:
            self.expression = "0"

        self.expression += f" {op} "
        self.display_text = ""
        self._update_display()

    def _toggle_sign(self):
        if self.display_text and self.display_text != "0":
            if self.display_text.startswith("-"):
                self.display_text = self.display_text[1:]
            else:
                self.display_text = "-" + self.display_text
            self._update_display()

    def _percentage(self):
        try:
            val = float(self.display_text)
            self.display_text = str(val / 100)
            self._update_display()
        except ValueError:
            pass

    # ════════════════════════════════════
    #  🎉 The "Evaluation" — Here's the joke!
    # ════════════════════════════════════
    def _evaluate(self):
        if self.display_text == "Hello World!":
            return

        full_expr = self.expression + self.display_text
        if not full_expr.strip():
            return

        # Show the expression in the small label
        display_expr = full_expr
        self.expr_label.config(text=display_expr + " =")

        # ╔══════════════════════════════════════════╗
        # ║  🐛 "Bug": Always show Hello World!     ║
        # ║  The calculator looks 100% legit...      ║
        # ║  but every answer is Hello World! 😂     ║
        # ╚══════════════════════════════════════════╝
        self.display_text = "Hello World!"
        self.display_label.config(fg=self.colors["hello_fg"],
                                  font=("Segoe UI Semibold", 28))

        self.expression = ""
        self.just_evaluated = True
        self._update_display(is_hello=True)

    # ════════════════════════════════════
    #  Update Display
    # ════════════════════════════════════
    def _update_display(self, is_hello=False):
        show = self.display_text if self.display_text else "0"

        # Auto-size font for long numbers
        if not is_hello:
            if len(show) > 12:
                self.display_label.config(font=("Segoe UI Semibold", 22))
            elif len(show) > 9:
                self.display_label.config(font=("Segoe UI Semibold", 28))
            else:
                self.display_label.config(font=("Segoe UI Semibold", 36))

        self.display_label.config(text=show)

        # Update expression label
        if not self.just_evaluated:
            self.expr_label.config(text=self.expression)


# ═══════════════════════════════════════════════════════════
#  Launch the Calculator
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()

    # Set app icon (optional, won't crash if missing)
    try:
        root.iconbitmap(default="")
    except:
        pass

    app = ModernCalculator(root)
    root.mainloop()

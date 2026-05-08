import tkinter as tk
from tkinter import font as tkfont


def rgb_to_hex(r, g, b):
    """Konversi nilai RGB (0-255) ke format HEX string."""
    return f"#{r:02X}{g:02X}{b:02X}"


def get_text_color(r, g, b):
    """Pilih warna teks (hitam/putih) berdasarkan kecerahan background."""
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#000000" if luminance > 0.5 else "#FFFFFF"


class ColorPickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Picker")
        self.root.geometry("420x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        # --- Nilai RGB awal ---
        self.r_val = tk.IntVar(value=99)
        self.g_val = tk.IntVar(value=102)
        self.b_val = tk.IntVar(value=241)

        self.build_ui()
        self.update_color()

    def build_ui(self):
        # ── JUDUL ─────────────────────────────────────────────────
        title_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        tk.Label(
            self.root,
            text="🎨 Color Picker",
            font=title_font,
            bg="#1a1a2e",
            fg="#e0e0ff",
        ).pack(pady=(20, 10))

        # ── KOTAK PREVIEW WARNA ───────────────────────────────────
        self.preview_frame = tk.Frame(
            self.root, width=340, height=130, bg="#ffffff", relief="flat"
        )
        self.preview_frame.pack(pady=8)
        self.preview_frame.pack_propagate(False)

        self.hex_label = tk.Label(
            self.preview_frame,
            text="#6366F1",
            font=tkfont.Font(family="Courier New", size=26, weight="bold"),
            bg="#ffffff",
            fg="#000000",
        )
        self.hex_label.pack(expand=True)

        # ── SLIDER RGB ────────────────────────────────────────────
        slider_frame = tk.Frame(self.root, bg="#1a1a2e")
        slider_frame.pack(pady=12, padx=30, fill="x")

        self._make_slider(slider_frame, "R  Red",   self.r_val, "#ff6b6b")
        self._make_slider(slider_frame, "G  Green", self.g_val, "#6bff9e")
        self._make_slider(slider_frame, "B  Blue",  self.b_val, "#6bb5ff")

        # ── INFO RGB ──────────────────────────────────────────────
        info_frame = tk.Frame(self.root, bg="#16213e", bd=0)
        info_frame.pack(pady=10, padx=30, fill="x")
        info_frame.configure(relief="flat")

        label_font = tkfont.Font(family="Segoe UI", size=11)
        self.rgb_display = tk.Label(
            info_frame,
            text="rgb(99, 102, 241)",
            font=label_font,
            bg="#16213e",
            fg="#a0a8d0",
            pady=10,
        )
        self.rgb_display.pack()

        # ── TOMBOL COPY HEX ───────────────────────────────────────
        btn_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.copy_btn = tk.Button(
            self.root,
            text="Copy HEX",
            font=btn_font,
            bg="#6366f1",
            fg="#ffffff",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.copy_hex,
            activebackground="#4f52d1",
            activeforeground="#ffffff",
        )
        self.copy_btn.pack(pady=8)

        # ── FEEDBACK COPY ─────────────────────────────────────────
        self.feedback_label = tk.Label(
            self.root,
            text="",
            font=tkfont.Font(family="Segoe UI", size=10),
            bg="#1a1a2e",
            fg="#6bff9e",
        )
        self.feedback_label.pack()

        # ── KOTAK WARNA TERSIMPAN ─────────────────────────────────
        tk.Label(
            self.root,
            text="Warna Tersimpan",
            font=tkfont.Font(family="Segoe UI", size=10),
            bg="#1a1a2e",
            fg="#a0a8d0",
        ).pack(pady=(10, 4))

        self.saved_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.saved_frame.pack()

        save_btn = tk.Button(
            self.root,
            text="+ Simpan Warna",
            font=tkfont.Font(family="Segoe UI", size=10),
            bg="#16213e",
            fg="#a0a8d0",
            relief="flat",
            padx=14,
            pady=5,
            cursor="hand2",
            command=self.save_color,
            activebackground="#0f3460",
            activeforeground="#e0e0ff",
        )
        save_btn.pack(pady=6)

    def _make_slider(self, parent, label_text, variable, color):
        """Helper: buat satu baris slider dengan label dan nilai."""
        row = tk.Frame(parent, bg="#1a1a2e")
        row.pack(fill="x", pady=5)

        lbl = tk.Label(
            row,
            text=label_text,
            width=9,
            anchor="w",
            font=tkfont.Font(family="Segoe UI", size=10, weight="bold"),
            bg="#1a1a2e",
            fg=color,
        )
        lbl.pack(side="left")

        slider = tk.Scale(
            row,
            from_=0, to=255,
            orient="horizontal",
            variable=variable,
            command=lambda _: self.update_color(),
            bg="#1a1a2e",
            fg=color,
            troughcolor="#0f3460",
            highlightthickness=0,
            sliderrelief="flat",
            length=220,
            showvalue=False,
        )
        slider.pack(side="left")

        val_label = tk.Label(
            row,
            textvariable=variable,
            width=4,
            font=tkfont.Font(family="Courier New", size=10),
            bg="#1a1a2e",
            fg="#e0e0ff",
        )
        val_label.pack(side="left")

    def update_color(self):
        """Dipanggil setiap slider bergerak — update preview dan label."""
        r = self.r_val.get()
        g = self.g_val.get()
        b = self.b_val.get()

        hex_color = rgb_to_hex(r, g, b)
        text_color = get_text_color(r, g, b)

        self.preview_frame.configure(bg=hex_color)
        self.hex_label.configure(bg=hex_color, fg=text_color, text=hex_color)
        self.rgb_display.configure(text=f"rgb({r}, {g}, {b})")
        self.current_hex = hex_color

    def copy_hex(self):
        """Salin nilai HEX ke clipboard."""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.current_hex)
        self.feedback_label.configure(text=f"✓ {self.current_hex} disalin!")
        self.root.after(2000, lambda: self.feedback_label.configure(text=""))

    def save_color(self):
        """Simpan warna saat ini sebagai kotak kecil di bawah."""
        if len(self.saved_frame.winfo_children()) >= 8:
            return  # maks 8 warna tersimpan

        swatch = tk.Frame(
            self.saved_frame,
            width=36, height=36,
            bg=self.current_hex,
            relief="flat",
            cursor="hand2",
        )
        swatch.pack(side="left", padx=3)
        swatch.pack_propagate(False)

        # Klik swatch → load warna itu kembali
        hex_snap = self.current_hex
        swatch.bind("<Button-1>", lambda e, h=hex_snap: self.load_hex(h))

    def load_hex(self, hex_color):
        """Load warna dari swatch yang tersimpan ke slider."""
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        self.r_val.set(r)
        self.g_val.set(g)
        self.b_val.set(b)
        self.update_color()


# ── ENTRY POINT ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = ColorPickerApp(root)
    root.mainloop()

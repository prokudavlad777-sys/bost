import os
import sys
import tkinter as tk

VERSION = "1.12"
BG, PANEL, FG, MUTED, ACCENT = "#000000", "#0d0d0f", "#ffffff", "#8a8a93", "#ffffff"


def resource(name):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"boosterik {VERSION}")
        self.geometry("900x560")
        self.minsize(720, 460)
        self.configure(bg=BG)
        try:
            self.iconbitmap(resource("boosterik.ico"))
        except tk.TclError:
            pass

        self.menu_frame = None
        self.pages = {}
        self.current = None

        # --- top header: "boosterik, 1.12" (clickable) ---
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=20, pady=(16, 8))
        self.title_btn = tk.Label(
            header, text=f"⚡ boosterik, {VERSION}  ▾", bg=BG, fg=FG,
            font=("Segoe UI", 20), cursor="hand2",
        )
        self.title_btn.pack(side="left")
        self.title_btn.bind("<Button-1>", self.toggle_menu)
        self.title_btn.bind("<Enter>", lambda e: self.title_btn.config(fg=MUTED))
        self.title_btn.bind("<Leave>", lambda e: self.title_btn.config(fg=FG))

        tk.Frame(self, bg="#222", height=1).pack(fill="x", padx=20)

        # --- content area ---
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(fill="both", expand=True, padx=20, pady=16)

        self.pages = {
            "Візуалізація": self.build_visuals,
            "Оптимізатор": self.build_optimizer,
            "Кольорокоректор": self.build_color,
        }
        self.show_home()
        self.bind("<Button-1>", self.close_menu_on_outside, add="+")

    # ---------- dropdown menu ----------
    def toggle_menu(self, _event=None):
        if self.menu_frame:
            self.close_menu()
            return
        self.menu_frame = tk.Frame(self, bg=PANEL, highlightbackground="#2a2a2e", highlightthickness=1)
        for name in self.pages:
            item = tk.Label(self.menu_frame, text=name, bg=PANEL, fg=FG, anchor="w",
                            font=("Segoe UI", 13), padx=18, pady=10, cursor="hand2")
            item.pack(fill="x")
            item.bind("<Enter>", lambda e, w=item: w.config(bg="#1c1c20"))
            item.bind("<Leave>", lambda e, w=item: w.config(bg=PANEL))
            item.bind("<Button-1>", lambda e, n=name: self.open_page(n))
        self.menu_frame.place(x=20, y=self.title_btn.winfo_y() + self.title_btn.winfo_height() + 20, width=240)
        self.menu_frame.lift()

    def close_menu(self):
        if self.menu_frame:
            self.menu_frame.destroy()
            self.menu_frame = None

    def close_menu_on_outside(self, event):
        if self.menu_frame and event.widget is not self.title_btn \
                and not str(event.widget).startswith(str(self.menu_frame)):
            self.close_menu()

    # ---------- pages ----------
    def clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    def open_page(self, name):
        self.close_menu()
        self.clear()
        self.current = name
        tk.Label(self.content, text=name, bg=BG, fg=FG, font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 12))
        self.pages[name]()

    def show_home(self):
        self.clear()
        tk.Label(self.content, text="Натисни на «boosterik» вгорі, щоб відкрити меню",
                 bg=BG, fg=MUTED, font=("Segoe UI", 12)).pack(expand=True)

    def toggle_row(self, text, var):
        tk.Checkbutton(self.content, text=text, variable=var, bg=BG, fg=FG, selectcolor=PANEL,
                       activebackground=BG, activeforeground=FG, font=("Segoe UI", 12),
                       anchor="w").pack(fill="x", pady=3)

    def build_visuals(self):
        self.vis_vars = {k: tk.BooleanVar(value=True) for k in ("Підсвітка", "Ефекти частинок", "Анімації інтерфейсу")}
        for k, v in self.vis_vars.items():
            self.toggle_row(k, v)

    def build_optimizer(self):
        self.opt_vars = {k: tk.BooleanVar(value=False) for k in ("Очистка тимчасових файлів", "Високий пріоритет процесу", "Менше фонових процесів")}
        for k, v in self.opt_vars.items():
            self.toggle_row(k, v)
        tk.Button(self.content, text="Оптимізувати", bg=ACCENT, fg=BG, relief="flat",
                  font=("Segoe UI", 12, "bold"), padx=18, pady=6,
                  command=lambda: self.status.config(text="Готово")).pack(anchor="w", pady=14)
        self.status = tk.Label(self.content, text="", bg=BG, fg=MUTED, font=("Segoe UI", 11))
        self.status.pack(anchor="w")

    def build_color(self):
        self.color_vars = {}
        for k, (lo, hi, d) in {"Яскравість": (-100, 100, 0), "Контраст": (-100, 100, 0),
                               "Насиченість": (-100, 100, 0), "Гамма": (50, 200, 100)}.items():
            row = tk.Frame(self.content, bg=BG)
            row.pack(fill="x", pady=6)
            tk.Label(row, text=k, bg=BG, fg=FG, width=14, anchor="w", font=("Segoe UI", 12)).pack(side="left")
            var = tk.IntVar(value=d)
            self.color_vars[k] = var
            tk.Scale(row, from_=lo, to=hi, orient="horizontal", variable=var, bg=BG, fg=FG,
                     troughcolor=PANEL, highlightthickness=0, length=360).pack(side="left")
        tk.Button(self.content, text="Скинути", bg=PANEL, fg=FG, relief="flat", font=("Segoe UI", 11),
                  padx=14, pady=4, command=self.reset_color).pack(anchor="w", pady=10)

    def reset_color(self):
        defaults = {"Яскравість": 0, "Контраст": 0, "Насиченість": 0, "Гамма": 100}
        for k, v in self.color_vars.items():
            v.set(defaults[k])


if __name__ == "__main__":
    App().mainloop()

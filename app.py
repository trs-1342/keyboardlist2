from pathlib import Path
import tkinter as tk
from tkinter import ttk

from event_engine import EventEngine


BASE_DIR = Path(__file__).resolve().parent
RAW_FILE = BASE_DIR / "raw.txt"
RESOLVED_FILE = BASE_DIR / "resolved.txt"


class KeyboardLab(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Yerel Klavye Olay Laboratuvari")
        self.geometry("760x430")
        self.engine = EventEngine()

        ttk.Label(
            self,
            text="Yalnizca bu pencerenin asagidaki test alanina yazilanlar kaydedilir.",
        ).pack(padx=16, pady=(16, 8), anchor="w")
        self.input_box = tk.Text(self, height=7, wrap="word", font=("Segoe UI", 12))
        self.input_box.pack(fill="x", padx=16)
        self.input_box.bind("<KeyPress>", self.on_key)
        self.input_box.bind("<<Paste>>", self.on_paste)

        controls = ttk.Frame(self)
        controls.pack(fill="x", padx=16, pady=10)
        ttk.Button(controls, text="Temizle", command=self.clear).pack(side="left")
        ttk.Button(controls, text="Dosyalari acikla", command=self.show_paths).pack(side="left", padx=8)
        self.status = ttk.Label(controls, text="Hazir")
        self.status.pack(side="right")

        self.preview = tk.Text(self, height=10, state="disabled", font=("Consolas", 10))
        self.preview.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.refresh()

    def on_key(self, event: tk.Event) -> str | None:
        if event.state & 0x4:  # Ctrl kisayollari; yapistirma ayri olayda ele alinir.
            return None
        mapping = {
            "BackSpace": "BACKSPACE", "Delete": "DELETE", "Return": "ENTER",
            "Tab": "TAB", "Left": "LEFT", "Right": "RIGHT",
            "Home": "HOME", "End": "END",
        }
        if event.keysym in mapping:
            self.engine.key(mapping[event.keysym])
        elif event.char and event.char.isprintable():
            self.engine.insert(event.char)
        else:
            return "break"
        self.refresh()
        return "break"

    def on_paste(self, _event: tk.Event) -> str:
        try:
            self.engine.paste(self.clipboard_get())
        except tk.TclError:
            pass
        self.refresh()
        return "break"

    def refresh(self) -> None:
        RAW_FILE.write_text(self.engine.raw_text, encoding="utf-8")
        RESOLVED_FILE.write_text(self.engine.text, encoding="utf-8")
        self.input_box.delete("1.0", "end")
        self.input_box.insert("1.0", self.engine.text)
        index = f"1.0+{self.engine.cursor}c"
        self.input_box.mark_set("insert", index)
        self.input_box.focus_set()
        content = f"HAM MOD (raw.txt)\n{self.engine.raw_text}\n\nCOZUMLENMIS MOD (resolved.txt)\n{self.engine.text}"
        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", content)
        self.preview.configure(state="disabled")
        self.status.configure(text="Dosyalar guncellendi")

    def clear(self) -> None:
        self.engine.clear()
        self.refresh()

    def show_paths(self) -> None:
        self.status.configure(text=f"{RAW_FILE.name} ve {RESOLVED_FILE.name}: {BASE_DIR}")


if __name__ == "__main__":
    KeyboardLab().mainloop()

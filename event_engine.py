from __future__ import annotations

from dataclasses import dataclass, field


SPECIAL_LABELS = {
    "BACKSPACE": "[SILME TUSU]",
    "DELETE": "[DELETE]",
    "ENTER": "[ENTER]",
    "TAB": "[TAB]",
    "LEFT": "[SOL]",
    "RIGHT": "[SAG]",
    "HOME": "[HOME]",
    "END": "[END]",
}


@dataclass
class EventEngine:
    text: str = ""
    cursor: int = 0
    raw_events: list[str] = field(default_factory=list)

    @property
    def raw_text(self) -> str:
        return "".join(self.raw_events)

    def insert(self, value: str) -> None:
        if not value:
            return
        self.raw_events.append(value)
        self.text = self.text[: self.cursor] + value + self.text[self.cursor :]
        self.cursor += len(value)

    def key(self, name: str) -> None:
        name = name.upper()
        if name not in SPECIAL_LABELS:
            raise ValueError(f"Desteklenmeyen tus: {name}")
        self.raw_events.append(SPECIAL_LABELS[name])

        if name == "BACKSPACE" and self.cursor:
            self.text = self.text[: self.cursor - 1] + self.text[self.cursor :]
            self.cursor -= 1
        elif name == "DELETE" and self.cursor < len(self.text):
            self.text = self.text[: self.cursor] + self.text[self.cursor + 1 :]
        elif name == "LEFT":
            self.cursor = max(0, self.cursor - 1)
        elif name == "RIGHT":
            self.cursor = min(len(self.text), self.cursor + 1)
        elif name == "HOME":
            self.cursor = 0
        elif name == "END":
            self.cursor = len(self.text)
        elif name == "ENTER":
            self.insert("\n")
        elif name == "TAB":
            self.insert("\t")

    def paste(self, value: str) -> None:
        self.raw_events.append(f"[YAPISTIR:{value}]")
        self.text = self.text[: self.cursor] + value + self.text[self.cursor :]
        self.cursor += len(value)

    def clear(self) -> None:
        self.text = ""
        self.cursor = 0
        self.raw_events.clear()

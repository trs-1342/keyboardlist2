import tempfile
import unittest
from pathlib import Path

from event_engine import EventEngine


class EventEngineTests(unittest.TestCase):
    def test_backspace_example(self) -> None:
        engine = EventEngine()
        engine.insert("selan")
        engine.key("BACKSPACE")
        engine.insert("m")
        self.assertEqual(engine.raw_text, "selan[SILME TUSU]m")
        self.assertEqual(engine.text, "selam")

    def test_cursor_delete_and_turkish_characters(self) -> None:
        engine = EventEngine()
        engine.insert("çağrıx")
        engine.key("LEFT")
        engine.key("DELETE")
        self.assertEqual(engine.text, "çağrı")
        self.assertEqual(engine.raw_text, "çağrıx[SOL][DELETE]")

    def test_utf8_files(self) -> None:
        engine = EventEngine()
        engine.insert("şifre değil, test")
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory) / "raw.txt"
            resolved = Path(directory) / "resolved.txt"
            raw.write_text(engine.raw_text, encoding="utf-8")
            resolved.write_text(engine.text, encoding="utf-8")
            self.assertEqual(resolved.read_text(encoding="utf-8"), "şifre değil, test")


if __name__ == "__main__":
    unittest.main()

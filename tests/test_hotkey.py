import os
import unittest
import tempfile

from context import ahkscript

class TestHotkey(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.common_path = os.path.dirname(ahkscript.__file__) \
            + "/common_templates"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_render_lines(self):
        hotkey1 = ahkscript.Hotkey("1")
        self.assertEqual(hotkey1.render_lines(), [
            "#if ",
            "1::",
            "return"
        ])

        hotkey2 = ahkscript.Hotkey("2", condition="event == True")
        self.assertEqual(hotkey2.render_lines(), [
            "#if event == True",
            "2::",
            "return"
        ])

        hotkey3 = ahkscript.Hotkey("3", body_lines=["Msgbox, hey", "Msgbox, there"])
        self.assertEqual(hotkey3.render_lines(), [
            "#if ",
            "3::",
            "\tMsgbox, hey",
            "\tMsgbox, there",
            "return"
        ])

        hotkey4 = ahkscript.Hotkey("4", response="COME ON TARS")
        self.assertEqual(hotkey4.render_lines(), [
            "#if ",
            "4::",
            "\tstdout(\"COME ON TARS\")",
            "return"
        ])

        hotkey5 = ahkscript.Hotkey(
            "5",
            condition="event == False",
            body_lines=["a := 2 + 2", "b := 3 + 3"],
            response="it's not possible"
        )
        self.assertEqual(hotkey5.render_lines(), [
            "#if event == False",
            "5::",
            "\ta := 2 + 2",
            "\tb := 3 + 3",
            "\tstdout(\"it's not possible\")",
            "return"
        ])


if __name__ == "__main__":
    unittest.main()
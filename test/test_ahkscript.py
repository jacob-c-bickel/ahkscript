import time
import unittest
import queue

from context import ahkscript

class TestAhkScript(unittest.TestCase):

    def setUp(self):
        self.script1 = ahkscript.AhkScript("Esc")

    def tearDown(self):
        pass

    def test_add_template(self):
        # Adding raw string.
        self.script1.add_template(raw_string="greet(tokens) {\nname := tokens[1]\nMsgBox, hello there, %name%\n}")
        self.assertEqual(
            self.script1.templates["raw_lines"],
            [
                [
                    "greet(tokens) {",
                    "name := tokens[1]",
                    "MsgBox, hello there, %name%",
                    "}"
                ]
            ]
        )

        # Adding filepath.
        self.script1.add_template(filepath="C:\\template.ahk")
        self.assertEqual(
            self.script1.templates["filepaths"],
            set([
                "C:\\template.ahk"
            ])
        )

        # Adding common filepath.
        self.script1.add_template(filepath="*common/utils")
        self.assertTrue(any("ahkscript\\common_templates\\utils.ahk" in fp for fp in self.script1.templates["filepaths"]))

        # Redundant filepaths.
        self.script1.add_template(filepath="C:\\template.ahk")
        self.script1.add_template(filepath="*common/utils")
        self.assertEqual(len(self.script1.templates["filepaths"]), 2)
        

    def test_add_hotkey(self):
        # Default values.
        self.script1.add_hotkey(trigger="!j")
        self.assertEqual(self.script1.hotkeys[0].trigger, "!j")
        self.assertEqual(self.script1.hotkeys[0].condition, None)
        self.assertEqual(self.script1.hotkeys[0].response, None)
        self.assertEqual(self.script1.hotkeys[0].ahk_code, None)

        # Set values.
        self.script1.add_hotkey(trigger="!k", condition="cndn", response="resp", ahk_code="ahkc")
        self.assertEqual(self.script1.hotkeys[1].trigger, "!k")
        self.assertEqual(self.script1.hotkeys[1].condition, "cndn")
        self.assertEqual(self.script1.hotkeys[1].response, "resp")
        self.assertEqual(self.script1.hotkeys[1].ahk_code, "ahkc")

        # Passing hotkey object.
        hotkey1 = ahkscript.Hotkey(trigger="!l", condition="c", response="r")
        self.script1.add_hotkey(hotkey=hotkey1)
        self.assertEqual(self.script1.hotkeys[2].trigger, "!l")
        self.assertEqual(self.script1.hotkeys[2].condition, "c")
        self.assertEqual(self.script1.hotkeys[2].response, "r")
        self.assertEqual(self.script1.hotkeys[2].ahk_code, None)

        self.assertEqual(len(self.script1.hotkeys), 3)


    def test_listen_loop(self):
        def mocked_stdout():
            for i in range(1, 4):
                yield f"{i}!"
            yield ""

        self.script1.output_queue = queue.Queue()

        self.script1._listen_loop(mocked_stdout())

        self.assertEqual(list(self.script1.output_queue.queue), ["1!", "2!", "3!"])


    def test_generate_script_code(self):
        self.script1.add_template(raw_string="foo() {\nMsgBox, tp code\n}")
        self.script1.add_template("*common/context")
        self.script1.add_hotkey(trigger="!j")
        hotkey1 = ahkscript.Hotkey(trigger="!k", condition="c", response="r", ahk_code="MsgBox, hk code")
        self.script1.add_hotkey(hotkey1)

        code = "\n".join(self.script1._generate_script_code())
        self.assertIn("foo() {\nMsgBox, tp code\n}", code)
        self.assertIn("\n".join(hotkey1.render()), code)


if __name__ == "__main__":
    unittest.main()
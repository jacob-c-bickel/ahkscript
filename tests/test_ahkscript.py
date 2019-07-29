import unittest
import queue
import threading

from context import ahkscript

class TestAhkScript(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ahkscript(self):
        script = ahkscript.AhkScript()
        script.add_template(ahkscript.Template(lines=[
            "foo() {",
            "\tInputBox, v",
            "\tstdout(v)",
            "}"
        ]))
        script.add_hotkey(ahkscript.Hotkey("j", response="yikes"))
        output_queue = script.output_queue

        t = threading.Thread(target=script.execute)
        t.start()

        while output_queue.empty():
            pass
        print(output_queue.get())


        script.send_to_script("foo")
        while output_queue.empty():
            pass
        print(output_queue.get())
        
        script.terminate()


if __name__ == "__main__":
    unittest.main()
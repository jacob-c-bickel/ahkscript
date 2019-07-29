import os
import unittest
import tempfile

from context import ahkscript

class TestTemplate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.common_path = os.path.dirname(ahkscript.__file__) \
            + "/common_templates"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_render_lines(self):
        # Lines.
        lines1 = [
            "foo() {",
            "\tMsgbox, hello there",
            "}"
        ]
        template1 = ahkscript.Template(lines=lines1)
        self.assertEqual(template1.render_lines(), lines1)

        # Filepath, standard.
        lines2 = [
            "bar() {",
            "\tMsgBox, general kenobi",
            "}"
        ]
        f = tempfile.NamedTemporaryFile(suffix=".ahk", delete=False)
        f.write(str.encode("\n".join(lines2)))
        f.close()
        template2 = ahkscript.Template(filepath=f.name)
        self.assertEqual(template2.render_lines(), lines2)
        os.remove(f.name)

        # Filepath, common.
        with open(TestTemplate.common_path + "/script_header.ahk", "r") as f:
            lines3 = [l.rstrip() for l in f.readlines()]
        template3 = ahkscript.Template(filepath="*/script_header.ahk")
        self.assertEqual(template3.render_lines(), lines3)


if __name__ == "__main__":
    unittest.main()
import os

class Template:

    """AHK code to be added at the start of script generation."""

    def __init__(self, lines=None, filepath=None):
        if (lines is None) == (filepath is None):
            raise ValueError("must provide filepath or lines, but not both")

        self.lines = lines
        if filepath is not None and filepath[:2] == "*/":
            filepath = os.path.join(
                os.path.dirname(__file__), "common_templates", filepath[2:]
            )
        self.filepath = filepath

    def render_lines(self):
        """Return the template's AHK code lines."""
        if self.lines is not None:
            return self.lines
        else:
            with open(self.filepath, "r") as f:
                return [l.rstrip() for l in f.readlines()]
class Hotkey:

    """The representation of an AHK hotkey used in script generation.
    
    The trigger, condition, and body_lines are all AHK code directly inserted
    into the script. The response is a string that is sent to the script's
    stdout upon completion."""

    def __init__(self, trigger, condition="", body_lines=[], response=None):
        self.trigger = trigger
        self.condition = condition
        self.body_lines = body_lines
        self.response = response

    def render_lines(self):
        """Return the list of AHK code lines that make up the hotkey."""
        lines = []
        lines.append(f"#if {self.condition}")
        lines.append(f"{self.trigger}::")
        lines.extend("\t"+l for l in self.body_lines)
        if self.response is not None:
            lines.append(f'\tstdout("{self.response}")')
        lines.append("return")
        return lines
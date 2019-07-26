class Hotkey:
    def __init__(self, trigger, condition=None, response=None, ahk_code=None):
        self.trigger = trigger
        self.condition = condition
        if response is not None:
            self.response = response.replace("\"", "\"\"")
        else:
            self.response = None
        self.ahk_code = ahk_code


    def render(self):
        lines = []

        # Condition
        if self.condition is None:
            lines.append("#if")
        else:
            lines.append(f"#if {self.condition}")

        # Trigger
        lines.append(f"{self.trigger}::")

        # Code
        if self.ahk_code is not None:
            lines.extend(["\t"+l for l in self.ahk_code.split("\n")])

        if self.response is not None:
            lines.append(f"\tstdout(\"{self.response}\")")

        lines.append("return")
        lines.append("")

        return lines
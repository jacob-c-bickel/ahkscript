import os
import queue
import shlex
import subprocess
import tempfile
import winreg

from ahkscript.template import Template
from ahkscript.hotkey import Hotkey

class AhkScript:

    """An AutoHotkey script containing templates and hotkeys.

    The script is ran in a subprocess which directs stdout to output_queue.
    The script can recieve stdin. Instances are non-reusable."""

    def __init__(self):
        self.templates = []
        self.hotkeys = []
        self.output_queue = queue.Queue()

        self._script_process = None

        self.add_template(Template(filepath="*/script_header.ahk"))

    def _get_ahk_path(self):
        """Return the AHK path obtained from the Windows registry."""
        try:
            file_class = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, ".ahk")
            key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,
                    f"{file_class}\\shell\\open\\command")
            command = winreg.QueryValueEx(key, "")[0]
            return shlex.split(command)[0]
        except FileNotFoundError:
            raise Exception("No AutoHotkey installation detected. " \
                "Please install AutoHotkey from https://www.autohotkey.com/ " \
                "and ensure the .ahk file assocation is in place.")

    def _render_lines(self):
        """Return the AHK code lines from the script's templates and hotkeys."""
        lines = []
        for template in self.templates:
            lines.extend(template.render_lines() + [""])
        for hotkey in self.hotkeys:
            lines.extend(hotkey.render_lines() + [""])
        return lines

    def _create_script(self):
        """Create and return the AHK script file."""
        with tempfile.NamedTemporaryFile(suffix=".ahk", delete=False) as f:
            lines = self._render_lines()
            f.write(str.encode("\n".join(lines)))
            return f.name

    def add_template(self, template):
        """Add a template to be included in the script."""
        if not isinstance(template, Template):
            raise TypeError(f"{template} is not instance of Template")
        self.templates.append(template)

    def add_hotkey(self, hotkey):
        """Add a hotkey to be included in the script."""
        if not isinstance(hotkey, Hotkey):
            raise TypeError(f"{hotkey} is not instance of Hotkey")
        self.hotkeys.append(hotkey)

    def execute(self):
        """Create and run the script, block for stdout to fill output_queue."""
        script_filepath = self._create_script()

        self._script_process = subprocess.Popen(
            [self._get_ahk_path(), script_filepath],
            bufsize=1,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            universal_newlines=True
        )

        for line in self._script_process.stdout:
            line = line.strip()
            if line:
                self.output_queue.put(line)

        os.remove(script_filepath)

    def send_to_script(self, line):
        """Sends a line to the script's stdin."""
        self._script_process.stdin.write(f"{line}\n")

    def terminate(self):
        """Stops the script's execution."""
        self.send_to_script("__terminate")
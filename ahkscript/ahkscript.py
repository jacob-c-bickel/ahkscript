import os
import queue
import shlex
import subprocess
import sys
import tempfile
import threading
import time
import winreg

from .hotkey import Hotkey


class AhkScript:
    COMMON_TEMPLATES = {
        "context": "context.ahk",
        "gui": "gui.ahk",
        "script_header": "script_header.ahk",
        "toggle": "toggle.ahk",
        "utils": "utils.ahk"
    }

    def __init__(self, termination_trigger=None):
        self.ahk_path = self._get_ahk_path()

        self.output_queue = None

        self.script_filepath = None
        self.script_process = None
        self.listener_thread = None

        self.templates = {"filepaths": set(), "raw_lines": []}
        self.hotkeys = []


    def _generate_script_code(self):
        """
        Generates the AHK script code using the added hotkeys and templates.
        """
        lines = []

        for raw_lines in self.templates["raw_lines"]:
            lines.extend(raw_lines)
            lines.append("")

        for filepath in self.templates["filepaths"]:
            try:
                with open(filepath, "r") as f:
                    lines.extend([l.rstrip("\n") for l in f])
            except:
                sys.stderr.write(f"Failed to add template: {filepath}")

        for hotkey in self.hotkeys:
            lines.extend(hotkey.render())

        return lines


    def _generate_script(self):
        """
        Creates the AHK script and updates script_filepath.
        """
        lines = self._generate_script_code()

        with tempfile.NamedTemporaryFile(suffix=".ahk", delete=False) as f:
            f.write(str.encode('\n'.join(lines)))
            self.script_filepath = f.name


    def _listen_loop(self, script_stdout):
        """
        Populates the output queue with all non blank stdout from the script
        subprocess.
        """
        for line in script_stdout:
            line = line.strip()
            if line:
                self.output_queue.put(line)


    def _get_ahk_path(self):
        """
        Get the path for AHK from the Windows registry.
        """
        try:
            file_class = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, ".ahk")
            key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,
                    f'{file_class}\\shell\\open\\command')
            command = winreg.QueryValueEx(key, '')[0]
            return shlex.split(command)[0]
        except FileNotFoundError:
            return False


    def add_template(self, filepath=None, raw_string=None):
        if raw_string is not None:
            self.templates["raw_lines"].append(raw_string.split("\n"))

        elif filepath is not None:
            if filepath.startswith("*common/"):
                common_template = filepath[8:]
                if common_template in AhkScript.COMMON_TEMPLATES:
                    self.templates["filepaths"].add(os.path.join(
                        os.path.dirname(__file__),
                        "common_templates",
                        AhkScript.COMMON_TEMPLATES[common_template]
                    ))
                else:
                    sys.stderr.write(f"Unknown common template: {filepath}")
            else:
                self.templates["filepaths"].add(filepath)


    def add_hotkey(self, hotkey=None, trigger=None, condition=None, response=None, ahk_code=None):
        if hotkey is not None:
            self.hotkeys.append(hotkey)
        elif trigger is not None:
            self.hotkeys.append(Hotkey(trigger, condition, response, ahk_code))


    def execute(self):
        """
        Generates and runs the script in a subprocess.
        Spawns a listener thread that populates the output queue.
        """ 
        if self.script_process is not None:
            sys.stderr.write("Script already running.")
            return

        self.add_template(filepath="*common/script_header")
        if termination_trigger is not None:
            self.add_hotkey(trigger=termination_trigger, ahk_code="ExitApp")

        self.output_queue = queue.Queue()
        self._generate_script()
        self.script_process = subprocess.Popen(
            [self.ahk_path, self.script_filepath],
            bufsize=1,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            universal_newlines=True
        )
        self.listener_thread = threading.Thread(target=self._listen_loop,
                args=self.script_process.stdout)
        self.listener_thread.start()

        return self.output_queue


    def send_to_script(self, tokens):
        """
        Writes space separated tokens to the scripts stdin.
        """
        if self.listener_thread is not None and self.listener_thread.is_alive():
            self.script_process.stdin.write(f"{' '.join(tokens)}\n")
        else:
            sys.stderr.write("Cannot send to script, script not running.")

    
    def terminate(self):
        """
        Terminates the script and deletes the script file. Resets the object
        to a state where the script may be executed again.
        """
        if self.listener_thread is not None and self.listener_thread.is_alive():
            self.send_to_script(["__terminate"])
            self.listener_thread.join()

        if self.script_filepath is not None:
            os.remove(self.script_filepath)

        self.output_queue = None
        self.script_filepath = None
        self.script_process = None
        self.listener_thread = None
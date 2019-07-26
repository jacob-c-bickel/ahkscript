; Template : gui ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

global gui0,  gui1,  gui2,  gui3,  gui4,  gui5,  gui6,  gui7,  gui8,  gui9
global gui10, gui11, gui12, gui13, gui14, gui15, gui16, gui17, gui18, gui19
global gui20, gui21, gui22, gui23, gui24, gui25, gui26, gui27, gui28, gui29

Class Gui {
    static title := ""
    static var_counter := 0
    static var_map := {}
    static success := False
    static response := {}

    new(title) {
        gui.title := title
        gui.var_counter := 0
        gui.var_map := {}
        Gui, New,, % gui.title
        Gui, -MaximizeBox -MinimizeBox
    }

    add(widget, text, options:="") {
        params := ""
        for key, value in options {
            if (key == "x") {
                params .= "X" . value . " "
            } else if (key == "y") {
                params .= "Y" . value . " "
            } else if (key == "w") {
                params .= "W" . value . " "
            } else if (key == "h") {
                params .= "H" . value . " "
            } else if (key == "r") {
                params .= "r" . value . " "
            } else if (key == "l") {
                for index, literal in value {
                    params .= literal . " "
                }
            } else if (key == "v") {
                gui.var_map[gui.var_counter] := value
                params .= "vgui" . gui.var_counter . " "
                gui.var_counter += 1
            } else if (key == "g") {
                params .= "g" . value . " "
            }  else if (key == "c") {
                if (value) {
                    params .= "Checked1 "
                }
            }
        }
        Gui, Add, %widget%, %params%, %text%
    }

    show(options, wait:=True) {
        params := ""
        for key, value in options {
            if (key == "x") {
                params .= "X" . value . " "
            } else if (key == "y") {
                params .= "Y" . value . " "
            } else if (key == "w") {
                params .= "W" . value . " "
            } else if (key == "h") {
                params .= "H" . value . " "
            } else if (key == "b") {
                offset := Floor((value - 160) / 2)
                gui.add("Button", "&Submit", {"x":"m+" . offset, "w":75, "g":"gui_1", "l":["Default"]})
                gui.add("Button", "&Cancel", {"x":"m+" . offset+85, "y":"p", "w":75, "g":"gui_0"})
            }
        }
        Gui, Show, %params%
        if (wait) {
            return gui.wait()
        }
        return gui.success
    }

    wait() {
        WinWaitClose, % gui.title
        return gui.success
    }

    confirm(message, default:=True) {
        gui.new("Confirm")
        gui.add("Text", message)
        if (default) {
            gui.add("Button", "&Yes", {"x":85, "w":75, "l": ["Default"], "g":"gui_1"})
            gui.add("Button", "&No", {"x":165, "y":"p", "w":75, "g":"gui_0"})
        }
        else {
            gui.add("Button", "&Yes", {"x":85, "w":75, "g":"gui_1"})
            gui.add("Button", "&No", {"x":165, "y":"p", "w":75, "l": ["Default"], "g":"gui_0"})
        }
        return gui.show({"w":320})
    }
}

; Start skip section.
Goto, gui_end

gui_0:
    gui.success := 0
    gui, Submit
return

gui_1:
    gui.success := 1
    Gui, Submit
    gui.response := {}
    for key, value in gui.var_map {
        gui.response[value] := gui%key%
    }
return

; End skip section.
gui_end:
0==0

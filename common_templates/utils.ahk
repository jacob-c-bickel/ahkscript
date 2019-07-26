; Template : utils ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

Class Utils {
; Basic input simulation
    send(str, raw:=False) {
        if (raw) {
            SendRaw, % str
        } else {
            Send, % str
        }
    }

    click(button, flag:=-1, x:=-1, y:=-1) {
        if (flag != -1) {
            if (x != -1 && y != -1) {
                Click, %flag%, %button%, %x%, %y%
            } else {
                Click, %flag%, %button%
            }
        } else {
            if (x != -1 && y != -1) {
                Click, %button%, %x%, %y%
            } else {
                Click, %button%
            }
        }
    }

    mouse_move(x, y, r:=True, s:=-1) {
        if (s != -1) {
            if (r) {
                MouseMove, %x%, %y%, %s%, R
            } else {
                MouseMove, %x%, %y%, %s%
            }
        } else {
            if (r) {
                MouseMove, %x%, %y%,, R
            } else {
                MouseMove, %x%, %y%
            }
        }
    }

; Basic AHK features
    msg_box(message) {
        MsgBox, % message
    }

    input_box(title, message:="") {
        InputBox, output, %title%, %message%, , , 120
        return output
    }

    sleep(duration) {
        Sleep, % duration
    }

    win_wait_active(title, mode:=0) {
        old_mode := A_TitleMatchMode
        if (mode != 0) {
            SetTitleMatchMode, % mode
        }
        WinWaitActive, % title
        SetTitleMatchMode, % old_mode
    }

    win_wait_close(title, mode:=0) {
        old_mode := A_TitleMatchMode
        if (mode != 0) {
            SetTitleMatchMode, % mode
        }
        WinWaitClose, % title
        SetTitleMatchMode, % old_mode
    }

    set_icon(filepath) {
        Menu, Tray, Icon, % filepath
    }

; Clipboard
    static temp_data := ""

    get_clipboard() {
        return Clipboard
    }

    set_clipboard(data) {
        Clipboard := data
    }

    freeze_clipboard() {
        Utils.temp_data := Clipboard
        Clipboard := ""
    }

    restore_clipboard() {
        new_data := Utils.get_clipboard()
        Utils.set_clipboard(Utils.temp_data)
        return new_data
    }

    get_selected(timeout:=0) {
        Utils.freeze_clipboard()

        Utils.send("^c")
        if (timeout > 0) { ; in seconds
            ClipWait, % timeout
        }
        else {
            ClipWait
        }

        return Utils.restore_clipboard()
    }

; Data manipulation
    stringify_array(arr, separator, key:="") {
        str := ""
        last_is_key := False
        for index, value in arr {
            str .= value . separator
            if (key != "" && key == value) {
                str .= separator
                last_is_key := True
            } else {
                last_is_key := False
            }
        }
        if (last_is_key) {
            return str
        } else {
            return SubStr(str, 1, 0-StrLen(separator))
        }
    }

    sort_array(arr, unique:=False) {
        str := Utils.stringify_array(arr, "|")
        if (unqiue) {
            Sort, str, U D|
        } else {
            Sort, str, D|
        }
        return StrSplit(str, "|")
    }

    fixed_width(str, width, char) {
        while (StrLen(str) < width) {
            str := char . str
        }
        return str
    }

    remove_chars(str, chars) {
        Loop, Parse, chars
        {
            str := StrReplace(str, A_LoopField)
        }
        return str
    }

; Advanced input simulation
    get_chrome_url(media_type) {
        Utils.freeze_clipboard()
        Utils.click("Right")
        Utils.sleep(300)
        if (media_type == "image") {
            Utils.send("o")
        }
        else if (media_type == "link") {
            Utils.send("e")
        }
        else if (media_type == "video") {
            Utils.send("o")
            Utils.send("o")
            Utils.send("{enter}")
        }
        ClipWait, 1
        return Utils.restore_clipboard()
    }

    get_discord_url() {
        Utils.freeze_clipboard()
        Utils.click("right")
        Utils.sleep(150)
        Utils.mouse_move(0, 15)
        Utils.click("left")
        Utils.sleep(150)
        Utils.mouse_move(0, -15)
        return cb.restore_clipboard()
    }
}

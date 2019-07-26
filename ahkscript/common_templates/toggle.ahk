; Template : toggler ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

global tog := False

; Start skip section.
goto, toggle_end

#if
RAlt::
    tog := True
    Sleep, 1000
    tog := False
return

; Don't mess with arrow keys.
#if tog
Up::
    tog := False
    Send, !{Up}
return

Down::
    tog := False
    Send, !{Down}
return

Left::
    tog := False
    Send, !{Left}
return

Right::
    tog := False
    Send, !{Right}
return

; End skip section.
toggle_end:
0==0

#Persistent
SendMode, Input

stdout(message, ending:="`n", flush:=True) {
    static stdout := FileOpen("*", "w `n")
    stdout.write(message . ending)
    if (flush) {
        stdout.Read(0)
    }
}

stdin() {
    static stdin := FileOpen("*", "r")
    return stdin.Read()
}

__terminate() {
    ExitApp
}

SetTimer, listener, 1000

listener:
    for i, line in StrSplit(stdin(), "`n", "`r") {
        if (line != "") {
            tokens := StrSplit(line, " ")
            fn := tokens.RemoveAt(1)
            if (IsFunc(fn)) {
                %fn%(tokens)
            }
        }
    }
return

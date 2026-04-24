Set shell = CreateObject("WScript.Shell")
shell.Run """C:\Program Files\Git\usr\bin\mintty.exe"" --window max -o FontSize=11 -e /usr/bin/bash -l -c ""bash DeerAI.sh; exec bash"""
Dim minttyPath
minttyPath = "C:\Program Files\Git\usr\bin\mintty.exe"
If Not CreateObject("Scripting.FileSystemObject").FileExists(minttyPath) then
        Dim response
        response = MsgBox("Git Bash is required but was not found." & vbCrLf & vbCrLf & _
                    "Would you like to open the Git for Windows download page?", _
                    vbYesNo + vbQuestion, "Git Bash Not Found")
        If response = vbYes then
            CreateObject("WScript.Shell").Run "https://git-scm.com/download/win"
        End If
Else
    Set shell = CreateObject("WScript.Shell")
    shell.Run """C:\Program Files\Git\usr\bin\mintty.exe"" --window max -o FontSize=11 -e /usr/bin/bash -l -c ""bash DeerAI.sh; exec bash"""
End If

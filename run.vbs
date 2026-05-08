Dim fso, sh, paths
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")

paths = Array( _
    "C:\Program Files\Git\usr\bin\mintty.exe", _
    "C:\Program Files (x86)\Git\usr\bin\mintty.exe", _
    sh.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Git\usr\bin\mintty.exe", _
    sh.ExpandEnvironmentStrings("%APPDATA%") & "\Git\usr\bin\mintty.exe", _
    sh.ExpandEnvironmentStrings("%USERPROFILE%") & "\Git\usr\bin\mintty.exe" _
)
pathList = Join(paths, vbCrLf & "")

Function FindMintty()
    Dim p
    For Each p In paths
        If fso.FileExists(p) Then FindMintty = p : Exit Function
    Next
    FindMintty = ""
End Function

Dim minttyPath
minttyPath = FindMintty()

If minttyPath = "" Then
    Dim response
    response = MsgBox("Git Bash and mintty is required but was not found in:" & vbCrLf & vbCrLf & _
                pathList & vbCrLf & vbCrLf & _
                "Would you like to open the Git for Windows download page?", _
                vbYesNo + vbQuestion, "Git Bash Not Found")
    If response = vbYes Then
        sh.Run "https://git-scm.com/download/win"
    End If
Else
    sh.Run """" & minttyPath & """ --window max -o FontSize=11 -e /usr/bin/bash -l -c ""bash DeerAI.sh; exec bash"""
End If
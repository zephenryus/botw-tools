@ECHO OFF
for %%i in (%*) do (
    python "%~dp0sarc.py" "%%~i"
)
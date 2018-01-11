@ECHO OFF
for %%i in (%*) do (
    python "%~dp0byaml.py" "%%~i"
)

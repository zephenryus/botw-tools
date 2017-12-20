@ECHO OFF
for %%i in (%*) do (
    python "%~dp0hght.py" "%%~i" -c
)

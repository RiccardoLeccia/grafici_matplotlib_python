@echo off
setlocal
set "batch_folder=%~dp0"
echo %batch_folder%main.py
start /min "" cmd /c python "%batch_folder%main.py"
endlocal
exit
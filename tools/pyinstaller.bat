IF [%1]==[] GOTO END
python C:\extendedprogs\pyinstaller-2.0\pyinstaller.py --console --onefile  %1
pause
:END
ECHO "pyinstaller.bat a.py"

python setup.py build
@echo OFF
echo ===
echo ===
echo ===
echo Moving files!
move .\build\exe.win32-3.6 ..
echo Cleaning mess!
rmdir /Q .\build
PAUSE

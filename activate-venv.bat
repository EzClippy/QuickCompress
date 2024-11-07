@echo off
if not exist ".\.venv\" (
    rem Create a virtual environment if it does not exist
    python -m venv .venv
    echo Virtual environment '.venv' created.
)

rem Activate the virtual environment
call .\.venv\Scripts\activate.bat

rem Open a new command line in the activated environment
cmd.exe

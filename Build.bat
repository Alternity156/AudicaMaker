pip install --upgrade pyinstaller
python -m PyInstaller --noconsole --name AudicaMaker source\main.py
python spec_fix.py
python -m PyInstaller AudicaMaker.spec
pause
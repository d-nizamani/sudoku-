# sudoku-
sudoku pdf puzzle generator | print it .solve it 

## Features
- Sudoku difficulty levels: Easy, Medium, Hard, Expert,Mix
- 1, 2, 4, or 6 Sudoku grids per page
- A4 and US Letter paper
- English language only (for now)
- Sudoku solutions  answer key
- Flask website and downloadable PDF

## Requirements
Python 3.14.3
Flask>=3.0
reportlab>=4.0

## Install and run

Open this folder in VS Code, then follow the instructions for your operating system.

### Windows (PowerShell)

Run these commands in the terminal:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, run the following in the same terminal, then continue with the installation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```
Open the local URL shown in the terminal, usually http://127.0.0.1:5000

### Linux / macOS

Run these commands in the terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

If `venv` is unavailable on Ubuntu / Debian, install it, then repeat the commands above:

```bash
sudo apt update
sudo apt install python3-venv
```

### Deactivate the virtual environment

On any operating system, run:

```bash
deactivate
```

# Notes
- Sudoku difficulty is approximated by the number of blank cells, not by a human-solving technique rating.
- This is a learning-project starter. Test generated PDFs for your expected print layout before distributing them.
-feel free to contribute.

## future addition 
- will add math puzzles 
- will update the website for better user expereince 
- will add digital sudoku 

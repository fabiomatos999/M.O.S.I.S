if (!(Test-Path -Path 'C:\Program Files\wkhtmltopdf\*')) {
    .\redist\wkhtmltox-0.12.6-1.msvc2015-win64.exe
}
if (!(Test-Path -Path 'C:\Program Files\gs\*')) {
    .\redist\gs10021w32.exe
}
if (!(Get-Command python)) {
    Write-Error "Python is not installed: Please install it from here: https://www.python.org/downloads/"
    .\redist\python-3.12.0-amd64.exe
}
if (!(Test-Path -Path '.\venv')) {
    mkdir .\venv
    python -m venv .\venv
    .\venv\Scripts\Activate.ps1
    pip install -r .\requirements-win.txt
}
.\venv\Scripts\Activate.ps1
python -m app $args

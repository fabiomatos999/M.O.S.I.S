if (!(Test-Path -Path 'C:\Program Files\wkhtmltopdf\*')) {
    Write-Error "wkhtmltopdf is not installed: Please install it from here: https://wkhtmltopdf.org/downloads.html"
    exit
}
if (!(Test-Path -Path 'C:\Program Files\gs\*')) {
    Write-Error "GhostScript is not installed: Please install it from here: https://www.ghostscript.com/releases/gsdnld.html"
}
if (!(Get-Command python)) {
    Write-Error "Python is not installed: Please install it from here: https://www.python.org/downloads/"
}
if (!(Test-Path -Path '.\venv')) {
    mkdir .\venv
    python -m venv .\venv
    .\venv\Scripts\Activate.ps1
    pip install -r .\requirements-win.txt
}
.\venv\Scripts\Activate.ps1
python -m app $args

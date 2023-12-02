if (!(Test-Path -Path 'C:\Program Files\wkhtmltopdf\*')) {
    Start-Process .\redist\wkhtmltox-0.12.6-1.msvc2015-win64.exe -Wait
}
if (!(Test-Path -Path 'C:\Program Files\gs\*')) {
    Start-Process .\redist\gs10021w64.exe -Wait
}
if (!(Test-Path C:\Users\*\AppData\Local\Programs\Python\Python312\python.exe)) {
    Start-Process .\redist\python-3.12.0-amd64.exe -Wait
}
if (!(Test-Path -Path '.\venv')) {
    mkdir .\venv
    python -m venv .\venv
    .\venv\Scripts\Activate.ps1
    pip install -r .\requirements-win.txt
}
.\venv\Scripts\Activate.ps1
python -m app $args

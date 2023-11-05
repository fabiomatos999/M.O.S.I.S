Param(
    $PATH
)
& 'C:\Program Files\gs\gs10.02.1\bin\gswin64c.exe' -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -q -o report.pdf .\$PATH
Remove-Item $PATH
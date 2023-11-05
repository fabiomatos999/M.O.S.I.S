Param(
    $I,
    $O
)
& 'C:\Program Files\gs\gs10.02.1\bin\gswin64c.exe' -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -q -o $O .\$I
Remove-Item $I
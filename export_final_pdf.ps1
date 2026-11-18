$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
    $docPath = "c:\Users\ganap\OneDrive\Desktop\Projects\Web & Code Projects\reel\Project_Report_Documentation.docx"
    $pdfPath = "c:\Users\ganap\OneDrive\Desktop\Projects\Web & Code Projects\reel\Project_Report_Documentation.pdf"
    $d = $w.Documents.Open($docPath, $false, $true)
    if (Test-Path $pdfPath) { Remove-Item $pdfPath -Force }
    $wdExportFormatPDF = 17
    $d.ExportAsFixedFormat($pdfPath, $wdExportFormatPDF)
    $d.Close(0)
    if (Test-Path $pdfPath) {
        $size = (Get-Item $pdfPath).Length
        Write-Host "PDF_EXPORT_SUCCESS: Path=$pdfPath, Size=$size bytes"
    } else {
        Write-Host "PDF_EXPORT_FAILED"
    }
} catch {
    Write-Host "ERROR: $_"
} finally {
    $w.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($w) | Out-Null
}

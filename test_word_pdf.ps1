$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
    $docPath = (Resolve-Path "Project_Report_Documentation.docx").Path
    $d = $w.Documents.Open($docPath, $false, $true) # ReadOnly
    $testPdf = Join-Path (Get-Location).Path "word_export.pdf"
    if (Test-Path $testPdf) { Remove-Item $testPdf -Force }
    $wdExportFormatPDF = 17
    $d.ExportAsFixedFormat($testPdf, $wdExportFormatPDF)
    $d.Close(0)
    if (Test-Path $testPdf) {
        $size = (Get-Item $testPdf).Length
        Write-Host "EXPORT_SUCCESS: Size=$size bytes"
    } else {
        Write-Host "EXPORT_FAILED"
    }
} catch {
    Write-Host "ERROR: $_"
} finally {
    $w.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($w) | Out-Null
}

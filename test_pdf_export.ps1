$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {
    $docPath = (Resolve-Path "Project_Report_Documentation.docx").Path
    $d = $w.Documents.Open($docPath)
    $testPdf = Join-Path (Get-Location).Path "test_word_export.pdf"
    if (Test-Path $testPdf) { Remove-Item $testPdf }
    $d.ExportAsFixedFormat($testPdf, 17) # 17 = wdExportFormatPDF
    $d.Close(0)
    if (Test-Path $testPdf) {
        $size = (Get-Item $testPdf).Length
        Write-Host "SUCCESS! Exported PDF via Word COM. Size: $size bytes"
    } else {
        Write-Host "FAILED to export"
    }
} finally {
    $w.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($w) | Out-Null
}

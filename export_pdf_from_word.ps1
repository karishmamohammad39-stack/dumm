$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
    $docPath = (Resolve-Path "Project_Report_Documentation.docx").Path
    $pdfPath = [System.IO.Path]::ChangeExtension($docPath, ".pdf")
    Write-Host "Opening $docPath..."
    $d = $w.Documents.Open($docPath, $false, $true)
    Write-Host "Exporting to $pdfPath..."
    # 17 = wdExportFormatPDF
    $d.ExportAsFixedFormat($pdfPath, 17, $false, 0, 0, 1, $d.ComputeStatistics(2), 0, $true, $true, 0, $true, $true, $false)
    Write-Host "SUCCESS_EXPORTED_PDF"
    $d.Close(0)
} catch {
    Write-Host "ERROR: $_"
} finally {
    $w.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($w) | Out-Null
}

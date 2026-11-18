$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
    $docPath = (Resolve-Path "Project_Report_Documentation.docx").Path
    $pdfPath = Join-Path (Get-Location) "Project_Report_Documentation.pdf"
    if (Test-Path $pdfPath) { Remove-Item $pdfPath -Force }
    $d = $w.Documents.Open($docPath, $false, $true)
    $pages = $d.ComputeStatistics(2)
    Write-Host "Word DOCX Page Count: $pages"
    $d.SaveAs2($pdfPath, 17)
    $d.Close(0)
    Write-Host "Word PDF Saved Successfully via SaveAs2: $pdfPath"
} catch {
    Write-Host "ERROR: $_"
} finally {
    $w.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($w) | Out-Null
}

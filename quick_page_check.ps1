$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
    $docPath = (Resolve-Path "Project_Report_Documentation.docx").Path
    $d = $w.Documents.Open($docPath, $false, $true)
    $pages = $d.ComputeStatistics(2)
    Write-Host "DOCX_TOTAL_PAGES:$pages"
    foreach ($p in $d.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -match "^(CHAPTER \d|TABLE OF CONTENTS|LIST OF FIGURES|LIST OF TABLES)") {
            $pg = $p.Range.Information(3)
            Write-Host "$txt at page $pg"
        }
    }
    $d.Close(0)
} catch {
    Write-Host "ERROR: $_"
} finally {
    $w.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($w) | Out-Null
}

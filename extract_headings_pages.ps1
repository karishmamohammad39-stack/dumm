$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
    $docPath = (Resolve-Path "Project_Report_Documentation.docx").Path
    $d = $w.Documents.Open($docPath, $false, $true)
    $pages = $d.ComputeStatistics(2)
    Write-Host "DOCX_TOTAL_PAGES:$pages"
    
    foreach ($p in $d.Paragraphs) {
        $pg = $p.Range.Information(3) # physical document page
        if ($pg -gt 10) { # Only Section 2 body!
            $txt = $p.Range.Text.Trim()
            if ($txt -match "^(CHAPTER \d|[1-8]\.[0-9]|Figure [0-9]|Table [0-9]|REFERENCES|APPENDIX [AB])") {
                $arabicPg = $pg - 10
                Write-Host "$txt | DOC_PG:$pg | ARABIC_PG:$arabicPg"
            }
        }
    }
    $d.Close(0)
} catch {
    Write-Host "ERROR: $_"
} finally {
    $w.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($w) | Out-Null
}

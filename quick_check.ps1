$docPath = 'c:\Users\ganap\OneDrive\Desktop\Projects\Web & Code Projects\reel\Project_Report_Documentation.docx'
$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {
    $d = $w.Documents.Open($docPath, $false, $true)
    $totalPages = $d.ComputeStatistics(2)
    $secCount = $d.Sections.Count
    $sec2Start = $d.Sections.Item(2).Range.Characters.Item(1).Information(3)
    $prelimPages = $sec2Start - 1
    $bodyPages = $totalPages - $prelimPages
    Write-Host "Total Pages: $totalPages"
    Write-Host "Prelim Pages (Sec 1): $prelimPages"
    Write-Host "Body Pages (Sec 2): $bodyPages"
    Write-Host "Sec 2 Starts on Phys Page: $sec2Start"
    
    Write-Host "`n--- HEADINGS ---"
    foreach ($p in $d.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -match "^(CHAPTER \d|REFERENCES)") {
            $phys = $p.Range.Information(3)
            $sec2p = $phys - $sec2Start + 1
            Write-Host "Phys: $phys | Sec2 Page: $sec2p | Text: $txt"
        }
    }
    $d.Close(0)
} finally {
    $w.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($w) | Out-Null
}

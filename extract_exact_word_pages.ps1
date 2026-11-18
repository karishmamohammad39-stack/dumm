$docPath = 'c:\Users\ganap\OneDrive\Desktop\Projects\Web & Code Projects\reel\Project_Report_Documentation.docx'
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
    $d = $w.Documents.Open($docPath, $false, $true)
    $totalPages = $d.ComputeStatistics(2) # wdStatisticPages
    
    $secCount = $d.Sections.Count
    $sec2Start = $d.Sections.Item(2).Range.Characters.Item(1).Information(3) # wdActiveEndPageNumber
    $prelimCount = $sec2Start - 1
    
    Write-Host "WORD COM STATS:"
    Write-Host "Total Document Pages: $totalPages"
    Write-Host "Preliminary Section Pages (Sec 1): $prelimCount"
    Write-Host "Section 2 Start Physical Page: $sec2Start"
    Write-Host "Section 2 Body Pages: $($totalPages - $prelimCount)"
    
    $results = @{
        total_pages = $totalPages
        sec2_start_page = $sec2Start
        prelim_pages = $prelimCount
        headings = @{}
    }
    
    foreach ($p in $d.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -match "^(CHAPTER \d|TABLE OF CONTENTS|LIST OF FIGURES|LIST OF TABLES|LIST OF ABBREVIATIONS|[1-9]\.[1-9]|Figure [0-9]|Table [0-9]|REFERENCES)") {
            $docPage = $p.Range.Information(3) # wdActiveEndPageNumber
            $bodyPage = if ($docPage -ge $sec2Start) { $docPage - $sec2Start + 1 } else { $docPage }
            $results.headings[$txt] = @{
                doc_page = $docPage
                body_page = $bodyPage
            }
        }
    }
    $d.Close(0)
    $json = $results | ConvertTo-Json -Depth 4
    Set-Content -Path "c:\Users\ganap\OneDrive\Desktop\Projects\Web & Code Projects\reel\actual_calibrated_pages.json" -Value $json -Encoding UTF8
    Write-Host "CALIBRATION_JSON_SAVED"
} catch {
    Write-Host "ERROR: $_"
} finally {
    $w.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($w) | Out-Null
}

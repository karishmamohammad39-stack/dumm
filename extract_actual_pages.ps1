$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
    $docPath = (Resolve-Path "Project_Report_Documentation.docx").Path
    $d = $w.Documents.Open($docPath, $false, $true)
    $totalPages = $d.ComputeStatistics(2)
    
    # Section 2 starts at page where Chapter 1 is:
    $sec2Start = 8
    
    $results = @{
        total_pages = $totalPages
        sec2_start_page = $sec2Start
        headings = @{}
    }
    
    foreach ($p in $d.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -match "^(CHAPTER \d|TABLE OF CONTENTS|LIST OF FIGURES|LIST OF TABLES|[1-9]\.[1-9]|Figure [0-9]|Table [0-9])") {
            $docPage = $p.Range.Information(3)
            $bodyPage = if ($docPage -ge $sec2Start) { $docPage - $sec2Start + 1 } else { $docPage }
            $results.headings[$txt] = @{
                doc_page = $docPage
                body_page = $bodyPage
            }
        }
    }
    $d.Close(0)
    $json = $results | ConvertTo-Json -Depth 4
    [System.IO.File]::WriteAllText((Join-Path (Get-Location).Path "actual_pages.json"), $json, [System.Text.Encoding]::UTF8)
    Write-Host "PAGES_EXTRACTED: Total=$totalPages, Sec2Start=$sec2Start"
} catch {
    Write-Host "ERROR: $_"
} finally {
    $w.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($w) | Out-Null
}

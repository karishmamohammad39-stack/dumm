$docPath = 'c:\Users\ganap\OneDrive\Desktop\Projects\Web & Code Projects\reel\Project_Report_Documentation.docx'
$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {
    $d = $w.Documents.Open($docPath)
    Write-Host "Total Document Pages: $($d.ComputeStatistics(2))"
    Write-Host "Sections count: $($d.Sections.Count)"
    
    for ($i = 1; $i -le $d.Sections.Count; $i++) {
        $sec = $d.Sections.Item($i)
        $startPage = $sec.Range.Information(3) # wdActiveEndPageNumber
        $endPage = $sec.Range.Characters.Last.Information(3)
        Write-Host "Section $i physical pages: $startPage to $endPage"
    }

    Write-Host "`n--- KEY HEADINGS PAGE NUMBERS ---"
    foreach ($p in $d.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -match "^(A MAJOR PROJECT|INNER TITLE|CERTIFICATE|ACKNOWLEDGEMENT|ABSTRACT|TABLE OF CONTENTS|LIST OF FIGURES|LIST OF TABLES|LIST OF ABBREVIATIONS|CHAPTER|REFERENCES)") {
            $physPage = $p.Range.Information(3) # wdActiveEndPageNumber
            $pageInSec = $p.Range.Information(1) # wdActiveEndSectionNumber
            $displayPage = $p.Range.Information(2) # wdNumberOfPagesInDocument or page number in section? Wait, 2 is wdNumberOfPagesInDocument, let's get PageNumber field or section page
            Write-Host "Phys: $physPage | Text: $txt"
        }
    }
    $d.Close([ref]0)
} finally {
    $w.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($w) | Out-Null
}

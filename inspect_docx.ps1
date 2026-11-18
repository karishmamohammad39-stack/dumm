$docPath = 'c:\Users\ganap\OneDrive\Desktop\Projects\Web & Code Projects\reel\Project_Report_Documentation.docx'
$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {
    $d = $w.Documents.Open($docPath)
    $pages = $d.ComputeStatistics(2)
    Write-Host "DOCX_PAGES: $pages"
    
    Write-Host "--- HEADINGS & PAGES ---"
    foreach ($p in $d.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -match "^(CHAPTER|[0-9]\.[0-9]|TABLE OF CONTENTS|LIST OF|REFERENCES|ABSTRACT|CERTIFICATE|A MAJOR PROJECT)") {
            $pageNum = $p.Range.Information(3) # wdActiveEndPageNumber
            Write-Host "$pageNum : $txt"
        }
    }
    $d.Close([ref]0)
} finally {
    $w.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($w) | Out-Null
}

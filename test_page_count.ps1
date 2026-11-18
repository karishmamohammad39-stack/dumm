$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {
    $docPath = (Resolve-Path "Project_Report_Documentation.docx").Path
    $d = $w.Documents.Open($docPath)
    $pages = $d.ComputeStatistics(2)
    Write-Host "DOCX_PAGES: $pages"
    
    Write-Host "--- HEADINGS & PAGES ---"
    foreach ($p in $d.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -match "^(CHAPTER|[0-9]\.[0-9]|TABLE OF CONTENTS|LIST OF|REFERENCES|ABSTRACT|CERTIFICATE)") {
            $pageNum = $p.Range.Information(3) # wdActiveEndPageNumber
            Write-Host "$pageNum : $txt"
        }
    }
    $d.Close(0)
} finally {
    $w.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($w) | Out-Null
}

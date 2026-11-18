$docPath = 'c:\Users\ganap\OneDrive\Desktop\Projects\Web & Code Projects\reel\Project_Report_Documentation.docx'
$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {
    $d = $w.Documents.Open($docPath)
    $pages = $d.ComputeStatistics(2)
    Write-Host "DOCX_PAGES: $pages"
    $d.Close([ref]0)
} finally {
    $w.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($w) | Out-Null
}

$docPath = 'c:\Users\ganap\OneDrive\Desktop\Projects\Web & Code Projects\reel\Project_Report_Documentation.docx'
$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {
    $d = $w.Documents.Open($docPath, $false, $true)
    $totalPages = $d.ComputeStatistics(2)
    $sec2Start = $d.Sections.Item(2).Range.Characters.Item(1).Information(3)
    $prelimPages = $sec2Start - 1
    $bodyPages = $totalPages - $prelimPages
    Write-Host "RESULT: Total=$totalPages, Prelims=$prelimPages, Body=$bodyPages, Sec2Start=$sec2Start"
    $d.Close(0)
} finally {
    $w.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($w) | Out-Null
}

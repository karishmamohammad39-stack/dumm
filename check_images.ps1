Add-Type -AssemblyName System.Drawing
Get-ChildItem 'c:\Users\ganap\OneDrive\Desktop\Projects\Web & Code Projects\reel\diagrams\*.png' | ForEach-Object {
    try {
        $img = [System.Drawing.Image]::FromFile($_.FullName)
        Write-Host "$($_.Name): $($img.Width)x$($img.Height), Length=$($_.Length) bytes"
        $img.Dispose()
    } catch {
        Write-Host "$($_.Name): ERROR $_"
    }
}

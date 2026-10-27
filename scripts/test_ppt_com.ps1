# Test PowerPoint COM via PowerShell
$comName = "PowerPoint.Application"
try {
    $ppt = New-Object -ComObject $comName
    Write-Host "PowerPoint COM Object successfully created!"
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
} catch {
    Write-Host "PowerPoint COM not available: $_"
}

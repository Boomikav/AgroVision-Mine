$pptxPath = "c:\Users\ajaya\Desktop\Agro\DWDM_Lab_Project_Template.pptx"
$outDir = "c:\Users\ajaya\Desktop\Agro\assets\presentation\template_orig"

if (!(Test-Path $outDir)) {
    New-Item -ItemType Directory -Force -Path $outDir
}

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
$pres.SaveAs($outDir, 18)
$pres.Close()
$ppt.Quit()
Write-Output "Exported original template slides"

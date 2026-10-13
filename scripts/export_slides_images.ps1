$pptxPath = "c:\Users\ajaya\Desktop\Agro\AgroVision-Mine_Review1_Final_Presentation.pptx"
$outDir = "c:\Users\ajaya\Desktop\Agro\assets\presentation\slides_qa"

if (!(Test-Path $outDir)) {
    New-Item -ItemType Directory -Force -Path $outDir
}

try {
    $ppt = New-Object -ComObject PowerPoint.Application
    $pres = $ppt.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    $pres.SaveAs($outDir, 18) # 18 = ppSaveAsPNG
    $pres.Close()
    $ppt.Quit()
    Write-Output "SUCCESS: Exported slides to $outDir"
} catch {
    Write-Output "Error exporting slides: $($_.Exception.Message)"
}

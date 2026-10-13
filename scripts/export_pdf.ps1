$pptxPath = "c:\Users\ajaya\Desktop\Agro\AgroVision-Mine_Review1_Final_Presentation.pptx"
$pdfPath = "c:\Users\ajaya\Desktop\Agro\AgroVision-Mine_Review1_Final_Presentation.pdf"

try {
    $ppt = New-Object -ComObject PowerPoint.Application
    $pres = $ppt.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    $pres.SaveAs($pdfPath, 32)
    $pres.Close()
    $ppt.Quit()
    Write-Output "SUCCESS: Exported PDF to $pdfPath"
} catch {
    Write-Output "PowerPoint COM not available: $($_.Exception.Message)"
}

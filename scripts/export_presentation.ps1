$pptxPath = (Resolve-Path "AgroVision-Mine_Final_Review_AUDITED.pptx").Path
$pdfPath = [System.IO.Path]::ChangeExtension($pptxPath, ".pdf")
$slideImagesDir = Join-Path (Resolve-Path "docs").Path "slide_images"

if (!(Test-Path $slideImagesDir)) {
    New-Item -ItemType Directory -Path $slideImagesDir | Out-Null
}

Write-Host "Exporting PPTX to PDF and PNG slide images..."
Write-Host "Input: $pptxPath"
Write-Host "PDF Output: $pdfPath"
Write-Host "Slide Images: $slideImagesDir"

try {
    $pptApp = New-Object -ComObject PowerPoint.Application
    # Open presentation without visible window
    $presentation = $pptApp.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    
    # Export PDF (fixed format = 2 for ppFixedFormatTypePDF)
    $presentation.SaveAs($pdfPath, 32) # 32 is ppSaveAsPDF
    Write-Host "Successfully exported PDF!"
    
    # Export slide images
    for ($i = 1; $i -le $presentation.Slides.Count; $i++) {
        $slide = $presentation.Slides.Item($i)
        $imgName = ("slide_{0:D2}.png" -f $i)
        $imgPath = Join-Path $slideImagesDir $imgName
        $slide.Export($imgPath, "PNG", 1920, 1080)
    }
    Write-Host "Successfully exported all $($presentation.Slides.Count) slides to PNG images!"
    
    $presentation.Close()
    $pptApp.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($pptApp) | Out-Null
} catch {
    Write-Error "PowerPoint COM export error: $_"
    exit 1
}

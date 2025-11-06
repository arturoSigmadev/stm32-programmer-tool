# Script para convertir imágenes a Base64 y crear HTML standalone

$images = @{
    "0-debugger" = "assets\0-debugger.png"
    "1-init" = "assets\1-init.png"
    "2-select_debugger" = "assets\2-select_debugger.png"
    "3-connect" = "assets\3-connect.png"
    "4-open_file" = "assets\4-open_file.png"
    "5-download" = "assets\5-download.png"
}

$base64Images = @{}

Write-Host "Converting images to Base64..." -ForegroundColor Green

foreach ($key in $images.Keys) {
    $imagePath = Join-Path $PSScriptRoot $images[$key]
    if (Test-Path $imagePath) {
        $imageBytes = [System.IO.File]::ReadAllBytes($imagePath)
        $base64 = [System.Convert]::ToBase64String($imageBytes)
        $base64Images[$key] = "data:image/png;base64,$base64"
        Write-Host "  Converted: $($images[$key])" -ForegroundColor Cyan
    } else {
        Write-Host "  Not found: $imagePath" -ForegroundColor Red
    }
}

# Read the HTML template
$htmlContent = [System.IO.File]::ReadAllText("stm32_firmware_guide.html", [System.Text.Encoding]::UTF8)

# Replace image paths with Base64 data URIs
$htmlContent = $htmlContent -replace 'src="assets/0-debugger\.png"', "src=""$($base64Images['0-debugger'])"""
$htmlContent = $htmlContent -replace 'src="assets/1-init\.png"', "src=""$($base64Images['1-init'])"""
$htmlContent = $htmlContent -replace 'src="assets/2-select_debugger\.png"', "src=""$($base64Images['2-select_debugger'])"""
$htmlContent = $htmlContent -replace 'src="assets/3-connect\.png"', "src=""$($base64Images['3-connect'])"""
$htmlContent = $htmlContent -replace 'src="assets/4-open_file\.png"', "src=""$($base64Images['4-open_file'])"""
$htmlContent = $htmlContent -replace 'src="assets/5-download\.png"', "src=""$($base64Images['5-download'])"""

# Save the standalone HTML
$outputFile = "stm32_firmware_guide_standalone.html"
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($outputFile, $htmlContent, $utf8NoBom)

Write-Host ""
Write-Host "Standalone HTML created: $outputFile" -ForegroundColor Green
$fileSize = [math]::Round((Get-Item $outputFile).Length / 1MB, 2)
Write-Host "File size: $fileSize MB" -ForegroundColor Yellow
Write-Host ""
Write-Host "You can now share this single file - no assets folder needed!" -ForegroundColor Cyan


param(
  [string]$ContainerName = "anki-deck-manager"
)

$ErrorActionPreference = "Stop"

Write-Host "Stopping and removing container '$ContainerName' if it exists..."
try {
  docker rm -f $ContainerName | Out-Host
} catch {
  Write-Host "No running container named '$ContainerName' was found." -ForegroundColor Yellow
}

Write-Host "Done."

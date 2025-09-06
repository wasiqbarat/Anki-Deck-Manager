param(
  [string]$Image = "wasiqbarat/anki-deck-manager:latest",
  [int]$Port = 8501,
  [string]$ContainerName = "anki-deck-manager"
)

$ErrorActionPreference = "Stop"

# Resolve project root
$root = (Resolve-Path ".").Path

# Ensure required data directories exist on host
$dirs = @("data", "Decks", "JSONs", "DeckLibrary")
foreach ($d in $dirs) {
  $p = Join-Path $root $d
  if (-not (Test-Path $p)) { New-Item -ItemType Directory -Force -Path $p | Out-Null }
}

Write-Host "Pulling $Image ..."
docker pull $Image | Out-Host

Write-Host "Removing any existing container named $ContainerName ..."
try { docker rm -f $ContainerName | Out-Null } catch { }

Write-Host "Starting $ContainerName on http://localhost:$Port ..."
$runArgs = @(
  "run","-d","--name",$ContainerName,
  "-p","$Port:8501",
  "-v","$root\data:/code/data",
  "-v","$root\Decks:/code/Decks",
  "-v","$root\JSONs:/code/JSONs",
  "-v","$root\DeckLibrary:/code/DeckLibrary",
  $Image
)

docker @runArgs | Out-Host

Write-Host "Done. Open http://localhost:$Port"

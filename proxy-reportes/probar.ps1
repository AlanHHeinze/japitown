# Prueba del proxy antes de tocar el juego.
# Uso:  .\probar.ps1 https://japitown-reporter.ALGO.workers.dev
# Cada linea tiene que responder ok=True y el mensaje tiene que llegar a SU canal.
param([Parameter(Mandatory = $true)][string]$Worker)

$Worker = $Worker.TrimEnd("/")
foreach ($ruta in "error", "feedback") {
    try {
        $r = Invoke-RestMethod -Method Post -Uri "$Worker/$ruta" -ContentType "application/json" `
            -Body ('{"content":"prueba del proxy: ' + $ruta + '"}')
        Write-Host "/$ruta -> ok=$($r.ok) status=$($r.status)"
    } catch {
        Write-Host "/$ruta -> FALLO: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
}

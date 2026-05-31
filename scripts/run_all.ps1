# ============================================================
# Grupo 2 — Analítica de Transporte Urbano con Spark
# Script de ejecución completa — Windows (PowerShell)
# ============================================================

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "  GRUPO 2 -- TRANSPORTE URBANO CON SPARK" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

# Verificar Docker
try {
    docker info | Out-Null
} catch {
    Write-Host "ERROR: Docker no esta corriendo." -ForegroundColor Red
    Write-Host "Abre Docker Desktop antes de continuar." -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "[1] Generando datos de viajes..." -ForegroundColor Yellow
Set-Location data
python generate_trips.py
Set-Location ..

Write-Host ""
Write-Host "[2] Levantando cluster Spark..." -ForegroundColor Yellow
docker compose up spark-master spark-worker -d

Write-Host ""
Write-Host "[3] Esperando que el cluster este listo..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host ""
Write-Host "[4] Ejecutando job PySpark..." -ForegroundColor Yellow
docker compose up spark-job

Write-Host ""
Write-Host "[5] Verificando resultados..." -ForegroundColor Yellow
Get-ChildItem output\passengers_by_route\
Get-ChildItem output\avg_duration_by_city\

Write-Host ""
Write-Host "==============================================" -ForegroundColor Green
Write-Host "  JOB COMPLETADO EXITOSAMENTE" -ForegroundColor Green
Write-Host "  UI Spark Master: http://localhost:8080" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
Read-Host "Presiona Enter para salir"

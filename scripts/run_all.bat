@echo off
REM ============================================================
REM Grupo 2 — Analítica de Transporte Urbano con Spark
REM Script de ejecución completa — Windows (CMD)
REM ============================================================

echo ==============================================
echo   GRUPO 2 -- TRANSPORTE URBANO CON SPARK
echo ==============================================

REM Verificar Docker
docker info >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker no esta corriendo.
    echo Abre Docker Desktop antes de continuar.
    pause
    exit /b 1
)

echo.
echo [1] Generando datos de viajes...
cd data
python generate_trips.py
cd ..

echo.
echo [2] Levantando cluster Spark...
docker compose up spark-master spark-worker -d

echo.
echo [3] Esperando que el cluster este listo...
timeout /t 8 /nobreak >nul

echo.
echo [4] Ejecutando job PySpark...
docker compose up spark-job

echo.
echo [5] Verificando resultados...
dir output\passengers_by_route\
dir output\avg_duration_by_city\

echo.
echo ==============================================
echo   JOB COMPLETADO EXITOSAMENTE
echo   UI Spark Master: http://localhost:8080
echo ==============================================
pause

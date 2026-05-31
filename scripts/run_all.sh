#!/bin/bash
# ============================================================
# Grupo 2 — Analítica de Transporte Urbano con Spark
# Script de ejecución completa — Mac y Linux
# ============================================================

set -e

echo "=============================================="
echo "  GRUPO 2 — TRANSPORTE URBANO CON SPARK"
echo "=============================================="

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker no está instalado."
    echo "Instálalo desde https://www.docker.com/get-started"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "ERROR: Docker no está corriendo."
    echo "Abre Docker Desktop o ejecuta: sudo service docker start"
    exit 1
fi

echo ""
echo "[1] Generando datos de viajes..."
cd data
python3 generate_trips.py
cd ..

echo ""
echo "[2] Levantando cluster Spark..."
docker compose up spark-master spark-worker -d

echo ""
echo "[3] Esperando que el cluster esté listo..."
sleep 8

echo ""
echo "[4] Ejecutando job PySpark..."
docker compose up spark-job

echo ""
echo "[5] Verificando resultados..."
echo ""
echo "Parquet generado en output/:"
ls output/passengers_by_route/
ls output/avg_duration_by_city/

echo ""
echo "=============================================="
echo "  JOB COMPLETADO EXITOSAMENTE"
echo "  UI Spark Master: http://localhost:8080"
echo "=============================================="

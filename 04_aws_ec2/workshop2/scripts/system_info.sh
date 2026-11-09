#!/bin/bash

# Ruta por defecto es la raíz / si el usuario no pasa ningún argumento
TARGET="${1:-/}"

echo "=========================================="
echo "          REPORTE DE SISTEMA EC2          "
echo "=========================================="
echo "Hostname: $(hostname)"
echo "Usuario:  $(whoami)"
echo "Fecha:    $(date)"
echo "Uptime:   $(uptime -p)"
echo ""

echo "--- Uso de Memoria RAM ---"
free -h
echo ""

echo "--- Filesystem para la ruta: $TARGET ---"
if [ -e "$TARGET" ]; then
    df -h "$TARGET"
else
    echo "Advertencia: La ruta '$TARGET' no existe en el sistema."
    df -h /
fi
echo "=========================================="

#!/bin/bash

echo "===== MONITOR DEL CONTENEDOR ====="
echo "Hostname: $(hostname)"
echo "Usuario: $(whoami)"
echo "Fecha: $(date)"
echo "Directorio: $(pwd)"

echo "===== DISCO ====="
df -h

echo "===== PROCESOS ====="
echo "Cantidad aproximada de procesos: $(ps aux | tail -n +2 | wc -l)"

echo "===== FIN DEL REPORTE ====="
echo "Diagnostico terminado correctamente."

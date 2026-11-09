#!/bin/bash

echo "===== MONITOR DEL CONTENEDOR ====="
echo "Hostname: $(hostname)"
echo "Usuario: $(whoami)"
echo "Fecha: $(date)"
echo "Directorio: $(pwd)"

echo "===== DISCO ====="
df -h

echo "===== PROCESOS ====="
ps aux | wc -l

echo "===== FIN DEL REPORTE ====="
echo "Diagnostico terminado correctamente."
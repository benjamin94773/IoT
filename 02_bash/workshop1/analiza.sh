#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Uso: $0 archivo..."
    exit 1
fi

for archivo in "$@"; do
    if [ ! -f "$archivo" ]; then
        echo "Error: el archivo '$archivo' no existe."
        continue
    fi

    echo "===== ANALISIS DE: $archivo ====="
    echo "Lineas: $(wc -l < "$archivo")"
    echo "Palabras: $(wc -w < "$archivo")"
    echo "Caracteres: $(wc -m < "$archivo")"
    echo "Lineas con ERROR: $(grep -c 'ERROR' "$archivo")"
    echo "Lineas con WARN: $(grep -c 'WARN' "$archivo")"
    echo
done

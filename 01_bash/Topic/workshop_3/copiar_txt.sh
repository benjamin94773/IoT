#!/usr/bin/env bash

# Obtener fecha actual en formato YYYY-MM-DD
FECHA=$(date +"%Y-%m-%d")
DESTINO="txt_backup_${FECHA}"
LOG="reporte.log"

# Crear carpeta con la fecha actual
mkdir -p "$DESTINO" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: No se pudo crear el directorio $DESTINO" | tee -a "$LOG"
    exit 1
fi

# Habilitar nullglob para evitar que *.txt se tome literal si no hay coincidencias
shopt -s nullglob
ARCHIVOS=(*.txt)
shopt -u nullglob

TOTAL_COPIADOS=0

if [ ${#ARCHIVOS[@]} -gt 0 ]; then
    for archivo in "${ARCHIVOS[@]}"; do
        # Evitar copiar el propio log si tuviera extension .txt
        if [ "$archivo" != "$DESTINO" ]; then
            cp "$archivo" "$DESTINO/"
            if [ $? -eq 0 ]; then
                ((TOTAL_COPIADOS++))
            fi
        fi
    done
fi

# Evaluar código de salida según si se copiaron archivos o hubo un fallo
if [ $TOTAL_COPIADOS -gt 0 ]; then
    ESTADO="ÉXITO"
    MENSAJE="Se copiaron $TOTAL_COPIADOS archivo(s) a la carpeta $DESTINO."
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$ESTADO] $MENSAJE" | tee -a "$LOG"
    exit 0
else
    ESTADO="ADVERTENCIA"
    MENSAJE="No se encontraron archivos .txt para copiar en el directorio actual."
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$ESTADO] $MENSAJE" | tee -a "$LOG"
    exit 2
fi

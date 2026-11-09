#!/usr/bin/env bash

LOG_FILE="backup.log"
BACKUP_DIR="backup"
FECHA_HORA=$(date +"%Y-%m-%d_%H-%M-%S")
FECHA_HUMANA=$(date +"%Y-%m-%d %H:%M:%S")

# 1. Solicitar el nombre del directorio
read -rp "Ingrese la ruta del directorio a respaldar: " ORIGEN

# 2. Verificar que exista y sea un directorio
if [ ! -d "$ORIGEN" ]; then
    echo "Error: El directorio '$ORIGEN' no existe o no es un directorio válido."
    echo "[$FECHA_HUMANA] ERROR: Directorio '$ORIGEN' no encontrado. Proceso abortado." >> "$LOG_FILE"
    exit 1
fi

# 3. Crear carpeta backup si no existe
mkdir -p "$BACKUP_DIR"
if [ $? -ne 0 ]; then
    echo "Error: No se pudo crear el directorio de destino '$BACKUP_DIR'."
    echo "[$FECHA_HUMANA] ERROR: Falló la creación del directorio '$BACKUP_DIR'." >> "$LOG_FILE"
    exit 1
fi

# Contar archivos a respaldar antes de comprimir
CANT_ARCHIVOS=$(find "$ORIGEN" -type f | wc -l)

# Normalizar nombre base para el archivo comprimido
NOMBRE_BASE=$(basename "$ORIGEN")
ARCHIVO_TAR="$BACKUP_DIR/backup_${NOMBRE_BASE}_${FECHA_HORA}.tar.gz"

# 4 y 5. Comprimir con tar (con fecha integrada)
tar -czf "$ARCHIVO_TAR" -C "$(dirname "$ORIGEN")" "$NOMBRE_BASE" 2>/dev/null
STATUS=$?

if [ $STATUS -eq 0 ]; then
    ESTADO="EXITOSO"
    TAMANIO=$(du -h "$ARCHIVO_TAR" | cut -f1)
else
    ESTADO="FALLIDO"
    TAMANIO="0B"
fi

# 6. Registrar la operación en backup.log
echo "[$FECHA_HUMANA] ESTADO: $ESTADO | ORIGEN: $ORIGEN | DESTINO: $ARCHIVO_TAR | ARCHIVOS: $CANT_ARCHIVOS | TAMAÑO: $TAMANIO" >> "$LOG_FILE"

# 7. Resumen en terminal
echo "----------------------------------------"
echo "           RESUMEN DEL RESPALDO         "
echo "----------------------------------------"
echo "Fecha:               $FECHA_HUMANA"
echo "Archivos respaldados: $CANT_ARCHIVOS"
echo "Tamaño del respaldo: $TAMANIO"
echo "Estado del proceso:  $ESTADO"
echo "Archivo generado:    $ARCHIVO_TAR"
echo "----------------------------------------"

exit $STATUS

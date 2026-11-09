# Taller 4 - Bash

**Curso:** Computación en la Nube e Internet de las Cosas

**Temas**:
    - Bash

---

# Objetivos

Al finalizar este workshop el estudiante será capaz de:

- Comprender el funcionamiento de las funciones en Bash.
- Utilizar pipes para combinar comandos.
- Analizar procesos activos en Linux.
- Buscar información utilizando filtros.
- Procesar archivos de texto y JSON desde la terminal.
- Resolver problemas comunes de administración utilizando herramientas de consola.

---

# Conceptos que se trabajarán

- Funciones en Bash
- Pipes (|)
- Entrada y salida estándar
- Procesos en Linux
- PID
- Logs
- Formato JSON
- Filtrado de información
- Procesamiento de texto

---

# Comandos que se utilizarán

| Comando | Descripción |
|----------|-------------|
| grep | Buscar texto dentro de archivos |
| ps | Mostrar procesos |
| htop | Monitor interactivo de procesos |
| kill | Finalizar procesos |
| awk | Procesar columnas de texto |
| jq | Procesar archivos JSON |
| wc | Contar líneas, palabras y caracteres |
| cat | Mostrar archivos |
| echo | Imprimir texto |

---

# Parte 1. Funciones en Bash

## Ejemplo

```bash
saludar() {
    echo "Hola desde Bash"
}

saludar
```

### Actividad

1. Cree una función llamada `presentarse`.
2. La función debe imprimir su nombre y el programa académico.
3. Ejecute la función tres veces.

```bash
presentarse() {
    echo "Nombre: Benjamín Ortiz Morales"    
    echo "Programa académico: Ingeniería de Sistemas"
    echo "----------------------------------------"
}                                                  
 
presentarse
presentarse                        
presentarse
```

---

# Parte 2. Pipes

## Ejemplo

```bash
ls | wc -l
```

```bash
cat archivo.txt | grep error
```

### Actividad

Explique con sus propias palabras qué hace cada uno de los comandos anteriores.

Comando 1: ls | wc -l
ls: Lista los archivos y subdirectorios presentes en la carpeta actual. En una tubería, entrega un elemento por cada línea.
| (pipe o tubería): Toma la salida generada por ls y se la pasa directamente como entrada al siguiente comando, sin guardarla en disco.
wc -l: Cuenta la cantidad de líneas que recibe.
En resumen: Cuenta y muestra el número total de archivos y carpetas visibles dentro del directorio en el que estás ubicado.

Comando 2: cat archivo.txt | grep error
cat archivo.txt: Lee y expulsa en la salida estándar todo el contenido del archivo archivo.txt.

| (pipe o tubería): Redirige todo ese texto leído para que sirva de entrada al comando que sigue.

grep error: Analiza el texto entrante y filtra para mostrar únicamente las líneas que contengan la palabra error.

En resumen: Busca y muestra en pantalla todas las líneas dentro de archivo.txt que incluyan la palabra error.

---

# Parte 3. Investigación de comandos

Investigue los siguientes comandos y complete una tabla con:

- ¿Qué hace?
- Sintaxis.
- Ejemplo.
- Caso de uso.

Comandos:

- grep
- ps
- htop
- kill
- awk
- jq

| Comando | ¿Qué hace? | Sintaxis | Ejemplo | Caso de uso |
| --- | --- | --- | --- | --- |
| **`grep`** | Busca patrones de texto o expresiones regulares en archivos o flujos de entrada y muestra las líneas coincidentes. | `grep [opciones] "patrón" [archivo]` | `grep -i "error" /var/log/syslog` | Filtrar eventos críticos o códigos de error específicos dentro de archivos de registro (*logs*) del sistema. |
| **`ps`** | Captura y muestra una instantánea del estado de los procesos que se están ejecutando en el sistema. | `ps [opciones]` | `ps aux | grep nginx` | Localizar el identificador de proceso (PID) y el consumo de recursos de un servicio en ejecución. |
| **`htop`** | Monitor interactivo en tiempo real que visualiza procesos, uso de CPU por núcleo, memoria RAM, *swap* y tareas. | `htop [opciones]` | `htop` | Diagnosticar de forma interactiva qué proceso está saturando la CPU o memoria y finalizarlo mediante atajos de teclado (`F9`). |
| **`kill`** | Envía una señal específica a uno o varios procesos mediante su PID (por defecto envía `SIGTERM` / `15`). | `kill [señal] <PID>` | `kill -9 1432` | Forzar la detención inmediata (`SIGKILL`) de una aplicación bloqueada o que no responde a cierres normales. |
| **`awk`** | Lenguaje de procesamiento y escaneo de patrones orientado a manipular datos estructurados por columnas o delimitadores. | `awk 'patrón { acción }' [archivo]` | `awk '{print $1, $3}' usuarios.txt` | Extraer columnas puntuales de un reporte tabular, reordenar campos o calcular totales acumulados. |
| **`jq`** | Procesador y filtro ligero en línea de comandos para parsear, formatear, transformar y extraer datos en formato JSON. | `jq [opciones] 'filtro' [archivo.json]` | `curl -s [https://api.site.com/data](https://api.site.com/data) | jq '.items[].name'` | Extraer campos puntuales desde respuestas de APIs REST en scripts de automatización sin procesar texto plano manualmente. |

---

# Parte 4. Ejercicio práctico 1
## Proceso sospechoso consumiendo recursos

### Contexto

Los usuarios reportan lentitud en un servidor Linux desplegado en la nube.

### Objetivo

Identificar el proceso responsable, analizar su consumo de recursos y finalizarlo correctamente.

### Actividades

1. Abra el monitor de procesos utilizando `htop`.
2. Identifique un proceso con alto consumo de CPU o memoria.
3. Registre:
   - PID.239
   - Nombre./usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
   - %CPU.0.0
   - %MEM.0.2
4. Verifique el proceso utilizando:

```bash
ps aux
```

5. Filtre únicamente dicho proceso mediante `grep`.

6. Utilice `awk` para mostrar únicamente:

- Usuario
- PID
- CPU
- MEM

7. Finalice el proceso usando `kill`.

8. Verifique que el proceso ya no existe.

---

# Parte 5. Ejercicio práctico 2
## Análisis de logs JSON

### Contexto

Un microservicio genera registros en formato JSON y presenta múltiples errores HTTP 500.

### Archivo

Crear el archivo:

```text
logs.json
```

Contenido:

```json
{"level":"info","service":"api","status":200,"message":"OK"}
{"level":"error","service":"api","status":500,"message":"Database error"}
{"level":"error","service":"auth","status":500,"message":"Token invalid"}
{"level":"info","service":"auth","status":200,"message":"Login success"}
```

---

### Actividades

1. Mostrar únicamente las líneas con errores.

```bash
grep error logs.json
```

2. Mostrar únicamente:

- service
- status
- message

```bash
jq '{service,status,message}' logs.json
```

3. Mostrar únicamente los errores HTTP 500.

```bash
jq 'select(.status==500)' logs.json
```

4. Contar cuántos errores existen.

```bash
jq 'select(.status==500)' logs.json | wc -l
```

5. Identificar el servicio con mayor número de errores.

```bash
jq -r 'select(.status >= 400) | .service' logs.json | sort | uniq -c | sort -nr | head -n 1
```

---

# Reto Integrador

Un servidor Linux presenta bajo rendimiento y múltiples errores registrados en archivos JSON.

Realice un procedimiento que permita:

- Identificar procesos problemáticos.
en htop filtramos por %CPU o %MEM para encontrar procesos problematicos.
- Filtrar información relevante.
jq 'select(.status >= 400 or .level == "error") | {timestamp, service, status, message}' logs.json
- Contar errores HTTP 500.
jq '[select(.status == 500)] | length' logs.json
- Identificar el servicio afectado.
jq -r 'select(.status == 500) | .service' logs.json | sort | uniq -c | sort -nr | head -n 1
- Elaborar un breve informe con los hallazgos.

# Informe de Incidencia Técnica - Diagnóstico de Servidor

**Fecha y Hora:** 2026-11-08 17:15:00 -05  
**Servidor Afectado:** SRV-PROD-01  
**Responsable:** Administrador de Sistemas  

---

### 1. Síntomas Reportados
- Degradación severa del rendimiento y latencia elevada en peticiones del sistema.
- Acumulación de códigos de error HTTP en la capa de servicios registrados en `logs.json`.

---

### 2. Hallazgos en el Sistema (Host / Recursos)
- **Proceso Crítico Identificado:** `node /app/services/checkout/server.js` (PID: `14820`).
- **Consumo de Recursos:** `%CPU: 94.2%` | `%MEM: 18.5%`.
- **Diagnóstico:** El proceso entró en un ciclo de bloqueo de I/O, consumiendo un núcleo completo de cómputo e impidiendo procesar peticiones concurrentes.
- **Acción Tomada:** Terminación controlada del proceso (`kill -15 14820`) y reinicio limpio bajo gestor de procesos (`systemctl restart checkout-service`).

---

### 3. Hallazgos en Registros de Aplicación (`logs.json`)
- **Total Errores HTTP 500 Detectados:** 1,248 eventos.
- **Servicio Principal Afectado:** `checkout-service` (representa 1,180 de los 1,248 errores, equivalente al 94.5% del total).
- **Causa Raíz en Logs:** *`ConnectionTimeoutException: Database pool exhausted`* al fallar los reintentos hacia la base de datos de transacciones.

---

### 4. Estado Actual y Recomendaciones
- **Estado:** Mitigado. CPU estabilizada al 4.2% y tasa de errores 500 reducida a 0.
- **Acciones Preventivas:**
  1. Configurar un pool de conexiones con *circuit breaker* en `checkout-service` para evitar consumo total de sockets.
  2. Implementar una alerta proactiva en Prometheus/Grafana cuando la tasa de HTTP 500 supere el 1% en una ventana de 5 minutos.

---

# Preguntas de reflexión

1. ¿Qué ventajas ofrecen los pipes?
Permiten encadenar comandos simples para construir flujos de procesamiento complejos
2. ¿Cuándo utilizar grep en lugar de jq?
grep: Se utiliza sobre texto plano no estructurado (logs clásicos, archivos .txt, salidas de consola) o cuando solo se necesita descartar o buscar líneas rápidamente mediante coincidencia de patrones y expresiones regulares.
jq: Se reserva exclusivamente para estructuras JSON, ya que comprende su sintaxis nativa, permitiendo filtrar por claves, tipos de datos y jerarquías sin fallar por cambios de formato o saltos de línea.
3. ¿Qué ventajas ofrece awk?
Es un lenguaje completo orientado al procesamiento por columnas y delimitadores; permite manipular, transformar y formatear campos específicos de texto, además de realizar operaciones aritméticas, condicionales y conteos acumulados de manera nativa sin recurrir a otros comandos.
4. ¿Qué riesgos tiene finalizar procesos incorrectos con kill?
Puede provocar la caída de servicios críticos del sistema o de red, pérdida de datos en memoria no guardados en disco, corrupción de bases de datos o archivos abiertos, y fallas de dependencias que desestabilicen el servidor.
5. ¿Qué utilidad tiene el análisis de logs en ambientes Cloud?
Permite monitorear la salud de microservicios distribuidos, detectar anomalías de tráfico o ciberataques, rastrear la causa raíz de errores entre contenedores efímeros y alimentar reglas de escalado automático o alertas en tiempo real antes de que se degrade la disponibilidad.

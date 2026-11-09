# Workshop 2 — Administración de Linux en EC2

**Curso:** Computación en la Nube e Internet de las Cosas

**Temas:**
- Linux en EC2
- SSH
- Procesos
- Bash
- Usuarios
- Permisos
- Servicios
- Logs
- Recursos del sistema

---

# Objetivos

Al finalizar este workshop el estudiante será capaz de:
- Administrar remotamente un servidor Linux.
- Analizar recursos de una instancia.
- Crear archivos y scripts Bash.
- Identificar procesos.
- Consultar logs.
- Trabajar con permisos.
- Comprender que EC2 entrega infraestructura, pero la administración del sistema sigue siendo responsabilidad del usuario.

---

# Parte 1. Exploración del servidor (Evidencia)

```text
ubuntu@ip-172-31-26-92:~$ pwd
/home/ubuntu

ubuntu@ip-172-31-26-92:~$ uptime
 23:28:30 up 17 min,  1 user,  load average: 0.00, 0.00, 0.00

ubuntu@ip-172-31-26-92:~$ df -h
Filesystem       Size  Used Avail Use% Mounted on
/dev/root        6.7G  2.1G  4.6G  31% /
tmpfs            455M     0  455M   0% /dev/shm
tmpfs            182M  892K  181M   1% /run
/dev/nvme0n1p13  989M   98M  824M  11% /boot
/dev/nvme0n1p15  105M  6.3M   99M   7% /boot/efi

ubuntu@ip-172-31-26-92:~$ free -h
               total        used        free      shared  buff/cache   available
Mem:           908Mi       299Mi       385Mi       2.7Mi       333Mi       609Mi
Swap:             0B          0B          0B
```

---

# Parte 2. Estructura de directorios

```bash
mkdir -p ~/ec2-lab/{scripts,logs,data}
cd ~/ec2-lab
echo "EC2 laboratorio" > data/identificacion.txt
cat data/identificacion.txt
```

---

# Parte 3. Procesos

```text
ubuntu@ip-172-31-26-92:~/ec2-lab$ ps aux | grep ssh
root         698  0.0  0.8  10720  7576 ?        Ss   23:11   0:00 sshd: /usr/sbin/sshd -D -o AuthorizedKeysCommand /usr/share/ec2-instance-connect/eic_run_authorized_keys %u %f -o AuthorizedKeysCommandUser ec2-instance-connect [listener] 0 of 10-100 startups
root        1111  0.0  1.3  18132 12204 ?        Ss   23:18   0:00 sshd-session: ubuntu [priv]
ubuntu      1231  0.0  0.8  18432  7904 ?        S    23:18   0:00 sshd-session: ubuntu@pts/0
ubuntu      1442  0.0  0.2   7144  2368 pts/0    S+   23:29   0:00 grep --color=auto ssh
```

### Análisis de los campos de un proceso:
* **PID (Process Identifier):** Identificador numérico único asignado por el kernel de Linux a cada proceso activo.
* **Usuario (USER):** Cuenta propietaria del proceso que define su nivel de permisos y accesos en el sistema (`root` para demonios globales, `ubuntu` para procesos de usuario).
* **CPU (%CPU):** Porcentaje de uso del procesador por parte del proceso (en reposo suele ser 0.0%).
* **Memoria (%MEM):** Porcentaje de memoria RAM física asignada al proceso.
* **Comando (COMMAND):** Ruta del archivo binario ejecutable y argumentos con los que fue invocado.

---

# Parte 4. Usuarios y permisos

```bash
sudo adduser operador
sudo usermod -aG sudo operador
su - operador
touch archivo_operador.txt
ls -l archivo_operador.txt
exit
```

---

# Parte 5 y 6. Script `system_info.sh` y Reto

Script guardado en `scripts/system_info.sh`:

```bash
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
```

### Evidencia de ejecución con argumento (`./scripts/system_info.sh /var/log`):

```text
ubuntu@ip-172-31-26-92:~/ec2-lab$ ./scripts/system_info.sh /var/log
==========================================
          REPORTE DE SISTEMA EC2          
==========================================
Hostname: ip-172-31-26-92
Usuario:  ubuntu
Fecha:    Sun Nov  8 23:45:32 UTC 2026
Uptime:   up 34 minutes

--- Uso de Memoria RAM ---
               total        used        free      shared  buff/cache   available
Mem:           908Mi       312Mi       367Mi       2.7Mi       338Mi       595Mi
Swap:             0B          0B          0B

--- Filesystem para la ruta: /var/log ---
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       6.7G  2.1G  4.6G  31% /
==========================================
```

---

# Entregables

### 1. Resumen de recursos observados en la EC2:
* **CPU:** 2 vCPUs con carga nula (`load average: 0.00`), lo que indica un sistema ágil y sin cuellos de botella de procesamiento.
* **Memoria RAM:** 908 MiB de memoria total disponible (`t3.micro`), con 312 MiB en uso (34%), 367 MiB completamente libres y 338 MiB en buffers/caché del sistema. No se observa memoria de intercambio activa (`Swap: 0B`).
* **Almacenamiento en Disco:** El volumen raíz EBS montado en `/` (`/dev/root`) cuenta con 6.7 GiB útiles, de los cuales 2.1 GiB están ocupados por el sistema operativo base y 4.6 GiB permanecen disponibles (31% de ocupación).

### 2. Explicación de tres procesos encontrados en la instancia:
1. **`/sbin/init` (PID 1):** Es el primer proceso que ejecuta el kernel al arrancar (systemd en Ubuntu). Es el ancestro de todos los demás procesos y demonios del sistema operativo; administra el ciclo de vida de los servicios del servidor.
2. **`systemd-journald` (PID 129):** Demonio encargado de recolectar, estructurar, indexar y gestionar los registros de eventos y logs de todo el sistema operativo (accesibles mediante `journalctl`).
3. **`sshd` (PID 698):** Demonio del servidor OpenSSH. Permanece en ejecución constante como servicio en segundo plano escuchando en el puerto 22 para autenticar y establecer túneles de comunicación remota cifrada con los clientes SSH.

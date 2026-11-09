# Workshop 5 — Automatización de EC2 con User Data

**Curso:** Computación en la Nube e Internet de las Cosas

**Temas:**

- User Data
- Bash
- Automatización
- Provisionamiento
- Reproducibilidad
- EC2

---

# Objetivos

Al finalizar este workshop el estudiante será capaz de:

- Comprender el propósito de User Data.
- Automatizar tareas de inicialización.
- Instalar software automáticamente.
- Crear un servidor reproducible.
- Comparar configuración manual frente a configuración automatizada.

---

# Parte 1. Configuración manual

En una EC2 nueva, realice manualmente:

```bash
sudo apt update
sudo apt install -y nginx
sudo systemctl status nginx
```

---

# Parte 2. Convertir la configuración en script

Cree un script como User Data:

```bash
#!/bin/bash

apt update
apt install -y nginx

systemctl enable nginx
systemctl start nginx

cat > /var/www/html/index.html <<'EOFHTML'
<h1>Servidor provisionado automáticamente</h1>
<p>EC2 + User Data</p>
EOFHTML
```

---

# Parte 3. Lanzar otra EC2

Cree una nueva instancia y coloque el script anterior en **User Data** durante el lanzamiento.

```text
Launch EC2
     |
     v
User Data
     |
     +--> apt update
     +--> install nginx
     +--> create website
     |
     v
Servidor listo
```

---

# Parte 4. Verificación

Desde el computador acceda a:

```text
http://<IP_PUBLICA>
```

---

# Parte 5. Análisis

| Criterio | Configuración Manual (SSH) | User Data (Automatización) |
| :--- | :--- | :--- |
| **Repetibilidad** | **Muy baja.** Depende de la memoria, notas o historial de comandos del operador; propensa a que dos servidores queden con versiones o configuraciones diferentes. | **Idéntica (100%).** Cada instancia que se lanza ejecuta exactamente las mismas instrucciones de forma determinística. |
| **Tiempo requerido** | **Alto.** Requiere esperar que la máquina inicie, buscar la IP, autenticarse por SSH, ejecutar comando por comando y esperar descargas interactivamente (10 - 20 min). | **Mínimo (0 intervención).** El operador lanza la máquina en un clic y el sistema se auto-configura en segundo plano en 1 a 2 minutos. |
| **Errores humanos** | **Elevado.** Riesgo de cometer errores tipográficos (*typos*), omitir pasos, aplicar permisos erróneos o saltarse dependencias críticas. | **Nulo.** Una vez probado y validado el script, se ejecuta de forma desatendida sin intervención humana. |
| **Documentación** | **Tradicional/Frágil.** Depende de manuales "paso a paso" (runbooks/playbooks) que rápidamente quedan obsoletos respecto a lo instalado en el servidor. | **Infraestructura como Código (IaC).** El script de User Data es código ejecutable y versionable en Git que documenta con precisión el estado deseado. |
| **Escalabilidad** | **Inviable.** No permite escalar dinámicamente cuando hay picos de tráfico; imposible de usar en grupos de auto-escalado. | **Nativa y masiva.** Es el pilar para los *Auto Scaling Groups*; permite encender 10 o 100 máquinas que entran productivas automáticamente. |

---

# Reto

Modifique el script para instalar Docker y dejar un contenedor ejecutándose automáticamente.

Resultado esperado:

```text
Nueva EC2
   |
User Data
   |
Docker
   |
Container
   |
Aplicación
```

---

# Entregable

- Script User Data.
- Captura del servidor funcionando.
- Comparación manual vs automatización.
- Explicación de qué tareas convendría automatizar en una arquitectura real.

¿Qué tareas convendría automatizar en una arquitectura real de producción?
En entornos empresariales y de producción cloud, se automatizan obligatoriamente:
1. **Actualizaciones críticas y parches de seguridad del sistema operativo** (`security patches`) al momento de inicializar la máquina.
2. **Instalación de agentes de observabilidad y telemetría:** AWS CloudWatch Agent, Datadog Agent, o Prometheus Node Exporter para monitorizar CPU, RAM y disco en tiempo real.
3. **Instalación de agentes de seguridad y gestión centralizada:** AWS Systems Manager (SSM Agent) para prescindir totalmente de abrir el puerto 22 SSH.
4. **Montaje de sistemas de archivos de red o volúmenes compartidos:** Montaje automático de Amazon EFS (`NFS`) o adjuntar volúmenes EBS secundarios con formateo condicional.
5. **Configuración de variables de entorno y secretos:** Descarga segura de secretos y credenciales de bases de datos desde AWS Secrets Manager o AWS Systems Manager Parameter Store.
6. **Descarga y ejecución de artefactos de software:** Clonar repositorios de Git, descargar imágenes de Docker desde Amazon ECR y ejecutar `docker compose up -d`.
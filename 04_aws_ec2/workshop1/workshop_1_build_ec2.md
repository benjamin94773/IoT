# Workshop 1 — Crear y conectar una instancia EC2

**Curso:** Computación en la Nube e Internet de las Cosas

**Temas:**

- Amazon EC2
- AMI
- Instance Type
- Region y Availability Zone
- Key Pair
- Security Group
- VPC y Subnet
- IP pública
- SSH

---

# Objetivos

Al finalizar este workshop el estudiante será capaz de:

- Crear una instancia EC2 desde la consola de AWS.
- Identificar los componentes principales de una instancia.
- Seleccionar una AMI y un tipo de instancia.
- Configurar un Key Pair.
- Configurar un Security Group básico.
- Identificar la IP pública de una instancia.
- Conectarse a una instancia Linux mediante SSH.

---

# Conceptos que se trabajarán

- EC2 como IaaS.
- AMI.
- Instance Type.
- Region y Availability Zone.
- VPC y Subnet.
- Security Group.
- Key Pair.
- SSH.
- Public IP y Private IP.

---

# Parte 1. Preparación

Antes de crear la instancia, responder:

1. ¿Qué diferencia existe entre una AMI y un Instance Type?
La **AMI** es la plantilla de software (sistema operativo, configuraciones y librerías); el **Instance Type** define el hardware virtual asignado (vCPU, memoria RAM y rendimiento de red).
2. ¿Qué función cumple el Security Group?
Actúa como un firewall virtual a nivel de instancia que filtra el tráfico de red entrante y saliente mediante reglas con estado (*stateful*), bloqueando todo por defecto.
3. ¿Por qué SSH requiere una autenticación segura?
Protege el acceso administrativo remoto frente a ataques continuos de fuerza bruta en el puerto 22, utilizando criptografía asimétrica (pares de claves pública/privada) en lugar de contraseñas vulnerables.
4. ¿Por qué debemos seleccionar cuidadosamente la región?
Impacta directamente en la latencia de conexión (cercanía física), la variación de tarifas de cómputo, la disponibilidad de tipos de instancias/servicios y el cumplimiento de leyes locales de soberanía de datos.

---

# Parte 2. Crear la instancia

Desde AWS Console:

1. Ingrese a EC2.
2. Seleccione una región.
3. Seleccione **Launch Instance**.
4. Asigne un nombre, por ejemplo:

```text
curso-ec2-<nombre>
```

5. Seleccione una AMI Linux, por ejemplo Ubuntu.
6. Seleccione un Instance Type pequeño apropiado para laboratorio.
7. Cree o seleccione un Key Pair.
8. Configure un Security Group que permita SSH desde una fuente restringida cuando sea posible.
9. Revise el almacenamiento.
10. Lance la instancia.

---

# Parte 3. Verificar el estado

La instancia debe llegar al estado:

```text
running
```

Identifique:

- Instance ID.
- Public IPv4 address.
- Private IPv4 address.
- Availability Zone.
- AMI.
- Instance Type.
- Security Group.

---

# Parte 4. Conectarse por SSH

En Linux/macOS:

```bash
chmod 400 ~/Downloads/labsuser.pem
```

Después:

```bash
ssh -i ~/Downloads/labsuser.pem ubuntu@13.218.87.210
```

El nombre del usuario depende de la AMI seleccionada.

---

# Parte 5. Verificar el sistema

Una vez conectado:

```bash
whoami
hostname
uname -a
df -h
free -h
ip addr
```

---

# Parte 6. Actividad de análisis

Construya una tabla con:

| Elemento | Valor | ¿Para qué sirve? |
|----------|-------|------------------|
| AMI | `ami-0cb97d7f07b25dd693` (Ubuntu Server LTS) | Plantilla de software preconfigurada que contiene el sistema operativo Linux con el que arranca la instancia. |
| Instance Type | `t3.micro` | Define el hardware virtualizado de la máquina (capacidad de cómputo: 2 vCPU y 1 GiB de memoria RAM). |
| Region | `us-east-1` (Norte de Virginia) | Ubicación geográfica mundial donde se encuentran los centros de datos físicos de AWS que alojan los recursos. |
| Availability Zone | `us-east-1d` | Centro de datos físico aislado e independiente dentro de la región, con alimentación y redes redundantes para tolerar fallos. |
| VPC | `vpc-0e28e3641cd1bb206` | Red virtual privada aislada lógicamente en la nube donde conviven tus servidores de forma segura. |
| Subnet | `subnet-02d093c299cb94a2c` | Rango de direcciones IP asignado dentro de la VPC para una zona de disponibilidad específica. |
| Public IP | `13.218.87.210` | Dirección IP accesible y enrutable desde todo Internet para comunicarse con la máquina por SSH y HTTP. |
| Private IP | `172.31.26.92` | Dirección IP interna para comunicación privada y segura entre instancias dentro de la misma VPC sin salir a Internet. |
| Security Group | `Test` (o `launch-wizard-3`) | Firewall virtual a nivel de red que controla el tráfico entrante y saliente permitido hacia la instancia. |
| Key Pair | `vockey` | Par de llaves criptográficas asimétricas (pública/privada) para autenticar la conexión segura por SSH sin usar contraseñas débiles. |

---

# Reto

Explique con sus propias palabras qué sucede desde que presiona **Launch Instance** hasta que obtiene acceso por SSH.

AWS asigna el hardware: Al presionar Launch Instance, AWS busca un servidor físico en su centro de datos con espacio libre y reserva los recursos virtuales de la máquina (en este caso, los 2 núcleos y 1 GB de RAM del t3.micro).
Crea el disco duro: Se clona la imagen de Ubuntu (la AMI) en un disco virtual nuevo (EBS de 8 GB) y se conecta a la máquina como disco principal.
Inyecta la llave de acceso: Durante el primer arranque, el sistema operativo guarda la llave pública del par vockey dentro de la carpeta oculta ~/.ssh/authorized_keys del usuario ubuntu para poder reconocernos luego.
Configura la red y el firewall: Le asigna una IP privada interna y una IP pública para Internet, y activa el Security Group como un firewall que solo deja pasar tráfico por el puerto 22 (SSH).
Arranca el sistema: Ubuntu inicia todos sus servicios en segundo plano, incluyendo el servidor SSH (sshd). Una vez el sistema pasa las revisiones de salud de AWS, se pone en estado Running.
Conexión SSH: Cuando ejecutamos ssh -i labsuser.pem ubuntu@13.218.87.210, la petición llega a la IP pública, el Security Group la deja pasar por el puerto 22, el servidor comprueba que nuestra llave privada (.pem) coincide con la pública que guardó al inicio y nos da acceso directo a la terminal.

---

# Entregable

- Captura de la instancia en estado `running`.
- Captura de la conexión SSH.
- Tabla de componentes.
- Respuestas de análisis.

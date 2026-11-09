# Taller 2 - Bash

**Curso:** Computación en la Nube e Internet de las Cosas

**Temas**:
    - Bash

---

# Objetivos

- Manipular archivos mediante filtros.
- Buscar información.
- Redireccionar entrada y salida.
- Utilizar tuberías.
- Trabajar con permisos.

---

# Conceptos

- Entrada estándar (stdin)
- Salida estándar (stdout)
- Error estándar (stderr)
- Pipes
- Redirecciones
- Permisos Linux
- Usuarios y grupos

---

# Comandos

| Comando | Función |
|----------|----------|
| grep | Buscar texto |
| find | Buscar archivos |
| wc | Contar |
| sort | Ordenar |
| uniq | Eliminar repetidos |
| head | Primeras líneas |
| tail | Últimas líneas |
| chmod | Cambiar permisos |
| chown | Cambiar propietario |
| tee | Duplicar salida |
| cut | Extraer columnas |
| tr | Transformar texto |
| diff | Comparar archivos |
| file | Tipo de archivo |

---

# Ejercicio 1

Crear un archivo

```bash
cat > estudiantes.txt
```

Ingresar

```
Ana
Pedro
Juan
Ana
Carlos
Pedro
```

---

# Ejercicio 2

Buscar

```bash
grep Ana estudiantes.txt
```

Buscar ignorando mayúsculas

```bash
grep -i ana estudiantes.txt
```

---

# Ejercicio 3

Contar líneas

```bash
wc estudiantes.txt
```

Solo líneas

```bash
wc -l estudiantes.txt
```

---

# Ejercicio 4

Ordenar

```bash
sort estudiantes.txt
```

Eliminar duplicados

```bash
sort estudiantes.txt | uniq
```

---

# Ejercicio 5

Primeras líneas

```bash
head estudiantes.txt
```

Últimas

```bash
tail estudiantes.txt
```

---

# Ejercicio 6

Buscar archivos

```bash
find . -name "*.txt"
```

Buscar directorios

```bash
find . -type d
```

---

# Ejercicio 7

Redirecciones

```bash
ls > archivos.txt
```

Agregar

```bash
pwd >> archivos.txt
```

Errores

```bash
ls carpeta_inexistente 2> errores.txt
```

---

# Ejercicio 8

Pipes

```bash
cat estudiantes.txt | sort | uniq | wc -l
```

---

# Ejercicio 9

Permisos

Crear script

```bash
touch hola.sh
```

Dar permisos

```bash
chmod +x hola.sh
```

Verificar

```bash
ls -l
```

---

# Ejercicio 10

Tipo de archivo

```bash
file hola.sh
```

---

# Reto

Encontrar todos los archivos `.txt`, ordenarlos alfabéticamente y guardar el resultado en `reporte.txt`.
find . -name "*.txt" | sort > reporte.txt

---

# Preguntas

1. ¿Qué hace una tubería?
Conecta la salida de un comando directamente con la entrada de otro comando
2. Diferencia entre `>` y `>>`.
El > (Redirección simple / Sobrescribir): Si el archivo ya existe, borra todo su contenido y escribe lo nuevo. Si no existe, lo crea.
El >> (Redirección doble / Añadir): No borra nada. Agrega el nuevo texto al final del archivo, justo debajo de lo que ya existía.
3. ¿Qué significa `chmod +x`?
Significa darle permisos de ejecución (+x) a un archivo.
4. ¿Qué diferencia existe entre `grep` y `find`?
Aunque ambos sirven para buscar, lo hacen en lugares completamente distintos:
find: Busca archivos y carpetas por su nombre, tamaño o fecha en el disco (ej. "busca el archivo reporte.txt").
grep: Busca texto específico dentro del contenido de los archivos (ej. "busca la palabra 'Ana' adentro de estudiantes.txt").

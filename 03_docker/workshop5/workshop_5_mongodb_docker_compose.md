# Taller 5 - MongoDB con Docker y Docker Compose

**Curso:** Computación en la Nube e Internet de las Cosas

**Temas**:

- MongoDB
- Docker
- Docker Compose
- NoSQL
- Documentos
- Colecciones
- Scripts de inicialización

---

# Objetivos

Al finalizar este workshop el estudiante será capaz de:

- Ejecutar MongoDB con Docker Compose.
- Utilizar `mongosh`.
- Crear manualmente una base y colecciones.
- Insertar y consultar documentos.
- Comprender el modelo documental.
- Automatizar la creación de colecciones y documentos con JavaScript.
- Reinicializar MongoDB desde cero y verificar la estructura resultante.

---

# Parte 1. MongoDB manual

Crear:

```yaml
services:
  mongo:
    image: mongo:8
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin
    ports:
      - "27017:27017"
```

Levantar:

```bash
docker compose up -d
```

Entrar:

```bash
docker compose exec mongo mongosh -u admin -p admin --authenticationDatabase admin
```

Crear la base:

```javascript
use tienda
```

Crear colección:

```javascript
db.createCollection("products")
```

Insertar:

```javascript
db.products.insertMany([
  { name: "Laptop", price: 3500000, stock: 5 },
  { name: "Mouse", price: 80000, stock: 20 },
  { name: "Keyboard", price: 150000, stock: 12 }
])
```

Consultar:

```javascript
db.products.find()
```
Evidencia ejecucion
```
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop5> docker compose config
>> 
name: workshop5
services:
  mongo:
    environment:
      MONGO_INITDB_ROOT_PASSWORD: admin
      MONGO_INITDB_ROOT_USERNAME: admin
    image: mongo:8
    networks:
      default: null
    ports:
      - mode: ingress
        target: 27017
        published: "27017"
        protocol: tcp
networks:
  default:
    name: workshop5_default
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop5> docker compose up -d
[+] up 13/13
 ✔ Image mongo:8               Pulled                                                                                                      25.2s
 ✔ Network workshop5_default   Created                                                                                                      0.0s
 ✔ Container workshop5-mongo-1 Started                                                                                                      0.5s
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop5> docker compose ps
NAME                IMAGE     COMMAND                  SERVICE   CREATED         STATUS        PORTS
workshop5-mongo-1   mongo:8   "docker-entrypoint.s…"   mongo     2 seconds ago   Up 1 second   0.0.0.0:27017->27017/tcp, [::]:27017->27017/tcp
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop5> docker compose exec mongo mongosh -u admin -p admin --authenticationDatabase admin
Current Mongosh Log ID: 6a9c9ca2c5af876b072e8e75
Connecting to:          mongodb://<credentials>@127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+2.10.0
Using MongoDB:          8.3.8
Using Mongosh:          2.10.0

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/


To help improve our products, anonymous usage data is collected and sent to MongoDB periodically (https://www.mongodb.com/legal/privacy-policy).
You can opt-out by running the disableTelemetry() command.

------
   The server generated these startup warnings when booting
   2026-09-05T22:50:03.205+00:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   2026-09-05T22:50:03.489+00:00: For customers running the current memory allocator, we suggest changing the contents of the following sysfsFile
   2026-09-05T22:50:03.489+00:00: For customers running the current memory allocator, we suggest changing the contents of the following sysfsFile
   2026-09-05T22:50:03.489+00:00: We suggest setting the contents of sysfsFile to 0.
   2026-09-05T22:50:03.489+00:00: vm.max_map_count is too low
   2026-09-05T22:50:03.489+00:00: We suggest setting swappiness to 0 or 1, as swapping can cause performance problems.
------

test> use tienda
switched to db tienda
tienda> db.createCollection("products")
{ ok: 1 }
tienda> db.products.insertMany([
|   { name: "Laptop", price: 3500000, stock: 5 },
|   { name: "Mouse", price: 80000, stock: 20 },
|   { name: "Keyboard", price: 150000, stock: 12 }
| ])
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId('6a9c9cc7c5af876b072e8e76'),
    '1': ObjectId('6a9c9cc7c5af876b072e8e77'),
    '2': ObjectId('6a9c9cc7c5af876b072e8e78')
  }
}
tienda> db.products.find()
[
  {
    _id: ObjectId('6a9c9cc7c5af876b072e8e76'),
    name: 'Laptop',
    price: 3500000,
    stock: 5
  },
  {
    _id: ObjectId('6a9c9cc7c5af876b072e8e77'),
    name: 'Mouse',
    price: 80000,
    stock: 20
  },
  {
    _id: ObjectId('6a9c9cc7c5af876b072e8e78'),
    name: 'Keyboard',
    price: 150000,
    stock: 12
  }
]
tienda> 

```

---

# Parte 2. Explorar colecciones y documentos

```javascript
show dbs
show collections
db.products.countDocuments()
db.products.find({ stock: { $gt: 10 } })
```

Analizar cómo un documento puede incluir estructuras anidadas.

### Documentos anidados

MongoDB permite almacenar objetos y arreglos dentro de un documento. En el producto `Laptop Pro`, el campo `specifications` contiene información técnica como marca, memoria RAM y almacenamiento. El campo `tags` contiene un arreglo de etiquetas.

Esto permite guardar información relacionada en un solo documento, sin necesitar tablas adicionales ni relaciones obligatorias como en una base de datos relacional.


Evidencia
```
tienda> show dbs
admin   100.00 KiB
config   12.00 KiB
local    72.00 KiB
tienda   40.00 KiB
tienda> show collections
products
tienda> db.products.countDocuments()
3
tienda> db.products.find({ stock: { $gt: 10 } })
[
  {
    _id: ObjectId('6a9c9cc7c5af876b072e8e77'),
    name: 'Mouse',
    price: 80000,
    stock: 20
  },
  {
    _id: ObjectId('6a9c9cc7c5af876b072e8e78'),
    name: 'Keyboard',
    price: 150000,
    stock: 12
  }
]
tienda> 
tienda> db.products.insertOne({
|   name: "Laptop Pro",
|   price: 5000000,
|   stock: 8,
|   specifications: {
|     brand: "Lenovo",
|     ram: "16GB",
|     storage: "512GB SSD"
|   },
|   tags: ["computers", "portable", "premium"]
| })
{
  acknowledged: true,
  insertedId: ObjectId('6a9c9d6dc5af876b072e8e79')
}
tienda> db.products.findOne({ name: "Laptop Pro" })
{
  _id: ObjectId('6a9c9d6dc5af876b072e8e79'),
  name: 'Laptop Pro',
  price: 5000000,
  stock: 8,
  specifications: { brand: 'Lenovo', ram: '16GB', storage: '512GB SSD' },
  tags: [ 'computers', 'portable', 'premium' ]
}
tienda> db.products.find({ "specifications.ram": "16GB" })
[
  {
    _id: ObjectId('6a9c9d6dc5af876b072e8e79'),
    name: 'Laptop Pro',
    price: 5000000,
    stock: 8,
    specifications: { brand: 'Lenovo', ram: '16GB', storage: '512GB SSD' },
    tags: [ 'computers', 'portable', 'premium' ]
  }
]
```

---

# Parte 3. Automatización mediante archivo JavaScript

Crear:

```text
mongo/init/01-init.js
```

Contenido:

```javascript
db = db.getSiblingDB('tienda');

db.products.insertMany([
  { name: 'Laptop', price: 3500000, stock: 5 },
  { name: 'Mouse', price: 80000, stock: 20 },
  { name: 'Keyboard', price: 150000, stock: 12 }
]);

db.customers.insertMany([
  { name: 'Ana', email: 'ana@example.com' },
  { name: 'Luis', email: 'luis@example.com' }
]);
```

Montar el directorio:

```yaml
services:
  mongo:
    image: mongo:8
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
      - ./mongo/init:/docker-entrypoint-initdb.d:ro

volumes:
  mongo_data:
```

---

# Parte 4. Verificar la carga automática

Recrear la instancia desde cero:

```bash
docker compose down -v
```

Luego:

```bash
docker compose up -d
```

Entrar y consultar:

```bash
docker compose exec mongo mongosh -u admin -p admin --authenticationDatabase admin
```

```javascript
use tienda
show collections
db.products.find()
db.customers.find()
```
Evidencia Parte 4
```
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop5> docker compose down -v
[+] down 2/2
 ✔ Container workshop5-mongo-1 Removed                                                                                                      0.4s
 ✔ Network workshop5_default   Removed                                                                                                      0.2s
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop5> docker compose up -d
[+] up 3/3
 ✔ Volume workshop5_mongo_data Created                                                                                                      0.0s
 ✔ Network workshop5_default   Created                                                                                                      0.0s
 ✔ Container workshop5-mongo-1 Started                                                                                                      0.2s
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop5> docker compose exec mongo mongosh -u admin -p admin --authenticationDatabase admin
Current Mongosh Log ID: 6a9c9e2163e4fc89248d7ca7
Connecting to:          mongodb://<credentials>@127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+2.10.0
Using MongoDB:          8.3.8
Using Mongosh:          2.10.0

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/


To help improve our products, anonymous usage data is collected and sent to MongoDB periodically (https://www.mongodb.com/legal/privacy-policy).
You can opt-out by running the disableTelemetry() command.

------
   The server generated these startup warnings when booting
   2026-09-05T22:56:31.331+00:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   2026-09-05T22:56:31.557+00:00: For customers running the current memory allocator, we suggest changing the contents of the following sysfsFile
   2026-09-05T22:56:31.557+00:00: For customers running the current memory allocator, we suggest changing the contents of the following sysfsFile
   2026-09-05T22:56:31.558+00:00: We suggest setting the contents of sysfsFile to 0.
   2026-09-05T22:56:31.558+00:00: vm.max_map_count is too low
   2026-09-05T22:56:31.558+00:00: We suggest setting swappiness to 0 or 1, as swapping can cause performance problems.
------

test> use tienda
switched to db tienda
tienda> show collections
customers
products
tienda> db.products.find()
[
  {
    _id: ObjectId('6a9c9e1efa371b12b8903258'),
    name: 'Laptop',
    price: 3500000,
    stock: 5
  },
  {
    _id: ObjectId('6a9c9e1efa371b12b8903259'),
    name: 'Mouse',
    price: 80000,
    stock: 20
  },
  {
    _id: ObjectId('6a9c9e1efa371b12b890325a'),
    name: 'Keyboard',
    price: 150000,
    stock: 12
  }
]
tienda> db.customers.find()
[
  {
    _id: ObjectId('6a9c9e1efa371b12b890325b'),
    name: 'Ana',
    email: 'ana@example.com'
  },
  {
    _id: ObjectId('6a9c9e1efa371b12b890325c'),
    name: 'Luis',
    email: 'luis@example.com'
  }
]
tienda> 

```

---

# Parte 5. Reto de modelado

Crear mediante script las colecciones:

```text
products
customers
orders
```

Una orden puede almacenar:

```javascript
{
  customerId: 1,
  date: ISODate("2026-08-24T00:00:00Z"),
  items: [
    { product: "Laptop", quantity: 1 },
    { product: "Mouse", quantity: 2 }
  ]
}
```
Evidencia Parte 5

```

PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop5> docker compose down -v                                                  
[+] down 3/3
 ✔ Container workshop5-mongo-1 Removed                                                                                                      0.4s
 ✔ Volume workshop5_mongo_data Removed                                                                                                      0.0s
 ✔ Network workshop5_default   Removed                                                                                                      0.2s
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop5> docker compose up -d                                                    
[+] up 3/3
 ✔ Volume workshop5_mongo_data Created                                                                                                      0.0s
 ✔ Network workshop5_default   Created                                                                                                      0.0s
 ✔ Container workshop5-mongo-1 Started                                                                                                      0.2s
PS C:\Users\Benja\OneDrive\Desktop\IOT\Entregables\03_docker\workshop5> docker compose exec mongo mongosh -u admin -p admin --authenticationDatabase admin
Current Mongosh Log ID: 6a9c9eb525ab235586bcb0ce
Connecting to:          mongodb://<credentials>@127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+2.10.0
Using MongoDB:          8.3.8
Using Mongosh:          2.10.0

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/


To help improve our products, anonymous usage data is collected and sent to MongoDB periodically (https://www.mongodb.com/legal/privacy-policy).
You can opt-out by running the disableTelemetry() command.

------
   The server generated these startup warnings when booting
   2026-09-05T22:59:01.080+00:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   2026-09-05T22:59:01.314+00:00: For customers running the current memory allocator, we suggest changing the contents of the following sysfsFile
   2026-09-05T22:59:01.314+00:00: For customers running the current memory allocator, we suggest changing the contents of the following sysfsFile
   2026-09-05T22:59:01.314+00:00: We suggest setting the contents of sysfsFile to 0.
   2026-09-05T22:59:01.314+00:00: vm.max_map_count is too low
   2026-09-05T22:59:01.314+00:00: We suggest setting swappiness to 0 or 1, as swapping can cause performance problems.
------

test> use tienda
switched to db tienda
tienda> show collections
customers
orders
products
tienda> db.orders.find().pretty()
[
  {
    _id: ObjectId('6a9c9eb3026d08135a27b2dd'),
    customerId: 1,
    date: ISODate('2026-08-24T00:00:00.000Z'),
    items: [
      { product: 'Laptop', quantity: 1 },
      { product: 'Mouse', quantity: 2 }
    ]
  }
]
tienda> db.orders.find({ "items.product": "Laptop" })
[
  {
    _id: ObjectId('6a9c9eb3026d08135a27b2dd'),
    customerId: 1,
    date: ISODate('2026-08-24T00:00:00.000Z'),
    items: [
      { product: 'Laptop', quantity: 1 },
      { product: 'Mouse', quantity: 2 }
    ]
  }
]
tienda> 
```

---

# Parte 6. Comparación PostgreSQL vs MongoDB

Responder:

1. ¿Qué diferencia existe entre tabla y colección?
una tabla tiene estructura definida por columnas; una colección agrupa documentos y puede contener documentos con estructuras diferentes.

2. ¿Qué diferencia existe entre fila y documento?
una fila contiene valores en columnas; un documento contiene pares clave-valor y puede incluir objetos o arreglos anidados.

3. ¿Qué ventaja ofrecen los documentos anidados?
permiten guardar información relacionada en un solo documento, evitando muchas uniones o tablas intermedias.

4. ¿Qué riesgos tiene duplicar datos en documentos?
la información puede quedar inconsistente si se actualiza en un documento pero no en los demás.

5. ¿Qué tipos de aplicaciones podrían beneficiarse de MongoDB?
catálogos, redes sociales, registros de eventos, sistemas IoT y aplicaciones con datos flexibles o cambiantes.

6. ¿Qué modelo resulta más adecuado para el ejercicio universitario y por qué?
PostgreSQL resulta más adecuado porque estudiantes, profesores, cursos y matrículas tienen relaciones claras y llaves foráneas. MongoDB sería útil si los datos fueran más variables o si se quisieran guardar estructuras anidadas.


---

# Entregables

- `docker-compose.yml`.
- Carpeta `mongo/init/`.
- Script `.js`.
- Evidencia de creación manual.
- Evidencia de carga automática.
- Consultas realizadas.
- Comparación PostgreSQL vs MongoDB.

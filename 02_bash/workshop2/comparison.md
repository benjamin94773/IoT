# Comparacion entre CMD y ENTRYPOINT

| Caso | Sin argumentos | Con argumento | Comportamiento |
|---|---|---|---|
| Solo CMD | Ejecuta el comando y mensaje definidos en CMD | El argumento reemplaza completamente a CMD | CMD funciona como valor por defecto y puede ser reemplazado |
| Solo ENTRYPOINT | Ejecuta el programa definido en ENTRYPOINT sin argumentos adicionales | El argumento se agrega al programa fijo | ENTRYPOINT define el ejecutable principal |
| ENTRYPOINT + CMD | Ejecuta ENTRYPOINT con el valor de CMD | El argumento reemplaza el valor de CMD | ENTRYPOINT queda fijo y CMD funciona como argumento por defecto |

## Respuestas

1. `CMD` se comporta como valor por defecto. Puede definir el comando principal por defecto o los argumentos por defecto.
2. `ENTRYPOINT` define el programa principal del contenedor y normalmente permanece fijo cuando se pasan argumentos.
3. Cuando se pasa un comando al final de `docker run`, ese valor reemplaza completamente a `CMD`. En la combinacion `ENTRYPOINT` + `CMD`, reemplaza los argumentos definidos por `CMD` y conserva `ENTRYPOINT`.
4. `ENTRYPOINT` es util cuando el contenedor debe comportarse como una herramienta concreta, porque fija el ejecutable y evita que el uso normal cambie el programa principal.
5. Usaria `ENTRYPOINT` para el ejecutable fijo y `CMD` para los parametros por defecto que se puedan reemplazar al ejecutar `docker run`.
---
title: Injection
node_type: machine
platform: dockerlabs
difficulty: muy-facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Muy Faciles/Injection.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Injection

## Resumen

Injection resume una cadena de SQL Injection y login bypass: el acceso se obtiene manipulando la logica de autenticacion y despues se revisan permisos locales para escalar por SUID.

Fuente original: [Maquinas De Dockerlabs/Maquinas Muy Faciles/Injection.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Muy%20Faciles/Injection.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | muy-facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 80 |
| Imagenes en fuente | 12 |
| Palabras en fuente | 1007 |
| Requiere revision | false |

## Resolucion paso a paso

>Hoy tenemos la máquina Injection, de Dificultad muy fácil, muy muy fácil…

![Ingection](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Ingection.png)

>Así que bien, como siempre, empezamos descomprimiendo el archivo zip que descargamos de Docker Labs:[https://dockerlabs.es](https://dockerlabs.es)

![Ingection](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Ingection%201.png)

>Una vez en uso, haremos un escaneo general (a modo de traza), a la interfaz de red Docker0, donde encontramos la IP Victima :3

![Ingection](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Ingection%202.png)

>Procedemos con un escaneo relativamente completo con nmap

![Ingection](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Ingection%203.png)
1. _-- min-rate 4000 (Quiero tramitar mínimo 4000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (No deseo que nmap haga una resolución DNS automática)
3. _-p- (Quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
_El segundo escaneo, hecho al encontrar los puertos abiertos de la máquina, se realiza para identificarlos. -sVC es una forma acortada de los parámetros -sV (para identificar los servicios que pueden estar activos en cada puerto) y -sC (que realiza un pequeño ataque con algunos scripts propios de nmap)_

>Ahora bien, los scripts de nmap no nos dan mucha información, y al hacer una exploración bastante simple de las posibles vulnerabilidades de los servicios corriendo tampoco encontramos mucho. Así que, empezando por el puerto 80, haremos una exploración del servidor apache, donde encontramos un panel de login.

![Ingection](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Ingection%204.png)

>Antes de probar los usuarios y contraseñas más comunes, revisar el código fuente, o tal vez fuerza bruta. testeamos con una comilla si la base de datos tras el panel de login puede ser vulnerable a un SQLI.

![Ingection](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Ingection%205.png)

>Nos encontramos con que si, lo mas probable es que si. Lo usual al ver un error así de vistoso, es testear lo que sucede al cambiar la lógica de la consulta, con un payload muy conocido:

![Ingection](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Ingection%206.png)
_Bien, desglosando un poco lo sucedido: ‘ or 1=1- - -_

_Al ingresar en un panel de login, por lo general, la consulta que se realiza por detrás a una base de datos SQL se ve algo así:_

```sql
SELECT * FROM usuarios WHERE usuario = 'tu usuario' AND password = 'tu contraseña';
```
_Para generar un error en la consulta, ponemos la comilla. esto, por lógica, cerraría el valor esperado de usuario, y quedaría una comilla sobrando en la consulta, lo que la rompe._
```sql
SELECT * FROM usuarios WHERE usuario = ‘’ ’ AND password = 'tu contraseña';
```
_Luego, al inyectar el payload, la consulta quedara algo así:
```sql
SELECT * FROM usuarios WHERE usuario = ‘’ OR 1=1-- - ’ AND password = 'tu contraseña';
```
Al cerrar el valor esperado para “usuario” la consulta devolverá un código de estado falso o negativo, PERO con el operador lógico “or” le decimos a la consulta que si la primera condición (selección de usuario) no es correcta, compruebe otra condición, que sería “1=1”. Como en la lógica de programación 1 siempre será igual a 1, la consulta se toma como verdadera. Por último, con “-- -” comentamos el resto de la consulta SQL, la consulta quedaría algo así:_
```sql
SELECT * FROM usuarios WHERE usuario = ‘’ OR 1=1;
```

_Así que, lo que en pocas palabras se le dice al servidor es “si el usuario es correcto O si 1 es igual a 1 dame una respuesta positiva”, el servidor devuelve un usuario cualquiera y me permite entrar._

_Para entenderlo del todo, te recomiendo ir a la biblia del Hacking, donde lo entenderás a la perfección:_[_https://book.hacktricks.wiki/en/pentesting-web/sql-injection/index.html_](https://book.hacktricks.wiki/en/pentesting-web/sql-injection/index.html)

>Una vez explotado el SQL, vemos que el servidor nos devuelve un usuario y una contraseña.

![Ingection](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Ingection%207.png)

>Guiándonos por la corazonada de que reutilizan las contraseñas y usuarios de los servicios de la máquina, probamos con ssh.

![Ingection](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Ingection%208.png)

>Y efectivamente entramos a la máquina por ssh utilizando el usuario y la contraseña, si quieres saber un poco más sobre ssh aquí te dejo un versículo de la biblia:[https://book.hacktricks.wiki/es/network-services-pentesting/pentesting-ssh.html](https://book.hacktricks.wiki/es/network-services-pentesting/pentesting-ssh.html)

**Escalada de privilegios**

>Nuestro primer paso para escalar privilegios será buscar archivos con el bit SUID (en síntesis, archivos que podemos ejecutar con privilegios del propietario ROOT)

![Ingection](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Ingection%209.png)
1. Con el comando “find” Buscamos archivos
2. Con “/” especificamos que sea desde el directorio raiz
3. “-perm -4000” para especificar que queremos listar solamente archivos con el bit SUID
4. “-type f” para solo mostrar archivos y no directorios
5. “2>/dev/null” para enviar los errores al agujero negro de Linux (que no se muestren en pantalla)
6. A todo lo anterior le concatenamos un "xargs ls -lah" para que a cada iteración del primer comando (find / -perm -4000 -type f) le aplique un segundo comando (ls -lah), para así poder ver los permisos de cada archivo y sus propietarios.

>Bien, de todo lo anterior nos encontramos con el muy conocido archivo /usr/bin/env cuyo propietario es ROOT y tiene en sus permisos la s, que lo identifica como SUID.

>Este archivo con el bit SUID nos permite ejecutar otros archivos de la máquina con los permisos de ROOT, así que con abrir una terminal bash desde este archivo sería suficiente para ser usuario root

![Ingection](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Ingection%2010.png)

>Tristemente, parece que no podemos usar sudo, en esta maquina, así que probamos de otra manera

![Ingection](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Ingection%2011.png)

>Con el archivo /usr/bin/env ejecutamos /bin/sh (una Shell interactiva) y con el parámetro -p evitamos que /bin/sh ignore el bit SUID, es decir, lo obligamos a darnos una consola como ROOT. la máquina es nuestra :3

O.O   //El comando "rm -rf /*" ejecutado como administrador borra todos los archivos del sistema, es un pequeño guiño al ganar acceso como root a una máquina, NO LO EJECUTES//   O.O


## Cadena de ataque detectada

- **Enumeration**: Apache, HTTP, Port enumeration, SSH, Web enumeration
- **Initial Access**: Brute force, Login bypass, SQL Injection
- **Post Exploitation**: Credential extraction
- **Privilege Escalation**: SUID abuse, SUID binary abuse


## Tecnicas utilizadas

- [Brute force](../../../techniques/brute-force.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Login bypass](../../../techniques/login-bypass.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [SQL Injection](../../../techniques/sql-injection.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [find](../../../tools/find.md)
- [Nmap](../../../tools/nmap.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)


## Servicios relacionados

- [Apache](../../../services/apache.md)
- [HTTP](../../../services/http.md)
- [SSH](../../../services/ssh.md)


## Vulnerabilidades relacionadas

- [Exposed error message](../../../vulnerabilities/exposed-error-message.md)
- [SUID misconfiguration](../../../vulnerabilities/suid-misconfiguration.md)
- [Unsanitized user input](../../../vulnerabilities/unsanitized-user-input.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

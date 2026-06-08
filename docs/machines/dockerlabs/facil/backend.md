---
title: Backend
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Backend.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Backend

## Resumen

Backend documenta una ruta web centrada en SQL Injection error-based: enumeracion de HTTP/SSH, abuso de una entrada vulnerable para extraer informacion de base de datos, obtencion de credenciales y escalada posterior mediante cracking de hashes y binarios SUID.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Backend.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Backend.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 22, 80 |
| Imagenes en fuente | 46 |
| Palabras en fuente | 2727 |
| Requiere revision | false |

## Resolucion paso a paso

>Bueno bueno, hoy haremos una maquina sencilla para reforzar conceptos de SQLI Error Based

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250527020629.png)

>Así que sin mas, empezamos :3
>Primero, levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250527020730.png)

>Con Ping, enviamos unas cuantas trazas ICMP para verificar la conexión con la maquina:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250527020812.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, revisa las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse (Por lo general funciona para determinar el sistema operativo víctima)
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)

>Sabiendo que tenemos conexión con la maquina, procedemos a escanear con Nmap puertos abiertos y servicios de la maquina:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250527021108.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sVC (Aquí se concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_

>Vemos el puerto 22 SSH con un servicio OpenSSH relativamente actual, y un puerto 80 con un servicio Apache 2.4.61 corriendo.
>Vamos a la Web en el puerto 80 para conocer mas:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250527021542.png)

>Podemos observar una pagina bastante simple con un Home Page (Index.html) y un panel de Login (Login.html)
>Ese login se ve prometedor, así que vamos allí:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250527021808.png)

>El panel es bastante simple, si introducimos credenciales invalidas nos direcciona a una pagina de error:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250527022021.png)
_Intentamos inicial sesión con un usuario y contraseña cualquiera_

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250527022108.png)
_La pagina nos redirecciona a "logerror.html" si las credenciales son erróneas_

>Por detrás, hay una consulta a una base de datos para validar usuario y contraseña.
>Para verificar si el panel es vulnerable a "SQL Injection", introducimos una comilla como valor en el panel:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250527022447.png)
_Introducimos una comilla en el panel de usuario, y una contraseña cualquiera

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250527022541.png)
_Respuesta de la web_

>Vemos que la web nos responde con un error de SQL, esto quiere decir que el panel muy probablemente es vulnerable a SQLI.
>Al ingresar en un panel de login, por lo general, la consulta que se realiza por detrás a una base de datos SQL se ve algo así:

```sql
SELECT * FROM usuarios WHERE usuario = 'tu usuario' AND password = 'tu contraseña';
```
_Para generar un error en la consulta, ponemos la comilla. esto, por lógica, cerraría el valor esperado de usuario, y quedaría una comilla sobrando en la consulta, lo que la rompe y nos da el error que observamos en la web._
```sql
SELECT * FROM usuarios WHERE usuario = ‘’ ’ AND password = 'tu contraseña';
```

>Bien, desde este punto podríamos intentar cambiar la lógica de la consulta para saltarnos el panel de Login, pero, tristemente no podemos hacer un Bypass así de fácil (_Aun así, puedes ver su explotación en la maquina [Injection](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Injection.md)_). También podemos usar SQLMap para explotar la vulnerabilidad de manera automatizada, pero ya que complicándose se aprende mas, vamos a intentar explotarlo manualmente ╰(*°▽°*)╯

>El primero paso es determinar si podemos controlar el flujo de la consulta, es decir, ya sabemos que podemos ver errores que no deberíamos ver al romper una consulta, debido a que la entrada de usuario no fue bien sanitizada, pero debemos determinar si podemos inyectar mas parámetros en la consulta para que sean leídos por la base de datos, para esto, haremos una inyección simple:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250527024844.png)
1. _Con el operador lógico "or" le decimos a la web "si la anterior consulta es falsa , ejecuta esto"_
2. _Sleep(2) demora la consulta en la base de datos 2 segundos mas de lo habitual_
3. -- - Es una manera de cerrar la consulta y comentar todo lo que sigue tras de ella

>Y la web a tardado mas en respondernos!! ahora sabemos que podemos concatenar instrucciones, esto en la consulta en la base de datos se vería algo así:

```sql
SELECT * FROM usuarios WHERE usuario = ‘’ OR sleep(2)-- - ’ AND password = 'tu contraseña';
```
_Al cerrar el valor esperado para “usuario” la consulta devolverá un código de estado falso o negativo, PERO con el operador lógico “or” le decimos a la consulta que si la primera condición (selección de usuario) no es correcta, compruebe algo diferente (sleep(2)). Por último, con “-- -” comentamos el resto de la consulta SQL para evitar errores o la no ejecución del sleep, la consulta quedaría algo así:_
```sql
SELECT * FROM usuarios WHERE usuario = ‘’ OR sleep(2);
```

>Bien, los pasos para hacer una inyección SQL casi siempre son los mismos (O similares), ya sea un SQLI a ciegas, un Boolean Based o Error Based.
>Primero se descubren el numero de columnas que nos retorna una consulta, luego, se busca la columna visible en la web (la columna desde donde podremos inyectar querys maliciosas), desde allí, se va cambiando la lógica de la consulta para ir obteniendo información, desde las bases de datos y tablas, hasta la información de columnas como usuarios y contraseñas.

>Vamos desde el principio, intentando describir paso a paso, para la explotación utilizaremos Burpsuite:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528015746.png)
_Interceptamos una petición con la ventana proxy de burpsuite._

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528015930.png)
_Con CTRL+R enviamos la petición al repeater para mayor comodidad_

>Para descubrir el numero de columnas que nos retorna el panel utilizamos la inyección  "ORDER BY", que nos permite listar la cantidad de columnas existentes, en teoría, el numero exacto de columnas debería ser el anterior al que nos da un error:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528020727.png)
_Vemos que al inyectar "order by 100" la web nos devuelve un error, quiere decir que no es el numero correcto, lo mas optimo, seria probar desde el 1 hasta que obtengamos el primer error_

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528020943.png)
_Vemos que al inyectar "Order By 3" no recibimos error alguno_

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528021112.png)
_Pero, al inyectar "Order By 4" La pagina nos dirige a un error, es decir, que solamente son 3 columnas las que nos retorna el panel_

>Desde este punto se complica un poco, en general procederíamos con un "UNION SELECT 1,2,3", si el error nos devuelve uno de esos números, sabríamos que allí es donde iría la inyección (Si el error nos devuelve un dos, seguiríamos la inyección dentro de ese campo UNION SELECT 1,(Aquí seguiríamos inyectando),3).
>Pero, la web no nos lo permite:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528021827.png)
_Vemos por el código de estado 302 que se aplica una redirección, y la pagina no nos devuelve el error que necesitamos para seguir inyectando_

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528155455.png)
_Si lo intentamos con un operador OR al principio, si que nos devuelve un error, pero este no nos dice nada._

>Para este punto podríamos seguir inyectando con otra metodología de SQLI, como "Boolean Based" o "Time Based" que son bastante mas complejas, pero para no complicarnos tanto, vamos a generar un error en la consulta, para obligar a SQL a devolvernos información sensible.
>Es decir, no podemos proseguir con facilidad porque la web no nos devuelve un error en donde ver resultados, así que forzaremos uno en la Query.
>Para ello, usaremos la función de MariaDB "Updatexml" (También se puede abusar de funciones como extractvalue o name_const de la siguiente manera:

```sql
upatexml(1, concat(0x7e, (SELECT database())), 1)
```
_A la función updatexml le pasamos 3 parámetros, el primero (1) será un nodo XML inexistente, el segundo (concat(0x7e, (SELECT database()))) será la instrucción en si. La tilde (~ o %x7e en hexadecimal) se usa para romper la sintaxis XML y generar un error. Y el tercero (1) es una posición XPath_

>Al generar un error, la consulta nos retornara como parte del mensaje la instrucción de "concat()":

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528163320.png)
_La respuesta Users hace referencia a la base de datos actual (Utilizada por el panel de login)_

>Y Vemos que funciona :3, si queremos listar las demás bases de datos, lo podemos lograr con la siguiente inyección:

```sql
updatexml(1,concat(0x7e,(SELECT schema_name FROM information_schema.schemata)),1)-- -
```
_La forma de abusar de la función es la misma, solo que ahora, con la sintaxis propia de MariaDB, seleccionamos del information_schema (Esquema de información) el schema_name (Nombre de las bases de datos)

>Si lo aplicamos así:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528164500.png)
_Vemos que la web nos devuelve un error "Subquery returns more than 1 row" porque la respuesta de la Query tiene demasiadas filas, y por la manera en la que estamos realizando la inyección solamente podemos listar de a 1. Para ello, en la consulta aplicaremos un limite de respuestas_

```sql
updatexml(1,concat(0x7e,(SELECT schema_name FROM information_schema.schemata LIMIT 0,1)),1)-- -
```
_Con "LIMIT 0,1" obligamos a la consulta a devolver solamente la primera fila_

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528165133.png)
_La respuesta del panel, nos da un error con el nombre de la primera base de datos_

>Para listar las demás, vamos aumentando el primer numero (1.1, 2.1, 3.1) para optener filas diferentes de la misma respuesta:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528165440.png)
_Obtenemos la Base De Datos sys_
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528165458.png)
_Obtenemos la Base De Datos mysql_
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528165520.png)
_Obtenemos la Base De Datos performance_schema
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528165540.png)
_Obtenemos la Base De Datos Users

>Vemos que son 5 bases de datos en total, la mas prometedora es "Users", así que listaremos ahora las tablas de esa base de datos, para ello, la sintaxis de la inyección seria:

```sql
updatexml(1,concat(0x7e,(SELECT table_name FROM information_schema.tables WHERE table_schema='nombre de la base de datos' LIMIT 0,1)),1)-- -
```
_De esta manera intentamos obtener las tablas (table_name) del esquema de información de tablas (information_schema. Tables) donde el esquema de tablas (table_schema) es... Y de la misma manera, con LIMIT filtramos entre filas de la misma respuesta_

>Esto en la practica:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528170747.png)

>Parece que esta base de datos "Users" solamente tiene una tabla "usuarios", así que ahora vamos a listar las columnas de esta tabla:

```sql
updatexml(1,concat(0x7e,(SELECT column_name FROM information_schema.columns WHERE table_name='nombre de la tabla' LIMIT 0,1)),1)-- -
```
_seleccionamos las columnas (column_name) de el esquema de información de columnas (information_schema.columns) donde el nombre de la tabla (table_name) es... Con LIMIT, filtramos la respuesta entre filas_

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528171610.png)
_La Query nos devuelve la columna id_
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528171638.png)
_La Query nos devuelve la columna username_
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528171653.png)
_La Query nos devuelve la columna password_

>Vemos columnas muy interesantes ╰(*°▽°*)╯
>Para listar el contenido de las columnas usaremos la siguiente sintaxis:

```sql
updatexml(1,concat(0x7e,(SELECT 'nombre de la columba' FROM 'nombre de la tabla' LIMIT 0,1)),1)-- -
```
_Obtenemos la información de la columna de la tabla..._

>Como ya sabemos cual es la tabla y las columnas, podemos extraer la información completa parte por parte:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528172348.png)
_Obtenemos el usuario paco_
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528172409.png)
_Obtenemos el usuario pepe_
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528172440.png)
_Obtenemos el usuario juan_

>Ya con los usuarios, vamos a por la columna password:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528172630.png)
_Obtenemos la contraseña de paco_
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528172716.png)
_Obtenemos la contraseña de pepe_
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250528172738.png)
_Obtenemos la contraseña de juan_

>Y ya hemos explotado un SQL Injection basado en error manualmente :3
>Probamos los usuarios y las contraseñas en ssh:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250530143419.png)

>Lo primero que haremos al iniciar sesión como el usuario pepe por ssh, será realizar un tratamiento de la TTY para hacerla mas interactiva, y menos propensa a errores:

```bash
 script /dev/null -c bash
```
_Script solicita una PTY (Pseudo terminal) al kernel, luego, ejecuta en el proceso hijo que se crea, el comando que pasamos con la flag "-c", es decir una bash. Por ultimo, script no graba nada de la sesión al redirigirlo al /dev/null (Si no esta script disponible, puedes usar Python: python3 -c 'import pty; pty.spawn("/bin/bash")')._

>Ahora, con un CTRL+Z enviamos la Shell a segundo plano y desde nuestra terminal:

```bash
stty raw -echo; fg
```
1. _stty es la herramienta que nos ayudara a cambiar los parámetros de la terminal (eco, señales, etc.)
2. _raw es la flag que nos ayudara a desactivar el procesamiento de señales como CTRL+C (para que al hacerlo la Shell no muera) o CTRL+Z (para no poner en segundo plano la Shell por error)
3. _-echo Desactiva el echo del teclado, que nos puede dar problemas
4. _; fg (foreground) devuelve a primer plano nuestra querida Shell O.o

>Por ultimo vamos a establecer las variables de entorno correctas para una Shell totalmente funcional:

```bash
export TERM=xterm
export SHELL=/bin/bash
```
_Le estamos diciendo a la Shell que deseamos que la variable de entorno TERM (responsable de especificar el tipo de terminal usado), sea igual a Xterm.
Sí TERM está mal establecido en la máquina, cosas como clear, nano, vim, less, no funcionan correctamente. Y luego Establecemos /bin/bash como la Shell por defecto para que otras herramientas lo usen.

>Bien, en búsqueda de una escalada de privilegios, revisamos el directorio root en la raíz del sistema:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250530152307.png)

>Nos encontramos con un archivo pass.hash que tristemente no podemos listar:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250530152435.png)

>En búsqueda de mas vectores de entrada, listamos archivos SUID vulnerables en la maquina:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250530143958.png)
1. _find (comando de búsqueda en Linux)
2. _/ (búsqueda desde la raíz del sistema)
3. _-perm -4000 (Filtramos por archivos que tengan el permiso 4000 o SUID activado)
4. _2>/dev/null (redirige los errores o stder al agujero negro de Linux)

>Vemos que el Binario "Grep" es SUID, esto es critico, ya que "Grep" tiene la capacitad de leer archivos y mostrarlos por pantalla. Ya que lo podemos ejecutar como el usuario propietario (root), podemos leer prácticamente cualquier archivo sin tener en cuenta permisos... según [GTFOBins](https://gtfobins.github.io/gtfobins/grep/#suid).
>Vamos a ponerlo en practica:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250530144634.png)
_Grep toma la cadena vacía como "cualquier cosa" y devuelve todo el archivo /etc/shadow, que normalmente no tendríamos permitido listar_

>Ya que podemos listar archivos, intentamos leer el "pass.hash" que descubrimos antes:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250530152748.png)

>Nos llevamos el hash a nuestra maquina host y lo insertamos en un archivo .txt:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250530153043.png)

>Nos encontramos con una cadena de 32 dígitos hexadecimales que tienen toda la pinta de ser un hash MD5, para actuar con un poco mas de seguridad, pasamos el hash por herramientas que nos ayuden a identificarlo:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250530153645.png)

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250530153618.png)

>Vamos a intentar romper el hash con John:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250530153028.png)
_John reconoce el algoritmo de cifrado que le pasamos con la flag "--format=", así, va cifrando posibles contraseñas (que hay en el diccionario rockyou que le pasamos con la flag "--wordlist=") y comparando los hashes que generan con el real en busca de coincidencia.

>Así que bien, solo nos queda iniciar como usuario root:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250530154439.png)

>Y la maquina es nuestra :3


## Cadena de ataque detectada

- **Enumeration**: Apache, Connectivity check, HTTP, MariaDB / MySQL, Port enumeration, SSH, Web enumeration
- **Initial Access**: Login bypass, SQL Injection
- **Post Exploitation**: Credential extraction, Hash cracking, TTY stabilization
- **Privilege Escalation**: Hash cracking to root, SUID abuse, SUID binary abuse


## Tecnicas utilizadas

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Hash cracking](../../../techniques/hash-cracking.md)
- [Login bypass](../../../techniques/login-bypass.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [SQL Injection](../../../techniques/sql-injection.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [TTY stabilization](../../../techniques/tty-stabilization.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [Burp Suite](../../../tools/burp-suite.md)
- [find](../../../tools/find.md)
- [grep](../../../tools/grep.md)
- [GTFOBins](../../../tools/gtfobins.md)
- [John the Ripper](../../../tools/john-the-ripper.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [ssh](../../../tools/ssh.md)


## Servicios relacionados

- [Apache](../../../services/apache.md)
- [HTTP](../../../services/http.md)
- [MariaDB / MySQL](../../../services/mariadb-mysql.md)
- [SSH](../../../services/ssh.md)


## Vulnerabilidades relacionadas

- [Exposed error message](../../../vulnerabilities/exposed-error-message.md)
- [SUID misconfiguration](../../../vulnerabilities/suid-misconfiguration.md)
- [Unsanitized user input](../../../vulnerabilities/unsanitized-user-input.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [Hash cracking to root](../../../privilege_methods/hash-cracking-to-root.md)
- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

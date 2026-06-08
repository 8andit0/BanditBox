---
title: Vulnvault
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Vulnvault.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Vulnvault

## Resumen

Vulnvault combina CMS/web exploitation con LFI y RCE: la resolucion pasa por Joomla/PHP, aprovecha lectura o ejecucion desde la aplicacion y remata con revision de permisos SUID.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Vulnvault.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Vulnvault.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 22, 80 |
| Imagenes en fuente | 27 |
| Palabras en fuente | 2039 |
| Requiere revision | false |

## Resolucion paso a paso

>Vamos a por una maquina de dificultado "fácil" creada por "d1seo"

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531102806.png)

>Primero, levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531102845.png)

>Para comprobar la conexión con la maquina, enviamos unas cuantas trazas ICMP a la maquina victima con el comando Ping:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531103029.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, revisa las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse (Por lo general funciona para determinar el sistema operativo víctima)
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)

>Bien ya que vemos que los paquetes retornan y tenemos conexión con la maquina, empezamos el escaneo de puertos con Nmap:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531103220.png)
1. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
2. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
3.  _-Pn (Omite el descubrimiento de Host)_
4. _-n (no deseo que nmap haga una resolución DNS automática)
5. _-sVC (Aquí se concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_

>Nos encontramos con un servicio SSH corriendo por el puerto 22, y un servicio HTTP por el 80. Para obtener algo mas de información sobre las tecnologías que corren por el puerto 80, podemos utilizar whatweb:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531103601.png)
_Whatweb es una herramienta de reconocimiento web creada en Ruby, esta hecha para identificar tecnologías web (Es capaz de detectar Frameworks, plugins, CMS, etc).
Por lo general, mediante una petición GET, recolecta información de toda la respuesta (Cookies, código HTML, encabezados), para que luego, el motor de whatweb con REGEX (expresiones regulares) y sus propios plugins (scripts) de Ruby analicen la respuesta en búsqueda de particularidades propias de tecnologías (Como wp-content para WordPress, X-Powered-By para php o /templates/Joomla para Joomla).
Al encontrar coincidencias. usa sus propios plugins (scripts) de Ruby para identificar las tecnologías:
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506154219.png)_
_Para este escaneo en especial, usamos la flag "-a 3" para indicar un nivel 3 en agresividad (Bastante agresivo) y "-t 200" para indicar que deseamos 200 tareas en realización paralela (Para que el escaneo vaya un poco mas rápido)_

>Bien, la versión de apache que vemos no es vulnerable por si sola, así que vamos a la web, en búsqueda de mas información:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531104243.png)

>Nos encontramos con una pagina relativamente sencilla para generar reportes, con un campo para "Nombre del archivo" y otro para "Fecha".
>Al hacer un reporte, la pagina nos renderiza la información del mismo, incluyendo los campos que llenamos y la ruta donde son guardados en el directorio web:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531104929.png)
_En este reporte incluimos la comilla con el fin de testear un posible SQL. También, notamos que el panel de "Fecha" admite todo tipo de caracteres, así que probamos un posible XXS _

>Vemos que el panel parece "escapar" los caracteres especiales, vamos a probar concatenar comandos en la misma linea:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531105428.png)
_Testeamos concatenando comandos con la sintaxis básica en Linux para ello, separando comandos con un ";"_
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531105339.png)
_Recibimos como respuesta en la web la respuesta del comando whoami el usuario actual, y el listado de los archivos del directorio web, listados con el comando "ls -lah" _

>Vemos que ambos paneles son vulnerables ╰(*°▽°*)╯
>Mas tarde, analizaremos un poco por que la web permite algo así, por ahora, tenemos un RCE.
>Para convertir un "Remote Code Execution" a una intrusión directa al sistema (Obteniendo una revese Shell) Podemos utilizar varias técnicas (Como el envenenamiento de logs, o desde el RCE inyectar y envenenar archivos de la web). Hoy,  como primera medida, podemos listar los usuarios del sistema que se encuentran en el archivo /etc/passwd, para luego intentar obtener
> la clave privada de ssh de alguno:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531110221.png)
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531110259.png)

>Vemos el usuario "Samara", cullo directorio personal esta definido en "/home/Samara". Ya con esto vamos por su clave SSH privada, ubicada por defecto en el directorio oculto ".ssh":

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531121326.png)
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531121424.png)
_El archivo id_rsa es una clave privada codificada en base64 y cifrada por un algoritmo de cifrado asimétrico (RSA). Al iniciar sesión con ella, ssh la detecta y realiza una validación en el archivo de claves publicas ".ssh/authorized_keys", crea un bloque de datos aleatorio y lo cifra con la clave publica, si la clave privada id_rsa descifra ese bloque, podremos ingresar por ssh sin proporcionar contraseña. Puedes verlo como una analogía; la clave publica=.ssh/authorized_keys=cerradura crea un reto criptográfico que solo la clave privada=.ssh/id_rsa=llave puede descifrar.

>Así que podemos robar la clave privada de Samara. Procedemos copiándola a un archivo llamado id_rsa en nuestro directorio de trabajo:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531125601.png)

>Para que funcione, debemos modificar los permisos del archivo, con el fin de hacerlo "Mas Seguro":

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531125711.png)

>Ya con todo lo anterior, podemos suplantar a Samara e ingresar por ssh tranquilamente :3

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250531125844.png)

 >Primero, haremos un tratamiento de la TTY para una shell mas interactiva y menos problemática:

```bash
 script /dev/null -c bash
```
_Script solicita una PTY (Pseudo terminal) al kernel, luego, ejecuta en el proceso hijo que se crea, el comando que pasamos con la flag "-c", es decir una bash. Por ultimo, script no graba nada de la sesión al redirigirlo al /dev/null (Si no esta script disponible, puedes usar Python: python3 -c 'import pty; pty.spawn("/bin/bash")')._

>Ahora, con un CTRL+Z enviamos la Shell a segundo plano y desde nuestra terminal:

```bash
stty raw -echo; fg
```
1. _stty es la herramienta que nos ayudara a cambiar los parámetros de la terminal (eco, señales, etc.)
2. _raw es la flag que nos ayudara a desactivar el procesamiento de señales como CTRL+C (para que al hacerlo la shell no muera) o CTRL+Z (para no poner en segundo plano la shell por error)
3. _-echo Desactiva el echo del teclado, que nos puede dar problemas
4. _; fg (foreground) devuelve a primer plano nuestra querida Shell O.o

>Por ultimo vamos a establecer las variables de entorno correctas para una Shell totalmente funcional:

```bash
export TERM=xterm
export SHELL=/bin/bash
```
_Le estamos diciendo a la Shell que deseamos que la variable de entorno TERM (responsable de especificar el tipo de terminal usado), sea igual a Xterm.
Sí TERM está mal establecido en la máquina, cosas como clear, nano, vim, less, no funcionan correctamente. Y luego Establecemos /bin/bash como la Shell por defecto para que otras herramientas lo usen.

>Bien, para escalar privilegios, listaremos los procesos en ejecución en la maquina:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250601172111.png)
_Los procesos en Linux se encuentran organizados y diferenciados en las carpetas /proc/. Lo que hace el comando ps es buscar el directorio asociado a un proceso y extraer información del mismo._
_Es decir, busca el proceso --> /proc/PID_del_proceso, y lista su información existente sus directorios --> /proc/PID_del_proceso/status (para verificar su estado) o /proc/PID_del_proceso/cmdline (para verificar el comando ejecutado) o /proc/PID_del_proceso/meminfo (Para calcular su uso en memoria).
1. _"ps" es el comando en Linux que nos muestra información sobre los procesos en ejecución "Process status"_
2. _"a" nos muestra los procesos de todos los usuarios, no solo del propio_
3. _"u" nos permite ver mas información; como el usuario dueño de un proceso o el uso de memoria_
4. _"x" nos muestra todos los procesos que operan por separado de la terminal; como demonios o servicios en segundo plano._

>Vemos que el usuario "Root" ejecuta con el binario /bin/bash el script /usr/local/bin/echo.sh. Para verificar que lo ejecuta de manera cíclica, podemos usar la herramienta watch para monitorizar el proceso:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250601174900.png)
1. _watch es una utilidad en Linux que nos permite ejecutar repetidamente un comando en intervalos de tiempo, puedes verlo como un bucle por tiempo de un comando_
2. _-n 1 es la flag que nos permite determinar el intervalo de actualización del comando, en este caso, deseamos que cada segundo se ejecute nuevamente.
3. _"ps aux | grep echo.sh" es el comando que deseamos ejecutar de manera cíclica (En este caso agregamos "grep echo.sh" para filtrar solamente por el proceso de nuestro interés) _

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250601174914.png)
_Vemos que el proceso de root aparece y desaparece, lo que quiere decir que se esta lanzando a intervalos_

>Vamos a listar permisos del archivo ejecutado, si podemos sobrescribirlo, podemos ejecutar comandos como usuario ROOT

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250601175807.png)

>Y vemos que si que tenemos permisos de escritura sobre el archivo, así que, sin mas, lo abrimos con nano y inyectamos un comando malicioso:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250601180241.png)
_Vemos que el archivo original lo que hacia era introducir la cadena "No tienes permitido  estar  aquí   :(" a un archivo .txt_

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250601180400.png)
_Simplemente inyectamos un nuevo comando, en este caso estamos convirtiendo el binario /bin/bash en SUID, esto, lo definirá como "BINARIO UNICAMENTE EJECUTADO COMO SU PROPIETARIO", es decir, que al ejecutar un /bin/bash siempre se ejecutara como ROOT_

>Este comando será ejecutado por ROOT y tendremos posibilidades de obtener una bin/bash privilegiada con un simple comando, para saber si se ejecuto correctamente, revisaremos los Binario SUID del sistema:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250601180723.png)
1. Con el comando “find” Buscamos archivos
2. Con “/” especificamos que sea desde el directorio raíz
3. “-perm -4000” para especificar que queremos listar solamente archivos con el bit SUID
4. “2>/dev/null” para enviar los errores al agujero negro de Linux (que no se muestren en pantalla)

>Y si que se ha ejecutado correctamente :3
>Ahora solo nos queda abrir una /bin/bash de manera privilegiada:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250601180957.png)

>Pero, antes de borrar todos los archivos del sistema, veamos por que el panel de la web, era vulnerable.
>La web se encuentra en el directorio /var/www/html por defecto, nos dirigimos allí, y abrimos el index.php, que era el archivo que nos permitió la ejecución de comandos:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250601182315.png)

>Examinando un poco el código de index.php, encontramos la zona vulnerable:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250601182254.png)

>En la zona de abajo, se construye el comando con el input del usuario (Lo que insertamos en hora y fecha). Aunque se usa la función "escapeshellcmd" para intentar escapar los caracteres especiales (Con la intención de sanitizar un poco el input), esta misma no funciona bien con los parámetros entre comillas dobles como "$ nombre" o "$ fecha".
>Por eso, al insertar un nuevo comando separado por ";" no es bien sanitizado, y la variable "Comando" termina conteniendo algo así:

```bash
generate_report --name "reporte1; id" --date "22/02/2024; whoami"
```
_Inyectamos el comando id con el campo reporte y el comando whoami con en el campo fecha_

>La ultima función llamada "shell_exec" ejecuta TODO tomado ";" como separador entre comandos (el punto y coma ";" SIEMPRE se interpreta fuera del contexto del argumento, aunque este dentro de comillas dobles). Es decir, se interpretan 3 comandos, en vez de 1, y las respuestas se almacenan en la variable $output.
>Al confiar en el input de usuario, el código permite concatenar comandos con facilidad.
>Ahora si, ya terminamos con la maquina :3


## Cadena de ataque detectada

- **Enumeration**: Apache, Connectivity check, HTTP, Joomla, PHP, Port enumeration, SSH, Web enumeration
- **Initial Access**: CMS exploitation, Local File Inclusion, Remote Code Execution
- **Post Exploitation**: Credential extraction, TTY stabilization
- **Privilege Escalation**: SUID abuse, SUID binary abuse


## Tecnicas utilizadas

- [CMS exploitation](../../../techniques/cms-exploitation.md)
- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Local File Inclusion](../../../techniques/lfi.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Remote Code Execution](../../../techniques/rce.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [TTY stabilization](../../../techniques/tty-stabilization.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [base64](../../../tools/base64.md)
- [grep](../../../tools/grep.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [Ruby](../../../tools/ruby.md)
- [ssh](../../../tools/ssh.md)
- [WhatWeb](../../../tools/whatweb.md)


## Servicios relacionados

- [Apache](../../../services/apache.md)
- [HTTP](../../../services/http.md)
- [Joomla](../../../services/joomla.md)
- [PHP](../../../services/php.md)
- [SSH](../../../services/ssh.md)


## Vulnerabilidades relacionadas

- [Exposed error message](../../../vulnerabilities/exposed-error-message.md)
- [Insecure file upload](../../../vulnerabilities/insecure-file-upload.md)
- [SUID misconfiguration](../../../vulnerabilities/suid-misconfiguration.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

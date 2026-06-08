---
title: SecretJenkins
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/SecretJenkins.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# SecretJenkins

## Resumen

SecretJenkins relaciona Jenkins/Tomcat con enumeracion web: el writeup busca rutas y secretos expuestos, prueba credenciales y documenta como una mala exposicion de servicios permite avanzar hacia una shell.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/SecretJenkins.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/SecretJenkins.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 22, 8080 |
| Imagenes en fuente | 26 |
| Palabras en fuente | 2105 |
| Requiere revision | false |

## Resolucion paso a paso

>Hoy vamos con una maquina de dificultad fácil bastante interesante :3

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250521172822.png)

>Primero, levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250521172936.png)

>Ya habiendo levantado la maquina, vamos a probar la conexión que tenemos con ella, con el comando ping:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250521173107.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, revisa las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse (Por lo general funciona para determinar el sistema operativo víctima)
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)

>Escaneamos la IP con "nmap" para determinar puertos abiertos, sus servicios y versiones:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250521173304.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sVC (Aquí se concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_

>Bien, vemos un servicio ssh corriendo por el puerto 22, y un servicio Jetty en su versión 10.0.18 corriendo por el puerto 8080
>Jetty, es un servidor web creado en Java que sirve a aplicaciones web de la misma tecnología. Aunque esta versión 10.0.18 no es vulnerable a nada en si, no esta de mas escanear un poco mas las tecnologías del puerto 8080, para ello, usaremos "Whatweb":

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250521174117.png)
_Whatweb es una herramienta de reconocimiento web creada en Ruby, esta hecha para identificar tecnologías web (Es capaz de detectar Frameworks, plugins, CMS, etc).
Por lo general, mediante una petición GET, recolecta información de toda la respuesta (Cookies, código HTML, encabezados), para que luego, el motor de whatweb con REGEX (expresiones regulares) y sus propios plugins (scripts) de Ruby analicen la respuesta en búsqueda de particularidades propias de tecnologías (Como wp-content para WordPress, X-Powered-By para php o /templates/Joomla para Joomla).
Al encontrar coincidencias. usa sus propios plugins (scripts) de Ruby para identificar las tecnologías:
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506154219.png)_
_En este caso, usamos el parámetro -t para determinar un numero máximo de 200 hilos para el escaneo, lo que lo hará mas rápido, y usamos -a para determinar el grado 3 de agresividad (bastante agresivo)_

>Nos encontramos con la tecnología Jenkins en su versión 2.441.
>Es, en síntesis, un servidor de automatización de código abierto que corre dentro de "Jetty". Procedemos a buscar exploits para esa versión en especial:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250521175030.png)
_Searchsploit es una herramienta de terminal que filtra y busca entre todos los exploits que se encuentran en ExploitDB [[https://www.exploit-db.com/]]_. _En el paquete preinstalado en Kali "ExploitDB" existe un archivo files_exploits.csv en donde se encuentran los metadatos de TODOS los exploits.
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250504142751.png)
La herramienta Searchsploit filtra por todos ellos buscando coincidencias por sistema operativo, descripción o nombre del servicio, hasta encontrar una coincidencia para una vulnerabilidad que estemos buscando.

>Así que es una versión vulnerable a LFI, traeremos el exploit a nuestro directorio de trabajo:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250521175405.png)
Con el parámetro -m (mirror) creamos una copia en el directorio de trabajo actual del exploit que deseamos. Searchsploit copia este archivo desde una ruta en particular del sistema en la que se almacenan los exploits del paquete "ExploitDB" _
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250504143519.png)

>Ya con el exploit, analizamos un poco su código.

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250521175658.png)

>Intentando resumirlo mucho, el script envía una petición http al "/cli" de la web vulnerable haciéndose pasar por el cliente real para java (jenkins-cli.jar). Desde la petición envía un argumento envenenado en binario por POST que explota la vulnerabilidad de LFI, para luego recibir el contenido, parsearlo, y mostrarlo por pantalla.
>El exploit en realidad es bastante complejo, podemos usarlo con facilidad para llegar a un LFI, pero, como nos encanta complicarnos, vamos a intentar explotarlo manualmente ╰(*°▽°*)╯

>Primero, debemos entender bien la vulnerabilidad para poder explotarle manualmente... Intentemos las 2 cosas a la vez :3

>Jenkins tiene una función particular. Su cliente "CLI" esta diseñado para automatizar tareas y ser usado por administradores, permitiéndonos mediante su herramienta (Jenkins-cli.jar) ejecutar algunos trabajos como gestionar nodos y demás cosas:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522002039.png)
_Como puedes ver, el directorio /cli/ nos es accesible aun sin estar autenticados, y allí se explica como utilizar su cliente desde la terminal_

>Así que nos traemos Jenkins-cli.jar a nuestro entorno de trabajo descargándolo desde la misma web (En el directorio /jnlpJars/jenkins-cli.jar).
>En configuraciones por defecto algunos comandos CLI (o todos) no requieren autorización estricta, es decir, aun sin tener las claves de Jenkins, podemos "jugar" con CLI libremente:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522002958.png)
_Aquí puedes ver el uso básico de CLI, aplicando el comando help, listamos todos los comandos CLI que podemos utilizar_

>Entonces bien, en este punto ya llegamos al fallo critico.
>Jenkins interpreta toda ruta empezada por "@" como eso mismo, una ruta, no un string. Esta misma es una función normal, el problema radica en que algunos comandos CLI no sanitizan correctamente los argumentos que empiezan por "@".
>Quiere decir que si un comando CLI nos permite pasar como argumento @/etc/passwd, Jenkins lo tomara como una ruta a un archivo, lo leerá y devolverá su contenido:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522003847.png)
_En este caso usamos el comando CLI console, al pasarle la ruta de un archivo, podemos ver en la respuesta que lo lee y devuelve como tal.
Mas comandos que te servirían para lo mismo son install-plugin, reload-configuration, groovy, help ..._

>Bien, ya sabemos que Jenkins interpreta las rutas y nos las devuelve con facilidad, también sabemos como hacer que pase, pero hay un pequeño problema, no podemos ver todo el archivo.
>Jenkins intenta interpretar el contenido de @/etc/passwd como un parámetro, como no es valido, solo nos devuelve partes del archivo. Como casi todos los comandos CLI no están hechos para interpretar archivos, devuelven solamente errores con lo que se intento interpretar como argumento de cada archivo.
>Ahí es donde entra el comando "Connect-node" (Que usa el script de Python que vimos antes).
>Este comando puede aceptar nombres de nodos como argumentos, y cuando le pasamos un archivo, este intentara parsear cada linea como el nombre de un nodo. Como ninguna linea del @/etc/passwd no son nodos, Jenkins genera un error PERO POR CADA LINEA :3, así, tendríamos nuestro output completo, solo que un tanto corrompido:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522005631.png)

>Ya en este punto, tenemos un LFI :3, solo nos falta parsear la información que obtenemos de un archivo. Para ello podemos usar grep para tomar solamente lo que se encuentra entre comillas de cada respuesta:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522015303.png)
1. _Como la respuesta de Jenkins son errores (stder), no es posible realizar un tratamiento eficiente de la respuesta, para solucionarlo, con "2>$1" direccionamos el stder cuyo referente es el 2, al stdout (respuesta común) cuyo referente es el 1_
2. _grep es el comando filtrador por excelencia en Linux
3. _con el paramento -o indicamos que filtraremos resultados con "expresiones regulares"_
4. '"[^"]*"' es una expresión regular que coincide con cualquier texto entre comillas dobles.

>Bien, vemos dos usuarios; pingüinito y Bobby, ya que el puerto 22 esta abierto, podemos intentar un ataque de fuerza bruta para encontrar las contraseñas:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522024224.png)
1. _-l (este parámetro se usa para determinar el usuario que ya tenemos, si no tenemos un usuario, al colocar “-L” podemos incluir una wordlist para atacarlos también)_
2. _-P (para determinar, una wordlist con posibles contraseñas, si tuviéramos una contraseña y quisiéramos probar usuarios, en este punto colocamos “-p” y la contraseña)_
3. _ssh:// (para determinar el servicio a atacar)
4. _-t (indico que deseo emplear 64 hilos, para agilizar el escaneo)_

>Bien, tenemos una contraseña, ya podremos entrar a la maquina por ssh:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522024455.png)

 >Primero, haremos un tratamiento de la TTY para una shell mas interactiva y menos problemática, primero:

```bash
 script /dev/null -c bash
```
_Script solicita una PTY (Pseudo terminal) al kernel, luego, ejecuta en el proceso hijo que se crea, el comando que pasamos con la flag "-c", es decir una bash. Por ultimo, script no graba nada de la sesión al redirigirlo al /dev/null (Si no esta script disponible, puedes usar Python: python3 -c 'import pty; pty.spawn("/bin/bash")')._

>Ahora, con un CTRL+Z enviamos la Reverse Shell a segundo plano y desde nuestra terminal:

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

>Ya con una Shell interactiva, listaremos privilegios para determinar si tenemos permisos sobre algún binario en especial:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522024912.png)
_Ejecutamos el binario setuid (que siempre se ejecuta como root)“SUDO”, con la flag “-l”. El binario busca los privilegios que el usuario actual tiene descritos en el archivo /etc/sudoers y los muestra por pantalla (Si aplica)_
1. _(pingüinito) Permite ejecutar el binario como si fuéramos el usuario pingüinito_
2. _NOPASSWD Nos indica que no es necesario ingresar contraseña para ejecutar el binario_
3. _/usr/bin/python3 Binario sobre el que tenemos privilegios (cuya ruta está definida arriba en “secure_path”_

>Vemos que podemos ejecutar como el usuario "pingüinito" el binario Python3, al correrlo como root y usar una librería que nos permita ejecutar comandos (como sys, subprosess, os), estos mismos se ejecutarán con el contexto de pingüinito.

>En la practica:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522025533.png)
_Ejecutamos el binario “sudo” con la flag “-u” para indicar el usuario con el cual queremos ejecutar el comando, de allí nos abrimos el intérprete de Python; Importando la librería “os”(import os), abrimos un proceso hijo, y en este mismo se ejecuta una bash con el contexto de root (os.system(“bin/bash”))_

>Ya siendo "Pingüinito"  listamos privilegios ahora para este usuario:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522025715.png)

>Podemos ejecutar como root el script /opt/script.py con el binario /usr/bin/python3

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522030231.png)

>Con el script no podemos hacer mucho, pero, al listar privilegios el la carpeta opt:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522030346.png)

>Vemos que tenemos Permisos sobre el directorio, siendo así, para escalar privilegios solo tenemos que eliminar el script original (ya que tenemos permiso para ello) y remplazarlo por uno infectado.

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522030620.png)
_Con "rm" eliminamos el archivo original_

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522030905.png)
_Importamos la librería "os", con ella desde el sistema ejecutamos una /bin/bash, y todo esto lo enviamos a un nuevo archivo script.py

>Ya que al ejecutar el script lo hacemos como usuario root, el proceso hijo de "/bin/bash" tendrá el contexto de aquel usuario:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522030954.png)

>La maquina es toda nuestra  :3


## Cadena de ataque detectada

- **Enumeration**: Connectivity check, HTTP, Jenkins, Joomla, Metadata analysis, PHP, Port enumeration, SSH, Tomcat, Web enumeration
- **Initial Access**: Brute force, CMS exploitation, Local File Inclusion, Malicious file upload
- **Post Exploitation**: Credential extraction, TTY stabilization


## Tecnicas utilizadas

- [Brute force](../../../techniques/brute-force.md)
- [CMS exploitation](../../../techniques/cms-exploitation.md)
- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Local File Inclusion](../../../techniques/lfi.md)
- [Malicious file upload](../../../techniques/malicious-file-upload.md)
- [Metadata analysis](../../../techniques/metadata-analysis.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [TTY stabilization](../../../techniques/tty-stabilization.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [grep](../../../tools/grep.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [Ruby](../../../tools/ruby.md)
- [Searchsploit](../../../tools/searchsploit.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)
- [WhatWeb](../../../tools/whatweb.md)


## Servicios relacionados

- [HTTP](../../../services/http.md)
- [Jenkins](../../../services/jenkins.md)
- [Joomla](../../../services/joomla.md)
- [PHP](../../../services/php.md)
- [SSH](../../../services/ssh.md)
- [Tomcat](../../../services/tomcat.md)


## Vulnerabilidades relacionadas

- [Exposed error message](../../../vulnerabilities/exposed-error-message.md)
- [Insecure file upload](../../../vulnerabilities/insecure-file-upload.md)
- [Secret in metadata](../../../vulnerabilities/secret-in-metadata.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- Sin relaciones confirmadas en el contenido actual.

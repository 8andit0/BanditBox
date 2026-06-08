---
title: Pequeñas mentirosas
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Pequeñas_mentirosas.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Pequeñas mentirosas

## Resumen

Pequenas mentirosas es una ruta clasica de acceso por credenciales: enumera web y SSH, prueba fuerza bruta controlada y despues revisa binarios SUID para convertir el acceso inicial en privilegios elevados.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Pequeñas_mentirosas.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Peque%C3%B1as_mentirosas.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 22, 80 |
| Imagenes en fuente | 18 |
| Palabras en fuente | 1034 |
| Requiere revision | false |

## Resolucion paso a paso

>Bien, hoy vamos con una maquinita de dificultad fácil para pulir habilidades...

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas.png)

>Primero, levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%201.png)

>Verificamos la conexión con la dirección ip a vulnerar con unas tramas ICMP:

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%202.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, verifica las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)_

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,_
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse(Por lo general funciona para determinar el sistema operativo víctima)._
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)_

>Una vez verificamos conexión con la máquina, realizamos una escaneo fuerte con nmap para enumerar puertos abiertos y servicios:

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%203.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sVC (Aquí se concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_

>Con todo lo anterior, notamos que en el puerto 22 corre una versión relativamente antigua de OpenSSH, y en el puerto 80 una versión medianamente actual de Apache.

>Terminamos con el reconocimiento haciendo una pequeña enumeración a las tecnologías que corren en el servidor web, escaneo que no nos da mucha info :(

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%204.png)

>Así que, vamos a ver el servidor web…

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%205.png)
![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%206.png)

>Una pequeña y muy bien escondida pista nos da un posible nombre de usuario “a”. En realidad después de enumerar directorios no encontramos nada más en el servicio web, así que, pasamos a la fuerza bruta:

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%207.png)
1. _-l (este parámetro se usa para determinar el usuario que ya tenemos. Si no hubiéramos tenido un usuario, al colocar “-L” podemos incluir una Wordlist para atacarlos también)_
2. _-P (para determinar, una Wordlist con posibles contraseñas, si tuviéramos una contraseña y quisiéramos probar usuarios, en este punto colocamos “-p” y la contraseña)_
3. _ssh:// (para determinar el servicio a atacar, puede ser http// o ftp:// )
4. _-t (indico que deseo emplear 64 hilos (El máximo de Hydra), para agilizar el escaneo)_

>No nos toma mucho tiempo descubrir la contraseña. Intentamos ingresar por ssh con las nuevas credenciales:

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%208.png)

>Primero le indicamos a la Shell que la variable de entorno TERM debe establecerse en xterm:

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%209.png)
_Aquí, le estamos diciendo a la shell que deseamos que la variable de entorno (responsable de especificar el tipo de terminal usado) TERM, sea igual a Xterm._
_Sí TERM no se establece o está mal establecido en la máquina, cosas como clear, nano, vim, less, no funcionan correctamente (Es para tener una experiencia un poco más funcional)._

>Luego de esto, intentamos listar privilegios del usuario:

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%2010.png)
_Ejecutamos el binario setuid (que siempre se ejecuta como root)“SUDO”, con la flag “-l”. El binario busca los privilegios que el usuario actual tiene descritos en el archivo /etc/sudoers y los muestra por pantalla (Si aplica)._

>Tristemente, no podemos listar privilegios como usuario “a”, pero, buscando un poco más, encontramos al usuario “Spencer”

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%2011.png)
![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%2012.png)

>Al no ver otra manera de escalada de privilegios, realizamos otra fuerza bruta, pero ahora para el usuario “Spencer”

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%2013.png)

>Encontramos su super contraseña, así que cambiamos de usuario para ver si este otro si cuenta con privilegios de ejecución de algún archivo:

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%2014.png)
_Se ejecuta “su” para realizar un cambio de identidad, “su” llama a una función del sistema (setuid) para cambiar el UserID y el GroupID al del usuario de destino, para finalmente lanzar una nueva shell como el usuario spencer._

>Ahora que somos “Spencer” podemos intentar listar privilegios nuevamente:

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%2015.png)
1. _(ALL) Permite ejecutar el binario como CUALQUIER usuario, incluido claro, el mas privilegiado_
2. _NOPASSWD Nos indica que no es necesario ingresar contraseña para ejecutar el binario_
3. _/usr/bin/python3 Binario sobre el que tenemos privilegios (cuya ruta está definida arriba en “secure_path”)_

>En pocas palabras, podemos ejecutar Python3 como root. Esto es crítico, ya que Python es un lenguaje bastante potente que nos permite interactuar con el sistema operativo a bajo nivel. Al ejecutarlo como root y usar una librería que nos permita ejecutar comandos (como sys, subprocess, os), estos mismos se ejecutarán con el contexto de root.

>Aquí te dejo la biblia de la escalada de privilegios: ([https://gtfobins.github.io/gtfobins/python/](https://gtfobins.github.io/gtfobins/python/) )

>Así bien:

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%2016.png)
_Ejecutamos el binario “sudo” con la flag “-u” para indicar el usuario con el cual queremos ejecutar el comando, de allí nos abrimos el intérprete de Python; Importando la librería “os”(import os), abrimos un proceso hijo, y en este mismo se ejecuta una bash con el contexto de root (os.system(“bin/bash”))_

![Pequeñas_mentirosas](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Peque%C3%B1as_mentirosas%2017.png)

>Y la maquinita es nuestra :)

_/O.O   //El comando "rm -rf /*" ejecutado como administrador borra todos los archivos del sistema, es un pequeño guiño al ganar acceso como root a una máquina, NO LO EJECUTES//   O.O


## Cadena de ataque detectada

- **Enumeration**: Apache, Connectivity check, FTP, HTTP, Port enumeration, SSH, Web enumeration
- **Initial Access**: Brute force
- **Post Exploitation**: Credential extraction
- **Privilege Escalation**: SUID abuse, SUID binary abuse


## Tecnicas utilizadas

- [Brute force](../../../techniques/brute-force.md)
- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [GTFOBins](../../../tools/gtfobins.md)
- [Hydra](../../../tools/hydra.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)


## Servicios relacionados

- [Apache](../../../services/apache.md)
- [FTP](../../../services/ftp.md)
- [HTTP](../../../services/http.md)
- [SSH](../../../services/ssh.md)


## Vulnerabilidades relacionadas

- [SUID misconfiguration](../../../vulnerabilities/suid-misconfiguration.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

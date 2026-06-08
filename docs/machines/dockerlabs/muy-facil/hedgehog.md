---
title: HedgeHog
node_type: machine
platform: dockerlabs
difficulty: muy-facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Muy Faciles/HedgeHog.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# HedgeHog

## Resumen

HedgeHog plantea una trampa sencilla alrededor de web y SSH: tras enumerar HTTP, se recuperan credenciales o usuarios y se escala mediante reglas sudo mal acotadas.

Fuente original: [Maquinas De Dockerlabs/Maquinas Muy Faciles/HedgeHog.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Muy%20Faciles/HedgeHog.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | muy-facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 80 |
| Imagenes en fuente | 11 |
| Palabras en fuente | 573 |
| Requiere revision | false |

## Resolucion paso a paso

**MAQUINA HEDGEHOG(DockerLabs)**

>Bien, hoy tenemos una maquina sencilla de DockerLabs que tiene su trampa… Empezamos como siempre:

![HedgeHog](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/HedgeHog.png)
_Al hacer un Ping a La ip vulnerable, vemos que tenemos conexión a ella, y por el “ttl” que nos muestra el comando ping, notamos que nos enfrentamos a una máquina Linux.
(El valor “ttl” o “Time To Live” Nos informa cuántos saltos tiene permitido dar un paquete antes de llegar nuevamente a nosotros, esto es "único" entre sistemas operativos, siendo así, con este valor se puede determinar tanto el sistema operativo “Linux si son 64”, como los saltos de los paquetes en la red)

>Así que bien, vamos a hacer un escaneo fuerte:

![HedgeHog](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/HedgeHog%201.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sV (realiza un reconocimiento de versiones de servicios)_

>Vemos que tiene el puerto 80 y el 22 abiertos, con servicios en versiones relativamente actualizadas, al inspeccionar un poco la red, nos encontramos con casi nada:

![HedgeHog](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/HedgeHog%202.png)

>Se inspecciona el código fuente, y nada :(, se buscan subdirectorios y nada :(

![HedgeHog](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/HedgeHog%203.png)

>Se buscan archivos, y nada :(

![HedgeHog](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/HedgeHog%204.png)

>De allí, solamente nos queda intentar romper el servicio ssh con fuerza bruta, tal vez con el usuario "tail", encontrado en la web. Pero después de 2 días haciendo fuerza bruta, fue necesario hacer un poco de trampa, y ver un write up :(

>Resulta que hay un pequeño truco en la fuerza bruta, debemos hacer un tratamiento al diccionario "rockyou" que por lo general se usa para hacer fuerza bruta:

![HedgeHog](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/HedgeHog%205.png)
_El comando TAC lo usamos para darle la vuelta al diccionario_
_Con el comando sed (-i para aplicar los cambios en el archivo en sí, y no mostrarlos por pantalla) cambiamos los espacios / / por nada //._

>Ahora si, y por fin:

![HedgeHog](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/HedgeHog%206.png)
1. _-l (este parámetro se usa determinar el usuario que ya tenemos, si no tuviésemos un usuario, al colocar “-L” podemos incluir una wordlist para probar aplicar fuerza bruta también allí)_
2. _-P (para determinar, una wordlist con posibles contraseñas, si tuviéramos una contraseña y quisiéramos probar usuarios, en este punto colocamos “-p” y la contraseña)_
3. _ssh:// (para determinar el servicio a atacar, puede ser http// o ftp:// )

>Ingresamos por ssh con el usuario y la contraseña encontrados:

![HedgeHog](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/HedgeHog%207.png)

>Con el Comando sudo -l listaremos los permisos que tenemos sobre archivos del sistema (permisos que el comando “sudo” lee del /etc/sudoers)

![HedgeHog](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/HedgeHog%208.png)
>Vemos que podemos pivotar al usuario Sonic sin contraseña
>Una vez nos abrimos una bash con el usuario Sonic, listamos permisos nuevamente, y nos encontramos con que podemos escalar privilegios sin contraseña, así que:

![HedgeHog](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/HedgeHog%209.png)

>O, también podemos desde el principio:

![HedgeHog](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/HedgeHog%2010.png)

O.O   //El comando "rm -rf /*" ejecutado como administrador borra todos los archivos del sistema, es un pequeño guiño al ganar acceso como root a una máquina, NO LO EJECUTES//   O.O


## Cadena de ataque detectada

- **Enumeration**: Connectivity check, FTP, HTTP, Port enumeration, SSH, Web enumeration
- **Initial Access**: Brute force
- **Post Exploitation**: Credential extraction
- **Privilege Escalation**: sudo abuse, sudo binary abuse


## Tecnicas utilizadas

- [Brute force](../../../techniques/brute-force.md)
- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [sudo abuse](../../../techniques/sudo-abuse.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)


## Servicios relacionados

- [FTP](../../../services/ftp.md)
- [HTTP](../../../services/http.md)
- [SSH](../../../services/ssh.md)


## Vulnerabilidades relacionadas

- [sudo misconfiguration](../../../vulnerabilities/sudo-misconfiguration.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [sudo binary abuse](../../../privilege_methods/sudo-binary-abuse.md)

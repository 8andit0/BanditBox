---
title: FirstHacking
node_type: machine
platform: dockerlabs
difficulty: muy-facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Muy Faciles/FirstHacking.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# FirstHacking

## Resumen

FirstHacking es una introduccion a enumeracion de FTP y servicios simples: el writeup identifica puertos relevantes, reconoce versiones y aprovecha el comportamiento del servicio para obtener acceso.

Fuente original: [Maquinas De Dockerlabs/Maquinas Muy Faciles/FirstHacking.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Muy%20Faciles/FirstHacking.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | muy-facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 21, 6200 |
| Imagenes en fuente | 10 |
| Palabras en fuente | 611 |
| Requiere revision | false |

## Resolucion paso a paso

>Hoy tenemos la maquina FirstHacking, bastante, BASTANTE simple, pero muy interesante
   en su esencia…
>Empezamos por levantar la maquina:

![FirstHacking](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/FirstHacking.png)

>Ahora, hacemos un escaneo de puertos con nmap:

![FirstHacking](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/FirstHacking%201.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (omite el descubrimiento de Host)_
5. _-sV (realiza un reconocimiento de versiones de servicios)_

>Particularmente, notamos que solamente hay un servicio FTP corriendo en el puerto 21, con una versión un tanto desactualizada del servicio Vsftpd
>Searchsploit nos indica que la versión es vulnerable:

![FirstHacking](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/FirstHacking%202.png)
_Searchsploit es una herramienta de terminal que filtra y busca entre todos los exploits que se encuentran en [*ExploitDB*](https://www.exploit-db.com/). _En el paquete preinstalado en kali "exploitdb" existe un archivo files_exploits.csv en donde se encuentran los metadatos de TODOS los exploits.
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250504142751.png)
La herramienta "Searchsploit" filtra por todos ellos buscando coincidencias por sistema operativo, descripción o nombre del servicio, hasta encontrar una coincidencia para una vulnerabilidad que estemos buscando._

>Así que, vamos a traernos ese exploit al directorio actual de trabajo:

![FirstHacking](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/FirstHacking%203.png)
_Con el parámetro -m (mirror) creamos una copia en el directorio de trabajo actual del exploit que deseamos. Searchsploit copia este archivo desde una ruta en particular del sistema en la que se almacenan los exploits del paquete "ExploitDB" _
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250504143519.png)

>Con un poco de ayuda, logramos interpretar el código dentro del exploit, bastante sencillo en realidad.

>Luego de investigar un poco, en síntesis, Esta versión del servicio (vsftpd 2.3.4.) fue crackeada, y el servicio infectado se esparció con rapidez, en él, un Cracker inserto al código fuente un backdoor, así cuando un usuario se intenta autenticar con cualquier nombre y una carita feliz, se abrirá el puerto 6200 de la máquina, que otorga una /bin/sh a quien se conecte.

_Si quieres entender un poco más de este hackeo aquí te dejo un poco de lo mejor que encontré (_[_https://github.com/puckiestyle/exploit-CVE-2011-2523_](https://github.com/puckiestyle/exploit-CVE-2011-2523)

_Este repositorio que contiene la versión Infectada del código fuente de Vsftpd.), (_[_https://seclists.org/oss-sec/2011/q3/119_](https://seclists.org/oss-sec/2011/q3/119)


>Bien, vamos a explotarlo manualmente, para que sea más interesante, primero, nos intentamos autenticar, puede ser con Telnet, ftp o nc:

![FirstHacking](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/FirstHacking%204.png)

>El usuario que insertamos puede ser cualquiera, pero, para activar el backdoor debe tener al final una carita feliz :)

>Por otro lado la contraseña puede ser cualquiera.

>Si analizamos el puerto 6200 nuevamente, nos encontramos con que ahora está abierto

![FirstHacking](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/FirstHacking%205.png)

>Ya solo queda conectarnos con nc por ese mismo puerto, como el servicio Vsftpd corre con privilegios de root, la Shell que obtenemos tiene privilegios máximos

![FirstHacking](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/FirstHacking%206.png)

>También lo puedes lograr solo con el one liner:

```bash
printf “USER bandit:)\r\nPASS pass\r\n” | nc 172.17.0.2 && sleep 1 && nc 172.17.0.2 6200
```
_Funciona 1 de cada 3 veces :(

![FirstHacking](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/FirstHacking%207.png)
O.O   //El comando "rm -rf /*" ejecutado como administrador borra todos los archivos del sistema, es un pequeño guiño al ganar acceso como root a una máquina, NO LO EJECUTES//   O.O


## Cadena de ataque detectada

- **Enumeration**: FTP, Metadata analysis, Port enumeration, Web enumeration
- **Post Exploitation**: Credential extraction


## Tecnicas utilizadas

- [Credential extraction](../../../techniques/credential-extraction.md)
- [Metadata analysis](../../../techniques/metadata-analysis.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [Netcat](../../../tools/netcat.md)
- [Nmap](../../../tools/nmap.md)
- [Searchsploit](../../../tools/searchsploit.md)


## Servicios relacionados

- [FTP](../../../services/ftp.md)


## Vulnerabilidades relacionadas

- [Secret in metadata](../../../vulnerabilities/secret-in-metadata.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- Sin relaciones confirmadas en el contenido actual.

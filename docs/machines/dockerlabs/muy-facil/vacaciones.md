---
title: Vacaciones
node_type: machine
platform: dockerlabs
difficulty: muy-facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Muy Faciles/Vacaciones.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Vacaciones

## Resumen

Vacaciones trabaja una ruta corta de web a SSH: se enumeran puertos 22/80, se obtiene informacion util desde HTTP y se valida una escalada local por sudo o SUID.

Fuente original: [Maquinas De Dockerlabs/Maquinas Muy Faciles/Vacaciones.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Muy%20Faciles/Vacaciones.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | muy-facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 22, 80 |
| Imagenes en fuente | 12 |
| Palabras en fuente | 361 |
| Requiere revision | false |

## Resolucion paso a paso

---
>Hoy, una maquina muy muy facilita, vamos allá...

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Vacaciones.png)

>Primero desplegamos la maquina

![Vacaciones](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Vacaciones%201.png)
1. sudo: Ejecuta como superusuario El siguiente comando
2. auto_deploy: Herramienta de DockerLabs para levantar máquinas.
3. vacaciones.tar: El "paquete" de la máquina vulnerable.
---

>Ya con la maquina desplegada, hacemos un escaneo a profundidad con nmap:

![Vacaciones](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Vacaciones%202.png)
1. -p-: Escanea todos los puertos (65535 puertos en total).
2. -sV: Detecta versiones de servicios escaneados
3. --min-rate 5000: no envía paquetes mas lento que 5000 por segundo, es decir va volando

>Nos encontramos con el puerto 22 con OpenSSH 7.6 y el puerto 80 con Apache 2.4.29.

![Vacaciones](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Vacaciones%203.png)

>Al revisar la web, la misma esta vacía, así que procedemos revisar el código fuente, allí si que hay cosas interesantes:

![Vacaciones](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Vacaciones%204.png)

>Con este mensaje super escondido, ya podremos intentar romper el servicio ssh con fuerza bruta.

![Vacaciones](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Vacaciones%205.png)
1. -l camilo: Atacamos al usuario "Camilo" (encontrado en el código HTML).
2. -P rockyou.txt: Usamos el diccionario rockyou.txt (El de siempre).
3. -t 64: 64 hilos paralelos (Máximo de hilos que permite la herramienta).

Contraseña encontrada: password1, Así que ingresamos al servicio SSH

![Vacaciones](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Vacaciones%206.png)

>Recordando un poco, el mensaje encontrado en la web era de juan para camilo, hablando sobre un correo importante, así que, naturalmente, revisamos el lugar donde se almacenan los correos en Linux, /var/mail

![Vacaciones](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Vacaciones%207.png)

>Fácilmente encontramos una contraseña en texto claro, con las que podemos cambiar de usuario

![Vacaciones](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Vacaciones%208.png)

>Con un “sudo -l” Listamos los privilegios que tiene juan en todo el sistema, y…

![Vacaciones](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Vacaciones%209.png)

>Juan puede ejecutar /usr/bin/ruby como root sin contraseña.


![Vacaciones](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Vacaciones%2010.png)
- GTFOBins nos ilumina

>Vemos una manera muy simple de escalar privilegios, así que:

![Vacaciones](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Vacaciones%2011.png)

---
O.O   //El comando "rm -rf /*" ejecutado como administrador borra todos los archivos del sistema, es un pequeño guiño al ganar acceso como root a una máquina, NO LO EJECUTES//   O.O


## Cadena de ataque detectada

- **Enumeration**: Apache, HTTP, Port enumeration, SSH
- **Initial Access**: Brute force
- **Post Exploitation**: Credential extraction
- **Privilege Escalation**: SUID abuse, SUID binary abuse, sudo abuse, sudo binary abuse


## Tecnicas utilizadas

- [Brute force](../../../techniques/brute-force.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [sudo abuse](../../../techniques/sudo-abuse.md)
- [SUID abuse](../../../techniques/suid-abuse.md)


## Herramientas utilizadas

- [GTFOBins](../../../tools/gtfobins.md)
- [Nmap](../../../tools/nmap.md)
- [Ruby](../../../tools/ruby.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)


## Servicios relacionados

- [Apache](../../../services/apache.md)
- [HTTP](../../../services/http.md)
- [SSH](../../../services/ssh.md)


## Vulnerabilidades relacionadas

- [sudo misconfiguration](../../../vulnerabilities/sudo-misconfiguration.md)
- [SUID misconfiguration](../../../vulnerabilities/suid-misconfiguration.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [sudo binary abuse](../../../privilege_methods/sudo-binary-abuse.md)
- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

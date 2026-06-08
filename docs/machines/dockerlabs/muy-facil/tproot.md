---
title: Tproot
node_type: machine
platform: dockerlabs
difficulty: muy-facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Muy Faciles/Tproot.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Tproot

## Resumen

Tproot documenta una ruta muy facil alrededor de FTP: la resolucion confirma conectividad, enumera puertos y analiza el servicio expuesto antes de aprovechar el comportamiento vulnerable.

Fuente original: [Maquinas De Dockerlabs/Maquinas Muy Faciles/Tproot.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Muy%20Faciles/Tproot.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | muy-facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 21, 6200 |
| Imagenes en fuente | 8 |
| Palabras en fuente | 460 |
| Requiere revision | false |

## Resolucion paso a paso

Resolución de la Máquina "Tproot" - DockerLabs

>En esta ocasión nos enfrentamos a la máquina *Tproot*, calificada como "Muy Fácil" y creada por el autor d1se0.

---

![Tproot](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Tproot.png)

>Primero, levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![Tproot](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Tproot%201.png)

>Confirmamos que la IP 172.17.0.2 está viva y coleando con un ping.

![Tproot](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Tproot%202.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, revisa las cabeceras del paquete para verificar que es para ella, y responde con un (Echo Reply).)

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse (Por lo general funciona para determinar el sistema operativo víctima)
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)_

>Ya con conexión a la maquina, vamos con el primero escaneo:

![Tproot](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Tproot%203.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-T 5 (Ajusta la velocidad del escaneo, muy muy rápido)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-sV (Realiza un reconocimiento de versiones de servicios)

>Ya con los puertos identificados, buscaremos con la herramienta "Searchsploit" posibles vulnerabilidades de los servicios que están en funcionamiento:

![Tproot](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Tproot%204.png)

>Searchsploit nos revela algo particular; vsftpd 2.3.4 con backdoor incluido. Y es uno muy particular. Algún pillo, pirateo la versión oficial de vsftpd y la infectó con un backdoor, luego la subió a un canal de distribución ilegítimo, y se empezó a esparcir. La manera de activar el backdoor es lo más particular, ya que se activa al colocar una carita feliz en el nombre de usuario al ingresar por ftp:

![Tproot](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Tproot%205.png)
_Ingresamos con la herramienta nc por el puerto 21_

>No muestra nada en un primer momento
>Pero, al escanear nuevamente la ip, vemos que se ha abierto un puerto que antes no estaba.

![Tproot](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Tproot%206.png)

>Nos conectamos al puerto 6200 y... Shell como root. Tan fácil que hasta da miedo...

![Tproot](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Tproot%207.png)

>Así concluye nuestra incursión en *Tproot*. Una máquina simple, directa, y con una explotación bastante interesante.

O.O   //El comando "rm -rf /*" ejecutado como administrador borra todos los archivos del sistema, es un pequeño guiño al ganar acceso como root a una máquina, NO LO EJECUTES//   O.O


## Cadena de ataque detectada

- **Enumeration**: Connectivity check, FTP, Port enumeration


## Tecnicas utilizadas

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Port enumeration](../../../techniques/port-enumeration.md)


## Herramientas utilizadas

- [Netcat](../../../tools/netcat.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Searchsploit](../../../tools/searchsploit.md)


## Servicios relacionados

- [FTP](../../../services/ftp.md)


## Vulnerabilidades relacionadas

- Sin relaciones confirmadas en el contenido actual.


## Metodos de escalada

- Sin relaciones confirmadas en el contenido actual.

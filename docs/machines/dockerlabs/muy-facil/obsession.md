---
title: Obsession
node_type: machine
platform: dockerlabs
difficulty: muy-facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Muy Faciles/Obsession.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Obsession

## Resumen

Obsession es una maquina de calentamiento para enumeracion y credenciales: combina reconocimiento de red, servicios web/FTP y pruebas controladas de credenciales hasta obtener acceso.

Fuente original: [Maquinas De Dockerlabs/Maquinas Muy Faciles/Obsession.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Muy%20Faciles/Obsession.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | muy-facil |
| Sistema operativo | linux |
| Puertos detectados por texto | No detectados en texto |
| Imagenes en fuente | 11 |
| Palabras en fuente | 626 |
| Requiere revision | false |

## Resolucion paso a paso

>Hoy vamos con otra maquina muy sencillita, para pasar el rato y aprender un poco de paso.

**![Obsession](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Obsession.png)**

>Empezamos por levantarla:

![Obsession](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Obsession%201.png)

>Después, verificamos que tenemos conexión con la maquina. Usamos el comando ping

![Obsession](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Obsession%202.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, revisa las cabeceras del paquete para verificar que es para ella, y responde con un (Echo Reply).)

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse (Por lo general funciona para determinar el sistema operativo víctima)
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)

> Vamos al primer escaneo:

![Obsession](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Obsession%203.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sV (realiza un reconocimiento de versiones de servicios)_

>Encontramos 3 servicios corriendo en versiones relativamente actuales, así que, en primera medida, vamos a la web.

![Obsession](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Obsession%204.png)

>Vemos una pagina muy simple, ningún link nos direcciona a ningún lado, excepto el del GitHub de su creador. Hay un panel de datos, que realmente no tramita información, así que procedemos a analizar el código fuente de la página:

![Obsession](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Obsession%205.png)

>Encontramos un muy pero muy sutil mensaje, ya al saber que reutiliza el usuario "russoski" para todos los servicios, atacamos con fuerza bruta:

![Obsession](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Obsession%206.png)
1. _-l (este parámetro se usa determinar el usuario que ya tenemos, si no hubiéramos tenido un usuario, al colocar “-L” podemos incluir una wordlist para probar usuarios)_
2. _-P (para determinar una wordlist con posibles contraseñas, si tuviéramos una contraseña y quisiéramos probar usuarios, en este punto colocamos “-p” y la contraseña)_
3. _ssh:// (para determinar el servicio a atacar, puede ser http// o ftp://)_
4. _-t (indico que deseo emplear 64 hilos, para agilizar el escaneo)_

>Una vez encontradas las credenciales, ingresamos:

![Obsession](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Obsession%207.png)

>Al listar privilegios para el usuario "russoski", vemos que puede ejecutar “VIM” Como cualquier usuario

![Obsession](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Obsession%208.png)
_Ejecutamos el binario setuid (que siempre se ejecuta como root)“SUDO”, con la flag “-l”. El binario busca los privilegios que el usuario actual tiene descritos en el archivo /etc/sudoers y los muestra por pantalla (Si aplica)_

1. _(root) Permite ejecutar el binario como el usuario mas privilegiado_
2. _NOPASSWD Nos indica que no es necesario ingresar contraseña para ejecutar el binario de manera privilegiada_
3. _/usr/bin/vim Binario sobre el que tenemos privilegios (cuya ruta está definida arriba en “secure_path”_

>Esto es toda una bendición, ya que “vim” es mucho mas que un editor de texto, es tan potente, que permite la ejecución de comandos, pero, si lo ejecutamos como SUDO, los comandos se ejecutaran con el contexto del usuario root y no como el usuario "russoski", así que:

![Obsession](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Obsession%209.png)

![Obsession](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Obsession%2010.png)

La máquina es nuestra :3

_//nota: el comando rm -rf /* ejecutado como administrador borra todos los archivos del sistema, es un pequeño guiño al ganar acceso como root a una máquina, NO LO EJECUTES//_


## Cadena de ataque detectada

- **Enumeration**: Connectivity check, FTP, HTTP, Port enumeration, Web enumeration
- **Initial Access**: Brute force
- **Post Exploitation**: Credential extraction


## Tecnicas utilizadas

- [Brute force](../../../techniques/brute-force.md)
- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [sudo](../../../tools/sudo.md)
- [Vim](../../../tools/vim.md)


## Servicios relacionados

- [FTP](../../../services/ftp.md)
- [HTTP](../../../services/http.md)


## Vulnerabilidades relacionadas

- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- Sin relaciones confirmadas en el contenido actual.

---
title: Trust
node_type: machine
platform: dockerlabs
difficulty: muy-facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Muy Faciles/Trust.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Trust

## Resumen

Trust combina fuerza bruta SSH, fuzzing web y abuso de sudo: la ruta recupera credenciales desde la superficie web y escala aprovechando permisos sobre Vim.

Fuente original: [Maquinas De Dockerlabs/Maquinas Muy Faciles/Trust.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Muy%20Faciles/Trust.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | muy-facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 22, 80 |
| Imagenes en fuente | 13 |
| Palabras en fuente | 1056 |
| Requiere revision | false |

## Resolucion paso a paso

---

**![Trust](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Trust.png)**

Una maquina fácil y agradable, para un día agradable…

El dia de hoy, con esta máquina aprenderemos los conceptos basicos de:

1. Fuerza bruta con Hydra a servicio SSH
2. Enumeración de directorios con WFUZZ
3. Abuso del binario /usr/bin/vim para escalar privilegios

---

>Ahora bien, empezamos por descomprimir el archivo de la maquina con “unzip” y levantarla con el script automatizado que nos entrega DOCKERLABS [https://dockerlabs.es](https://dockerlabs.es)

![Trust](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Trust%201.png)

>A modo de traza y para afianzar conceptos, procedemos a hacer un pequeño escaneo de la red con “arp-scan” para encontrar la IP victima (completamente innecesario, ya que el script nos arroja la ip de la máquina).

![Trust](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Trust%202.png)

>Una vez encontrada la IP victima, hacemos un escaneo bastante fuerte con nmap (al ser un entorno local y controlado, no debemos preocuparnos por romper algo, o ser incognitos)

![Trust](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Trust%203.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
_El segundo escaneo, hecho al encontrar los puertos abiertos de la máquina, se realiza para identificarlos. -sVC es una forma acortada de los parámetros -sV (para un escaneo de los servicios que pueden estar activos en cada puerto) y -sC (realiza un pequeño ataque con algunos scripts propios de nmap)_

>Dentro del escaneo de Nmap encontramos el puerto 22 que pertenece al servicio SSH, y el puerto 80 del servicio APACHE. Con la Herramienta “Searchsploit” podemos buscar alguna vulnerabilidad conocida para las versiones de estos servicios.

![Trust](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Trust%204.png)

>Fue tristemente ineficiente, así que antes de intentar algo con el puerto 22, vamos a analizar el puerto 80

![Trust](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Trust%205.png)

>Realmente no hay demasiado por ver, es una pagina por defecto del servicio apache, así que, para ver si hay algo escondido, vamos a enumerar directorios…

Hay muchas herramientas para enumerar directorios; [Dirb](https://www.kali.org/tools/dirb/), [Gobuster](https://github.com/OJ/gobuster), [ffuf](https://github.com/ffuf/ffuf), Hoy vamos a usar [Wfuzz](https://www.kali.org/tools/wfuzz/), así que para ello:

![Trust](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Trust%206.png)

1. _-c (Para que los códigos de estado en la respuesta tengan colorcitos)_ O.O
2. _-w (Para indicar la Wordlist o lista de palabras con la que Wfuzz aplicara fuerza Bruta, el Wordlist que usamos es de Seclist, lo puedes encontrar aqui:_[_https://github.com/danielmiessler/SecLists_](https://github.com/danielmiessler/SecLists) _)_
3. _--hl hide lines(Se usa para que en la respuesta de Wfuzz no aparezcan los resultados que en el código de la web tengan 368 líneas, en este caso, es para que no aparezcan algunos falsos positivos)_
4. _--hc hide code(Se usa para filtrar un código de estado no deseado en la respuesta. Ya que el 404 es un código de ERROR, lo filtramos para que no aparezca)_
5. _-u (Para determinar la ip a examinar, en ella al final se coloca la palabra clave FUZZ, ese mismo será el lugar donde Wfuzz probara todos los posibles directorios)_
6. _-t (Con este parámetro le informamos a Wfuzz cuantos hilos deseamos que sean usados para esta tarea, es decir, cuántas combinaciones de palabras va a probar al mismo tiempo, en este caso 20, así el escaneo ira mas rápido)_

>En este caso, no obtenemos nada, así que probando con archivos, concatenamos a la palabra interna FUZZ un .php para buscar archivos PHP

![Trust](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Trust%207.png)

>Esto nos revela un archivo secret.php, al abrirlo nos encontramos con un pequeño troleo del creador:

![Trust](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Trust%208.png)

>Pero, nos ha dado un posible nombre de usuario; Mario, así que podemos probar ingresar por el servicio ssh con este nombre de usuario y una fuerza bruta a la contraseña, Con la herramienta “Hydra” será rápido:

![Trust](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Trust%209.png)

1. _-l (este parámetro se usa determinar el usuario que ya tenemos, si no tuviéramos un usuario, al colocar “-L” podemos incluir una Wordlist para probar combinatorias también)_
2. _-P (para determinar, una wordlist con posibles contraseñas, si tuviéramos una contraseña y quisiéramos probar usuarios, en este punto colocamos “-p” y la contraseña)_
3. _ssh:// (para determinar el servicio a atacar, puede ser http// o ftp:// )_

>Así que ya sabiendo el usuario y la contraseña, entramos…

![Trust](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Trust%2010.png)

>Una vez ingresado al sistema, podemos proceder de diferentes maneras con la escalada de privilegios. Con “sudo -l” podemos listar los binarios que tenemos permitido ejecutar como root.

![Trust](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Trust%2011.png)
1. _(ALL) Permite ejecutar el binario como CUALQUIER usuario, incluido claro, el mas privilegiado_
2. _/usr/bin/vim Binario sobre el que tenemos privilegios (cuya ruta está definida arriba en “secure_path”_

>En ello, nos encontramos con la herramienta "Vim", un potente procesador de texto, que mal configurado, es una forma bastante simple de engañar el sistema y subir privilegios.

>Para estos casos, el recurso magno para escalar privilegios: [https://gtfobins.github.io/](https://gtfobins.github.io/). En él, encontramos una manera muy simple de escalar privilegios.

>Resulta que el procesador de texto “Vim” Permite al usuario ejecutar comandos desde si mismo, así que, si nosotros  podemos abrir Vim “sudo /usr/bin/vim” como usuario ROOT, tenemos desde allí una manera de ejecutar comandos como el propio administrador “ROOT”, o simplemente llamar una /bin/bash desde el editor.

_Todo lo anterior se puede simplificar con ejecutar “sudo /usr/bin/vim -c ‘!/bin/bash’” para inyectar de una vez el comando

![Trust](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Trust%2012.png)

>Y Listo, la maquina es toda nuestra :3

O.O   //El comando "rm -rf /*" ejecutado como administrador borra todos los archivos del sistema, es un pequeño guiño al ganar acceso como root a una máquina, NO LO EJECUTES//   O.O


## Cadena de ataque detectada

- **Enumeration**: Apache, FTP, HTTP, PHP, Port enumeration, SSH, Web enumeration
- **Initial Access**: Brute force
- **Post Exploitation**: Credential extraction
- **Privilege Escalation**: SUID abuse, SUID binary abuse, sudo abuse, sudo binary abuse


## Tecnicas utilizadas

- [Brute force](../../../techniques/brute-force.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [sudo abuse](../../../techniques/sudo-abuse.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [FFUF / WFuzz](../../../tools/ffuf-wfuzz.md)
- [Gobuster](../../../tools/gobuster.md)
- [GTFOBins](../../../tools/gtfobins.md)
- [Hydra](../../../tools/hydra.md)
- [Nmap](../../../tools/nmap.md)
- [Searchsploit](../../../tools/searchsploit.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)
- [Vim](../../../tools/vim.md)


## Servicios relacionados

- [Apache](../../../services/apache.md)
- [FTP](../../../services/ftp.md)
- [HTTP](../../../services/http.md)
- [PHP](../../../services/php.md)
- [SSH](../../../services/ssh.md)


## Vulnerabilidades relacionadas

- [sudo misconfiguration](../../../vulnerabilities/sudo-misconfiguration.md)
- [SUID misconfiguration](../../../vulnerabilities/suid-misconfiguration.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [sudo binary abuse](../../../privilege_methods/sudo-binary-abuse.md)
- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

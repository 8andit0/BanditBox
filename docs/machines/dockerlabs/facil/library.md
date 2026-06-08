---
title: Library
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Library.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Library

## Resumen

Library conecta descubrimiento web con explotacion de Joomla y acceso SSH: tras encontrar una pista de credenciales, fuerza usuarios con Hydra y escala explotando un script Python ejecutable con privilegios mediante Python Library Hijacking.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Library.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Library.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 22, 80 |
| Imagenes en fuente | 27 |
| Palabras en fuente | 1716 |
| Requiere revision | false |

## Resolucion paso a paso

>Hoy explotaremos una vulnerabilidad bastante interesante, en este maquina sencillita :3
>Primero, levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506150925.png)

>Levantamos la maquina:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506151102.png)

>Para verificar a modo de traza la conectividad con la maquina victima, hacemos un ping a la ip que nos proporciona el script "auto_deploy":

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506151253.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, revisa las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse (Por lo general funciona para determinar el sistema operativo víctima)
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)

>Ya siendo consientes de la conexión entre maquinas, vamos a escanear puertos abiertos en la maquina, para determinar posibles vectores de explotación:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506151631.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sVC (Aquí se concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_

>Nos encontramos con los puertos 22 y 80, con los servicios OpenSSH y Apache respectivamente. Ya que sus versiones son mas o menos actuales, no buscaremos vulnerabilidades para ellas, en cambio, con la herramienta "whatweb" haremos un reconocimiento de las tecnologías del servicio web Apache que corre por el puerto 80:

**![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506152128.png)
_Whatweb es una herramienta de reconocimiento web creada en Ruby, esta hecha para identificar tecnologías web (Es capaz de detectar Frameworks, plugins, CMS, etc).
Por lo general, mediante una petición GET, recolecta información de toda la respuesta (Cookies, código HTML, encabezados), para que luego, el motor de whatweb con REGEX (expresiones regulares) y sus propios plugins (scripts) de Ruby analicen la respuesta en búsqueda de particularidades propias de tecnologías (Como wp-content para WordPress, X-Powered-By para php o /templates/Joomla para Joomla). [Aqui](https://github.com/urbanadventurer/WhatWeb) te dejo el repo oficial con el código fuente de la herramienta.
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506154219.png)_
_Whatweb nos permite modificar la agresividad del escaneo, modificar hilos y hasta usar un proxy, pero para un escaneo sencillo dentro de un entorno controlado, solamente pasamos la url para un análisis simple_

>Whatweb nos indica que la web tiene una pagina por defecto de apache con el titulo "It works"

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506160626.png)

>Ya verificando que no hay nada en la pagina principal ni el código fuente, procedemos a buscar directorios y archivos web.
>Hay muchas herramientas para enumerar directorios; [Dirb](https://www.kali.org/tools/dirb/), [Gobuster](https://github.com/OJ/gobuster), [Wfuzz](https://www.kali.org/tools/wfuzz/), Pero tal vez la más eficiente es [ffuf](https://github.com/ffuf/ffuf), así que para usarla:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506160933.png)
1. _-c Para que se vea bonito con colorcitos_ ╰(*°▽°*)╯
2. _-w Para especificar el diccionario que se probará en la url (uso un diccionario de [Seclists](https://github.com/danielmiessler/SecLists) )_
3. _-t Para indicarle la cantidad de hilos (tareas múltiples) que deseo para la tarea a realizar, en este caso 200_
4. _-u Indicamos la web a atacar, con la palabra interna FUZZ le indicamos a la herramienta que parte de la url debe ser cambiada por las palabras del el diccionario._
5. _-e Indicamos diferentes terminaciones que deseamos agregar a cada iteración en el diccionario, mientras que las comillas vacías hacen referencia a probar la palabra sin ninguna terminación (ej: -e .txt,.php,”” Probará en la web: palabra.txt, palabra.php y palabra)_

>Dentro de la respuesta de ffuf encontramos unos directorios de JavaScript, el index.html y un extraño index.php

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506162807.png)
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506162819.png)

>Vamos a verlo en la web:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506163142.png)

>Parece ser una contraseña, ya que tenemos el servicio ssh en el puerto 22, podemos intentar un ataque de fuerza bruta de usuarios, ya teniendo una contraseña:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506163432.png)
1. _-L (con este parámetro proporcionamos un diccionario con posibles usuarios, si ya tuviéramos uno pondríamos el parámetro en minúscula "-l" )_
2. _-p (para indicar la contraseña, si no tuviéramos una, colocamos “-P” y el diccionario para probar contraseñas)_
3. _ssh:// (para determinar el servicio a atacar, puede ser http// o ftp://)
4. _-t (indico que deseo emplear 64 hilos, para agilizar el escaneo)_

> Tenemos usuario:contraseña, así que ingresamos por ssh:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506164225.png)

>Primero, para tener una shell mas interactiva:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506180300.png)
_Aquí le estamos diciendo a la Shell que deseamos que la variable de entorno TERM (responsable de especificar el tipo de terminal usado), sea igual a Xterm.
Sí TERM no se establece o está mal establecido en la máquina, cosas como clear, nano, vim, less, no funcionan correctamente (Es para tener una experiencia un poco más funcional).

>Para buscar posibles vectores de escalada de privilegios, vamos a listar privilegios:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506164423.png)
_Ejecutamos el binario setuid (que siempre se ejecuta como root)“SUDO”, con la flag “-l”. El binario busca los privilegios que el usuario actual tiene descritos en el archivo /etc/sudoers y los muestra por pantalla (Si aplica)_
1. _(ALL) Permite ejecutar el binario como CUALQUIER usuario, incluido claro, el mas privilegiado_
2. _NOPASSWD Nos indica que no es necesario ingresar contraseña para ejecutar el binario_
3. _/usr/bin/python3 Binario sobre el que tenemos privilegios (cuya ruta está definida arriba en “secure_path”_
4. /opt/script.py UNICO archivo sobre el cual podemos ejecutar python3

>Vemos que tenemos podemos ejecutar un script como usuario root, al analizarlo un poco, podemos ver que es un script muy sencillo, que copia el contenido de si mismo a la ruta /tmp/script_backup.py con la librería shutil:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506164951.png)
_Con "sudo -u root" el usuario Carlos invoca sudo, que verifica permisos en /etc/sudoers. Si tiene permiso para ejecutar cierto binario como root, sudo llama a setuid() para cambiar al usuario root y ejecutar lo siguiente.

>Con el script no podemos hacer mucho, pero, al listar privilegios el la carpeta opt:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506165536.png)

>Vemos que tenemos Permisos sobre el directorio, siendo asi, para escalar privilegios solo tenemos que eliminar el script original (ya que tenemos permiso para ello) y remplazarlo por uno infectado.

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506170046.png)
_Con "rm" eliminamos el archivo original_

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506170119.png)
_Creamos un nuevo archivo del mismo nombre con nano_

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506170229.png)
_Importamos la librería "os" con ella desde el sistema ejecutamos una /bin/bash

>Ya que al ejecutar el script lo hacemos como usuario root, el proceso hijo de "/bin/bash" tendrá el contexto de aquel usuario:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506170658.png)

Para escalar privilegios de una forma mucho mas interesante O.O, podemos hacer un "Python Library Hijacking":

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506172404.png)

>Ya que sabemos que librería utiliza el script, vamos a verificar la ruta desde la cual Python empieza a buscar la librería que utiliza el script _(Cuando se inicia el interprete de Python, la Shell inicia un proceso hijo, desde allí, una de las primeras cosas que hace, es configurar las rutas de búsqueda (sys.path), rutas que podemos listar, y si tenemos permiso de escritura en alguna de todas, existe la posibilidad de insertar un script infectado)

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506173427.png)
_Con este pequeño inline Podemos listar la rutas de ejecución de librerías predeterminadas de Python
1. _Python3 -c (Para indicar que lo siguiente es un código a ejecutar directamente)
2. _import sys (Importamos el modulo sys (Es el que contiene información sobre rutas, etc))_
3. _print (Función que nos permite imprimir por pantalla el resultado de todo lo que esta dentro del siguiente paréntesis)_
4. _'\n'.join(sys.path) (Llamamos el método join para que itere sobre cada respuesta que nos da "sys.path" y le concatene saltos de linea "\n" para que se imprima de manera mas ordenada)
5. _sys.path (Es la **lista interna de rutas** que Python usa para buscar módulos cuando se importan desde un ejecutable)

>Vemos que aparece un salto de linea particular en la respuesta, para verlo bien, quitamos el método join del comando anterior:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506175240.png)

_Lo anterior también lo puedes lograr_
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506181428.png)
_desde el interprete de Python_

>Lo que esas pequeñas comillas que el primer comando no nos mostro, nos dicen que el primer directorio donde se buscan las librerías, es donde se encuentra el script, es decir /opt.
>Ya que podemos escribir dentro del directorio, Solo nos queda crear un archivo shutil.py infectado en el directorio actual, para que al ejecutar el script y el interprete de Python lea la linea "import shutil", encuentre primero nuestro script infectado en /opt que el real en /usr/lib/python3.12/.

>Creamos nuestro archivo infectado:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506180042.png)

>Y ejecutamos como root:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506180115.png)

La maquina es toda nuestra ahora si :3

O.O   //El comando "rm -rf /*" ejecutado como administrador borra todos los archivos del sistema, es un pequeño guiño al ganar acceso como root a una máquina, NO LO EJECUTES//   O.O


## Cadena de ataque detectada

- **Enumeration**: Apache, Connectivity check, FTP, HTTP, Joomla, PHP, Port enumeration, SSH, Web enumeration
- **Initial Access**: Brute force, CMS exploitation
- **Post Exploitation**: Credential extraction
- **Privilege Escalation**: Python Library Hijacking


## Tecnicas utilizadas

- [Brute force](../../../techniques/brute-force.md)
- [CMS exploitation](../../../techniques/cms-exploitation.md)
- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Python Library Hijacking](../../../techniques/python-library-hijacking.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [FFUF / WFuzz](../../../tools/ffuf-wfuzz.md)
- [Gobuster](../../../tools/gobuster.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [Ruby](../../../tools/ruby.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)
- [WhatWeb](../../../tools/whatweb.md)


## Servicios relacionados

- [Apache](../../../services/apache.md)
- [FTP](../../../services/ftp.md)
- [HTTP](../../../services/http.md)
- [Joomla](../../../services/joomla.md)
- [PHP](../../../services/php.md)
- [SSH](../../../services/ssh.md)


## Vulnerabilidades relacionadas

- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [Python Library Hijacking](../../../privilege_methods/python-library-hijacking.md)

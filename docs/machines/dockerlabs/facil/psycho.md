---
title: Psycho
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Psycho.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Psycho

## Resumen

Psycho trabaja LFI y ejecucion remota con posterior abuso de Python: la resolucion identifica una inclusion de archivos, consigue ejecucion o credenciales y escala con reglas sudo y secuestro de librerias Python.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Psycho.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Psycho.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | No detectados en texto |
| Imagenes en fuente | 21 |
| Palabras en fuente | 1390 |
| Requiere revision | false |

## Resolucion paso a paso

>Buenas Buenas, hoy Tenemos nuestra primera maquina de dificultad Fácil, así que, sin más, vamos por ella intentando aprender lo máximo posible :3

**![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho.png)**

>Primero, levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%201.png)

>Verificamos que tenemos conexión con la máquina realizando un comando ping, con este mismo, determinamos que estamos frente a un sistema Linux (como todas las máquinas de DockerLabs):

**![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%202.png)**
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, verifica las cabeceras del paquete para verificar que es para ella, y responde con un (Echo Reply).)_

_(Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”, con el valor de “ttl=” podemos ver el numero maximo de saltos que puede dar un paquete antes de descartarse(Por lo general funciona para determinar el sistema operativo víctima), y con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)_

>Empezamos con el primer escaneo de nmap:

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%203.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)_
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sV (realiza un reconocimiento de versiones de servicios)_

>Podemos observar 2 servicios corriendo en sus puertos por defecto, cada uno con versiones relativamente actualizadas, así que vamos a escanear la web:

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%204.png)

>Vemos una web bastante simple, sin mucho que analizar, excepto por un error extraño en la zona de abajo.
>Luego de fuzzear directorios y no encontrar mucho, probamos a fuzzear archivos y encontramos el "index.php":

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%205.png)
1. _-c Para que se vea bonito con colorcitos O.O_
2. _-w Para especificar el diccionario que se probara en la url (uso un diccionario de [Seclists_](https://github.com/danielmiessler/SecLists)
3. _-t Para indicar la cantidad de hilos (tareas múltiples) que deseamos para la tarea a realizar, en este caso 200_
4. _-u Indicamos la url a atacar, con la palabra interna FUZZ  le decimos a la herramienta la parte de la url que debe ser cambiada por las palabras en el diccionario._
5. _–hc=404 Filtra como no deseadas las respuestas 404 (de error) del servidor http_

>Aunque solo descubrimos el "index.php", es usual que los archivos PHP contengan parámetros mal sanitizados, si así es, podríamos ver archivos de la maquina (LFI).
>Si probamos fuzzear parámetros para este archivo, podríamos observar un posible cambio en la web, para buscar un LFI(si quieres un poco mas de informacion: [https://book.hacktricks.wiki/en/pentesting-web/file-inclusion/index.html](https://book.hacktricks.wiki/en/pentesting-web/file-inclusion/index.html) ):

>Modificamos un poco el comando anterior, aunque lo haremos con el mismo diccionario, esta vez buscaremos parámetros que generen un cambio en la web.

>La estructura usual en la que un archivo ".php" recibe un parámetro desde la URL es “[http://URL/archivo.php?parámetro=valor_del_parametro](http://url/archivo.php?parámetro=valor_del_parametro)”, así que la parte que debemos fuzzear cambia. También modificamos el filtro --hc=404" por --hw=169" para en vez de filtrar por código de estado, filtremos por numero de palabras:

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%206.png)

>Encontramos un parámetro "secret" con 3 lineas menos que el anterior

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%207.png)

>El error que habíamos visto antes cobra sentido, ya que ahora que usamos el parámetro encontrado, ya no aparece ningún error. Prometedor…

>Intentamos un LFI:

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%208.png)

>Allí lo tenemos, Vemos que esta el usuario "luisillo" y "vaxei", al no encontrar logs para envenenar y pasar a un RCE buscamos claves privadas de ssh en los directorios personales de los usuarios, y esas si que encontramos :3

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%209.png)

>Encontramos la clave privada de vaxei, podemos entrar por ssh, si está habilitado claro, para ello copiamos la clave privada de la web a un archivo id_rsa.

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%2010.png)
_Para que funcione, el archivo debe tener solamente permisos de lectura y ejecución (o solo lectura) para el usuario propietario, de no ser así, el cliente ssh no permitirá el uso de la clave privada._
_Para ello usamos el comando “chmod 600 id_rsa” (un poco de info para entenderlo a fondo [https://www.profesionalreview.com/2017/01/28/permisos-basicos-linux-ubuntu-chmod/](https://www.profesionalreview.com/2017/01/28/permisos-basicos-linux-ubuntu-chmod/) )

>Ya que esta listo, ingresamos por ssh:

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%2011.png)

>Procedemos a listar privilegios con sudo -l

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%2012.png)
_Ejecutamos el binario setuid (que siempre se ejecuta como root)“SUDO”, con la flag “-l”. El binario busca los privilegios que el usuario actual tiene descritos en el archivo /etc/sudoers y los muestra por pantalla (Si aplica)_

1. _(luisillo) Permite ejecutar el binario SOLAMENTE como el usuario luisillo
2. _NOPASSWD Nos indica que no es necesario ingresar contraseña para ejecutar el binario_
3. _/usr/bin/perl Binario sobre el que tenemos privilegios (cuya ruta está definida arriba en “secure_path”_

>Vemos que podemos ejecutar el binario perl como el usuario luisillo (Los lenguajes interpretados siempre nos pueden permitir obtener una Shell como otro usuario en tiempo real y con mucha facilidad (Python, Perl, ruby).

>En la práctica:

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%2013.png)
1. _sudo -u luisillo: El usuario vaxet invoca sudo, que verifica permisos en /etc/sudoers.
   Si tiene acceso, sudo llama a setuid() para cambiar al usuario luisillo.
2. _Ejecución de Perl: El intérprete de Perl (/usr/bin/perl) inicia un proceso hijo.
   La opción -e permite ejecutar código directamente desde la línea de comandos.
3. _exec "/bin/bash": La función exec de Perl sobrescribe el proceso actual con /bin/bash.
Todo este resulta en que la nueva shell (/bin/bash) se ejecuta como luisillo, confirmado por whoami.

>Ahora que somos luisillo volvemos a listar privilegios:

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%2014.png)

>Podemos ver que Podemos ejecutar como root el binario python3 SOLAMENTE para el archivo /opt/paw.py

>Al ejecutarlo, nos da un error de sintaxis y de una librería:

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%2015.png)

>En realidad, la explotación en este punto puede ser bastante simple, ya que al ver los permisos de la carpeta opt, vemos que los tenemos todos:

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%2016.png)

>Es decir, podríamos simplemente borrar el archivo paw.py, crear otro con un payload que nos de una Shell, y ejecutarlo… Sería hasta un poco más práctico, pero, ya que se ve el error de las librerías de Python, podríamos intentar hacer un “python library hijacking”.

>Para esto, primero vamos a ver qué librerías usa el script:

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%2017.png)

>Usa 4 librerías, y la de subprosess es la que da el error, así que, como segunda medida, vamos a ver las rutas que Python sigue para buscar y ejecutar las librerías importadas, para ello abrimos el interprete de Python, y:

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%2018.png)

>Para nuestra ventaja ese primer ‘ ‘ en la respuesta de Python, nos indica que el primer directorio en donde Python busca librerías es el directorio actual (opt), y ya que nosotros podemos escribir en este, podemos falsificar la librería con código arbitrario :3

![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%2019.png)
_Aquí le estamos diciendo a la Shell que deseamos que la variable de entorno TERM (responsable de especificar el tipo de terminal usado), sea igual a Xterm.
_Sí TERM no se establece o está mal establecido en la máquina, cosas como clear, nano, vim, less, no funcionan correctamente (Es para tener una experiencia un poco más funcional).
_
![Psycho](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Psycho%2020.png)
O.O
>El payload es muy sencillo, simplemente con la librería os desde el sistema ejecutamos una bash privilegiada.

>Al ejecutar el script, Python empieza a buscar las librerías, y encuentra y ejecuta primero nuestra librería infectada que la real. Asi, tenemos un Python Librari hijacking exitoso :3


## Cadena de ataque detectada

- **Enumeration**: Connectivity check, HTTP, PHP, Port enumeration, SSH, Web enumeration
- **Initial Access**: Local File Inclusion, Remote Code Execution
- **Post Exploitation**: Credential extraction
- **Privilege Escalation**: Python Library Hijacking, sudo abuse, sudo binary abuse


## Tecnicas utilizadas

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Local File Inclusion](../../../techniques/lfi.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Python Library Hijacking](../../../techniques/python-library-hijacking.md)
- [Remote Code Execution](../../../techniques/rce.md)
- [sudo abuse](../../../techniques/sudo-abuse.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [Ruby](../../../tools/ruby.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)


## Servicios relacionados

- [HTTP](../../../services/http.md)
- [PHP](../../../services/php.md)
- [SSH](../../../services/ssh.md)


## Vulnerabilidades relacionadas

- [Exposed error message](../../../vulnerabilities/exposed-error-message.md)
- [Insecure file upload](../../../vulnerabilities/insecure-file-upload.md)
- [sudo misconfiguration](../../../vulnerabilities/sudo-misconfiguration.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [Python Library Hijacking](../../../privilege_methods/python-library-hijacking.md)
- [sudo binary abuse](../../../privilege_methods/sudo-binary-abuse.md)

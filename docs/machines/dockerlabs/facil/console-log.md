---
title: Console log
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Console log.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Console log

## Resumen

Console log esta orientada a fugas de informacion en cliente y APIs: la resolucion pivota desde enumeracion web hacia datos expuestos en consola/servicio Node.js, reutiliza credenciales y cierra con abuso local de permisos SUID.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Console log.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Console%20log.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 22, 80, 3000 |
| Imagenes en fuente | 26 |
| Palabras en fuente | 1693 |
| Requiere revision | false |

## Resolucion paso a paso

>Una maquina sencilla, perfecta para aprender conceptos de fugas de información y Fuzzing, asi que vamos :3

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508040242.png)

>Primero, levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508040104.png)

>Hacemos un "Ping" a la maquina victima para verificar la conexión:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508040428.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, revisa las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse (Por lo general funciona para determinar el sistema operativo víctima)
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)

>Ya que tenemos conexión con la maquina, vamos a escanear los posibles puertos abiertos y sus servicios:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508040630.png)
 1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sVC (Aquí se concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_

 >Vemos que el servicio ssh que normalmente esta en el puerto 22 se encuentra en el 5000, en el puerto 80 corre un servicio web "Apache httpd 2.4.61", y en el puerto 3000 encontramos un servicio Node.js Express Framework...
 >_Node.js es un entorno de ejecución de JavaScript bastante útil para crear servicios web funcionales con rapidez. Por otro lado, Express Framework es un marco de trabajo para Node.js que permite crear servidores HTTP, ampliamente usado para crear APIs web.

 >Para terminar con enumeración web, vamos a hacer un escaneo con whatweb a los puertos 3000 y 80:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508042438.png)
_Whatweb es una herramienta de reconocimiento web creada en Ruby, esta hecha para identificar tecnologías web (Es capaz de detectar Frameworks, plugins, CMS, etc).
Por lo general, mediante una petición GET, recolecta información de toda la respuesta (Cookies, código HTML, encabezados), para que luego, el motor de whatweb con REGEX (expresiones regulares) y sus propios plugins (scripts) de Ruby analicen la respuesta en búsqueda de particularidades propias de tecnologías (Como wp-content para WordPress, X-Powered-By para php o /templates/Joomla para Joomla).
Al encontrar coincidencias. usa sus propios plugins (scripts) de Ruby para identificar las tecnologías:
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506154219.png)_
_Whatweb nos permite modificar la agresividad del escaneo, modificar hilos y hasta usar un proxy, pero para un escaneo sencillo dentro de un entorno controlado, solamente pasamos la url para un análisis simple_

>Whatweb nos confirma el uso de Express en el puerto 3000, así que muy probablemente nos enfrentamos a una API...
>Vamos a ver que tiene el servicio web:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508042721.png)

>Tristemente, la pagina no tiene mucho, pero al revisar su código fuente, vemos un archivo interesante:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508042843.png)

>Al revisar el archivo nos encontramos con una fuga de información sensible:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508043041.png)
_Se declara una función llamada autenticate, desde allí, con console.log se imprime el siguiente mensaje en la consola del navegador_

>Bien, según la fuga de información que encontramos, el token para ingresar al directorio /recurso/ es "tockentraviesito"
>Todo lo anterior nos hace suponer que en el puerto 3000 de Node.js hay un directorio "/recurso/"

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508144409.png)

>Aunque por lo visto, no podemos acceder a el. Tal vez, si logramos proporcionar el token que encontramos de manera correcta podremos verlo.

>Ahora bien, desde este punto, la explotación se divide en dos posibles vectores. Primero, vamos a contemplar el primero, en donde usamos el Token encontrado.
>Vamos a ver que tipo de peticiones acepta la web...

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508150853.png)
1. _Curl es una herramienta versátil, para transmitir datos y recibir respuestas en formato url_
2. _Con el parámetro -X le indicamos el método HTTP
3. _OPTIONS es un método que nos permite descubrir que otros métodos HTTP acepta el servidor_
4. _http: //172.17.0.2:3000/recurso/ Es la ruta sobre la que hacemos la petición

>Como podemos ver, la web solo recibe solicitudes por POST, por eso al intentar ingresar antes al recurso recibíamos un error. Hacemos la solicitud con el tipo de petición correcta:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508150052.png)

>POST es un método que envía datos en el cuerpo de la petición, así que para tramitar correctamente nuestro token, debemos hacerlo en el cuerpo de la petición y en el formato correcto (El formato predilecto para tramitar información a una API de Node.js es json)

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508154119.png)
_Con el parámetro -H indicamos que el cuerpo de la petición va en formato JSON (Formato de texto que representa datos de manera estructurada para ser leídos por Node.js), y con el parámetro -d indicamos el cuerpo de la petición, en formato Json_

>Vemos que al proporcionar el token de manera correcta el servidor nos responde correctamente.
>El otro vector de ataque, consiste en Fuzzear la web aun mas:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508155514.png)
1. _-c Para que se vea bonito con colorcitos_ ╰(*°▽°*)╯
2. _-w Para especificar el diccionario que se probará en la url (uso un diccionario de [Seclists](https://github.com/danielmiessler/SecLists) )_
3. _-t Para indicarle la cantidad de hilos (tareas múltiples) que deseo para la tarea a realizar, en este caso 200_
4. _-u Indicamos la web a atacar, con la palabra interna FUZZ le indicamos a la herramienta que parte de la url debe ser cambiada por las palabras del el diccionario._

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508155609.png)

>Encontramos dos directorios web, si inspeccionamos el primero, nos encontramos con algo interesante

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508155924.png)

>La web esta mal configurada, la opción _Listing_ esta habilitada. En una vulnerabilidad de "Directory Listing" podemos ver el árbol de archivos de una web.
>inspeccionando los archivos, nos encontramos con:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508160551.png)
_Explicado muy por encimita :(:_
_Las primeras 4 lineas de codigo; importan el framework Express, luego lo inicia y define el puerto 3000 para el mismo, por ultimo obliga a Express a parsear la peticiones "Content-Type:application/Json"._
_Las siguientes 6 definen que solo se permiten solicitudes POST a /recurso/, se extrae el campo "token" del cuepo de la peticion, si el token es igual a "tokentraviesito", responde con una contraseña._
_Por ultimo inicia el servidor escuchando por cualquier interfaz._

>Todo lo anterior es lo que crea he inicializa la API que acabamos de explotar en el caso anterior, con esto podemos entender como funciona una API sencilla creada con el Framework Express en JavaScript.
>Con la contraseña, ya sea obtenida con Fuzzing o por la API, vamos a probar usuarios para ssh:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508163427.png)
1. _-L (este parámetro nos permite incluir una wordlist con posibles usuarios)_
2. _-p (con este parámetro determinamos la contraseña que ya tenemos en texto plano)_
3. _ssh:// (para determinar el servicio a atacar, luego de ello va la IP a atacar, y por ultimo el puerto)
4. _-t (indico que deseo emplear 64 hilos, para agilizar el escaneo)_

>Después de un rato, encontramos el usuario, así que ingresamos por ssh:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508163601.png)
_Con -p indicamos el puerto, ya que esta vez el servicio no corre por el puerto por defecto (22)_

>Una vez ingresamos a la maquina, hacemos la shell un poco mas interactiva:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508164810.png)
_Aquí le estamos diciendo a la Shell que deseamos que la variable de entorno TERM (responsable de especificar el tipo de terminal usado), sea igual a Xterm.
Sí TERM no se establece o está mal establecido en la máquina, cosas como clear, nano, vim, less, no funcionan correctamente (Es para tener una experiencia un poco más funcional).

>Como primero medida para escalar privilegios, vamos a listar los que tiene el usuario Lovely:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508163820.png)
_Ejecutamos el binario setuid (que siempre se ejecuta como root)“SUDO”, con la flag “-l”. El binario busca los privilegios que el usuario actual tiene descritos en el archivo /etc/sudoers y los muestra por pantalla (Si aplica)_
1. _(ALL) Permite ejecutar el binario como CUALQUIER usuario, incluido claro, el mas privilegiado_
2. _NOPASSWD Nos indica que no es necesario ingresar contraseña para ejecutar el binario_
3. _/usr/bin/nano Binario sobre el que tenemos privilegios (cuya ruta está definida arriba en “secure_path”_

>Vemos que podemos ejecutar el binario /usr/bin/nano como root sin proporcionar contraseña, esto es critico, ya que dentro de si, nano permite la ejecución de comandos con ^T (Atajo Ctrl+T)
>En pocas palabras, si abrimos nano como root:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508165148.png)

>Aplicamos el atajo ^T y pasamos un comando:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508165440.png)

>Este mismo comando se ejecutara como root:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508165332.png)

>Para encontrar la manera de recibir una shell mediante esta vulnerabilidad, la podemos buscar en la biblia de la escalada de privilegios [Gtfobins](https://gtfobins.github.io/gtfobins/nano/)

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508165830.png)

>Para explotarlo, solamente seguimos los pasos dados ejecutando nano como root:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250508170021.png)

>Y la maquina es nuestra  ╰(*°▽°*)╯

O.O   //El comando "rm -rf /*" ejecutado como administrador borra todos los archivos del sistema, es un pequeño guiño al ganar acceso como root a una máquina, NO LO EJECUTES//   O.O


## Cadena de ataque detectada

- **Enumeration**: API, Apache, Connectivity check, HTTP, Joomla, Node.js service, PHP, Port enumeration, SSH, Web enumeration
- **Initial Access**: API abuse, CMS exploitation
- **Post Exploitation**: Credential extraction
- **Privilege Escalation**: SUID abuse, SUID binary abuse


## Tecnicas utilizadas

- [API abuse](../../../techniques/api-abuse.md)
- [CMS exploitation](../../../techniques/cms-exploitation.md)
- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [GTFOBins](../../../tools/gtfobins.md)
- [nano](../../../tools/nano.md)
- [Nmap](../../../tools/nmap.md)
- [Node.js](../../../tools/nodejs.md)
- [Ping](../../../tools/ping.md)
- [Ruby](../../../tools/ruby.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)
- [WhatWeb](../../../tools/whatweb.md)


## Servicios relacionados

- [Apache](../../../services/apache.md)
- [API](../../../services/api.md)
- [HTTP](../../../services/http.md)
- [Joomla](../../../services/joomla.md)
- [Node.js service](../../../services/nodejs-service.md)
- [PHP](../../../services/php.md)
- [SSH](../../../services/ssh.md)


## Vulnerabilidades relacionadas

- [SUID misconfiguration](../../../vulnerabilities/suid-misconfiguration.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

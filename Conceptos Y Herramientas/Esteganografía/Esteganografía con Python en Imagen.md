
------------

>_En secciones posteriores, usaremos y explicaremos herramientas bastante potentes de ocultamiento, cada una de ellas maneja metodologías distintas de Esteganografía. Pero, para entender la esteganografía mas básica, lo mejor será hacerlo manualmente, ya sabes, complicándonos mas aprendemos mas..._
>Para nuestro ejemplo usaremos Python, ya que es la manera mas sencilla de entender lo que sucede a bajo nivel sin herramientas automatizadas. 
>Primero, antes de ir de cabeza a modificar los Bytes de una imagen (Archivo de ejemplo), debemos entender como esta fundamentalmente compuesta y su formato PNG, para así, después poder modificar sus valores sin perder la cabeza :3

>Digamos que tenemos una imagen cualquiera:


![Img](/Attachments/Pasted%20image%2020250627171929.png)
_Nuestra Imagen es una simple captura de pantalla con un archivo y una contraseña en la terminal_

>Un archivo con formato PNG esta compuesto por una secuencia estructurada de bytes en bloques (También llamados Chunks), que podemos visualizar con herramientas como hexdump o xxd:

![Img](/Attachments/Pasted%20image%2020250627172158.png)
_xxd es una herramienta de terminal que nos permite convertir archivos Binarios a una representación hexadecimal o binaria en texto plano. En este caso, el stdout (Respuesta del comando) lo enviamos a "Less" para que sea mas fácil leer el archivo demasiado grande en terminal_

![Img](/Attachments/Pasted%20image%2020250627172736.png)
_En la zona izquierda tenemos el offset (Direcciones de memoria que indican la posición de cada byte), en la mitad están los bytes en hexadecimal (Lo que nos atañe), y a la derecha la representación en ASCII de los bytes imprimibles en ese offset (Función nativa de xxd)_

>Bien. Siempre un PNG empieza por 8 Bytes de cabecera (Siempre son los mismos en PNG)

---->> 89 50 4E 47 0D 0A 1A 0A <<-----
_Explicándolo muy por encima, el 89 indica que es una archivo binario, el "50 4E 47" es la cadena "PNG" en ASCII y todo lo demás es una salto de linea_

>Luego de los 8 bytes de cabecera, tenemos lo bloques o Chunks; IHDR, IDAT, IEND

![Img](/Attachments/Pasted%20image%2020250628003524.png)
1. _El Chunk IHDR contiene información sobre el ancho, alto, la profundidad de los Bits, la compresión, el filtro. Metadata que no usaremos para el ejemplo._
2. _El Chunk IDAT contiene todos los pixeles de la imagen comprimidos con zlib (Estándar en PNG), Pueden haber varios bloques de IDAT en una imagen, pero no es el caso.
3. _El Chunk IEND marca el final del archivo.
4. _Cada Chunk esta delimitado por su nombre en ASCII (Por ejemplo IEND en ASCII es 49 45 4E 44) al comienzo, y por su CRC (Calculo de total de Bytes) al final_

>Cada uno de los Chunks que hemos visto tiene en su interior:

1. _4 Bytes de Longitud que determinan el tamaño del Chunk
2. _4 bytes de Tipo que seria su Identificador ASCII (IHDR,IDAT, IEND).
3. Contenido del Chunk.
4. 4 bytes de CRC que seria el calculo total de bytes de tipo mas el contenido del Chunk

>Ejemplificándolo con el bloque IDAT que modificaremos, tenemos sus 4 Bytes de longitud:

![Img](/Attachments/Pasted%20image%2020250629175345.png)

>Y, inmediatamente después sus 4 Bytes de Tipo:

![Img](/Attachments/Pasted%20image%2020250629175317.png)

>Que darán inicio a todo el contenido de Chunk:

![Img](/Attachments/Pasted%20image%2020250629175607.png)

>Ya con lo anterior tenemos suficiente como para entender las partes de un PNG, entenderemos su proceso de funcionamiento mientras incrustamos el mensaje oculto :3
>_Para que sea mas fácil de comprender, lo haremos desde la consola interactiva de Python, y lo dividiremos en 3 fases:

>FASE 1:

![Img](/Attachments/Pasted%20image%2020250628010150.png)
1. _Abrimos la consola de Python_
2. _Importamos de la librería "pathlib" la clase "Path" que nos ayudara a manejar rutas de archivos_

![Img](/Attachments/Captura%20de%20pantalla%202025-06-28%20010753.png)
1. _Declaramos la variable "File_path" que contiene la ruta de nuestra imagen
2. _luego leemos la variable "File_path" con "read_bytes" un método propio de "pathlib", todo ello lo declaramos en la variable "Datos_png"

>El método read_bytes() nos devolverá el contenido del archivo en Bytes crudos, que es lo que necesitamos para trabajar... Tenemos en total:

![Img](/Attachments/Pasted%20image%2020250628012057.png)
_51.968 Bytes de la imagen en la variable "Datos_png"

>Como se explico antes, TODOS los Chunks o bloques en PNG contienen 4 bytes de longitud, 4 de Tipo, datos en si, y CRC. Necesitamos llegar Hasta los 4 Bytes de Tipo del bloque "IDAT", que son los que dan comienzo a los datos comprimidos de los pixeles, para ello, declaramos una función para extraer todos los datos comprimidos del bloque IDAT.

![Img](/Attachments/Pasted%20image%2020250628013154.png)
```python
def extractor_de_idat(png_bytes):
    chunks = []
    i = 8
```
1. _Empezamos por definir la función "extractor_de_idat"_
2. _Definimos la lista "Chunks" vacía, en donde vamos a almacenar luego los datos del Chunk IDAT
3. _Definimos la variable "i" con el valor 8 (Que hace referencia a los 8 primeros bytes de PNG que lo identifican y NO necesitamos)
```python
    while i < len(png_bytes):
        length = int.from_bytes(png_bytes[i:i+4], byteorder='big')
        chunk_type = png_bytes[i+4:i+8]
```
4. Con "While 1 < len(png_bytes)" iteramos los bytes de la imagen hasta acabarlos
5. Estamos guardando en la variable "Length" los 4 Bytes siguientes a la posición "i" (Variable que ya habíamos definido como 8) que serian los 4 Bytes de longitud de un Chunk:
   
   ![Img](/Attachments/Pasted%20image%2020250628015400.png)
5. Luego guardamos en la variable "Chunk_type" los siguientes 4 bytes que corresponden a los Bytes de tipo, que identificarían la clase de Chunk:
   ![Img](/Attachments/Pasted%20image%2020250628020125.png)

```python
if chunk_type == b'IDAT':
            chunk_data = png_bytes[i+8:i+8+length]
            chunks.append(chunk_data)
```
7. Creamos un condicional "if" en donde verificamos si en la variable "Cunk_type" tenemos "IDAT".
   Si es así, extraemos todos los datos del bloque en la variable Chunk_data que después se agregan a la lista "Chunks"
```python
 i += 4 + 4 + length + 4
```
8. Si el condicional no es cumplido, le agregamos a la variable "i" el valor total del Chunk, con sus 4 Bits de longitud, 4 Bits de Tipo y sus 4 Bytes de CRC, para que en la próxima Iteración se analice el siguiente Bloque o Chunk en busca de IDAT
```python
   return b''.join(chunks)
```
9. Por ultimo, Unimos Todos los Chunks IDAT encontrados (Aunque no es el caso, es una buena practica, ya que muchas veces hay varios)

>Con todo lo anterior, ya tenemos definida una función que extraerá con facilidad los pixeles comprimidos de IDAT:

![Img](/Attachments/Pasted%20image%2020250628022908.png)
_TODOS los datos de IDAT (Pixeles comprimidos) quedarían en la variable "Idat_data"_

![Img](/Attachments/Pasted%20image%2020250628023043.png)
Tenemos 51.861 Bytes

>Ahora, descomprimimos los pixeles usando el modulo zlib (Que utiliza el algoritmo DEFLATE, estándar para compresión de archivos ZIP o PNG)

![Img](/Attachments/Pasted%20image%2020250628023514.png)
_Insertamos los datos descomprimidos a la variable "decompressed_data"_

![Img](/Attachments/Pasted%20image%2020250628023626.png)
_Ahora tenemos 283.725 Bytes a nuestra disposición_

>Bien, ya completamos la primera fase, Tenemos todos los datos descomprimidos y podemos modificarlos al gusto. 
>Desde este punto en realidad las posibilidades son bastantes, como este es un caso explicativo, vamos realizar una inserción de las mas facilitas; Insertaremos nuestro mensaje en los últimos bytes de la imagen, así que pasamos a la FASE 2:

![Img](/Attachments/Pasted%20image%2020250628024421.png)
_Creamos una variable con el mensaje que deseamos insertar en bytes_

>Verificamos el final de los últimos Bytes antes de insertar nuestro mensaje:

![Img](/Attachments/Pasted%20image%2020250628024645.png)
_Exploramos solamente los últimos 30 bytes en hexadecimal_

>Y ahora si, lo insertamos:

![Img](/Attachments/Pasted%20image%2020250628025049.png)
_Creamos en la variable "modificado" con todos los bytes de la variable "decompressed_data" exceptuando el numero de bytes de nuestro mensaje, para luego insertarlo en remplazo de los anteriores bytes_

![Img](/Attachments/Pasted%20image%2020250628025309.png)
_Al verificar nuevamente los últimos 30 Bytes notamos que ahora nuestro mensaje se encuentra allí_

>Bien, esa fue toda la segunda fase, tenemos un variable con todos los pixeles descomprimidos y un mensaje oculto.
>Ya solo nos queda comprimir nuevamente los Bytes con zlib, crear nuevamente el Chunk IDAT, y reconstruir la imagen en la FASE 3:

![Img](/Attachments/Pasted%20image%2020250628030030.png)
_Creamos una nueva variable con los datos comprimidos y los verificamos leyendo su numero de bytes_

>Ahora, para crear un Chunk valido de IDAT debe tener los 4 bytes de Tipo:

![Img](/Attachments/Pasted%20image%2020250628030343.png)
_Creamos la variable "Chunk_type" que contenga la cadena IDAT en bytes, y luego la concatenamos con la variable "nuevo_idat_data" en "Chunk_con_datos"_

>El valor CRC bien calculado:

![Img](/Attachments/Pasted%20image%2020250628030924.png)
1. _Importamos la librería "Binascii" para calcular el CRC32 del Chunk (Estándar en PNG)_
2. calculamos el CRC sobre los datos comprimidos de IDAT mas los 4 Bytes de Tipo que son necesarios.
3. Como lo anterior nos deja un numero entero, y lo necesitamos en bytes lo convertimos a 4 bytes en big endian

>Y la longitud exacta del bloque:

![Img](/Attachments/Pasted%20image%2020250628031626.png)
1. _Creamos la variable "length" y le damos el valor de los bytes totales de la variable "nuevo_idat_data" que tiene los 4 bytes de tipo y los datos comprimidos_
2. Como lo necesitamos en Bytes lo convertimos a 4 bytes en big endian

>Nos queda ahora concatenar todo:

![Img](/Attachments/Pasted%20image%2020250628031940.png)

>Ya tenemos un Bloque IDAT completamente valido y con nuestra cadena oculta.
>Para insertarlo nuevamente, lo mejor seria copiar todo lo que había antes del antiguo IDAT, insertamos el nuevo IDAT, y copiamos todo lo que había después de el!

![Img](/Attachments/Pasted%20image%2020250628033059.png)
1. _Identificamos donde empezaba el primer IDAT antiguo y le restamos 4 para incluir los 4 Bytes de longitud del bloque_
2. Insertamos en una variable los datos anteriores al antiguo IDAT

![Img](/Attachments/Pasted%20image%2020250628033711.png)
_Extraemos la parte de después da IDAT calculando su longitud total, mas la primera parte, mas los Bytes estándar que debe tener para ser valido, mas su CRC. para luego extraerlo en la variable "parte_despues"_

>Unimos todo creando una variable con todos los datos de la nueva imagen:

![Img](/Attachments/Pasted%20image%2020250628034335.png)

>Y por ultimo, la guardamos:

![Img](/Attachments/Pasted%20image%2020250628034507.png)

![Img](/Attachments/Pasted%20image%2020250628034643.png)
_Tenemos nuestra 2 imágenes, una con un mensaje oculto, y la otra original sin modificaciones_

>Vamos a verificar el resultado final de nuestra creación:

![Img](/Attachments/Pasted%20image%2020250628035021.png)
_Abrimos las 2 imágenes con "feh" en segundo plano para que no ocupe nuestra terminal_

>Tenemos la imagen modificada:

![Img](/Attachments/Pasted%20image%2020250628035102.png)

>Y la imagen original:

![Img](/Attachments/Pasted%20image%2020250628035138.png)

>Y ahí lo tenemos :3
>La diferencia no es apreciable a simple vista. Si insertamos un mensaje muy grande si será notorio en los últimos pixeles de la imagen; para ello hay técnicas mas avanzadas de inserción, pero, ahora ya sabemos lo que sucede por detrás de cualquiera de ellas, lo que cambia, es de que manera y que parte modificamos...

>Para encontrar el mensaje podemos simplemente revertir el proceso:

![Img](/Attachments/Pasted%20image%2020250628040355.png)
_Lo único que reutilizamos que no se ve en la imagen es la función extractora de IDAT_

>_Te pido disculpas si mis explicaciones sobre el código son un poco confusas, espero aun así pudieras comprender el concepto, de aquí para adelante, todo es ganancia :3_
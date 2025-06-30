
-------------

>Base 64 es un método de codificación de Binarios, nos puede ayudar cuando necesitamos transmitir imágenes o cadenas complejas por un medio que no lo permite o da errores con caracteres especiales.
>Es decir, es una manera de convertir un binario o cadena compleja en texto de fácil transmisión.

>Su metodología de codificado es bastante sencilla en realidad, vamos a desglosarla un poco...

>Si quisiéramos codificar una cadena:
>Para poner un ejemplo reducido antes de complicarnos un poco mas, podemos entender el proceso de codificado en base64 de esta manera:

1. _Tenemos 1 carácter que seria la "p"
2. Lo pasamos a Binario "01110000"
3. Dividimos el valor binario en partes de 6 bits, la primera parte es "011100" y la segunda quedaría "000000" (En realidad es solo "00" pero completamos para que sea de 6 bits)
4. Pasamos las cadenas de 6 bits a decimal "28" "0"
5. El "Item" 28 de la tabla de base 64 es "c" y el "Item" 0 en la tabla de base64 es "A",  es decir que el valor del carácter "p" en base64 es cA==

![Img](/Attachments/Pasted%20image%2020250619033855.png)

_Agregamos los dos paréntesis porque base64 acepta coherentemente grupos de a 3
caracteres o múltiplos de 3 ("ahí" "clanes" "%%$"), pero "p" es un solo carácter, así pues como le faltan 2 caracteres para llegar a un múltiplo de 3, agregamos dos paréntesis.
si la cadena fuera "pr" o "12" o ".?" agregaríamos solo un paréntesis, ya que solo un carácter haría falta para ser múltiplo de 3.

![Img](/Attachments/Pasted%20image%2020250619034119.png)

_Ejemplo con 2 caracteres, donde solo se agrega 1 paréntesis_

![Img](/Attachments/Pasted%20image%2020250619034205.png)

_Ejemplo con 3 caracteres, donde no se agrega ningún paréntesis_

>Bien :3
>Todo lo anterior lo podemos hacer manualmente desde terminal, para así entenderlo y hacerlo con cadenas un poco mas complejas...
>base64 no opera sobre "caracteres" ni "números" ni "texto", solo sobre bytes crudos. Es decir, no importa si el valor es una imagen (PNG), o una cadena de texto, o un MP3, todo se reduce a una secuencia de bytes.
>Para convertir a bytes debemos seguir el proceso de operación de base64, empezando por pasar los caracteres a Binario, esta vez, con la cadena "Prueba":

![Img](/Attachments/Pasted%20image%2020250618181034.png)
1. _Primero imprimimos la cadena "prueba" con "Echo" y la flag "-n" (Para evitar un salto de linea por defecto),
2. _Con "|" la salida estándar "stdout" pasa a el siguiente comando "xxd"_
3. _"xxd" es una herramienta que nos permite pasar un valor a hexadecimal o binario
4. _La flag "-b" aplica el "modo binario" a nuestra cadena que por defecto se agrupa en 8 caracteres_

>Ya tenemos nuestra cadena en binario, solo que la primera parte (0000000:), la cadena "prueba" y los espacios no nos sirven para el próximo paso de la codificación, así que los eliminamos:

![Img](/Attachments/Pasted%20image%2020250619020434.png)
_Por sobre la respuesta del comando que explicamos anteriormente, aplicamos:_
1. _Con "awk" podemos procesar texto y modificarlo con facilidad 
2. _Con la primera parte $1="" borramos el primer campo (00000000:)
3. _Con $NF="" Borramos el ultimo campo "Prueba"
4. _Con print $0 imprimimos la cadena resultante luego de ser tratada
5. _"|" Pasamos el stdout de "awk" al comando "tr"
6. _"tr" es la herramienta que nos permite filtrar y manipular caracteres de una cadena
7. _Con -d eliminamos un carácter, que en este caso es ' ' representando un espacio

>Bien, ya que tenemos la cadena en binario, según el proceso de codificado de base64, debemos separar la cadena en grupos de 6 bits exactos:

![Img](/Attachments/Pasted%20image%2020250619022904.png)
_Por sobre la respuesta del comando que explicamos anteriormente, aplicamos:_
_"fold" que nos permite dividir cadenas por linea, indicando la cantidad de caracteres de cada división con el parámetro -w_

>Bien, ahora es cuando seria muy eficaz hacer un poco de bash scripting, aunque para motivos de eficiencia, lo haremos desde la terminal.
>Base64 pasa los valores binarios a Decimal ---> Luego los compara en orden con su "item" en la tabla estándar de base64.
>La primera parte, la podemos hacer con un bucle while:

![Img](/Attachments/Pasted%20image%2020250619023757.png)
_Por sobre la respuesta del comando que explicamos anteriormente, aplicamos:_
1. _Con "while read b;" estamos definiendo el bucle while que leerá el valor de la variable "b" (Respuesta linea por linear del comando anterior) hasta terminar con sus iteraciones (Es decir, en la primera iteración $b es igual a 011100, en la segunda iteración $b es igual a 000111, y así hasta terminar con las líneas)_
2. _Con "echo '$ ((2#$b))'" estamos imprimiendo el valor por pantalla de la expresión aritmética de base 2 "2#" sobre $b para convertir en decimal_

>Ya tenemos todos lo bits en Decimal, solo nos hace falta un paso.
>Base64 tiene una tabla estandarizada en donde podemos remplazar un valor decimal por un carácter de la tabla:

```bash
Tabla_de_base64="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
```
_Como ejemplo, el decimal 2 tendría el carácter "C", o el decimal 5 tendría el carácter "F"_

>Así que, todo el Output del comando anterior lo enviamos a un archivo:

![Img](/Attachments/Pasted%20image%2020250619041647.png)

>Y definimos nuestra tabla de base64 como una variable:

![Img](/Attachments/Pasted%20image%2020250619035939.png)

>Con un Bucle for podemos iterar en cada uno de los decimales que tenemos en el archivo para obtener su "Item" en la tabla:

![Img](/Attachments/Pasted%20image%2020250619041733.png)
1. _Iniciamos el bucle for definiendo la variable $i que va a iterar por la lista de decimales que tenemos en nuestro archivo "ss.txt" (Usamos cat --> $(cat ss.txt) para no tener que pasar la lista manualmente, si no pasar El Output del comando directamente al bucle)_
2. _$i Itera sobre nuestra lista de decimales, y sobre cada iteración aplicamos la expansión de parámetros  ${tabla_b64: $i:1} que nos dará el carácter numero $i en la tabla de base 64
Para entender mejor la expansión de parámetros "${tabla_b64: $i:1}" lo podemos ver como ---> ${ variable : posición_que_deseo_obtener_de_la_variable : caracteres_que_deseo_extraer}

>Lo verificamos decodificándolo:

![Img](/Attachments/Pasted%20image%2020250619040911.png)

>Y he ahí el resultado.
>Como base64 opera sobre Bytes podemos convertir imágenes, PDFs, ZIPs, ejecutables...

![Img](/Attachments/Pasted%20image%2020250619212159.png)
_Vemos una codificación en base64 de un binario. Base64 añade un 33% al tamaño original del binario, es decir, entrega 4 Bytes por cada 3 Bytes _
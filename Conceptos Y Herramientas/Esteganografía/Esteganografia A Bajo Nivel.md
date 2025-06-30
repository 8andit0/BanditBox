
-------------

>Lo mas fundamental que debemos comprender es que la esteganografía en la informática SIEMPRE se reduce a los Bits. Cualquier método esteganográfico que estemos usando, a bajo nivel, lo que hace es manipular los Bits de algún archivo para ofuscar información en ellos.
>Vamos a desglosarlo un poco:

>Sin importar que clase de archivo sea, siempre se reduce a bytes o Bits. Binarios, Imágenes, Videos, Texto, TODO son ceros y unos. La maquina o CPU corre softwares que los leen e interpretan dependiendo del protocolo con el cual estén organizados. 
>Es decir, en el caso de una imagen, el formato PNG daría el estándar de como un software debe leer cada byte de la imagen para ser interpretado correctamente.

>Lo anterior nos lleva a pensar, que si tenemos la capacidad de alterar los Bits (Muy a bajo nivel) o los bytes (También bajo pero no tanto) de un archivo, podríamos ocultar cualquier cosa. El truco esta en hacerlo sin alterar el funcionamiento del archivo original...
>Si entendemos el FORMATO (Estándar en el que se organizan los Bits) de un archivo, podemos predecir con certeza que partes podemos modificar libremente sin dañar el archivo original. Lo anterior, aplica siempre, hasta los procesos de Esteganografía mas complejos que existen, se basan en modificación a bajo nivel de Bits.

>En realidad la esteganografía a bajo nivel es bastante subjetiva. Se basa siempre en una misma raíz, si, pero sus métodos de aplicación son infinitos. Cualquiera que controle y comprenda la organización de los Bits de un archivo, tiene a su disposición la oportunidad de esconder cualquier dato en el. 
>Siendo así, la capacidad de ocultación solo esta limitada por nuestro conocimiento individual a bajo nivel de cualquier entorno, archivo, o volumen informático.
>Vamos con un ejemplo con Python :3
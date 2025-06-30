
------

>La esteganografía es una de las ramas mas útiles y funcionales de la informática. En el ámbito real, es tremendamente aplicable, sobre todo en el tema que nos atañe :3

>_Mi intención en esta sección es plasmar y organizar parte de mis conocimientos en esta bella rama de la informática, a su vez dejando un poco de información útil para quien desea entender y practicar la esteganografía.
>Ten en cuenta que yo también soy un aprendiz permanente y lo que leerás es susceptible a fallos, aun así espero con la mejor intención que disfrutes la sección...

>Bien, empezamos definiendo la Esteganografía como el arte de ocultar cualquier tipo de información en cualquier tipo de información.... Es decir, ocultar cualquier dato (Imagen, Payload, código, texto) En otro dato que debería pasar inadvertido, intentando así, ocultar la existencia total del primer dato.

>La Esteganografía no se limita al ámbito informático, pero ya que es el pentesting lo que nos atañe, vamos a contextualizar sus elementos a la informática.
>_En todos los casos, independiente a la metodología esteganográfica, existirán estos elementos:

1. Payload o Información a encriptar
2. Portador, es el medio en el que ocultaremos la información
3. Método esteganográfico, que seria la metodología de ocultación a usar
4. Resultado, es el Portador con la información ya oculta en si

>_La totalidad de los elementos varia dependiendo de la robustez del método esteganográfico_.
>La esteganografía puede ser combinada con técnicas de criptografía y encriptado que darían como resultado (_En un caso de éxito_) información completamente oculta y MUY difícil de encontrar o identificar.
>En si, la Esteganografía en la ciberseguridad va desde la ofuscación simple de código php en una imagen para ejecutarlo desde un LFI, hasta una ofuscación Bit a Bit de Malware en un archivo que no levantara sospecha de ningún antivirus, IDS/IPS o Firewall.

>Vamos a dar una muy pequeña vuelta por algunos métodos esteganográficos que nos darán luz sobre la complejidad y funcionalidad que tiene esta rama de la ciberseguridad, con algunas herramientas de las mas útiles en el campo. Pero antes de eso, intentaremos comprender a bajo nivel como operan los métodos esteganográficos. 


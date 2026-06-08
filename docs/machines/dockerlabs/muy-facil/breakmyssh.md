---
title: BreakMySSH
node_type: machine
platform: dockerlabs
difficulty: muy-facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Muy Faciles/BreakMySSH.md
needs_review: false
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# BreakMySSH

## Resumen

BreakMySSH se enfoca en comprometer SSH: la nota revisa enumeracion de servicios, uso de fuerza bruta o cracking de credenciales y reutilizacion del acceso para completar el laboratorio.

Fuente original: [Maquinas De Dockerlabs/Maquinas Muy Faciles/BreakMySSH.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Muy%20Faciles/BreakMySSH.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | muy-facil |
| Sistema operativo | linux |
| Puertos detectados por texto | No detectados en texto |
| Imagenes en fuente | 17 |
| Palabras en fuente | 1369 |
| Requiere revision | false |

## Resolucion paso a paso

>Bien, hoy vamos a hacer una maquinita bastante simple, que tiene tras de sí la explotación de una vulnerabilidad muy pero muy interesante :3

>Empezamos por lo normal, levantando la máquina:

![BreakMySSH](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/BreakMySSH.png)

>Vamos a hacer un escaneo fuerte con nmap, sin tener en cuenta la detección, ya que estamos en un entorno controlado:

![BreakMySSH](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/BreakMySSH%201.png)
1. _-- min-rate 5000 (quiero tramitar mínimo 5000 paquetes por segundo) esto para que el escaneo vaya con bastante agilidad._
2. _-n (no deseo que nmap haga una resolución DNS automática)
3. _-p- (quiero escanear los 65535 puertos del sistema, no los 1000 más comunes, como normalmente hace nmap)._
4. _-Pn (Omite el descubrimiento de Host)_
5. _-sV (realiza un reconocimiento de versiones de servicios)_

>Ya que en la maquina solamente esta corriendo el servicio SSH, podríamos usar el script de nmap para una pequeña fuerza bruta, insertando en el escaneo “--script=ssh-brute.nse”.

>Particularmente,  encontramos las credenciales del usuario root, así de fácil:

![BreakMySSH](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/BreakMySSH%202.png)

>Claro que lo mismo hubiéramos logrado con una fuerza bruta mucho más potente con hydra

>Pero omitamos esto anterior, demasiado simple, no tendría sentido dejar la maquina hasta ahí, sin aprender mucho, así que vamos a complicarnos :3

>Buscamos en Searchsploit posibles vulnerabilidades conocidas, ya que en el escaneo nmap se noto que la versión de SSH (OpenSSH 7.7) esta bastante desactualizada.

![BreakMySSH](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/BreakMySSH%203.png)
_Searchsploit es una herramienta de terminal que filtra y busca entre todos los exploits que se encuentran en ExploitDB [[https://www.exploit-db.com/]]_. _En el paquete preinstalado en kali "exploitdb" existe un archivo files_exploits.csv en donde se encuentran los metadatos de TODOS los exploits.
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250504142751.png)
La herramienta Searchsploit filtra por todos ellos buscando coincidencias por sistema operativo, descripción o nombre del servicio, hasta encontrar una coincidencia para una vulnerabilidad que estemos buscando.
Con el parámetro -m (mirror) creamos una copia en el directorio de trabajo actual del exploit que deseamos. Searchsploit copia este archivo desde una ruta en particular del sistema en la que se almacenan los exploits del paquete "ExploitDB"
![Captura](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/Pasted%20image%2020250504143519.png)


>Encontramos varios exploits que permiten enumerar usuarios de ssh, procedemos a descargar uno de ellos con el comando --mirror o -m.

_Yo te recomiendo, descargar el 45939.py o en su defecto (_[_https://www.exploit-db.com/exploits/45939_](https://www.exploit-db.com/exploits/45939) _), ya que la gran mayoría de exploits para cubrir esta vulnerabilidad dan problemas de compatibilidad, logre hacer funcionar este, aun bajo condiciones específicas

_//También te recomiendo, siempre que descargues un exploit intenta entenderlo, si no saber interpretar código python, puedes pasarlo por una IA y pedirle una descripción detallada, así poco a poco, sera mas facil para ti solucionar errores//_

>Esta vulnerabilidad existe, ya que en versiones anteriores a la 7.8 de OpenSSH, el servicio trataba de manera distinta los intentos de autenticación fallidos con un usuario válido y los intentos de autenticación fallidos con usuario invalido. Esto no es transparente para el cliente, que puede analizar las diferencias entre la respuesta del servidor, y así identificar cuales corresponden a un usuario válido y cuales no.
>Esto mismo se puede automatizar con Python, más específicamente con la biblioteca Paramiko, que puede actuar como cliente o servidor SSH. Si quieres ahondar en el tema te recomiendo [esta](https://sekurak.pl/openssh-users-enumeration-cve-2018-15473/) investigación donde lo explican perfectamente.

>Al analizar el código notamos que el script está hecho en “Python 2” y utiliza de una manera muy específica una biblioteca llamada “Paramiko”.

>Después de unos cuantos ataques de ira, note que Paramiko (En su versión compatible con Python 3) no permite ser utilizada de la manera en que el exploit lo hace, así que usar Python 3 queda descartado.

>Para instalar python2 puedes utilizar el comando

```bash
sudo apt install python2
```

>Ahora con solo tener Python 2 no es suficiente, para que el script corra correctamente debemos descargar una versión de "pip" compatible para importar la librería Paramiko en su versión 2.4.2 (que si es compatible con Python 2 y el exploit)

>Descargamos pip2, luego lo instalamos con python2 y luego verificamos que funciona:

```bash
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
sudo python2 get-pip.py
pip2 --version
```

>Ahora instalamos la librería Paramiko desde pip2:

```bash
pip2 install paramiko==2.4.2
```

>Y ahora, por fin podemos correr el script sin errores, bueno, casi...

>_Puedes ingresar este “type=int” para que el puerto sea tratado como un entero, y no como un string, ya que eso te puede dar problemas._

![BreakMySSH](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/BreakMySSH%204.png)

>Ahora si :3

_![BreakMySSH](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/BreakMySSH%205.png)_

>Finalmente, tenemos una manera de enumerar usuarios. Aunque podemos enumerar usuarios escribiéndolos de manera manual, aquí hay un pequeño script de bash que te puede ayudar en el proceso (de ser posible, te sugiero crear el tuyo propio)

```bash
#!/bin/bash
ip="$2"
port="$1"
MAX_JOBS=10
sem(){
	while [ "$(jobs -r | wc -l)" -ge "$MAX_JOBS" ]; do
		sleep 0.2
	done
}
while read user; do
	sem
	(
		result=$(python2 45939.py -p "$port" "$ip" "$user" 2>/dev/null)
		if echo "$result" | grep -q "\[+\]"; then
			echo "$user"
		fi
	) &
done < user.txt_

wait
```

>Puedes usarlo de la siguiente manera:

![BreakMySSH](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/BreakMySSH%206.png)
_Para que funcione bien debes tener un diccionario de posibles usuarios en un archivo llamado “user” en la misma carpeta, y debes darle permisos de ejecución al script.

>Ya una vez tenemos los usuarios, podemos hacer fuerza bruta con cada uno de ellos, así encontramos la contraseña para 2 de ellos:

![BreakMySSH](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/BreakMySSH%207.png)
![BreakMySSH](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/BreakMySSH%208.png)
1. _-l (este parámetro se usa determinar el usuario que ya tenemos, si no tenemos un usuario, al colocar “-L” podemos incluir una wordlist para atacarlos también)_
2. _-P (para determinar, una wordlist con posibles contraseñas, si tuviéramos una contraseña y quisiéramos probar usuarios, en este punto colocamos “-p” y la contraseña)_
3. _ssh:// (para determinar el servicio a atacar, puede ser http// o ftp://, en este caso ssh://)_
4. _-t (indico que deseo emplear 64 hilos, para agilizar el escaneo)_

>Como ingresar como root no sería divertido, vamos a ingresar como usuario Lovely

![BreakMySSH](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/BreakMySSH%209.png)

>_Si te aparece este mismo error, es porque es servidor ssh entro en pánico, para solucionarlo solo sigues la instrucción._

```bash
ssh-keygen -f "/home/bandit0/.ssh/known_hosts" -R "172.17.0.2"
```

_![BreakMySSH](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/BreakMySSH%2010.png)_

>Hoy para escalar privilegios listamos archivos ocultos de sistema

![BreakMySSH](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/BreakMySSH%2011.png)
1. _find (comando de búsqueda en Linux)
2. _/ (búsqueda desde la raíz del sistema)
3. _-name (buscar por nombre)
4. “.*” (le dice al parámetro -name “busca cualquier cosa que empiece por punto y siga con cualquier carácter”)
5. _-readable (archivo al que yo tenga permisos de lectura)
6. _2>/dev/null (redirige los errores al agujero negro de Linux)
7. _"| xargs ls -lah" (le ordena al sistema que a cada iteración del primer comando, le aplique un segundo comando “ls -lah” para ver mas información)

>Así me encuentro con un hash oculto a simple vista

![BreakMySSH](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/BreakMySSH%2012.png)

>Tiene 33 caracteres caracteres hexadecimales así que puede ser un hash de tipo MD5, al usar herramientas como "hash-identifier" o "hashid" no nos dicen mucho. Así que intentamos crackearlo un poco a ciegas como MD5:

![BreakMySSH](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/BreakMySSH%2013.png)
1. _hashcat (herramienta para romper hashes)
2. _-m 0 (indica que el hash es MD5)
3. _-a 0 (ataque de diccionario)
4. _hash.txt (hash a romper)
5. _/usr/share/wordlists/rockyou.txt(diccionario a usar)

>Una vez encontrada la contraseña, ya podemos escalar privilegios con total tranquilidad :3

![BreakMySSH](https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments/BreakMySSH%2014.png)

O.O   //El comando "rm -rf /*" ejecutado como administrador borra todos los archivos del sistema, es un pequeño guiño al ganar acceso como root a una máquina, NO LO EJECUTES//   O.O


## Cadena de ataque detectada

- **Enumeration**: FTP, HTTP, Metadata analysis, Port enumeration, SSH, Web enumeration
- **Initial Access**: Brute force
- **Post Exploitation**: Credential extraction, Hash cracking
- **Privilege Escalation**: Hash cracking to root


## Tecnicas utilizadas

- [Brute force](../../../techniques/brute-force.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Hash cracking](../../../techniques/hash-cracking.md)
- [Metadata analysis](../../../techniques/metadata-analysis.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Web enumeration](../../../techniques/web-enumeration.md)


## Herramientas utilizadas

- [curl](../../../tools/curl.md)
- [find](../../../tools/find.md)
- [grep](../../../tools/grep.md)
- [Hydra](../../../tools/hydra.md)
- [Nmap](../../../tools/nmap.md)
- [Python](../../../tools/python.md)
- [Searchsploit](../../../tools/searchsploit.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)


## Servicios relacionados

- [FTP](../../../services/ftp.md)
- [HTTP](../../../services/http.md)
- [SSH](../../../services/ssh.md)


## Vulnerabilidades relacionadas

- [Secret in metadata](../../../vulnerabilities/secret-in-metadata.md)
- [Weak credentials](../../../vulnerabilities/weak-credentials.md)


## Metodos de escalada

- [Hash cracking to root](../../../privilege_methods/hash-cracking-to-root.md)

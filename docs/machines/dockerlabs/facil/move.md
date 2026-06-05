<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: Move
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Move.md
needs_review: false
---

# Move

## Resumen

Nodo de maquina DockerLabs generado a partir de la nota original. Esta pagina no reemplaza el writeup completo: resume relaciones verificables y deja TODO donde falta revision manual.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Move.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Move.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 21, 22, 80 |
| Imagenes en fuente | 33 |
| Palabras en fuente | 2326 |
| Requiere revision | false |

## Cadena de ataque

- **Enumeration**: API, Apache, Connectivity check, FTP, Grafana, HTTP, MariaDB / MySQL, Metadata analysis, PHP, Port enumeration, SSH, Web enumeration
- **Initial Access**: API abuse, Local File Inclusion, Malicious file upload
- **Post Exploitation**: Credential extraction, Hash cracking, TTY stabilization
- **Privilege Escalation**: Hash cracking to root

## Enumeracion

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Metadata analysis](../../../techniques/metadata-analysis.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Explotacion

- [API abuse](../../../techniques/api-abuse.md)
- [Local File Inclusion](../../../techniques/lfi.md)
- [Malicious file upload](../../../techniques/malicious-file-upload.md)

## Escalada de privilegios

- [Hash cracking to root](../../../privilege_methods/hash-cracking-to-root.md)

## Herramientas utilizadas

- [Burp Suite](../../../tools/burp-suite.md)
- [curl](../../../tools/curl.md)
- [FFUF / WFuzz](../../../tools/ffuf-wfuzz.md)
- [Gobuster](../../../tools/gobuster.md)
- [John the Ripper](../../../tools/john-the-ripper.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [Searchsploit](../../../tools/searchsploit.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)
- [wget](../../../tools/wget.md)

## Herramientas mencionadas

- TODO: informacion no confirmada en el contenido actual.

## Tecnicas utilizadas

- [API abuse](../../../techniques/api-abuse.md)
- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Hash cracking](../../../techniques/hash-cracking.md)
- [Local File Inclusion](../../../techniques/lfi.md)
- [Malicious file upload](../../../techniques/malicious-file-upload.md)
- [Metadata analysis](../../../techniques/metadata-analysis.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [TTY stabilization](../../../techniques/tty-stabilization.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Servicios relacionados

- [Apache](../../../services/apache.md)
- [API](../../../services/api.md)
- [FTP](../../../services/ftp.md)
- [Grafana](../../../services/grafana.md)
- [HTTP](../../../services/http.md)
- [MariaDB / MySQL](../../../services/mariadb-mysql.md)
- [PHP](../../../services/php.md)
- [SSH](../../../services/ssh.md)

## Notas relacionadas

- [Knowledge graph](../../../knowledge-graph.md)
- [Enumeration methodology](../../../learning-paths/enumeration-methodology.md)
- [Web exploitation](../../../learning-paths/web-exploitation.md)
- [Linux privilege escalation](../../../learning-paths/linux-privilege-escalation.md)

## Lecciones aprendidas

TODO: sintetizar aprendizajes especificos despues de migrar editorialmente el writeup completo.

## PENDIENTE

- TODO: revisar capturas para confirmar datos que no aparecen como texto.
- TODO: migrar la narrativa paso a paso desde la nota original.
- TODO: anadir mitigaciones defensivas especificas.

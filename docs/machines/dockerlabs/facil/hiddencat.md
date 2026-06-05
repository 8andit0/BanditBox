<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: HiddenCat
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/HiddenCat.md
needs_review: false
---

# HiddenCat

## Resumen

Nodo de maquina DockerLabs generado a partir de la nota original. Esta pagina no reemplaza el writeup completo: resume relaciones verificables y deja TODO donde falta revision manual.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/HiddenCat.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/HiddenCat.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 8009, 8080 |
| Imagenes en fuente | 18 |
| Palabras en fuente | 2104 |
| Requiere revision | false |

## Cadena de ataque

- **Enumeration**: Apache, Connectivity check, HTTP, Nginx, Port enumeration, SSH, Tomcat
- **Initial Access**: Brute force, Local File Inclusion, Malicious file upload
- **Post Exploitation**: Credential extraction, TTY stabilization
- **Privilege Escalation**: SUID abuse, SUID binary abuse

## Enumeracion

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Port enumeration](../../../techniques/port-enumeration.md)

## Explotacion

- [Brute force](../../../techniques/brute-force.md)
- [Local File Inclusion](../../../techniques/lfi.md)
- [Malicious file upload](../../../techniques/malicious-file-upload.md)

## Escalada de privilegios

- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

## Herramientas utilizadas

- [find](../../../tools/find.md)
- [GTFOBins](../../../tools/gtfobins.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)

## Herramientas mencionadas

- TODO: informacion no confirmada en el contenido actual.

## Tecnicas utilizadas

- [Brute force](../../../techniques/brute-force.md)
- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Local File Inclusion](../../../techniques/lfi.md)
- [Malicious file upload](../../../techniques/malicious-file-upload.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [TTY stabilization](../../../techniques/tty-stabilization.md)

## Servicios relacionados

- [Apache](../../../services/apache.md)
- [HTTP](../../../services/http.md)
- [Nginx](../../../services/nginx.md)
- [SSH](../../../services/ssh.md)
- [Tomcat](../../../services/tomcat.md)

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

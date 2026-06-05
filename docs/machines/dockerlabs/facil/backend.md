<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: Backend
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Backend.md
needs_review: false
---

# Backend

## Resumen

Nodo de maquina DockerLabs generado a partir de la nota original. Esta pagina no reemplaza el writeup completo: resume relaciones verificables y deja TODO donde falta revision manual.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Backend.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Backend.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 22, 80 |
| Imagenes en fuente | 46 |
| Palabras en fuente | 2727 |
| Requiere revision | false |

## Cadena de ataque

- **Enumeration**: Apache, Connectivity check, HTTP, MariaDB / MySQL, Port enumeration, SSH, Web enumeration
- **Initial Access**: Login bypass, SQL Injection
- **Post Exploitation**: Credential extraction, Hash cracking, TTY stabilization
- **Privilege Escalation**: Hash cracking to root, SUID abuse, SUID binary abuse

## Enumeracion

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Explotacion

- [Login bypass](../../../techniques/login-bypass.md)
- [SQL Injection](../../../techniques/sql-injection.md)

## Escalada de privilegios

- [Hash cracking to root](../../../privilege_methods/hash-cracking-to-root.md)
- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

## Herramientas utilizadas

- [Burp Suite](../../../tools/burp-suite.md)
- [find](../../../tools/find.md)
- [grep](../../../tools/grep.md)
- [GTFOBins](../../../tools/gtfobins.md)
- [John the Ripper](../../../tools/john-the-ripper.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [ssh](../../../tools/ssh.md)

## Herramientas mencionadas

- [SQLMap](../../../tools/sqlmap.md)

## Tecnicas utilizadas

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Hash cracking](../../../techniques/hash-cracking.md)
- [Login bypass](../../../techniques/login-bypass.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [SQL Injection](../../../techniques/sql-injection.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [TTY stabilization](../../../techniques/tty-stabilization.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Servicios relacionados

- [Apache](../../../services/apache.md)
- [HTTP](../../../services/http.md)
- [MariaDB / MySQL](../../../services/mariadb-mysql.md)
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

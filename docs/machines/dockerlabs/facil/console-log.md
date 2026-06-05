<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: Console log
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Console log.md
needs_review: false
---

# Console log

## Resumen

Nodo de maquina DockerLabs generado a partir de la nota original. Esta pagina no reemplaza el writeup completo: resume relaciones verificables y deja TODO donde falta revision manual.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Console log.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Console%20log.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 22, 80, 3000 |
| Imagenes en fuente | 26 |
| Palabras en fuente | 1693 |
| Requiere revision | false |

## Cadena de ataque

- **Enumeration**: API, Apache, Connectivity check, HTTP, Joomla, Node.js service, PHP, Port enumeration, SSH, Web enumeration
- **Initial Access**: API abuse, CMS exploitation
- **Post Exploitation**: Credential extraction
- **Privilege Escalation**: SUID abuse, SUID binary abuse

## Enumeracion

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Explotacion

- [API abuse](../../../techniques/api-abuse.md)
- [CMS exploitation](../../../techniques/cms-exploitation.md)

## Escalada de privilegios

- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

## Herramientas utilizadas

- [GTFOBins](../../../tools/gtfobins.md)
- [nano](../../../tools/nano.md)
- [Nmap](../../../tools/nmap.md)
- [Node.js](../../../tools/nodejs.md)
- [Ping](../../../tools/ping.md)
- [Ruby](../../../tools/ruby.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)
- [WhatWeb](../../../tools/whatweb.md)

## Herramientas mencionadas

- TODO: informacion no confirmada en el contenido actual.

## Tecnicas utilizadas

- [API abuse](../../../techniques/api-abuse.md)
- [CMS exploitation](../../../techniques/cms-exploitation.md)
- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Servicios relacionados

- [Apache](../../../services/apache.md)
- [API](../../../services/api.md)
- [HTTP](../../../services/http.md)
- [Joomla](../../../services/joomla.md)
- [Node.js service](../../../services/nodejs-service.md)
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

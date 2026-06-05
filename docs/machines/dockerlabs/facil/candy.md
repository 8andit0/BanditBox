<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: Candy
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Candy.md
needs_review: false
---

# Candy

## Resumen

Nodo de maquina DockerLabs generado a partir de la nota original. Esta pagina no reemplaza el writeup completo: resume relaciones verificables y deja TODO donde falta revision manual.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Candy.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Candy.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 80, 1234 |
| Imagenes en fuente | 31 |
| Palabras en fuente | 2168 |
| Requiere revision | false |

## Cadena de ataque

- **Enumeration**: Apache, Connectivity check, HTTP, Joomla, Metadata analysis, PHP, Port enumeration, Steganography, Web enumeration
- **Initial Access**: CMS exploitation, Malicious file upload, Remote Code Execution
- **Post Exploitation**: Credential extraction
- **Privilege Escalation**: SUID abuse, SUID binary abuse, sudo abuse, sudo binary abuse

## Enumeracion

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Metadata analysis](../../../techniques/metadata-analysis.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Steganography](../../../techniques/steganography.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Explotacion

- [CMS exploitation](../../../techniques/cms-exploitation.md)
- [Malicious file upload](../../../techniques/malicious-file-upload.md)
- [Remote Code Execution](../../../techniques/rce.md)

## Escalada de privilegios

- [sudo binary abuse](../../../privilege_methods/sudo-binary-abuse.md)
- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

## Herramientas utilizadas

- [base64](../../../tools/base64.md)
- [CiberChef](../../../tools/ciberchef.md)
- [find](../../../tools/find.md)
- [grep](../../../tools/grep.md)
- [GTFOBins](../../../tools/gtfobins.md)
- [Netcat](../../../tools/netcat.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Ruby](../../../tools/ruby.md)
- [strings](../../../tools/strings.md)
- [sudo](../../../tools/sudo.md)
- [WhatWeb](../../../tools/whatweb.md)

## Herramientas mencionadas

- TODO: informacion no confirmada en el contenido actual.

## Tecnicas utilizadas

- [CMS exploitation](../../../techniques/cms-exploitation.md)
- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Malicious file upload](../../../techniques/malicious-file-upload.md)
- [Metadata analysis](../../../techniques/metadata-analysis.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Remote Code Execution](../../../techniques/rce.md)
- [Steganography](../../../techniques/steganography.md)
- [sudo abuse](../../../techniques/sudo-abuse.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Servicios relacionados

- [Apache](../../../services/apache.md)
- [HTTP](../../../services/http.md)
- [Joomla](../../../services/joomla.md)
- [PHP](../../../services/php.md)

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

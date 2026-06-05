<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: Verdejo
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Verdejo.md
needs_review: false
---

# Verdejo

## Resumen

Nodo de maquina DockerLabs generado a partir de la nota original. Esta pagina no reemplaza el writeup completo: resume relaciones verificables y deja TODO donde falta revision manual.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Verdejo.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Verdejo.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 22, 80, 8089, 12345 |
| Imagenes en fuente | 37 |
| Palabras en fuente | 2622 |
| Requiere revision | false |

## Cadena de ataque

- **Enumeration**: Apache, Connectivity check, HTTP, Joomla, Metadata analysis, PHP, Port enumeration, SSH, Web enumeration
- **Initial Access**: CMS exploitation, Malicious file upload, Remote Code Execution, SSTI
- **Post Exploitation**: Credential extraction, Hash cracking
- **Privilege Escalation**: Hash cracking to root, SUID abuse, SUID binary abuse

## Enumeracion

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Metadata analysis](../../../techniques/metadata-analysis.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Explotacion

- [CMS exploitation](../../../techniques/cms-exploitation.md)
- [Malicious file upload](../../../techniques/malicious-file-upload.md)
- [Remote Code Execution](../../../techniques/rce.md)
- [SSTI](../../../techniques/ssti.md)

## Escalada de privilegios

- [Hash cracking to root](../../../privilege_methods/hash-cracking-to-root.md)
- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

## Herramientas utilizadas

- [base64](../../../tools/base64.md)
- [Burp Suite](../../../tools/burp-suite.md)
- [grep](../../../tools/grep.md)
- [GTFOBins](../../../tools/gtfobins.md)
- [John the Ripper](../../../tools/john-the-ripper.md)
- [Netcat](../../../tools/netcat.md)
- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [Ruby](../../../tools/ruby.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)
- [WhatWeb](../../../tools/whatweb.md)

## Herramientas mencionadas

- TODO: informacion no confirmada en el contenido actual.

## Tecnicas utilizadas

- [CMS exploitation](../../../techniques/cms-exploitation.md)
- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Hash cracking](../../../techniques/hash-cracking.md)
- [Malicious file upload](../../../techniques/malicious-file-upload.md)
- [Metadata analysis](../../../techniques/metadata-analysis.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Remote Code Execution](../../../techniques/rce.md)
- [SSTI](../../../techniques/ssti.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Servicios relacionados

- [Apache](../../../services/apache.md)
- [HTTP](../../../services/http.md)
- [Joomla](../../../services/joomla.md)
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

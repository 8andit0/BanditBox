<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: nodeclimb
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/nodeclimb.md
needs_review: false
---

# nodeclimb

## Resumen

Nodo de maquina DockerLabs generado a partir de la nota original. Esta pagina no reemplaza el writeup completo: resume relaciones verificables y deja TODO donde falta revision manual.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/nodeclimb.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/nodeclimb.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 21 |
| Imagenes en fuente | 22 |
| Palabras en fuente | 1324 |
| Requiere revision | false |

## Cadena de ataque

- **Enumeration**: Connectivity check, FTP, Node.js service, Port enumeration, SSH, Web enumeration
- **Post Exploitation**: Credential extraction, Hash cracking
- **Privilege Escalation**: Hash cracking to root, SUID abuse, SUID binary abuse, sudo abuse, sudo binary abuse

## Enumeracion

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Explotacion

- TODO: informacion no confirmada en el contenido actual.

## Escalada de privilegios

- [Hash cracking to root](../../../privilege_methods/hash-cracking-to-root.md)
- [sudo binary abuse](../../../privilege_methods/sudo-binary-abuse.md)
- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

## Herramientas utilizadas

- [find](../../../tools/find.md)
- [John the Ripper](../../../tools/john-the-ripper.md)
- [Nmap](../../../tools/nmap.md)
- [Node.js](../../../tools/nodejs.md)
- [Ping](../../../tools/ping.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)
- [wget](../../../tools/wget.md)

## Herramientas mencionadas

- TODO: informacion no confirmada en el contenido actual.

## Tecnicas utilizadas

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Hash cracking](../../../techniques/hash-cracking.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [sudo abuse](../../../techniques/sudo-abuse.md)
- [SUID abuse](../../../techniques/suid-abuse.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Servicios relacionados

- [FTP](../../../services/ftp.md)
- [Node.js service](../../../services/nodejs-service.md)
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

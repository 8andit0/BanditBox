<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: Psycho
node_type: machine
platform: dockerlabs
difficulty: facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Faciles/Psycho.md
needs_review: false
---

# Psycho

## Resumen

Nodo de maquina DockerLabs generado a partir de la nota original. Esta pagina no reemplaza el writeup completo: resume relaciones verificables y deja TODO donde falta revision manual.

Fuente original: [Maquinas De Dockerlabs/Maquinas Faciles/Psycho.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Faciles/Psycho.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | facil |
| Sistema operativo | linux |
| Puertos detectados por texto | TODO |
| Imagenes en fuente | 21 |
| Palabras en fuente | 1390 |
| Requiere revision | false |

## Cadena de ataque

- **Enumeration**: Connectivity check, HTTP, PHP, Port enumeration, SSH, Web enumeration
- **Initial Access**: Local File Inclusion, Remote Code Execution
- **Post Exploitation**: Credential extraction
- **Privilege Escalation**: Python Library Hijacking, sudo abuse, sudo binary abuse

## Enumeracion

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Explotacion

- [Local File Inclusion](../../../techniques/lfi.md)
- [Remote Code Execution](../../../techniques/rce.md)

## Escalada de privilegios

- [Python Library Hijacking](../../../privilege_methods/python-library-hijacking.md)
- [sudo binary abuse](../../../privilege_methods/sudo-binary-abuse.md)

## Herramientas utilizadas

- [Nmap](../../../tools/nmap.md)
- [Ping](../../../tools/ping.md)
- [Python](../../../tools/python.md)
- [Ruby](../../../tools/ruby.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)

## Herramientas mencionadas

- TODO: informacion no confirmada en el contenido actual.

## Tecnicas utilizadas

- [Connectivity check](../../../techniques/connectivity-check.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Local File Inclusion](../../../techniques/lfi.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Python Library Hijacking](../../../techniques/python-library-hijacking.md)
- [Remote Code Execution](../../../techniques/rce.md)
- [sudo abuse](../../../techniques/sudo-abuse.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Servicios relacionados

- [HTTP](../../../services/http.md)
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

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: BreakMySSH
node_type: machine
platform: dockerlabs
difficulty: muy-facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Muy Faciles/BreakMySSH.md
needs_review: false
---

# BreakMySSH

## Resumen

Nodo de maquina DockerLabs generado a partir de la nota original. Esta pagina no reemplaza el writeup completo: resume relaciones verificables y deja TODO donde falta revision manual.

Fuente original: [Maquinas De Dockerlabs/Maquinas Muy Faciles/BreakMySSH.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Muy%20Faciles/BreakMySSH.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | muy-facil |
| Sistema operativo | linux |
| Puertos detectados por texto | TODO |
| Imagenes en fuente | 17 |
| Palabras en fuente | 1369 |
| Requiere revision | false |

## Cadena de ataque

- **Enumeration**: FTP, HTTP, Metadata analysis, Port enumeration, SSH, Web enumeration
- **Initial Access**: Brute force
- **Post Exploitation**: Credential extraction, Hash cracking
- **Privilege Escalation**: Hash cracking to root

## Enumeracion

- [Metadata analysis](../../../techniques/metadata-analysis.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Explotacion

- [Brute force](../../../techniques/brute-force.md)

## Escalada de privilegios

- [Hash cracking to root](../../../privilege_methods/hash-cracking-to-root.md)

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

## Herramientas mencionadas

- TODO: informacion no confirmada en el contenido actual.

## Tecnicas utilizadas

- [Brute force](../../../techniques/brute-force.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Hash cracking](../../../techniques/hash-cracking.md)
- [Metadata analysis](../../../techniques/metadata-analysis.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [Web enumeration](../../../techniques/web-enumeration.md)

## Servicios relacionados

- [FTP](../../../services/ftp.md)
- [HTTP](../../../services/http.md)
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

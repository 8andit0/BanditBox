<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: Vacaciones
node_type: machine
platform: dockerlabs
difficulty: muy-facil
os: linux
source_path: Maquinas De Dockerlabs/Maquinas Muy Faciles/Vacaciones.md
needs_review: false
---

# Vacaciones

## Resumen

Nodo de maquina DockerLabs generado a partir de la nota original. Esta pagina no reemplaza el writeup completo: resume relaciones verificables y deja TODO donde falta revision manual.

Fuente original: [Maquinas De Dockerlabs/Maquinas Muy Faciles/Vacaciones.md](https://github.com/8andit0/BanditBox/blob/main/Maquinas%20De%20Dockerlabs/Maquinas%20Muy%20Faciles/Vacaciones.md)

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | muy-facil |
| Sistema operativo | linux |
| Puertos detectados por texto | 22, 80 |
| Imagenes en fuente | 12 |
| Palabras en fuente | 361 |
| Requiere revision | false |

## Cadena de ataque

- **Enumeration**: Apache, HTTP, Port enumeration, SSH
- **Initial Access**: Brute force
- **Post Exploitation**: Credential extraction
- **Privilege Escalation**: SUID abuse, SUID binary abuse, sudo abuse, sudo binary abuse

## Enumeracion

- [Port enumeration](../../../techniques/port-enumeration.md)

## Explotacion

- [Brute force](../../../techniques/brute-force.md)

## Escalada de privilegios

- [sudo binary abuse](../../../privilege_methods/sudo-binary-abuse.md)
- [SUID binary abuse](../../../privilege_methods/suid-binary-abuse.md)

## Herramientas utilizadas

- [GTFOBins](../../../tools/gtfobins.md)
- [Nmap](../../../tools/nmap.md)
- [Ruby](../../../tools/ruby.md)
- [ssh](../../../tools/ssh.md)
- [sudo](../../../tools/sudo.md)

## Herramientas mencionadas

- TODO: informacion no confirmada en el contenido actual.

## Tecnicas utilizadas

- [Brute force](../../../techniques/brute-force.md)
- [Credential extraction](../../../techniques/credential-extraction.md)
- [Port enumeration](../../../techniques/port-enumeration.md)
- [sudo abuse](../../../techniques/sudo-abuse.md)
- [SUID abuse](../../../techniques/suid-abuse.md)

## Servicios relacionados

- [Apache](../../../services/apache.md)
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

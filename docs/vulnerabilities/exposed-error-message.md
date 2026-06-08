---
title: Exposed error message
node_type: vulnerability
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Exposed error message

## Descripcion

Mensajes de error visibles revelan rutas, consultas, versiones, usuarios o trazas internas. En explotacion ayudan a ajustar payloads; en defensa deben reducirse a mensajes controlados y logs internos.

## Senales de deteccion

- stack traces
- errores SQL
- rutas absolutas
- versiones de framework
- mensajes distintos ante entradas manipuladas

## Mitigacion

Desactivar errores detallados en produccion, registrar internamente con contexto suficiente y devolver respuestas genericas al usuario.

## Guias externas

- [https://hacktricks.wiki/en/generic-methodologies-and-resources/pentesting-methodology.html](https://hacktricks.wiki/en/generic-methodologies-and-resources/pentesting-methodology.html)

## Maquinas relacionadas

- [Backend](../machines/dockerlabs/facil/backend.md)
- [HiddenCat](../machines/dockerlabs/facil/hiddencat.md)
- [Injection](../machines/dockerlabs/muy-facil/injection.md)
- [Internship](../machines/dockerlabs/facil/internship.md)
- [Move](../machines/dockerlabs/facil/move.md)
- [Psycho](../machines/dockerlabs/facil/psycho.md)
- [SecretJenkins](../machines/dockerlabs/facil/secretjenkins.md)
- [Vulnvault](../machines/dockerlabs/facil/vulnvault.md)

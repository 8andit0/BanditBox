---
title: Weak credentials
node_type: vulnerability
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Weak credentials

## Descripcion

Credenciales debiles, por defecto o reutilizadas permiten acceso sin explotar una falla tecnica compleja. En laboratorios suele validarse con diccionarios acotados y evidencia clara del origen.

## Senales de deteccion

- usuarios filtrados
- passwords en web/configuracion
- servicios con login remoto
- credenciales por defecto
- reutilizacion entre servicios

## Mitigacion

Aplicar MFA, politicas de contrasenas, bloqueo progresivo, deteccion de intentos, rotacion de secretos y eliminacion de credenciales por defecto.

## Guias externas

- [https://book.hacktricks.wiki/en/generic-hacking/brute-force.html](https://book.hacktricks.wiki/en/generic-hacking/brute-force.html)

## Maquinas relacionadas

- [Backend](../machines/dockerlabs/facil/backend.md)
- [BorazuwarahCTF](../machines/dockerlabs/muy-facil/borazuwarahctf.md)
- [BreakMySSH](../machines/dockerlabs/muy-facil/breakmyssh.md)
- [Candy](../machines/dockerlabs/facil/candy.md)
- [Console log](../machines/dockerlabs/facil/console-log.md)
- [Extraviado](../machines/dockerlabs/facil/extraviado.md)
- [FirstHacking](../machines/dockerlabs/muy-facil/firsthacking.md)
- [HedgeHog](../machines/dockerlabs/muy-facil/hedgehog.md)
- [HiddenCat](../machines/dockerlabs/facil/hiddencat.md)
- [Injection](../machines/dockerlabs/muy-facil/injection.md)
- [Internship](../machines/dockerlabs/facil/internship.md)
- [Library](../machines/dockerlabs/facil/library.md)
- [Move](../machines/dockerlabs/facil/move.md)
- [nodeclimb](../machines/dockerlabs/facil/nodeclimb.md)
- [Obsession](../machines/dockerlabs/muy-facil/obsession.md)
- [Pequeñas mentirosas](../machines/dockerlabs/facil/pequenas-mentirosas.md)
- [Psycho](../machines/dockerlabs/facil/psycho.md)
- [Reflection](../machines/dockerlabs/facil/reflection.md)
- [SecretJenkins](../machines/dockerlabs/facil/secretjenkins.md)
- [Trust](../machines/dockerlabs/muy-facil/trust.md)
- [Upload](../machines/dockerlabs/facil/upload.md)
- [Vacaciones](../machines/dockerlabs/muy-facil/vacaciones.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)
- [Vulnvault](../machines/dockerlabs/facil/vulnvault.md)
- [Where Is My Web Shell](../machines/dockerlabs/facil/where-is-my-web-shell.md)

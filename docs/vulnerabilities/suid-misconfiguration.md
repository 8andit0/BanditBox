---
title: SUID misconfiguration
node_type: vulnerability
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# SUID misconfiguration

## Descripcion

Un binario SUID mal elegido ejecuta acciones como su propietario. Si ese binario permite invocar comandos, cargar archivos controlados o escribir en rutas sensibles, puede escalar a root.

## Senales de deteccion

- permiso 4000
- binarios no estandar con SUID
- GTFOBins aplicable
- rutas escribibles usadas por el binario
- lectura/escritura privilegiada

## Mitigacion

Reducir SUID al minimo, retirar permisos innecesarios, usar capacidades Linux cuando aplique y monitorizar cambios de permisos privilegiados.

## Guias externas

- [https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/index.html](https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/index.html)

## Maquinas relacionadas

- [Backend](../machines/dockerlabs/facil/backend.md)
- [Candy](../machines/dockerlabs/facil/candy.md)
- [Console log](../machines/dockerlabs/facil/console-log.md)
- [HiddenCat](../machines/dockerlabs/facil/hiddencat.md)
- [Injection](../machines/dockerlabs/muy-facil/injection.md)
- [nodeclimb](../machines/dockerlabs/facil/nodeclimb.md)
- [Pequeñas mentirosas](../machines/dockerlabs/facil/pequenas-mentirosas.md)
- [Reflection](../machines/dockerlabs/facil/reflection.md)
- [Trust](../machines/dockerlabs/muy-facil/trust.md)
- [Upload](../machines/dockerlabs/facil/upload.md)
- [Vacaciones](../machines/dockerlabs/muy-facil/vacaciones.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)
- [Vulnvault](../machines/dockerlabs/facil/vulnvault.md)

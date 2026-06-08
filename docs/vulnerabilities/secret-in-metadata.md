---
title: Secret in metadata
node_type: vulnerability
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Secret in metadata

## Descripcion

Secretos en metadatos aparecen cuando documentos, imagenes o backups conservan usuarios, rutas, comentarios, coordenadas, software o cadenas sensibles.

## Senales de deteccion

- EXIF con autor/ruta
- strings legibles
- comentarios en documentos
- archivos comprimidos con nombres reveladores
- pistas ocultas en imagenes

## Mitigacion

Limpiar metadatos antes de publicar, revisar pipelines de exportacion, bloquear secretos en repositorios y automatizar escaneo de archivos adjuntos.

## Guias externas

- [https://hacktricks.wiki/en/generic-methodologies-and-resources/pentesting-methodology.html](https://hacktricks.wiki/en/generic-methodologies-and-resources/pentesting-methodology.html)

## Maquinas relacionadas

- [BorazuwarahCTF](../machines/dockerlabs/muy-facil/borazuwarahctf.md)
- [BreakMySSH](../machines/dockerlabs/muy-facil/breakmyssh.md)
- [Candy](../machines/dockerlabs/facil/candy.md)
- [Extraviado](../machines/dockerlabs/facil/extraviado.md)
- [FirstHacking](../machines/dockerlabs/muy-facil/firsthacking.md)
- [Internship](../machines/dockerlabs/facil/internship.md)
- [Move](../machines/dockerlabs/facil/move.md)
- [SecretJenkins](../machines/dockerlabs/facil/secretjenkins.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)

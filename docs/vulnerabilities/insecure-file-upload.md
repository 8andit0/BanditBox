---
title: Insecure file upload
node_type: vulnerability
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Insecure file upload

## Descripcion

Una subida insegura permite almacenar archivos no esperados o ejecutables. Si el servidor interpreta el archivo como codigo, la vulnerabilidad puede convertirse en web shell o RCE.

## Senales de deteccion

- validacion solo por extension
- MIME confiado desde el cliente
- archivos publicos en ruta ejecutable
- nombres manipulables
- falta de reescritura del nombre

## Mitigacion

Usar allowlist estricta, validar contenido real, renombrar archivos, almacenar fuera del webroot, retirar permisos de ejecucion y servir descargas desde un controlador seguro.

## Guias externas

- [https://book.hacktricks.wiki/en/pentesting-web/file-upload/index.html](https://book.hacktricks.wiki/en/pentesting-web/file-upload/index.html)

## Maquinas relacionadas

- [Candy](../machines/dockerlabs/facil/candy.md)
- [HiddenCat](../machines/dockerlabs/facil/hiddencat.md)
- [Internship](../machines/dockerlabs/facil/internship.md)
- [Move](../machines/dockerlabs/facil/move.md)
- [Psycho](../machines/dockerlabs/facil/psycho.md)
- [SecretJenkins](../machines/dockerlabs/facil/secretjenkins.md)
- [Upload](../machines/dockerlabs/facil/upload.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)
- [Vulnvault](../machines/dockerlabs/facil/vulnvault.md)
- [Where Is My Web Shell](../machines/dockerlabs/facil/where-is-my-web-shell.md)

---
title: Unsanitized user input
node_type: vulnerability
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Unsanitized user input

## Descripcion

Entrada de usuario sin validacion llega a interpretes como SQL, shell o motores de plantillas. El mismo patron explica SQLi, Command Injection y SSTI: datos tratados como instrucciones.

## Senales de deteccion

- parametros reflejados en consultas
- caracteres especiales alteran la respuesta
- errores ante comillas o separadores
- payloads que cambian logica o salida

## Mitigacion

Separar datos de codigo con consultas parametrizadas, APIs sin shell, plantillas seguras, validacion por allowlist y escaping contextual.

## Guias externas

- [https://book.hacktricks.wiki/en/pentesting-web/sql-injection/index.html](https://book.hacktricks.wiki/en/pentesting-web/sql-injection/index.html)
- [https://book.hacktricks.wiki/pentesting-web/command-injection.html](https://book.hacktricks.wiki/pentesting-web/command-injection.html)

## Maquinas relacionadas

- [Backend](../machines/dockerlabs/facil/backend.md)
- [Injection](../machines/dockerlabs/muy-facil/injection.md)
- [Internship](../machines/dockerlabs/facil/internship.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)

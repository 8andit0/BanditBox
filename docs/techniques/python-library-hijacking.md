---
title: Python Library Hijacking
node_type: technique
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Python Library Hijacking

## Descripcion

Python Library Hijacking aprovecha el orden de busqueda de modulos. Si un script privilegiado importa una libreria desde un directorio escribible, un modulo falso puede ejecutar codigo con esos privilegios.

## Uso en laboratorio

Usarla solo en laboratorios propios, CTFs o entornos con autorizacion explicita. La evidencia debe separar enumeracion, explotacion y post-explotacion para que la ruta sea reproducible.

## Metodologia minima

- Identificar superficie y prerequisitos.
- Confirmar la tecnica con evidencia reproducible.
- Documentar payloads, errores y condiciones.
- Conectar la causa raiz con mitigaciones defensivas.

## Comandos

Sin comandos cortos extraidos automaticamente desde los writeups relacionados.

## Herramientas relacionadas

- [FFUF / WFuzz](../tools/ffuf-wfuzz.md)
- [Gobuster](../tools/gobuster.md)
- [Nmap](../tools/nmap.md)
- [Ping](../tools/ping.md)
- [Python](../tools/python.md)
- [Ruby](../tools/ruby.md)
- [ssh](../tools/ssh.md)
- [sudo](../tools/sudo.md)
- [WhatWeb](../tools/whatweb.md)

## Servicios relacionados

- [Apache](../services/apache.md)
- [FTP](../services/ftp.md)
- [HTTP](../services/http.md)
- [Joomla](../services/joomla.md)
- [PHP](../services/php.md)
- [SSH](../services/ssh.md)

## Maquinas que utilizan esta tecnica

- [Library](../machines/dockerlabs/facil/library.md)
- [Psycho](../machines/dockerlabs/facil/psycho.md)

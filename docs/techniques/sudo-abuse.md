---
title: sudo abuse
node_type: technique
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# sudo abuse

## Descripcion

El abuso de sudo revisa reglas con sudo -l, NOPASSWD, variables preservadas y binarios permitidos. Una regla demasiado amplia puede convertirse en shell privilegiada.

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

- [base64](../tools/base64.md)
- [CiberChef](../tools/ciberchef.md)
- [FFUF / WFuzz](../tools/ffuf-wfuzz.md)
- [find](../tools/find.md)
- [Gobuster](../tools/gobuster.md)
- [grep](../tools/grep.md)
- [GTFOBins](../tools/gtfobins.md)
- [Hydra](../tools/hydra.md)
- [John the Ripper](../tools/john-the-ripper.md)
- [Netcat](../tools/netcat.md)
- [Nmap](../tools/nmap.md)
- [Node.js](../tools/nodejs.md)
- [Ping](../tools/ping.md)
- [Python](../tools/python.md)
- [Ruby](../tools/ruby.md)
- [Searchsploit](../tools/searchsploit.md)
- [ssh](../tools/ssh.md)
- [strings](../tools/strings.md)
- [sudo](../tools/sudo.md)
- [Vim](../tools/vim.md)
- [wget](../tools/wget.md)
- [WhatWeb](../tools/whatweb.md)

## Servicios relacionados

- [Apache](../services/apache.md)
- [FTP](../services/ftp.md)
- [HTTP](../services/http.md)
- [Joomla](../services/joomla.md)
- [Node.js service](../services/nodejs-service.md)
- [PHP](../services/php.md)
- [SSH](../services/ssh.md)

## Maquinas que utilizan esta tecnica

- [Candy](../machines/dockerlabs/facil/candy.md)
- [HedgeHog](../machines/dockerlabs/muy-facil/hedgehog.md)
- [nodeclimb](../machines/dockerlabs/facil/nodeclimb.md)
- [Psycho](../machines/dockerlabs/facil/psycho.md)
- [Trust](../machines/dockerlabs/muy-facil/trust.md)
- [Vacaciones](../machines/dockerlabs/muy-facil/vacaciones.md)

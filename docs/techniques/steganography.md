---
title: Steganography
node_type: technique
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Steganography

## Descripcion

La esteganografia busca informacion escondida dentro de archivos aparentemente normales. En CTFs suele combinarse con strings, binwalk, steghide, metadatos y cracking de contrasenas.

## Uso en laboratorio

Usarla solo en laboratorios propios, CTFs o entornos con autorizacion explicita. La evidencia debe separar enumeracion, explotacion y post-explotacion para que la ruta sea reproducible.

## Metodologia minima

- Identificar superficie y prerequisitos.
- Confirmar la tecnica con evidencia reproducible.
- Documentar payloads, errores y condiciones.
- Conectar la causa raiz con mitigaciones defensivas.

## Comandos

```bash
SELECT * FROM usuarios WHERE usuario = 'tu usuario' AND password = 'tu contraseña';
```

## Herramientas relacionadas

- [base64](../tools/base64.md)
- [CiberChef](../tools/ciberchef.md)
- [ExifTool](../tools/exiftool.md)
- [find](../tools/find.md)
- [grep](../tools/grep.md)
- [GTFOBins](../tools/gtfobins.md)
- [Netcat](../tools/netcat.md)
- [Nmap](../tools/nmap.md)
- [Ping](../tools/ping.md)
- [Python](../tools/python.md)
- [Ruby](../tools/ruby.md)
- [ssh](../tools/ssh.md)
- [steghide](../tools/steghide.md)
- [strings](../tools/strings.md)
- [sudo](../tools/sudo.md)
- [wget](../tools/wget.md)
- [WhatWeb](../tools/whatweb.md)

## Servicios relacionados

- [Apache](../services/apache.md)
- [FTP](../services/ftp.md)
- [HTTP](../services/http.md)
- [Joomla](../services/joomla.md)
- [PHP](../services/php.md)
- [SSH](../services/ssh.md)

## Maquinas que utilizan esta tecnica

- [BorazuwarahCTF](../machines/dockerlabs/muy-facil/borazuwarahctf.md)
- [Candy](../machines/dockerlabs/facil/candy.md)
- [Internship](../machines/dockerlabs/facil/internship.md)

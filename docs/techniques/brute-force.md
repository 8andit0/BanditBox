---
title: Brute force
node_type: technique
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Brute force

## Descripcion

La fuerza bruta prueba combinaciones de usuarios, contrasenas o tokens de forma controlada. En laboratorios se usa para validar credenciales debiles; en defensa exige rate limiting, bloqueo progresivo y MFA.

## Uso en laboratorio

Usarla solo en laboratorios propios, CTFs o entornos con autorizacion explicita. La evidencia debe separar enumeracion, explotacion y post-explotacion para que la ruta sea reproducible.

## Metodologia minima

- Identificar superficie y prerequisitos.
- Confirmar la tecnica con evidencia reproducible.
- Documentar payloads, errores y condiciones.
- Conectar la causa raiz con mitigaciones defensivas.

## Comandos

```bash
sudo docker run -d --ulimit nofile=32768:65536 hiddencat
```

```bash
SELECT * FROM usuarios WHERE usuario = 'tu usuario' AND password = 'tu contraseña';
```

```bash
script /dev/null -c bash
```

```bash
sudo apt install python2
```

```bash
SELECT * FROM usuarios WHERE usuario = 'tu usuario' AND password = 'tu contraseña';
```

## Herramientas relacionadas

- [base64](../tools/base64.md)
- [curl](../tools/curl.md)
- [ExifTool](../tools/exiftool.md)
- [FFUF / WFuzz](../tools/ffuf-wfuzz.md)
- [find](../tools/find.md)
- [Gobuster](../tools/gobuster.md)
- [grep](../tools/grep.md)
- [GTFOBins](../tools/gtfobins.md)
- [Hydra](../tools/hydra.md)
- [Netcat](../tools/netcat.md)
- [Nmap](../tools/nmap.md)
- [Ping](../tools/ping.md)
- [Python](../tools/python.md)
- [Ruby](../tools/ruby.md)
- [Searchsploit](../tools/searchsploit.md)
- [ssh](../tools/ssh.md)
- [steghide](../tools/steghide.md)
- [strings](../tools/strings.md)
- [sudo](../tools/sudo.md)
- [Vim](../tools/vim.md)
- [wget](../tools/wget.md)
- [WhatWeb](../tools/whatweb.md)

## Servicios relacionados

- [Apache](../services/apache.md)
- [FTP](../services/ftp.md)
- [HTTP](../services/http.md)
- [Jenkins](../services/jenkins.md)
- [Joomla](../services/joomla.md)
- [Nginx](../services/nginx.md)
- [PHP](../services/php.md)
- [SSH](../services/ssh.md)
- [Tomcat](../services/tomcat.md)

## Maquinas que utilizan esta tecnica

- [BorazuwarahCTF](../machines/dockerlabs/muy-facil/borazuwarahctf.md)
- [BreakMySSH](../machines/dockerlabs/muy-facil/breakmyssh.md)
- [HedgeHog](../machines/dockerlabs/muy-facil/hedgehog.md)
- [HiddenCat](../machines/dockerlabs/facil/hiddencat.md)
- [Injection](../machines/dockerlabs/muy-facil/injection.md)
- [Internship](../machines/dockerlabs/facil/internship.md)
- [Library](../machines/dockerlabs/facil/library.md)
- [Obsession](../machines/dockerlabs/muy-facil/obsession.md)
- [Pequeñas mentirosas](../machines/dockerlabs/facil/pequenas-mentirosas.md)
- [SecretJenkins](../machines/dockerlabs/facil/secretjenkins.md)
- [Trust](../machines/dockerlabs/muy-facil/trust.md)
- [Vacaciones](../machines/dockerlabs/muy-facil/vacaciones.md)

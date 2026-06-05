<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: Malicious file upload
node_type: technique
---

# Malicious file upload

## Descripcion

Tecnica detectada en BanditBox. TODO: ampliar con contexto teorico y defensivo.

## Cuando usarla

Usarla solo cuando el servicio, la vulnerabilidad y el laboratorio autorizado lo justifiquen.

## Metodologia

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
script /dev/null -c bash
```

```bash
<?php
echo "TESTING";
?>
```

## Errores comunes

- Confundir una mencion con uso real.
- No separar fase de enumeracion y fase de explotacion.
- Omitir mitigaciones.

## Herramientas relacionadas

- [base64](../tools/base64.md)
- [Burp Suite](../tools/burp-suite.md)
- [CiberChef](../tools/ciberchef.md)
- [curl](../tools/curl.md)
- [ExifTool](../tools/exiftool.md)
- [FFUF / WFuzz](../tools/ffuf-wfuzz.md)
- [find](../tools/find.md)
- [Gobuster](../tools/gobuster.md)
- [grep](../tools/grep.md)
- [GTFOBins](../tools/gtfobins.md)
- [John the Ripper](../tools/john-the-ripper.md)
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
- [wget](../tools/wget.md)
- [WhatWeb](../tools/whatweb.md)

## Servicios relacionados

- [Apache](../services/apache.md)
- [API](../services/api.md)
- [FTP](../services/ftp.md)
- [Grafana](../services/grafana.md)
- [HTTP](../services/http.md)
- [Jenkins](../services/jenkins.md)
- [Joomla](../services/joomla.md)
- [MariaDB / MySQL](../services/mariadb-mysql.md)
- [Nginx](../services/nginx.md)
- [PHP](../services/php.md)
- [SSH](../services/ssh.md)
- [Tomcat](../services/tomcat.md)

## Maquinas que utilizan esta tecnica

- [Candy](../machines/dockerlabs/facil/candy.md)
- [HiddenCat](../machines/dockerlabs/facil/hiddencat.md)
- [Internship](../machines/dockerlabs/facil/internship.md)
- [Move](../machines/dockerlabs/facil/move.md)
- [SecretJenkins](../machines/dockerlabs/facil/secretjenkins.md)
- [Upload](../machines/dockerlabs/facil/upload.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)
- [Where Is My Web Shell](../machines/dockerlabs/facil/where-is-my-web-shell.md)

## Referencias

- [Knowledge graph](../knowledge-graph.md)
- TODO: agregar referencias externas verificadas si aplica.

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: Connectivity check
node_type: technique
---

# Connectivity check

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
SELECT * FROM usuarios WHERE usuario = 'tu usuario' AND password = 'tu contraseña';
```

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
<h1 style="color:red">AQUI ESTAMOS INYECTANDO HTML</h1>
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
- [Hydra](../tools/hydra.md)
- [John the Ripper](../tools/john-the-ripper.md)
- [nano](../tools/nano.md)
- [Netcat](../tools/netcat.md)
- [Nmap](../tools/nmap.md)
- [Node.js](../tools/nodejs.md)
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
- [API](../services/api.md)
- [FTP](../services/ftp.md)
- [Grafana](../services/grafana.md)
- [HTTP](../services/http.md)
- [Jenkins](../services/jenkins.md)
- [Joomla](../services/joomla.md)
- [MariaDB / MySQL](../services/mariadb-mysql.md)
- [Nginx](../services/nginx.md)
- [Node.js service](../services/nodejs-service.md)
- [PHP](../services/php.md)
- [SSH](../services/ssh.md)
- [Tomcat](../services/tomcat.md)

## Maquinas que utilizan esta tecnica

- [Backend](../machines/dockerlabs/facil/backend.md)
- [BorazuwarahCTF](../machines/dockerlabs/muy-facil/borazuwarahctf.md)
- [Candy](../machines/dockerlabs/facil/candy.md)
- [Console log](../machines/dockerlabs/facil/console-log.md)
- [Extraviado](../machines/dockerlabs/facil/extraviado.md)
- [HedgeHog](../machines/dockerlabs/muy-facil/hedgehog.md)
- [HiddenCat](../machines/dockerlabs/facil/hiddencat.md)
- [Internship](../machines/dockerlabs/facil/internship.md)
- [Library](../machines/dockerlabs/facil/library.md)
- [Move](../machines/dockerlabs/facil/move.md)
- [nodeclimb](../machines/dockerlabs/facil/nodeclimb.md)
- [Obsession](../machines/dockerlabs/muy-facil/obsession.md)
- [Pequeñas mentirosas](../machines/dockerlabs/facil/pequenas-mentirosas.md)
- [Psycho](../machines/dockerlabs/facil/psycho.md)
- [Reflection](../machines/dockerlabs/facil/reflection.md)
- [SecretJenkins](../machines/dockerlabs/facil/secretjenkins.md)
- [Tproot](../machines/dockerlabs/muy-facil/tproot.md)
- [Upload](../machines/dockerlabs/facil/upload.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)
- [Vulnvault](../machines/dockerlabs/facil/vulnvault.md)
- [Where Is My Web Shell](../machines/dockerlabs/facil/where-is-my-web-shell.md)

## Referencias

- [Knowledge graph](../knowledge-graph.md)
- TODO: agregar referencias externas verificadas si aplica.

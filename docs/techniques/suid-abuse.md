<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: SUID abuse
node_type: technique
---

# SUID abuse

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
<h1 style="color:red">AQUI ESTAMOS INYECTANDO HTML</h1>
```

```bash
<?php
echo "TESTING";
?>
```

```bash
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def hello():
    nombre = request.args.get('nombre', 'Invitado')
    plantilla = f"<h1>Hola, {nombre}!</h1>"  # PARTE VULNERABLE A SSTI
    return render_template_string(plantilla)
```

## Errores comunes

- Confundir una mencion con uso real.
- No separar fase de enumeracion y fase de explotacion.
- Omitir mitigaciones.

## Herramientas relacionadas

- [base64](../tools/base64.md)
- [Burp Suite](../tools/burp-suite.md)
- [CiberChef](../tools/ciberchef.md)
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
- [strings](../tools/strings.md)
- [sudo](../tools/sudo.md)
- [Vim](../tools/vim.md)
- [wget](../tools/wget.md)
- [WhatWeb](../tools/whatweb.md)

## Servicios relacionados

- [Apache](../services/apache.md)
- [API](../services/api.md)
- [FTP](../services/ftp.md)
- [HTTP](../services/http.md)
- [Joomla](../services/joomla.md)
- [MariaDB / MySQL](../services/mariadb-mysql.md)
- [Nginx](../services/nginx.md)
- [Node.js service](../services/nodejs-service.md)
- [PHP](../services/php.md)
- [SSH](../services/ssh.md)
- [Tomcat](../services/tomcat.md)

## Maquinas que utilizan esta tecnica

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

## Referencias

- [Knowledge graph](../knowledge-graph.md)
- TODO: agregar referencias externas verificadas si aplica.

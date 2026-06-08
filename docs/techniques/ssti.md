<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: SSTI
node_type: technique
---

# SSTI

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
- [grep](../tools/grep.md)
- [GTFOBins](../tools/gtfobins.md)
- [John the Ripper](../tools/john-the-ripper.md)
- [Netcat](../tools/netcat.md)
- [Nmap](../tools/nmap.md)
- [Ping](../tools/ping.md)
- [Python](../tools/python.md)
- [Ruby](../tools/ruby.md)
- [ssh](../tools/ssh.md)
- [sudo](../tools/sudo.md)
- [WhatWeb](../tools/whatweb.md)

## Servicios relacionados

- [Apache](../services/apache.md)
- [HTTP](../services/http.md)
- [Joomla](../services/joomla.md)
- [PHP](../services/php.md)
- [SSH](../services/ssh.md)

## Maquinas que utilizan esta tecnica

- [Verdejo](../machines/dockerlabs/facil/verdejo.md)

## Referencias

- [Knowledge graph](../knowledge-graph.md)
- TODO: agregar referencias externas verificadas si aplica.

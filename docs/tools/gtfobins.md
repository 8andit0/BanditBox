---
title: GTFOBins
node_type: tool
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# GTFOBins

## Proposito

GTFOBins aparece en BanditBox como herramienta de apoyo para la fase de privilege-escalation. La pagina agrupa maquinas y tecnicas donde la herramienta tiene evidencia de uso o mencion relevante.

## Uso operativo

Mantener el uso dentro de laboratorios autorizados, registrar comandos reproducibles y separar pruebas de enumeracion de acciones que cambian estado en el objetivo.

## Comandos comunes

```bash
SELECT * FROM usuarios WHERE usuario = 'tu usuario' AND password = 'tu contraseña';
```

```bash
sudo docker run -d --ulimit nofile=32768:65536 hiddencat
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

## Uso dentro de este repositorio

- [Backend](../machines/dockerlabs/facil/backend.md)
- [Candy](../machines/dockerlabs/facil/candy.md)
- [Console log](../machines/dockerlabs/facil/console-log.md)
- [HiddenCat](../machines/dockerlabs/facil/hiddencat.md)
- [Pequeñas mentirosas](../machines/dockerlabs/facil/pequenas-mentirosas.md)
- [Trust](../machines/dockerlabs/muy-facil/trust.md)
- [Upload](../machines/dockerlabs/facil/upload.md)
- [Vacaciones](../machines/dockerlabs/muy-facil/vacaciones.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)

## Maquinas relacionadas

- [Backend](../machines/dockerlabs/facil/backend.md)
- [Candy](../machines/dockerlabs/facil/candy.md)
- [Console log](../machines/dockerlabs/facil/console-log.md)
- [HiddenCat](../machines/dockerlabs/facil/hiddencat.md)
- [Pequeñas mentirosas](../machines/dockerlabs/facil/pequenas-mentirosas.md)
- [Trust](../machines/dockerlabs/muy-facil/trust.md)
- [Upload](../machines/dockerlabs/facil/upload.md)
- [Vacaciones](../machines/dockerlabs/muy-facil/vacaciones.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)

## Tecnicas relacionadas

- [API abuse](../techniques/api-abuse.md)
- [Brute force](../techniques/brute-force.md)
- [CMS exploitation](../techniques/cms-exploitation.md)
- [Connectivity check](../techniques/connectivity-check.md)
- [Credential extraction](../techniques/credential-extraction.md)
- [Hash cracking](../techniques/hash-cracking.md)
- [Local File Inclusion](../techniques/lfi.md)
- [Login bypass](../techniques/login-bypass.md)
- [Malicious file upload](../techniques/malicious-file-upload.md)
- [Metadata analysis](../techniques/metadata-analysis.md)
- [Port enumeration](../techniques/port-enumeration.md)
- [Remote Code Execution](../techniques/rce.md)
- [SQL Injection](../techniques/sql-injection.md)
- [SSTI](../techniques/ssti.md)
- [Steganography](../techniques/steganography.md)
- [sudo abuse](../techniques/sudo-abuse.md)
- [SUID abuse](../techniques/suid-abuse.md)
- [TTY stabilization](../techniques/tty-stabilization.md)
- [Web enumeration](../techniques/web-enumeration.md)

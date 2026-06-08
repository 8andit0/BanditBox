---
title: sudo
node_type: tool
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# sudo

## Proposito

sudo aparece en BanditBox como herramienta de apoyo para la fase de privilege-escalation. La pagina agrupa maquinas y tecnicas donde la herramienta tiene evidencia de uso o mencion relevante.

## Uso operativo

Mantener el uso dentro de laboratorios autorizados, registrar comandos reproducibles y separar pruebas de enumeracion de acciones que cambian estado en el objetivo.

## Comandos comunes

```bash
sudo docker run -d --ulimit nofile=32768:65536 hiddencat
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

- [BorazuwarahCTF](../machines/dockerlabs/muy-facil/borazuwarahctf.md)
- [BreakMySSH](../machines/dockerlabs/muy-facil/breakmyssh.md)
- [Candy](../machines/dockerlabs/facil/candy.md)
- [Console log](../machines/dockerlabs/facil/console-log.md)
- [HedgeHog](../machines/dockerlabs/muy-facil/hedgehog.md)
- [HiddenCat](../machines/dockerlabs/facil/hiddencat.md)
- [Injection](../machines/dockerlabs/muy-facil/injection.md)
- [Library](../machines/dockerlabs/facil/library.md)
- [Move](../machines/dockerlabs/facil/move.md)
- [nodeclimb](../machines/dockerlabs/facil/nodeclimb.md)
- [Obsession](../machines/dockerlabs/muy-facil/obsession.md)
- [Pequeñas mentirosas](../machines/dockerlabs/facil/pequenas-mentirosas.md)
- [Psycho](../machines/dockerlabs/facil/psycho.md)
- [SecretJenkins](../machines/dockerlabs/facil/secretjenkins.md)
- [Trust](../machines/dockerlabs/muy-facil/trust.md)
- [Upload](../machines/dockerlabs/facil/upload.md)
- [Vacaciones](../machines/dockerlabs/muy-facil/vacaciones.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)

## Maquinas relacionadas

- [BorazuwarahCTF](../machines/dockerlabs/muy-facil/borazuwarahctf.md)
- [BreakMySSH](../machines/dockerlabs/muy-facil/breakmyssh.md)
- [Candy](../machines/dockerlabs/facil/candy.md)
- [Console log](../machines/dockerlabs/facil/console-log.md)
- [HedgeHog](../machines/dockerlabs/muy-facil/hedgehog.md)
- [HiddenCat](../machines/dockerlabs/facil/hiddencat.md)
- [Injection](../machines/dockerlabs/muy-facil/injection.md)
- [Library](../machines/dockerlabs/facil/library.md)
- [Move](../machines/dockerlabs/facil/move.md)
- [nodeclimb](../machines/dockerlabs/facil/nodeclimb.md)
- [Obsession](../machines/dockerlabs/muy-facil/obsession.md)
- [Pequeñas mentirosas](../machines/dockerlabs/facil/pequenas-mentirosas.md)
- [Psycho](../machines/dockerlabs/facil/psycho.md)
- [SecretJenkins](../machines/dockerlabs/facil/secretjenkins.md)
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
- [Python Library Hijacking](../techniques/python-library-hijacking.md)
- [Remote Code Execution](../techniques/rce.md)
- [SQL Injection](../techniques/sql-injection.md)
- [SSTI](../techniques/ssti.md)
- [Steganography](../techniques/steganography.md)
- [sudo abuse](../techniques/sudo-abuse.md)
- [SUID abuse](../techniques/suid-abuse.md)
- [TTY stabilization](../techniques/tty-stabilization.md)
- [Web enumeration](../techniques/web-enumeration.md)

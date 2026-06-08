<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: grep
node_type: tool
---

# grep

## Proposito

Herramienta detectada dentro del repositorio BanditBox. TODO: ampliar proposito y limites de uso.

## Instalacion

TODO: documentar instalacion segura y sistema recomendado.

## Comandos comunes

```bash
SELECT * FROM usuarios WHERE usuario = 'tu usuario' AND password = 'tu contraseña';
```

```bash
SELECT * FROM usuarios WHERE usuario = 'tu usuario' AND password = 'tu contraseña';
```

```bash
script /dev/null -c bash
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

## Uso dentro de este repositorio

- [Backend](../machines/dockerlabs/facil/backend.md)
- [BreakMySSH](../machines/dockerlabs/muy-facil/breakmyssh.md)
- [Candy](../machines/dockerlabs/facil/candy.md)
- [Internship](../machines/dockerlabs/facil/internship.md)
- [SecretJenkins](../machines/dockerlabs/facil/secretjenkins.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)
- [Vulnvault](../machines/dockerlabs/facil/vulnvault.md)

## Maquinas relacionadas

- [Backend](../machines/dockerlabs/facil/backend.md)
- [BreakMySSH](../machines/dockerlabs/muy-facil/breakmyssh.md)
- [Candy](../machines/dockerlabs/facil/candy.md)
- [Internship](../machines/dockerlabs/facil/internship.md)
- [SecretJenkins](../machines/dockerlabs/facil/secretjenkins.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)
- [Vulnvault](../machines/dockerlabs/facil/vulnvault.md)

## Tecnicas relacionadas

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

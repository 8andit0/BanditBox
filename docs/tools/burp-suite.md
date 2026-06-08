---
title: Burp Suite
node_type: tool
---

<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

# Burp Suite

## Proposito

Burp Suite aparece en BanditBox como herramienta de apoyo para la fase de initial-access. La pagina agrupa maquinas y tecnicas donde la herramienta tiene evidencia de uso o mencion relevante.

## Uso operativo

Mantener el uso dentro de laboratorios autorizados, registrar comandos reproducibles y separar pruebas de enumeracion de acciones que cambian estado en el objetivo.

## Comandos comunes

```bash
SELECT * FROM usuarios WHERE usuario = 'tu usuario' AND password = 'tu contraseña';
```

```bash
script /dev/null -c bash
```

```bash
<h1 style="color:red">AQUI ESTAMOS INYECTANDO HTML</h1>
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
- [Move](../machines/dockerlabs/facil/move.md)
- [Reflection](../machines/dockerlabs/facil/reflection.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)

## Maquinas relacionadas

- [Backend](../machines/dockerlabs/facil/backend.md)
- [Move](../machines/dockerlabs/facil/move.md)
- [Reflection](../machines/dockerlabs/facil/reflection.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)

## Tecnicas relacionadas

- [API abuse](../techniques/api-abuse.md)
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
- [SUID abuse](../techniques/suid-abuse.md)
- [TTY stabilization](../techniques/tty-stabilization.md)
- [Web enumeration](../techniques/web-enumeration.md)

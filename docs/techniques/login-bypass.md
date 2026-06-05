<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->

---
title: Login bypass
node_type: technique
---

# Login bypass

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
SELECT * FROM usuarios WHERE usuario = 'tu usuario' AND password = 'tu contraseña';
```

```bash
SELECT * FROM usuarios WHERE usuario = 'tu usuario' AND password = 'tu contraseña';
```

## Errores comunes

- Confundir una mencion con uso real.
- No separar fase de enumeracion y fase de explotacion.
- Omitir mitigaciones.

## Herramientas relacionadas

- [base64](../tools/base64.md)
- [Burp Suite](../tools/burp-suite.md)
- [ExifTool](../tools/exiftool.md)
- [find](../tools/find.md)
- [grep](../tools/grep.md)
- [GTFOBins](../tools/gtfobins.md)
- [John the Ripper](../tools/john-the-ripper.md)
- [Netcat](../tools/netcat.md)
- [Nmap](../tools/nmap.md)
- [Ping](../tools/ping.md)
- [Python](../tools/python.md)
- [ssh](../tools/ssh.md)
- [steghide](../tools/steghide.md)
- [strings](../tools/strings.md)
- [sudo](../tools/sudo.md)

## Servicios relacionados

- [Apache](../services/apache.md)
- [HTTP](../services/http.md)
- [MariaDB / MySQL](../services/mariadb-mysql.md)
- [PHP](../services/php.md)
- [SSH](../services/ssh.md)

## Maquinas que utilizan esta tecnica

- [Backend](../machines/dockerlabs/facil/backend.md)
- [Injection](../machines/dockerlabs/muy-facil/injection.md)
- [Internship](../machines/dockerlabs/facil/internship.md)

## Referencias

- [Knowledge graph](../knowledge-graph.md)
- TODO: agregar referencias externas verificadas si aplica.

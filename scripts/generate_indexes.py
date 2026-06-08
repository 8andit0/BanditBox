from __future__ import annotations

import re
import os
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote

from kb_common import DOCS, ROOT, commands_markdown, label, read_relationships, write_generated
from content_guidance import (
    MACHINE_SUMMARIES,
    PRIVILEGE_METHOD_DESCRIPTIONS,
    SERVICE_DESCRIPTIONS,
    TECHNIQUE_DESCRIPTIONS,
    VULNERABILITY_GUIDANCE,
)

GITHUB_BASE = "https://github.com/8andit0/BanditBox/blob/main"
RAW_ATTACHMENTS_BASE = "https://raw.githubusercontent.com/8andit0/BanditBox/main/Attachments"


def page_url(path: str) -> str:
    return "/" + path.replace(".md", "/")


def source_url(path: str) -> str:
    return f"{GITHUB_BASE}/{quote(path, safe='/')}"


def links(items: list[str], group: str, data: dict[str, Any]) -> str:
    if not items:
        return "- Sin relaciones confirmadas en el contenido actual."
    return "\n".join(f"- [{label(data, group, item)}](/{group}/{item}/)" for item in items)


def machine_links(machines: list[dict[str, Any]]) -> str:
    if not machines:
        return "- Sin maquinas relacionadas confirmadas."
    return "\n".join(
        f"- [{m['label']}]({page_url(m['page_path'])})"
        for m in sorted(machines, key=lambda item: item["label"].lower())
    )


def related_machines(node_id: str, field: str, data: dict[str, Any]) -> list[dict[str, Any]]:
    return [m for m in data["nodes"]["machines"] if node_id in m.get(field, [])]


def phase_items(machine: dict[str, Any], data: dict[str, Any], phase: str) -> list[str]:
    return [
        item
        for item in machine.get("techniques", [])
        if data["canonical"]["techniques"].get(item, {}).get("phase") == phase
    ]


def optional_section(title: str, body: str) -> str:
    if not body.strip():
        return ""
    return f"\n## {title}\n\n{body.strip()}\n"


def attachment_url(target: str) -> str:
    cleaned = unquote(target).replace("\\", "/").lstrip("/")
    if cleaned.lower().startswith("attachments/"):
        cleaned = cleaned.split("/", 1)[1]
    return f"{RAW_ATTACHMENTS_BASE}/{quote(cleaned, safe='/')}"


def replace_outside_fences(text: str, pattern: str, repl: Any) -> str:
    parts = re.split(r"(```.*?```)", text, flags=re.S)
    for index, part in enumerate(parts):
        if not part.startswith("```"):
            parts[index] = re.sub(pattern, repl, part)
    return "".join(parts)


def vault_link_url(source_path: str, target: str) -> str:
    clean = unquote(target.strip())
    if clean.startswith(("http://", "https://", "mailto:", "#")):
        return clean
    if Path(clean).suffix.lower() != ".md" and re.fullmatch(r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/.*)?", clean):
        return "https://" + clean
    if clean.startswith("/"):
        rel_path = clean.lstrip("/")
    else:
        rel_path = (Path(source_path).parent / clean).as_posix()
    if Path(rel_path).suffix == "":
        rel_path += ".md"
    return source_url(rel_path)


def normalize_writeup_markdown(text: str, machine_label: str, source_path: str) -> str:
    text = text.replace("\ufeff", "").strip()
    text = re.sub(r"^\s*-{5,}\s*", "", text)
    text = re.sub(
        r"\[([^\]]+)\]\(\[(https?://[^\]]+)\]\([^)]+\)\s*\)",
        r"[\1](\2)",
        text,
    )

    def wiki_image(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        return f"![{machine_label}]({attachment_url(target)})"

    def markdown_image(match: re.Match[str]) -> str:
        alt, target = match.group(1).strip(), match.group(2).strip()
        if "/Attachments/" not in target and not target.lower().startswith("attachments/"):
            return match.group(0)
        alt = "Captura" if alt in {"\\1", "1", ""} else alt
        return f"![{alt}]({attachment_url(target)})"

    def markdown_link(match: re.Match[str]) -> str:
        label_text, target = match.group(1).strip(), match.group(2).strip()
        if "/Attachments/" in target or target.lower().startswith("attachments/"):
            return f"[{label_text}]({attachment_url(target)})"
        return f"[{label_text}]({vault_link_url(source_path, target)})"

    text = replace_outside_fences(text, r"!\[\[([^\]]+)\]\]", wiki_image)
    text = replace_outside_fences(text, r"!\[([^\]]*)\]\(([^)]+)\)", markdown_image)
    text = replace_outside_fences(text, r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", markdown_link)
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return text.strip()


def machine_summary(machine: dict[str, Any], data: dict[str, Any]) -> str:
    custom = MACHINE_SUMMARIES.get(machine["id"])
    if custom:
        return custom
    techniques = ", ".join(label(data, "techniques", item) for item in machine.get("techniques", [])[:4])
    services = ", ".join(label(data, "services", item) for item in machine.get("services", [])[:3])
    return (
        f"{machine['label']} es una maquina {machine['difficulty']} de DockerLabs "
        f"con foco en {techniques or 'enumeracion y post-explotacion'}"
        f"{' sobre ' + services if services else ''}."
    )


def machine_page(machine: dict[str, Any], data: dict[str, Any]) -> str:
    ports = ", ".join(str(port) for port in machine.get("ports", [])) or "No detectados en texto"
    needs_review = "true" if machine.get("needs_review") else "false"
    chain = []
    for phase in ["enumeration", "initial-access", "post-exploitation", "privilege-escalation"]:
        names = [label(data, "techniques", item) for item in phase_items(machine, data, phase)]
        if phase == "enumeration":
            names += [label(data, "services", item) for item in machine.get("services", [])]
        if phase == "privilege-escalation":
            names += [label(data, "privilege_methods", item) for item in machine.get("privilege_methods", [])]
        if names:
            chain.append(f"- **{phase.replace('-', ' ').title()}**: {', '.join(sorted(set(names)))}")
    chain_text = "\n".join(chain) or "- Cadena pendiente de confirmar con evidencia textual suficiente."
    source = (ROOT / machine["source_path"]).read_text(encoding="utf-8", errors="replace")
    writeup = normalize_writeup_markdown(source, machine["label"], machine["source_path"])
    relation_sections = "\n".join(
        section
        for section in [
            optional_section("Cadena de ataque detectada", chain_text),
            optional_section("Tecnicas utilizadas", links(machine.get("techniques", []), "techniques", data)),
            optional_section("Herramientas utilizadas", links(machine.get("tools", []), "tools", data)),
            optional_section("Servicios relacionados", links(machine.get("services", []), "services", data)),
            optional_section("Vulnerabilidades relacionadas", links(machine.get("vulnerabilities", []), "vulnerabilities", data)),
            optional_section("Metodos de escalada", links(machine.get("privilege_methods", []), "privilege_methods", data)),
        ]
        if section.strip()
    )
    return f"""
---
title: {machine['label']}
node_type: machine
platform: dockerlabs
difficulty: {machine['difficulty']}
os: {machine['os']}
source_path: {machine['source_path']}
needs_review: {needs_review}
---

# {machine['label']}

## Resumen

{machine_summary(machine, data)}

Fuente original: [{machine['source_path']}]({source_url(machine['source_path'])})

## Datos clave

| Campo | Valor |
|---|---|
| Plataforma | DockerLabs |
| Dificultad | {machine['difficulty']} |
| Sistema operativo | {machine['os']} |
| Puertos detectados por texto | {ports} |
| Imagenes en fuente | {machine.get('image_count', 0)} |
| Palabras en fuente | {machine.get('word_count', 0)} |
| Requiere revision | {needs_review} |

## Resolucion paso a paso

{writeup}

{relation_sections}
"""


def technique_page(item: dict[str, str], data: dict[str, Any]) -> str:
    machines = related_machines(item["id"], "techniques", data)
    tools = sorted({tool for machine in machines for tool in machine.get("tools", [])})
    services = sorted({service for machine in machines for service in machine.get("services", [])})
    commands = [command for machine in machines for command in machine.get("commands", [])[:1]]
    description = TECHNIQUE_DESCRIPTIONS.get(
        item["id"],
        "Tecnica observada en BanditBox y conectada a maquinas donde existe evidencia textual suficiente.",
    )
    return f"""
---
title: {item['label']}
node_type: technique
---

# {item['label']}

## Descripcion

{description}

## Uso en laboratorio

Usarla solo en laboratorios propios, CTFs o entornos con autorizacion explicita. La evidencia debe separar enumeracion, explotacion y post-explotacion para que la ruta sea reproducible.

## Metodologia minima

- Identificar superficie y prerequisitos.
- Confirmar la tecnica con evidencia reproducible.
- Documentar payloads, errores y condiciones.
- Conectar la causa raiz con mitigaciones defensivas.

## Comandos

{commands_markdown(commands)}

## Herramientas relacionadas

{links(tools, 'tools', data)}

## Servicios relacionados

{links(services, 'services', data)}

## Maquinas que utilizan esta tecnica

{machine_links(machines)}
"""


def tool_page(item: dict[str, str], data: dict[str, Any]) -> str:
    machines = related_machines(item["id"], "tools", data)
    techniques = sorted({tech for machine in machines for tech in machine.get("techniques", [])})
    commands = [command for machine in machines for command in machine.get("commands", [])[:1]]
    phase = data["canonical"]["tools"].get(item["id"], {}).get("phase", "operacion")
    return f"""
---
title: {item['label']}
node_type: tool
---

# {item['label']}

## Proposito

{item['label']} aparece en BanditBox como herramienta de apoyo para la fase de {phase}. La pagina agrupa maquinas y tecnicas donde la herramienta tiene evidencia de uso o mencion relevante.

## Uso operativo

Mantener el uso dentro de laboratorios autorizados, registrar comandos reproducibles y separar pruebas de enumeracion de acciones que cambian estado en el objetivo.

## Comandos comunes

{commands_markdown(commands)}

## Uso dentro de este repositorio

{machine_links(machines)}

## Maquinas relacionadas

{machine_links(machines)}

## Tecnicas relacionadas

{links(techniques, 'techniques', data)}
"""


def service_page(item: dict[str, str], data: dict[str, Any]) -> str:
    machines = related_machines(item["id"], "services", data)
    techniques = sorted({tech for machine in machines for tech in machine.get("techniques", [])})
    tools = sorted({tool for machine in machines for tool in machine.get("tools", [])})
    enum = data["canonical"]["services"].get(item["id"], {}).get("enumeration", [])
    vulnerabilities = sorted(
        vuln_id
        for vuln_id, vuln in data["canonical"]["vulnerabilities"].items()
        if any(tech in vuln.get("techniques", []) for tech in techniques)
    )
    return f"""
---
title: {item['label']}
node_type: service
---

# {item['label']}

## Descripcion

{SERVICE_DESCRIPTIONS.get(item['id'], 'Servicio o tecnologia observado en maquinas de BanditBox. La pagina conecta enumeracion, tecnicas y laboratorios donde aparece.')}

## Lista de verificacion de enumeracion

{links(enum, 'techniques', data)}

## Vulnerabilidades comunes

{links(vulnerabilities, 'vulnerabilities', data)}

## Herramientas comunes

{links(tools, 'tools', data)}

## Maquinas relacionadas

{machine_links(machines)}

## Tecnicas relacionadas

{links(techniques, 'techniques', data)}
"""


def node_page(group: str, item: dict[str, str], data: dict[str, Any]) -> str:
    machines = related_machines(item["id"], group, data)
    if group == "vulnerabilities":
        guidance = VULNERABILITY_GUIDANCE.get(item["id"], {})
        signals = "\n".join(f"- {signal}" for signal in guidance.get("signals", [])) or "- Senales no catalogadas todavia."
        links_text = "\n".join(f"- [{url}]({url})" for url in guidance.get("links", [])) or "- Sin guia externa asociada."
        return f"""
---
title: {item['label']}
node_type: vulnerability
---

# {item['label']}

## Descripcion

{guidance.get('description', 'Vulnerabilidad detectada por relaciones del grafo de BanditBox.')}

## Senales de deteccion

{signals}

## Mitigacion

{guidance.get('mitigation', 'Aplicar minimo privilegio, validacion estricta y revision de configuracion segun el servicio afectado.')}

## Guias externas

{links_text}

## Maquinas relacionadas

{machine_links(machines)}
"""
    if group == "privilege_methods":
        description = PRIVILEGE_METHOD_DESCRIPTIONS.get(
            item["id"],
            "Metodo de escalada observado en BanditBox y asociado a evidencia textual de los writeups.",
        )
        return f"""
---
title: {item['label']}
node_type: privilege_method
---

# {item['label']}

## Descripcion

{description}

## Uso dentro de BanditBox

{machine_links(machines)}
"""
    return f"""
---
title: {item['label']}
node_type: {group}
---

# {item['label']}

## Descripcion

Nodo del modelo de conocimiento usado para conectar contenido relacionado.

## Maquinas relacionadas

{machine_links(machines)}
"""


def index_page(title: str, description: str, entries: list[str]) -> str:
    body = "\n".join(entries) if entries else "- Sin entradas generadas."
    return f"# {title}\n\n{description}\n\n{body}\n"


def write_indexes(data: dict[str, Any]) -> None:
    machines = data["nodes"]["machines"]
    write_generated(
        DOCS / "machines/index.md",
        index_page(
            "Machines",
            "Indice logico de laboratorios convertidos en nodos de conocimiento.",
            [f"- [{m['label']}]({page_url(m['page_path'])}) - {m['difficulty']}" for m in sorted(machines, key=lambda x: x["label"].lower())],
        ),
    )
    for group, title in [
        ("techniques", "Techniques"),
        ("tools", "Tools"),
        ("services", "Services"),
        ("vulnerabilities", "Vulnerabilities"),
        ("privilege_methods", "Privilege escalation methods"),
    ]:
        write_generated(
            DOCS / group / "index.md",
            index_page(title, f"Indice de {title.lower()} detectados en BanditBox.", [f"- [{item['label']}]({page_url(group + '/' + item['id'] + '.md')})" for item in data["nodes"].get(group, [])]),
        )


def write_section_pages() -> None:
    pages = {
        "index.md": """# BanditBox

Base de conocimiento de ciberseguridad ofensiva en entornos controlados.

## Entradas principales

- [Machines](machines/index.md)
- [Techniques](techniques/index.md)
- [Tools](tools/index.md)
- [Services](services/index.md)
- [Knowledge graph](knowledge-graph.md)
- [Learning paths](learning-paths/index.md)

!!! warning "Uso etico"
    Este material debe utilizarse solo en laboratorios propios, CTFs o entornos donde tengas autorizacion explicita.
""",
        "web/index.md": "# Web security\n\nNodos relacionados con enumeracion y explotacion web.\n\n- [Web exploitation](/learning-paths/web-exploitation/)\n- [SQL Injection](/techniques/sql-injection/)\n- [Local File Inclusion](/techniques/lfi/)\n- [Remote Code Execution](/techniques/rce/)\n",
        "linux/index.md": "# Linux\n\nConceptos Linux reutilizables dentro de BanditBox.\n\n- [TTY stabilization](/techniques/tty-stabilization/)\n- [SUID abuse](/techniques/suid-abuse/)\n- [sudo abuse](/techniques/sudo-abuse/)\n",
        "privilege-escalation/index.md": "# Privilege escalation\n\nIndice editorial de escalada de privilegios.\n\n- [Privilege escalation methods](/privilege_methods/)\n- [Linux privilege escalation path](/learning-paths/linux-privilege-escalation/)\n",
        "malware-analysis/index.md": "# Malware analysis\n\nNo se detecto una seccion explicita de analisis de malware en el contenido actual. Esta pagina queda reservada para futuras notas.\n",
        "references/index.md": "# References\n\nReferencias internas, mapa de fuentes y metadatos generados.\n\n- [Content inventory](/_meta/content_inventory/)\n- [Relationship model](/_meta/relationship_model/)\n",
    }
    for path, content in pages.items():
        write_generated(DOCS / path, content)


def write_learning_paths(data: dict[str, Any]) -> None:
    write_generated(DOCS / "learning-paths/index.md", "# Learning paths\n\n- [Enumeration methodology](enumeration-methodology.md)\n- [Web exploitation](web-exploitation.md)\n- [Linux privilege escalation](linux-privilege-escalation.md)\n- [Active Directory](active-directory.md)\n")
    write_generated(DOCS / "learning-paths/enumeration-methodology.md", "# Enumeration methodology\n\n## Objetivo\n\nConstruir una rutina consistente antes de explotar cualquier maquina.\n\n## Ruta sugerida\n\n1. Verificar conectividad.\n2. Enumerar puertos y servicios.\n3. Fingerprinting web si hay HTTP/HTTPS.\n4. Enumerar credenciales, directorios, CMS o servicios especificos.\n5. Documentar evidencia y relaciones.\n\n## Nodos relacionados\n\n- [Port enumeration](/techniques/port-enumeration/)\n- [Web enumeration](/techniques/web-enumeration/)\n- [Nmap](/tools/nmap/)\n- [WhatWeb](/tools/whatweb/)\n")
    web_techs = [t for t in ["sql-injection", "command-injection", "lfi", "rce", "ssti", "malicious-file-upload", "cms-exploitation", "api-abuse"] if any(t == item["id"] for item in data["nodes"].get("techniques", []))]
    write_generated(DOCS / "learning-paths/web-exploitation.md", "# Web exploitation\n\n## Objetivo\n\nRelacionar servicios web con tecnicas de explotacion vistas en BanditBox.\n\n## Tecnicas\n\n" + links(web_techs, "techniques", data))
    pe = [t for t in ["suid-abuse", "sudo-abuse", "python-library-hijacking", "process-abuse", "tty-stabilization", "hash-cracking"] if any(t == item["id"] for item in data["nodes"].get("techniques", []))]
    write_generated(DOCS / "learning-paths/linux-privilege-escalation.md", "# Linux privilege escalation\n\n## Objetivo\n\nConectar conceptos Linux con rutas reales de escalada documentadas en BanditBox.\n\n## Tecnicas\n\n" + links(pe, "techniques", data))
    write_generated(DOCS / "learning-paths/active-directory.md", "# Active Directory\n\n## Estado actual\n\nEl repositorio contiene notas relacionadas con SMB, rpcclient y CrackMapExec, pero no se detecto una ruta completa de Active Directory en las maquinas actuales.\n\n## Base disponible\n\n- [SMB / Samba](/services/smb/)\n- [rpcclient](/tools/rpcclient/)\n- [CrackMapExec](/tools/crackmapexec/)\n")


def write_graph(data: dict[str, Any]) -> None:
    graph = ["graph TD"]
    for machine in data["nodes"]["machines"]:
        mid = "M_" + re.sub(r"[^A-Za-z0-9]", "_", machine["id"])
        graph.append(f"  {mid}[{machine['label']}]")
        for group, prefix, limit in [("techniques", "T", 5), ("tools", "O", 4), ("services", "S", 4)]:
            for item in machine.get(group, [])[:limit]:
                node_id = prefix + "_" + re.sub(r"[^A-Za-z0-9]", "_", item)
                graph.append(f"  {node_id}[{label(data, group, item)}]")
                graph.append(f"  {mid} --> {node_id}")
    service_enum = ["graph LR"]
    for item in data["nodes"].get("services", []):
        sid = "S_" + re.sub(r"[^A-Za-z0-9]", "_", item["id"])
        for enum in data["canonical"]["services"].get(item["id"], {}).get("enumeration", []):
            eid = "E_" + re.sub(r"[^A-Za-z0-9]", "_", enum)
            service_enum.append(f"  {sid}[{item['label']}] --> {eid}[{label(data, 'techniques', enum)}]")
    content = f"""# Knowledge graph

Este grafo resume relaciones generadas desde evidencia textual del repositorio. Las relaciones inciertas se mantienen marcadas con `needs_review`.

## Maquinas, tecnicas, herramientas y servicios

```mermaid
{chr(10).join(graph)}
```

## Servicios y enumeracion

```mermaid
{chr(10).join(service_enum)}
```

## Escalada de privilegios y Linux

```mermaid
graph LR
  Linux[Linux concepts] --> SUID[SUID]
  Linux --> sudo[sudo]
  Linux --> PATH[PATH and libraries]
  Linux --> Processes[Processes]
  SUID --> GTFOBins[GTFOBins]
  SUID --> Binaries[Linux binaries]
  sudo --> Binaries
  PATH --> PythonHijacking[Python Library Hijacking]
  Processes --> ProcessAbuse[Process abuse]
```

## Estadisticas

| Relacion | Conteo |
|---|---:|
| Maquina -> tecnica | {data['stats']['edges_machine_technique']} |
| Maquina -> herramienta | {data['stats']['edges_machine_tool']} |
| Maquina -> servicio | {data['stats']['edges_machine_service']} |
"""
    write_generated(DOCS / "knowledge-graph.md", content)


def write_meta_docs(data: dict[str, Any]) -> None:
    rows = [
        f"| {m['label']} | {m['difficulty']} | {m['os']} | {', '.join(map(str, m['ports'])) or 'No detectados'} | {len(m['techniques'])} | {len(m['tools'])} | {len(m['services'])} |"
        for m in data["nodes"]["machines"]
    ]
    write_generated(DOCS / "_meta/content_inventory.md", "# Content inventory\n\n| Machine | Difficulty | OS | Ports | Techniques | Tools | Services |\n|---|---|---|---|---:|---:|---:|\n" + "\n".join(rows))
    write_generated(DOCS / "_meta/relationship_model.md", "# Relationship model\n\n## Principios\n\n- Precision sobre cobertura.\n- Toda relacion curada debe tener fase, confianza y evidencia.\n- Las relaciones automaticas son punto de partida, no verdad absoluta.\n- Si la informacion es incierta, marcar `needs_review` y explicar la razon.\n\n## Tipos de nodos\n\n- Machine\n- Technique\n- Tool\n- Service\n- Vulnerability\n- Privilege method\n- Learning path\n\n## Relacion recomendada\n\n```yaml\nid: sql-injection\nrelation: used\nconfidence: high\nevidence: explicit-text\nphase: initial-access\n```\n")


def write_mkdocs(data: dict[str, Any]) -> None:
    machine_nav = []
    for diff in ["muy-facil", "facil"]:
        entries = [f"        - {m['label']}: {m['page_path']}" for m in sorted([x for x in data["nodes"]["machines"] if x["difficulty"] == diff], key=lambda x: x["label"].lower())]
        if entries:
            machine_nav.append(f"      - {diff}:\n" + "\n".join(entries))

    def nav_group(title: str, group: str) -> str:
        entries = [f"      - {item['label']}: {group}/{item['id']}.md" for item in data["nodes"].get(group, [])]
        return f"  - {title}:\n      - Overview: {group}/index.md\n" + "\n".join(entries)

    mkdocs = f"""site_name: BanditBox
site_description: Knowledge base de ciberseguridad ofensiva en laboratorios controlados
repo_url: https://github.com/8andit0/BanditBox
repo_name: 8andit0/BanditBox

theme:
  name: material
  language: es
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.indexes
    - navigation.top
    - toc.follow
    - search.suggest
    - search.highlight
    - content.code.copy

plugins:
  - search

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true
  - pymdownx.details
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true

nav:
  - Inicio: index.md
  - Knowledge graph: knowledge-graph.md
  - Learning paths:
      - Overview: learning-paths/index.md
      - Enumeration methodology: learning-paths/enumeration-methodology.md
      - Web exploitation: learning-paths/web-exploitation.md
      - Linux privilege escalation: learning-paths/linux-privilege-escalation.md
      - Active Directory: learning-paths/active-directory.md
  - Machines:
      - Overview: machines/index.md
{chr(10).join(machine_nav)}
{nav_group('Techniques', 'techniques')}
{nav_group('Tools', 'tools')}
{nav_group('Services', 'services')}
{nav_group('Vulnerabilities', 'vulnerabilities')}
{nav_group('Privilege methods', 'privilege_methods')}
  - Web: web/index.md
  - Linux: linux/index.md
  - Privilege escalation: privilege-escalation/index.md
  - Malware analysis: malware-analysis/index.md
  - References:
      - Overview: references/index.md
      - Content inventory: _meta/content_inventory.md
      - Relationship model: _meta/relationship_model.md
"""
    (ROOT / "mkdocs.yml").write_text(mkdocs, encoding="utf-8")
    (ROOT / "requirements.txt").write_text("mkdocs>=1.6,<2.0\nmkdocs-material>=9.5,<10.0\npymdown-extensions>=10.8\n", encoding="utf-8")


def relativize_internal_links() -> None:
    for path in DOCS.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")

        def repl(match: re.Match[str]) -> str:
            label_text, target = match.group(1), match.group(2)
            clean = target.strip("/")
            candidate = DOCS / clean
            if candidate.is_dir():
                candidate = candidate / "index.md"
            elif candidate.suffix == "":
                candidate = candidate.with_suffix(".md")
            if not candidate.exists():
                return match.group(0)
            relative = os.path.relpath(candidate, path.parent).replace("\\", "/")
            return f"[{label_text}]({relative})"

        updated = re.sub(r"(?<!!)\[([^\]]+)\]\(/([^)]+)\)", repl, text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def main() -> None:
    data = read_relationships()
    write_section_pages()
    for machine in data["nodes"]["machines"]:
        write_generated(DOCS / machine["page_path"], machine_page(machine, data))
    write_indexes(data)
    for item in data["nodes"].get("techniques", []):
        write_generated(DOCS / "techniques" / f"{item['id']}.md", technique_page(item, data))
    for item in data["nodes"].get("tools", []):
        write_generated(DOCS / "tools" / f"{item['id']}.md", tool_page(item, data))
    for item in data["nodes"].get("services", []):
        write_generated(DOCS / "services" / f"{item['id']}.md", service_page(item, data))
    for group in ["vulnerabilities", "privilege_methods"]:
        for item in data["nodes"].get(group, []):
            write_generated(DOCS / group / f"{item['id']}.md", node_page(group, item, data))
    write_learning_paths(data)
    write_graph(data)
    write_meta_docs(data)
    write_mkdocs(data)
    relativize_internal_links()
    print("generated MkDocs knowledge base")


if __name__ == "__main__":
    main()

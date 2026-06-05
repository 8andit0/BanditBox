from __future__ import annotations

import re
import os
from pathlib import Path
from typing import Any

from kb_common import DOCS, ROOT, commands_markdown, label, read_relationships, write_generated

GITHUB_BASE = "https://github.com/8andit0/BanditBox/blob/main"


def page_url(path: str) -> str:
    return "/" + path.replace(".md", "/")


def source_url(path: str) -> str:
    return f"{GITHUB_BASE}/{path.replace(' ', '%20')}"


def links(items: list[str], group: str, data: dict[str, Any]) -> str:
    if not items:
        return "- TODO: informacion no confirmada en el contenido actual."
    return "\n".join(f"- [{label(data, group, item)}](/{group}/{item}/)" for item in items)


def machine_links(machines: list[dict[str, Any]]) -> str:
    if not machines:
        return "- TODO: no hay maquinas relacionadas confirmadas."
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


def machine_page(machine: dict[str, Any], data: dict[str, Any]) -> str:
    ports = ", ".join(str(port) for port in machine.get("ports", [])) or "TODO"
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
    chain_text = "\n".join(chain) or "- TODO: completar cadena de ataque con revision manual."
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

Nodo de maquina DockerLabs generado a partir de la nota original. Esta pagina no reemplaza el writeup completo: resume relaciones verificables y deja TODO donde falta revision manual.

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

## Cadena de ataque

{chain_text}

## Enumeracion

{links(phase_items(machine, data, 'enumeration'), 'techniques', data)}

## Explotacion

{links(phase_items(machine, data, 'initial-access'), 'techniques', data)}

## Escalada de privilegios

{links(machine.get('privilege_methods', []), 'privilege_methods', data)}

## Herramientas utilizadas

{links(machine.get('tools', []), 'tools', data)}

## Herramientas mencionadas

{links(machine.get('mentioned_tools', []), 'tools', data)}

## Tecnicas utilizadas

{links(machine.get('techniques', []), 'techniques', data)}

## Servicios relacionados

{links(machine.get('services', []), 'services', data)}

## Notas relacionadas

- [Knowledge graph](/knowledge-graph/)
- [Enumeration methodology](/learning-paths/enumeration-methodology/)
- [Web exploitation](/learning-paths/web-exploitation/)
- [Linux privilege escalation](/learning-paths/linux-privilege-escalation/)

## Lecciones aprendidas

TODO: sintetizar aprendizajes especificos despues de migrar editorialmente el writeup completo.

## PENDIENTE

- TODO: revisar capturas para confirmar datos que no aparecen como texto.
- TODO: migrar la narrativa paso a paso desde la nota original.
- TODO: anadir mitigaciones defensivas especificas.
"""


def technique_page(item: dict[str, str], data: dict[str, Any]) -> str:
    machines = related_machines(item["id"], "techniques", data)
    tools = sorted({tool for machine in machines for tool in machine.get("tools", [])})
    services = sorted({service for machine in machines for service in machine.get("services", [])})
    commands = [command for machine in machines for command in machine.get("commands", [])[:1]]
    return f"""
---
title: {item['label']}
node_type: technique
---

# {item['label']}

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

{commands_markdown(commands)}

## Errores comunes

- Confundir una mencion con uso real.
- No separar fase de enumeracion y fase de explotacion.
- Omitir mitigaciones.

## Herramientas relacionadas

{links(tools, 'tools', data)}

## Servicios relacionados

{links(services, 'services', data)}

## Maquinas que utilizan esta tecnica

{machine_links(machines)}

## Referencias

- [Knowledge graph](/knowledge-graph/)
- TODO: agregar referencias externas verificadas si aplica.
"""


def tool_page(item: dict[str, str], data: dict[str, Any]) -> str:
    machines = related_machines(item["id"], "tools", data)
    techniques = sorted({tech for machine in machines for tech in machine.get("techniques", [])})
    commands = [command for machine in machines for command in machine.get("commands", [])[:1]]
    return f"""
---
title: {item['label']}
node_type: tool
---

# {item['label']}

## Proposito

Herramienta detectada dentro del repositorio BanditBox. TODO: ampliar proposito y limites de uso.

## Instalacion

TODO: documentar instalacion segura y sistema recomendado.

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

Servicio o tecnologia observado en maquinas de BanditBox. TODO: ampliar versionado y contexto.

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
    return f"""
---
title: {item['label']}
node_type: {group}
---

# {item['label']}

## Descripcion

Nodo generado para completar el modelo de conocimiento.

## Maquinas relacionadas

{machine_links(machines)}

## PENDIENTE

- TODO: ampliar contenido manualmente.
- TODO: confirmar evidencia antes de marcar este nodo como estable.
"""


def index_page(title: str, description: str, entries: list[str]) -> str:
    body = "\n".join(entries) if entries else "- TODO: sin entradas generadas."
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
        "malware-analysis/index.md": "# Malware analysis\n\nTODO: no se detecto una seccion explicita de analisis de malware en el contenido actual. Esta pagina queda reservada para futuras notas.\n",
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
    write_generated(DOCS / "learning-paths/active-directory.md", "# Active Directory\n\n## Estado actual\n\nTODO: el repositorio contiene notas relacionadas con SMB, rpcclient y CrackMapExec, pero no se detecto una ruta completa de Active Directory en las maquinas actuales.\n\n## Base disponible\n\n- [SMB / Samba](/services/smb/)\n- [rpcclient](/tools/rpcclient/)\n- [CrackMapExec](/tools/crackmapexec/)\n")


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

Este grafo resume relaciones generadas desde evidencia textual del repositorio. Las relaciones inciertas se mantienen como TODO o `needs_review`.

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
        f"| {m['label']} | {m['difficulty']} | {m['os']} | {', '.join(map(str, m['ports'])) or 'TODO'} | {len(m['techniques'])} | {len(m['tools'])} | {len(m['services'])} |"
        for m in data["nodes"]["machines"]
    ]
    write_generated(DOCS / "_meta/content_inventory.md", "# Content inventory\n\n| Machine | Difficulty | OS | Ports | Techniques | Tools | Services |\n|---|---|---|---|---:|---:|---:|\n" + "\n".join(rows))
    write_generated(DOCS / "_meta/relationship_model.md", "# Relationship model\n\n## Principios\n\n- Precision sobre cobertura.\n- Toda relacion curada debe tener fase, confianza y evidencia.\n- Las relaciones automaticas son punto de partida, no verdad absoluta.\n- Si la informacion es incierta, usar TODO o `needs_review`.\n\n## Tipos de nodos\n\n- Machine\n- Technique\n- Tool\n- Service\n- Vulnerability\n- Privilege method\n- Learning path\n\n## Relacion recomendada\n\n```yaml\nid: sql-injection\nrelation: used\nconfidence: high\nevidence: explicit-text\nphase: initial-access\n```\n")


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

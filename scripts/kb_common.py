from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
META = DOCS / "_meta"
MARKER = "<!-- AUTO-GENERATED: BanditBox knowledge base. Safe to overwrite. -->"

CANONICAL: dict[str, dict[str, dict[str, Any]]] = {
    "techniques": {
        "port-enumeration": {"label": "Port enumeration", "aliases": ["nmap", "puertos abiertos", "escaneo de puertos"], "phase": "enumeration"},
        "connectivity-check": {"label": "Connectivity check", "aliases": ["ping", "icmp", "ttl="], "phase": "enumeration"},
        "web-enumeration": {"label": "Web enumeration", "aliases": ["whatweb", "gobuster", "ffuf", "wfuzz", "burp", "panel", "login", "directorio"], "phase": "enumeration"},
        "sql-injection": {"label": "SQL Injection", "aliases": ["sql injection", "sqli", "union select", "order by", "updatexml", "information_schema"], "phase": "initial-access"},
        "login-bypass": {"label": "Login bypass", "aliases": ["bypass", "saltarnos el panel", "cambiar la logica"], "phase": "initial-access"},
        "command-injection": {"label": "Command Injection", "aliases": ["command injection", "inyeccion de comandos"], "phase": "initial-access"},
        "lfi": {"label": "Local File Inclusion", "aliases": ["lfi", "local file inclusion", "/etc/passwd", "path traversal"], "phase": "initial-access"},
        "rce": {"label": "Remote Code Execution", "aliases": ["rce", "remote command execution"], "phase": "initial-access"},
        "ssti": {"label": "SSTI", "aliases": ["ssti", "server side template", "jinja", "template injection"], "phase": "initial-access"},
        "malicious-file-upload": {"label": "Malicious file upload", "aliases": ["subida de archivos", "web shell", "webshell", "reverse shell"], "phase": "initial-access"},
        "brute-force": {"label": "Brute force", "aliases": ["fuerza bruta", "hydra"], "phase": "initial-access"},
        "credential-extraction": {"label": "Credential extraction", "aliases": ["credenciales", "password", "contrasena", "/etc/shadow", "usuarios"], "phase": "post-exploitation"},
        "hash-cracking": {"label": "Hash cracking", "aliases": ["john", "hash", "md5", "crack"], "phase": "post-exploitation"},
        "metadata-analysis": {"label": "Metadata analysis", "aliases": ["metadatos", "exiftool"], "phase": "enumeration"},
        "steganography": {"label": "Steganography", "aliases": ["esteganografia", "steghide", "binwalk", "strings"], "phase": "enumeration"},
        "suid-abuse": {"label": "SUID abuse", "aliases": ["suid", "permiso 4000", "-perm -4000", "gtfobins"], "phase": "privilege-escalation"},
        "sudo-abuse": {"label": "sudo abuse", "aliases": ["sudo -l", "permisos sudo", "abuso de binario con sudo"], "phase": "privilege-escalation"},
        "python-library-hijacking": {"label": "Python Library Hijacking", "aliases": ["library hijacking", "python library"], "phase": "privilege-escalation"},
        "process-abuse": {"label": "Process abuse", "aliases": ["pspy", "abuso de procesos"], "phase": "privilege-escalation"},
        "tty-stabilization": {"label": "TTY stabilization", "aliases": ["tratamiento de la tty", "stty raw", "script /dev/null", "pty.spawn", "export TERM"], "phase": "post-exploitation"},
        "cms-exploitation": {"label": "CMS exploitation", "aliases": ["joomla", "wordpress", "cms", "gestor de contenido"], "phase": "initial-access"},
        "api-abuse": {"label": "API abuse", "aliases": [" api", "apis"], "phase": "initial-access"},
    },
    "tools": {
        "nmap": {"label": "Nmap", "aliases": ["nmap"], "phase": "enumeration"},
        "ping": {"label": "Ping", "aliases": ["ping", "icmp"], "phase": "enumeration"},
        "burp-suite": {"label": "Burp Suite", "aliases": ["burp suite", "burpsuite", "repeater"], "phase": "initial-access"},
        "sqlmap": {"label": "SQLMap", "aliases": ["sqlmap"], "phase": "initial-access"},
        "hydra": {"label": "Hydra", "aliases": ["hydra"], "phase": "initial-access"},
        "john-the-ripper": {"label": "John the Ripper", "aliases": ["john", "john the ripper"], "phase": "post-exploitation"},
        "ciberchef": {"label": "CiberChef", "aliases": ["ciberchef", "cyberchef"], "phase": "analysis"},
        "whatweb": {"label": "WhatWeb", "aliases": ["whatweb"], "phase": "enumeration"},
        "gobuster": {"label": "Gobuster", "aliases": ["gobuster"], "phase": "enumeration"},
        "ffuf-wfuzz": {"label": "FFUF / WFuzz", "aliases": ["ffuf", "wfuzz"], "phase": "enumeration"},
        "searchsploit": {"label": "Searchsploit", "aliases": ["searchsploit"], "phase": "enumeration"},
        "netcat": {"label": "Netcat", "aliases": ["netcat", "nc -", " nc "], "phase": "initial-access"},
        "curl": {"label": "curl", "aliases": ["curl"], "phase": "enumeration"},
        "wget": {"label": "wget", "aliases": ["wget"], "phase": "enumeration"},
        "python": {"label": "Python", "aliases": ["python", "python3"], "phase": "post-exploitation"},
        "gtfobins": {"label": "GTFOBins", "aliases": ["gtfobins"], "phase": "privilege-escalation"},
        "find": {"label": "find", "aliases": ["find ", " find"], "phase": "privilege-escalation"},
        "grep": {"label": "grep", "aliases": ["grep"], "phase": "privilege-escalation"},
        "base64": {"label": "base64", "aliases": ["base64"], "phase": "analysis"},
        "sudo": {"label": "sudo", "aliases": ["sudo", "sudo -l"], "phase": "privilege-escalation"},
        "ssh": {"label": "ssh", "aliases": ["ssh", "openssh"], "phase": "initial-access"},
        "rpcclient": {"label": "rpcclient", "aliases": ["rpcclient"], "phase": "enumeration"},
        "smbclient": {"label": "smbclient", "aliases": ["smbclient"], "phase": "enumeration"},
        "crackmapexec": {"label": "CrackMapExec", "aliases": ["crackmapexec", "cme"], "phase": "enumeration"},
        "exiftool": {"label": "ExifTool", "aliases": ["exiftool"], "phase": "analysis"},
        "steghide": {"label": "steghide", "aliases": ["steghide"], "phase": "analysis"},
        "binwalk": {"label": "binwalk", "aliases": ["binwalk"], "phase": "analysis"},
        "strings": {"label": "strings", "aliases": ["strings"], "phase": "analysis"},
        "nodejs": {"label": "Node.js", "aliases": ["node.js", "nodejs", "node "], "phase": "privilege-escalation"},
        "vim": {"label": "Vim", "aliases": ["binario vim", "sudo vim", "/usr/bin/vim"], "phase": "privilege-escalation"},
        "nano": {"label": "nano", "aliases": ["binario nano", "sudo nano", "/usr/bin/nano"], "phase": "privilege-escalation"},
        "ruby": {"label": "Ruby", "aliases": ["ruby"], "phase": "privilege-escalation"},
        "dd": {"label": "dd", "aliases": [" dd ", "binario dd"], "phase": "privilege-escalation"},
        "env": {"label": "env", "aliases": [" env ", "binario env"], "phase": "privilege-escalation"},
    },
    "services": {
        "ssh": {"label": "SSH", "aliases": ["ssh", "openssh", "puerto 22"], "enumeration": ["port-enumeration", "brute-force"]},
        "http": {"label": "HTTP", "aliases": ["http", "web", "puerto 80"], "enumeration": ["web-enumeration"]},
        "apache": {"label": "Apache", "aliases": ["apache"], "enumeration": ["web-enumeration"]},
        "nginx": {"label": "Nginx", "aliases": ["nginx"], "enumeration": ["web-enumeration"]},
        "mariadb-mysql": {"label": "MariaDB / MySQL", "aliases": ["mariadb", "mysql", "information_schema"], "enumeration": ["sql-injection"]},
        "ftp": {"label": "FTP", "aliases": ["ftp", "puerto 21"], "enumeration": ["port-enumeration", "brute-force"]},
        "smb": {"label": "SMB / Samba", "aliases": ["smb", "samba", "rpcclient", "smbclient", "445"], "enumeration": ["port-enumeration"]},
        "jenkins": {"label": "Jenkins", "aliases": ["jenkins"], "enumeration": ["web-enumeration"]},
        "grafana": {"label": "Grafana", "aliases": ["grafana"], "enumeration": ["web-enumeration"]},
        "tomcat": {"label": "Tomcat", "aliases": ["tomcat", "8009", "8080"], "enumeration": ["web-enumeration"]},
        "joomla": {"label": "Joomla", "aliases": ["joomla"], "enumeration": ["web-enumeration", "cms-exploitation"]},
        "php": {"label": "PHP", "aliases": ["php"], "enumeration": ["web-enumeration"]},
        "nodejs-service": {"label": "Node.js service", "aliases": ["node.js", "nodejs"], "enumeration": ["web-enumeration"]},
        "api": {"label": "API", "aliases": [" api", "apis"], "enumeration": ["web-enumeration", "api-abuse"]},
    },
    "vulnerabilities": {
        "unsanitized-user-input": {"label": "Unsanitized user input", "techniques": ["sql-injection", "command-injection", "ssti"]},
        "exposed-error-message": {"label": "Exposed error message", "techniques": ["sql-injection", "lfi"]},
        "weak-credentials": {"label": "Weak credentials", "techniques": ["brute-force", "credential-extraction"]},
        "insecure-file-upload": {"label": "Insecure file upload", "techniques": ["malicious-file-upload", "rce"]},
        "suid-misconfiguration": {"label": "SUID misconfiguration", "techniques": ["suid-abuse"]},
        "sudo-misconfiguration": {"label": "sudo misconfiguration", "techniques": ["sudo-abuse"]},
        "secret-in-metadata": {"label": "Secret in metadata", "techniques": ["metadata-analysis", "steganography"]},
    },
    "privilege_methods": {
        "suid-binary-abuse": {"label": "SUID binary abuse", "techniques": ["suid-abuse"]},
        "sudo-binary-abuse": {"label": "sudo binary abuse", "techniques": ["sudo-abuse"]},
        "python-library-hijacking": {"label": "Python Library Hijacking", "techniques": ["python-library-hijacking"]},
        "process-abuse": {"label": "Process abuse", "techniques": ["process-abuse"]},
        "hash-cracking-to-root": {"label": "Hash cracking to root", "techniques": ["hash-cracking", "credential-extraction"]},
    },
}


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.replace("\ufeff", ""))
    return "".join(ch for ch in value if not unicodedata.combining(ch)).lower()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", normalize(value)).strip("-") or "untitled"


def detect(text: str, group: str) -> list[str]:
    normalized = normalize(text)
    found = []
    for item_id, item in CANONICAL[group].items():
        matched = False
        for alias in item.get("aliases", []):
            needle = normalize(alias)
            if re.fullmatch(r"[a-z0-9]{2,5}", needle):
                matched = bool(re.search(rf"\b{re.escape(needle)}\b", normalized))
            else:
                matched = needle in normalized
            if matched:
                break
        if matched:
            found.append(item_id)
    return sorted(set(found))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def detect_ports(text: str) -> list[int]:
    ports = set()
    for match in re.finditer(r"(?i)(?:puerto|puertos)\s+(\d{1,5})|\b(\d{1,5})/tcp\b", text):
        for value in match.groups():
            if value and 0 < int(value) <= 65535:
                ports.add(int(value))
    return sorted(ports)


def code_fences(text: str, limit: int = 6) -> list[str]:
    blocks = []
    for match in re.finditer(r"```(?:\w+)?\n(.*?)```", text, re.S):
        block = match.group(1).strip()
        if block and len(block) < 700:
            blocks.append(block)
    return blocks[:limit]


def technique_vulnerabilities() -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    for vuln_id, data in CANONICAL["vulnerabilities"].items():
        for technique_id in data.get("techniques", []):
            mapping.setdefault(technique_id, []).append(vuln_id)
    return mapping


def machine_record(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    source_path = rel(path)
    difficulty = "muy-facil" if "Maquinas Muy Faciles" in source_path else "facil" if "Maquinas Faciles" in source_path else "todo"
    techniques = detect(text, "techniques")
    tools = detect(text, "tools")
    mentioned_tools = []
    normalized = normalize(text)
    if "sqlmap" in tools and ("manual" in normalized or "automatizada" in normalized):
        tools.remove("sqlmap")
        mentioned_tools.append("sqlmap")
    services = detect(text, "services")
    vuln_map = technique_vulnerabilities()
    vulnerabilities = sorted({v for t in techniques for v in vuln_map.get(t, [])})
    privilege_methods = []
    if "suid-abuse" in techniques:
        privilege_methods.append("suid-binary-abuse")
    if "sudo-abuse" in techniques:
        privilege_methods.append("sudo-binary-abuse")
    if "python-library-hijacking" in techniques:
        privilege_methods.append("python-library-hijacking")
    if "process-abuse" in techniques:
        privilege_methods.append("process-abuse")
    if "hash-cracking" in techniques:
        privilege_methods.append("hash-cracking-to-root")
    return {
        "id": slugify(path.stem),
        "label": path.stem.replace("_", " "),
        "source_path": source_path,
        "page_path": f"machines/dockerlabs/{difficulty}/{slugify(path.stem)}.md",
        "platform": "dockerlabs",
        "difficulty": difficulty,
        "os": "linux" if any(t in normalize(text) for t in ["/etc/passwd", "/etc/shadow", "sudo", "suid", "/bin/bash", "root", "dockerlabs"]) else "todo",
        "ports": detect_ports(text),
        "services": services,
        "tools": tools,
        "mentioned_tools": sorted(set(mentioned_tools)),
        "techniques": techniques,
        "vulnerabilities": vulnerabilities,
        "privilege_methods": sorted(set(privilege_methods)),
        "commands": code_fences(text),
        "word_count": len(re.findall(r"\w+", text)),
        "image_count": len(re.findall(r"!\[[^\]]*\]\([^)]+\)|!\[\[[^\]]+\]\]", text)),
        "needs_review": bool(not techniques or not services),
    }


def source_note_record(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    combined = f"{path.stem}\n{text}"
    return {
        "id": slugify(path.stem),
        "label": path.stem.replace("_", " "),
        "source_path": rel(path),
        "techniques": detect(combined, "techniques"),
        "tools": detect(combined, "tools"),
        "services": detect(combined, "services"),
        "commands": code_fences(text),
    }


def build_relationships() -> dict[str, Any]:
    machines = [machine_record(path) for path in sorted((ROOT / "Maquinas De Dockerlabs").rglob("*.md"))]
    notes = []
    for folder in ["Conceptos Y Herramientas", "Explotaciones", "Escalada De Privilegios"]:
        notes.extend(source_note_record(path) for path in sorted((ROOT / folder).rglob("*.md")))
    used = {group: set() for group in ["techniques", "tools", "services", "vulnerabilities", "privilege_methods"]}
    for machine in machines:
        for group in used:
            used[group].update(machine.get(group, []))
        used["tools"].update(machine.get("mentioned_tools", []))
    for note in notes:
        for group in ["techniques", "tools", "services"]:
            used[group].update(note.get(group, []))
        if "process-abuse" in note.get("techniques", []) or "abuso-de-procesos" in note.get("id", ""):
            used["privilege_methods"].add("process-abuse")
    nodes = {"machines": machines}
    for group in used:
        nodes[group] = [{"id": item_id, "label": CANONICAL[group].get(item_id, {}).get("label", item_id)} for item_id in sorted(used[group])]
    stats = {
        "machines": len(machines),
        "techniques": len(nodes["techniques"]),
        "tools": len(nodes["tools"]),
        "services": len(nodes["services"]),
        "vulnerabilities": len(nodes["vulnerabilities"]),
        "privilege_methods": len(nodes["privilege_methods"]),
        "edges_machine_technique": sum(len(m["techniques"]) for m in machines),
        "edges_machine_tool": sum(len(m["tools"]) for m in machines),
        "edges_machine_service": sum(len(m["services"]) for m in machines),
    }
    return {
        "schema_version": "0.2",
        "generated_by": "scripts/build_relationships.py",
        "policy": {
            "precision_over_coverage": True,
            "uncertain_data": "Use TODO or needs_review fields",
            "manual_content_policy": "Generated scripts only overwrite files with AUTO-GENERATED markers",
        },
        "canonical": CANONICAL,
        "nodes": nodes,
        "source_notes": notes,
        "stats": stats,
    }


def write_generated(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and MARKER not in path.read_text(encoding="utf-8", errors="replace"):
        print(f"SKIP manual file: {path.relative_to(ROOT)}")
        return
    path.write_text(MARKER + "\n\n" + content.strip() + "\n", encoding="utf-8")


def read_relationships() -> dict[str, Any]:
    return json.loads((META / "relationships.json").read_text(encoding="utf-8"))


def label(data: dict[str, Any], group: str, item_id: str) -> str:
    for item in data["nodes"].get(group, []):
        if item["id"] == item_id:
            return item["label"]
    return CANONICAL.get(group, {}).get(item_id, {}).get("label", item_id)


def commands_markdown(commands: list[str]) -> str:
    if not commands:
        return "TODO: extraer comandos relevantes durante la revision manual."
    return "\n\n".join("```bash\n" + command.strip() + "\n```" for command in commands[:5])

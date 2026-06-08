from __future__ import annotations

import json

from kb_common import META, build_relationships


def main() -> None:
    META.mkdir(parents=True, exist_ok=True)
    data = build_relationships()
    (META / "relationships.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (META / "relationships.yml").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    schema = {
        "schema_version": "0.2",
        "required_machine_fields": [
            "title",
            "node_type",
            "platform",
            "difficulty",
            "os",
            "phases",
            "relationships",
            "source_path",
        ],
        "relation_fields": ["id", "relation", "confidence", "evidence", "phase"],
        "confidence_values": ["high", "medium", "low"],
        "evidence_values": ["explicit-text", "screenshot", "inferred", "manual-review"],
        "relation_strength_values": ["primary", "secondary", "mentioned"],
        "rule": "Use needs_review when a field cannot be supported by repository content.",
    }
    (META / "schema.yml").write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(data["stats"], indent=2))


if __name__ == "__main__":
    main()

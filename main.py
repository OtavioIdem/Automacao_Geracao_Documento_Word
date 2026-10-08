"""Gera DOCX com dados JSON somente quando autorizado por --apply."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from docxtpl import DocxTemplate


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(data: dict, required: list[str], source: Path) -> None:
    missing = [field for field in required if not str(data.get(field, "")).strip()]
    if missing:
        raise ValueError(f"Campos obrigatorios ausentes em {source}: {', '.join(missing)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("config.json"))
    parser.add_argument("--apply", action="store_true", help="autoriza a criacao de DOCX")
    args = parser.parse_args()
    config = load_json(args.config)
    template = Path(config["template"])
    sources = sorted(Path(config["data_dir"]).glob("*.json"))
    if not template.exists():
        raise FileNotFoundError(f"Modelo DOCX nao encontrado: {template}")
    for source in sources:
        validate(load_json(source), config["required_fields"], source)
    print(f"Plano: gerar {len(sources)} documento(s) a partir de {template}.")
    if not args.apply:
        print("Simulacao: nenhum documento foi criado.")
        return
    output_dir = Path(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    for source in sources:
        data = load_json(source)
        document = DocxTemplate(template)
        document.render(data)
        output = output_dir / config["output_name_pattern"].format(**data)
        document.save(output)
        print(f"Documento criado: {output}")


if __name__ == "__main__":
    main()

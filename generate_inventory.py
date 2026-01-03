#!/usr/bin/env python3
"""
Script para gerar inventário de workflows Make.com
Baseado no estilo do N8Np
"""

import json
import os
from pathlib import Path
from collections import Counter
from datetime import datetime

DOC_PATH = Path("doc/2277358326")
OUTPUT_FILE = "workflow_inventory.json"

# Categorias baseadas nos módulos Make.com
CATEGORY_MAPPING = {
    "telegram": "Comunicação", "whatsapp": "Comunicação", "email": "Comunicação",
    "gmail": "Comunicação", "outlook": "Comunicação", "smtp": "Comunicação",
    "slack": "Comunicação", "discord": "Comunicação",
    "instagram": "Redes Sociais", "facebook": "Redes Sociais", "linkedin": "Redes Sociais",
    "twitter": "Redes Sociais", "tiktok": "Redes Sociais", "youtube": "Redes Sociais",
    "openai": "IA", "anthropic": "IA", "gpt": "IA", "claude": "IA", "langchain": "IA",
    "hotmart": "Vendas", "stripe": "Vendas", "asaas": "Vendas", "pagarme": "Vendas",
    "pipedrive": "CRM", "hubspot": "CRM", "salesforce": "CRM",
    "google": "Produtividade", "sheets": "Produtividade", "drive": "Produtividade",
    "notion": "Produtividade", "airtable": "Produtividade", "trello": "Produtividade",
    "canva": "Design", "figma": "Design",
    "vapi": "Voice AI", "retell": "Voice AI", "bland": "Voice AI", "synthflow": "Voice AI",
    "http": "Web/API", "webhook": "Web/API", "gateway": "Web/API", "rss": "Web/API",
}

def extract_modules(flow):
    modules = set()
    if not isinstance(flow, list):
        return modules
    for item in flow:
        if isinstance(item, dict) and "module" in item:
            module = item["module"]
            parts = module.split(":")
            for part in parts:
                modules.add(part.lower())
    return modules

def detect_categories(name, modules):
    categories = set()
    search_text = (name + " " + " ".join(modules)).lower()
    for keyword, category in CATEGORY_MAPPING.items():
        if keyword in search_text:
            categories.add(category)
    return list(categories) if categories else ["Outros"]

def find_images(folder):
    images = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif']:
        images.extend(folder.glob(ext))
    return [str(img.relative_to(Path.cwd())) for img in list(images)[:5]]

def main():
    workflows = []
    all_modules = Counter()
    all_categories = Counter()

    print(f"Escaneando {DOC_PATH}...")

    for topic_dir in sorted(DOC_PATH.iterdir()):
        if not topic_dir.is_dir():
            continue

        for bp_file in topic_dir.glob("*.json"):
            if bp_file.name in ['metadata.json', 'messages.json']:
                continue

            try:
                with open(bp_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                flow = data.get("flow", [])
                if not isinstance(flow, list) or len(flow) == 0:
                    continue

                name = data.get("name", bp_file.stem)
                modules = extract_modules(flow)
                categories = detect_categories(name, modules)

                workflow = {
                    "name": name,
                    "file": str(bp_file.relative_to(Path.cwd())),
                    "folder": topic_dir.name,
                    "node_count": len(flow),
                    "modules": list(modules),
                    "categories": categories,
                    "images": find_images(topic_dir),
                    "topic_id": topic_dir.name,
                    "source": "INEMA VIP"
                }
                workflows.append(workflow)

                for mod in modules:
                    all_modules[mod] += 1
                for cat in categories:
                    all_categories[cat] += 1

            except Exception as e:
                continue

    top_modules = [mod for mod, _ in all_modules.most_common(20)]
    categories = {cat: count for cat, count in all_categories.most_common()}

    inventory = {
        "metadata": {
            "total_workflows": len(workflows),
            "total_categories": len(categories),
            "generated_at": datetime.now().isoformat(),
            "source": "INEMA.Make VIP - Telegram"
        },
        "categories": categories,
        "top_modules": top_modules,
        "sources": [{
            "id": "inema-vip",
            "name": "INEMA VIP",
            "color": "#f59e0b",
            "badge": "VIP",
            "link": "https://t.me/+dN1X5kYnfgFkNmQx"
        }],
        "workflows": workflows
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, ensure_ascii=False, indent=2)

    print(f"\nInventário gerado: {OUTPUT_FILE}")
    print(f"Total de workflows: {len(workflows)}")
    print(f"Categorias: {list(categories.keys())}")
    print(f"Top módulos: {top_modules[:10]}")

if __name__ == "__main__":
    main()

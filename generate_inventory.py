#!/usr/bin/env python3
"""
Script para gerar inventario de workflows Make.com
Estilo N8Np VIP - Cataloga blueprints com imagens, nodes e categorias
"""

import json
import os
from pathlib import Path
from collections import Counter
from datetime import datetime
import re

# Usa assets/workflows que e o caminho publicado no GitHub Pages
ASSETS_PATH = Path("assets/workflows")
OUTPUT_FILE = "workflow_inventory.json"

# Categorias baseadas nos modulos Make.com
CATEGORY_MAPPING = {
    # Comunicacao
    "telegram": "Comunicacao", "whatsapp": "Comunicacao", "email": "Comunicacao",
    "gmail": "Comunicacao", "outlook": "Comunicacao", "smtp": "Comunicacao",
    "slack": "Comunicacao", "discord": "Comunicacao", "evolution": "Comunicacao",
    "zapi": "Comunicacao", "z-api": "Comunicacao",

    # Redes Sociais
    "instagram": "Redes Sociais", "facebook": "Redes Sociais", "linkedin": "Redes Sociais",
    "twitter": "Redes Sociais", "tiktok": "Redes Sociais", "youtube": "Redes Sociais",
    "meta": "Redes Sociais", "canva": "Redes Sociais",

    # IA
    "openai": "IA", "anthropic": "IA", "gpt": "IA", "claude": "IA", "langchain": "IA",
    "groq": "IA", "deepseek": "IA", "gemini": "IA", "perplexity": "IA",
    "vectorstore": "IA", "embedding": "IA", "rag": "IA", "pinecone": "IA",

    # Vendas
    "hotmart": "Vendas", "stripe": "Vendas", "asaas": "Vendas", "pagarme": "Vendas",
    "checkout": "Vendas", "payment": "Vendas", "cobranca": "Vendas",

    # CRM
    "pipedrive": "CRM", "hubspot": "CRM", "salesforce": "CRM", "kommo": "CRM",
    "crm": "CRM", "lead": "CRM",

    # Produtividade
    "google": "Produtividade", "sheets": "Produtividade", "drive": "Produtividade",
    "notion": "Produtividade", "airtable": "Produtividade", "trello": "Produtividade",
    "calendar": "Produtividade", "docs": "Produtividade", "dropbox": "Produtividade",

    # Voice AI
    "vapi": "Voice AI", "retell": "Voice AI", "bland": "Voice AI", "synthflow": "Voice AI",
    "elevenlabs": "Voice AI", "voice": "Voice AI",

    # Web/API
    "http": "Web/API", "webhook": "Web/API", "gateway": "Web/API", "rss": "Web/API",
    "api": "Web/API", "json": "Web/API", "scraper": "Web/API", "apify": "Web/API",

    # Automacao
    "router": "Automacao", "iterator": "Automacao", "aggregator": "Automacao",
    "filter": "Automacao", "switch": "Automacao", "flow": "Automacao",
}

def extract_modules_from_flow(flow):
    """Extrai modulos/nodes do flow do blueprint"""
    modules = []
    module_types = set()

    if not isinstance(flow, list):
        return modules, list(module_types)

    for item in flow:
        if isinstance(item, dict) and "module" in item:
            module_full = item["module"]
            module_name = module_full.split(":")[-1] if ":" in module_full else module_full
            module_app = module_full.split(":")[0] if ":" in module_full else module_full

            module_info = {
                "full": module_full,
                "app": module_app.lower(),
                "action": module_name,
                "id": item.get("id", 0)
            }
            modules.append(module_info)
            module_types.add(module_app.lower())

    return modules, list(module_types)

def detect_categories(name, modules):
    """Detecta categorias baseado no nome e modulos"""
    categories = set()
    search_text = (name + " " + " ".join(modules)).lower()

    for keyword, category in CATEGORY_MAPPING.items():
        if keyword in search_text:
            categories.add(category)

    return list(categories) if categories else ["Outros"]

def find_images(folder):
    """Encontra imagens no folder - retorna caminhos relativos para web"""
    images = []
    seen = set()

    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.JPG', '*.JPEG', '*.PNG', '*.GIF']:
        for img in folder.glob(ext):
            # Evita duplicatas (alguns arquivos tem sufixos diferentes)
            base_name = re.sub(r'_\d+\.', '.', img.name.lower())
            if base_name not in seen:
                seen.add(base_name)
                # Caminho relativo para funcionar na web (ex: assets/workflows/1/photo.jpg)
                relative_path = str(img.relative_to(Path(".")))
                images.append({
                    "path": relative_path,
                    "name": img.name
                })

    # Limita a 10 imagens por workflow
    return images[:10]

def get_topic_title(folder):
    """Tenta extrair titulo do topico do content.txt ou messages.json"""
    content_file = folder / "content.txt"
    if content_file.exists():
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                first_lines = f.read(500)
                # Tenta extrair titulo das primeiras linhas
                lines = first_lines.split('\n')
                for line in lines[:5]:
                    line = line.strip()
                    if line and len(line) > 5 and len(line) < 100:
                        # Remove caracteres especiais
                        clean = re.sub(r'[^\w\s\-]', '', line)
                        if clean:
                            return clean[:80]
        except:
            pass
    return None

def main():
    workflows = []
    all_modules = Counter()
    all_categories = Counter()
    all_apps = Counter()

    print(f"Escaneando {ASSETS_PATH}...")

    folders = sorted([d for d in ASSETS_PATH.iterdir() if d.is_dir()])
    print(f"Encontradas {len(folders)} pastas")

    found_count = 0
    for topic_dir in folders:
        # Carrega metadata se existir
        metadata_file = topic_dir / "metadata.json"
        topic_meta = {}
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    topic_meta = json.load(f)
            except:
                pass

        # Procura blueprints JSON
        for bp_file in topic_dir.glob("*.json"):
            if bp_file.name in ['metadata.json', 'messages.json']:
                continue

            try:
                with open(bp_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Verifica se e um blueprint valido (tem flow ou name)
                flow = data.get("flow", [])
                name = data.get("name", bp_file.stem)

                # Pula se nao tem flow ou flow vazio
                if not isinstance(flow, list) or len(flow) == 0:
                    continue

                # Extrai modulos
                modules, module_types = extract_modules_from_flow(flow)

                # Detecta categorias
                categories = detect_categories(name, module_types)

                # Encontra imagens do topico
                images = find_images(topic_dir)

                # Monta objeto do workflow
                # Caminho relativo para web
                relative_bp_path = str(bp_file.relative_to(Path(".")))
                workflow = {
                    "id": f"{topic_dir.name}_{bp_file.stem}",
                    "name": name,
                    "file": bp_file.name,
                    "path": relative_bp_path,
                    "folder": topic_dir.name,
                    "topic_id": topic_meta.get("topic_id", topic_dir.name),
                    "node_count": len(flow),
                    "modules": modules[:20],  # Limita a 20 modulos
                    "module_types": module_types,
                    "categories": categories,
                    "images": images,
                    "image_count": len(images),
                    "source": "INEMA VIP",
                    "source_color": "#f59e0b",
                    "has_telegram": True,
                    "telegram_link": "https://t.me/+dN1X5kYnfgFkNmQx"
                }

                # Adiciona thumbnail (primeira imagem)
                if images:
                    workflow["thumbnail"] = images[0]["path"]

                workflows.append(workflow)
                found_count += 1

                # Contadores
                for mod in module_types:
                    all_modules[mod] += 1
                    all_apps[mod] += 1
                for cat in categories:
                    all_categories[cat] += 1

            except json.JSONDecodeError as e:
                print(f"  JSON Error in {bp_file.name}: {e}")
                continue
            except Exception as e:
                print(f"  Error in {bp_file.name}: {e}")
                continue

    # Top modulos
    top_modules = [{"name": mod, "count": count} for mod, count in all_modules.most_common(30)]

    # Categorias ordenadas
    categories = {cat: count for cat, count in all_categories.most_common()}

    # Monta inventario final
    inventory = {
        "metadata": {
            "total_workflows": len(workflows),
            "total_categories": len(categories),
            "total_folders": len(folders),
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
            "badge_color": "gold",
            "link": "https://t.me/+dN1X5kYnfgFkNmQx",
            "has_telegram": True
        }],
        "workflows": workflows
    }

    # Salva JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Inventario gerado: {OUTPUT_FILE}")
    print(f"Total de workflows: {len(workflows)}")
    print(f"Total de pastas: {len(folders)}")
    print(f"Categorias: {list(categories.keys())}")
    print(f"Top 10 modulos: {[m['name'] for m in top_modules[:10]]}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()

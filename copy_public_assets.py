#!/usr/bin/env python3
"""
Copia imagens e blueprints para pasta publica
Evita duplicatas e organiza por topico
"""

import os
import shutil
import json
import re
from pathlib import Path
from hashlib import md5

DOC_PATH = Path("doc/2277358326")
PUBLIC_PATH = Path("assets/workflows")
OUTPUT_FILE = "workflow_inventory.json"

# Limita imagens por topico para evitar duplicatas
MAX_IMAGES_PER_TOPIC = 5

def get_file_hash(filepath):
    """Calcula hash MD5 do arquivo para detectar duplicatas"""
    with open(filepath, 'rb') as f:
        return md5(f.read()).hexdigest()

def main():
    # Cria pasta publica
    PUBLIC_PATH.mkdir(parents=True, exist_ok=True)

    copied_images = 0
    copied_blueprints = 0
    seen_hashes = set()

    folders = sorted([d for d in DOC_PATH.iterdir() if d.is_dir()])
    print(f"Processando {len(folders)} pastas...")

    for topic_dir in folders:
        topic_id = topic_dir.name
        topic_public = PUBLIC_PATH / topic_id

        # Copia blueprints JSON
        for bp_file in topic_dir.glob("*.json"):
            if bp_file.name in ['metadata.json', 'messages.json']:
                continue

            try:
                with open(bp_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Verifica se e um blueprint valido
                flow = data.get("flow", [])
                if not isinstance(flow, list) or len(flow) == 0:
                    continue

                # Cria pasta do topico se nao existe
                topic_public.mkdir(parents=True, exist_ok=True)

                # Copia blueprint
                dest = topic_public / bp_file.name
                shutil.copy2(bp_file, dest)
                copied_blueprints += 1

            except:
                continue

        # Copia imagens (evitando duplicatas)
        images_copied_for_topic = 0
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            if images_copied_for_topic >= MAX_IMAGES_PER_TOPIC:
                break

            for img in sorted(topic_dir.glob(ext)):
                if images_copied_for_topic >= MAX_IMAGES_PER_TOPIC:
                    break

                try:
                    # Verifica duplicata por hash
                    file_hash = get_file_hash(img)
                    if file_hash in seen_hashes:
                        continue
                    seen_hashes.add(file_hash)

                    # Cria pasta do topico se nao existe
                    topic_public.mkdir(parents=True, exist_ok=True)

                    # Copia imagem
                    dest = topic_public / img.name
                    shutil.copy2(img, dest)
                    copied_images += 1
                    images_copied_for_topic += 1

                except:
                    continue

    print(f"\n{'='*50}")
    print(f"Copiados para {PUBLIC_PATH}:")
    print(f"  - {copied_blueprints} blueprints")
    print(f"  - {copied_images} imagens")
    print(f"{'='*50}")

    # Agora atualiza o inventario com os novos caminhos
    update_inventory()

def update_inventory():
    """Atualiza o inventario para usar os novos caminhos"""
    print("\nAtualizando inventario...")

    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        inventory = json.load(f)

    for wf in inventory['workflows']:
        folder = wf['folder']

        # Atualiza caminho do blueprint
        new_path = f"assets/workflows/{folder}/{wf['file']}"
        if Path(new_path).exists():
            wf['path'] = new_path

        # Atualiza caminhos das imagens
        new_images = []
        for img in wf.get('images', []):
            old_name = img['name']
            new_img_path = f"assets/workflows/{folder}/{old_name}"
            if Path(new_img_path).exists():
                new_images.append({
                    "path": new_img_path,
                    "name": old_name
                })

        wf['images'] = new_images
        wf['image_count'] = len(new_images)

        # Atualiza thumbnail
        if new_images:
            wf['thumbnail'] = new_images[0]['path']
        elif 'thumbnail' in wf:
            del wf['thumbnail']

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, ensure_ascii=False, indent=2)

    print("Inventario atualizado!")

if __name__ == "__main__":
    main()

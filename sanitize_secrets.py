#!/usr/bin/env python3
"""
Remove API keys e secrets dos blueprints
"""

import os
import re
import json
from pathlib import Path

ASSETS_PATH = Path("assets/workflows")

# Padroes de API keys para remover
SECRET_PATTERNS = [
    # Replicate API Token (r8_... ou Token r8_...)
    (r'r8_[a-zA-Z0-9]{20,}', 'REMOVED_API_KEY'),
    # Groq API Key (gsk_...)
    (r'gsk_[a-zA-Z0-9]{40,}', 'REMOVED_API_KEY'),
    # OpenAI API Key (sk-...)
    (r'sk-[a-zA-Z0-9]{30,}', 'REMOVED_API_KEY'),
    # Generic bearer tokens
    (r'Bearer [a-zA-Z0-9_\-]{30,}', 'Bearer REMOVED_API_KEY'),
    # Anthropic API Key (sk-ant-...)
    (r'sk-ant-[a-zA-Z0-9\-]{40,}', 'REMOVED_API_KEY'),
]

def sanitize_file(filepath):
    """Remove secrets de um arquivo JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        for pattern, replacement in SECRET_PATTERNS:
            content = re.sub(pattern, replacement, content)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error in {filepath}: {e}")
        return False

def main():
    sanitized = 0
    for json_file in ASSETS_PATH.glob("**/*.json"):
        if sanitize_file(json_file):
            print(f"Sanitized: {json_file}")
            sanitized += 1

    print(f"\nTotal sanitized: {sanitized} files")

if __name__ == "__main__":
    main()

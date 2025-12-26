"""
conversation_preserve_original_v1.py
Version: 1.0.0
Author: GitHub Copilot
Description: 
  Preserves the original conversation input as highly structured markdown for NotebookLM workflows. 
  Uses YAML config for all metadata, cell block structure, and signposts. 
  Outputs a markdown file with metadata and original content in a cell block, without any preprocessing.
"""

import argparse
import os
import sys
import yaml
from datetime import datetime


def load_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load config: {e}")
        sys.exit(1)

def read_input_file(input_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"[ERROR] Failed to read input file: {e}")
        sys.exit(1)

def write_output_file(output_path, content):
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"[ERROR] Failed to write output file: {e}")
        sys.exit(1)

def build_metadata_block(config, input_path):
    meta = config.get('preservation_metadata', {})
    meta_lines = ["---"]
    meta_lines.append(f"version: 1.0.0")
    meta_lines.append(f"script: conversation_preserve_original_v1.py")
    meta_lines.append(f"date: {datetime.now().isoformat()}")
    meta_lines.append(f"input_file: {os.path.basename(input_path)}")
    for k, v in meta.items():
        meta_lines.append(f"{k}: {v}")
    meta_lines.append("---\n")
    return '\n'.join(meta_lines)

def build_cell_block(config, content):
    cell_label = config.get('preservation_cell_label', 'cell')
    cell_delim = config.get('preservation_cell_delimiter', '```')
    cell_type = config.get('preservation_cell_type', 'markdown')
    block = []
    block.append(f"## {cell_label}: original_input")
    block.append(f"{cell_delim}{cell_type}")
    block.append(content.rstrip())
    block.append(f"{cell_delim}\n")
    return '\n'.join(block)

def main():
    parser = argparse.ArgumentParser(description="Preserve original conversation as structured markdown.")
    parser.add_argument('--input_file', required=True, help='Path to the input conversation file (e.g., .md, .txt)')
    parser.add_argument('--output_file', required=False, help='Path to output markdown file')
    parser.add_argument('--config_file', default='config/config.yaml', help='Path to YAML config file')
    args = parser.parse_args()

    config = load_config(args.config_file)
    content = read_input_file(args.input_file)

    metadata_block = build_metadata_block(config, args.input_file)
    cell_block = build_cell_block(config, content)

    output = f"{metadata_block}\n{cell_block}\n"

    output_path = args.output_file or os.path.splitext(args.input_file)[0] + '_preserved.md'
    write_output_file(output_path, output)
    print(f"[INFO] Original input preserved as structured markdown: {output_path}")

if __name__ == '__main__':
    main()

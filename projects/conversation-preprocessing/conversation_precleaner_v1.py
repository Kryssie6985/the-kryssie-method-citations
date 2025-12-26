"""
Script 1: Conversation Pre-Cleaner & Signpost Standardizer.

Version: 1.0.6
- Correctly uses explicit_preamble_ends_signpost AND
explicit_kryssie_turn_starts_signpost from config.yaml.
- Ensures these two distinct signposts are output when the preamble end marker is found.
"""

import re
import os
import argparse
import yaml
import traceback # For more detailed error logging if needed

__version__ = "1.0.6"
__author__ = "Kode_Animator (with A.C.E. assistance)"
__description__ = "Cleans raw logs & standardizes key markers, including explicit preamble end."

CONFIG = None

def load_config(config_path="config.yaml"):
    global CONFIG
    paths_to_try = [
        config_path,
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "config.yaml"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), config_path)
    ]
    loaded_successfully = False
    for path in paths_to_try:
        try:
            normalized_path = os.path.abspath(os.path.expanduser(path))
            if os.path.exists(normalized_path):
                with open(normalized_path, 'r', encoding='utf-8') as f:
                    CONFIG = yaml.safe_load(f)
                if CONFIG is not None and "pre_cleaner_settings" in CONFIG:
                    CONFIG['loaded_config_path'] = normalized_path
                    loaded_successfully = True
                    # print(f"DEBUG: Script 1 Config loaded from '{normalized_path}'")
                    return True
                else: CONFIG = None
        except FileNotFoundError: continue
        except yaml.YAMLError as e:
            print(f"Error parsing YAML '{normalized_path}': {e}"); CONFIG = None; return False
        except Exception as e:
            print(f"Error loading config '{normalized_path}': {e}"); CONFIG = None; return False
    if not loaded_successfully:
        print(f"Error: Could not load valid config for Script 1 from: {paths_to_try}"); CONFIG = {}
    return loaded_successfully

def get_config_value(keys, default=None):
    if CONFIG is None: return default
    temp_dict = CONFIG
    for key_part in keys:
        if isinstance(temp_dict, dict) and key_part in temp_dict: temp_dict = temp_dict[key_part]
        else: return default
    return temp_dict

# --- Core Logic ---
def clean_and_signpost_conversation(raw_text_lines):
    if not CONFIG or "pre_cleaner_settings" not in CONFIG:
        print("Error: Pre-cleaner settings not found in config. Aborting clean_and_signpost.")
        return raw_text_lines

    settings = CONFIG["pre_cleaner_settings"]
    preamble_marker_text_lc = settings.get("preamble_end_marker_text", "flowchartMind Map").lower()
    
    # Get the TWO distinct signposts from config
    explicit_preamble_ends_signpost = settings.get("explicit_preamble_ends_signpost", "%%PREAMBLE_ENDS_HERE%%")
    explicit_kryssie_starts_signpost = settings.get("explicit_kryssie_turn_starts_signpost", "%%KRYSSIE_TURN_STARTS_AFTER_PREAMBLE%%")

    ai_end_markers_lc = [m.lower() for m in settings.get("ai_end_turn_marker_strings", [])]
    ai_end_signpost = settings.get("standardized_ai_end_signpost", "%%AI_TURN_ENDED_KRYSSIE_NEXT%%")
    general_noise_lc = [n.lower() for n in settings.get("general_noise_lines_to_remove", [])]
    
    complex_noise_patterns_text = settings.get("complex_noise_patterns_to_remove", [])
    compiled_complex_noise = []
    for pattern_text in complex_noise_patterns_text:
        try: compiled_complex_noise.append(re.compile(pattern_text, re.IGNORECASE))
        except re.error as e: print(f"Warning: Invalid regex in config: '{pattern_text}'. Error: {e}")

    processed_lines = []
    preamble_marker_found_and_replaced = False

    for line in raw_text_lines:
        stripped_line_lower = line.strip().lower()

        if not preamble_marker_found_and_replaced and preamble_marker_text_lc in stripped_line_lower:
            processed_lines.append(explicit_preamble_ends_signpost) 
            processed_lines.append(explicit_kryssie_starts_signpost) 
            preamble_marker_found_and_replaced = True
            continue 

        is_ai_end_marker = False
        for ai_marker_pattern in ai_end_markers_lc:
            if ai_marker_pattern == stripped_line_lower:
                processed_lines.append(ai_end_signpost)
                is_ai_end_marker = True; break
        if is_ai_end_marker: continue

        is_general_noise = False
        for noise in general_noise_lc:
            if noise == stripped_line_lower:
                is_general_noise = True; break
        if is_general_noise: continue

        is_complex_noise = False
        for pattern_re in compiled_complex_noise:
            if pattern_re.search(stripped_line_lower):
                is_complex_noise = True; break
        if is_complex_noise: continue
            
        processed_lines.append(line)
    return processed_lines

# --- File Handling and Main Execution ---
def process_file(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as infile:
            raw_lines = [line.rstrip('\n\r') for line in infile.readlines()]
        processed_lines = clean_and_signpost_conversation(raw_lines)
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for line in processed_lines: outfile.write(line + '\n')
        print(f"Successfully pre-cleaned '{input_path}' -> '{output_path}'")
        # print(f"  Lines read: {len(raw_lines)}, Lines written: {len(processed_lines)}")
    except Exception as e:
        print(f"Error processing file '{input_path}': {e}"); traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description=__description__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("input_path", help="Path to raw log file or directory.")
    parser.add_argument("output_dir", help="Path to directory for pre-cleaned files.")
    parser.add_argument("--config_file", default="config.yaml", help="Path to YAML config.")
    parser.add_argument("--output_prefix", default="cleaned_", help="Prefix for output filenames.")
    parser.add_argument("--extensions", default=".txt,.md", help="File extensions to process.")
    args = parser.parse_args()

    if not load_config(args.config_file):
        print("Critical Error: Script 1 Could not load configuration. Exiting."); return
    if not CONFIG or "pre_cleaner_settings" not in CONFIG:
        print("Critical Error: Script 1 'pre_cleaner_settings' not found in config. Exiting."); return

    args.input_path = args.input_path.strip(); args.output_dir = args.output_dir.strip()
    # print(f"DEBUG: Pre-cleaner received input_path: '{args.input_path}'")
    # print(f"DEBUG: Pre-cleaner received output_dir: '{args.output_dir}'")
    # print(f"DEBUG: Pre-cleaner using config file: '{CONFIG.get('loaded_config_path', 'Not found')}'")

    if not os.path.exists(args.output_dir):
        try: os.makedirs(args.output_dir); print(f"Created output directory: '{os.path.abspath(args.output_dir)}'")
        except OSError as e: print(f"Error creating output directory '{args.output_dir}': {e}"); return

    allowed_extensions = [ext.strip().lower() for ext in args.extensions.split(',')]
    if os.path.isfile(args.input_path):
        output_file_path = os.path.join(args.output_dir, args.output_prefix + os.path.basename(args.input_path))
        process_file(args.input_path, output_file_path)
    elif os.path.isdir(args.input_path):
        abs_input_path = os.path.abspath(args.input_path)
        print(f"Processing files in directory: '{abs_input_path}'")
        if not os.path.isdir(abs_input_path): print(f"Error: Path '{abs_input_path}' not a dir."); return
        processed_count = 0
        for item_name in os.listdir(abs_input_path):
            item_path = os.path.join(abs_input_path, item_name)
            if os.path.isfile(item_path):
                _, file_ext = os.path.splitext(item_name)
                if file_ext.lower() in allowed_extensions:
                    output_file_path = os.path.join(args.output_dir, args.output_prefix + item_name)
                    process_file(item_path, output_file_path)
                    processed_count +=1
        if processed_count == 0: print(f"No files with specified extensions in '{abs_input_path}'.")
    else: print(f"Error: Input path '{args.input_path}' not valid.")

if __name__ == "__main__":
    main()

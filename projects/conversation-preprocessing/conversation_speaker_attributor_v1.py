"""
Script 2: Conversation Speaker Attributor.

Version: 1.0.5
- Correctly loads and uses the two distinct preamble signposts from
config.yaml (script2_signpost_settings) for more robust preamble handling.
- Preamble lines are collected until PREAMBLE_ENDS_MARKER.
- Kryssie's turn starts after KRYSSIE_STARTS_AFTER_PREAMBLE_MARKER.
"""

import re
import os
import argparse
import yaml 
import traceback

__version__ = "1.0.5"
__author__ = "Kode_Animator (with A.C.E. assistance)"
__description__ = "Attributes speakers to pre-cleaned and signposted conversation logs using config.yaml."

CONFIG = None
PREAMBLE_BLOCK_SPEAKER_KEY = "PREAMBLE_METADATA_BLOCK" 

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
                if CONFIG is not None and "script2_signpost_settings" in CONFIG and "speaker_definitions" in CONFIG:
                    CONFIG['loaded_config_path'] = normalized_path
                    loaded_successfully = True
                    return True
                else: CONFIG = None
        except FileNotFoundError: continue
        except yaml.YAMLError as e:
            print(f"Error parsing YAML '{normalized_path}': {e}"); CONFIG = None; return False
        except Exception as e:
            print(f"Error loading config '{normalized_path}': {e}"); CONFIG = None; return False
    if not loaded_successfully:
        print(f"Error: Could not load valid config from: {paths_to_try}"); CONFIG = {}
    return loaded_successfully

def get_config_value(keys, default=None):
    if CONFIG is None: return default
    temp_dict = CONFIG
    for key_part in keys: # Renamed key to key_part to avoid conflict with outer scope
        if isinstance(temp_dict, dict) and key_part in temp_dict: temp_dict = temp_dict[key_part]
        else: return default
    return temp_dict

# Constants to be populated from config
PREAMBLE_ENDS_MARKER = ""
KRYSSIE_STARTS_AFTER_PREAMBLE_MARKER = ""
AI_END_TURN_SIGNPOST_MARKER = "" # Renamed for clarity
SPEAKER_ALIAS_TO_FULL_ATTRIBUTION = {}
AI_PERSONA_HEURISTICS = {}
KRYSSIE_ATTRIBUTION = ""
DEFAULT_AI_ATTRIBUTION = ""

MARKDOWN_LEADING_PATTERNS_FOR_ID = [
    re.compile(r"^\s*#+\s*"), re.compile(r"^\s*-\s+"), re.compile(r"^\s*\*\s+"),
    re.compile(r"^\s*>\s*"), re.compile(r"^\s*\d+\.\s+"),
]

def populate_constants_from_config():
    global PREAMBLE_ENDS_MARKER, KRYSSIE_STARTS_AFTER_PREAMBLE_MARKER, AI_END_TURN_SIGNPOST_MARKER, \
        SPEAKER_ALIAS_TO_FULL_ATTRIBUTION, AI_PERSONA_HEURISTICS, \
        KRYSSIE_ATTRIBUTION, DEFAULT_AI_ATTRIBUTION

    # Use script2_signpost_settings from config.yaml v1.1
    PREAMBLE_ENDS_MARKER = get_config_value(["script2_signpost_settings", "preamble_ends_marker"], "%%PREAMBLE_ENDS_HERE%%")
    KRYSSIE_STARTS_AFTER_PREAMBLE_MARKER = get_config_value(["script2_signpost_settings", "kryssie_starts_after_preamble_marker"], "%%KRYSSIE_TURN_STARTS_AFTER_PREAMBLE%%")
    AI_END_TURN_SIGNPOST_MARKER = get_config_value(["script2_signpost_settings", "ai_turn_ended_kryssie_next_marker"], "%%AI_TURN_ENDED_KRYSSIE_NEXT%%")
    
    SPEAKER_ALIAS_TO_FULL_ATTRIBUTION = get_config_value(["speaker_definitions", "speaker_alias_to_full_attribution"], {})
    AI_PERSONA_HEURISTICS = get_config_value(["speaker_definitions", "ai_persona_heuristics"], {})
    kryssie_key = get_config_value(["speaker_definitions", "kryssie_attribution_key"], "Kryssie:")
    KRYSSIE_ATTRIBUTION = SPEAKER_ALIAS_TO_FULL_ATTRIBUTION.get(kryssie_key, "Kryssie (Kode_Animator):")
    default_ai_key = get_config_value(["speaker_definitions", "default_ai_attribution_key"], "CODY:")
    DEFAULT_AI_ATTRIBUTION = SPEAKER_ALIAS_TO_FULL_ATTRIBUTION.get(default_ai_key, "AI Persona (Unknown):")

    if not all([PREAMBLE_ENDS_MARKER, KRYSSIE_STARTS_AFTER_PREAMBLE_MARKER, AI_END_TURN_SIGNPOST_MARKER, SPEAKER_ALIAS_TO_FULL_ATTRIBUTION, KRYSSIE_ATTRIBUTION]):
        print("Warning: Some critical configuration values were not loaded correctly for Script 2.")

def get_signpost_from_config():
    pre_cleaner_settings = CONFIG.get('pre_cleaner_settings', {}) if CONFIG else {}
    preamble_end_signpost = pre_cleaner_settings.get('standardized_preamble_end_signpost', '%%END_PREAMBLE_KRYSSIE_STARTS%%')
    ai_end_turn_signpost = pre_cleaner_settings.get('standardized_ai_end_signpost', '%%AI_TURN_ENDED_KRYSSIE_NEXT%%')
    return preamble_end_signpost, ai_end_turn_signpost

def identify_ai_speaker(line_text, sorted_ai_aliases, full_ai_attributions_set, ai_heuristics_map):
    line_for_identification = line_text
    for md_pattern in MARKDOWN_LEADING_PATTERNS_FOR_ID:
        line_for_identification = md_pattern.sub("", line_for_identification)
    line_for_identification = line_for_identification.strip()
    if not line_for_identification: return None, line_text
    for full_attr in full_ai_attributions_set:
        if line_for_identification.startswith(full_attr):
            return full_attr, line_for_identification[len(full_attr):].lstrip()
    for alias_key in sorted_ai_aliases:
        if not isinstance(alias_key, str) or alias_key not in SPEAKER_ALIAS_TO_FULL_ATTRIBUTION: continue
        is_ai_alias = (alias_key in ai_heuristics_map or any(p_key in alias_key.upper() for p_key in SPEAKER_ALIAS_TO_FULL_ATTRIBUTION.keys() if SPEAKER_ALIAS_TO_FULL_ATTRIBUTION[p_key] != KRYSSIE_ATTRIBUTION))
        if not is_ai_alias: continue
        safe_alias_regex = re.escape(alias_key)
        match = re.match(r"^\s*" + safe_alias_regex + r"\s*(.*)", line_for_identification, re.IGNORECASE)
        if match:
            speech_after_alias = match.group(1).strip()
            full_attribution = SPEAKER_ALIAS_TO_FULL_ATTRIBUTION.get(alias_key)
            if full_attribution: return full_attribution, speech_after_alias
    for persona_simple_alias, patterns in ai_heuristics_map.items():
        if persona_simple_alias not in SPEAKER_ALIAS_TO_FULL_ATTRIBUTION: continue
        persona_full_attribution = SPEAKER_ALIAS_TO_FULL_ATTRIBUTION[persona_simple_alias]
        for pattern_text in patterns:
            if not isinstance(pattern_text, str): continue
            if line_for_identification.lower().startswith(pattern_text.lower()):
                return persona_full_attribution, line_text.strip()
    return None, line_text

def attribute_speakers_from_cleaned_log(cleaned_lines):
    preamble_end_signpost, ai_end_turn_signpost = get_signpost_from_config()
    attributed_blocks = []
    current_speaker = None
    current_block_lines = []
    
    processing_preamble = True 

    ai_aliases_map = {k: v for k, v in SPEAKER_ALIAS_TO_FULL_ATTRIBUTION.items() if v != KRYSSIE_ATTRIBUTION}
    sorted_ai_aliases = sorted(ai_aliases_map.keys(), key=len, reverse=True)
    full_ai_attributions_set = set(ai_aliases_map.values())

    for line_num, line_content in enumerate(cleaned_lines):
        stripped_line = line_content.strip()

        if processing_preamble:
            if stripped_line == preamble_end_signpost:
                # Preamble officially ends here. Finalize the collected preamble lines.
                if current_block_lines: # current_block_lines holds preamble here
                    attributed_blocks.append({"speaker": PREAMBLE_BLOCK_SPEAKER_KEY, "lines": list(current_block_lines)})
                current_block_lines = [] # Reset for next phase
                # The PREAMBLE_ENDS_MARKER itself is consumed, not part of any dialogue.
                # We are now waiting for KRYSSIE_STARTS_AFTER_PREAMBLE_MARKER
            elif stripped_line == KRYSSIE_STARTS_AFTER_PREAMBLE_MARKER:
                # This confirms preamble is done, and Kryssie's turn is next.
                processing_preamble = False # Exit preamble mode
                current_speaker = KRYSSIE_ATTRIBUTION
                current_block_lines = [] # Ready for Kryssie's first actual line
                # This marker is also consumed.
            else: # Still in preamble phase, collect the line
                current_block_lines.append(line_content)
            continue # Next line

        # --- Post-Preamble Processing (processing_preamble is False) ---
        if stripped_line == ai_end_turn_signpost: # Use the correctly loaded constant
            if current_block_lines and current_speaker:
                attributed_blocks.append({"speaker": current_speaker, "lines": list(current_block_lines)})
            current_speaker = KRYSSIE_ATTRIBUTION
            current_block_lines = []
            continue

        if not stripped_line: # Blank line
            if current_speaker: 
                current_block_lines.append(line_content)
            continue

        # Content line processing
        ai_speaker_identified, ai_speech_content = identify_ai_speaker(
            line_content, sorted_ai_aliases, full_ai_attributions_set, AI_PERSONA_HEURISTICS
        )

        if ai_speaker_identified:
            if current_speaker != ai_speaker_identified: 
                if current_block_lines and current_speaker:
                    attributed_blocks.append({"speaker": current_speaker, "lines": list(current_block_lines)})
                current_speaker = ai_speaker_identified
                current_block_lines = [ai_speech_content if ai_speech_content else line_content.strip()]
            else: 
                current_block_lines.append(ai_speech_content if ai_speech_content else line_content.strip())
        else: # Not an AI starting line
            if current_speaker == KRYSSIE_ATTRIBUTION: 
                current_block_lines.append(line_content)
            elif current_speaker: # An AI was speaking
                # This implies Kryssie's turn, but should have been AI_END_TURN_SIGNPOST_MARKER
                # For robustness, we'll switch to Kryssie here if AI was last.
                print(f"Warning: Assuming Kryssie turn after AI without explicit end signpost. Line: {line_content[:70].strip()}...")
                if current_block_lines and current_speaker:
                    attributed_blocks.append({"speaker": current_speaker, "lines": list(current_block_lines)})
                current_speaker = KRYSSIE_ATTRIBUTION
                current_block_lines = [line_content]
            elif not current_speaker : # Should be Kryssie if no speaker yet post-preamble
                current_speaker = KRYSSIE_ATTRIBUTION
                current_block_lines = [line_content]
    
    if current_block_lines and current_speaker:
        attributed_blocks.append({"speaker": current_speaker, "lines": list(current_block_lines)})
    return attributed_blocks

def format_output(attributed_blocks):
    output_lines = []
    for block in attributed_blocks:
        speaker, lines_in_block = block["speaker"], block["lines"]
        if not lines_in_block: continue
        if speaker == PREAMBLE_BLOCK_SPEAKER_KEY:
            output_lines.extend(lines_in_block)
            if lines_in_block and lines_in_block[-1].strip() != "": output_lines.append("")
            continue
        if not speaker:
            print(f"Warning: Block with no speaker: {lines_in_block[0][:50]}..."); output_lines.extend(lines_in_block)
            if lines_in_block and lines_in_block[-1].strip() != "": output_lines.append("")
            continue
        first_line_content = lines_in_block[0]
        output_lines.append(f"{speaker} {first_line_content.lstrip()}")
        for i in range(1, len(lines_in_block)): output_lines.append(f"    {lines_in_block[i]}")
        if output_lines and output_lines[-1].strip() != "": output_lines.append("")
    if output_lines and not output_lines[-1].strip(): output_lines.pop()
    return "\n".join(output_lines)

def process_attribution_file(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as infile:
            cleaned_lines = [line.rstrip('\n\r') for line in infile.readlines()]
        attributed_blocks = attribute_speakers_from_cleaned_log(cleaned_lines)
        final_output_text = format_output(attributed_blocks)
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.write(final_output_text)
        print(f"Successfully attributed speakers in '{input_path}' -> '{output_path}'")
    except Exception as e:
        print(f"Error processing file for attribution '{input_path}': {e}"); traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description=__description__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("input_path", help="Path to pre-cleaned log file or directory.")
    parser.add_argument("output_dir", help="Path to directory for attributed files.")
    parser.add_argument("--config_file", default="config.yaml", help="Path to YAML config.")
    parser.add_argument("--output_prefix", default="processed_", help="Prefix for output filenames.")
    parser.add_argument("--extensions", default=".txt,.md", help="File extensions to process.")
    args = parser.parse_args()

    if not load_config(args.config_file):
        print("Critical Error: Could not load configuration. Exiting."); return
    populate_constants_from_config()

    args.input_path = args.input_path.strip(); args.output_dir = args.output_dir.strip()
    print(f"DEBUG: Attributor received input_path: '{args.input_path}'")
    print(f"DEBUG: Attributor received output_dir: '{args.output_dir}'")
    print(f"DEBUG: Using config file: '{CONFIG.get('loaded_config_path', 'Not found')}'")
    print(f"DEBUG: PREAMBLE_ENDS_MARKER='{PREAMBLE_ENDS_MARKER}'")
    print(f"DEBUG: KRYSSIE_STARTS_AFTER_PREAMBLE_MARKER='{KRYSSIE_STARTS_AFTER_PREAMBLE_MARKER}'")


    if not os.path.exists(args.output_dir):
        try: os.makedirs(args.output_dir); print(f"Created output directory: '{os.path.abspath(args.output_dir)}'")
        except OSError as e: print(f"Error creating output directory '{args.output_dir}': {e}"); return

    allowed_extensions = [ext.strip().lower() for ext in args.extensions.split(',')]
    if os.path.isfile(args.input_path):
        name_part, file_ext_val = os.path.splitext(os.path.basename(args.input_path))
        output_file_path = os.path.join(args.output_dir, args.output_prefix + name_part + file_ext_val) 
        process_attribution_file(args.input_path, output_file_path)
    elif os.path.isdir(args.input_path):
        abs_input_path = os.path.abspath(args.input_path)
        print(f"Processing files in directory: '{abs_input_path}'")
        if not os.path.isdir(abs_input_path): print(f"Error: Path '{abs_input_path}' not a dir."); return
        processed_count = 0
        for item_name in os.listdir(abs_input_path):
            item_path = os.path.join(abs_input_path, item_name)
            if os.path.isfile(item_path):
                name_part, file_ext_val = os.path.splitext(item_name)
                if file_ext_val.lower() in allowed_extensions:
                    output_file_path = os.path.join(args.output_dir, args.output_prefix + name_part + file_ext_val)
                    process_attribution_file(item_path, output_file_path)
                    processed_count +=1
        if processed_count == 0: print(f"No files with specified extensions in '{abs_input_path}'.")
    else: print(f"Error: Input path '{args.input_path}' not valid.")

if __name__ == "__main__":
    main()

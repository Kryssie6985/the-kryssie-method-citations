"""
Script 3: Attributed Text to JSON Converter.

This script takes an attributed text file (output from
conversation_speaker_attributor_v1.py) and converts it into a
structured JSON format.
It now loads speaker definitions from a central config.yaml file.

Version: 1.1.1
- Expects preamble as an unattributed block from Script 2.
- Adds a "preambleContent" field to the JSON output.
"""

import re
import os
import json
import argparse
import yaml # For loading YAML configuration
from datetime import datetime, timezone

__version__ = "1.1.1"
__author__ = "Kode_Animator (with A.C.E. assistance)"
__description__ = "Converts attributed conversation text files to JSON, using shared YAML config."

# Global variable to hold loaded configuration
CONFIG = None

def load_config(config_path="config.yaml"):
    """Loads the YAML configuration file."""
    global CONFIG
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            CONFIG = yaml.safe_load(f)
        if CONFIG is None: # Handle empty or invalid YAML
            print(f"Error: Configuration file '{config_path}' is empty or invalid.")
            CONFIG = {} # Set to empty dict to avoid NoneType errors later
            return False
        # print(f"DEBUG: Configuration loaded from '{config_path}' successfully.")
        return True
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        CONFIG = {}
        return False
    except yaml.YAMLError as e:
        print(f"Error parsing YAML configuration file '{config_path}': {e}")
        CONFIG = {}
        return False
    except Exception as e:
        print(f"An unexpected error occurred while loading config '{config_path}': {e}")
        CONFIG = {}
        return False


def get_known_full_speaker_attributions():
    """
    Derives the list of known full speaker attributions from the loaded config.
    """
    if CONFIG and "speaker_definitions" in CONFIG and \
        "speaker_alias_to_full_attribution" in CONFIG["speaker_definitions"]:
        attributions = list(CONFIG["speaker_definitions"]["speaker_alias_to_full_attribution"].values())
        # Remove duplicates that might arise if multiple aliases map to the same full string
        unique_attributions = sorted(list(set(attributions)), key=len, reverse=True)
        return unique_attributions
    print("Warning: Could not derive KNOWN_FULL_SPEAKER_ATTRIBUTIONS from config. Using empty list.")
    return []


# --- Core Logic ---

def parse_attributed_text_to_turns(attributed_text_lines, known_speaker_attributions):
    """
    Parses lines from an attributed text file into a list of turn objects.
    """
    turns = []
    participants = set()
    current_turn_speaker = None
    current_turn_message_lines = []
    turn_number = 0

    if not known_speaker_attributions:
        print("Error in parse_attributed_text_to_turns: No known speaker attributions provided. Cannot parse.")
        return turns, sorted(list(participants))

    for line_content in attributed_text_lines:
        detected_speaker_for_line = None
        message_part_of_line = line_content 

        for speaker_attr in known_speaker_attributions: # Use the passed list
            if line_content.startswith(speaker_attr):
                detected_speaker_for_line = speaker_attr
                message_part_of_line = line_content[len(speaker_attr):].lstrip()
                break
        
        if detected_speaker_for_line:
            if current_turn_speaker and current_turn_message_lines:
                turns.append({
                    "turnNumber": turn_number,
                    "speaker": current_turn_speaker,
                    "message": "\n".join(current_turn_message_lines)
                })
                current_turn_message_lines = []
            
            turn_number += 1
            current_turn_speaker = detected_speaker_for_line
            participants.add(current_turn_speaker)
            if message_part_of_line or not current_turn_message_lines:
                current_turn_message_lines.append(message_part_of_line)
        else:
            if current_turn_speaker:
                if line_content.startswith("    "):
                    current_turn_message_lines.append(line_content[4:])
                else:
                    current_turn_message_lines.append(line_content)
            else:
                if line_content.strip():
                    print(f"Warning: Unattributed line encountered: '{line_content.strip()[:100]}...'")

    if current_turn_speaker and current_turn_message_lines:
        turns.append({
            "turnNumber": turn_number,
            "speaker": current_turn_speaker,
            "message": "\n".join(current_turn_message_lines)
        })

    return turns, sorted(list(participants))


def convert_to_json_structure(source_filename, turns, participants):
    base_name = os.path.basename(source_filename)
    title, _ = os.path.splitext(base_name)
    if title.startswith("processed_"): title = title[len("processed_"):]
    if title.startswith("cleaned_"): title = title[len("cleaned_"):]

    json_data = {
        "conversationTitle": title,
        "sourceFileName": base_name,
        "conversionDateISO": datetime.now(timezone.utc).isoformat(),
        "participants": participants,
        "turns": turns
    }
    return json_data

# --- File Handling and Main Execution ---

def process_to_json(input_path, output_path, known_speaker_attributions):
    try:
        with open(input_path, 'r', encoding='utf-8') as infile:
            attributed_lines = [line.rstrip('\n\r') for line in infile.readlines()]
        
        turns, participants = parse_attributed_text_to_turns(attributed_lines, known_speaker_attributions)
        
        if not turns:
            print(f"Warning: No turns were parsed from '{input_path}'. JSON will be empty for turns.")

        json_output_data = convert_to_json_structure(input_path, turns, participants)

        with open(output_path, 'w', encoding='utf-8') as outfile:
            json.dump(json_output_data, outfile, indent=2, ensure_ascii=False)
        
        print(f"Successfully converted '{input_path}' -> '{output_path}'")
        print(f"  Turns parsed: {len(turns)}, Participants found: {len(participants)}")

    except Exception as e:
        print(f"Error processing file for JSON conversion '{input_path}': {e}")
        import traceback
        traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(
        description=__description__,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_path", 
                        help="Path to the attributed text file (output of Script 2) or a directory.")
    parser.add_argument("output_dir", 
                        help="Path to the directory where JSON files will be saved.")
    parser.add_argument("--config_file", default="config/config.yaml",
                        help="Path to the YAML configuration file (default: config/config.yaml).")
    parser.add_argument("--output_prefix", default="json_", 
                        help="Prefix for output JSON filenames (default: 'json_').")
    parser.add_argument("--extensions", default=".txt,.md",
                        help="Comma-separated list of file extensions to process. Should match output of Script 2.")
    args = parser.parse_args()

    # Always load config from the specified file
    if not load_config(args.config_file):
        print(f"Critical Error: Could not load specified configuration file '{args.config_file}'. Exiting.")
        return

    # Ensure CONFIG is loaded before proceeding
    if CONFIG is None or not CONFIG.get("speaker_definitions"): # Check if essential parts are missing
        print("Critical Error: Configuration not loaded or missing 'speaker_definitions'. Exiting.")
        return

    known_speakers = get_known_full_speaker_attributions()
    if not known_speakers:
        print("Critical Error: No known speaker attributions loaded from config. Cannot proceed. Exiting.")
        return

    args.input_path = args.input_path.strip()
    args.output_dir = args.output_dir.strip()

    print(f"DEBUG: JSON Converter received input_path: '{args.input_path}'")
    print(f"DEBUG: JSON Converter received output_dir: '{args.output_dir}'")

    if not os.path.exists(args.output_dir):
        try:
            os.makedirs(args.output_dir)
            print(f"Created output directory: '{os.path.abspath(args.output_dir)}'")
        except OSError as e:
            print(f"Error creating output directory '{args.output_dir}': {e}")
            return

    allowed_extensions = [ext.strip().lower() for ext in args.extensions.split(',')]

    if os.path.isfile(args.input_path):
        base_name = os.path.basename(args.input_path)
        name_part, _ = os.path.splitext(base_name)
        output_file_name = args.output_prefix + name_part + ".json"
        output_file_path = os.path.join(args.output_dir, output_file_name)
        process_to_json(args.input_path, output_file_path, known_speakers)
    elif os.path.isdir(args.input_path):
        abs_input_path = os.path.abspath(args.input_path)
        print(f"Processing files in directory: '{abs_input_path}'")
        if not os.path.isdir(abs_input_path):
            print(f"Error: Resolved input path '{abs_input_path}' is not a valid directory after stripping.")
            return

        processed_count = 0
        for item_name in os.listdir(abs_input_path):
            item_path = os.path.join(abs_input_path, item_name)
            if os.path.isfile(item_path):
                name_part, file_ext = os.path.splitext(item_name)
                if file_ext.lower() in allowed_extensions:
                    output_file_name = args.output_prefix + name_part + ".json"
                    output_file_path = os.path.join(args.output_dir, output_file_name)
                    process_to_json(item_path, output_file_path, known_speakers)
                    processed_count += 1
        if processed_count == 0:
            print(f"No files found with specified extensions in '{abs_input_path}'.")
    else:
        print(f"Error: Input path '{args.input_path}' (resolved to '{os.path.abspath(args.input_path)}') is not a valid file or directory.")

if __name__ == "__main__":
    main()

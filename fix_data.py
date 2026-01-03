import json
import os
import glob
import re

def extract_json_objects(text):
    """
    Generator that parses a string containing multiple JSON objects,
    handling standard lists, concatenated objects, and comma-separated objects.
    """
    decoder = json.JSONDecoder()
    pos = 0
    length = len(text)
    
    while pos < length:
        # 1. Skip whitespace immediately
        while pos < length and text[pos].isspace():
            pos += 1
        
        if pos >= length:
            break
            
        # 2. Check for "garbage" characters often found in messy files
        # We assume the file might be a loose list like [{...}, {...}] 
        # or concatenated like {...}{...} or comma separated {...}, {...}
        if text[pos] in [',', '[', ']']:
            pos += 1
            continue
            
        # 3. Attempt to decode exactly one JSON object
        try:
            # raw_decode returns the object and the index where the object ended
            obj, next_pos = decoder.raw_decode(text, pos)
            yield obj
            pos = next_pos
        except json.JSONDecodeError:
            # If we hit an error, we might be looking at a stray character.
            # We advance by one to try and find the start of the next valid object.
            # This is a brute-force recovery method.
            pos += 1

def fix_jsonl_file(filepath):
    print(f"Checking {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pre-processing: Handle literal string newlines if they were dumped incorrectly
    # Only do this if you suspect the file has literal "\n" characters text instead of actual newlines
    # content = content.replace('\\n', '\n') 

    valid_lines = []
    
    # Use the stream extractor
    for entry in extract_json_objects(content):
        # Dump it back to a clean, one-line string
        valid_lines.append(json.dumps(entry))
        
    if valid_lines:
        print(f"  -> Found {len(valid_lines)} valid JSON objects. Rewriting...")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(valid_lines) + '\n')
        print("  ✅ File repaired.")
    else:
        print("  ⚠️ No valid JSON objects found. File might be empty or too corrupted.")

def main():
    # Look for all .jsonl files in ./data
    files = glob.glob("./data/*.jsonl")
    if not files:
        print("No .jsonl files found in ./data")
        return

    for file in files:
        fix_jsonl_file(file)

if __name__ == "__main__":
    main()
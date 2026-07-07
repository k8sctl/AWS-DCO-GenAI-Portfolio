import os
import glob
import re

def get_log_level(line):
    tokens = line.split()
    for i, token in enumerate(tokens):
        if re.match(r'^server\d+$', token, re.IGNORECASE):
            if i + 1 < len(tokens):
                return tokens[i+1].upper()
    return None

def parse_log_entries(file_path):
    entries = []
    current_entry = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith(" ") or line.startswith("\t"):
                if current_entry:
                    current_entry.append(line)
            else:
                if current_entry:
                    entries.append(current_entry)
                current_entry = [line]
        if current_entry:
            entries.append(current_entry)
            
    parsed_entries = []
    for entry_lines in entries:
        main_line = entry_lines[0]
        full_content = "".join(entry_lines)
        parsed_entries.append({
            "main_line": main_line,
            "full_content": full_content
        })
    return parsed_entries

def analyze_logs():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_files = sorted(glob.glob(os.path.join(script_dir, "server*.log")))
    
    if not log_files:
        log_files = sorted(glob.glob("server*.log"))
        
    print("=" * 95)
    print(f"{'Server Log Analysis Results (Ignoring Case & Multi-line Friendly)':^95}")
    print("=" * 95)
    print(f"{'Log File':<15} | {'CRC Error (Substrings)':<22} | {'CRC Error (Actual ERRORs)':<25} | {'Link Down (Substrings)':<22} | {'Link Down (Actual ERRORs)':<25}")
    print("-" * 95)
    
    for file_path in log_files:
        file_name = os.path.basename(file_path)
        
        crc_sub = 0
        crc_err = 0
        link_sub = 0
        link_err = 0
        
        entries = parse_log_entries(file_path)
        
        for entry in entries:
            content_lower = entry["full_content"].lower()
            
            level = get_log_level(entry["main_line"])
            if level:
                is_error = (level == "ERROR")
            else:
                is_error = "error" in entry["main_line"].lower()
            
            # Check for CRC error (case-insensitive)
            if "crc error" in content_lower:
                crc_sub += 1
                if is_error:
                    crc_err += 1
            
            # Check for Link Down (case-insensitive)
            if "link down" in content_lower:
                link_sub += 1
                if is_error:
                    link_err += 1
                    
        print(f"{file_name:<15} | {crc_sub:<22} | {crc_err:<25} | {link_sub:<22} | {link_err:<25}")
        
    print("=" * 95)
    print("Note:")
    print(" - 'Substrings' counts all occurrences of 'crc error' or 'link down' (case-insensitive)")
    print("   where multiple lines in a single log entry are grouped and counted as one.")
    print(" - 'Actual ERRORs' only counts those entries that are marked with the 'ERROR' log level.")
    print("=" * 95)

if __name__ == "__main__":
    analyze_logs()

import os
import glob

def analyze_logs():
    log_dir = r"D:\AWS-DCO-GenAI-Portfolio\07_log_analysis_script2"
    log_files = sorted(glob.glob(os.path.join(log_dir, "server*.log")))
    
    print("=" * 95)
    print(f"{'Server Log Analysis Results':^95}")
    print("=" * 95)
    print(f"{'Log File':<15} | {'CRC Error (Substrings)':<22} | {'CRC Error (Actual ERRORs)':<25} | {'Link Down (Substrings)':<22} | {'Link Down (Actual ERRORs)':<25}")
    print("-" * 95)
    
    for file_path in log_files:
        file_name = os.path.basename(file_path)
        
        crc_sub = 0
        crc_err = 0
        link_sub = 0
        link_err = 0
        
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_lower = line.lower()
                is_error = " ERROR " in line
                
                # Check for CRC error (case-insensitive)
                if "crc error" in line_lower:
                    crc_sub += 1
                    if is_error:
                        crc_err += 1
                
                # Check for Link Down (case-insensitive)
                if "link down" in line_lower:
                    link_sub += 1
                    if is_error:
                        link_err += 1
                        
        print(f"{file_name:<15} | {crc_sub:<22} | {crc_err:<25} | {link_sub:<22} | {link_err:<25}")
        
    print("=" * 95)
    print("Note:")
    print(" - 'Substrings' counts all occurrences of the phrase 'crc error' or 'link down' regardless of log level.")
    print(" - 'Actual ERRORs' only counts lines with the log level 'ERROR' indicating a real failure event.")
    print("=" * 95)

if __name__ == "__main__":
    analyze_logs()
